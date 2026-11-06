import numpy as np
import pytest

import c11x_cache as cc


def cache(order):
    """Hai ảnh a (2 dự đoán), b (1 dự đoán), c (0), xếp theo `order`. Điểm mã hóa ảnh: a 1.x, b 2.x."""
    per = {"a": [1.1, 1.2], "b": [2.1], "c": []}
    sc = np.array([v for s in order for v in per[s]])
    off = np.cumsum([0] + [len(per[s]) for s in order])
    return {
        "stems": np.array(order), "T": np.array(2),
        "k0_a0_sc": sc, "k0_a0_tp": np.stack([sc > 2, sc > 1]), "k0_a0_fp": np.stack([sc <= 2, sc <= 1]),
        "k0_a0_off": off, "k0_a0_npig": np.array([{"a": 5, "b": 6, "c": 7}[s] for s in order]),
        "k0_a0_present": np.array([s != "c" for s in order]),
    }


def test_reorder_matches_a_cache_built_in_that_order():
    want = cache(["c", "a", "b"])
    got = cc.reorder_cache(cache(["a", "b", "c"]), np.array(["c", "a", "b"]))
    assert set(got) == set(want)
    for k in want:
        assert np.array_equal(got[k], want[k]), k


def test_missing_field_is_rejected():
    c = cache(["a", "b", "c"])
    del c["k0_a0_npig"]
    with pytest.raises(ValueError, match="thiếu"):
        cc.reorder_cache(c, np.array(["a", "b", "c"]))


def test_align_caches_fixes_order_and_keeps_backup(tmp_path):
    ref = tmp_path / "ref.npz"
    np.savez(ref, **cache(["a", "b", "c"]))
    good, bad = tmp_path / "c11_A0_s1", tmp_path / "c11_A2_s4"
    good.mkdir(), bad.mkdir()
    np.savez(good / "evalcache_e2e.npz", **cache(["a", "b", "c"]))
    np.savez(bad / "evalcache_nms.npz", **cache(["b", "c", "a"]))
    assert cc.align_caches([good, bad], ref) == ["c11_A2_s4/evalcache_nms.npz"]
    with np.load(bad / "evalcache_nms.npz") as z:
        assert z["stems"].tolist() == ["a", "b", "c"]
        assert z["k0_a0_sc"].tolist() == [1.1, 1.2, 2.1]
    with np.load(bad / "evalcache_nms.unsorted.npz") as z:
        assert z["stems"].tolist() == ["b", "c", "a"]
    assert cc.align_caches([good, bad], ref) == []  # chạy lại không đổi gì


def test_different_image_set_is_rejected(tmp_path):
    ref = tmp_path / "ref.npz"
    np.savez(ref, **cache(["a", "b"]))
    d = tmp_path / "run"
    d.mkdir()
    np.savez(d / "evalcache_e2e.npz", **cache(["a", "c"]))
    with pytest.raises(ValueError, match="tập ảnh"):
        cc.align_caches([d], ref)
