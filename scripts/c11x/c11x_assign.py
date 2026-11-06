"""Quy tắc vùng ứng viên cho RotatedTaskAlignedAssigner của Ultralytics 8.4.174, và bộ ghi số mẫu dương theo GT.

Module độc lập: không import `scripts/c11` (bản trên Drive). Tên arm A0/A1/A8/A2 theo proposal v2.1 (C-11):

| Arm | Quy tắc cho hộp thay thế, chỉ dùng ở bước chọn ứng viên |
|---|---|
| A0 | không có sàn (giữ nguyên hộp GT) |
| A1 | cạnh < 8 → 16 (STAL-8) |
| A8 | cạnh < 8·√2 → 8·√2 (sàn phủ tối thiểu ở stride 8) |
| A2 | cạnh < 16 → 16 (STAL-16, đúng mã gốc của 8.4.174) |
| K<k> | sàn thích nghi theo số ứng viên: mỗi GT lấy sàn nhỏ nhất trong `K_LADDER` để có ≥ k ứng viên |

Quy tắc K chỉ bảo đảm ≥ k **ứng viên**. Mẫu dương cuối cùng còn qua top-k (o2m: 10; o2o: 7 rồi giữ 1) và xử lý
xung đột, nên số mẫu dương được đo riêng bằng `PositiveRecorder`.

Cách dùng khi train (một tiến trình, một GPU):

    import c11x_assign as ca
    ca.apply_arm("K3")      # vá class RotatedTaskAlignedAssigner, trước khi tạo trainer
    ...train...
    ca.remove_patch()
"""

from __future__ import annotations

import math
import re
from contextlib import contextmanager

import torch

ULTRALYTICS_VERSION = "8.4.174"
SQRT2 = math.sqrt(2.0)

# (ngưỡng, giá trị): cạnh < ngưỡng thì thay bằng giá trị. None = không có sàn.
FIXED_ARMS: dict[str, tuple[float, float] | None] = {
    "A0": None,
    "A1": (8.0, 16.0),
    "A8": (8.0 * SQRT2, 8.0 * SQRT2),
    "A2": (16.0, 16.0),
}
# Các mức sàn thử lần lượt cho quy tắc K (px, cạnh của hộp thay thế). Lồng nhau: sàn lớn hơn chứa sàn nhỏ hơn.
K_LADDER: tuple[float, ...] = (8.0, 8.0 * SQRT2, 16.0, 16.0 * SQRT2, 32.0, 32.0 * SQRT2, 64.0)

STATE: dict = {"arm": None, "rule": None, "calls": 0, "orig": None, "kstats": None}


def parse_arm(arm: str) -> dict:
    """Đổi tên arm thành quy tắc. 'A0' → {'kind': 'none'}; 'A2' → fixed; 'K3' → kcand với k = 3."""
    if arm in FIXED_ARMS:
        fl = FIXED_ARMS[arm]
        return {"kind": "none"} if fl is None else {"kind": "fixed", "thr": fl[0], "val": fl[1]}
    m = re.fullmatch(r"K(\d+)", arm)
    if m and int(m.group(1)) >= 1:
        return {"kind": "kcand", "k": int(m.group(1)), "ladder": K_LADDER}
    raise ValueError(f"arm không hợp lệ: {arm!r} (dùng A0/A1/A8/A2 hoặc K<k>, k ≥ 1)")


def floor_boxes(gt_bboxes: torch.Tensor, mask_gt: torch.Tensor, thr: float, val: float) -> torch.Tensor:
    """Hộp thay thế kiểu STAL: cạnh (w, h) < thr thì thay bằng val. gt_bboxes: (b, n, 5) xywhr, px."""
    out = gt_bboxes.clone()
    small = (out[..., 2:4] < thr) & mask_gt.bool()
    out[..., 2:4] = torch.where(small, torch.tensor(val, dtype=out.dtype, device=out.device), out[..., 2:4])
    return out


def points_in_rboxes(xy_centers: torch.Tensor, boxes: torch.Tensor) -> torch.Tensor:
    """Phép thử điểm-trong-hộp xoay, chép đúng phép tính của RotatedTaskAlignedAssigner 8.4.174. → (b, n, h*w)."""
    from ultralytics.utils.ops import xywhr2xyxyxyxy

    corners = xywhr2xyxyxyxy(boxes)
    a, b, _, d = corners.split(1, dim=-2)
    ab = b - a
    ad = d - a
    apx = xy_centers[:, 0] - a[..., 0]
    apy = xy_centers[:, 1] - a[..., 1]
    norm_ab = (ab * ab).sum(dim=-1)
    norm_ad = (ad * ad).sum(dim=-1)
    ap_dot_ab = apx * ab[..., 0] + apy * ab[..., 1]
    ap_dot_ad = apx * ad[..., 0] + apy * ad[..., 1]
    return (ap_dot_ab >= 0) & (ap_dot_ab <= norm_ab) & (ap_dot_ad >= 0) & (ap_dot_ad <= norm_ad)


def candidate_mask(xy_centers, gt_bboxes, mask_gt, rule: dict, stats: dict | None = None) -> torch.Tensor:
    """Mặt nạ ứng viên (b, n, h*w) theo quy tắc. Với 'kcand', ghi vào `stats` (nếu có) số GT phải nới theo từng mức."""
    if rule["kind"] == "none":
        return points_in_rboxes(xy_centers, gt_bboxes)
    if rule["kind"] == "fixed":
        return points_in_rboxes(xy_centers, floor_boxes(gt_bboxes, mask_gt, rule["thr"], rule["val"]))
    if rule["kind"] != "kcand":
        raise ValueError(rule)
    valid = mask_gt.bool().squeeze(-1)  # (b, n)
    mask = points_in_rboxes(xy_centers, gt_bboxes)
    count = mask.sum(-1)
    level = torch.zeros_like(count)  # 0 = giữ hộp gốc; i = dùng K_LADDER[i - 1]
    for i, f in enumerate(rule["ladder"], start=1):
        need = (count < rule["k"]) & valid
        if not bool(need.any()):
            break
        m_f = points_in_rboxes(xy_centers, floor_boxes(gt_bboxes, mask_gt, f, f))
        mask = torch.where(need.unsqueeze(-1), m_f, mask)
        level = torch.where(need, torch.full_like(level, i), level)
        count = mask.sum(-1)
    if stats is not None:
        n_levels = len(rule["ladder"]) + 1
        hist = torch.bincount(level[valid].flatten(), minlength=n_levels)
        short = (count < rule["k"]) & valid  # vẫn thiếu sau mức sàn lớn nhất
        if stats.get("level_hist") is None:
            stats["level_hist"] = hist
            stats["still_short"] = short.sum()
        else:
            stats["level_hist"] = stats["level_hist"] + hist
            stats["still_short"] = stats["still_short"] + short.sum()
    return mask


def _patched_select(self, xy_centers, gt_bboxes, mask_gt):
    STATE["calls"] += 1
    return candidate_mask(xy_centers, gt_bboxes, mask_gt, STATE["rule"], STATE["kstats"])


def check_version() -> None:
    import ultralytics

    if ultralytics.__version__ != ULTRALYTICS_VERSION:
        raise RuntimeError(
            f"c11x_assign viết cho ultralytics=={ULTRALYTICS_VERSION}, đang có {ultralytics.__version__}. "
            "Quy tắc STAL cho OBB đổi theo phiên bản; không chạy trên bản khác."
        )


def apply_arm(arm: str) -> dict:
    """Vá RotatedTaskAlignedAssigner.select_candidates_in_gts theo arm. Gọi lại với arm khác thì thay quy tắc."""
    check_version()
    from ultralytics.utils.tal import RotatedTaskAlignedAssigner as R

    rule = parse_arm(arm)
    if STATE["orig"] is None:
        STATE["orig"] = R.select_candidates_in_gts
    R.select_candidates_in_gts = _patched_select
    STATE.update(arm=arm, rule=rule, calls=0, kstats={} if rule["kind"] == "kcand" else None)
    return rule


def remove_patch() -> None:
    from ultralytics.utils.tal import RotatedTaskAlignedAssigner as R

    if STATE["orig"] is not None:
        R.select_candidates_in_gts = STATE["orig"]
    STATE.update(arm=None, rule=None, calls=0, orig=None, kstats=None)


def pop_kstats() -> dict | None:
    """Lấy và xoá thống kê quy tắc K đã tích luỹ (để ghi theo epoch). None nếu arm không phải K."""
    ks = STATE.get("kstats")
    if not ks or ks.get("level_hist") is None:
        return None
    out = {"level_hist": ks["level_hist"].tolist(), "still_short": int(ks["still_short"]),
           "ladder_px": [0.0, *STATE["rule"]["ladder"]]}
    STATE["kstats"] = {}
    return out


# ---------------------------------------------------------------- bộ ghi số mẫu dương theo GT (hướng 2)


def _assigners(criterion) -> dict:
    """{'o2m': assigner, 'o2o': assigner} cho E2ELoss của YOLO26; {'single': assigner} nếu chỉ có một nhánh."""
    if hasattr(criterion, "one2many") and hasattr(criterion, "one2one"):
        return {"o2m": criterion.one2many.assigner, "o2o": criterion.one2one.assigner}
    return {"single": criterion.assigner}


class PositiveRecorder:
    """Ghi theo từng lần gọi assigner: số ứng viên, mẫu dương trước xung đột và mẫu dương cuối cho mỗi GT hợp lệ.

    Bọc phương thức ở mức **instance** (không đổi class), nên chạy được cùng `apply_arm`. Mỗi bản ghi:
    {'branch', 'n_cand', 'n_pos_pre', 'n_pos', 'valid'}: mảng numpy (b, n_max) theo thứ tự GT sau bước lọc < 2 px
    của v8OBBLoss.
    """

    def __init__(self, criterion):
        self.assigners = _assigners(criterion)
        self.records: list[dict] = []
        self._tmp: dict = {}

    def _wrap(self, name, asg):
        orig_sel, orig_pos, orig_fwd = asg.select_candidates_in_gts, asg.get_pos_mask, asg._forward

        def sel(xy_centers, gt_bboxes, mask_gt, *a, **k):
            m = orig_sel(xy_centers, gt_bboxes, mask_gt, *a, **k)
            self._tmp[name] = {"n_cand": m.sum(-1)}
            return m

        def pos(*a, **k):
            mask_pos, align, ov = orig_pos(*a, **k)
            self._tmp[name]["n_pos_pre"] = mask_pos.sum(-1)
            return mask_pos, align, ov

        def fwd(pd_scores, pd_bboxes, anc_points, gt_labels, gt_bboxes, mask_gt):
            res = orig_fwd(pd_scores, pd_bboxes, anc_points, gt_labels, gt_bboxes, mask_gt)
            fg, tgi = res[3], res[4]
            n_pos = torch.zeros(gt_bboxes.shape[:2], dtype=torch.long, device=fg.device)
            n_pos.scatter_add_(1, tgi.long(), fg.long())
            t = self._tmp.pop(name)
            self.records.append({
                "branch": name,
                "n_cand": t["n_cand"].cpu().numpy(),
                "n_pos_pre": t["n_pos_pre"].cpu().numpy(),
                "n_pos": n_pos.cpu().numpy(),
                "valid": mask_gt.bool().squeeze(-1).cpu().numpy(),
            })
            return res

        asg.select_candidates_in_gts, asg.get_pos_mask, asg._forward = sel, pos, fwd


    @contextmanager
    def active(self):
        for n, a in self.assigners.items():
            self._wrap(n, a)
        try:
            yield self
        finally:
            for n, a in self.assigners.items():
                for attr in ("select_candidates_in_gts", "get_pos_mask", "_forward"):
                    a.__dict__.pop(attr, None)
            self._tmp.clear()
