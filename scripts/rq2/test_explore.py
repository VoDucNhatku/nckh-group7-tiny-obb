"""Checks without ultralytics: prediction files are readable by rq2_recall, and the decision rule behaves as written."""

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import explore_decision as ed
import predict_split as ps
import rq2_errors as re_
import rq2_recall as rr


class FakeObb:
    def __init__(self, polys, cls, conf):
        self.xyxyxyxy, self.cls, self.conf = np.array(polys, dtype=float).reshape(-1, 4, 2), np.array(cls), np.array(conf)

    def __len__(self):
        return len(self.cls)


class FakeResult:
    def __init__(self, path, obb):
        self.path, self.obb = path, obb


class FakeModel:
    names = {0: "vehicle", 1: "ship"}

    def __init__(self):
        self.calls = []

    def predict(self, src, **kw):
        self.calls.append((len(src), kw))
        for p in src:
            yield FakeResult(p, None if "empty" in p else FakeObb([[10, 10, 20, 10, 20, 20, 10, 20]], [0], [0.9]))


def _images(tmp_path, names):
    d = tmp_path / "images"
    d.mkdir()
    for n in names:
        (d / f"{n}.png").write_bytes(b"x")
    return d


def test_files_round_trip_through_read_predictions(tmp_path):
    img = _images(tmp_path, ["a", "b", "empty"])
    out = tmp_path / "pred"
    m = FakeModel()
    info = ps.predict_to_dota("w.pt", img, out, "e2e", chunk=2, model=m)
    assert info["n_images"] == 3 and info["n_boxes"] == 2
    assert [c[0] for c in m.calls] == [2, 1]  # chunked
    assert m.calls[0][1]["nms"] is False
    got = rr.read_predictions(out, {"a", "b", "empty"})
    assert set(got) == {("a", rr.g.CLASSES.index("vehicle")), ("b", rr.g.CLASSES.index("vehicle"))}
    scores, polys = got[("a", rr.g.CLASSES.index("vehicle"))]
    assert scores[0] == pytest.approx(0.9) and polys.shape == (1, 8)


def test_done_file_skips_prediction(tmp_path):
    img = _images(tmp_path, ["a"])
    out = tmp_path / "pred"
    ps.predict_to_dota("w.pt", img, out, "nms", model=FakeModel())
    m2 = FakeModel()
    ps.predict_to_dota("w.pt", img, out, "nms", model=m2)
    assert m2.calls == []
    assert json.loads((out / "_done.json").read_text())["head"] == "nms"


def test_nms_head_uses_library_default(tmp_path):
    m = FakeModel()
    ps.predict_to_dota("w.pt", _images(tmp_path, ["a"]), tmp_path / "p", "nms", model=m)
    assert m.calls[0][1]["nms"] is None


def test_rejects_unknown_class_names(tmp_path):
    m = FakeModel()
    m.names = {0: "car"}
    with pytest.raises(ValueError, match="car"):
        ps.predict_to_dota("w.pt", _images(tmp_path, ["a"]), tmp_path / "p", "e2e", model=m)


def test_fates_run_on_written_files(tmp_path):
    lab = tmp_path / "labels"
    lab.mkdir()
    pts = "10 10 20 10 20 20 10 20"
    (lab / "a.txt").write_text(f"{pts} vehicle 0\n100 100 110 100 110 110 100 110 vehicle 0\n")
    img = _images(tmp_path, ["a"])
    out = tmp_path / "pred"
    ps.predict_to_dota("w.pt", img, out, "e2e", model=FakeModel())
    r = re_.fates_run(lab, ["a"], out, 0.25)
    assert list(r["fate"]) == ["detected", "miss"] and list(r["gt"]) == [0, 1]


def frame(arms=("A0", "A8", "A2"), seeds=(1, 2, 3), n=2000, rec=None, fates=None, rng_seed=0):
    """Very tiny GTs, half starved under A0, half dense. rec(arm, starved, dense) gives recall."""
    rng = np.random.default_rng(rng_seed)
    out = []
    for s in seeds:
        for a in arms:
            starved = np.arange(n) % 2 == 0
            dense = np.arange(n) % 4 < 2
            p = np.array([rec(a, st, de) for st, de in zip(starved, dense)])
            det = rng.random(n) < p
            f = np.where(det, "detected", rng.choice(list(fates), size=n, p=list(fates.values())))
            out.append(pd.DataFrame(dict(arm=a, seed=s, bin="vt", starved_A0=starved,
                                         density=np.where(dense, ">=3", "isolated"), detected=det, fate=f)))
    return pd.concat(out, ignore_index=True)


FOCUSED = {"loc": 0.8, "miss": 0.2}
MISS_HEAVY = {"miss": 0.8, "loc": 0.2}
SPREAD = {"miss": 0.34, "loc": 0.33, "cls": 0.33}
FLAT = lambda a, st, de: 0.3  # noqa: E731


def test_clear_case_trains_with_a8():
    rec = lambda a, st, de: 0.5 + (0.2 if st and a != "A0" else 0) + (0.2 if de and a == "A2" else 0)  # noqa: E731
    d = frame(rec=rec, fates=FOCUSED)
    r = ed.decide(d, d)
    assert r["verdict"] == "train" and r["C2_reason"]["top"] == "loc"
    assert r["arms_if_training"] == ["A0", "A8", "A2"] and r["runs_if_training"] == 6


def test_no_density_contrast_drops_a8():
    rec = lambda a, st, de: 0.3 + (0.2 if st and a != "A0" else 0)  # noqa: E731
    d = frame(rec=rec, fates=FOCUSED, n=20000)
    r = ed.decide(d, d)
    assert r["verdict"] == "train" and r["arms_if_training"] == ["A0", "A2"] and r["runs_if_training"] == 4


def test_no_rescue_and_no_reason_stops():
    d = frame(rec=FLAT, fates=SPREAD, n=20000)
    assert ed.decide(d, d)["verdict"] == "do_not_train_yet"


def test_miss_cannot_pass_c2():
    d = frame(rec=FLAT, fates=MISS_HEAVY, n=20000)
    r = ed.decide(d, d)
    assert r["C2_reason"]["top"] == "miss" and not r["C2_reason"]["passed"]
    assert r["verdict"] == "do_not_train_yet"


def test_either_criterion_alone_trains():
    d = frame(rec=FLAT, fates=FOCUSED, n=20000)
    assert ed.decide(d, d)["verdict"] == "train"
    rescue_only = lambda a, st, de: 0.3 + (0.2 if st and a != "A0" else 0)  # noqa: E731
    d = frame(rec=rescue_only, fates=SPREAD, n=20000)
    assert ed.decide(d, d)["verdict"] == "train"


def test_scope_drops_low_score_level_when_over_budget():
    n_val = ed.N_GT_TEST // 10
    assert ed.test_scope(60, n_val, 15)["scores"] == [0.25, 0.05]  # 60 s x 10 x 15 = 2.5 h per level
    assert ed.test_scope(200, n_val, 15)["scores"] == [0.25]  # 8.3 h per level


def test_module_docstring_states_thresholds_are_design():
    assert "[design]" in Path(ed.__file__).read_text(encoding="utf-8")
