"""What happens to each GT that is not detected? (GT-centred error fate, oriented boxes.)

Inspired by the error types of TIDE (Bolya et al., ECCV 2020) but GT-centred and using rotated IoU; it does not
compute TIDE's delta-AP. It answers: after a floor gives a tiny GT a positive, is it still missed outright, found
but badly localised, given the wrong class, or taken by a neighbour's prediction?

Fate of one GT, for predictions with score >= ``score`` (first rule that applies):
- ``detected``: greedy score-ordered same-class match at IoU >= ``iou_fg`` (same matching as ``rq2_recall``);
- ``lost_to_neighbour``: a same-class prediction reaches IoU >= ``iou_fg`` but was matched to another GT;
- ``cls``: a prediction of another class reaches IoU >= ``iou_fg``;
- ``loc``: the best same-class prediction has ``iou_bg`` <= IoU < ``iou_fg``;
- ``both``: the best prediction of another class has ``iou_bg`` <= IoU < ``iou_fg``;
- ``miss``: no prediction reaches IoU >= ``iou_bg``.

Also returns detection at several IoU thresholds, for a recall-versus-IoU curve per size bin.

Usage
    python rq2_errors.py --labels <test labels> --offline <rq2_test>/rq2_per_gt.csv.gz \
        --run A0:4:<runs>/c11x_A0_s4/dota_e2e ... --score 0.25 --out <dir>
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

import rq2_recall as rr

FATES = ("detected", "lost_to_neighbour", "cls", "loc", "both", "miss")
IOU_CURVE = (0.1, 0.25, 0.5, 0.75)


def best_ious(gpolys, gcls, preds_img: dict, score_thr: float):
    """Best same-class and best other-class IoU per GT, among predictions with score >= score_thr."""
    n = len(gpolys)
    same, other = np.zeros(n), np.zeros(n)
    polys, cls = [], []
    for c, (scores, q) in preds_img.items():
        keep = scores >= score_thr
        if keep.any():
            polys.append(q[keep])
            cls.append(np.full(int(keep.sum()), c))
    if not polys or n == 0:
        return same, other
    polys, cls = np.concatenate(polys), np.concatenate(cls)
    pc = polys.reshape(-1, 4, 2).mean(1)
    pr = np.linalg.norm(polys.reshape(-1, 4, 2) - pc[:, None], axis=2).max(1)
    for i, g in enumerate(gpolys):
        gp = g.reshape(4, 2)
        gc = gp.mean(0)
        gr = np.linalg.norm(gp - gc, axis=1).max()
        for j in np.where(np.linalg.norm(pc - gc, axis=1) <= gr + pr)[0]:
            v = rr.rotated_iou(g, polys[j])
            if cls[j] == gcls[i]:
                same[i] = max(same[i], v)
            else:
                other[i] = max(other[i], v)
    return same, other


def fate_of(detected: bool, same: float, other: float, iou_fg: float, iou_bg: float) -> str:
    if detected:
        return "detected"
    if same >= iou_fg:
        return "lost_to_neighbour"
    if other >= iou_fg:
        return "cls"
    if same >= iou_bg:
        return "loc"
    if other >= iou_bg:
        return "both"
    return "miss"


def fates_image(gpolys, gcls, preds_img: dict, score_thr: float, iou_fg=0.5, iou_bg=0.1, curve=IOU_CURVE) -> dict:
    gcls = np.asarray(gcls)
    det = {t: rr.match_image(gpolys, gcls, preds_img, t, score_thr) for t in curve}
    if iou_fg not in det:
        det[iou_fg] = rr.match_image(gpolys, gcls, preds_img, iou_fg, score_thr)
    same, other = best_ious(gpolys, gcls, preds_img, score_thr)
    fates = [fate_of(bool(d), s, o, iou_fg, iou_bg) for d, s, o in zip(det[iou_fg], same, other)]
    out = {"fate": fates, "best_same": same, "best_other": other}
    out.update({f"det_{t:g}": det[t] for t in curve})
    return out


def fates_run(labels: Path, stems: list[str], pred_dir: Path, score_thr: float, **kw) -> pd.DataFrame:
    preds = rr.read_predictions(Path(pred_dir), set(stems))
    if not preds:
        raise ValueError(f"no predictions read from {pred_dir}: check its layout (see rq2_recall.read_predictions)")
    by_img = defaultdict(dict)
    for (stem, c), v in preds.items():
        by_img[stem][c] = v
    frames = []
    for stem in stems:
        gp, gc = rr.gt_polys(Path(labels) / f"{stem}.txt")
        if not len(gp):
            continue
        r = fates_image(gp, gc, by_img.get(stem, {}), score_thr, **kw)
        r.update(stem=stem, gt=np.arange(len(gp)))
        frames.append(pd.DataFrame(r))
    return pd.concat(frames, ignore_index=True)


def density_bin(nn16) -> pd.Series:
    return pd.cut(pd.Series(nn16), [-1, 0, 2, np.inf], labels=["isolated", "1-2", ">=3"]).astype(str)


def fate_table(df: pd.DataFrame, by=("arm", "bin")) -> pd.DataFrame:
    """Share of each fate per group and seed, then mean and sd over seeds."""
    keys = [*by, "seed"]
    share = df.groupby(keys + ["fate"], observed=True).size().unstack("fate", fill_value=0)
    for f in FATES:
        if f not in share:
            share[f] = 0
    n = share[list(FATES)].sum(axis=1)
    share = share[list(FATES)].div(n, axis=0).assign(n=n)
    return share.groupby(list(by), observed=True).agg(["mean", "std"])


def recall_curve(df: pd.DataFrame, by=("arm", "bin"), curve=IOU_CURVE) -> pd.DataFrame:
    cols = [f"det_{t:g}" for t in curve]
    return df.groupby([*by, "seed"], observed=True)[cols].mean().groupby(list(by), observed=True).agg(["mean", "std"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--labels", required=True, type=Path)
    ap.add_argument("--offline", required=True, type=Path)
    ap.add_argument("--run", action="append", required=True, help="ARM:SEED:PRED_DIR")
    ap.add_argument("--score", type=float, default=0.25)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    off = pd.read_csv(args.offline)
    stems = sorted(off.stem.unique())
    args.out.mkdir(parents=True, exist_ok=True)
    frames = []
    for spec in args.run:
        arm, seed, folder = spec.split(":", 2)
        r = fates_run(args.labels, stems, Path(folder), args.score).assign(arm=arm, seed=int(seed))
        frames.append(r)
        print(arm, seed, r.fate.value_counts(normalize=True).round(3).to_dict(), flush=True)
    df = pd.concat(frames).merge(off, on=["stem", "gt"], how="left")
    df["density"] = density_bin(df["nn16"]).values
    df["starved_A0"] = df["A0_cand"] == 0
    df.to_csv(args.out / f"fates_score{args.score:g}.csv.gz", index=False)
    fate_table(df).to_csv(args.out / f"fate_by_arm_bin_score{args.score:g}.csv")
    recall_curve(df).to_csv(args.out / f"recall_iou_by_arm_bin_score{args.score:g}.csv")
    (args.out / "meta.json").write_text(json.dumps(dict(score=args.score, runs=args.run), indent=2))


if __name__ == "__main__":
    main()
