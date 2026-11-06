"""Sinh notebooks/C11x_explore_val_colab.ipynb: phân tích 12 run cũ trên val, không train, để quyết định có train thêm không.

    python scripts/c11x/build_explore_notebook.py

Sửa ở đây rồi chạy lại; không sửa tay file .ipynb.
"""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf

from build_notebooks import DATA, DATA_MD, INSTALL, SETUP, SETUP_MD, code, md

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "notebooks" / "C11x_explore_val_colab.ipynb"
BRANCH = "admin/journal-diagnostic"


def cells():
    return [
        md("""
# C11x · Phân tích 12 run cũ trên val (không train)

**Mục đích:** biết bài có nội dung đáng viết không, **trước khi** tốn GPU cho seed 4–5.

**Vì sao dùng val:** recall theo GT trên tập test và seed 4–5 vẫn chưa bị xem. Notebook này **không chạm tập test**.

**Cách chạy:** Runtime → **L4 hoặc A100** → **Run all**. Bị ngắt thì Run all lại; phần đã xong tự bỏ qua.

**Tiêu chí quyết định, ghi trước khi xem kết quả** (`scripts/rq2/explore_decision.py`; ngưỡng là [design], không phải phép kiểm thống kê, không dùng làm kết luận trong bài). Tính trên GT rất nhỏ, trung bình theo seed:

| Tiêu chí | Đạt khi |
|---|---|
| C1 · Có cứu thật | Với GT mà A0 không cho ứng viên: recall(A2) − recall(A0) > 0 ở mọi seed, trung bình ≥ 0,02 (score ≥ 0,25) |
| C2 · Rõ lý do | Trong GT rất nhỏ mà A2 chưa phát hiện được: loại lỗi nhiều nhất là `loc`, `lost_to_neighbour`, `cls` hoặc `both` và chiếm ≥ 50% (score ≥ 0,05). `miss` vẫn báo nhưng không tính cho C2 |
| C3 · Giữ A8 | [A2 − A8] ở cụm dày trừ ở GT cô lập: cùng dấu ở mọi seed, độ lớn trung bình ≥ 0,01 |

**Kết quả:** đạt C1 **hoặc** C2 → train. Không đạt cái nào → chưa train. C3 trượt → bỏ A8, còn 4 run thay vì 6.

Ô cuối cũng ước thời gian phân tích theo GT trên test từ thời gian đo ở đây, và chọn trước mức score sẽ chạy (`explore_decision.test_scope`).

**Khi xong:** gửi lại nội dung ô cuối cùng (và thư mục `c11x-explore-val` nếu được).
"""),
        md(SETUP_MD),
        code(SETUP + f'''
BRANCH = "{BRANCH}"                                   # đổi thành "main" sau khi merge
ARMS, SEEDS = ["A0", "A1", "A8", "A2"], [1, 2, 3]
if not EXP_DRIVE.exists():
    raise StopRun(f"Không thấy {{EXP_DRIVE}}. Acc này cần quyền Editor trên thư mục NCKH và một shortcut tên NCKH "
                  "trong My Drive (Shared with me → chuột phải → Organize → Add shortcut → My Drive), rồi Run all lại.")
OUT_DIR = EXP_DRIVE / "c11x-explore-val"
OUT_DIR.mkdir(parents=True, exist_ok=True)
'''),
        code(INSTALL + '''
sys.path.insert(0, str(GH_DIR / "scripts/rq2"))
r = subprocess.run([sys.executable, "-m", "pytest", "-q", "test_errors_did.py", "test_explore.py", "-p", "no:cacheprovider"],
                   cwd=str(GH_DIR / "scripts/rq2"), capture_output=True, text=True)
print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-500:])
if r.returncode != 0:
    print(r.stdout[-5000:], r.stderr[-1000:])
    raise StopRun("Test hỏng. Sửa trước khi chạy tiếp.")
missing = [f"c11_{a}_s{s}" for a in ARMS for s in SEEDS if not (RUNS_OLD / f"c11_{a}_s{s}" / "weights" / "last.pt").exists()]
if missing:
    raise StopRun(f"Thiếu checkpoint trên Drive: {missing}")
print("đủ 12 checkpoint")

# Notebook train dùng dota_e2e của seed 1–3 cho phân tích theo GT trên test. Chỉ đọc điểm, không đọc GT test.
import rq2_recall as rr
OLD_DOTA = {f"c11_{a}_s{s}": rr.score_floor(RUNS_OLD / f"c11_{a}_s{s}" / "dota_e2e") for a in ("A0", "A8", "A2") for s in SEEDS}
OLD_DOTA_OK = all(v["n_boxes"] > 0 and v["min_score"] <= 0.05 + 1e-9 for v in OLD_DOTA.values())
(OUT_DIR / "old_dota_check.json").write_text(json.dumps(OLD_DOTA, indent=2))
print("dota_e2e seed 1–3 dùng được cho score ≥ 0,05:", OLD_DOTA_OK)
if not OLD_DOTA_OK:
    print("CẢNH BÁO: thiếu dota_e2e hoặc lưu ở ngưỡng > 0,05:", {k: v for k, v in OLD_DOTA.items()
          if not (v["n_boxes"] and v["min_score"] <= 0.05 + 1e-9)})
'''),
        md(DATA_MD),
        code(DATA),
        md("## 2. Bảng theo GT từ nhãn, chỉ giữ ảnh val"),
        code(r'''
import pandas as pd, rq2_errors as re_, rq2_did as did, predict_split as ps, explore_decision as ed
import c11x_results as cr
from aitodr_data import scene_key
RQ2_DIR = GH_DIR / "scripts/rq2"
OFF = OUT_DIR / "rq2_trainval"
if not (OFF / "rq2_per_gt.csv.gz").exists():
    subprocess.run([sys.executable, "rq2_offline.py", "--labels", str(LABELS / "trainval"), "--out", str(OFF),
                    "--protocol", "woX", "--arms", "A0,A1,A8,A2"], cwd=str(RQ2_DIR), check=True)
VAL_IMAGES = DS / "images" / "val"
val_stems = {p.stem for p in VAL_IMAGES.iterdir()}
off = pd.read_csv(OFF / "rq2_per_gt.csv.gz")
off = off[off.stem.isin(val_stems)].copy()
stems = sorted(off.stem.unique())
print(len(val_stems), "ảnh val;", len(stems), "ảnh có GT;", len(off), "GT; rất nhỏ:", int((off.bin == "vt").sum()))
pairs = pd.DataFrame({"a": off.scene, "b": off.stem.map(scene_key)}).drop_duplicates()
if not (len(pairs) == pairs.a.nunique() == pairs.b.nunique()):
    raise StopRun(f"scene_key lệch: {len(pairs)} cặp, {pairs.a.nunique()} và {pairs.b.nunique()} nhóm.")
print(off.scene.nunique(), "cụm cảnh, khớp aitodr_data.scene_key")
off2 = off[["stem", "gt", "scene", "bin", "nn16", "A0_cand", "cls"]].assign(starved_A0=off.A0_cand == 0,
                                                                            density=re_.density_bin(off.nn16).values)
print("GT rất nhỏ mà A0 không cho ứng viên:", int((off2[off2.bin == "vt"].starved_A0).sum()))
'''),
        md("## 3. Predict val cho 12 run, hai head (lưu trên Drive, score ≥ 0,05)"),
        code(r'''
import gc, torch
PRED = OUT_DIR / "pred"
for s in SEEDS:
    for a in ARMS:
        for head in ("e2e", "nms"):
            info = ps.predict_to_dota(RUNS_OLD / f"c11_{a}_s{s}" / "weights" / "last.pt", VAL_IMAGES,
                                      PRED / f"{a}_s{s}_{head}", head, conf=0.05)
            print(a, s, head, info, flush=True)
        gc.collect(); torch.cuda.empty_cache()
'''),
        md("""
## 4. Số phận từng GT, recall theo IoU, M1 và M2

Chỉ để mô tả. Bootstrap B = 2.000 theo cụm cảnh, gộp bất định seed với t 2 bậc tự do, nên khoảng rất rộng.
"""),
        code(r'''
FATES = OUT_DIR / "fates"
FATES.mkdir(parents=True, exist_ok=True)
SECONDS_FILE = FATES / "_seconds.json"
SECONDS = json.loads(SECONDS_FILE.read_text()) if SECONDS_FILE.exists() else {}

def fates(head, score):
    frames = []
    for s in SEEDS:
        for a in ARMS:
            f = FATES / f"{head}_score{score:g}_{a}_s{s}.parquet"
            if not f.exists():
                t0 = time.time()
                re_.fates_run(LABELS / "trainval", stems, PRED / f"{a}_s{s}_{head}", score).to_parquet(f)
                SECONDS[f.stem] = time.time() - t0
                SECONDS_FILE.write_text(json.dumps(SECONDS, indent=1))
                print(head, score, a, s, f"{SECONDS[f.stem]:.0f}s", flush=True)
            frames.append(pd.read_parquet(f).assign(arm=a, seed=s))
    df = pd.concat(frames, ignore_index=True).merge(off2, on=["stem", "gt"], how="left", validate="many_to_one")
    assert df["scene"].notna().all(), "có GT không khớp bảng nhãn"
    return df.assign(detected=lambda x: x["det_0.5"])

TABLES = {}
for head, score in (("e2e", 0.25), ("e2e", 0.05), ("nms", 0.25)):
    TABLES[(head, score)] = df = fates(head, score)
    tag = f"{head}_score{score:g}"
    for name, by in (("arm_bin", ("arm", "bin")), ("arm_bin_starved", ("arm", "bin", "starved_A0")),
                     ("arm_bin_density", ("arm", "bin", "density"))):
        re_.fate_table(df, by=by).to_csv(OUT_DIR / f"fate_{name}_{tag}.csv")
    re_.recall_curve(df).to_csv(OUT_DIR / f"recall_iou_{tag}.csv")
    print("==", tag); display(re_.fate_table(df).round(3)); display(re_.recall_curve(df).round(3))
    vt = df[df.bin == "vt"]
    mech = {"M1_A2-A0_starved_vs_not": did.did_bootstrap(vt, "A2", "A0", group="starved_A0", g1=True, g0=False, B=2000),
            "M2_A2-A8_dense_vs_isolated": did.did_bootstrap(vt, "A2", "A8", group="density", g1=">=3", g0="isolated", B=2000)}
    for k, r in mech.items():
        r["combined"] = cr.combine_scene_seed(r["scene"], r["seed"])
        print(tag, k, "Δ =", round(r["scene"]["delta"], 4), "theo seed:", {s: round(v, 4) for s, v in r["seed"]["per_seed"].items()},
              "CI gộp:", round(r["combined"]["lo"], 4), round(r["combined"]["hi"], 4))
    (OUT_DIR / f"mech_{tag}.json").write_text(json.dumps(mech, indent=2, default=float))
'''),
        md("## 5. Quyết định theo tiêu chí đã ghi. Gửi lại nội dung ô này."),
        code(r'''
res = ed.decide(TABLES[("e2e", 0.25)], TABLES[("e2e", 0.05)])
res["env"] = ENV
res["n_gt_val"] = len(off2)
e2e_sec = [v for k, v in SECONDS.items() if k.startswith("e2e_")]
res["test_scope"] = (ed.test_scope(sum(e2e_sec) / len(e2e_sec), len(off2), res["runs_if_training"] // 2 * 5)
                     if e2e_sec else "không có số đo giây: xóa thư mục fates rồi Run all lại")
res["old_dota_ok"] = OLD_DOTA_OK
res["recall_iou_e2e_0.25"] = re_.recall_curve(TABLES[("e2e", 0.25)]).xs("mean", axis=1, level=1).round(4).reset_index().to_dict("records")
(OUT_DIR / "decision.json").write_text(json.dumps(res, indent=2, ensure_ascii=False, default=float))
print(json.dumps(res, indent=1, ensure_ascii=False, default=float))
'''),
    ]


def build():
    meta = {"accelerator": "GPU", "colab": {"gpuType": "L4", "provenance": []},
            "kernelspec": {"display_name": "Python 3", "name": "python3"}, "language_info": {"name": "python"}}
    nb = nbf.v4.new_notebook(cells=cells(), metadata=meta)
    nbf.validate(nb)
    nbf.write(nb, OUT)
    print("ghi", OUT.name, len(nb.cells), "ô")


if __name__ == "__main__":
    build()
