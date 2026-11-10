"""Sinh notebooks/C11x_train_a8_colab.ipynb: A8 trên seed 4–5 theo preregistration, phụ lục A3.

    python scripts/c11x/build_a8_notebook.py

Sửa ở đây rồi chạy lại; không sửa tay file .ipynb. Luật nằm ở `a8_rule.py` (có test).
"""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf

from build_notebooks import DATA, DATA_MD, INSTALL, SETUP, SETUP_MD, TESTS, code, md

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "notebooks" / "C11x_train_a8_colab.ipynb"
BRANCH = "main"

FASTPATH = '"test_fastpath.py"])'
assert TESTS.count(FASTPATH) == 1
# test đường chấm nhanh chỉ cần ở đợt train (đợt phân tích không chấm lại); nó từng trượt ở môi trường đợt 2 ngày 07/11
TESTS_A8 = TESTS.replace(FASTPATH, '*(["test_fastpath.py"] if PHASE == "train" else [])])')


def cells():
    return [
        md("""
# C11x · Sàn phủ tối thiểu A8 trên seed 4–5

Theo `experiments/preregistration.md`, **phụ lục A3**. Câu hỏi: sàn nhỏ nhất đủ cho mọi hộp có ứng viên (A8, 8√2 ≈ 11,3 px) có cho mức tăng AP_vt như sàn 16 px của thư viện (A2) không.

**Đợt 1 làm gì:**
1. **R1:** train lại A2 seed 4 trong môi trường Colab hiện tại, so với run A2 seed 4 ngày 07/11. Quyết định ghi vào `a8_env_check.json`, chạy lại không tính lại.
2. **Khớp:** train A8 × seed 4, 5 (2 run), so với A0, A2 seed 4–5 đã có.
3. **Không khớp:** train A0, A8 × seed 4, 5 và A2 seed 5 (5 run) trong cùng môi trường; R1 là A2 seed 4 của nhóm mới.

| Đợt | `PHASE` | Runtime | Thời gian [ước lượng] |
|---|---|---|---|
| 1 | `"train"` | **A100** | khớp: khoảng 2,5 giờ; không khớp: khoảng 4,5 giờ |
| 2 | `"analyze"` | L4 (hoặc A100) | khoảng 1–2 giờ |

**Căn cứ ước lượng:** 0,57 giờ/run train và 337 giây/run/head chấm (log 07/11 và `C11_colab.ipynb`). Thời gian bootstrap và phân tích theo GT với 6 run chưa đo; con số trên là ước lượng. Tốc độ CU xem trong Colab.

**Cách chạy:** Run all. Bị ngắt thì Run all lại; phần đã xong tự bỏ qua. Xong đợt 1, notebook tự dừng và nhắc đổi sang đợt 2.
"""),
        md(SETUP_MD),
        code(SETUP + f'''
BRANCH = "{BRANCH}"
PHASE = "train"                                       # "train" (A100) rồi "analyze"
if not EXP_DRIVE.exists():
    raise StopRun(f"Không thấy {{EXP_DRIVE}}. Acc này cần quyền Editor trên thư mục NCKH và một shortcut tên NCKH "
                  "trong My Drive (Shared with me → chuột phải → Organize → Add shortcut → My Drive), rồi Run all lại.")
RUNS_A8 = EXP_DRIVE / "runs-woX-A8"                   # R1, và cả nhóm mới nếu R1 không khớp
RESULTS = EXP_DRIVE / "c11x-a8-results"
CHECK = RESULTS / "a8_env_check.json"
ARMS, SEEDS, SCORES = ["A0", "A8", "A2"], [4, 5], [0.25, 0.05]
DIAG_EVERY = 10                                       # giống seed 1–5
RESULTS.mkdir(parents=True, exist_ok=True)
assert PHASE in ("train", "analyze")
'''),
        code(INSTALL + '''
sys.path.insert(0, str(GH_DIR / "scripts/rq2"))
prereg_text = (GH_DIR / "experiments" / "preregistration.md").read_text(encoding="utf-8")
# Khóa thật: phụ lục A3 phải nằm trên main và BRANCH dùng đúng bản đó.
subprocess.run(["git", "-C", str(GH_DIR), "fetch", "-q", "--depth", "1", "origin", "main"], check=True)
main_prereg = subprocess.check_output(["git", "-C", str(GH_DIR), "show", "FETCH_HEAD:experiments/preregistration.md"]).decode()
if "### A3 ·" not in main_prereg:
    raise StopRun("Phụ lục A3 chưa có trên main. Merge PR chứa phụ lục A3 trước, rồi Run all.")
if prereg_text != main_prereg:
    raise StopRun('preregistration của BRANCH khác bản trên main. Đặt BRANCH = "main" rồi Run all.')
print(subprocess.check_output(["git", "-C", str(GH_DIR), "log", "-1", "--format=preregistration: %H %ci", "--",
                               "experiments/preregistration.md"]).decode())
if PHASE == "train" and "A100" not in str(ENV["gpu"]):
    raise StopRun(f"Đợt train phải dùng A100 như seed 1–5, đang là {ENV['gpu']}.")
SEEDS45_ENV = json.loads((GH_DIR / "experiments/2026-11-07-c11x-seeds1to5/r0_check.json").read_text())["env"]
print("môi trường train seed 4–5 ngày 07/11:", SEEDS45_ENV)
print("môi trường hiện tại:               ", ENV)
'''),
        code(TESTS_A8 + r'''
run_pytest(GH_DIR / "scripts/rq2", ["test_errors_did.py", "test_recall.py", "-p", "no:cacheprovider"])
'''),
        md(DATA_MD),
        code(DATA),
        code(r'''
import inspect, pandas as pd, c11_pipeline as cp, a8_rule as ar
missing = {"project", "diag_every"} - set(inspect.signature(cp.train_arm).parameters)
if missing:
    raise StopRun(f"c11_pipeline.train_arm trên Drive thiếu tham số {missing}")
need = [RUNS_OLD / cp.run_name(a, s) for a in ("A0", "A2") for s in SEEDS]
absent = [rd.name for rd in need if not ((rd / "c11_done.json").exists() and (rd / "eval_e2e.json").exists())]
if absent:
    raise StopRun(f"Thiếu run seed 4–5 của ngày 07/11 trong runs-woX: {absent}")
TEST_IMAGES = DS / "images" / "test"

def ap_e2e(rd):
    return json.loads((rd / "eval_e2e.json").read_text())["AP"]

def last_val(rd):
    f = rd / "results.csv"
    if not f.exists():
        return None
    d = pd.read_csv(f)
    d.columns = d.columns.str.strip()
    return float(d[[c for c in d.columns if "mAP50-95" in c][0]].iloc[-1])

def train_eval(a, s, project, heads=("e2e", "nms")):
    rd = Path(project) / cp.run_name(a, s)
    if not (rd / "c11_done.json").exists():
        t0 = time.time()
        print(">>> train", a, s, "→", project.name, "GPU:", ENV["gpu"], flush=True)
        cp.train_arm(DATA_YAML, a, s, project=project, diag_every=DIAG_EVERY)
        print(rd.name, f"xong sau {(time.time() - t0) / 3600:.2f} giờ", flush=True)
    for head in heads:
        out = rd / f"eval_{head}.json"
        if out.exists():
            continue
        st = cp.predict_and_eval(rd / "weights" / "last.pt", LABELS / "test", TEST_IMAGES, out, head=head,
                                 version=VERSION, exclude_stems=EXCLUDE, save_dota_dir=rd / f"dota_{head}")
        print(rd.name, head, {k: round(st[k], 4) for k in ("AP", "AP_vt", "AP_t", "AP_s")}, flush=True)
    return rd
'''),
        md("""
## 2. Đợt 1: R1 rồi train A8

R1 chỉ chấm head e2e trước khi quyết định (đủ cho luật); nếu không khớp, head nms của R1 được chấm sau cùng nhóm mới.
"""),
        code(r'''
if PHASE == "train":
    if not CHECK.exists():
        rd1, old1 = train_eval("A2", 4, RUNS_A8, heads=("e2e",)), RUNS_OLD / cp.run_name("A2", 4)
        r1 = ar.r1_check(ap_e2e(rd1), ap_e2e(old1), last_val(rd1), last_val(old1))
        group, todo = ar.jobs(r1["match"])
        r1.update(group=group, todo=todo, env=ENV, env_seeds45_train=SEEDS45_ENV)
        CHECK.write_text(json.dumps(r1, indent=2, ensure_ascii=False))
    r1 = json.loads(CHECK.read_text())
    print(json.dumps(r1, indent=1, ensure_ascii=False))
    project = EXP_DRIVE / r1["group"]
    for a, s in r1["todo"] + ([] if r1["match"] else [["A2", 4]]):
        train_eval(a, s, project)
    raise StopRun("XONG ĐỢT 1. Ngắt runtime A100 để khỏi tốn CU, đặt PHASE = \"analyze\", rồi Run all.")
'''),
        md("""
## 3. Đợt 2: P2 và bảng mô tả

- **P2a (chính):** Δ AP_vt(A8 − A0), head e2e, seed 4 và 5. "Lặp lại được" khi cả hai > 0 và trung bình ≥ 0,006.
- **P2b (phụ):** trung bình Δ AP_vt(A8 − A2) ≥ −0,006.
- **AP_m:** chỉ báo từng seed, không gắn nhãn (phụ lục A3 mục 5).
"""),
        code(r'''
import c11x_results as cr, c11x_cache as cc, c11_bootstrap as cb
from aitodr_data import scene_key
if not CHECK.exists():
    raise StopRun("Chưa có a8_env_check.json. Chạy đợt 1 trước.")
r1 = json.loads(CHECK.read_text())
project = EXP_DRIVE / r1["group"]
print("R1 khớp:", r1["match"], "| nhóm:", r1["group"], "| Δ AP:", round(r1["d_ap"], 5), "| Δ val:", r1["d_val_last"])
RUN_DIRS = [project / cp.run_name(a, s) for s in SEEDS for a in ARMS]
absent = [rd.name for rd in RUN_DIRS if not all((rd / f).exists() for f in ("c11_done.json", "eval_e2e.json", "eval_nms.json"))]
if absent:
    raise StopRun(f"Chưa train hoặc chấm xong: {absent}. Chạy đợt 1 trước.")
print("sắp lại cache:", cc.align_caches(RUN_DIRS, RUNS_OLD / "c11_A0_s1" / "evalcache_e2e.npz"))
res = cr.collect_runs(project)
res = res[res["arm"].isin(ARMS) & res["seed"].isin(SEEDS)]
assert (res.groupby(["head", "arm"]).size() == len(SEEDS)).all(), res.groupby(["head", "arm"]).size()
if res["batch_changed"].fillna(False).astype(bool).any():
    raise StopRun(f"Run bị đổi batch (preregistration §7): {res.loc[res.batch_changed == True, 'run'].tolist()}. "
                  "Loại và báo; P2 không phán quyết được.")
res.to_csv(RESULTS / "results_long.csv", index=False)
for h in ("e2e", "nms"):
    display(cr.per_seed_table(res, h, metrics=("AP", "AP_vt", "AP_t", "AP_s", "AP_m")).round(4))
d = lambda x, y, m: cr.paired_seed_deltas(res, "e2e", x, y, m)["per_seed"]
p2 = ar.p2_verdict(d("A8", "A0", "AP_vt"), d("A8", "A2", "AP_vt"), d("A8", "A2", "AP_m"))
p2.update(group=r1["group"], r1_match=r1["match"], rule="PREREG-C11X-v1 + A3")
(RESULTS / "p2_verdict.json").write_text(json.dumps(p2, indent=2, ensure_ascii=False, default=float))
print(json.dumps(p2, indent=1, ensure_ascii=False, default=float))

PAIRS = [("A8", "A0"), ("A2", "A8"), ("A2", "A0")]
KEYS = ("AP_vt", "AP_t", "AP_s", "AP_m", "AP")
f = RESULTS / "bootstrap_e2e_B10000.json"
t0 = time.time()
boot = json.loads(f.read_text()) if f.exists() else cr.run_scene_bootstrap(cb, [project], "e2e", PAIRS, KEYS, 10_000,
                                                                             scene_key, f, only_seeds=SEEDS)
print(f"bootstrap {(time.time() - t0) / 3600:.2f} giờ", boot["_c11x_meta"]["seeds"], flush=True)
rows = []
for x, y in PAIRS:
    for m in KEYS:
        sc, sd = boot[f"{x}-{y}"][m], cr.paired_seed_deltas(res, "e2e", x, y, m)
        assert abs(sc["delta"] - sd["mean"]) < 2e-4, ("Δ từ cache lệch eval json", x, y, m, sc["delta"], sd["mean"])
        cmb = cr.combine_scene_seed(sc, sd)
        rows.append(dict(head="e2e", pair=f"{x}-{y}", metric=m, delta=sc["delta"], scene_lo=sc["ci_lo"],
                         scene_hi=sc["ci_hi"], s4=sd["per_seed"].get(4), s5=sd["per_seed"].get(5),
                         comb_lo=cmb["lo"], comb_hi=cmb["hi"], comb_excl0=cmb.get("excludes_zero")))
ci = pd.DataFrame(rows); display(ci.round(4)); ci.to_csv(RESULTS / "ci_scene_seed.csv", index=False)
'''),
        md("""
## 4. Đợt 2: theo từng GT trên test, seed 4–5, head e2e (mô tả)

Số phận GT, recall theo IoU, M1 cho A8 − A0 và A2 − A0, M2 (A2 − A8, cụm dày so với cô lập). Chỉ mô tả (phụ lục A3 mục 6).
"""),
        code(r'''
import rq2_errors as re_, rq2_did as did
RQ2_DIR, MECH = GH_DIR / "scripts/rq2", RESULTS / "mechanism"
OFF_OLD = EXP_DRIVE / "c11x-seeds1to5-results" / "mechanism" / "rq2_test"
OFF = OFF_OLD if (OFF_OLD / "rq2_per_gt.csv.gz").exists() else MECH / "rq2_test"
if not (OFF / "rq2_per_gt.csv.gz").exists():
    subprocess.run([sys.executable, "rq2_offline.py", "--labels", str(LABELS / "test"), "--out", str(OFF),
                    "--protocol", "woX", "--arms", "A0,A1,A8,A2"], cwd=str(RQ2_DIR), check=True)
off = pd.read_csv(OFF / "rq2_per_gt.csv.gz")
stems = sorted(off.stem.unique())
if set(stems) & set(EXCLUDE):
    raise StopRun("bảng theo GT còn ảnh xView.")
off2 = off[["stem", "gt", "scene", "bin", "nn16", "A0_cand", "cls"]].assign(starved_A0=off.A0_cand == 0,
                                                                            density=re_.density_bin(off.nn16).values)

def fates(score):
    dd = MECH / f"fates_e2e_score{score:g}"
    dd.mkdir(parents=True, exist_ok=True)
    frames = []
    for s in SEEDS:
        for a in ARMS:
            fp = dd / f"{r1['group']}_{a}_s{s}.parquet"
            if not fp.exists():
                t0 = time.time()
                re_.fates_run(LABELS / "test", stems, project / cp.run_name(a, s) / "dota_e2e", score).to_parquet(fp)
                print(score, a, s, f"{time.time() - t0:.0f}s", flush=True)
            frames.append(pd.read_parquet(fp).assign(arm=a, seed=s))
    df = pd.concat(frames, ignore_index=True).merge(off2, on=["stem", "gt"], how="left", validate="many_to_one")
    assert df["scene"].notna().all(), "có GT không khớp bảng nhãn"
    return df.assign(detected=lambda x: x["det_0.5"])

summary = {"p2": p2, "r1": r1}
for score in SCORES:
    df, tag = fates(score), f"e2e_score{score:g}"
    t, c = re_.fate_table(df), re_.recall_curve(df)
    t.to_csv(MECH / f"fate_by_arm_bin_{tag}.csv"); c.to_csv(MECH / f"recall_iou_by_arm_bin_{tag}.csv")
    re_.fate_table(df, by=("arm", "bin", "starved_A0")).to_csv(MECH / f"fate_by_arm_bin_starved_{tag}.csv")
    re_.fate_table(df, by=("arm", "bin", "density")).to_csv(MECH / f"fate_by_arm_bin_density_{tag}.csv")
    display(t.round(3)); display(c.round(3))
    vt = df[df.bin == "vt"]
    mech = {"M1_A8-A0_starved_vs_not": did.did_bootstrap(vt, "A8", "A0", group="starved_A0", g1=True, g0=False),
            "M1_A2-A0_starved_vs_not": did.did_bootstrap(vt, "A2", "A0", group="starved_A0", g1=True, g0=False),
            "M2_A2-A8_dense_vs_isolated": did.did_bootstrap(vt, "A2", "A8", group="density", g1=">=3", g0="isolated")}
    for k, r in mech.items():
        r["combined"] = cr.combine_scene_seed(r["scene"], r["seed"])
        print(tag, k, {x: round(r["combined"][x], 4) for x in ("delta", "lo", "hi")},
              "theo seed:", {s: round(v, 4) for s, v in r["seed"]["per_seed"].items()})
    (MECH / f"mech_{tag}.json").write_text(json.dumps(mech, indent=2, default=float))
    summary[tag] = {k: dict(delta=r["combined"]["delta"], lo=r["combined"]["lo"], hi=r["combined"]["hi"],
                            per_seed=r["seed"]["per_seed"]) for k, r in mech.items()}
(RESULTS / "env.json").write_text(json.dumps(ENV, indent=2))
(RESULTS / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, default=float))
print(json.dumps(summary, indent=1, ensure_ascii=False, default=float))
print("XONG. Gửi lại notebook kèm output và thư mục", RESULTS)
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
