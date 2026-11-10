"""Luật của phụ lục A3 (preregistration): kiểm môi trường R1 và phán quyết P2 cho sàn phủ tối thiểu A8.

Tách khỏi notebook để test được trên máy. Notebook `C11x_train_a8_colab.ipynb` chỉ gọi các hàm ở đây.
"""

from __future__ import annotations

MEI_VT = 0.006      # §3 của preregistration
TOL_R = 0.005       # cùng ngưỡng tái lập với phụ lục A2 mục 5
SEEDS = (4, 5)
GROUP_OLD, GROUP_NEW = "runs-woX", "runs-woX-A8"


def r1_check(ap_new: float, ap_old: float, val_new: float | None, val_old: float | None, tol: float = TOL_R) -> dict:
    """R1 = train lại A2 seed 4 trong môi trường hiện tại, so với `c11_A2_s4` đã train ngày 07/11.

    Khớp khi |Δ AP test e2e| ≤ tol và |Δ mAP50-95 val ở epoch cuối| ≤ tol. Thiếu số val thì tính là không khớp.
    """
    out = {"ap_new": ap_new, "ap_old": ap_old, "d_ap": ap_new - ap_old, "tol": tol}
    if val_new is None or val_old is None:
        out.update(d_val_last=None, match=False, note="thiếu results.csv: không kiểm được val, tính là không khớp")
        return out
    out["d_val_last"] = val_new - val_old
    out["match"] = abs(out["d_ap"]) <= tol and abs(out["d_val_last"]) <= tol
    return out


def jobs(match: bool) -> tuple[str, list[tuple[str, int]]]:
    """Nhóm run dùng để phán quyết và các run còn phải train sau R1.

    R1 luôn ghi vào `runs-woX-A8/c11_A2_s4`. Khớp: A8 × seed 4, 5 ghi cạnh A0, A2 cũ trong `runs-woX`.
    Không khớp: train đủ A0, A8, A2 × seed 4, 5 trong `runs-woX-A8`; R1 chính là A2 seed 4 của nhóm này.
    """
    if match:
        return GROUP_OLD, [("A8", s) for s in SEEDS]
    return GROUP_NEW, [(a, s) for s in SEEDS for a in ("A0", "A8", "A2") if (a, s) != ("A2", 4)]


def _two(d: dict) -> tuple[float, float]:
    missing = [s for s in SEEDS if s not in d]
    if missing:
        raise ValueError(f"thiếu seed {missing}")
    return float(d[SEEDS[0]]), float(d[SEEDS[1]])


def p2_verdict(a8_a0_vt: dict, a8_a2_vt: dict, a8_a2_m: dict) -> dict:
    """Phán quyết P2 trên seed 4 và 5. Mỗi tham số là {seed: Δ}.

    P2a (chính): Δ AP_vt(A8 − A0) > 0 ở cả hai seed và trung bình ≥ MEI_vt. Cùng luật với P1.
    P2b (phụ): trung bình Δ AP_vt(A8 − A2) ≥ −MEI_vt.
    AP_m (A8 − A2) chỉ mô tả: hai seed không đủ để phán quyết (xem phụ lục A3).
    """
    a = _two(a8_a0_vt)
    mean_a = sum(a) / 2
    pos = all(x > 0 for x in a)
    p2a = "Lặp lại được" if pos and mean_a >= MEI_VT else "Có hướng nhưng dưới MEI" if pos else "Không lặp lại"
    b = _two(a8_a2_vt)
    mean_b = sum(b) / 2
    m = _two(a8_a2_m)
    return {
        "P2a": {"verdict": p2a, "s4": a[0], "s5": a[1], "mean": mean_a, "mei": MEI_VT},
        "P2b": {"holds": mean_b >= -MEI_VT, "s4": b[0], "s5": b[1], "mean": mean_b, "margin": -MEI_VT},
        "AP_m_A8-A2_descriptive": {"s4": m[0], "s5": m[1], "mean": sum(m) / 2},
    }
