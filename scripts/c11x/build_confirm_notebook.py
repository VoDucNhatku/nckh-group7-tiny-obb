"""Sinh notebooks/C11x_train_confirm_colab.ipynb: thêm seed 4–5 theo preregistration, phụ lục A2.

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
# C11x · Thêm seed 4–5: A0, A8, A2

Theo `experiments/preregistration.md`, **phụ lục A2**. Train bằng cùng đường code với seed 1–3 để gộp được 5 seed.

Notebook có **hai đợt**, để tiết kiệm compute unit. Đổi biến `PHASE` ở ô cấu hình.

| Đợt | `PHASE` | Runtime | Làm gì | Thời gian [ước lượng] | CU [ước lượng] |
|---|---|---|---|---|---|
| 1 | `"train"` | **A100** | R0 + 6 run, chấm 13 lần | khoảng 5,7 giờ | khoảng 31 (86 nếu A100 tốn 15 CU/giờ) |
| 2 | `"analyze"` | **L4** | Bootstrap, phân tích theo GT | khoảng 9–19 giờ | khoảng 16–33 |

**Cách chạy:** Run all. Bị ngắt thì Run all lại; phần đã xong tự bỏ qua. Xong đợt 1, notebook tự dừng và nhắc đổi sang đợt 2.

Bootstrap chỉ ghi file khi xong cả head, nên bị ngắt giữa chừng là mất phần của head đó. Để tab mở, máy không ngủ.

**Căn cứ ước lượng:** train 0,56 giờ/run và chấm 337 giây/run/head đo ở `C11_colab.ipynb`. Bootstrap 0,93 giây/vòng trên L4 với 12 run ở `notes/08-c11-execution/t07-c11x-handoff-2026-10-30.md`, giả định tăng tuyến tính theo số run. Phân tích theo GT mới đo trên dữ liệu giả. Tốc độ CU là số cộng đồng đo, Google không công bố: đọc tốc độ thật trong Colab.
"""),
        md(SETUP_MD),
        code(SETUP + f'''
BRANCH = "{BRANCH}"                                   # đổi thành "main" sau khi merge
PHASE = "train"                                       # "train" (A100) rồi "analyze" (L4)
ARMS  = ["A0", "A8", "A2"]                            # phụ lục A2; bỏ "A8" nếu tiêu chí C3 trượt
NEW_SEEDS, ALL_SEEDS = [4, 5], [1, 2, 3, 4, 5]
DIAG_EVERY = 10                                       # giống seed 1–3
RESULTS = EXP_DRIVE / "c11x-seeds1to5-results"
R0_DIR = EXP_DRIVE / "runs-woX-R0"
RESULTS.mkdir(parents=True, exist_ok=True)
assert PHASE in ("train", "analyze")
'''),
        code(INSTALL + '''
sys.path.insert(0, str(GH_DIR / "scripts/rq2"))
prereg_text = (GH_DIR / "experiments" / "preregistration.md").read_text(encoding="utf-8")
if "### A2 ·" not in prereg_text:
    raise StopRun("preregistration chưa có phụ lục A2. Merge trước khi train.")
print(subprocess.check_output(["git", "-C", str(GH_DIR), "log", "-1", "--format=preregistration: %H %ci", "--",
                               "experiments/preregistration.md"]).decode())
if PHASE == "train" and "A100" not in str(ENV["gpu"]):
    raise StopRun(f"Đợt train phải dùng A100 như seed 1–3, đang là {ENV['gpu']}.")
'''),
        code(TESTS + r'''
run_pytest(GH_DIR / "scripts/rq2", ["test_errors_did.py", "test_recall.py", "-p", "no:cacheprovider"])
'''),
        md(DATA_MD),
        code(DATA),
        code(r'''
import inspect, pandas as pd, c11_pipeline as cp
missing = {"project", "diag_every"} - set(inspect.signature(cp.train_arm).parameters)
if missing:
    raise StopRun(f"c11_pipeline.train_arm trên Drive thiếu tham số {missing}")
absent = [f"c11_{a}_s{s}" for a in ARMS for s in (1, 2, 3) if not (RUNS_OLD / f"c11_{a}_s{s}" / "c11_done.json").exists()]
if absent:
    raise StopRun(f"Thiếu run cũ: {absent}")
TEST_IMAGES = DS / "images" / "test"
RUN_DIRS = [RUNS_OLD / cp.run_name(a, s) for s in ALL_SEEDS for a in ARMS]
'''),
        md("""
## 2. Đợt 1: train R0 và seed 4–5, rồi chấm

- Cùng `c11_pipeline.train_arm` như `C11_colab.ipynb` ô #23. Run mới ghi vào `runs-woX`, cạnh seed 1–3.
- R0 (A2 seed 1) ghi riêng, để không đụng run cũ.
"""),
        code(r'''
if PHASE == "train":
    jobs = [("A2", 1, R0_DIR)] + [(a, s, RUNS_OLD) for s in NEW_SEEDS for a in ARMS]
    for a, s, project in jobs:
        rd = Path(project) / cp.run_name(a, s)
        if (rd / "c11_done.json").exists():
            print("đã xong", rd); continue
        t0 = time.time()
        print(">>> train", a, s, "GPU:", ENV["gpu"], flush=True)
        cp.train_arm(DATA_YAML, a, s, project=project, diag_every=DIAG_EVERY)
        print(rd.name, f"xong sau {(time.time() - t0) / 3600:.2f} giờ", flush=True)
    evals = [(R0_DIR / cp.run_name("A2", 1), "e2e")] + [(RUNS_OLD / cp.run_name(a, s), h) for s in NEW_SEEDS for a in ARMS
                                                        for h in ("e2e", "nms")]
    for rd, head in evals:
        out = rd / f"eval_{head}.json"
        if out.exists():
            continue
        st = cp.predict_and_eval(rd / "weights" / "last.pt", LABELS / "test", TEST_IMAGES, out, head=head,
                                 version=VERSION, exclude_stems=EXCLUDE, save_dota_dir=rd / f"dota_{head}")
        print(rd.name, head, {k: round(st[k], 4) for k in ("AP", "AP_vt", "AP_t", "AP_s")}, flush=True)
    # Kiểm tái lập R0 (phụ lục A2, mục 5)
    rd0, old0 = R0_DIR / cp.run_name("A2", 1), RUNS_OLD / cp.run_name("A2", 1)
    r0 = {"ap_new": json.loads((rd0 / "eval_e2e.json").read_text())["AP"],
          "ap_old": json.loads((old0 / "eval_e2e.json").read_text())["AP"]}
    r0["d_ap"] = r0["ap_new"] - r0["ap_old"]
    if (old0 / "results.csv").exists():
        new, old = pd.read_csv(rd0 / "results.csv"), pd.read_csv(old0 / "results.csv")
        new.columns, old.columns = new.columns.str.strip(), old.columns.str.strip()
        col = [c for c in new.columns if "mAP50-95" in c][0]
        r0["d_val_ep24"] = float(new[col].iloc[-1] - old[col].iloc[-1])
    r0["match"] = abs(r0["d_ap"]) <= 0.005 and abs(r0.get("d_val_ep24", 0.0)) <= 0.005
    r0["env"] = ENV
    (RESULTS / "r0_check.json").write_text(json.dumps(r0, indent=2))
    print(json.dumps(r0, indent=1))
    raise StopRun("XONG ĐỢT 1. Ngắt runtime A100 để khỏi tốn CU, đổi sang L4, đặt PHASE = \"analyze\", rồi Run all.")
'''),
        md("""
## 3. Đợt 2: bảng 5 seed, P1, bootstrap

P1: A2 − A0, AP_vt, head e2e. "Lặp lại được" khi Δ của cả seed 4 và seed 5 > 0, khoảng t theo seed của 5 seed không chứa 0, và Δ ≥ MEI_vt = 0,006.
"""),
        code(r'''
import c11x_results as cr, c11x_cache as cc, c11_bootstrap as cb
from aitodr_data import scene_key
r0 = json.loads((RESULTS / "r0_check.json").read_text())
print("R0 khớp:", r0["match"], "| Δ AP:", round(r0["d_ap"], 5), "| Δ val:", r0.get("d_val_ep24"))
if not r0["match"]:
    print("CẢNH BÁO: R0 không khớp. Theo phụ lục A2 mục 5, KHÔNG gộp seed 1–3 với seed 4–5 trong bài.")
absent = [rd.name for rd in RUN_DIRS if not (rd / "c11_done.json").exists()]
if absent:
    raise StopRun(f"Chưa train xong: {absent}. Chạy đợt 1 trước.")
print("sắp lại cache:", cc.align_caches(RUN_DIRS, RUNS_OLD / "c11_A0_s1" / "evalcache_e2e.npz"))
res = cr.collect_runs(RUNS_OLD)
res = res[res["arm"].isin(ARMS) & res["seed"].isin(ALL_SEEDS)]
assert (res.groupby(["head", "arm"]).size() == len(ALL_SEEDS)).all(), res.groupby(["head", "arm"]).size()
display(cr.summary_table(res).round(4))
for h in ("e2e", "nms"):
    display(cr.per_seed_table(res, h).round(4))
res.to_csv(RESULTS / "results_long.csv", index=False)
PAIRS = [p for p in [("A2", "A0"), ("A8", "A0"), ("A2", "A8")] if set(p) <= set(ARMS)]
KEYS = ("AP_vt", "AP_t", "AP_s", "AP_m", "AP")
rows = []
for head, B in (("e2e", 10_000), ("nms", 2_000)):
    f = RESULTS / f"bootstrap_{head}_B{B}.json"
    t0 = time.time()
    boot = json.loads(f.read_text()) if f.exists() else cr.run_scene_bootstrap(cb, [RUNS_OLD], head, PAIRS, KEYS, B, scene_key, f)
    print(head, f"{(time.time() - t0) / 3600:.2f} giờ", boot.get("_c11x_meta", {}).get("seeds"), flush=True)
    for x, y in PAIRS:
        for m in KEYS:
            sc, sd = boot[f"{x}-{y}"][m], cr.paired_seed_deltas(res, head, x, y, m)
            assert abs(sc["delta"] - sd["mean"]) < 2e-4, ("Δ từ cache lệch eval json", head, x, y, m, sc["delta"], sd["mean"])
            cmb = cr.combine_scene_seed(sc, sd)
            rows.append(dict(head=head, pair=f"{x}-{y}", metric=m, delta=sc["delta"], scene_lo=sc["ci_lo"], scene_hi=sc["ci_hi"],
                             seed_t_lo=sd.get("t_lo"), seed_t_hi=sd.get("t_hi"), seed_min=sd.get("min"), seed_max=sd.get("max"),
                             s4=sd["per_seed"].get(4), s5=sd["per_seed"].get(5), comb_lo=cmb["lo"], comb_hi=cmb["hi"],
                             comb_excl0=cmb.get("excludes_zero")))
ci = pd.DataFrame(rows); display(ci.round(4)); ci.to_csv(RESULTS / "ci_scene_seed.csv", index=False)
p1 = ci[(ci["head"] == "e2e") & (ci["pair"] == "A2-A0") & (ci["metric"] == "AP_vt")].iloc[0]
MEI_VT = 0.006
same_dir = p1["s4"] > 0 and p1["s5"] > 0 and p1["seed_t_lo"] > 0
verdict = "Lặp lại được" if same_dir and p1["delta"] >= MEI_VT else "Có hướng nhưng dưới MEI" if same_dir else "Không lặp lại"
p1_out = dict(verdict=verdict, delta=p1["delta"], s4=p1["s4"], s5=p1["s5"], seed_t=[p1["seed_t_lo"], p1["seed_t_hi"]],
              scene_ci=[p1["scene_lo"], p1["scene_hi"]], combined_ci=[p1["comb_lo"], p1["comb_hi"]], mei=MEI_VT, r0_match=r0["match"])
(RESULTS / "p1_verdict.json").write_text(json.dumps(p1_out, indent=2, ensure_ascii=False, default=float))
print(json.dumps(p1_out, indent=1, ensure_ascii=False, default=float))
'''),
        md("""
## 4. Đợt 2: theo từng GT trên tập test, seed 1–5, head e2e (M1, M2, M3)

- `score ≥ 0,25` là chính; `score ≥ 0,05` kiểm độ nhạy. Ở 0,25, "bỏ sót" gồm cả hộp đúng chỗ nhưng điểm thấp.
- Mỗi run lưu một file trên Drive; chạy lại thì bỏ qua run đã xong.
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
    raise StopRun(f"scene_key lệch: {len(pairs)} cặp, {pairs.a.nunique()} và {pairs.b.nunique()} nhóm.")
print(len(off), "GT;", off.scene.nunique(), "cụm cảnh, khớp aitodr_data.scene_key")
off2 = off[["stem", "gt", "scene", "bin", "nn16", "A0_cand", "cls"]].assign(starved_A0=off.A0_cand == 0,
                                                                            density=re_.density_bin(off.nn16).values)

def fates(score):
    d = MECH / f"fates_e2e_score{score:g}"
    d.mkdir(parents=True, exist_ok=True)
    frames = []
    for s in ALL_SEEDS:
        for a in ARMS:
            f = d / f"{a}_s{s}.parquet"
            if not f.exists():
                t0 = time.time()
                re_.fates_run(LABELS / "test", stems, RUNS_OLD / cp.run_name(a, s) / "dota_e2e", score).to_parquet(f)
                print(score, a, s, f"{time.time() - t0:.0f}s", flush=True)
            frames.append(pd.read_parquet(f).assign(arm=a, seed=s))
    df = pd.concat(frames, ignore_index=True).merge(off2, on=["stem", "gt"], how="left", validate="many_to_one")
    assert df["scene"].notna().all(), "có GT không khớp bảng nhãn"
    return df.assign(detected=lambda x: x["det_0.5"])

summary = {"p1": p1_out}
for score in (0.25, 0.05):
    df, tag = fates(score), f"e2e_score{score:g}"
    t, c = re_.fate_table(df), re_.recall_curve(df)
    t.to_csv(MECH / f"fate_by_arm_bin_{tag}.csv"); c.to_csv(MECH / f"recall_iou_by_arm_bin_{tag}.csv")
    re_.fate_table(df, by=("arm", "bin", "starved_A0")).to_csv(MECH / f"fate_by_arm_bin_starved_{tag}.csv")
    re_.fate_table(df, by=("arm", "bin", "density")).to_csv(MECH / f"fate_by_arm_bin_density_{tag}.csv")
    display(t.round(3)); display(c.round(3))
    vt = df[df.bin == "vt"]
    mech = {"M1_A2-A0_starved_vs_not": did.did_bootstrap(vt, "A2", "A0", group="starved_A0", g1=True, g0=False)}
    if "A8" in ARMS:
        mech["M2_A2-A8_dense_vs_isolated"] = did.did_bootstrap(vt, "A2", "A8", group="density", g1=">=3", g0="isolated")
    for k, r in mech.items():
        r["combined"] = cr.combine_scene_seed(r["scene"], r["seed"])
        print(tag, k, {x: round(r["combined"][x], 4) for x in ("delta", "lo", "hi")}, "CI gộp loại 0:", r["combined"]["excludes_zero"],
              "theo seed:", {s: round(v, 4) for s, v in r["seed"]["per_seed"].items()})
    (MECH / f"mech_{tag}.json").write_text(json.dumps(mech, indent=2, default=float))
    summary[tag] = {k: dict(delta=r["combined"]["delta"], lo=r["combined"]["lo"], hi=r["combined"]["hi"],
                            supported=bool(r["combined"]["delta"] > 0 and r["combined"]["excludes_zero"])) for k, r in mech.items()}
(RESULTS / "env.json").write_text(json.dumps(ENV, indent=2))
(RESULTS / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, default=float))
print(json.dumps(summary, indent=1, ensure_ascii=False, default=float))
print("XONG. Gửi lại ô này và thư mục", RESULTS)
'''),
    ]


def build():
    meta = {"accelerator": "GPU", "colab": {"gpuType": "A100", "provenance": []},
            "kernelspec": {"display_name": "Python 3", "name": "python3"}, "language_info": {"name": "python"}}
    nb = nbf.v4.new_notebook(cells=cells(), metadata=meta)
    nbf.validate(nb)
    nbf.write(nb, OUT)
    print("ghi", OUT.name, len(nb.cells), "ô")


if __name__ == "__main__":
    build()
