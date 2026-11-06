"""Scene-clustered bootstrap of a recall difference, or a difference-in-differences, between two arms.

Input: long per-GT table with columns ``scene``, ``arm``, ``seed``, a 0/1 outcome, and optionally a group column.
Delta for one seed = [recall_x(g1) - recall_y(g1)] - [recall_x(g0) - recall_y(g0)]; without groups it is
recall_x - recall_y. The estimate is the mean over seeds present in both arms. Scenes are resampled with one set of
weights for all runs, so the pairing across arms and seeds is preserved.

The returned ``scene`` and ``seed`` dicts plug into ``c11x_results.combine_scene_seed`` (preregistration, annex A1):
the bootstrap covers test scenes only; seed uncertainty is added there.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def _tensor(df, y, arms, seeds, group, groups):
    """Scene x (arm, seed, group) arrays of outcome sums and counts."""
    scene_idx, scenes = pd.factorize(df["scene"])
    arm_idx = df["arm"].map({a: i for i, a in enumerate(arms)}).to_numpy(dtype=float)
    seed_idx = df["seed"].map({s: i for i, s in enumerate(seeds)}).to_numpy(dtype=float)
    if group is None:
        grp_idx = np.zeros(len(df))
    else:
        grp_idx = df[group].map({g: i for i, g in enumerate(groups)}).to_numpy(dtype=float)
    keep = ~(np.isnan(arm_idx) | np.isnan(seed_idx) | np.isnan(grp_idx))
    n_g = 1 if group is None else len(groups)
    shape = (len(scenes), len(arms) * len(seeds) * n_g)
    cell = (arm_idx[keep].astype(int) * len(seeds) + seed_idx[keep].astype(int)) * n_g + grp_idx[keep].astype(int)
    num, den = np.zeros(shape), np.zeros(shape)
    np.add.at(num, (scene_idx[keep], cell), df[y].to_numpy(dtype=float)[keep])
    np.add.at(den, (scene_idx[keep], cell), 1.0)
    return num, den, n_g


def _per_seed(num_sum, den_sum, n_seed, n_g):
    """(..., cells) totals -> (..., seed) Delta of arm 0 minus arm 1, contrasted over groups if there are two."""
    with np.errstate(invalid="ignore", divide="ignore"):
        r = num_sum / den_sum
    r = r.reshape(*r.shape[:-1], 2, n_seed, n_g)
    d = r[..., 0, :, :] - r[..., 1, :, :]
    return d[..., 1] - d[..., 0] if n_g == 2 else d[..., 0]


def did_bootstrap(df: pd.DataFrame, x: str, y: str, outcome: str = "detected", group: str | None = None,
                  g1=None, g0=None, B: int = 10_000, seed: int = 0, chunk: int = 200) -> dict:
    """Bootstrap the x - y contrast. With ``group`` it is the contrast at g1 minus the contrast at g0."""
    if (group is None) != (g1 is None) or (group is None) != (g0 is None):
        raise ValueError("give group, g1 and g0 together")
    seeds = sorted(set(df.loc[df.arm == x, "seed"]) & set(df.loc[df.arm == y, "seed"]))
    if len(seeds) < 2:
        raise ValueError(f"need at least 2 shared seeds for {x} and {y}, got {seeds}")
    groups = None if group is None else [g0, g1]
    num, den, n_g = _tensor(df, outcome, (x, y), seeds, group, groups)
    n_seed = len(seeds)
    point = _per_seed(num.sum(0), den.sum(0), n_seed, n_g)
    rng = np.random.default_rng(seed)
    draws = []
    n_scene = num.shape[0]
    for start in range(0, B, chunk):
        m = min(chunk, B - start)
        w = rng.multinomial(n_scene, np.full(n_scene, 1 / n_scene), size=m).astype(float)
        draws.append(np.nanmean(_per_seed(w @ num, w @ den, n_seed, n_g), axis=-1))
    draws = np.concatenate(draws)
    delta = float(np.mean(point))
    lo, hi = np.nanpercentile(draws, [2.5, 97.5])
    sd = float(np.std(point, ddof=1))
    return {
        "pair": f"{x}-{y}", "group": group, "g1": g1, "g0": g0, "B": B, "n_scene": n_scene,
        "scene": {"delta": delta, "ci_lo": float(lo), "ci_hi": float(hi), "sd": float(np.nanstd(draws, ddof=1))},
        "seed": {"n": n_seed, "mean": delta, "sd": sd, "se": sd / np.sqrt(n_seed), "min": float(np.min(point)),
                 "max": float(np.max(point)), "per_seed": {int(s): float(v) for s, v in zip(seeds, point)},
                 "n_pos_sign": int((point > 0).sum())},
    }
