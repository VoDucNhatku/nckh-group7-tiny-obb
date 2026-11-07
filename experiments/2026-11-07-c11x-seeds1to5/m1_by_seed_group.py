"""M1 tách theo nhóm seed (phụ lục A2 mục 5: R0 không khớp nên không gộp seed 1–3 với seed 4–5).

Cùng phép tính với ô mục 4 của C11x_train_confirm_colab.ipynb, chỉ đổi tập seed: trước hết chạy lại trên
seed 1–5 và so với mech_*.json (phải trùng), rồi chạy cho {1,2,3} và {4,5}.
Đầu vào ở _local/ (không lên Git: bảng theo GT chứa hình học nhãn). Bản gốc trên Drive:
NCKH/repo/NCKH/experiments/c11x-seeds1to5-results/mechanism/. Chạy: python m1_by_seed_group.py
"""
import json
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(ROOT / "scripts/rq2"), str(ROOT / "scripts/c11x")]
import c11x_results as cr  # noqa: E402
import rq2_did as did  # noqa: E402

LOCAL = HERE / "_local" / "mechanism"
GROUPS = {"1-5": [1, 2, 3, 4, 5], "1-3": [1, 2, 3], "4-5": [4, 5]}

off = pd.read_csv(LOCAL / "rq2_test" / "rq2_per_gt.csv.gz")
off2 = off[["stem", "gt", "scene", "bin", "A0_cand"]].assign(starved_A0=off.A0_cand == 0)
out = {}
for score in (0.25, 0.05):
    tag = f"e2e_score{score:g}"
    frames = [pd.read_parquet(LOCAL / f"fates_{tag}" / f"{a}_s{s}.parquet").assign(arm=a, seed=s)
              for s in GROUPS["1-5"] for a in ("A0", "A2")]
    df = pd.concat(frames, ignore_index=True).merge(off2, on=["stem", "gt"], how="left", validate="many_to_one")
    assert df["scene"].notna().all()
    vt = df[df.bin == "vt"].assign(detected=lambda x: x["det_0.5"])
    ref = json.loads((HERE / "mechanism" / f"mech_{tag}.json").read_text())["M1_A2-A0_starved_vs_not"]
    out[tag] = {}
    for name, seeds in GROUPS.items():
        r = did.did_bootstrap(vt[vt.seed.isin(seeds)], "A2", "A0", group="starved_A0", g1=True, g0=False)
        c = cr.combine_scene_seed(r["scene"], r["seed"])
        out[tag][name] = dict(delta=r["scene"]["delta"], scene_ci=[r["scene"]["ci_lo"], r["scene"]["ci_hi"]],
                              combined_ci=[c["lo"], c["hi"]], combined_excludes_zero=bool(c["excludes_zero"]),
                              per_seed=r["seed"]["per_seed"], n_scene=r["n_scene"])
        if name == "1-5":  # phải trùng kết quả của notebook
            assert abs(r["scene"]["delta"] - ref["scene"]["delta"]) < 1e-12
            assert abs(c["lo"] - ref["combined"]["lo"]) < 1e-9 and abs(c["hi"] - ref["combined"]["hi"]) < 1e-9
        print(tag, name, {k: (round(v, 4) if isinstance(v, float) else [round(x, 4) for x in v])
                          for k, v in out[tag][name].items() if k in ("delta", "scene_ci", "combined_ci")})
(HERE / "m1_by_seed_group.json").write_text(json.dumps(out, indent=2))
