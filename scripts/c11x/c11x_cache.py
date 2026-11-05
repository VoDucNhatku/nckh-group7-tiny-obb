"""Đưa `evalcache_<head>.npz` về cùng thứ tự ảnh, để bootstrap theo cảnh ghép đúng ảnh giữa các run.

Chép từ ô #17 của `notebooks/C11x_analysis_colab.ipynb` (commit f7b30f7): cache nms của 8/12 run có thứ tự ảnh khác cache
e2e. Bản gốc được giữ thành `.unsorted.npz`.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import numpy as np

SUFFIXES = {"sc", "tp", "fp", "off", "npig", "present"}


def _is_group_key(k: str) -> bool:
    return k[:1] == "k" and "_a" in k


def reorder_cache(c: dict, ref: np.ndarray) -> dict:
    """Trả về bản sao của cache `c` theo thứ tự ảnh `ref`. Mỗi nhóm (lớp, bin) có mảng dự đoán chia theo ảnh bằng `off`."""
    pos = {s: i for i, s in enumerate(c["stems"].tolist())}
    perm = np.array([pos[s] for s in ref.tolist()])
    out = {k: v for k, v in c.items() if not _is_group_key(k)}
    out["stems"] = ref.copy()
    for g in sorted({k.rsplit("_", 1)[0] for k in c if _is_group_key(k)}):
        if {k.rsplit("_", 1)[1] for k in c if k.startswith(g + "_")} != SUFFIXES:
            raise ValueError(f"nhóm {g} thiếu trường")
        off, n = c[g + "_off"], len(c[g + "_sc"])
        if not (len(off) == len(ref) + 1 and off[0] == 0 and off[-1] == n and (np.diff(off) >= 0).all()):
            raise ValueError(f"nhóm {g}: off không hợp lệ")
        idx = np.concatenate([np.arange(off[p], off[p + 1]) for p in perm]) if n else np.zeros(0, dtype=int)
        out[g + "_sc"] = c[g + "_sc"][idx]
        out[g + "_tp"] = c[g + "_tp"][:, idx]
        out[g + "_fp"] = c[g + "_fp"][:, idx]
        out[g + "_off"] = np.concatenate([[0], np.cumsum(np.diff(off)[perm])]).astype(off.dtype)
        out[g + "_npig"] = c[g + "_npig"][perm]
        out[g + "_present"] = c[g + "_present"][perm]
    return out


def align_caches(run_dirs, ref_file) -> list[str]:
    """Sắp lại mọi cache e2e và nms trong `run_dirs` theo `ref_file`. Trả về tên file đã sửa."""
    with np.load(ref_file, allow_pickle=False) as z:
        ref = np.asarray(z["stems"])
    changed = []
    for rd in run_dirs:
        for head in ("e2e", "nms"):
            f = Path(rd) / f"evalcache_{head}.npz"
            if not f.exists():
                continue
            with np.load(f, allow_pickle=False) as z:
                c = {k: z[k] for k in z.files}
            if np.array_equal(c["stems"], ref):
                continue
            if set(c["stems"].tolist()) != set(ref.tolist()):
                raise ValueError(f"{f}: tập ảnh khác cache tham chiếu")
            bak = f.with_name(f"evalcache_{head}.unsorted.npz")
            if not bak.exists():
                shutil.copy2(f, bak)
            tmp = f.with_name(f"evalcache_{head}.tmp.npz")
            np.savez(tmp, **reorder_cache(c, ref))
            tmp.replace(f)
            changed.append(f"{Path(rd).name}/{f.name}")
    return changed
