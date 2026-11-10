"""Rough pass rates of the A8 rule from the seed spread seen on seeds 1-3 (test, e2e). Estimates only."""
import numpy as np

rng = np.random.default_rng(0)
N = 200_000


def sd3(lo, hi, mean):
    mid = 3 * mean - lo - hi
    return np.std([lo, mid, hi], ddof=1)


sd_vt_a8a0 = sd3(0.0042, 0.0115, 0.0071)      # A8-A0 AP_vt
sd_m_a8a2 = sd3(-0.0039, 0.0222, 0.0054)      # A8-A2 AP_m = -(A2-A8)
sd_vt_a8a2 = sd3(-0.0100, 0.0045, -0.0019)    # A8-A2 AP_vt
print("sd per seed:", round(sd_vt_a8a0, 4), round(sd_m_a8a2, 4), round(sd_vt_a8a2, 4))


def rate(true, sd, n, thr, both_pos=True):
    d = rng.normal(true, sd, size=(N, n))
    ok = d.mean(1) >= thr
    if both_pos:
        ok &= (d > 0).all(1)
    return ok.mean()


for n in (2, 3):
    print(f"n seeds = {n}")
    print("  (a) A8-A0 AP_vt, true 0.0071:", round(rate(0.0071, sd_vt_a8a0, n, 0.006), 2),
          "| true 0:", round(rate(0.0, sd_vt_a8a0, n, 0.006), 3))
    for t in (0.0, 0.0054, 0.010):
        print(f"  (b) A8-A2 AP_m, true {t}:", round(rate(t, sd_m_a8a2, n, 0.005), 2))
    for t in (-0.0019, 0.0):
        print(f"  (c) A8-A2 AP_vt mean >= -0.006, true {t}:", round(rate(t, sd_vt_a8a2, n, -0.006, both_pos=False), 2))
