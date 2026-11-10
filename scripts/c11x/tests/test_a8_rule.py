import pytest

import a8_rule as ar


def test_r1_match_and_mismatch():
    assert ar.r1_check(0.135, 0.133, 0.300, 0.297)["match"]
    assert not ar.r1_check(0.135, 0.133, 0.300, 0.280)["match"]       # val lệch 0,02 như R0
    assert not ar.r1_check(0.140, 0.133, 0.300, 0.300)["match"]       # test lệch 0,007
    r = ar.r1_check(0.135, 0.133, None, 0.297)
    assert not r["match"] and r["d_val_last"] is None


def test_jobs_match_trains_only_a8():
    group, todo = ar.jobs(True)
    assert group == "runs-woX" and todo == [("A8", 4), ("A8", 5)]


def test_jobs_mismatch_trains_full_group_reusing_r1():
    group, todo = ar.jobs(False)
    assert group == "runs-woX-A8"
    assert ("A2", 4) not in todo and len(todo) == 5
    assert set(todo) | {("A2", 4)} == {(a, s) for a in ("A0", "A8", "A2") for s in (4, 5)}


@pytest.mark.parametrize("vt,expected", [
    ({4: 0.008, 5: 0.007}, "Lặp lại được"),
    ({4: 0.004, 5: 0.003}, "Có hướng nhưng dưới MEI"),
    ({4: 0.020, 5: -0.001}, "Không lặp lại"),
    ({4: 0.006, 5: 0.006}, "Lặp lại được"),
])
def test_p2a_labels(vt, expected):
    out = ar.p2_verdict(vt, {4: 0.0, 5: 0.0}, {4: 0.0, 5: 0.0})
    assert out["P2a"]["verdict"] == expected


def test_p2b_margin_and_descriptive_ap_m():
    out = ar.p2_verdict({4: 0.008, 5: 0.008}, {4: -0.010, 5: -0.001}, {4: 0.01, 5: -0.02})
    assert out["P2b"]["holds"]                      # trung bình −0,0055 ≥ −0,006
    out = ar.p2_verdict({4: 0.008, 5: 0.008}, {4: -0.010, 5: -0.004}, {4: 0.01, 5: -0.02})
    assert not out["P2b"]["holds"]                  # trung bình −0,007
    assert out["AP_m_A8-A2_descriptive"]["mean"] == pytest.approx(-0.005)
    assert "verdict" not in out["AP_m_A8-A2_descriptive"]


def test_p2_requires_both_seeds():
    with pytest.raises(ValueError):
        ar.p2_verdict({4: 0.01}, {4: 0.0, 5: 0.0}, {4: 0.0, 5: 0.0})
