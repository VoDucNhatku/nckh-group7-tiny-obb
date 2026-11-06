"""Check that geometry.candidates_one matches Ultralytics 8.4.174 select_candidates_in_gts."""

import math

import numpy as np
import pytest
import torch

import geometry as g

ul_tal = pytest.importorskip("ultralytics.utils.tal")


def _ultralytics_mask(boxes: np.ndarray, stride_val: float):
    from ultralytics.utils.tal import RotatedTaskAlignedAssigner, make_anchors

    feats = [torch.zeros(1, 1, g.IMG_SIZE // s, g.IMG_SIZE // s) for s in g.STRIDES]
    anc, st = make_anchors(feats, torch.tensor(g.STRIDES, dtype=torch.float32), 0.5)
    xy = (anc * st).double()
    asg = RotatedTaskAlignedAssigner(topk=10, num_classes=8, stride=list(g.STRIDES))
    asg.stride_val = stride_val
    gt = torch.tensor(boxes, dtype=torch.float64)[None]
    mask_gt = torch.ones(1, len(boxes), 1, dtype=torch.float64)
    return asg.select_candidates_in_gts(xy, gt, mask_gt)[0].numpy(), xy.numpy()


@pytest.mark.parametrize("arm,stride_val", [("A0", 0.0), ("A2", 16.0), ("A8", g.SQRT2_8)])
def test_matches_ultralytics(arm, stride_val):
    rng = np.random.default_rng(0)
    n = 400
    boxes = np.stack(
        [
            rng.uniform(40, 760, n),
            rng.uniform(40, 760, n),
            rng.uniform(2, 40, n),
            rng.uniform(2, 20, n),
            rng.uniform(-math.pi / 4, 3 * math.pi / 4, n),
        ],
        1,
    )
    mask, xy = _ultralytics_mask(boxes, stride_val)
    for i, b in enumerate(boxes):
        ids = g.candidates_one(b, g.ARMS[arm])
        ours = {tuple(np.round(p, 3)) for p in g.anchor_xy(ids)}
        ref = {tuple(np.round(p, 3)) for p in xy[mask[i]]}
        assert ours == ref, (arm, i, b, ours ^ ref)


def test_coverage_floor_guarantees_candidate():
    rng = np.random.default_rng(1)
    for _ in range(2000):
        b = (rng.uniform(40, 760), rng.uniform(40, 760), rng.uniform(2, 11), rng.uniform(2, 11), rng.uniform(0, math.pi))
        assert len(g.candidates_one(b, g.ARMS["A8"])) >= 1


def test_scene_key_and_xview():
    assert g.is_xview("100__0_1800") and not g.is_xview("0000001_03499_d_0000006__1120_280")
    assert g.scene_key("0000001_03499_d_0000006__1120_280") == "visdrone:0000001_03499_d_0000006"
    assert g.scene_key("P0000__1.0__0___0") == "dota:P0000"
    assert g.scene_key("100__0_1800") == "xview:100"
