import json
import math

import numpy as np
import pytest

import c11x_results as cr


def _mk_run(root, name, arm, seed, done="c11_done.json", **heads):
    rd = root / name
    rd.mkdir(parents=True)
    (rd / done).write_text(json.dumps({"arm": arm, "seed": seed}))
    for head, ap in heads.items():
        (rd / f"eval_{head}.json").write_text(json.dumps({"head": head, "AP": ap, "AP_vt": ap / 3, "version": "oc"}))
    return rd


@pytest.fixture
def runs(tmp_path):
    aps = {("A0", 1): 0.131, ("A0", 2): 0.130, ("A0", 3): 0.128,
           ("A2", 1): 0.1321, ("A2", 2): 0.1384, ("A2", 3): 0.1292}
    for (arm, seed), ap in aps.items():
        _mk_run(tmp_path, f"c11_{arm}_s{seed}", arm, seed, e2e=ap, nms=ap + 0.006)
    # file chấm lại từng gây đếm trùng ở ô #32
    (tmp_path / "c11_A0_s1" / "eval_e2e_recheck.json").write_text(json.dumps({"head": "e2e", "AP": 0.131}))
    return tmp_path


def test_collect_ignores_recheck_and_counts_three_seeds(runs):
    df = cr.collect_runs(runs)
    t = cr.summary_table(df, metrics=("AP",))
    assert t.loc[("e2e", "A0"), ("AP", "count")] == 3
    assert math.isclose(t.loc[("e2e", "A0"), ("AP", "mean")], (0.131 + 0.130 + 0.128) / 3)


def test_collect_rejects_duplicate_arm_seed(runs):
    _mk_run(runs, "c11_A0_s1_copy", "A0", 1, e2e=0.2)
    with pytest.raises(AssertionError):
        cr.collect_runs(runs)


def test_collect_reads_new_done_file(tmp_path):
    _mk_run(tmp_path, "c11x_K3_s4", "K3", 4, done="c11x_done.json", e2e=0.14)
    df = cr.collect_runs(tmp_path)
    assert df.loc[0, "arm"] == "K3" and df.loc[0, "source"] == "c11x_done.json"


def test_paired_seed_deltas(runs):
    df = cr.collect_runs(runs)
    d = cr.paired_seed_deltas(df, "e2e", "A2", "A0", "AP")
    exp = np.array([0.1321 - 0.131, 0.1384 - 0.130, 0.1292 - 0.128])
    assert d["n"] == 3
    assert math.isclose(d["mean"], exp.mean())
    assert math.isclose(d["sd"], exp.std(ddof=1))
    assert d["t_lo"] < d["mean"] < d["t_hi"]
    assert d["n_pos_sign"] == 3


def test_combine_scene_seed_widens_interval():
    scene = {"delta": 0.0035, "ci_lo": 0.0018, "ci_hi": 0.0057}
    seed = {"se": 0.002}
    c = cr.combine_scene_seed(scene, seed)
    se_scene = (0.0057 - 0.0018) / (2 * 1.959964)
    assert math.isclose(c["se_scene"], se_scene)
    assert math.isclose(c["hi"] - c["lo"], 2 * 1.959964 * math.sqrt(se_scene ** 2 + 0.002 ** 2))
    assert (c["hi"] - c["lo"]) > (scene["ci_hi"] - scene["ci_lo"])


def test_ci_skew_flags_asymmetry():
    assert math.isclose(cr.ci_skew({"delta": 0.0074, "ci_lo": 0.0033, "ci_hi": 0.0161}), (0.0161 - 0.0074) / 0.0041)
    assert math.isclose(cr.ci_skew({"delta": 1.0, "ci_lo": 0.0, "ci_hi": 2.0}), 1.0)


def test_head_interaction(runs):
    df = cr.collect_runs(runs)
    h = cr.head_interaction(df, "A2", "A0", "AP")
    assert np.allclose(h["d_nms_minus_d_e2e"], 0.0)  # nms = e2e + 0,006 ở mọi run nên hiệu của hiệu bằng 0


def test_seeds_needed():
    # Δ = sd ⇒ (1,96 + 0,84)² ≈ 7,85 → 8
    assert cr.seeds_needed(0.01, 0.01) == 8
    assert cr.seeds_needed(0.0, 0.01) == math.inf


def test_scene_key_audit_detects_split_crops():
    stems = ["9999955_00000_d_0000223__0_0", "9999955_00000_d_0000223__0_600", "04755", "04756"]
    per_image = cr.scene_key_audit(stems, lambda s: s)  # mỗi ảnh một nhóm: tách sai hai ô cùng ảnh gốc
    assert per_image["n_prefixes_split"] == 1 and per_image["n_groups"] == 4
    by_prefix = cr.scene_key_audit(stems, lambda s: s.split("__")[0])
    assert by_prefix["n_prefixes_split"] == 0 and by_prefix["n_groups"] == 3


def test_run_scene_bootstrap_with_fake_module(runs, tmp_path):
    for rd in runs.glob("c11_*"):
        (rd / "evalcache_e2e.npz").write_bytes(b"x")

    class FakeCB:
        @staticmethod
        def load_cache(f):
            return f.parent.name

        @staticmethod
        def multi_pair_bootstrap(by_arm, pairs, scene_key, keys, B, engine):
            assert B == 10000 and keys == ("AP",)
            assert sorted(by_arm["A0"]) == ["c11_A0_s1", "c11_A0_s2", "c11_A0_s3"]
            return {"A2-A0": {"AP": {"delta": 0.0035, "ci_lo": 0.001, "ci_hi": 0.006, "excludes_zero": True}}}

    out = tmp_path / "boot.json"
    boot = cr.run_scene_bootstrap(FakeCB, [runs], "e2e", [("A2", "A0"), ("A8", "A0")], ("AP",), 10000, None, out)
    meta = json.loads(out.read_text())["_c11x_meta"]
    assert meta["pairs"] == ["A2-A0"] and meta["B"] == 10000
    assert boot["A2-A0"]["AP"]["delta"] == 0.0035
