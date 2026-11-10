"""Build the appendix of the paper: status of every preregistered hypothesis, recipe, evaluator check, environments.

Reads only files in the repo: the saved outputs of C11_colab.ipynb and notebooks/C11x_analysis_colab.ipynb, and
experiments/2026-10-30-c11x-analysis/ (gate JSON and exploratory CI table written by export_explor.py).
Writes paper/tables/appendix_macros.tex and paper/tables/appendix_prereg.tex.

    python scripts/c11x/export_appendix.py
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAB = ROOT / "paper" / "tables"
EXP = ROOT / "experiments" / "2026-10-30-c11x-analysis"
MEI_VT = 0.006
ARMS = ("A1", "A8", "A2")


def outputs(nb_path: Path, index: int) -> str:
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    parts = []
    for o in nb["cells"][index].get("outputs", []):
        if "text" in o:
            parts.append("".join(o["text"]))
        elif "data" in o and "text/plain" in o["data"]:
            parts.append("".join(o["data"]["text/plain"]))
    return "\n".join(parts)


def last_output(nb_path: Path) -> str:
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    return outputs(nb_path, len(nb["cells"]) - 1)


def block(text: str, name: str) -> list[list[str]]:
    """Rows of a pandas frame printed after '=== <name> (... bytes) ==='."""
    part = text.split(f"=== {name}", 1)[1].split("\n", 1)[1]
    part = part.split("\n===", 1)[0]
    return [ln.split() for ln in part.strip().splitlines()]


def num(x: float, d: int = 3, sign: bool = True) -> str:
    return (f"{x:+.{d}f}" if sign else f"{x:.{d}f}").replace("-", "$-$")


def main():
    c11 = ROOT / "C11_colab.ipynb"
    an = ROOT / "notebooks" / "C11x_analysis_colab.ipynb"
    env_old = eval(re.search(r"\{'ultralytics'.*?\}", outputs(c11, 5)).group(0))  # dict printed by the notebook
    ev = outputs(c11, 14)
    roundtrip = float(re.search(r'"frac_ge_0999":\s*([\d.]+)', ev).group(1))
    oracle_ap = float(re.search(r'"AP":\s*([\d.]+)', ev).group(1))
    oracle_vt = float(re.search(r'"AP_vt":\s*([\d.]+)', ev).group(1))
    recipe = eval(re.search(r"'recipe':\s*(\{.*?\})\}", outputs(c11, 21)).group(1))
    env_new = json.loads((ROOT / "experiments/2026-11-07-c11x-seeds1to5/r0_check.json").read_text())["env"]
    env_ph2 = json.loads((ROOT / "experiments/2026-11-07-c11x-seeds1to5/env.json").read_text())

    gate = json.loads((EXP / "c11x-h2-gate.json").read_text())
    rec = {k: v[0] for k, v in gate["recall_lt8_by_npos"].items()}
    cnt = {k: v[1] for k, v in gate["recall_lt8_by_npos"].items()}
    ge2 = sum(rec[k] * cnt[k] for k in ("2", "3-4", "5-9", "10+")) / sum(cnt[k] for k in ("2", "3-4", "5-9", "10+"))
    h2b_first, h2b_rest = rec["1"] - rec["0"], ge2 - rec["1"]

    text = last_output(an)
    med = {r[1].split("[T.")[1].rstrip("]"): (float(r[2]), float(r[3])) for r in block(text, "mediation_nms_o2m.csv")[1:]}
    h2c = {a: abs(w) <= 0.5 * abs(wo) for a, (wo, w) in med.items()}
    ang_rows = [r for r in block(text, "angle_error_by_size.csv")[1:] if r[1] == "e2e"]
    bins = ["<4", "4-8", "8-11.3", "11.3-16", "16-32", "32+"]
    ang = {(r[0], r[2]): float(r[3]) for r in ang_rows}
    monotone = {a: all(ang[(a, bins[i])] >= ang[(a, bins[i + 1])] for i in range(len(bins) - 1)) for a in ("A0",) + ARMS}
    spread = max(max(ang[(a, b)] for a in ("A0",) + ARMS) - min(ang[(a, b)] for a in ("A0",) + ARMS) for b in bins)
    peak_bin = max(bins, key=lambda b: ang[("A0", b)])

    hi = block(text, "head_interaction_per_seed.csv")
    d = {}
    for r in hi[1:]:
        if r[1] == "AP_vt":
            d.setdefault(r[0], []).append(float(r[5]))
    h1b_arms = [a for a, v in d.items() if (all(x > 0 for x in v) or all(x < 0 for x in v)) and abs(sum(v) / len(v)) >= MEI_VT]
    h1b_mean = {a: sum(v) / len(v) for a, v in d.items()}

    ci = list(csv.DictReader((EXP / "ci_scene_seed.csv").open(encoding="utf-8")))
    dl = {(r["head"], r["pair"], r["metric"]): float(r["delta"]) for r in ci}
    h1a = all(dl[(h, f"{a}-A0", "AP_vt")] > 0 for h in ("e2e", "nms") for a in ARMS)
    h1c = all(dl[(h, f"{a}-A0", "AP_s")] <= 0 for h in ("e2e", "nms") for a in ARMS)

    macros = {
        "rtFrac": f"{100 * roundtrip:.1f}", "oracleAP": f"{oracle_ap:.3f}", "oracleVt": f"{oracle_vt:.3f}",
        "lrZero": f"{recipe['lr0']}", "momentum": f"{recipe['momentum']}", "wDecay": f"{recipe['weight_decay']}",
        "warmup": f"{recipe['warmup_epochs']:g}", "flipP": f"{recipe['fliplr']}",
        "envOldNumpy": env_old["numpy"], "envOldPython": env_old["python"], "envOldTorch": env_old["torch"],
        "envNewNumpy": env_new["numpy"], "envNewPython": env_new["python"], "envPhTwoTorch": env_ph2["torch"],
        "nposCoef": num(gate["n_pos_coef"], 2), "nposLo": num(gate["n_pos_ci_lo"], 2), "nposHi": num(gate["n_pos_ci_hi"], 2),
        "hTwoBFirst": num(h2b_first), "hTwoBRest": num(h2b_rest),
        "medAtwoWo": num(med["A2"][0]), "medAtwoW": num(med["A2"][1]),
        "medAoneWo": num(med["A1"][0]), "medAoneW": num(med["A1"][1]),
        "medAeightWo": num(med["A8"][0]), "medAeightW": num(med["A8"][1]),
        "angPeakBin": peak_bin.replace("-", "--"), "angSpread": f"{spread:.1f}",
        "angPeak": f"{ang[('A0', peak_bin)]:.1f}", "angSmall": f"{ang[('A0', '11.3-16')]:.1f}",
        "hOneBMeanAtwo": num(h1b_mean["A2"], 4),
    }
    (TAB / "appendix_macros.tex").write_text("".join(f"\\newcommand{{\\{k}}}{{{v}}}\n" for k, v in macros.items()), encoding="utf-8")

    def status(ok, yes="holds", no="not supported"):
        return yes if ok else no

    rows = [
        ("H1a", "$\\Delta$AP$_{vt}>0$ for A1, A8, A2 vs A0, both heads", status(h1a, "holds (descriptive)")),
        ("H1b", "floor gain larger with the NMS head than with e2e", f"not supported: {len(h1b_arms)} of 3 arms meet the rule"),
        ("H1c", "$\\Delta$AP$_s\\leq 0$ for the floors, both heads", status(h1c, "holds (descriptive)")),
        ("H2a", "recall rises with candidate count (gate)", "not supported: coefficient negative"),
        ("H2b", "first positive matters most for boxes $<8$ px", f"holds in part: {num(h2b_first)} vs {num(h2b_rest)}; 95\\% share not computed"),
        ("H2c", "arm effect shrinks $\\geq 50\\%$ once positives enter", "holds for " + ", ".join(a for a in ARMS if h2c[a]) + "; not for " + ", ".join(a for a in ARMS if not h2c[a])),
        ("H3a--c", "K-floor runs", "cancelled after the gate"),
        ("H4a", "angle error falls with size", status(all(monotone.values()), "holds", f"not supported: peaks at {peak_bin.replace('-', '--')} px")),
        ("H4b", "arms within 2$^\\circ$ at equal size", status(spread <= 2, f"holds (max spread {spread:.1f}$^\\circ$)", "not supported")),
        ("P1", "$\\Delta$AP$_{vt}$(A2$-$A0) $>0$ on seeds 4, 5, mean $\\geq 0.006$", "replicated under the rule"),
        ("M1", "starved minus other very tiny boxes, $\\Delta$recall $>0$", "positive in every seed; criterion met on seeds 1--3, not on 4--5"),
        ("M2", "A2$-$A8 larger in dense clusters", "cancelled (A8 not trained)"),
        ("M3a", "missed is the largest fate (A2, very tiny)", "holds at score $\\geq 0.25$; reverses at $\\geq 0.05$"),
        ("M3b", "starved boxes keep lower recall under A2", "holds"),
        ("M3c", "IoU 0.25$\\to$0.5 drop larger for very tiny than tiny", "holds (seen on val first)"),
    ]
    lines = ["\\begin{tabular}{lp{6.2cm}p{6.2cm}}", "\\toprule", "ID & Prediction & Outcome \\\\", "\\midrule"]
    lines += [f"{a} & {b} & {c} \\\\" for a, b, c in rows]
    lines += ["\\bottomrule", "\\end{tabular}"]
    (TAB / "appendix_prereg.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Vietnamese version for paper/main_vi.tex: same outcomes, same numbers.
    def trang_thai(ok, yes="đúng", no="không được ủng hộ"):
        return yes if ok else no

    rows_vi = [
        ("H1a", "$\\Delta$AP$_{vt}>0$ cho A1, A8, A2 so với A0, cả hai đầu", trang_thai(h1a, "đúng (mô tả)")),
        ("H1b", "mức tăng do sàn ở đầu NMS lớn hơn ở đầu e2e", f"không được ủng hộ: {len(h1b_arms)} trên 3 nhánh đạt luật"),
        ("H1c", "$\\Delta$AP$_s\\leq 0$ với các sàn, cả hai đầu", trang_thai(h1c, "đúng (mô tả)")),
        ("H2a", "recall tăng theo số ứng viên (cổng)", "không được ủng hộ: hệ số âm"),
        ("H2b", "mẫu dương đầu tiên quan trọng nhất với hộp $<8$ px", f"đúng một phần: {num(h2b_first)} so với {num(h2b_rest)}; chưa tính tỉ lệ 95\\%"),
        ("H2c", "hiệu ứng của nhánh giảm $\\geq 50\\%$ khi đưa mẫu dương vào", "đúng với " + ", ".join(a for a in ARMS if h2c[a]) + "; không đúng với " + ", ".join(a for a in ARMS if not h2c[a])),
        ("H3a--c", "các lần chạy K-floor", "hủy sau cổng"),
        ("H4a", "sai số góc giảm theo kích thước", trang_thai(all(monotone.values()), "đúng", f"không được ủng hộ: cao nhất ở {peak_bin.replace('-', '--')} px")),
        ("H4b", "các nhánh lệch nhau trong 2$^\\circ$ ở cùng kích thước", trang_thai(spread <= 2, f"đúng (lệch tối đa {spread:.1f}$^\\circ$)", "không được ủng hộ")),
        ("P1", "$\\Delta$AP$_{vt}$(A2$-$A0) $>0$ trên seed 4, 5, trung bình $\\geq 0.006$", "lặp lại được theo luật"),
        ("M1", "hộp bị bỏ đói trừ hộp rất nhỏ khác, $\\Delta$recall $>0$", "dương ở mọi seed; đạt tiêu chí trên seed 1--3, không đạt trên 4--5"),
        ("M2", "A2$-$A8 lớn hơn ở cụm dày", "hủy (không huấn luyện A8)"),
        ("M3a", "bỏ sót là kết quả lớn nhất (A2, rất nhỏ)", "đúng ở score $\\geq 0.25$; đảo ngược ở $\\geq 0.05$"),
        ("M3b", "hộp bị bỏ đói vẫn có recall thấp hơn dưới A2", "đúng"),
        ("M3c", "mức giảm IoU 0.25$\\to$0.5 ở hộp rất nhỏ lớn hơn ở hộp tí hon", "đúng (đã thấy trên tập kiểm định trước)"),
    ]
    lines = ["\\begin{tabular}{lp{6.2cm}p{6.2cm}}", "\\toprule", "Mã & Dự báo & Kết quả \\\\", "\\midrule"]
    lines += [f"{a} & {b} & {c} \\\\" for a, b, c in rows_vi]
    lines += ["\\bottomrule", "\\end{tabular}"]
    (TAB / "appendix_prereg_vi.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("h1b arms meeting rule:", h1b_arms, "h2c:", h2c, "monotone:", monotone, "spread:", round(spread, 2))
    print(len(macros), "macros")


if __name__ == "__main__":
    main()
