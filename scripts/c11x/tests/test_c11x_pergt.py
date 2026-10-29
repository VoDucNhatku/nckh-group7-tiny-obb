import math

import numpy as np
import pandas as pd
import pytest

import c11x_pergt as cg


def test_xywhr_to_poly_matches_ultralytics():
    import torch
    from ultralytics.utils.ops import xywhr2xyxyxyxy

    rng = np.random.default_rng(0)
    b = np.c_[rng.uniform(0, 100, (20, 2)), rng.uniform(1, 30, (20, 2)), rng.uniform(-3, 3, 20)]
    ref = xywhr2xyxyxyxy(torch.tensor(b)).numpy()
    assert np.allclose(cg.xywhr_to_poly(b), ref, atol=1e-9)


def test_angle_error_is_periodic_and_axis_invariant():
    g = np.array([[10, 10, 8, 3, 0.2]])
    same_rect_other_param = np.array([[10, 10, 3, 8, 0.2 + math.pi / 2]])
    flipped = np.array([[10, 10, 8, 3, 0.2 + math.pi]])
    assert cg.angle_error_deg(g, same_rect_other_param)[0] == pytest.approx(0, abs=1e-9)
    assert cg.angle_error_deg(g, flipped)[0] == pytest.approx(0, abs=1e-9)
    assert cg.angle_error_deg(g, np.array([[10, 10, 8, 3, 0.2 + math.pi / 2]]))[0] == pytest.approx(90)
    assert cg.angle_error_deg(g, np.array([[10, 10, 8, 3, 0.2 + math.radians(10)]]))[0] == pytest.approx(10)


def test_poly_iou():
    a = cg.xywhr_to_poly(np.array([[0, 0, 4, 2, 0.0], [100, 100, 4, 2, 0.3]]))
    b = cg.xywhr_to_poly(np.array([[0, 0, 4, 2, 0.0], [2, 0, 4, 2, 0.0]]))
    m = cg.poly_iou_matrix(a, b)
    assert m[0, 0] == pytest.approx(1)
    assert m[0, 1] == pytest.approx(4 / 12)
    assert m[1].max() == 0


def test_greedy_match_one_to_one_and_by_class():
    gt = cg.xywhr_to_poly(np.array([[0, 0, 4, 4, 0], [10, 0, 4, 4, 0], [20, 0, 4, 4, 0]]))
    gcls = np.array([0, 0, 1])
    pd_ = cg.xywhr_to_poly(np.array([[0, 0, 4, 4, 0], [0.2, 0, 4, 4, 0], [20, 0, 4, 4, 0], [10, 0, 4, 4, 0]]))
    pcls = np.array([0, 0, 0, 1])  # dự đoán thứ 3 đúng chỗ GT 2 nhưng sai lớp; dự đoán 4 đúng chỗ GT 1 nhưng sai lớp
    conf = np.array([0.5, 0.9, 0.8, 0.7])
    mp, mi = cg.greedy_match(gt, gcls, pd_, pcls, conf)
    assert mp.tolist() == [1, -1, -1]  # dự đoán điểm cao hơn (0,9) lấy GT 0 trước; dự đoán 0 không còn GT nào
    assert mi[0] > 0.8


def test_nearest_neighbour():
    d = cg.nearest_neighbour_px(np.array([[0, 0], [3, 4], [100, 0]]))
    assert d.tolist() == [5, 5, pytest.approx(math.hypot(97, 4))]
    assert np.isinf(cg.nearest_neighbour_px(np.array([[1, 1]])))[0]


def test_recall_model_recovers_positive_effect():
    rng = np.random.default_rng(1)
    n = 4000
    df = pd.DataFrame(dict(
        im_file=[f"im{i % 200}.png" for i in range(n)], cls=rng.integers(0, 3, n),
        short=rng.uniform(2, 20, n), long=rng.uniform(20, 30, n), n_gt_img=rng.integers(1, 50, n),
        nn_px=rng.uniform(1, 50, n), o2m_n_pos=rng.integers(0, 11, n), in_loss=True,
        arm=rng.choice(["A0", "A2"], n)))
    df = cg.add_features(df)
    logit = -1.5 + 1.2 * np.log1p(df["o2m_n_pos"]) + 0.3 * df["log2_size_p3"]
    df["score"] = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(float)
    res = cg.fit_recall_models(df, tau=0.5)
    assert res["pooled"].params["lpos"] == pytest.approx(1.2, abs=0.25)
    assert set(res["per_arm"]) == {"A0", "A2"}
    med = cg.mediation_check(df, tau=0.5)
    assert list(med.index) == ["C(arm, Treatment('A0'))[T.A2]"]
    tab = cg.recall_table(df, 0.5)
    assert tab["n"].sum() == n


def test_record_and_match_end_to_end(tiny_dataset, random_weights):
    """Chạy cả đường ống trên CPU với mô hình ngẫu nhiên: đủ GT, khoá (im_file, gt_idx) duy nhất, đếm hợp lệ."""
    from pathlib import Path

    df = cg.record_assignment(random_weights, tiny_dataset, "K2", device="cpu", batch=2, workers=0)
    n_lab = sum(len(f.read_text().split("\n")) - 1 for f in (Path(tiny_dataset).parent / "labels" / "val").glob("*.txt"))
    assert len(df) == n_lab
    assert not df.duplicated(["im_file", "gt_idx"]).any()
    ok = df[df["in_loss"]]
    assert (ok["o2m_n_cand"] >= 2).all() and (ok["o2o_n_pos"] <= 1).all()
    assert (ok["o2m_n_pos"] <= ok["o2m_n_pos_pre"]).all()
    # toạ độ GT quy về ảnh gốc 128×128
    assert df["x"].between(0, 128).all() and df["short"].max() < 25
    m = cg.predict_and_match(random_weights, df, Path(tiny_dataset).parent / "images" / "val", head="e2e",
                             imgsz=128, device="cpu", batch=2)
    assert len(m) == len(df) and m["score"].between(0, 1).all()
    m2 = cg.predict_and_match(random_weights, df, Path(tiny_dataset).parent / "images" / "val", head="nms",
                              imgsz=128, device="cpu", batch=2)
    assert len(m2) == len(df)
    tab = cg.angle_table(cg.add_features(pd.concat([m, m2])))
    assert set(tab.columns) >= {"arm", "head", "size_bin", "median", "p90", "n"}
