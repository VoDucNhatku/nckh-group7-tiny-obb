"""Train thật trên CPU với dataset 4 ảnh (chậm, khoảng 1–2 phút). Kiểm file run, resume sau khi bị ngắt, file done."""

import json

import pytest

import c11x_assign as ca
import c11x_train as ct

RECIPE = {**ct.RECIPE_C11, "imgsz": 128, "epochs": 2, "batch": 2, "workers": 0, "amp": False}


class Interrupt(Exception):
    pass


def test_recipe_matches_itself_and_reports_diff():
    assert ct.check_recipe(dict(ct.RECIPE_C11)) == []
    assert ct.check_recipe({**ct.RECIPE_C11, "epochs": 100, "extra": 1}) == ["epochs", "extra"]


def test_train_interrupt_resume_done(tiny_dataset, tmp_path):
    def boom(trainer):
        if trainer.epoch == 0:
            raise Interrupt  # sau khi đã lưu last.pt của epoch 1, như Colab ngắt

    with pytest.raises(Interrupt):
        ct.train_arm(tiny_dataset, "K2", 4, tmp_path, recipe=RECIPE, device="cpu", init_weights=None,
                     extra_callbacks={"on_fit_epoch_end": boom})
    rd = tmp_path / "c11x_K2_s4"
    assert (rd / "weights" / "last.pt").exists() and not (rd / "c11x_done.json").exists()
    assert ca.STATE["rule"] is None  # bản vá được gỡ cả khi lỗi

    ct.train_arm(tiny_dataset, "K2", 4, tmp_path, recipe=RECIPE, device="cpu", init_weights=None)
    done = json.loads((rd / "c11x_done.json").read_text())
    assert done["arm"] == "K2" and done["seed"] == 4 and done["epochs"] == 2 and done["batch_changed"] is False
    ks = [json.loads(x) for x in (rd / "c11x_kstats.jsonl").read_text().splitlines()]
    assert [k["epoch"] for k in ks] == [1, 2]
    assert all(k["still_short"] == 0 and sum(k["level_hist"]) > 0 for k in ks)
    meta = json.loads((rd / "c11x_arm.json").read_text())
    assert meta["rule"] == {"kind": "kcand", "k": 2, "ladder": list(ca.K_LADDER)}

    # đã xong: gọi lại thì bỏ qua; mất file done (ngắt sau epoch cuối) thì ghi lại mà không train
    assert ct.train_arm(tiny_dataset, "K2", 4, tmp_path, recipe=RECIPE, device="cpu", init_weights=None) == rd
    (rd / "c11x_done.json").unlink()
    ct.train_arm(tiny_dataset, "K2", 4, tmp_path, recipe=RECIPE, device="cpu", init_weights=None)
    assert json.loads((rd / "c11x_done.json").read_text())["batch_actual"] is None


def test_wrong_run_dir_is_refused(tiny_dataset, tmp_path):
    rd = tmp_path / "c11x_A2_s5"
    rd.mkdir()
    (rd / "c11x_arm.json").write_text(json.dumps({"arm": "A8", "seed": 5}))
    with pytest.raises(AssertionError):
        ct.train_arm(tiny_dataset, "A2", 5, tmp_path, recipe=RECIPE, device="cpu", init_weights=None)
