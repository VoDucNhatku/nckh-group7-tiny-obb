"""Predict one image folder with a saved checkpoint and write per-image DOTA-style text files for rq2_errors.

Line format, one file per image (``<stem>.txt``), read by ``rq2_recall.read_predictions``:
    x1 y1 x2 y2 x3 y3 x4 y4 <class name> <score>

Head switch as in ``c11x_pergt.predict_and_match``: ``e2e`` uses nms=False, ``nms`` uses the library default.
Images go to the model in groups of ``chunk``, because Ultralytics batches a whole list of paths at once and a
longer list ran out of GPU memory in the analysis notebook (cell #24).
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import geometry as g


def _numpy(x) -> np.ndarray:
    return x.cpu().numpy() if hasattr(x, "cpu") else np.asarray(x)


def result_lines(res, names: dict) -> list[str]:
    ob = res.obb
    if ob is None or len(ob) == 0:
        return []
    polys = _numpy(ob.xyxyxyxy).reshape(-1, 8)
    cls = _numpy(ob.cls).astype(int)
    conf = _numpy(ob.conf)
    return [" ".join(f"{v:.2f}" for v in p) + f" {names[int(c)]} {s:.6f}" for p, c, s in zip(polys, cls, conf)]


def predict_to_dota(weights, images_dir, out_dir, head: str, conf=0.05, imgsz=800, max_det=12000, chunk=32, device=0,
                    model=None) -> dict:
    """Write predictions unless ``_done.json`` exists; return its content."""
    if head not in ("e2e", "nms"):
        raise ValueError(f"unknown head {head!r}")
    out_dir = Path(out_dir)
    done = out_dir / "_done.json"
    if done.exists():
        return json.loads(done.read_text())
    if model is None:
        from ultralytics import YOLO

        model = YOLO(str(weights))
    names = dict(model.names)
    unknown = sorted(set(names.values()) - set(g.CLASSES))
    if unknown:
        raise ValueError(f"model classes not in geometry.CLASSES: {unknown}")
    files = sorted(p for p in Path(images_dir).iterdir() if p.suffix.lower() in (".png", ".jpg", ".jpeg"))
    if not files:
        raise ValueError(f"no images in {images_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)
    n_box, t0 = 0, time.time()
    for i in range(0, len(files), chunk):
        src = [str(p) for p in files[i:i + chunk]]
        for res in model.predict(src, imgsz=imgsz, conf=conf, max_det=max_det, nms=False if head == "e2e" else None,
                                 batch=chunk, device=device, stream=True, verbose=False):
            lines = result_lines(res, names)
            n_box += len(lines)
            (out_dir / f"{Path(res.path).stem}.txt").write_text("\n".join(lines) + ("\n" if lines else ""))
    info = dict(n_images=len(files), n_boxes=n_box, head=head, conf=conf, seconds=round(time.time() - t0, 1))
    done.write_text(json.dumps(info))
    return info
