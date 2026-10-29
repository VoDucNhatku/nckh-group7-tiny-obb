"""Test nhẹ: không dựng model, không train, không tải gì."""

import json
import sys

import numpy as np
import pandas as pd
import pytest

import c11x_preflight as cp

FAKE_C11 = {
    "aitodr_data.py": "def xview_stems(): pass\ndef build_yolo_dataset(L, I, D, version, exclude_xview, val_frac, seed): pass\n"
                      "def scene_key(s): return s\n",
    "aitodr_evalkit.py": "def load_official_evaluator(): pass\n",
    "c11_pipeline.py": "RECIPE = {}\ndef predict_and_eval(w, l, i, o, head, version, exclude_stems, save_dota_dir=None): pass\n",
    "c11_bootstrap.py": "def load_cache(f): pass\ndef multi_pair_bootstrap(by_arm, pairs, scene_key, keys, B, engine): pass\n",
}


@pytest.fixture
def fake_c11(tmp_path):
    d = tmp_path / "c11"
    d.mkdir()
    for name, src in FAKE_C11.items():
        (d / name).write_text(src)
    yield d
    for m in ("aitodr_data", "aitodr_evalkit", "c11_pipeline", "c11_bootstrap"):
        sys.modules.pop(m, None)
    if str(d) in sys.path:
        sys.path.remove(str(d))


def test_c11_code_ok(fake_c11):
    assert cp.check_c11_code(fake_c11) == []


def test_c11_code_reports_missing_param_and_file(fake_c11):
    (fake_c11 / "c11_pipeline.py").write_text("RECIPE = {}\ndef predict_and_eval(w, l, i, o, head): pass\n")
    (fake_c11 / "c11_bootstrap.py").unlink()
    errs = cp.check_c11_code(fake_c11)
    assert any("predict_and_eval thiếu tham số" in e and "save_dota_dir" in e for e in errs)
    assert any("c11_bootstrap.py" in e for e in errs)


def test_c11_code_missing_dir(tmp_path):
    assert "Không thấy code C11" in cp.check_c11_code(tmp_path / "nope")[0]


def test_data_checks(tmp_path):
    errs = cp.check_data(tmp_path, tmp_path / "img")
    assert len(errs) == 3
    (tmp_path / "labels.zip").write_bytes(b"<html>quota")
    for z in cp.IMAGE_ZIPS:
        (tmp_path / z).write_bytes(b"PK")
    assert cp.check_data(tmp_path, tmp_path / "img") == [f"{tmp_path / 'labels.zip'} không phải file zip "
                                                       "(có thể là trang HTML báo hết hạn mức tải)."]
    (tmp_path / "labels.zip").write_bytes(b"PK\x03\x04")
    assert cp.check_data(tmp_path, tmp_path / "img") == []


def test_old_runs(tmp_path):
    exp, runs = tmp_path, tmp_path / "runs-woX"
    errs, _ = cp.check_old_runs(runs, exp)
    assert len(errs) == 13  # 12 run + split manifest
    for a in cp.OLD_ARMS:
        for s in cp.OLD_SEEDS:
            rd = runs / f"c11_{a}_s{s}"
            (rd / "weights").mkdir(parents=True)
            (rd / "c11_done.json").write_text(json.dumps({"arm": a, "seed": s}))
            (rd / "weights" / "last.pt").write_bytes(b"x")
    (exp / "2026-10-20-dataset-woX").mkdir()
    (exp / "2026-10-20-dataset-woX" / "split_manifest.json").write_text("{}")
    errs, warns = cp.check_old_runs(runs, exp)
    assert errs == [] and len(warns) == 1  # thiếu results.csv của c11_A2_s1 chỉ là cảnh báo


def test_gpu_check_without_cuda(monkeypatch):
    import torch

    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    assert "Không có GPU" in cp.check_gpu()[0]
    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    monkeypatch.setattr(torch.cuda, "get_device_name", lambda i: "Tesla T4")
    assert "không phải A100" in cp.check_gpu()[0]
    monkeypatch.setattr(torch.cuda, "get_device_name", lambda i: "NVIDIA A100-SXM4-40GB")
    assert cp.check_gpu() == []


def test_space_check(tmp_path):
    assert cp.check_space(tmp_path, 0.0, "x") == []
    assert "cần ≥" in cp.check_space(tmp_path, 1e9, "x")[0]


def test_run_all_collects_every_error(tmp_path, monkeypatch):
    monkeypatch.setattr(cp, "check_gpu", lambda require="A100": ["gpu"])
    with pytest.raises(cp.PreflightError) as ei:
        cp.run_all(code_dir=tmp_path / "c11", data_drive=tmp_path / "data", local=tmp_path / "local",
                   runs_old=tmp_path / "runs", exp_drive=tmp_path, prereg=tmp_path / "p.md", drive=tmp_path,
                   need_drive_gb=0, need_local_gb=0)
    msg = str(ei.value)
    for part in ("gpu", "PREREG-C11X-v1", "Không thấy code C11", "labels.zip", "c11_A0_s1", "split_manifest"):
        assert part in msg


# ---------------------------------------------------------------- ước lượng thời gian (c11x_train) và cổng H2


def test_estimate_and_eta_printer(capsys, monkeypatch):
    import c11x_train as ct

    e = ct.estimate(85.0, 360, n_eval=30, cu_per_hour=10.0)
    assert e["train_h"] == pytest.approx(85 * 360 / 3600)
    assert e["eval_h"] == pytest.approx(30 * 337 / 3600)
    assert e["cu"] == pytest.approx(e["total_h"] * 10)
    clock = iter([1000.0, 1085.0])
    monkeypatch.setattr(ct.time, "time", lambda: next(clock))
    p = ct.EtaPrinter(lambda: 359, n_eval=30, cu_per_hour=10.0)
    cbs = p.callbacks()
    cbs["on_train_epoch_start"](None)
    cbs["on_fit_epoch_end"](None)
    cbs["on_fit_epoch_end"](None)  # chỉ in một lần
    out = capsys.readouterr().out
    assert out.count("[ETA]") == 1 and "85 s" in out and "359 epoch" in out and "CU" in out


def test_epochs_logged(tmp_path):
    import c11x_train as ct

    assert ct.epochs_logged(tmp_path) == 0
    (tmp_path / "results.csv").write_text("epoch,a\n1,0\n2,0\n")
    assert ct.epochs_logged(tmp_path) == 2


def test_h2_gate_go_and_no_go():
    import c11x_pergt as cg

    rng = np.random.default_rng(3)
    n = 3000
    base = pd.DataFrame(dict(im_file=[f"im{i % 150}.png" for i in range(n)], cls=rng.integers(0, 3, n),
                             short=rng.uniform(2, 20, n), long=rng.uniform(20, 30, n), n_gt_img=rng.integers(1, 40, n),
                             nn_px=rng.uniform(1, 50, n), o2m_n_pos=rng.integers(0, 11, n), in_loss=True,
                             arm=rng.choice(["A0", "A2"], n), head="nms"))
    base = cg.add_features(base)
    for effect, go in ((1.0, True), (-1.0, False)):
        logit = -1.0 + effect * np.log1p(base["o2m_n_pos"])
        df = base.assign(score=(rng.random(n) < 1 / (1 + np.exp(-logit))).astype(float))
        g = cg.h2_gate(df)
        assert g["go"] is go and g["n"] == n
        assert set(g["recall_lt8_by_npos"]) <= {"0", "1", "2", "3-4", "5-9", "10+"}
