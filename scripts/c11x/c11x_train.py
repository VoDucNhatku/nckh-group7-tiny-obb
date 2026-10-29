"""Train một run YOLO26n-OBB với quy tắc vùng ứng viên của c11x_assign, tự resume, ghi file done.

Giữ giao thức C11: cùng recipe (`RECIPE_C11`, chép từ `pilot.json` mà ô #21 của `C11_colab.ipynb` in ra), cùng khởi
tạo từ `yolo26n.pt` (COCO), ultralytics 8.4.174. Thư mục run: `<project>/c11x_<arm>_s<seed>/`.

Mỗi run ghi:
- `c11x_arm.json`: arm, quy tắc, seed, recipe, phiên bản (viết trước khi train; resume kiểm lại khớp);
- `c11x_kstats.jsonl`: với arm K, theo epoch: số GT giữ hộp gốc / phải nới tới từng mức sàn, số GT vẫn thiếu;
- `c11x_done.json`: viết khi train xong 24 epoch.
Callback báo lỗi nếu bản vá không được gọi trong một epoch.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import c11x_assign as ca

# In ra ở ô #21 của C11_colab.ipynb (commit 58e2805), mục "recipe" trong pilot.json.
RECIPE_C11 = {
    "imgsz": 800, "epochs": 24, "batch": 16, "optimizer": "SGD", "lr0": 0.01, "momentum": 0.937,
    "weight_decay": 0.0005, "warmup_epochs": 1.0, "cos_lr": False, "close_mosaic": 0, "mosaic": 0.0,
    "mixup": 0.0, "copy_paste": 0.0, "degrees": 0.0, "translate": 0.0, "scale": 0.0, "shear": 0.0,
    "perspective": 0.0, "hsv_h": 0.0, "hsv_s": 0.0, "hsv_v": 0.0, "fliplr": 0.5, "flipud": 0.5, "max_det": 300,
    "amp": True, "deterministic": True, "workers": 8, "plots": False, "save_period": 1, "exist_ok": True,
}
MODEL_CFG = "yolo26n-obb.yaml"
INIT_WEIGHTS = "yolo26n.pt"  # trọng số COCO detection; không dùng trọng số DOTA (tránh rò rỉ, proposal §8.1)


def run_name(arm: str, seed: int) -> str:
    return f"c11x_{arm}_s{seed}"


def check_recipe(other: dict) -> list[str]:
    """So RECIPE_C11 với `c11_pipeline.RECIPE` trên Drive. Trả về danh sách khoá lệch (rỗng = khớp)."""
    keys = set(RECIPE_C11) | set(other)
    return sorted(k for k in keys if RECIPE_C11.get(k) != other.get(k))


def _versions() -> dict:
    import platform

    import numpy
    import torch
    import ultralytics

    return dict(ultralytics=ultralytics.__version__, torch=torch.__version__, numpy=numpy.__version__,
                python=platform.python_version(),
                gpu=torch.cuda.get_device_name(0) if torch.cuda.is_available() else None)


def epochs_logged(rd: Path) -> int:
    """Số epoch đã ghi trong results.csv của Ultralytics (0 nếu chưa có)."""
    f = rd / "results.csv"
    if not f.exists():
        return 0
    return max(sum(1 for ln in f.read_text().splitlines() if ln.strip()) - 1, 0)


def train_arm(data_yaml, arm: str, seed: int, project, recipe: dict | None = None, device=0,
              init_weights: str | None = INIT_WEIGHTS, extra_callbacks: dict | None = None) -> Path:
    """Train (hoặc resume) một run. Trả về thư mục run. Bỏ qua nếu đã có `c11x_done.json`.

    `init_weights=None` và `extra_callbacks` chỉ dùng cho test (khởi tạo ngẫu nhiên; giả lập Colab ngắt giữa chừng).
    """
    from ultralytics import YOLO

    recipe = dict(recipe or RECIPE_C11)
    rd = Path(project) / run_name(arm, seed)
    if (rd / "c11x_done.json").exists():
        return rd
    rule = ca.apply_arm(arm)
    meta = dict(arm=arm, rule=rule, seed=seed, recipe=recipe, model=MODEL_CFG, init=INIT_WEIGHTS, **_versions())
    meta_f = rd / "c11x_arm.json"
    last = rd / "weights" / "last.pt"
    if meta_f.exists():
        old = json.loads(meta_f.read_text())
        assert (old["arm"], old["seed"]) == (arm, seed), f"thư mục {rd} thuộc run khác: {old['arm']}, {old['seed']}"
    else:
        rd.mkdir(parents=True, exist_ok=True)
        meta_f.write_text(json.dumps(meta, indent=2, default=str))

    state = {"calls_at_epoch_start": 0}

    def on_epoch_start(trainer):
        state["calls_at_epoch_start"] = ca.STATE["calls"]

    def on_epoch_end(trainer):
        if ca.STATE["calls"] == state["calls_at_epoch_start"]:
            raise RuntimeError(f"bản vá {arm} không được gọi trong epoch {trainer.epoch + 1}: quy tắc không có hiệu lực")
        ks = ca.pop_kstats()
        if ks is not None:
            with open(rd / "c11x_kstats.jsonl", "a") as fh:
                fh.write(json.dumps(dict(epoch=trainer.epoch + 1, **ks)) + "\n")

    t0 = time.time()
    try:
        if last.exists() and epochs_logged(rd) >= recipe["epochs"]:
            # Đã train đủ nhưng phiên trước bị ngắt trước khi ghi file done: không resume (Ultralytics sẽ báo lỗi).
            batch_actual = None
        else:
            if last.exists():
                model = YOLO(str(last))
            else:
                model = YOLO(MODEL_CFG)
                if init_weights:
                    model = model.load(init_weights)
            model.add_callback("on_train_epoch_start", on_epoch_start)
            model.add_callback("on_train_epoch_end", on_epoch_end)
            for event, fn in (extra_callbacks or {}).items():
                model.add_callback(event, fn)
            if last.exists():
                model.train(resume=True)
            else:
                model.train(data=str(data_yaml), seed=seed, project=str(Path(project)), name=rd.name,
                            device=device, **recipe)
            tr = model.trainer
            assert Path(tr.save_dir).resolve() == rd.resolve(), f"Ultralytics ghi ra {tr.save_dir}, không phải {rd}"
            batch_actual = int(tr.batch_size)
        n_ep = epochs_logged(rd)
        assert n_ep >= recipe["epochs"], f"{rd.name}: results.csv mới có {n_ep}/{recipe['epochs']} epoch"
        done = dict(arm=arm, seed=seed, epochs=n_ep, batch_actual=batch_actual,
                    batch_changed=None if batch_actual is None else batch_actual != int(recipe["batch"]),
                    hours_this_session=(time.time() - t0) / 3600, **_versions())
        (rd / "c11x_done.json").write_text(json.dumps(done, indent=2))
    finally:
        ca.remove_patch()
    return rd


# ---------------------------------------------------------------- ước lượng thời gian và CU sau epoch đầu

# Tốc độ tiêu CU của A100 trên Colab không có trên trang giá chính thức mà tôi đọc được; các nguồn bên thứ ba
# (2023–2026) ghi từ khoảng 5,4 đến khoảng 15 CU/giờ. Đọc đúng tốc độ ở Colab (biểu tượng RAM/Disk → tài nguyên)
# rồi sửa CU_PER_HOUR trong notebook. [ước lượng]
CU_PER_HOUR_DEFAULT = 5.4
EVAL_S_PER_RUN_HEAD = 337.0  # chấm một run, một head, đường nhanh: C11_colab.ipynb #29
BOOT_S_PER_HEAD_B10K = 5700.0  # 570 s cho B = 1.000 ở #34, giả định tăng tuyến tính [ước lượng]


def estimate(epoch_s: float, epochs_left: int, n_eval: int, n_boot_heads: int = 2,
             cu_per_hour: float = CU_PER_HOUR_DEFAULT) -> dict:
    """Giờ còn lại = train (epoch_s × số epoch còn) + chấm (n_eval lần) + bootstrap. CU = giờ × cu_per_hour."""
    train_h = epoch_s * epochs_left / 3600
    eval_h = n_eval * EVAL_S_PER_RUN_HEAD / 3600
    boot_h = n_boot_heads * BOOT_S_PER_HEAD_B10K / 3600
    total = train_h + eval_h + boot_h
    return dict(train_h=train_h, eval_h=eval_h, boot_h=boot_h, total_h=total, cu=total * cu_per_hour,
                cu_per_hour=cu_per_hour)


class EtaPrinter:
    """Callback in ước lượng **một lần** mỗi phiên, sau epoch đầu tiên chạy trong phiên (tính cả val).

    `epochs_left_fn()` trả về tổng số epoch còn phải train của mọi run trong hàng đợi, đọc lúc in.
    """

    def __init__(self, epochs_left_fn, n_eval: int, cu_per_hour: float = CU_PER_HOUR_DEFAULT):
        self.epochs_left_fn, self.n_eval, self.cu_per_hour = epochs_left_fn, n_eval, cu_per_hour
        self.t_start = None
        self.printed = False

    def on_train_epoch_start(self, trainer):
        if not self.printed:
            self.t_start = time.time()

    def on_fit_epoch_end(self, trainer):
        if self.printed or self.t_start is None:
            return
        dt = time.time() - self.t_start
        left = self.epochs_left_fn()  # results.csv đã có epoch vừa xong (save_metrics chạy trước on_fit_epoch_end)
        e = estimate(dt, left, self.n_eval, cu_per_hour=self.cu_per_hour)
        print(f"\n[ETA] 1 epoch (train + val) = {dt:.0f} s. Còn khoảng {left} epoch → train {e['train_h']:.1f} giờ, "
              f"chấm {e['eval_h']:.1f} giờ, bootstrap {e['boot_h']:.1f} giờ. Tổng ≈ {e['total_h']:.1f} giờ A100 "
              f"≈ {e['cu']:.0f} CU (ở {self.cu_per_hour} CU/giờ; kiểm tốc độ thật trong Colab).\n", flush=True)
        self.printed = True

    def callbacks(self) -> dict:
        return {"on_train_epoch_start": self.on_train_epoch_start, "on_fit_epoch_end": self.on_fit_epoch_end}
