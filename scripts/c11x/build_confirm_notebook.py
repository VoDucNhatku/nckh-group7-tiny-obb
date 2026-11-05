"""Sinh notebooks/C11x_train_confirm_colab.ipynb: run xác nhận theo preregistration, phụ lục A2.

    python scripts/c11x/build_confirm_notebook.py

Để riêng khỏi build_notebooks.py vì file đó ghi đè C11x_analysis_colab.ipynb, làm mất output đã chạy trên Colab.
Sửa ở đây rồi chạy lại; không sửa tay file .ipynb.
"""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf

from build_notebooks import DATA, DATA_MD, INSTALL, SETUP, SETUP_MD, TESTS, code, md

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "notebooks" / "C11x_train_confirm_colab.ipynb"
BRANCH = "admin/journal-diagnostic"


def cells():
    return [
        md("""
# C11x · Run xác nhận cho bài tạp chí: A0, A8, A2 × seed 4–9

Theo `experiments/preregistration.md`, **phụ lục A2**. K-floor đã hủy vì cổng H2 trượt.

**Cách chạy**
- Runtime → Change runtime type → **A100 GPU** → **Run all**.
- Bị ngắt: kết nối lại rồi **Run all lần nữa**. Run đã xong tự bỏ qua; run dở chạy tiếp từ epoch cuối đã lưu trên Drive.

**Một lần Run all làm hết:** kiểm tra trước → test → dữ liệu → train R0 + 18 run → chấm hai head → kiểm R0 →
bảng và bootstrap → phân tích theo từng GT.

**Thời gian** [ước lượng; train 0,56 giờ/run và chấm 337 giây/run/head đo ở `C11_colab.ipynb`; bootstrap suy từ 6.348 giây
cho 12 run ở notebook phân tích, giả định tăng tuyến tính theo số run; chưa đo trên 18 run]:

| Việc | Thời gian |
|---|---|
| Train R0 + 18 run | ~10,6 giờ |
| Chấm 37 lần | ~3,5 giờ |
| Bootstrap hai head | ~5,3 giờ |
| Phân tích theo GT (CPU) | chưa đo; notebook in thời gian sau run đầu tiên |

Bootstrap chỉ ghi file khi xong cả head, nên bị ngắt giữa chừng là mất phần của head đó. Hãy chạy phần này trong một
phiên ổn định, để tab mở và máy không ngủ.
"""),
        md(SETUP_MD),
        code(SETUP + f'''
BRANCH = "{BRANCH}"                                   # đổi thành "main" sau khi merge
# Tốc độ tiêu CU của A100: đọc trong Colab và sửa nếu khác. [ước lượng]
CU_PER_HOUR = 5.4
ARMS  = ["A0", "A8", "A2"]                            # phụ lục A2; không đổi sau khi thấy kết quả
SEEDS = [4, 5, 6, 7, 8, 9]
RESULTS = EXP_DRIVE / "c11x-confirm-results"
R0_DIR = EXP_DRIVE / "runs-woX-c11x-R0"
'''),
        code(INSTALL + '''
sys.path.insert(0, str(GH_DIR / "scripts/rq2"))
'''),
        md("## 0.1 Kiểm tra trước (vài giây). Có lỗi thì in hết ra rồi dừng."),
        code(r"""
import c11x_preflight as pf
warns = pf.run_all(code_dir=CODE_DIR, data_drive=DATA_DRIVE, local=LOCAL, runs_old=RUNS_OLD, exp_drive=EXP_DRIVE,
                   prereg=GH_DIR / "experiments" / "preregistration.md", drive=DRIVE)
for w in warns:
    print("CẢNH BÁO:", w)
prereg_text = (GH_DIR / "experiments" / "preregistration.md").read_text(encoding="utf-8")
if "### A2 ·" not in prereg_text:
    raise StopRun("preregistration chưa có phụ lục A2. Merge trước khi train.")
print("Kiểm tra trước: OK")
print(subprocess.check_output(["git", "-C", str(GH_DIR), "log", "-1", "--format=preregistration: %H %ci", "--",
                               "experiments/preregistration.md"]).decode())
"""),
        code(TESTS + r'''
run_pytest(GH_DIR / "scripts/rq2", ["test_errors_did.py", "test_recall.py", "-p", "no:cacheprovider"])
'''),
        md(DATA_MD),
        code(DATA),
        code(r'''
import c11x_train as ct, c11_pipeline as cp
diff = ct.check_recipe(cp.RECIPE)
if diff:
    raise StopRun(f"RECIPE_C11 khác c11_pipeline.RECIPE trên Drive ở các khoá {diff}. Sửa trước khi train.")
print("recipe khớp C11")
'''),
        md("""
## 2. Train R0 (A2 seed 1, kiểm tái lập) rồi 3 arm × seed 4–9

- Thứ tự: R0 trước, sau đó seed ngoài, arm trong.
- Sau epoch đầu tiên của phiên, notebook in ước lượng tổng thời gian và CU.
"""),
        code(r'''
EPOCHS = ct.RECIPE_C11["epochs"]
JOBS = [("A2", 1, R0_DIR)] + [(a, s, RUNS_NEW) for s in SEEDS for a in ARMS]

def run_dir(a, s, p):
    return Path(p) / ct.run_name(a, s)

def epochs_left():
    return sum(0 if (run_dir(*j) / "c11x_done.json").exists() else EPOCHS - min(ct.epochs_logged(run_dir(*j)), EPOCHS)
               for j in JOBS)

EVALS = [(run_dir("A2", 1, R0_DIR), "e2e")] + [(run_dir(a, s, p), h) for a, s, p in JOBS[1:] for h in ("e2e", "nms")]
n_eval_left = sum(not (rd / f"eval_{h}.json").exists() for rd, h in EVALS)
print(f"còn {epochs_left()} epoch và {n_eval_left} lần chấm")
eta = ct.EtaPrinter(epochs_left, n_eval=n_eval_left, cu_per_hour=CU_PER_HOUR)
for a, s, p in JOBS:
    t0 = time.time()
    rd = ct.train_arm(DATA_YAML, a, s, p, extra_callbacks=eta.callbacks())
    print(rd.name, "xong", f"({(time.time() - t0) / 3600:.2f} giờ trong phiên này)", flush=True)
'''),
        md("## 3. Chấm bằng AITODReval gốc: hai head cho 18 run, head e2e cho R0. Lưu dự đoán để phân tích theo GT."),
        code(r'''
import importlib, aitodr_evalkit as ek, c11_bootstrap as cb
for m in (ek, cp, cb): importlib.reload(m)
TEST_IMAGES = DS / "images" / "test"
for rd, head in EVALS:
    out = rd / f"eval_{head}.json"
    if out.exists():
        continue
    if not (rd / "c11x_done.json").exists():
        raise StopRun(f"{rd.name} chưa train xong; chạy lại ô train.")
    st = cp.predict_and_eval(rd / "weights" / "last.pt", LABELS / "test", TEST_IMAGES, out, head=head,
                             version=VERSION, exclude_stems=EXCLUDE, save_dota_dir=rd / f"dota_{head}")
    print(rd.name, head, {k: round(st[k], 4) for k in ("AP", "AP_vt", "AP_t", "AP_s")}, flush=True)
'''),
        md("""
## 4. Kiểm tái lập R0 (preregistration §6)

- **Khớp** khi |Δ mAP50-95 val ở epoch 24| ≤ 0,003 và |Δ AP test e2e| ≤ 0,002.
- **Không khớp:** vẫn dùng 18 run (cùng một đường code), nhưng không gộp với 12 run cũ, và phải báo độ lệch.
"""),
        code(r'''
import pandas as pd
rd0, old0 = run_dir("A2", 1, R0_DIR), RUNS_OLD / "c11_A2_s1"
r0 = {"ap_new": json.loads((rd0 / "eval_e2e.json").read_text())["AP"],
      "ap_old": json.loads((old0 / "eval_e2e.json").read_text())["AP"]}
r0["d_ap"] = r0["ap_new"] - r0["ap_old"]
if (old0 / "results.csv").exists():
    new, old = pd.read_csv(rd0 / "results.csv"), pd.read_csv(old0 / "results.csv")
    new.columns, old.columns = new.columns.str.strip(), old.columns.str.strip()
    col = [c for c in new.columns if "mAP50-95" in c][0]
    r0["d_val_ep24"] = float(new[col].iloc[-1] - old[col].iloc[-1])
r0["match"] = abs(r0["d_ap"]) <= 0.002 and abs(r0.get("d_val_ep24", 0.0)) <= 0.003
RESULTS.mkdir(parents=True, exist_ok=True)
(RESULTS / "r0_check.json").write_text(json.dumps(r0, indent=2))
print(json.dumps(r0, indent=1))
'''),
        md("""
## 5. Bảng, bootstrap B = 10.000, gộp bất định theo seed

- Chỉ dùng 18 run seed 4–9; **không** trộn với 12 run thăm dò.
- **P1 (phép chính duy nhất):** A2 − A0, AP_vt, head e2e. "Xác nhận" khi CI gộp không chứa 0 **và** Δ ≥ MEI_vt = 0,006.
- Mọi dòng khác chỉ để mô tả.
"""),
        code(r'''
import c11x_results as cr
from aitodr_data import scene_key
res = cr.collect_runs(RUNS_NEW)
assert (res.groupby(["head", "arm"]).size() == len(SEEDS)).all(), res.groupby(["head", "arm"]).size()
assert set(res["seed"]) == set(SEEDS), "có run ngoài seed 4–9 trong RUNS_NEW"
display(cr.summary_table(res).round(4))
for h in ("e2e", "nms"):
    display(cr.per_seed_table(res, h).round(4))
res.to_csv(RESULTS / "results_long.csv", index=False)
PAIRS = [("A2", "A0"), ("A8", "A0"), ("A2", "A8")]
KEYS = ("AP_vt", "AP_t", "AP_s", "AP_m", "AP")
rows = []
for head in ("e2e", "nms"):
    f = RESULTS / f"bootstrap_{head}_B10000.json"
    boot = json.loads(f.read_text()) if f.exists() else cr.run_scene_bootstrap(cb, [RUNS_NEW], head, PAIRS, KEYS, 10_000, scene_key, f)
    for x, y in PAIRS:
        for m in KEYS:
            sc, sd = boot[f"{x}-{y}"][m], cr.paired_seed_deltas(res, head, x, y, m)
            cmb = cr.combine_scene_seed(sc, sd)
            rows.append(dict(head=head, pair=f"{x}-{y}", metric=m, delta=sc["delta"], scene_lo=sc["ci_lo"],
                             scene_hi=sc["ci_hi"], seed_t_lo=sd.get("t_lo"), seed_t_hi=sd.get("t_hi"),
                             seed_min=sd.get("min"), seed_max=sd.get("max"), comb_lo=cmb["lo"], comb_hi=cmb["hi"],
                             comb_excl0=cmb.get("excludes_zero")))
ci = pd.DataFrame(rows); display(ci.round(4)); ci.to_csv(RESULTS / "ci_scene_seed.csv", index=False)
p1 = ci[(ci["head"] == "e2e") & (ci["pair"] == "A2-A0") & (ci["metric"] == "AP_vt")].iloc[0]
MEI_VT = 0.006
verdict = ("Xác nhận" if p1["comb_excl0"] and p1["delta"] >= MEI_VT else
           "CI loại 0 nhưng dưới MEI" if p1["comb_excl0"] else "Không xác nhận")
print(f"P1: Δ = {p1['delta']:.4f}, CI gộp [{p1['comb_lo']:.4f}; {p1['comb_hi']:.4f}] → {verdict}")
(RESULTS / "p1_verdict.json").write_text(json.dumps(dict(delta=p1["delta"], lo=p1["comb_lo"], hi=p1["comb_hi"],
                                                         verdict=verdict, mei=MEI_VT), indent=2, ensure_ascii=False))
'''),
        md("""
## 6. Theo từng GT trên tập test: M1, M2, M3 (phụ lục A2)

- **M3:** số phận GT (phát hiện / mất cho hàng xóm / sai lớp / định vị kém / bỏ sót) và recall theo IoU.
- **M1:** GT mà A0 không cho ứng viên có tăng recall dưới A2 nhiều hơn các GT rất nhỏ khác không?
- **M2:** A2 − A8 ở cụm dày (≥ 3 hàng xóm trong 16 px) so với GT cô lập.
- Kết quả từng run lưu trên Drive; chạy lại thì bỏ qua run đã xong.
- `score ≥ 0,25` là chính; `score ≥ 0,05` kiểm độ nhạy. Ở 0,25, "bỏ sót" gồm cả hộp đúng chỗ nhưng điểm thấp.
"""),
        code(r'''
import rq2_errors as re_, rq2_did as did
RQ2_DIR, MECH = GH_DIR / "scripts/rq2", RESULTS / "mechanism"
OFF = MECH / "rq2_test"
if not (OFF / "rq2_per_gt.csv.gz").exists():
    subprocess.run([sys.executable, "rq2_offline.py", "--labels", str(LABELS / "test"), "--out", str(OFF),
                    "--protocol", "woX", "--arms", "A0,A1,A8,A2"], cwd=str(RQ2_DIR), check=True)
off = pd.read_csv(OFF / "rq2_per_gt.csv.gz")
stems = sorted(off.stem.unique())
if set(stems) & set(EXCLUDE):
    raise StopRun("bảng theo GT còn ảnh xView.")
pairs = pd.DataFrame({"a": off.scene, "b": off.stem.map(scene_key)}).drop_duplicates()
if not (len(pairs) == pairs.a.nunique() == pairs.b.nunique()):
    raise StopRun(f"scene_key của scripts/rq2 khác aitodr_data: {len(pairs)} cặp, {pairs.a.nunique()} và {pairs.b.nunique()} nhóm.")
print(len(off), "GT;", off.scene.nunique(), "cụm cảnh, khớp aitodr_data.scene_key")
COLS = ["stem", "gt", "scene", "bin", "nn16", "A0_cand", "cls"]
off2 = off[COLS].assign(starved_A0=off.A0_cand == 0, density=re_.density_bin(off.nn16).values)

def fates(head, score):
    d = MECH / f"fates_{head}_score{score:g}"
    d.mkdir(parents=True, exist_ok=True)
    frames = []
    for s in SEEDS:
        for a in ARMS:
            f = d / f"{a}_s{s}.parquet"
            if not f.exists():
                t0 = time.time()
                r = re_.fates_run(LABELS / "test", stems, run_dir(a, s, RUNS_NEW) / f"dota_{head}", score)
                r.to_parquet(f)
                print(head, score, a, s, f"{time.time() - t0:.0f}s", flush=True)
            frames.append(pd.read_parquet(f).assign(arm=a, seed=s))
    return pd.concat(frames, ignore_index=True).merge(off2, on=["stem", "gt"], how="left").assign(detected=lambda x: x["det_0.5"])

def mech_tests(df, tag):
    vt = df[df.bin == "vt"]
    out = {}
    out["M1_A2-A0_starved_vs_not"] = did.did_bootstrap(vt, "A2", "A0", group="starved_A0", g1=True, g0=False)
    out["M2_A2-A8_dense_vs_isolated"] = did.did_bootstrap(vt, "A2", "A8", group="density", g1=">=3", g0="isolated")
    for k, r in out.items():
        r["combined"] = cr.combine_scene_seed(r["scene"], r["seed"])
        print(tag, k, {x: round(r["combined"][x], 4) for x in ("delta", "lo", "hi")}, "CI gộp loại 0:", r["combined"]["excludes_zero"])
    (MECH / f"mech_{tag}.json").write_text(json.dumps(out, indent=2, default=float))

for head, score in (("e2e", 0.25), ("e2e", 0.05), ("nms", 0.25)):
    df = fates(head, score)
    tag = f"{head}_score{score:g}"
    t = re_.fate_table(df); c = re_.recall_curve(df)
    t.to_csv(MECH / f"fate_by_arm_bin_{tag}.csv"); c.to_csv(MECH / f"recall_iou_by_arm_bin_{tag}.csv")
    re_.fate_table(df, by=("arm", "bin", "starved_A0")).to_csv(MECH / f"fate_by_arm_bin_starved_{tag}.csv")
    re_.fate_table(df, by=("arm", "bin", "density")).to_csv(MECH / f"fate_by_arm_bin_density_{tag}.csv")
    display(t.round(3)); display(c.round(3))
    mech_tests(df, tag)
(RESULTS / "env.json").write_text(json.dumps(ENV, indent=2))
print("XONG. Kết quả ở", RESULTS)
'''),
    ]


def build():
    meta = {"accelerator": "GPU", "colab": {"gpuType": "A100", "provenance": []},
            "kernelspec": {"display_name": "Python 3", "name": "python3"}, "language_info": {"name": "python"}}
    nb = nbf.v4.new_notebook(cells=cells(), metadata=meta)
    nbf.validate(nb)
    nbf.write(nb, OUT)
    print("ghi", OUT, len(nb.cells), "ô")


if __name__ == "__main__":
    build()
