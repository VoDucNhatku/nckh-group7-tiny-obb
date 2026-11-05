"""Label-only geometry of YOLO-OBB candidate selection on AI-TOD-R.

Reproduces, without torch, the candidate step of Ultralytics 8.4.174
``RotatedTaskAlignedAssigner.select_candidates_in_gts`` for the C-11 arms:

- anchor centres at ((i + 0.5) * s, (j + 0.5) * s) for s in {8, 16, 32}
  (``make_anchors(..., grid_cell_offset=0.5)`` scaled by ``stride_tensor``);
- floor rule per arm: every side (w and h separately) below ``threshold`` is
  set to ``floor`` before the point-in-rotated-box test;
- inclusive point-in-box test on the rectangle corners, as in Ultralytics.

Training recipe of C-11: imgsz 800 on 800x800 crops, no mosaic/scale/translate,
only horizontal/vertical flips. 800 is divisible by 32, so flips map the anchor
lattice onto itself and these counts are exact for every training sample.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

STRIDES = (8, 16, 32)
IMG_SIZE = 800
CLASSES = ("airplane", "bridge", "storage-tank", "ship", "swimming-pool", "vehicle", "person", "wind-mill")
SQRT2_8 = 8 * math.sqrt(2)


@dataclass(frozen=True)
class Arm:
    name: str
    threshold: float  # sides strictly below this are floored
    floor: float  # replacement side length


ARMS = {
    "A0": Arm("A0", 0.0, 0.0),  # TAL, no floor (Ultralytics <= 8.4.7)
    "A1": Arm("A1", 8.0, 16.0),  # STAL as published: side < 8 -> 16
    "A8": Arm("A8", SQRT2_8, SQRT2_8),  # coverage-minimal floor: side < 8*sqrt(2) -> 8*sqrt(2)
    "A2": Arm("A2", 16.0, 16.0),  # STAL in Ultralytics >= 8.4.128: side < 16 -> 16
}

XVIEW_RE = re.compile(r"^\d+__\d+_\d+$")
DOTA_RE = re.compile(r"^(P\d+)__")
VISDRONE_RE = re.compile(r"^(\d{7}_\d{5}_d_\d{7})__")


def is_xview(stem: str) -> bool:
    """AI-TOD xView crops are named ``<tile>__<x>_<y>``; 4,639 trainval / 4,667 test files (Gate 0)."""
    return bool(XVIEW_RE.match(stem))


def scene_key(stem: str) -> str:
    """Group crops cut from one source image (xView tile, DOTA image, VisDrone frame); other sources: one image."""
    if is_xview(stem):
        return "xview:" + stem.split("__")[0]
    m = DOTA_RE.match(stem)
    if m:
        return "dota:" + m.group(1)
    m = VISDRONE_RE.match(stem)
    if m:
        return "visdrone:" + m.group(1)
    return "img:" + stem


def read_dota_label(path: Path, min_side: float = 2.0, clip: bool = True):
    """Return (xywhr[N,5], cls[N]) in pixels; drops GTs whose rotated side < ``min_side`` (official loader rule)."""
    boxes, cls = [], []
    for line in Path(path).read_text().splitlines():
        p = line.split()
        if len(p) < 9 or p[8] not in CLASSES:
            continue
        pts = np.array(p[:8], dtype=np.float32).reshape(4, 2)
        if clip:
            pts = np.clip(pts, 0, IMG_SIZE)
        (cx, cy), (w, h), ang = cv2.minAreaRect(pts)
        if min(w, h) < min_side:
            continue
        theta = ang / 180 * np.pi
        if w < h:
            w, h, theta = h, w, theta + np.pi / 2
        boxes.append((cx, cy, w, h, theta))
        cls.append(CLASSES.index(p[8]))
    return np.asarray(boxes, dtype=np.float64).reshape(-1, 5), np.asarray(cls, dtype=np.int64)


def floor_sides(wh: np.ndarray, arm: Arm) -> np.ndarray:
    out = wh.copy()
    if arm.threshold > 0:
        out[out < arm.threshold] = arm.floor
    return out


def corners(cx, cy, w, h, theta):
    """Corner order of Ultralytics ``xywhr2xyxyxyxy``: ctr + v1 + v2, ctr + v1 - v2, ctr - v1 - v2, ctr - v1 + v2."""
    c, s = math.cos(theta), math.sin(theta)
    v1 = np.array([w / 2 * c, w / 2 * s])
    v2 = np.array([-h / 2 * s, h / 2 * c])
    ctr = np.array([cx, cy])
    return ctr + v1 + v2, ctr + v1 - v2, ctr - v1 - v2, ctr - v1 + v2


def candidates_one(box, arm: Arm, strides=STRIDES, img=IMG_SIZE):
    """Anchor ids inside the floored region of one box. Id = (level, row, col) packed into one int."""
    cx, cy, w, h, theta = box
    w, h = floor_sides(np.array([w, h]), arm)
    a, b, _, d = corners(cx, cy, w, h, theta)
    ab, ad = b - a, d - a
    nab, nad = ab @ ab, ad @ ad
    r = 0.5 * math.hypot(w, h)
    ids = []
    for li, s in enumerate(strides):
        n = img // s
        i0, i1 = max(0, int((cx - r) / s - 0.5)), min(n - 1, int((cx + r) / s + 0.5))
        j0, j1 = max(0, int((cy - r) / s - 0.5)), min(n - 1, int((cy + r) / s + 0.5))
        if i1 < i0 or j1 < j0:
            continue
        xs = (np.arange(i0, i1 + 1) + 0.5) * s
        ys = (np.arange(j0, j1 + 1) + 0.5) * s
        gx, gy = np.meshgrid(xs, ys)
        px, py = gx.ravel() - a[0], gy.ravel() - a[1]
        dab = px * ab[0] + py * ab[1]
        dad = px * ad[0] + py * ad[1]
        m = (dab >= 0) & (dab <= nab) & (dad >= 0) & (dad <= nad)
        if m.any():
            col = (gx.ravel()[m] / s - 0.5).round().astype(np.int64)
            row = (gy.ravel()[m] / s - 0.5).round().astype(np.int64)
            ids.append(li * 10_000_000 + row * 10_000 + col)
    return np.concatenate(ids) if ids else np.empty(0, dtype=np.int64)


def level_of(anchor_id: np.ndarray) -> np.ndarray:
    return anchor_id // 10_000_000


def anchor_xy(anchor_id: np.ndarray, strides=STRIDES) -> np.ndarray:
    lvl = level_of(anchor_id)
    rem = anchor_id % 10_000_000
    s = np.asarray(strides)[lvl]
    return np.stack([((rem % 10_000) + 0.5) * s, ((rem // 10_000) + 0.5) * s], axis=-1)


def size_bin(w: float, h: float) -> str:
    """AI-TOD area bins on sqrt(area): very tiny <8, tiny 8-16, small 16-32, medium 32-64 (AITODReval)."""
    a = math.sqrt(w * h)
    return "vt" if a < 8 else "t" if a < 16 else "s" if a < 32 else "m" if a < 64 else "l"
