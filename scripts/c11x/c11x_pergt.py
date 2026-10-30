"""Phân tích theo từng GT cho hướng 2 (số mẫu dương → recall) và hướng 4 (sai số góc theo kích thước).

Đầu vào: trọng số `last.pt` của một run, dataset YOLO woX đã dựng (thư mục `yolo_woX/`, file `aitodr.yaml`).
Không cần `scripts/c11`.

Ba bước, mỗi bước ghi một bảng theo GT (khoá: `im_file`, `gt_idx`):

1. `record_assignment`: đưa ảnh val qua loss của mô hình đã train (eval, không gradient), với quy tắc vùng ứng viên
   của arm. Ghi số ứng viên, mẫu dương trước xung đột và mẫu dương cuối cho cả hai nhánh o2m/o2o.
   Đây là phép gán **tại checkpoint cuối**, không phải trung bình trong lúc train (xem kế hoạch, H2-giới hạn).
2. `predict_and_match`: predict ảnh gốc (head e2e hoặc nms), khớp tham lam theo điểm, theo lớp, ở IoU đa giác ≥ 0,5.
   Ghi điểm của dự đoán khớp, IoU, sai số góc.
3. `fit_recall_models`: hồi quy logistic "được phát hiện ở ngưỡng điểm τ" theo số mẫu dương và kích thước/stride P3,
   sai số chuẩn cụm theo ảnh.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd

P3_STRIDE = 8.0


# ---------------------------------------------------------------- hình học


def xywhr_to_poly(xywhr: np.ndarray) -> np.ndarray:
    """(N, 5) xywhr (r: radian) → (N, 4, 2) đỉnh. Cùng quy ước với ultralytics.utils.ops.xywhr2xyxyxyxy."""
    x, y, w, h, r = (xywhr[:, i] for i in range(5))
    c, s = np.cos(r), np.sin(r)
    v1 = np.stack([w / 2 * c, w / 2 * s], -1)
    v2 = np.stack([-h / 2 * s, h / 2 * c], -1)
    ctr = np.stack([x, y], -1)
    return np.stack([ctr + v1 + v2, ctr + v1 - v2, ctr - v1 - v2, ctr - v1 + v2], 1)


def long_side_angle(xywhr: np.ndarray) -> np.ndarray:
    """Góc của trục cạnh dài, quy về [0, π). Hộp xoay 90° với w↔h cho cùng giá trị."""
    w, h, r = xywhr[:, 2], xywhr[:, 3], xywhr[:, 4]
    a = np.where(w >= h, r, r + np.pi / 2)
    return np.mod(a, np.pi)


def angle_error_deg(gt_xywhr: np.ndarray, pd_xywhr: np.ndarray) -> np.ndarray:
    """|Δθ| giữa hai trục cạnh dài, tính theo chu kỳ π, đơn vị độ, trong [0, 90]."""
    d = np.abs(long_side_angle(gt_xywhr) - long_side_angle(pd_xywhr))
    d = np.minimum(d, np.pi - d)
    return np.degrees(d)


def poly_iou_matrix(polys_a: np.ndarray, polys_b: np.ndarray) -> np.ndarray:
    """IoU đa giác (shapely) giữa (Na, 4, 2) và (Nb, 4, 2) → (Na, Nb)."""
    import shapely

    if len(polys_a) == 0 or len(polys_b) == 0:
        return np.zeros((len(polys_a), len(polys_b)))
    ga = shapely.polygons(polys_a)
    gb = shapely.polygons(polys_b)
    ga = shapely.make_valid(ga)
    gb = shapely.make_valid(gb)
    inter = shapely.area(shapely.intersection(ga[:, None], gb[None, :]))
    union = shapely.area(ga)[:, None] + shapely.area(gb)[None, :] - inter
    return np.where(union > 0, inter / np.maximum(union, 1e-12), 0.0)


def greedy_match(gt_polys, gt_cls, pd_polys, pd_cls, pd_conf, iou_thr=0.5):
    """Khớp tham lam kiểu COCO ở một ngưỡng IoU: theo lớp, dự đoán điểm cao trước, mỗi GT/dự đoán dùng một lần.

    Trả về (match_pd, match_iou): chỉ số dự đoán khớp với từng GT (-1 nếu không có) và IoU tương ứng.
    """
    n = len(gt_polys)
    match_pd = np.full(n, -1, dtype=np.int64)
    match_iou = np.zeros(n)
    for c in np.unique(gt_cls):
        gi = np.flatnonzero(gt_cls == c)
        pi = np.flatnonzero(pd_cls == c)
        if len(pi) == 0:
            continue
        pi = pi[np.argsort(-pd_conf[pi], kind="stable")]
        iou = poly_iou_matrix(gt_polys[gi], pd_polys[pi])  # (ng, np)
        free = np.ones(len(gi), dtype=bool)
        for j in range(len(pi)):
            cand = np.where(free, iou[:, j], -1.0)
            k = int(np.argmax(cand))
            if cand[k] >= iou_thr:
                free[k] = False
                match_pd[gi[k]] = pi[j]
                match_iou[gi[k]] = cand[k]
            if not free.any():
                break
    return match_pd, match_iou


def nearest_neighbour_px(xy: np.ndarray) -> np.ndarray:
    """Khoảng cách tâm tới GT gần nhất trong cùng ảnh (px); inf nếu ảnh chỉ có một GT."""
    if len(xy) < 2:
        return np.full(len(xy), np.inf)
    d = np.sqrt(((xy[:, None, :] - xy[None, :, :]) ** 2).sum(-1))
    np.fill_diagonal(d, np.inf)
    return d.min(1)


# ---------------------------------------------------------------- bước 1: gán mẫu tại checkpoint cuối


def _model_for_loss(weights, device):
    import torch
    from ultralytics import YOLO
    from ultralytics.utils import DEFAULT_CFG_DICT, IterableSimpleNamespace

    model = YOLO(str(weights)).model
    ck_args = model.args if isinstance(model.args, dict) else vars(model.args)
    model.args = IterableSimpleNamespace(**{**DEFAULT_CFG_DICT, **ck_args})
    model = model.to(device).float().eval()
    model.criterion = model.init_criterion()
    torch.set_grad_enabled(False)
    return model


def val_loader(data_yaml, split="val", imgsz=800, batch=16, workers=4):
    """Dataloader không augmentation, giống bước val của Ultralytics (LetterBox imgsz, không rect)."""
    from ultralytics.cfg import get_cfg
    from ultralytics.data import build_dataloader, build_yolo_dataset
    from ultralytics.data.utils import check_det_dataset

    data = check_det_dataset(str(data_yaml))
    cfg = get_cfg(overrides=dict(task="obb", imgsz=imgsz, rect=False, fraction=1.0))
    ds = build_yolo_dataset(cfg, data[split], batch, data, mode="val", rect=False, stride=32)
    return build_dataloader(ds, batch, workers, shuffle=False, rank=-1)


def record_assignment(weights, data_yaml, arm, split="val", device="cuda:0", batch=16, workers=4) -> pd.DataFrame:
    """Một dòng cho mỗi GT của split: kích thước (px, ảnh gốc), số ứng viên / mẫu dương cho o2m và o2o."""
    import torch

    import c11x_assign as ca

    ca.apply_arm(arm)
    try:
        model = _model_for_loss(weights, device)
        rec = ca.PositiveRecorder(model.criterion)
        rows = []
        for b in val_loader(data_yaml, split, batch=batch, workers=workers):
            img = b["img"].to(device).float() / 255
            H, W = img.shape[2:]
            bb, bi, cl = b["bboxes"], b["batch_idx"].long(), b["cls"].view(-1).long()
            batch_t = {"img": img, "batch_idx": b["batch_idx"].to(device), "cls": b["cls"].to(device),
                       "bboxes": bb.to(device)}
            rec.records.clear()
            with rec.active():
                model.loss(batch_t)
            per_branch = {r["branch"]: r for r in rec.records}
            keep = (bb[:, 2] * W >= 2) & (bb[:, 3] * H >= 2)  # đúng bộ lọc của v8OBBLoss
            for i in range(img.shape[0]):
                sel = (bi == i).nonzero().view(-1)
                kept = sel[keep[sel]]
                (gh, gw), (left, top) = b["ratio_pad"][i]
                px = bb[sel].clone().numpy()
                px[:, 0] = (px[:, 0] * W - left) / gw
                px[:, 1] = (px[:, 1] * H - top) / gh
                px[:, 2] = px[:, 2] * W / gw
                px[:, 3] = px[:, 3] * H / gh
                nn_d = nearest_neighbour_px(px[:, :2])
                slot = {int(g): s for s, g in enumerate(kept.tolist())}
                for j, g in enumerate(sel.tolist()):
                    w, h = float(px[j, 2]), float(px[j, 3])
                    row = dict(im_file=Path(b["im_file"][i]).name, gt_idx=j, cls=int(cl[g]),
                               x=float(px[j, 0]), y=float(px[j, 1]), w=w, h=h, r=float(px[j, 4]),
                               short=min(w, h), long=max(w, h), n_gt_img=len(sel), nn_px=float(nn_d[j]),
                               in_loss=g in slot)
                    for br, r in per_branch.items():
                        s = slot.get(g)
                        for key in ("n_cand", "n_pos_pre", "n_pos"):
                            row[f"{br}_{key}"] = int(r[key][i, s]) if s is not None else -1
                    rows.append(row)
        df = pd.DataFrame(rows)
        df["arm"] = arm
        return df
    finally:
        ca.remove_patch()
        torch.set_grad_enabled(True)


# ---------------------------------------------------------------- bước 2: predict + khớp + góc


def read_gt_from_yolo_labels(label_file: Path, img_w: int, img_h: int) -> tuple[np.ndarray, np.ndarray]:
    """Nhãn YOLO-OBB (cls x1 y1 ... x4 y4, chuẩn hoá) → (cls (N,), poly (N, 4, 2) px)."""
    rows = [ln.split() for ln in label_file.read_text().splitlines() if ln.strip()]
    if not rows:
        return np.zeros(0, dtype=np.int64), np.zeros((0, 4, 2))
    a = np.array(rows, dtype=np.float64)
    poly = a[:, 1:9].reshape(-1, 4, 2) * np.array([img_w, img_h])
    return a[:, 0].astype(np.int64), poly


def predict_and_match(weights, pergt: pd.DataFrame, images_dir, head="e2e", imgsz=800, conf=0.001,
                      max_det=12000, iou_thr=0.5, batch=16, device=0) -> pd.DataFrame:
    """Thêm vào bảng theo GT: điểm của dự đoán khớp (0 nếu không khớp), IoU, sai số góc (độ).

    `pergt` lấy từ `record_assignment` (cần cột x, y, w, h, r, cls, im_file, gt_idx). Hộp GT dùng đúng xywhr mà
    loader của Ultralytics sinh ra, nên khớp với hộp đã dùng khi gán mẫu.
    """
    from ultralytics import YOLO

    model = YOLO(str(weights))
    nms = False if head == "e2e" else None
    out = []
    files = sorted(pergt["im_file"].unique())
    src = [str(Path(images_dir) / f) for f in files]
    g_by_img = dict(tuple(pergt.groupby("im_file", sort=False)))
    for res in model.predict(src, imgsz=imgsz, conf=conf, max_det=max_det, nms=nms, batch=batch, device=device,
                             stream=True, verbose=False):
        name = Path(res.path).name
        g = g_by_img[name].sort_values("gt_idx")
        gx = g[["x", "y", "w", "h", "r"]].to_numpy()
        ob = res.obb
        pd_xywhr = ob.xywhr.cpu().numpy() if ob is not None and len(ob) else np.zeros((0, 5))
        pd_cls = ob.cls.cpu().numpy().astype(np.int64) if ob is not None and len(ob) else np.zeros(0, np.int64)
        pd_conf = ob.conf.cpu().numpy() if ob is not None and len(ob) else np.zeros(0)
        mp, mi = greedy_match(xywhr_to_poly(gx), g["cls"].to_numpy(), xywhr_to_poly(pd_xywhr), pd_cls, pd_conf,
                              iou_thr)
        hit = mp >= 0
        ang = np.full(len(g), np.nan)
        if hit.any():
            ang[hit] = angle_error_deg(gx[hit], pd_xywhr[mp[hit]])
        out.append(pd.DataFrame(dict(im_file=name, gt_idx=g["gt_idx"].to_numpy(),
                                     score=np.where(hit, pd_conf[np.maximum(mp, 0)] if len(pd_conf) else 0, 0.0),
                                     match_iou=mi, angle_err_deg=ang)))
    m = pd.concat(out, ignore_index=True)
    m["head"] = head
    return pergt.merge(m, on=["im_file", "gt_idx"], how="left", validate="one_to_one")


# ---------------------------------------------------------------- bước 3: mô hình recall


def add_features(df: pd.DataFrame, min_class_n: int = 200) -> pd.DataFrame:
    """Biến giải thích đã khai trong preregistration (H2a)."""
    d = df.copy()
    d["size_p3"] = d["short"] / P3_STRIDE  # cạnh ngắn theo bước lưới P3
    d["log2_size_p3"] = np.log2(d["size_p3"].clip(lower=1 / 8))
    d["aspect"] = d["long"] / d["short"].clip(lower=1e-6)
    d["log2_aspect"] = np.log2(d["aspect"])
    d["crowd"] = np.log1p(d["n_gt_img"])
    d["near"] = (d["nn_px"] < 2 * P3_STRIDE).astype(int)  # có hàng xóm trong 16 px
    counts = d["cls"].map(d["cls"].value_counts())
    d["cls_g"] = np.where(counts >= min_class_n, d["cls"], -1)  # gộp lớp hiếm để logit không tách hoàn toàn
    for br in ("o2m", "o2o"):
        if f"{br}_n_pos" in d:
            d[f"{br}_pos_bin"] = pd.cut(d[f"{br}_n_pos"], [-0.5, 0.5, 1.5, 2.5, 4.5, 9.5, 1e9],
                                        labels=["0", "1", "2", "3-4", "5-9", "10+"])
    d["size_bin"] = pd.cut(d["short"], [0, 4, 8, 8 * math.sqrt(2), 16, 32, 1e9],
                           labels=["<4", "4-8", "8-11.3", "11.3-16", "16-32", "32+"])
    return d


def recall_table(df: pd.DataFrame, tau: float, by=("arm", "size_bin", "o2m_pos_bin")) -> pd.DataFrame:
    """Recall ở ngưỡng điểm τ theo ô; kèm số GT. Mô tả, không kiểm định."""
    d = df.assign(det=(df["score"] >= tau).astype(int))
    return d.groupby(list(by), observed=True)["det"].agg(recall="mean", n="size").reset_index()


def fit_recall_models(df: pd.DataFrame, tau: float, branch="o2m", count="n_pos"):
    """Logit(det_τ) ~ log1p(count) + log2(size/P3) + log2(aspect) + crowd + near + C(cls_g), SE cụm theo ảnh.

    `count="n_pos"`: mẫu dương cuối (phụ thuộc cả dự đoán của mô hình qua TAL, nên có thể bị nhân quả ngược);
    `count="n_cand"`: số ứng viên, chỉ phụ thuộc hình học và quy tắc của arm (biến kiểm tra độ vững, prereg §3).
    Trả về dict: {'pooled': kết quả có arm làm biến, 'per_arm': {arm: kết quả}}. Chỉ dùng GT có trong loss.
    """
    import statsmodels.formula.api as smf

    d = df[df["in_loss"]].assign(det=lambda x: (x["score"] >= tau).astype(int),
                                 lpos=lambda x: np.log1p(x[f"{branch}_{count}"]))
    f = "det ~ lpos + log2_size_p3 + log2_aspect + crowd + near + C(cls_g)"
    groups = pd.factorize(d["im_file"])[0]
    pooled = smf.logit(f + " + C(arm)", d).fit(disp=0, cov_type="cluster", cov_kwds={"groups": groups})
    per_arm = {}
    for a, da in d.groupby("arm"):
        ga = pd.factorize(da["im_file"])[0]
        per_arm[a] = smf.logit(f, da).fit(disp=0, cov_type="cluster", cov_kwds={"groups": ga})
    return {"pooled": pooled, "per_arm": per_arm}


def mediation_check(df: pd.DataFrame, tau: float, branch="o2m"):
    """H2c: nếu hệ số của arm (so với A0) gần 0 khi đã có lpos trong mô hình, thì khác biệt giữa arm đi qua số
    mẫu dương. So hệ số C(arm) giữa mô hình có và không có lpos. Mô tả; không phải phép thử nhân quả."""
    import statsmodels.formula.api as smf

    d = df[df["in_loss"]].assign(det=lambda x: (x["score"] >= tau).astype(int),
                                 lpos=lambda x: np.log1p(x[f"{branch}_n_pos"]))
    groups = pd.factorize(d["im_file"])[0]
    base = "det ~ log2_size_p3 + log2_aspect + crowd + near + C(cls_g) + C(arm, Treatment('A0'))"
    kw = dict(disp=0, cov_type="cluster", cov_kwds={"groups": groups})
    m0 = smf.logit(base, d).fit(**kw)
    m1 = smf.logit(base + " + lpos", d).fit(**kw)
    keep = [k for k in m0.params.index if k.startswith("C(arm")]
    return pd.DataFrame({"coef_without_lpos": m0.params[keep], "coef_with_lpos": m1.params[keep],
                         "se_with_lpos": m1.bse[keep]})


def angle_table(df: pd.DataFrame, min_aspect=1.5) -> pd.DataFrame:
    """Hướng 4: median và p90 của |Δθ| theo arm × head × nhóm kích thước, chỉ GT đã khớp và đủ dài (aspect ≥ min)."""
    d = df[(df["angle_err_deg"].notna()) & (df["long"] / df["short"].clip(lower=1e-6) >= min_aspect)]
    return (d.groupby(["arm", "head", "size_bin"], observed=True)["angle_err_deg"]
            .agg(median="median", p90=lambda s: s.quantile(0.9), n="size").reset_index())


# ---------------------------------------------------------------- vòng cho 12 run cũ và cổng H2 (preregistration §5)


def pergt_for_runs(runs_dir, data_yaml, images_val, out_dir, device="cuda:0", heads=("e2e", "nms")) -> pd.DataFrame:
    """Bước 1 + 2 cho mọi run có `c11_done.json`; mỗi run một file parquet trong out_dir (có rồi thì bỏ qua)."""
    import json
    import time

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for rd in sorted(Path(runs_dir).glob("c11_*_s*")):
        done_f = rd / "c11_done.json"
        f = out_dir / f"{rd.name}.parquet"
        if not done_f.exists() or f.exists():
            continue
        done = json.loads(done_f.read_text())
        t0 = time.time()
        g = record_assignment(rd / "weights" / "last.pt", data_yaml, done["arm"], split="val", device=device)
        g["seed"] = done["seed"]
        parts = [predict_and_match(rd / "weights" / "last.pt", g, images_val, head=h) for h in heads]
        tmp = f.with_suffix(".tmp")
        pd.concat(parts, ignore_index=True).to_parquet(tmp)
        tmp.replace(f)  # ghi xong mới đổi tên: phiên bị ngắt giữa chừng không để lại file dở
        print(rd.name, len(g), "GT", f"{time.time() - t0:.0f}s", flush=True)
    return add_features(pd.concat([pd.read_parquet(f) for f in sorted(out_dir.glob("*.parquet"))],
                                  ignore_index=True))


GATE_RULE = "PREREG-C11X-v1 + A1"


def h2_gate(pg: pd.DataFrame, tau: float = 0.25, head: str = "nms", branch: str = "o2m",
            count: str = "n_cand") -> dict:
    """Cổng go của hướng 3 (preregistration §5, sửa ở phụ lục A1): qua khi hệ số log1p(n_cand) > 0 và CI 95% không
    chứa 0. n_cand chỉ phụ thuộc hình học và quy tắc của arm. Hệ số của n_pos (TAL chọn theo điểm dự đoán, nên có
    thể nhân quả ngược) ghi kèm để mô tả, không quyết định cổng."""
    d = pg[pg["head"] == head]

    def coef_ci(c):
        p = fit_recall_models(d, tau, branch=branch, count=c)["pooled"]
        lo, hi = (float(v) for v in p.conf_int().loc["lpos"])
        return float(p.params["lpos"]), lo, hi, int(p.nobs)

    coef, lo, hi, n = coef_ci(count)
    pos_coef, pos_lo, pos_hi, _ = coef_ci("n_pos")
    small = add_features(d) if "size_bin" not in d else d
    small = small[(small["short"] < 8) & small["in_loss"]]
    by_pos = (small.assign(det=(small["score"] >= tau).astype(int))
              .groupby(f"{branch}_pos_bin", observed=True)["det"].agg(["mean", "size"]))
    return dict(rule=GATE_RULE, tau=tau, head=head, branch=branch, count=count, coef=coef, ci_lo=lo, ci_hi=hi, n=n,
                go=bool(coef > 0 and lo > 0), n_pos_coef=pos_coef, n_pos_ci_lo=pos_lo, n_pos_ci_hi=pos_hi,
                recall_lt8_by_npos={str(k): [float(v["mean"]), int(v["size"])] for k, v in by_pos.iterrows()})
