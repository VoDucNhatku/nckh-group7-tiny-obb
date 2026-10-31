"""Gộp kết quả run, bảng theo seed, và gộp bất định theo cảnh với bất định theo seed (hướng 1, hướng 5).

Sửa lỗi đếm trùng của ô #32 trong `C11_colab.ipynb`: chỉ đọc đúng tên `eval_e2e.json` / `eval_nms.json`, không
glob `eval_*.json` (file `eval_e2e_recheck.json` từng bị đếm như một seed thứ tư của A0), và chặn trùng bằng assert.

Không import `scripts/c11`. Hàm `run_scene_bootstrap` nhận module `c11_bootstrap` trên Drive làm tham số.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

HEADS = ("e2e", "nms")
DONE_FILES = ("c11_done.json", "c11x_done.json")  # run cũ (scripts/c11) và run mới (c11x_train)


def _run_meta(rd: Path) -> dict | None:
    for name in DONE_FILES:
        f = rd / name
        if f.exists():
            d = json.loads(f.read_text())
            return {"arm": d["arm"], "seed": int(d["seed"]), "batch_changed": d.get("batch_changed"),
                    "source": name}
    return None


def collect_runs(*runs_dirs, heads=HEADS) -> pd.DataFrame:
    """Một dòng cho mỗi (run, head). arm/seed đọc từ file done, không đoán từ tên thư mục."""
    recs = []
    for runs_dir in runs_dirs:
        for rd in sorted(Path(runs_dir).glob("c11*_s*")):
            meta = _run_meta(rd)
            if meta is None:
                continue
            for head in heads:
                f = rd / f"eval_{head}.json"  # đúng tên; *_recheck.json không được tính
                if not f.exists():
                    continue
                d = json.loads(f.read_text())
                stats = {k: float(v) for k, v in d.items()
                         if (k.startswith("AP") or k.startswith("AR")) and isinstance(v, (int, float))}
                recs.append(dict(run=rd.name, runs_dir=str(runs_dir), head=head, **meta, **stats))
    df = pd.DataFrame(recs)
    if len(df):
        dup = df.duplicated(["arm", "seed", "head"], keep=False)
        assert not dup.any(), f"run bị đếm hai lần:\n{df.loc[dup, ['run', 'arm', 'seed', 'head']]}"
    return df


def summary_table(df: pd.DataFrame, metrics=("AP", "AP50", "AP_vt", "AP_t", "AP_s", "AR1500")) -> pd.DataFrame:
    """mean, sd, n theo head × arm (mô tả)."""
    m = [c for c in metrics if c in df]
    return df.groupby(["head", "arm"])[m].agg(["mean", "std", "count"])


def per_seed_table(df: pd.DataFrame, head: str, metrics=("AP", "AP_vt", "AP_t", "AP_s")) -> pd.DataFrame:
    """Hàng = seed, cột = (metric, arm). Để thấy trực tiếp dao động theo seed bên cạnh CI theo cảnh."""
    m = [c for c in metrics if c in df]
    return df[df["head"] == head].pivot_table(index="seed", columns="arm", values=m)


def paired_seed_deltas(df: pd.DataFrame, head: str, x: str, y: str, metric: str) -> dict:
    """Δ theo từng seed (cùng seed cho hai arm), rồi mean, sd, khoảng t 95% với n − 1 bậc tự do, min, max."""
    from scipy import stats

    d = df[df["head"] == head].pivot_table(index="seed", columns="arm", values=metric)
    if x not in d or y not in d:
        return {"n": 0}
    delta = (d[x] - d[y]).dropna()
    n = len(delta)
    out = {"n": n, "per_seed": delta.round(6).to_dict(), "mean": float(delta.mean()) if n else math.nan,
           "min": float(delta.min()) if n else math.nan, "max": float(delta.max()) if n else math.nan}
    if n >= 2:
        sd = float(delta.std(ddof=1))
        half = stats.t.ppf(0.975, n - 1) * sd / math.sqrt(n)
        out.update(sd=sd, se=sd / math.sqrt(n), t_lo=out["mean"] - half, t_hi=out["mean"] + half,
                   n_pos_sign=int((delta > 0).sum()))
    return out


def combine_scene_seed(scene: dict, seed: dict, z: float = 1.959964) -> dict:
    """[design] Khoảng gộp xấp xỉ: Δ ± q·√(se_cảnh² + se_seed²), q = t_{0,975; n − 1} với n = số seed.

    Phụ lục A1 của preregistration: bản v1 dùng q = z ≈ 1,96, quá hẹp khi se_seed chỉ có n − 1 = 2 bậc tự do
    (t_{0,975; 2} ≈ 4,30). Lấy bậc tự do của nguồn ít bậc nhất nên khoảng thiên về rộng.
    se_cảnh suy từ CI percentile của bootstrap theo cảnh: (hi − lo) / (2z). Nếu JSON bootstrap có `sd` thì dùng sd.
    se_seed = sd(Δ theo seed) / √n. Giả định hai nguồn độc lập; luôn báo kèm khoảng t thuần theo seed
    (`paired_seed_deltas`). Đây là quy ước báo cáo đã khai trong preregistration, không phải phép thử chính xác.
    """
    from scipy import stats

    se_scene = scene.get("sd") or (scene["ci_hi"] - scene["ci_lo"]) / (2 * z)
    se_seed = seed.get("se", math.nan)
    n = seed.get("n", 0)
    if not np.isfinite(se_seed) or n < 2:
        return {"delta": scene["delta"], "lo": math.nan, "hi": math.nan, "se_scene": se_scene, "se_seed": se_seed}
    q = float(stats.t.ppf(0.975, n - 1))
    se = math.sqrt(se_scene ** 2 + se_seed ** 2)
    return {"delta": scene["delta"], "lo": scene["delta"] - q * se, "hi": scene["delta"] + q * se, "q": q,
            "se_scene": se_scene, "se_seed": se_seed, "excludes_zero": abs(scene["delta"]) > q * se}


def ci_skew(scene: dict) -> float:
    """(hi − Δ) / (Δ − lo). Gần 1 là đối xứng. Lệch xa 1 (vd > 2 hoặc < 0,5) thì phải kiểm phân phối bootstrap."""
    lo_gap = scene["delta"] - scene["ci_lo"]
    return (scene["ci_hi"] - scene["delta"]) / lo_gap if lo_gap > 0 else math.inf


def head_interaction(df: pd.DataFrame, x: str, base: str, metric: str) -> pd.DataFrame:
    """Hướng 1: theo từng seed, Δ_head = metric(x) − metric(base) cho mỗi head, và hiệu Δ_nms − Δ_e2e."""
    d = df.pivot_table(index="seed", columns=["head", "arm"], values=metric)
    out = pd.DataFrame(index=d.index)
    for h in HEADS:
        if (h, x) in d and (h, base) in d:
            out[f"d_{h}"] = d[(h, x)] - d[(h, base)]
    if {"d_e2e", "d_nms"} <= set(out):
        out["d_nms_minus_d_e2e"] = out["d_nms"] - out["d_e2e"]
    return out.dropna(how="all")


def seeds_needed(delta: float, sd_diff: float, alpha=0.05, power=0.8) -> float:
    """Hướng 5: số seed ghép cặp xấp xỉ cần để phát hiện Δ với sd của hiệu theo seed (xấp xỉ chuẩn, hai phía)."""
    from scipy import stats

    if delta == 0 or not np.isfinite(sd_diff):
        return math.inf
    zz = stats.norm.ppf(1 - alpha / 2) + stats.norm.ppf(power)
    return math.ceil((zz * sd_diff / abs(delta)) ** 2)


def scene_key_audit(stems, scene_key) -> dict:
    """Kiểm nhóm cảnh của phần không-xView (vấn đề 3.1.6 của báo cáo nhận xét).

    Tên ô cắt kiểu VisDrone/DOTA có hậu tố vị trí `__<x>_<y>` (vd `9999955_00000_d_0000223__0_0`). Các ô cùng tiền tố
    trước `__` đến từ cùng một ảnh gốc, nên phải cùng nhóm. Trả về số tiền tố bị `scene_key` tách thành nhiều nhóm.
    """
    stems = list(stems)
    by_prefix: dict[str, set] = {}
    for s in stems:
        if "__" in s:
            by_prefix.setdefault(s.split("__")[0], set()).add(scene_key(s))
    split = {p: sorted(map(str, g)) for p, g in by_prefix.items() if len(g) > 1}
    groups = {scene_key(s) for s in stems}
    return {"n_stems": len(stems), "n_groups": len(groups), "n_crop_prefixes": len(by_prefix),
            "n_prefixes_split": len(split), "examples": dict(list(split.items())[:5])}


def run_scene_bootstrap(cb, runs_dirs, head, pairs, keys, B, scene_key, out_json, engine="weighted") -> dict:
    """Gọi `c11_bootstrap.multi_pair_bootstrap` (module trên Drive) với cache `evalcache_<head>.npz`.

    Chỉ nhận run có file done; mỗi (arm, seed) đúng một cache. Ghi JSON kèm B, head, keys, seed của từng arm.
    """
    by_arm, seeds = {}, {}
    for runs_dir in runs_dirs:
        for rd in sorted(Path(runs_dir).glob("c11*_s*")):
            meta, f = _run_meta(rd), rd / f"evalcache_{head}.npz"
            if meta is None or not f.exists():
                continue
            assert meta["seed"] not in seeds.get(meta["arm"], []), f"trùng {meta}"
            seeds.setdefault(meta["arm"], []).append(meta["seed"])
            by_arm.setdefault(meta["arm"], []).append(cb.load_cache(f))
    pairs = [(x, y) for x, y in pairs if len(by_arm.get(x, [])) >= 2 and len(by_arm.get(y, [])) >= 2]
    boot = cb.multi_pair_bootstrap({a: by_arm[a] for a in {z for p in pairs for z in p}}, pairs, scene_key,
                                   keys=tuple(keys), B=B, engine=engine)
    boot["_c11x_meta"] = dict(head=head, B=B, keys=list(keys), seeds=seeds, pairs=[f"{x}-{y}" for x, y in pairs])
    Path(out_json).write_text(json.dumps(boot, indent=2, default=float))
    return boot
