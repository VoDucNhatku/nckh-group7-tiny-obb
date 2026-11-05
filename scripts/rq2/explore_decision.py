"""Decide from the 12 exploratory runs, on val, whether the new runs are worth training.

The thresholds below are [design]: fixed before looking at the val output, as a stopping rule for spending GPU time.
They are not statistical tests and support no claim in a paper. All values are per-seed means on very tiny GTs.

- C1, rescue: for GTs that A0 leaves without a candidate, recall(A2) - recall(A0) at score >= 0.25 is positive in every
  seed and its mean is at least RESCUE_MIN.
- C2, reason: at score >= 0.05, so a low score alone does not count as a miss, one fate covers at least REASON_MIN of the
  very tiny GTs that A2 leaves undetected.
- C3, keep A8: [recall(A2) - recall(A8)] on dense GTs minus the same on isolated GTs has the same sign in every seed and
  an absolute mean of at least A8_MIN. Otherwise A8 adds cost without a question to answer.

Outcome: C1 and C2 -> train; exactly one -> the team decides, with the reason shown; neither -> do not train yet.
"""

from __future__ import annotations

import pandas as pd

RESCUE_MIN = 0.02
REASON_MIN = 0.50
A8_MIN = 0.01


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
                passed=bool(share.iloc[0] >= REASON_MIN))


def keep_a8(df25: pd.DataFrame) -> dict:
    vt = df25[df25.bin == "vt"]

    def contrast(sub):
        return _recall(sub, "A2") - _recall(sub, "A8")

    d = (contrast(vt[vt.density == ">=3"]) - contrast(vt[vt.density == "isolated"])).dropna()
    same_sign = bool(len(d) >= 2 and ((d > 0).all() or (d < 0).all()))
    return dict(per_seed={int(k): float(v) for k, v in d.items()}, mean=float(d.mean()), same_sign=same_sign,
                passed=bool(same_sign and abs(d.mean()) >= A8_MIN))


def decide(df25: pd.DataFrame, df05: pd.DataFrame) -> dict:
    c1, c2, c3 = rescue(df25), reason(df05), keep_a8(df25)
    if c1["passed"] and c2["passed"]:
        verdict = "train"
    elif c1["passed"] or c2["passed"]:
        verdict = "team_decides"
    else:
        verdict = "do_not_train_yet"
    arms = ["A0", "A8", "A2"] if c3["passed"] else ["A0", "A2"]
    return dict(verdict=verdict, arms_if_training=arms, runs_if_training=len(arms) * 6, C1_rescue=c1, C2_reason=c2,
                C3_keep_A8=c3, thresholds=dict(RESCUE_MIN=RESCUE_MIN, REASON_MIN=REASON_MIN, A8_MIN=A8_MIN))
