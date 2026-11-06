"""RQ2 online link (H2c): does a GT's assignment geometry predict whether it is detected?

Inputs
- AI-TOD-R test labels (DOTA format) and the per-GT table written by ``rq2_offline.py`` on
  the *test* split (same GT filtering: side >= 2 px, clipped to the image).
- One prediction folder per run, DOTA Task1 format as written by ``c11_pipeline.predict_and_eval``
  (``save_dota_dir``). Two layouts are accepted:
    * per class:  ``Task1_<class>.txt`` with lines ``<stem> <score> x1 y1 x2 y2 x3 y3 x4 y4``;
    * per image:  ``<stem>.txt`` with lines ``x1 y1 ... y4 <class> <score>``.

Per GT and run: ``detected`` = matched by a same-class prediction with rotated IoU >= 0.5 under
greedy score-ordered matching (COCO style, 1,500 predictions kept per (image, class) as in
AITODReval), predictions with score >= ``--score`` only.

Outputs (``--out``)
- ``recall_per_gt.csv.gz``: GT x run table with ``detected`` and the offline geometry columns;
- ``recall_summary.json``: recall by arm x size bin x A0-starvation group (seed-averaged and per seed),
  the paired change vs A0 on the same GTs, and a logistic model
  ``detected ~ arm * starved_A0 + log(short) + log1p(nn16) + C(cls)`` with scene-clustered SEs.

Usage
    python rq2_recall.py --labels <test labels> --offline <rq2_test>/rq2_per_gt.csv.gz \
        --run A0:1:<runs>/c11_A0_s1/dota_e2e --run A2:1:<runs>/c11_A2_s1/dota_e2e ... --out <dir>
"""

from __future__ import annotations

import argparse
import gzip
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from shapely.geometry import Polygon

import geometry as g

MAX_PER_IMG_CLASS = 1500


def read_predictions(folder: Path, keep: set[str]) -> dict:
    """Return {(stem, cls_idx): (scores[N], polys[N,8])}."""
    preds = defaultdict(list)
    task1 = list(folder.glob("Task1_*.txt"))
    if task1:
        for f in task1:
            name = f.stem[len("Task1_") :]
            if name not in g.CLASSES:
                continue
            c = g.CLASSES.index(name)
            for line in f.read_text().splitlines():
                p = line.split()
                if len(p) >= 10 and p[0] in keep:
                    preds[(p[0], c)].append((float(p[1]), [float(x) for x in p[2:10]]))
    else:
        for f in folder.glob("*.txt"):
            if f.stem not in keep:
                continue
            for line in f.read_text().splitlines():
                p = line.split()
                if len(p) >= 10 and p[8] in g.CLASSES:
                    preds[(f.stem, g.CLASSES.index(p[8]))].append((float(p[9]), [float(x) for x in p[:8]]))
    out = {}
    for k, v in preds.items():
        v.sort(key=lambda t: -t[0])
        v = v[:MAX_PER_IMG_CLASS]
        out[k] = (np.array([s for s, _ in v]), np.array([q for _, q in v]))
    return out


def score_floor(folder: Path) -> dict:
    """Lowest score and box count in a prediction folder of either layout, to check the confidence it was saved at."""
    folder = Path(folder)
    task1 = list(folder.glob("Task1_*.txt"))
    files, col = (task1, 1) if task1 else (list(folder.glob("*.txt")), 9)
    low, n = np.inf, 0
    for f in files:
        for line in f.read_text().splitlines():
            p = line.split()
            if len(p) >= 10:
                low, n = min(low, float(p[col])), n + 1
    return dict(layout="task1" if task1 else "per_image", n_files=len(files), n_boxes=n,
                min_score=float(low) if n else None)


def gt_polys(path: Path):
    """GT polygons after the same filtering as geometry.read_dota_label, rebuilt from xywhr."""
    boxes, cls = g.read_dota_label(path)
    polys = [np.array(g.corners(*b)).reshape(-1) for b in boxes]
    return polys, cls


def rotated_iou(p: np.ndarray, q: np.ndarray) -> float:
    a, b = Polygon(p.reshape(4, 2)), Polygon(q.reshape(4, 2))
    if not a.is_valid or not b.is_valid:
        a, b = a.buffer(0), b.buffer(0)
    inter = a.intersection(b).area
    union = a.area + b.area - inter
    return inter / union if union > 0 else 0.0


def match_image(gpolys, gcls, preds_img: dict, iou_thr: float, score_thr: float) -> np.ndarray:
    det = np.zeros(len(gpolys), dtype=bool)
    for c in np.unique(gcls):
        gi = np.where(gcls == c)[0]
        if c not in preds_img:
            continue
        scores, polys = preds_img[c]
        gcent = np.array([gpolys[i].reshape(4, 2).mean(0) for i in gi])
        grad = np.array([np.linalg.norm(gpolys[i].reshape(4, 2) - gcent[k], axis=1).max() for k, i in enumerate(gi)])
        for s, q in zip(scores, polys):
            if s < score_thr:
                break
            qp = q.reshape(4, 2)
            qc = qp.mean(0)
            qrad = np.linalg.norm(qp - qc, axis=1).max()
            near = np.where((np.linalg.norm(gcent - qc, axis=1) <= grad + qrad) & ~det[gi])[0]
            best, bi = iou_thr, -1
            for j in near:
                iou = rotated_iou(gpolys[gi[j]], q)
                if iou >= best:
                    best, bi = iou, j
            if bi >= 0:
                det[gi[bi]] = True
    return det


def detect_run(labels: Path, stems: list[str], pred_dir: Path, iou_thr: float, score_thr: float):
    preds = read_predictions(pred_dir, set(stems))
    by_img = defaultdict(dict)
    for (stem, c), v in preds.items():
        by_img[stem][c] = v
    rows = []
    for stem in stems:
        gp, gc = gt_polys(labels / f"{stem}.txt")
        det = match_image(gp, gc, by_img.get(stem, {}), iou_thr, score_thr) if len(gp) else []
        rows += [(stem, i, bool(d)) for i, d in enumerate(det)]
    return pd.DataFrame(rows, columns=["stem", "gt", "detected"])


def summarize(df: pd.DataFrame) -> dict:
    df = df.copy()
    df["starved_A0"] = df["A0_cand"] == 0
    out = {}
    per_seed = df.groupby(["arm", "seed", "bin", "starved_A0"]).detected.mean().rename("recall").reset_index()
    out["recall_per_seed"] = per_seed.to_dict("records")
    mean = per_seed.groupby(["arm", "bin", "starved_A0"]).recall.agg(["mean", "std", "count"]).reset_index()
    out["recall_mean_over_seeds"] = mean.to_dict("records")
    if "A0" in set(df.arm):
        base = df[df.arm == "A0"].groupby(["stem", "gt"]).detected.mean().rename("r0")
        paired = []
        for arm in sorted(set(df.arm) - {"A0"}):
            x = df[df.arm == arm].groupby(["stem", "gt"]).detected.mean().rename("r1")
            j = pd.concat([base, x], axis=1, join="inner").join(
                df.drop_duplicates(["stem", "gt"]).set_index(["stem", "gt"])[["bin", "starved_A0"]]
            )
            for (b, s), sub in j.groupby(["bin", "starved_A0"]):
                paired.append(dict(arm=arm, bin=b, starved_A0=bool(s), n=len(sub), d_recall=float((sub.r1 - sub.r0).mean())))
        out["paired_delta_vs_A0"] = paired
    try:
        import statsmodels.formula.api as smf

        d = df[df.bin.isin(["vt", "t"])].copy()
        d["y"] = d.detected.astype(int)
        d["log_short"] = np.log(d["short"])
        d["log_nn16"] = np.log1p(d["nn16"])
        d["starved"] = d["starved_A0"].astype(int)
        m = smf.logit("y ~ C(arm, Treatment('A0')) * starved + log_short + log_nn16 + C(cls)", data=d)
        groups = pd.factorize(d["scene"])[0]
        r = m.fit(disp=0, cov_type="cluster", cov_kwds={"groups": groups})
        out["logit_vt_t"] = dict(
            n=int(r.nobs),
            params={k: float(v) for k, v in r.params.items()},
            se_cluster_scene={k: float(v) for k, v in r.bse.items()},
            pvalues={k: float(v) for k, v in r.pvalues.items()},
            note="exploratory unless pre-registered; SEs clustered by scene, seeds pooled",
        )
    except Exception as e:  # noqa: BLE001
        out["logit_vt_t"] = {"error": repr(e)}
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--labels", required=True, type=Path)
    ap.add_argument("--offline", required=True, type=Path, help="rq2_per_gt.csv.gz of the test split")
    ap.add_argument("--run", action="append", required=True, help="ARM:SEED:PRED_DIR")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--iou", type=float, default=0.5)
    ap.add_argument("--score", type=float, default=0.05)
    args = ap.parse_args()
    off = pd.read_csv(args.offline)
    stems = sorted(off.stem.unique())
    frames = []
    for spec in args.run:
        arm, seed, folder = spec.split(":", 2)
        r = detect_run(args.labels, stems, Path(folder), args.iou, args.score)
        r["arm"], r["seed"] = arm, int(seed)
        frames.append(r)
        print(arm, seed, "recall@IoU%.2f score>=%.2f = %.4f" % (args.iou, args.score, r.detected.mean()))
    det = pd.concat(frames).merge(off, on=["stem", "gt"], how="left")
    args.out.mkdir(parents=True, exist_ok=True)
    with gzip.open(args.out / "recall_per_gt.csv.gz", "wt") as fh:
        det.to_csv(fh, index=False)
    summ = summarize(det)
    summ["_meta"] = dict(iou=args.iou, score=args.score, runs=args.run, n_images=len(stems))
    (args.out / "recall_summary.json").write_text(json.dumps(summ, indent=2, default=str))
    print("->", args.out)


if __name__ == "__main__":
    main()
