"""Sinh hai notebook Colab của C11x từ mã nguồn này (sửa ở đây, rồi chạy lại; không sửa tay file .ipynb).

    python scripts/c11x/build_notebooks.py      # ghi notebooks/C11x_analysis_colab.ipynb và C11x_train_kfloor_colab.ipynb
"""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "notebooks"


def md(s):
    return nbf.v4.new_markdown_cell(s.strip())


def code(s):
    return nbf.v4.new_code_cell(s.strip())


SETUP_MD = """
## 0. Cấu hình

Đường dẫn giống `C11_colab.ipynb`. Code cũ (`scripts/c11`) đọc từ **Drive**; code mới (`scripts/c11x`) lấy từ
**GitHub** (`BRANCH`). Đổi `BRANCH` thành `main` sau khi PR được merge.
"""

SETUP = r'''
from pathlib import Path
import sys, json, time, subprocess

DRIVE      = Path("/content/drive/MyDrive/NCKH")
CODE_DIR   = DRIVE / "repo/NCKH/scripts/c11"          # code C11 trên Drive (không có trên GitHub)
DATA_DRIVE = DRIVE / "data"
EXP_DRIVE  = DRIVE / "repo/NCKH/experiments"
LOCAL      = Path("/content/aitodr")
PROTOCOL, VERSION = "woX", "oc"
RUNS_OLD   = EXP_DRIVE / "runs-woX"                    # 12 run thăm dò của C11 (A0/A1/A8/A2 × seed 1–3)
RUNS_NEW   = EXP_DRIVE / "runs-woX-c11x"               # run mới theo preregistration
BRANCH     = "admin/c11-novelty-plan"                  # đổi thành "main" sau khi merge
GH_DIR     = Path("/content/nckh_gh")

def today():
    """Ngày lúc ghi file (không cố định từ đầu phiên như biến TODAY của C11)."""
    return time.strftime("%Y-%m-%d")

from google.colab import drive
drive.mount("/content/drive")
!nvidia-smi --query-gpu=name,memory.total --format=csv || echo "CPU runtime"
'''

INSTALL = r'''
!pip -q install "ultralytics==8.4.174" shapely gdown statsmodels
!rm -rf "{GH_DIR}" && git clone -q --depth 1 -b "{BRANCH}" https://github.com/VoDucNhatku/nckh-group7-tiny-obb "{GH_DIR}"
GH_COMMIT = subprocess.check_output(["git", "-C", str(GH_DIR), "rev-parse", "HEAD"]).decode().strip()
!rm -rf /content/c11 && cp -r "{CODE_DIR}" /content/c11
for p in ("/content/c11", str(GH_DIR / "scripts/c11x")):
    if p not in sys.path:
        sys.path.insert(0, p)
import ultralytics, torch, numpy, platform
ENV = dict(ultralytics=ultralytics.__version__, torch=torch.__version__, numpy=numpy.__version__,
           python=platform.python_version(), gpu=torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
           c11x_commit=GH_COMMIT)
print(ENV)
assert ENV["ultralytics"] == "8.4.174"
'''

TESTS = r'''
# Test cũ (55, trên Drive) + test mới (bỏ file train chậm ~6 phút; chạy riêng nếu muốn)
!cd /content/c11 && python -m pytest -q test_stal_arms.py test_evalkit.py test_data_rq2.py test_bootstrap.py test_fastpath.py 2>&1 | tail -1
!cd "{GH_DIR}/scripts/c11x" && python -m pytest -q tests --ignore=tests/test_c11x_train.py -p no:cacheprovider 2>&1 | tail -1
'''

DATA_MD = """
## 1. Dữ liệu và dataset YOLO (giống hệt C11)

Giải nén nhãn + ảnh woX từ Drive, dựng lại `yolo_woX` bằng `aitodr_data.build_yolo_dataset` với **cùng `seed=0`**,
rồi so với `split_manifest.json` đã lưu ngày 20/10. Lệch thì dừng: mọi so sánh với 12 run cũ cần đúng split cũ.
"""

DATA = r'''
LOCAL.mkdir(parents=True, exist_ok=True)
lab_zip = DATA_DRIVE / "labels.zip"
assert lab_zip.exists() and open(lab_zip, "rb").read(2) == b"PK", "labels.zip chưa có trong DATA_DRIVE"
!unzip -q -o "{lab_zip}" -d "{LOCAL}"
LABELS = next(p.parent for p in LOCAL.rglob("trainval") if p.is_dir() and any(p.glob("*.txt")))
IMAGES = LOCAL / "images_raw"
IMAGES.mkdir(exist_ok=True)
for z in ["aitod_wo_xview_trainval_imgs.zip", "aitod_wo_xview_test_imgs.zip"]:
    src = DATA_DRIVE / z
    if src.exists() and not (IMAGES / (z + ".done")).exists():
        !cp "{src}" /content/ && unzip -q -o "/content/{z}" -d "{IMAGES}" && rm "/content/{z}" && touch "{IMAGES}/{z}.done"
    print(z, "OK" if (IMAGES / (z + ".done")).exists() else "CHƯA CÓ")

import aitodr_data as ad
XVIEW = ad.xview_stems()
EXCLUDE = (XVIEW["trainval"] | XVIEW["test"]) if PROTOCOL == "woX" else set()
DS = LOCAL / f"yolo_{PROTOCOL}"
man = ad.build_yolo_dataset(LABELS, IMAGES, DS, version=VERSION, exclude_xview=(PROTOCOL == "woX"),
                            val_frac=0.10, seed=0)
old = json.loads(next(EXP_DRIVE.glob(f"*-dataset-{PROTOCOL}/split_manifest.json")).read_text())
assert man["splits"] == old["splits"], ("split khác ngày 20/10", man["splits"], old["splits"])
DATA_YAML = DS / "aitodr.yaml"
print("split khớp:", man["splits"])
'''


def analysis_notebook():
    cells = [
        md("""
# C11x · Phân tích 12 run sẵn có: head × kích thước (hướng 1), số mẫu dương → recall (hướng 2), góc (hướng 4), seed (hướng 5)

Kế hoạch: `notes/08-c11-execution/t07-c11-novelty-plan-2026-10-30.md`.
Preregistration: `experiments/preregistration.md` (**PREREG-C11X-v1**). Notebook này **không train**.

Thứ tự bắt buộc: preregistration đã commit trước khi chạy các phần 3–6. Mọi số trong báo cáo đọc từ file mà
notebook ghi ra `EXP_DRIVE`, không gõ tay.

| Phần | Việc | GPU | Ước lượng thời gian [ước lượng, từ thời gian chấm ở #29 và bootstrap ở #34 của C11] |
|---|---|---|---|
| 0–1 | Cấu hình, test, dataset | không bắt buộc | ~15 phút |
| 2 | Bảng gộp đã sửa đếm trùng + bảng theo seed + kiểm `scene_key` | không | 1 phút |
| 3 | Chấm head nms cho đủ 12 run | có | ~6 phút/run → ~50 phút |
| 4 | Bootstrap B = 10.000 cho hai head + gộp bất định theo seed | có | ~95 phút/head |
| 5 | Gán mẫu tại checkpoint cuối + khớp từng GT trên val | có | ~3–5 phút/run [ước lượng] |
| 6 | Mô hình recall, góc, số seed cần | không | vài phút |
"""),
        md(SETUP_MD), code(SETUP), code(INSTALL), code(TESTS),
        md(DATA_MD), code(DATA),
        md("""
## 2. Bảng gộp đã sửa (vấn đề ô #32) và bảng theo seed

`collect_runs` chỉ đọc đúng `eval_e2e.json` / `eval_nms.json` và báo lỗi nếu một (arm, seed, head) xuất hiện hai lần.
Kỳ vọng: `count = 3` cho mọi arm của head e2e; trung bình AP của A0 ≈ 0,1297 (không còn 0,1301).
"""),
        code(r'''
import pandas as pd
import c11x_results as cr
OUT = EXP_DRIVE / f"{today()}-c11x-analysis"
OUT.mkdir(parents=True, exist_ok=True)
res = cr.collect_runs(RUNS_OLD)
display(cr.summary_table(res).round(4))
for h in ("e2e", "nms"):
    if (res["head"] == h).any():
        print("head", h); display(cr.per_seed_table(res, h).round(4))
res.to_csv(OUT / "results_long.csv", index=False)
'''),
        code(r'''
# Kiểm nhóm cảnh của phần không-xView (vấn đề 3.1.6): ô cắt cùng ảnh gốc có bị tách thành nhiều nhóm không
test_stems = [p.stem for p in (DS / "images" / "test").glob("*.png")]
audit = cr.scene_key_audit(test_stems, ad.scene_key)
print(json.dumps(audit, indent=1, ensure_ascii=False))
(OUT / "scene_key_audit.json").write_text(json.dumps(audit, indent=2, ensure_ascii=False))
'''),
        md("""
## 3. Hướng 1 — chấm head nms cho đủ 12 run

Dùng đúng `c11_pipeline.predict_and_eval` của C11 (Drive), `head="nms"`, chấm `last.pt`. Run đã có
`eval_nms.json` thì bỏ qua.
"""),
        code(r'''
import importlib, aitodr_evalkit as ek, c11_pipeline as cp, c11_bootstrap as cb
for m in (ek, cp, cb): importlib.reload(m)
TEST_IMAGES = DS / "images" / "test"
for rd in sorted(RUNS_OLD.glob("c11_*_s*")):
    if not (rd / "c11_done.json").exists():
        continue
    for head in ("e2e", "nms"):
        out = rd / f"eval_{head}.json"
        if out.exists():
            continue
        st = cp.predict_and_eval(rd / "weights" / "last.pt", LABELS / "test", TEST_IMAGES, out, head=head,
                                 version=VERSION, exclude_stems=EXCLUDE, save_dota_dir=rd / f"dota_{head}")
        print(rd.name, head, {k: round(st[k], 4) for k in ("AP", "AP_vt", "AP_t", "AP_s")})
res = cr.collect_runs(RUNS_OLD)
assert (res.groupby(["head", "arm"]).size() == 3).all(), res.groupby(["head", "arm"]).size()
res.to_csv(OUT / "results_long.csv", index=False)
'''),
        code(r'''
# Δ theo seed cho từng head và hiệu Δ_nms − Δ_e2e (H1a, H1b). Mô tả theo seed; kiểm định ở phần 4.
rows = []
for x in ("A1", "A8", "A2"):
    for metric in ("AP", "AP_vt", "AP_t", "AP_s", "AP_m"):
        if metric not in res:
            continue
        hi = cr.head_interaction(res, x, "A0", metric)
        for s, r in hi.iterrows():
            rows.append(dict(x=x, metric=metric, seed=s, **r.to_dict()))
inter = pd.DataFrame(rows)
display(inter.groupby(["x", "metric"])[["d_e2e", "d_nms", "d_nms_minus_d_e2e"]].agg(["mean", "min", "max"]).round(4))
inter.to_csv(OUT / "head_interaction_per_seed.csv", index=False)
'''),
        md("""
## 4. Bootstrap theo cụm cảnh B = 10.000, hai head, rồi gộp bất định theo seed

- Cặp và chỉ số đúng như preregistration §4. B = 10.000 như proposal §8.6 (C11 chạy 1.000).
- `combine_scene_seed`: khoảng xấp xỉ Δ ± 1,96·√(se_cảnh² + se_seed²) [design]; luôn báo kèm khoảng t theo seed.
- `ci_skew`: CI lệch (> 2 hoặc < 0,5) thì ghi chú; không đổi phép thử sau khi thấy số.
"""),
        code(r'''
from aitodr_data import scene_key
PAIRS = [("A1", "A0"), ("A8", "A0"), ("A2", "A0"), ("A2", "A8")]
KEYS = ("AP_vt", "AP_t", "AP_s", "AP_m", "AP")
B = 10_000
boots = {}
for head in ("e2e", "nms"):
    f = OUT / f"bootstrap_{head}_B{B}.json"
    if f.exists():
        boots[head] = json.loads(f.read_text()); continue
    t0 = time.time()
    boots[head] = cr.run_scene_bootstrap(cb, [RUNS_OLD], head, PAIRS, KEYS, B, scene_key, f)
    print(head, f"{time.time() - t0:.0f}s")
'''),
        code(r'''
rows = []
for head, boot in boots.items():
    for x, y in PAIRS:
        k = f"{x}-{y}"
        if k not in boot:
            continue
        for m in KEYS:
            sc = boot[k][m]
            sd = cr.paired_seed_deltas(res, head, x, y, m)
            cmb = cr.combine_scene_seed(sc, sd)
            rows.append(dict(head=head, pair=k, metric=m, delta=sc["delta"], scene_lo=sc["ci_lo"], scene_hi=sc["ci_hi"],
                             skew=cr.ci_skew(sc), seed_t_lo=sd.get("t_lo"), seed_t_hi=sd.get("t_hi"),
                             seed_min=sd.get("min"), seed_max=sd.get("max"), comb_lo=cmb["lo"], comb_hi=cmb["hi"],
                             comb_excl0=cmb.get("excludes_zero")))
ci = pd.DataFrame(rows)
display(ci.round(4))
ci.to_csv(OUT / "ci_scene_seed.csv", index=False)
'''),
        md("""
## 5. Hướng 2 (và 4) — gán mẫu tại checkpoint cuối, khớp từng GT trên **val**

Với mỗi run: (a) `record_assignment` đưa ảnh val qua loss với đúng quy tắc của arm, ghi số ứng viên / mẫu dương
o2m, o2o cho từng GT; (b) `predict_and_match` predict ảnh val cho **cả hai head**, khớp IoU ≥ 0,5, ghi điểm và sai số
góc. Val (936 ảnh) là tập chính cho phân tích cơ chế; test đã bị xem.

Đọc thêm log `c11_assign_diag.jsonl` (ghi lúc train): in cấu trúc trước, rồi gộp theo epoch × nhánh × ô.
"""),
        code(r'''
# Log chẩn đoán lúc train: chưa biết trước cấu trúc (mã ghi nằm trong scripts/c11/stal_arms.py) nên in ra để đọc
diag_rows = []
for rd in sorted(RUNS_OLD.glob("c11_*_s*")):
    f = rd / "c11_assign_diag.jsonl"
    if not f.exists():
        continue
    done = json.loads((rd / "c11_done.json").read_text())
    for ln in f.read_text().splitlines():
        if ln.strip():
            d = json.loads(ln); d.update(arm=done["arm"], seed=done["seed"]); diag_rows.append(d)
print(len(diag_rows), "dòng; khoá của dòng đầu:", sorted(diag_rows[0]) if diag_rows else None)
diag = pd.json_normalize(diag_rows)
diag.to_parquet(OUT / "assign_diag_all.parquet")
display(diag.head(3).T)
'''),
        code(r'''
import c11x_pergt as cg
PERGT = OUT / "pergt"
PERGT.mkdir(exist_ok=True)
for rd in sorted(RUNS_OLD.glob("c11_*_s*")):
    if not (rd / "c11_done.json").exists():
        continue
    done = json.loads((rd / "c11_done.json").read_text())
    f = PERGT / f"{rd.name}.parquet"
    if f.exists():
        continue
    t0 = time.time()
    g = cg.record_assignment(rd / "weights" / "last.pt", DATA_YAML, done["arm"], split="val", device="cuda:0")
    g["seed"] = done["seed"]
    parts = [cg.predict_and_match(rd / "weights" / "last.pt", g, DS / "images" / "val", head=h) for h in ("e2e", "nms")]
    pd.concat(parts, ignore_index=True).to_parquet(f)
    print(rd.name, len(g), "GT", f"{time.time() - t0:.0f}s")
'''),
        md("""
## 6. Mô hình recall (H2a–H2c), góc (H4), số seed cần (H5)

τ chính = 0,25 (ngưỡng predict mặc định của Ultralytics); độ nhạy τ ∈ {0,1; 0,5}. Nhánh chính o2m cho head nms,
o2o cho head e2e (preregistration §3).
"""),
        code(r'''
pg = cg.add_features(pd.concat([pd.read_parquet(f) for f in sorted(PERGT.glob("*.parquet"))], ignore_index=True))
print(pg.groupby(["head", "arm"]).size())
# Mẫu dương theo arm × kích thước (giải thích H2b: các sàn có cùng đưa GT tí hon qua ngưỡng bão hoà không)
display(pg[pg["head"] == "e2e"].groupby(["arm", "size_bin"], observed=True)[["o2m_n_cand", "o2m_n_pos", "o2o_n_pos"]]
        .agg(["mean", lambda s: (s == 0).mean()]).round(3))
for tau in (0.25, 0.1, 0.5):
    for head, br, cnt in (("nms", "o2m", "n_pos"), ("e2e", "o2o", "n_pos"), ("e2e", "o2m", "n_pos"),
                          ("nms", "o2m", "n_cand")):
        d = pg[pg["head"] == head]
        fit = cg.fit_recall_models(d, tau, branch=br, count=cnt)
        p = fit["pooled"]
        print(f"tau={tau} head={head} branch={br} count={cnt}: lpos = {p.params['lpos']:.3f} "
              f"[{p.conf_int().loc['lpos', 0]:.3f}; {p.conf_int().loc['lpos', 1]:.3f}]  n={int(p.nobs)}")
        if tau == 0.25 and cnt == "n_pos":
            (OUT / f"logit_{head}_{br}_tau{tau}.txt").write_text(str(p.summary()))
            med = cg.mediation_check(d, tau, branch=br)
            display(med.round(3)); med.to_csv(OUT / f"mediation_{head}_{br}.csv")
rt = cg.recall_table(pg[pg["head"] == "nms"], 0.25)
rt.to_csv(OUT / "recall_by_arm_size_npos_nms.csv", index=False)
display(rt.pivot_table(index=["size_bin", "o2m_pos_bin"], columns="arm", values="recall", observed=True).round(3))
'''),
        code(r'''
# Hướng 4: sai số góc theo kích thước (val, GT đã khớp, aspect ≥ 1,5)
at = cg.angle_table(pg)
display(at.pivot_table(index="size_bin", columns=["head", "arm"], values="median", observed=True).round(1))
at.to_csv(OUT / "angle_error_by_size.csv", index=False)
'''),
        code(r'''
# Hướng 5: dao động theo seed so với hiệu ứng; số seed ghép cặp cần (xấp xỉ) để phát hiện Δ đang thấy
rows = []
for head in ("e2e", "nms"):
    for x, y in PAIRS:
        for m in ("AP", "AP_vt", "AP_t"):
            sd = cr.paired_seed_deltas(res, head, x, y, m)
            if sd.get("n", 0) >= 2:
                rows.append(dict(head=head, pair=f"{x}-{y}", metric=m, mean=sd["mean"], sd=sd["sd"],
                                 min=sd["min"], max=sd["max"], seeds_needed=cr.seeds_needed(sd["mean"], sd["sd"])))
sv = pd.DataFrame(rows); display(sv.round(4)); sv.to_csv(OUT / "seed_variance.csv", index=False)
(OUT / "env.json").write_text(json.dumps(ENV, indent=2))
'''),
    ]
    return cells


def train_notebook():
    cells = [
        md("""
# C11x · Hướng 3 — sàn theo số ứng viên (K1, K4) so với sàn cố định (A0, A8, A2), seed 4–6

Giao thức C11: YOLO26n-OBB, AI-TOD-R woX, 24 epoch, `ultralytics==8.4.174`, A100, khởi tạo `yolo26n.pt` (COCO).
Run mới ghi vào `RUNS_NEW` trên Drive, lưu checkpoint mỗi epoch (`save_period=1`), chạy lại ô train là **tự
resume**. Mọi arm (kể cả A0/A8/A2) train bằng **cùng một đường code** `c11x_train.py`.

**Cổng (preregistration §5):** chỉ chạy phần 3 khi
1. `experiments/preregistration.md` (PREREG-C11X-v1) đã có trên GitHub — ô dưới kiểm;
2. hướng 2 đã cho tín hiệu "go" theo đúng tiêu chí §5 của preregistration (ghi kết quả vào ô "GO_H2").
3. Run kiểm tái lập R0 (phần 2) khớp trong ngưỡng.

| Phần | Việc | Thời gian A100 [ước lượng: 0,55–0,57 giờ/run ở #23 của C11; chấm ~6 phút/run/head ở #29] |
|---|---|---|
| 2 | R0: train lại A2 seed 1 bằng code mới, so với run cũ | ~0,6 giờ |
| 3 | 5 arm × 3 seed = 15 run | ~8,5 giờ |
| 4 | Chấm 2 head × 15 run | ~3 giờ |
| 5 | Bảng, bootstrap B = 10.000, gộp seed | ~3 giờ |
"""),
        md(SETUP_MD), code(SETUP), code(INSTALL),
        code(r'''
# Cổng 1: preregistration có trên nhánh đã clone, đúng mã phiên bản
prereg = GH_DIR / "experiments" / "preregistration.md"
assert prereg.exists() and "PREREG-C11X-v1" in prereg.read_text(encoding="utf-8"), "chưa có preregistration — dừng"
print(subprocess.check_output(["git", "-C", str(GH_DIR), "log", "-1", "--format=%H %ci", "--", "experiments/preregistration.md"]).decode())
'''),
        code(TESTS),
        md(DATA_MD), code(DATA),
        code(r'''
import c11x_train as ct, c11_pipeline as cp
diff = ct.check_recipe(cp.RECIPE)
print("recipe lệch so với C11:", diff)
assert not diff, "RECIPE_C11 khác c11_pipeline.RECIPE trên Drive — sửa trước khi train"
'''),
        md("""
## 2. R0 — kiểm tái lập: A2 seed 1 bằng code mới so với `c11_A2_s1` cũ

A2 trong `c11x_assign` trùng mã gốc 8.4.174 (đã test). Cùng seed, `deterministic=True`, cùng recipe nên đường
mAP50-95 trên val phải gần như trùng run cũ. Ngưỡng (preregistration §6): |ΔmAP50-95 val ở epoch 24| ≤ 0,003 và
|ΔAP test e2e| ≤ 0,002. Không đạt thì **không** dừng các so sánh mới (chúng cùng một đường code), nhưng không được
gộp run mới với 12 run cũ, và phải ghi lệch vào báo cáo.
"""),
        code(r'''
import pandas as pd
R0_DIR = EXP_DRIVE / "runs-woX-c11x-R0"
rd0 = ct.train_arm(DATA_YAML, "A2", 1, R0_DIR)
new = pd.read_csv(rd0 / "results.csv")
old = pd.read_csv(RUNS_OLD / "c11_A2_s1" / "results.csv")   # [chưa kiểm] run cũ có results.csv
col = [c for c in new.columns if "mAP50-95" in c][0]
print("mAP50-95 val epoch 24: mới", round(float(new[col].iloc[-1]), 4), "| cũ", round(float(old[col].iloc[-1]), 4))
print("lệch lớn nhất theo epoch:", float((new[col] - old[col]).abs().max()))
'''),
        md("""
## 3. Train 5 arm × seed 4–6 (tự resume)

Thứ tự: seed ngoài, arm trong (các arm cùng seed chạy sát nhau, cùng loại GPU). Colab ngắt thì chạy lại ô này.
"""),
        code(r'''
GO_H2 = None   # ghi True/False theo tiêu chí go của hướng 2 (preregistration §5) TRƯỚC khi chạy ô dưới
assert GO_H2 is True, "chưa có kết quả go của hướng 2 — xem preregistration §5"
ARMS  = ["A0", "A8", "A2", "K1", "K4"]       # đúng preregistration §4; không đổi sau khi đã thấy kết quả
SEEDS = [4, 5, 6]
QUEUE = [(a, s) for s in SEEDS for a in ARMS]
for arm, seed in QUEUE:
    t0 = time.time()
    rd = ct.train_arm(DATA_YAML, arm, seed, RUNS_NEW)
    print(rd.name, "xong", f"{(time.time() - t0) / 3600:.2f} giờ phiên này")
'''),
        md("## 4. Chấm hai head bằng AITODReval gốc (code C11 trên Drive)"),
        code(r'''
import importlib, aitodr_evalkit as ek, c11_bootstrap as cb
for m in (ek, cp, cb): importlib.reload(m)
TEST_IMAGES = DS / "images" / "test"
for rd in sorted(RUNS_NEW.glob("c11x_*_s*")):
    if not (rd / "c11x_done.json").exists():
        continue
    for head in ("e2e", "nms"):
        out = rd / f"eval_{head}.json"
        if out.exists():
            continue
        st = cp.predict_and_eval(rd / "weights" / "last.pt", LABELS / "test", TEST_IMAGES, out, head=head,
                                 version=VERSION, exclude_stems=EXCLUDE, save_dota_dir=rd / f"dota_{head}")
        print(rd.name, head, {k: round(st[k], 4) for k in ("AP", "AP_vt", "AP_t", "AP_s")})
'''),
        md("""
## 5. Bảng, bootstrap B = 10.000, gộp bất định theo seed

Chỉ dùng run trong `RUNS_NEW` (seed 4–6). **Không** trộn với 12 run thăm dò.
"""),
        code(r'''
import pandas as pd, c11x_results as cr
from aitodr_data import scene_key
OUT = EXP_DRIVE / f"{today()}-c11x-kfloor"
OUT.mkdir(parents=True, exist_ok=True)
res = cr.collect_runs(RUNS_NEW)
display(cr.summary_table(res).round(4))
for h in ("e2e", "nms"):
    display(cr.per_seed_table(res, h).round(4))
res.to_csv(OUT / "results_long.csv", index=False)
PAIRS = [("K1", "A0"), ("K4", "A0"), ("K1", "A8"), ("K4", "A2"), ("A2", "A0"), ("A8", "A0")]
KEYS = ("AP_vt", "AP_t", "AP_s", "AP_m", "AP")
rows = []
for head in ("e2e", "nms"):
    f = OUT / f"bootstrap_{head}_B10000.json"
    boot = json.loads(f.read_text()) if f.exists() else cr.run_scene_bootstrap(cb, [RUNS_NEW], head, PAIRS, KEYS, 10_000, scene_key, f)
    for x, y in PAIRS:
        for m in KEYS:
            sc, sd = boot[f"{x}-{y}"][m], cr.paired_seed_deltas(res, head, x, y, m)
            cmb = cr.combine_scene_seed(sc, sd)
            rows.append(dict(head=head, pair=f"{x}-{y}", metric=m, delta=sc["delta"], scene_lo=sc["ci_lo"],
                             scene_hi=sc["ci_hi"], seed_min=sd.get("min"), seed_max=sd.get("max"),
                             comb_lo=cmb["lo"], comb_hi=cmb["hi"], comb_excl0=cmb.get("excludes_zero")))
ci = pd.DataFrame(rows); display(ci.round(4)); ci.to_csv(OUT / "ci_scene_seed.csv", index=False)
# Thống kê quy tắc K theo epoch: bao nhiêu GT phải nới, tới mức sàn nào
for rd in sorted(RUNS_NEW.glob("c11x_K*_s*")):
    ks = [json.loads(x) for x in (rd / "c11x_kstats.jsonl").read_text().splitlines()]
    print(rd.name, "epoch cuối:", ks[-1])
(OUT / "env.json").write_text(json.dumps(ENV, indent=2))
'''),
    ]
    return cells


def build():
    OUT.mkdir(exist_ok=True)
    meta = {"accelerator": "GPU", "colab": {"gpuType": "A100", "provenance": []},
            "kernelspec": {"display_name": "Python 3", "name": "python3"}, "language_info": {"name": "python"}}
    for name, cells in (("C11x_analysis_colab.ipynb", analysis_notebook()),
                        ("C11x_train_kfloor_colab.ipynb", train_notebook())):
        nb = nbf.v4.new_notebook(cells=cells, metadata=meta)
        nbf.validate(nb)
        nbf.write(nb, OUT / name)
        print("ghi", OUT / name, len(cells), "ô")


if __name__ == "__main__":
    build()
