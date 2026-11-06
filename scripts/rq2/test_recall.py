"""Synthetic end-to-end check of rq2_recall matching and summary."""

import numpy as np
import pandas as pd

import geometry as g
import rq2_offline as ro
import rq2_recall as rr


def _write_label(path, boxes, cls):
    lines = []
    for b, c in zip(boxes, cls):
        pts = np.array(g.corners(*b)).reshape(-1)
        lines.append(" ".join(f"{v:.2f}" for v in pts) + f" {c} 0")
    path.write_text("\n".join(lines) + "\n")


def test_recall_pipeline(tmp_path):
    rng = np.random.default_rng(0)
    lab = tmp_path / "labels"
    lab.mkdir()
    for k in range(6):
        n = 20
        boxes = np.stack([rng.uniform(50, 750, n), rng.uniform(50, 750, n), rng.uniform(4, 30, n), rng.uniform(3, 12, n), rng.uniform(0, 3, n)], 1)
        _write_label(lab / f"P{k:04d}__1.0__0___0.txt", boxes, ["vehicle"] * n)
    rows = [r for f in sorted(lab.glob("*.txt")) for r in ro.analyze_file(str(f))]
    off = pd.DataFrame(rows)
    off_path = tmp_path / "off.csv.gz"
    off.to_csv(off_path, index=False)
    runs = {}
    for arm, keep in (("A0", 0.5), ("A2", 1.0)):
        d = tmp_path / arm
        d.mkdir()
        lines = []
        for f in sorted(lab.glob("*.txt")):
            polys, _ = rr.gt_polys(f)
            for p in polys:
                if rng.random() < keep:
                    lines.append(f"{f.stem} 0.9 " + " ".join(f"{v:.2f}" for v in p))
        (d / "Task1_vehicle.txt").write_text("\n".join(lines) + "\n")
        runs[arm] = rr.detect_run(lab, sorted(off.stem.unique()), d, 0.5, 0.05)
    assert runs["A2"].detected.all()
    assert 0.3 < runs["A0"].detected.mean() < 0.7
    frames = []
    for arm, r in runs.items():
        r["arm"], r["seed"] = arm, 1
        frames.append(r)
    det = pd.concat(frames).merge(off, on=["stem", "gt"], how="left")
    s = rr.summarize(det)
    assert s["paired_delta_vs_A0"] and all(x["d_recall"] >= 0 for x in s["paired_delta_vs_A0"])


def test_score_floor_reads_both_layouts(tmp_path):
    pts = "10 10 20 10 20 20 10 20"
    t1, per = tmp_path / "t1", tmp_path / "per"
    t1.mkdir(), per.mkdir()
    (t1 / "Task1_vehicle.txt").write_text(f"a 0.9 {pts}\nb 0.012 {pts}\n")
    (per / "a.txt").write_text(f"{pts} vehicle 0.3\n{pts} ship 0.07\n")
    assert rr.score_floor(t1) == dict(layout="task1", n_files=1, n_boxes=2, min_score=0.012)
    assert rr.score_floor(per)["min_score"] == 0.07
    assert rr.score_floor(tmp_path / "missing")["n_boxes"] == 0
