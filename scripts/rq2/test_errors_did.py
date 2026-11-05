"""Synthetic checks: every fate is reachable and exact; the bootstrap recovers a known difference-in-differences."""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "c11x"))

import rq2_did as rd  # noqa: E402
import rq2_errors as re_  # noqa: E402


def square(cx, cy, s=10.0):
    h = s / 2
    return np.array([cx - h, cy - h, cx + h, cy - h, cx + h, cy + h, cx - h, cy + h], dtype=float)


def preds(items):
    """{class: (scores desc, polys)} from (class, score, poly)."""
    out = {}
    for c in {i[0] for i in items}:
        v = sorted([i for i in items if i[0] == c], key=lambda t: -t[1])
        out[c] = (np.array([t[1] for t in v]), np.array([t[2] for t in v]))
    return out


def test_each_fate():
    gts = [square(50 + 100 * i, 50) for i in range(6)]
    gts.append(square(51, 50))  # overlaps GT 0 almost fully: the single prediction can match only one of them
    cls = np.zeros(7, dtype=int)
    p = preds([
        (0, 0.9, square(50, 50)),   # GT 0 detected; GT 6 therefore lost to a neighbour
        (1, 0.9, square(150, 50)),  # GT 1: other class, high IoU -> cls
        (0, 0.8, square(255, 50)),  # GT 2: shifted 5 px on a 10 px box, IoU = 1/3 -> loc
        (1, 0.8, square(355, 50)),  # GT 3: other class, shifted -> both
        (0, 0.1, square(450, 50)),  # GT 4: below the score threshold -> miss
    ])
    r = re_.fates_image(gts, cls, p, score_thr=0.25)
    assert r["fate"] == ["detected", "cls", "loc", "both", "miss", "miss", "lost_to_neighbour"]
    assert r["det_0.25"][2] and not r["det_0.5"][2]  # the localisation error shows in the recall curve
    assert r["best_same"][2] == pytest.approx(1 / 3, abs=1e-6)


def test_no_predictions_is_all_miss():
    r = re_.fates_image([square(50, 50)], np.array([0]), {}, 0.25)
    assert r["fate"] == ["miss"]


def test_fate_table_shares_sum_to_one():
    df = pd.DataFrame(dict(arm="A2", bin="vt", seed=[4, 4, 5, 5], fate=["miss", "detected", "loc", "loc"]))
    t = re_.fate_table(df)
    means = t.xs("mean", axis=1, level=1)[list(re_.FATES)]
    assert means.sum(axis=1).iloc[0] == pytest.approx(1.0)
    assert means["loc"].iloc[0] == pytest.approx(0.5)


def synth(n_scene=300, n_gt=20, seeds=(4, 5, 6, 7), effect=0.20, base=0.3, seed_sd=0.0, rng_seed=0):
    """A2 gains ``effect`` recall on starved GTs only, so the true DiD is ``effect``."""
    rng = np.random.default_rng(rng_seed)
    frames = []
    for s in seeds:
        shift = rng.normal(0, seed_sd)
        for arm in ("A0", "A2"):
            n = n_scene * n_gt
            starved = rng.random(n) < 0.5
            p = base + (effect + shift) * starved * (arm == "A2")
            frames.append(pd.DataFrame(dict(scene=np.repeat(np.arange(n_scene), n_gt), arm=arm, seed=s,
                                            starved=starved, detected=rng.random(n) < p)))
    return pd.concat(frames, ignore_index=True)


def test_did_recovers_known_effect():
    r = rd.did_bootstrap(synth(), "A2", "A0", group="starved", g1=True, g0=False, B=300)
    assert abs(r["scene"]["delta"] - 0.20) < 0.025
    assert r["scene"]["ci_lo"] < 0.20 < r["scene"]["ci_hi"]
    assert r["seed"]["n"] == 4 and r["seed"]["n_pos_sign"] == 4


def test_did_null_interval_covers_zero():
    r = rd.did_bootstrap(synth(effect=0.0), "A2", "A0", group="starved", g1=True, g0=False, B=300)
    assert r["scene"]["ci_lo"] < 0 < r["scene"]["ci_hi"]


def test_plain_difference_without_groups():
    r = rd.did_bootstrap(synth(), "A2", "A0", B=200)
    assert abs(r["scene"]["delta"] - 0.10) < 0.02  # half of the GTs gain 0.20


def test_scene_weights_pair_runs():
    """Identical arms give exactly 0 in every bootstrap draw, which needs one set of weights for all runs."""
    a = synth(effect=0.0, seeds=(4, 5))
    base = a[a.arm == "A0"]
    d = pd.concat([base, base.assign(arm="A2")])
    r = rd.did_bootstrap(d, "A2", "A0", group="starved", g1=True, g0=False, B=100)
    assert r["scene"]["ci_lo"] == 0 and r["scene"]["ci_hi"] == 0


def test_combines_with_annex_a1_rule():
    import c11x_results as cr

    r = rd.did_bootstrap(synth(seed_sd=0.05, rng_seed=1), "A2", "A0", group="starved", g1=True, g0=False, B=200)
    c = cr.combine_scene_seed(r["scene"], r["seed"])
    assert c["q"] == pytest.approx(3.182, abs=0.001)  # t(0.975, 3), four seeds
    assert c["hi"] - c["lo"] > r["scene"]["ci_hi"] - r["scene"]["ci_lo"]  # adding seed noise widens the interval


def test_bad_group_arguments():
    with pytest.raises(ValueError):
        rd.did_bootstrap(synth(), "A2", "A0", group="starved", B=10)
