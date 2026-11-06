"""Decide from the 12 exploratory runs, on val, whether the new runs are worth training.

The thresholds below are [design]: fixed before looking at the val output, as a stopping rule for spending GPU time.
They are not statistical tests and support no claim in a paper. All values are per-seed means on very tiny GTs.

- C1, rescue: for GTs that A0 leaves without a candidate, recall(A2) - recall(A0) at score >= 0.25 is positive in every
  seed and its mean is at least RESCUE_MIN.
- C2, reason: at score >= 0.05, so a low score alone does not count as a miss, the most common fate among the very tiny
  GTs that A2 leaves undetected is one of EXPLANATORY and covers at least REASON_MIN of them. ``miss`` (no prediction
  reaches IoU 0.1) is the residual class: it says the detector fired nowhere near the box, not why, so it is reported
  but cannot pass C2.
- C3, keep A8: [recall(A2) - recall(A8)] on dense GTs minus the same on isolated GTs has the same sign in every seed and
  an absolute mean of at least A8_MIN. Otherwise A8 adds cost without a question to answer.

Outcome (annex A2, revised 06/11 before any val output): C1 or C2 -> train; neither -> do not train yet.

``test_scope`` fixes in advance how much of the per-GT test analysis runs, from the time measured here on val.
"""

from __future__ import annotations

import pandas as pd

RESCUE_MIN = 0.02
REASON_MIN = 0.50
A8_MIN = 0.01
EXPLANATORY = ("loc", "lost_to_neighbour", "cls", "both")
# Per-GT test analysis (annex A2 §8): both score levels if the estimate fits this budget, else score >= 0.25 only.
TEST_BUDGET_HOURS = 10.0
N_GT_TEST = 128_769  # experiments/2026-11-05-rq2-offline-woX/rq2_summary_test.json, n_gt


def _recall(df: pd.DataFrame, arm: str) -> pd.Series:
    return df[df.arm == arm].groupby("seed")["detected"].mean()


def rescue(df25: pd.DataFrame) -> dict:
    vt = df25[(df25.bin == "vt") & df25.starved_A0]
    d = (_recall(vt, "A2") - _recall(vt, "A0")).dropna()
    return dict(per_seed={int(k): float(v) for k, v in d.items()}, mean=float(d.mean()), n_gt=int((vt.arm == "A2").sum() / max(d.size, 1)),
                passed=bool(len(d) >= 2 and (d > 0).all() and d.mean() >= RESCUE_MIN))


def reason(df05: pd.DataFrame) -> dict:
    u = df05[(df05.bin == "vt") & (df05.arm == "A2") & (df05.fate != "detected")]
    share = u.groupby(["seed", "fate"]).size().unstack("fate", fill_value=0)
    share = share.div(share.sum(axis=1), axis=0).mean().sort_values(ascending=False)
    top = str(share.index[0])
    return dict(shares={k: float(v) for k, v in share.items()}, top=top, top_share=float(share.iloc[0]),
                passed=bool(top in EXPLANATORY and share.iloc[0] >= REASON_MIN))


def keep_a8(df25: pd.DataFrame) -> dict:
    vt = df25[df25.bin == "vt"]

    def contrast(sub):
        return _recall(sub, "A2") - _recall(sub, "A8")

    d = (contrast(vt[vt.density == ">=3"]) - contrast(vt[vt.density == "isolated"])).dropna()
    same_sign = bool(len(d) >= 2 and ((d > 0).all() or (d < 0).all()))
    return dict(per_seed={int(k): float(v) for k, v in d.items()}, mean=float(d.mean()), same_sign=same_sign,
                passed=bool(same_sign and abs(d.mean()) >= A8_MIN))


def test_scope(seconds_per_run_val: float, n_gt_val: int, n_runs: int) -> dict:
    """Hours for the per-GT test analysis, scaled from val by GT count; which score levels fit TEST_BUDGET_HOURS."""
    per_level = seconds_per_run_val * N_GT_TEST / n_gt_val * n_runs / 3600
    scores = [0.25, 0.05] if 2 * per_level <= TEST_BUDGET_HOURS else [0.25]
    return dict(hours_per_score_level=round(per_level, 2), budget_hours=TEST_BUDGET_HOURS, scores=scores)


def decide(df25: pd.DataFrame, df05: pd.DataFrame) -> dict:
    c1, c2, c3 = rescue(df25), reason(df05), keep_a8(df25)
    verdict = "train" if c1["passed"] or c2["passed"] else "do_not_train_yet"
    arms = ["A0", "A8", "A2"] if c3["passed"] else ["A0", "A2"]
    return dict(verdict=verdict, arms_if_training=arms, runs_if_training=len(arms) * 2, C1_rescue=c1, C2_reason=c2,
                C3_keep_A8=c3, thresholds=dict(RESCUE_MIN=RESCUE_MIN, REASON_MIN=REASON_MIN, A8_MIN=A8_MIN))
