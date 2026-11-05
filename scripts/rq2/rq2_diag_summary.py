"""Summarize the online assignment logs ``c11_assign_diag.jsonl`` of the C-11 runs.

The log schema is defined in ``scripts/c11/c11_pipeline.py`` (on the team Drive, not in git).
This reader does not assume field names: it flattens every JSON record, takes the arm/seed from
``c11_done.json`` next to the log, and writes one long table plus a pivot of every numeric field
averaged over the last ``--last-epochs`` epochs, by arm x (any of branch / cell / bin) present.

Usage
    python rq2_diag_summary.py --runs <EXP_DRIVE>/runs-woX --out <dir>
Then read ``diag_fields.txt`` and choose the columns to report (e.g. share of GTs with zero
positives per arm x size cell x o2m/o2o, positives gained or lost through conflicts).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

GROUP_HINTS = ("branch", "head", "cell", "bin", "size", "ar", "density")


def load_run(rd: Path) -> pd.DataFrame | None:
    log, done = rd / "c11_assign_diag.jsonl", rd / "c11_done.json"
    if not log.exists() or not done.exists():
        return None
    meta = json.loads(done.read_text())
    recs = [json.loads(line) for line in log.read_text().splitlines() if line.strip()]
    df = pd.json_normalize(recs, sep=".")
    df["arm"], df["seed"] = meta.get("arm"), meta.get("seed")
    return df


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--last-epochs", type=int, default=4)
    args = ap.parse_args()
    frames = [d for rd in sorted(args.runs.glob("c11_*_s*")) if (d := load_run(rd)) is not None]
    if not frames:
        raise SystemExit(f"no c11_assign_diag.jsonl under {args.runs}")
    df = pd.concat(frames, ignore_index=True)
    args.out.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out / "diag_long.csv.gz", index=False)
    (args.out / "diag_fields.txt").write_text("\n".join(f"{c}\t{df[c].dtype}" for c in df.columns))
    ep = next((c for c in df.columns if c.split(".")[-1] in ("epoch", "ep")), None)
    if ep is not None:
        df = df[df[ep] > df[ep].max() - args.last_epochs]
    keys = ["arm"] + [c for c in df.columns if c != "arm" and any(h == c.split(".")[-1] or c.split(".")[-1].startswith(h) for h in GROUP_HINTS) and df[c].dtype == object]
    num = [c for c in df.select_dtypes("number").columns if c not in ("seed", ep)]
    piv = df.groupby(keys)[num].mean().reset_index()
    piv.to_csv(args.out / "diag_pivot_last_epochs.csv", index=False)
    print("group keys:", keys)
    print(piv.head(40).to_string())


if __name__ == "__main__":
    main()
