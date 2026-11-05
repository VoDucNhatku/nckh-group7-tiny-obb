"""RQ2 offline: where do tiny oriented GTs lose their candidates / positives? (labels only)

For every GT and every arm (A0, A1, A8, A2) this records the stages of YOLO-OBB
label assignment that can be computed from labels alone:

1. candidates   -- anchors inside the floored region (exact, matches Ultralytics 8.4.174);
2. top-k        -- YOLO26-OBB uses top-k = 10 for the one-to-many branch and top-k = 7 then
                   top-k2 = 1 for the one-to-one branch (``E2ELoss(model, v8OBBLoss)``);
3. conflicts    -- an anchor selected by several GTs is kept by the GT with the highest
                   predicted-box ProbIoU.

Stages 2-3 depend on predictions, so they are reported as a **label-only proxy**: the
alignment metric is replaced by distance from the anchor to the GT centre (closer = better).
Two exact bounds bracket the proxy: ``zero_cand`` (lower bound on GTs with no positive) and
``all_shared`` (GT whose every candidate is also a candidate of another GT; such a GT *can*
lose all positives, the upper bound). Online logs (``c11_assign_diag.jsonl``) remain the
measurement; this script fixes predictions *before* looking at them.

Usage:
    python rq2_offline.py --labels <AI-TOD-R>/labels/trainval --out <dir> [--protocol woX|full]
"""

from __future__ import annotations

import argparse
import gzip
import json
import time
from collections import defaultdict
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd

import geometry as g

TOPK_O2M = 10
TOPK_O2O = 7


def _assign_proxy(cands: list[np.ndarray], centres: np.ndarray, topk: int, topk2: int | None):
    """Label-only proxy of TAL top-k + highest-overlap conflict rule. Returns positives per GT."""
    n = len(cands)
    sel = []
    for i, c in enumerate(cands):
        if len(c) > topk:
            d = np.linalg.norm(g.anchor_xy(c) - centres[i], axis=1)
            c = c[np.argsort(d, kind="stable")[:topk]]
        sel.append(c)
    owners = defaultdict(list)
    for i, c in enumerate(sel):
        for a in c.tolist():
            owners[a].append(i)
    pos = [[] for _ in range(n)]
    n_conflict_anchor = 0
    for a, gts in owners.items():
        if len(gts) == 1:
            pos[gts[0]].append(a)
            continue
        n_conflict_anchor += 1
        xy = g.anchor_xy(np.array([a]))[0]
        d = np.linalg.norm(centres[gts] - xy, axis=1)
        pos[gts[int(np.argmin(d))]].append(a)
    if topk2 is not None:
        out = []
        for i, p in enumerate(pos):
            if len(p) > topk2:
                d = np.linalg.norm(g.anchor_xy(np.array(p)) - centres[i], axis=1)
                p = [p[j] for j in np.argsort(d, kind="stable")[:topk2]]
            out.append(len(p))
        return np.array(out), n_conflict_anchor
    return np.array([len(p) for p in pos]), n_conflict_anchor


def analyze_file(path: str, arms=tuple(g.ARMS)):
    stem = Path(path).stem
    boxes, cls = g.read_dota_label(Path(path))
    n = len(boxes)
    if n == 0:
        return []
    centres = boxes[:, :2]
    dist = np.linalg.norm(centres[:, None] - centres[None], axis=-1)
    np.fill_diagonal(dist, np.inf)
    nn16 = (dist < 16).sum(1)
    nn32 = (dist < 32).sum(1)
    nn_min = dist.min(1) if n > 1 else np.full(n, np.inf)
    rows = [
        dict(
            stem=stem,
            scene=g.scene_key(stem),
            gt=i,
            cls=g.CLASSES[cls[i]],
            w=boxes[i, 2],
            h=boxes[i, 3],
            short=min(boxes[i, 2], boxes[i, 3]),
            long=max(boxes[i, 2], boxes[i, 3]),
            theta=boxes[i, 4],
            bin=g.size_bin(boxes[i, 2], boxes[i, 3]),
            n_img=n,
            nn16=int(nn16[i]),
            nn32=int(nn32[i]),
            nn_min=float(nn_min[i]),
        )
        for i in range(n)
    ]
    for arm in arms:
        a = g.ARMS[arm]
        cands = [g.candidates_one(b, a) for b in boxes]
        count = defaultdict(int)
        for c in cands:
            for x in c.tolist():
                count[x] += 1
        pos_o2m, _ = _assign_proxy(cands, centres, TOPK_O2M, None)
        pos_o2o, _ = _assign_proxy(cands, centres, TOPK_O2O, 1)
        for i, c in enumerate(cands):
            lv = g.level_of(c)
            shared = sum(count[x] > 1 for x in c.tolist())
            r = rows[i]
            r[f"{arm}_cand"] = len(c)
            r[f"{arm}_cand_p3"] = int((lv == 0).sum())
            r[f"{arm}_cand_p4"] = int((lv == 1).sum())
            r[f"{arm}_cand_p5"] = int((lv == 2).sum())
            r[f"{arm}_shared"] = int(shared)
            r[f"{arm}_all_shared"] = bool(len(c) > 0 and shared == len(c))
            r[f"{arm}_pos_o2m"] = int(pos_o2m[i])
            r[f"{arm}_pos_o2o"] = int(pos_o2o[i])
    return rows


def density_bin(nn16: int) -> str:
    return "isolated" if nn16 == 0 else "1-2" if nn16 <= 2 else ">=3"


def summarize(df: pd.DataFrame, arms) -> dict:
    out = {"n_gt": int(len(df)), "n_images": int(df.stem.nunique()), "n_scenes": int(df.scene.nunique())}

    def stage_table(sub: pd.DataFrame) -> dict:
        res = {}
        for arm in arms:
            zc = sub[f"{arm}_cand"] == 0
            res[arm] = dict(
                n=int(len(sub)),
                zero_cand=float(zc.mean()),
                all_shared=float(sub[f"{arm}_all_shared"].mean()),
                zero_pos_o2m_proxy=float((sub[f"{arm}_pos_o2m"] == 0).mean()),
                zero_pos_o2o_proxy=float((sub[f"{arm}_pos_o2o"] == 0).mean()),
                lost_at_conflict_o2m_proxy=float(((sub[f"{arm}_pos_o2m"] == 0) & ~zc).mean()),
                mean_cand=float(sub[f"{arm}_cand"].mean()),
                mean_pos_o2m_proxy=float(sub[f"{arm}_pos_o2m"].mean()),
                shared_frac=float(sub[f"{arm}_shared"].sum() / max(sub[f"{arm}_cand"].sum(), 1)),
                frac_cand_gt_topk=float((sub[f"{arm}_cand"] > TOPK_O2M).mean()),
            )
        return res

    out["overall"] = stage_table(df)
    out["by_size"] = {b: stage_table(s) for b, s in df.groupby("bin")}
    out["by_size_density"] = {f"{b}|{d}": stage_table(s) for (b, d), s in df.groupby(["bin", df.nn16.map(density_bin)])}
    trans = {}
    for arm in arms:
        if arm == "A0":
            continue
        z0 = df["A0_pos_o2m"] == 0
        z1 = df[f"{arm}_pos_o2m"] == 0
        trans[arm] = dict(
            rescued=int((z0 & ~z1).sum()),
            newly_starved=int((~z0 & z1).sum()),
            still_zero=int((z0 & z1).sum()),
            net_rescued=int((z0 & ~z1).sum() - (~z0 & z1).sum()),
            newly_starved_by_size={b: int(((~z0 & z1) & (df.bin == b)).sum()) for b in sorted(df.bin.unique())},
        )
    out["transitions_vs_A0_o2m_proxy"] = trans
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--labels", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--protocol", default="woX", choices=("woX", "full"))
    ap.add_argument("--arms", default="A0,A1,A8,A2")
    ap.add_argument("--max-files", type=int, default=None)
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    arms = tuple(args.arms.split(","))
    files = sorted(p for p in args.labels.glob("*.txt") if args.protocol == "full" or not g.is_xview(p.stem))
    if args.max_files:
        files = files[: args.max_files]
    t0 = time.time()
    with Pool(args.workers) as pool:
        rows = [r for rs in pool.starmap(analyze_file, [(str(f), arms) for f in files], chunksize=32) for r in rs]
    df = pd.DataFrame(rows)
    args.out.mkdir(parents=True, exist_ok=True)
    with gzip.open(args.out / "rq2_per_gt.csv.gz", "wt") as fh:
        df.to_csv(fh, index=False)
    summ = summarize(df, arms)
    summ["_meta"] = dict(
        labels=str(args.labels),
        protocol=args.protocol,
        n_files=len(files),
        arms={a: vars(g.ARMS[a]) for a in arms},
        topk_o2m=TOPK_O2M,
        topk_o2o=TOPK_O2O,
        seconds=round(time.time() - t0, 1),
        note="pos_* and lost_at_conflict are label-only proxies (alignment metric replaced by centre distance)",
    )
    (args.out / "rq2_summary.json").write_text(json.dumps(summ, indent=2))
    print(json.dumps(summ["overall"], indent=1))
    print(f"{len(df)} GT, {len(files)} files, {time.time() - t0:.0f}s -> {args.out}")


if __name__ == "__main__":
    main()
