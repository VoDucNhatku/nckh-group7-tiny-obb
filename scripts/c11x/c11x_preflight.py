"""Kiểm tra trước khi train (chạy vài giây): GPU, phiên bản, code C11 trên Drive, dữ liệu, run cũ, dung lượng.

Mục đích: lỗi lộ ra ở ô đầu notebook, không phải sau nhiều giờ. Mọi kiểm tra đều chạy hết rồi báo một lần.
"""

from __future__ import annotations

import importlib
import importlib.util
import inspect
import shutil
import sys
from pathlib import Path

ULTRALYTICS_VERSION = "8.4.174"
OLD_ARMS, OLD_SEEDS = ("A0", "A1", "A8", "A2"), (1, 2, 3)
IMAGE_ZIPS = ("aitod_wo_xview_trainval_imgs.zip", "aitod_wo_xview_test_imgs.zip")
# Thuộc tính của scripts/c11 mà notebook C11x gọi, kèm tham số từ khoá phải có (theo cách C11_colab.ipynb gọi).
C11_API = {
    "aitodr_data": {"xview_stems": (), "build_yolo_dataset": ("version", "exclude_xview", "val_frac", "seed"),
                    "scene_key": ()},
    "aitodr_evalkit": {"load_official_evaluator": ()},
    "c11_pipeline": {"RECIPE": None, "predict_and_eval": ("head", "version", "exclude_stems", "save_dota_dir")},
    "c11_bootstrap": {"load_cache": (), "multi_pair_bootstrap": ("keys", "B", "engine")},
}


class PreflightError(RuntimeError):
    """Notebook dừng ngay, kèm danh sách mọi lỗi."""


def check_gpu(require="A100") -> list[str]:
    import torch

    if not torch.cuda.is_available():
        return ["Không có GPU. Colab: Runtime → Change runtime type → A100 GPU."]
    name = torch.cuda.get_device_name(0)
    return [] if require in name else [f"GPU là {name}, không phải {require}. Giao thức C11 dùng A100; đổi runtime."]


def check_versions() -> list[str]:
    errs = []
    try:
        import ultralytics

        if ultralytics.__version__ != ULTRALYTICS_VERSION:
            errs.append(f"ultralytics {ultralytics.__version__} ≠ {ULTRALYTICS_VERSION}. Chạy lại ô cài đặt.")
    except ImportError:
        errs.append("Chưa cài ultralytics. Chạy lại ô cài đặt.")
    for mod in ("shapely", "statsmodels", "pandas", "scipy"):
        if importlib.util.find_spec(mod) is None:
            errs.append(f"Thiếu thư viện {mod}.")
    return errs


def check_c11_code(code_dir: Path) -> list[str]:
    """Code C11 trên Drive có đủ file, import được, có đúng hàm và tham số mà notebook C11x gọi."""
    code_dir = Path(code_dir)
    if not code_dir.is_dir():
        return [f"Không thấy code C11 ở {code_dir} (scripts/c11 trên Drive)."]
    errs = []
    if str(code_dir) not in sys.path:
        sys.path.insert(0, str(code_dir))
    for mod_name, attrs in C11_API.items():
        if not (code_dir / f"{mod_name}.py").exists():
            errs.append(f"Thiếu {mod_name}.py trong {code_dir}.")
            continue
        try:
            mod = importlib.import_module(mod_name)
        except Exception as e:  # noqa: BLE001 — báo mọi lỗi import
            errs.append(f"Không import được {mod_name}: {type(e).__name__}: {e}")
            continue
        for attr, kwargs in attrs.items():
            if not hasattr(mod, attr):
                errs.append(f"{mod_name} không có {attr}.")
                continue
            if kwargs:
                params = inspect.signature(getattr(mod, attr)).parameters
                has_var_kw = any(p.kind is inspect.Parameter.VAR_KEYWORD for p in params.values())
                missing = [k for k in kwargs if k not in params and not has_var_kw]
                if missing:
                    errs.append(f"{mod_name}.{attr} thiếu tham số {missing}.")
    return errs


def check_data(data_drive: Path, local_images: Path) -> list[str]:
    data_drive = Path(data_drive)
    errs = []
    lab = data_drive / "labels.zip"
    if not lab.exists():
        errs.append(f"Thiếu {lab}. Make a copy file nhãn AI-TOD-R vào thư mục này.")
    elif open(lab, "rb").read(2) != b"PK":
        errs.append(f"{lab} không phải file zip (có thể là trang HTML báo hết hạn mức tải).")
    for z in IMAGE_ZIPS:
        if not (data_drive / z).exists() and not (Path(local_images) / f"{z}.done").exists():
            errs.append(f"Thiếu {data_drive / z}.")
    return errs


def check_old_runs(runs_old: Path, exp_drive: Path) -> tuple[list[str], list[str]]:
    """12 run C11 (cần cho cổng H2 và R0) và split_manifest ngày 20/10. Trả về (lỗi, cảnh báo)."""
    errs, warns = [], []
    for a in OLD_ARMS:
        for s in OLD_SEEDS:
            rd = Path(runs_old) / f"c11_{a}_s{s}"
            if not (rd / "c11_done.json").exists() or not (rd / "weights" / "last.pt").exists():
                errs.append(f"Thiếu run cũ {rd.name} (c11_done.json hoặc weights/last.pt).")
    if not (Path(runs_old) / "c11_A2_s1" / "results.csv").exists():
        warns.append("c11_A2_s1/results.csv không có: R0 chỉ so được AP test, không so được đường val theo epoch.")
    if not list(Path(exp_drive).glob("*-dataset-woX/split_manifest.json")):
        errs.append("Thiếu experiments/*-dataset-woX/split_manifest.json (để kiểm split giống ngày 20/10).")
    return errs, warns


def check_space(path: Path, need_gb: float, what: str) -> list[str]:
    try:
        free = shutil.disk_usage(path).free / 1e9
    except OSError:
        return [f"Không đọc được dung lượng trống của {what} ({path})."]
    return [] if free >= need_gb else [f"{what} còn {free:.1f} GB, cần ≥ {need_gb} GB."]


def run_all(*, code_dir, data_drive, local, runs_old, exp_drive, prereg, drive, need_drive_gb=15,
            need_local_gb=40, require_gpu="A100") -> list[str]:
    """Chạy mọi kiểm tra. Ném PreflightError nếu có lỗi; trả về danh sách cảnh báo."""
    errs = []
    errs += check_gpu(require_gpu)
    errs += check_versions()
    if not Path(drive).is_dir():
        errs.append(f"Chưa mount Drive hoặc thiếu thư mục {drive}.")
    if not Path(prereg).exists() or "PREREG-C11X-v1" not in Path(prereg).read_text(encoding="utf-8"):
        errs.append("Không thấy experiments/preregistration.md (PREREG-C11X-v1) trên nhánh đã clone.")
    errs += check_c11_code(code_dir)
    errs += check_data(data_drive, Path(local) / "images_raw")
    e, warns = check_old_runs(runs_old, exp_drive)
    errs += e
    errs += check_space(drive, need_drive_gb, "Drive")
    Path(local).mkdir(parents=True, exist_ok=True)
    errs += check_space(local, need_local_gb, "Đĩa VM")
    if errs:
        raise PreflightError("Dừng trước khi chạy:\n- " + "\n- ".join(errs))
    return warns
