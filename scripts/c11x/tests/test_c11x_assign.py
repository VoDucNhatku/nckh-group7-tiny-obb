import math

import numpy as np
import pytest
import torch

import c11x_assign as ca


def _grid(stride, size=256):
    g = torch.arange(stride / 2, size, stride)
    yy, xx = torch.meshgrid(g, g, indexing="ij")
    return torch.stack([xx.flatten(), yy.flatten()], -1)


def _anchors(size=256):
    return torch.cat([_grid(s, size) for s in (8, 16, 32)])


def _random_gt(seed, b=3, n=9, size=256):
    g = torch.Generator().manual_seed(seed)
    xy = torch.rand(b, n, 2, generator=g) * (size - 40) + 20
    wh = torch.rand(b, n, 2, generator=g) * 24 + 1
    r = torch.rand(b, n, 1, generator=g) * math.pi
    mask = (torch.rand(b, n, 1, generator=g) > 0.2).float()
    return torch.cat([xy, wh, r], -1), mask


@pytest.fixture(autouse=True)
def _clean():
    yield
    ca.remove_patch()


@pytest.mark.parametrize("seed", range(5))
def test_A2_equals_stock(seed):
    from ultralytics.utils.tal import RotatedTaskAlignedAssigner as R

    asg = R(topk=10, num_classes=8, stride=[8, 16, 32])
    gt, mask = _random_gt(seed)
    xy = _anchors()
    stock = R.select_candidates_in_gts(asg, xy, gt, mask)
    ca.apply_arm("A2")
    assert torch.equal(asg.select_candidates_in_gts(xy, gt, mask), stock)
    assert ca.STATE["calls"] == 1


def test_A0_matches_independent_point_in_polygon():
    gt, mask = _random_gt(7)
    xy = _anchors().numpy()
    got = ca.candidate_mask(torch.tensor(xy), gt, mask, ca.parse_arm("A0")).numpy()
    for bi in range(gt.shape[0]):
        for gi in range(gt.shape[1]):
            x, y, w, h, r = gt[bi, gi].tolist()
            d = xy - np.array([x, y])
            u = d @ np.array([math.cos(r), math.sin(r)])
            v = d @ np.array([-math.sin(r), math.cos(r)])
            inside = (np.abs(u) <= w / 2 - 1e-4) & (np.abs(v) <= h / 2 - 1e-4)
            outside = (np.abs(u) > w / 2 + 1e-4) | (np.abs(v) > h / 2 + 1e-4)
            assert got[bi, gi][inside].all() and not got[bi, gi][outside].any()


@pytest.mark.parametrize("chain", [("A0", "A8", "A2"), ("A0", "A1", "A2")])
def test_fixed_arms_are_nested(chain):
    xy = _anchors()
    for seed in range(5):
        gt, mask = _random_gt(seed)
        ms = [ca.candidate_mask(xy, gt, mask, ca.parse_arm(a)) for a in chain]
        for small, big in zip(ms, ms[1:]):
            assert not (small & ~big).any()


def test_A8_covers_every_gt_on_stride8_grid():
    """Định lý phủ √2·s: hộp có cạnh ngắn ≥ √2·8 luôn chứa ít nhất một điểm lưới bước 8 (mọi vị trí, mọi góc)."""
    xy = _grid(8)
    for seed in range(20):
        gt, mask = _random_gt(seed, n=30)
        gt[..., 2:4] = gt[..., 2:4] / 10  # toàn vật tí hon (≤ 2,5 px)
        cnt = ca.candidate_mask(xy, gt, torch.ones_like(mask), ca.parse_arm("A8")).sum(-1)
        assert (cnt >= 1).all()


@pytest.mark.parametrize("k", [1, 3, 6])
def test_K_rule_guarantees_k_candidates_and_keeps_big_boxes(k):
    xy = _anchors()
    gt, mask = _random_gt(3, n=20)
    valid = mask.bool().squeeze(-1)
    native = ca.candidate_mask(xy, gt, mask, ca.parse_arm("A0"))
    stats = {}
    got = ca.candidate_mask(xy, gt, mask, ca.parse_arm(f"K{k}"), stats)
    cnt = got.sum(-1)
    assert (cnt[valid] >= k).all()
    already = (native.sum(-1) >= k) & valid
    assert torch.equal(got[already], native[already])
    assert not (native & ~got)[valid].any()
    assert int(stats["level_hist"].sum()) == int(valid.sum())
    assert int(stats["still_short"]) == 0


def test_K_is_nested_in_k():
    xy = _anchors()
    gt, mask = _random_gt(11, n=20)
    valid = mask.bool().squeeze(-1)
    prev = None
    for k in (1, 2, 4, 8):
        m = ca.candidate_mask(xy, gt, mask, ca.parse_arm(f"K{k}"))
        if prev is not None:
            assert not (prev & ~m)[valid].any()
        prev = m


def test_parse_arm_rejects_unknown():
    for bad in ("A3", "K0", "K", "k2", "A4"):
        with pytest.raises(ValueError):
            ca.parse_arm(bad)


def test_version_guard(monkeypatch):
    import ultralytics

    monkeypatch.setattr(ultralytics, "__version__", "8.4.183")
    with pytest.raises(RuntimeError):
        ca.apply_arm("A2")


def test_remove_patch_restores_stock():
    from ultralytics.utils.tal import RotatedTaskAlignedAssigner as R

    orig = R.select_candidates_in_gts
    ca.apply_arm("K2")
    assert R.select_candidates_in_gts is not orig
    ca.remove_patch()
    assert R.select_candidates_in_gts is orig


def _yaml_model():
    from ultralytics.nn.tasks import OBBModel
    from ultralytics.utils import DEFAULT_CFG_DICT, IterableSimpleNamespace

    m = OBBModel("yolo26n-obb.yaml", nc=8, verbose=False)
    m.args = IterableSimpleNamespace(**{**DEFAULT_CFG_DICT, "epochs": 24})
    return m.eval()


def _batch():
    torch.manual_seed(0)
    bb = torch.tensor([[0.3, 0.3, 0.02, 0.01, 0.3], [0.5, 0.5, 0.05, 0.02, 1.0], [0.7, 0.2, 0.1, 0.06, 0.0],
                       [0.31, 0.31, 0.015, 0.015, 0.7], [0.4, 0.4, 0.03, 0.01, 0.5], [0.8, 0.8, 0.004, 0.003, 0.0]])
    return {"img": torch.rand(2, 3, 256, 256), "batch_idx": torch.tensor([0, 0, 0, 0, 1, 1.]),
            "cls": torch.tensor([[0], [1], [2], [0], [1], [0.]]), "bboxes": bb}


@pytest.mark.parametrize("arm", ["A0", "A2", "K3"])
@pytest.mark.heavy
def test_recorder_counts_are_consistent(arm):
    ca.apply_arm(arm)
    m = _yaml_model()
    with torch.no_grad():
        m.criterion = m.init_criterion()
        rec = ca.PositiveRecorder(m.criterion)
        with rec.active():
            m.loss(_batch())
    br = {r["branch"]: r for r in rec.records}
    assert set(br) == {"o2m", "o2o"}
    for name, topk in (("o2m", 10), ("o2o", 7)):
        r = br[name]
        v = r["valid"]
        assert (r["n_pos"][v] <= r["n_pos_pre"][v]).all()
        assert (r["n_pos_pre"][v] <= np.minimum(r["n_cand"][v], topk)).all()
    assert (br["o2o"]["n_pos"][br["o2o"]["valid"]] <= 1).all()
    # GT cuối (0,004 × 256 ≈ 1 px) bị bộ lọc < 2 px của loss bỏ: ảnh 1 chỉ còn 1 GT hợp lệ
    assert br["o2m"]["valid"][1].sum() == 1
    if arm == "K3":
        assert (br["o2m"]["n_cand"][br["o2m"]["valid"]] >= 3).all()
    # sau khi thoát context, assigner trở lại phương thức của class
    assert "_forward" not in m.criterion.one2many.assigner.__dict__
