"""Copy the exploratory results printed in notebooks/C11x_analysis_colab.ipynb to files, and build the paper table.

The CSV and JSON files of that run live on the team Drive. Until they are copied here, this script reads the same
values from the saved notebook output (cells "CỔNG H2" and "CI gộp"), so the paper has no hand-typed numbers.

    python scripts/c11x/export_explor.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NB = ROOT / "notebooks" / "C11x_analysis_colab.ipynb"
OUT = ROOT / "experiments" / "2026-10-30-c11x-analysis"
TEX = ROOT / "paper" / "tables" / "c11x_explor.tex"
COLS = ("head", "pair", "metric", "delta", "scene_lo", "scene_hi", "skew", "seed_t_lo", "seed_t_hi", "seed_min",
        "seed_max", "comb_lo", "comb_hi", "comb_excl0")
METRICS = (("AP_vt", "AP$_{vt}$"), ("AP_t", "AP$_{t}$"), ("AP_s", "AP$_{s}$"), ("AP_m", "AP$_{m}$"), ("AP", "AP"))
PAIRS = (("A1-A0", "A1$-$A0"), ("A8-A0", "A8$-$A0"), ("A2-A0", "A2$-$A0"), ("A2-A8", "A2$-$A8"))


def notebook_text() -> str:
    nb = json.loads(NB.read_text(encoding="utf-8"))
    for cell in nb["cells"]:
        for o in cell.get("outputs", []):
            text = "".join(o.get("text", []))
            if "=== CỔNG H2 ===" in text and "CI gộp" in text:
                return text
    raise SystemExit("summary cell not found in the notebook")


def parse_gate(text: str) -> dict:
    block = text.split("=== CỔNG H2 ===", 1)[1].split("số parquet", 1)[0]
    return json.loads(block)


def parse_ci(text: str) -> list[dict]:
    block = text.split("=== CI gộp", 1)[1]
    block = block.split("=== R0", 1)[0]
    rows = []
    for line in block.splitlines():
        p = line.split()
        if len(p) == len(COLS) and p[0] in ("e2e", "nms"):
            rows.append(dict(zip(COLS, p)))
    return rows


def fmt(x: str) -> str:
    return f"{float(x):+.4f}".replace("-", "$-$")


def table(rows: list[dict]) -> str:
    idx = {(r["head"], r["pair"], r["metric"]): r for r in rows}
    out = ["\\begin{tabular}{llrcc}", "\\toprule",
           "Head & Pair and metric & $\\Delta$ & Scene 95\\% CI & Scene + seed 95\\% CI \\\\", "\\midrule"]
    for head in ("e2e", "nms"):
        for pair, pair_tex in PAIRS:
            for metric, metric_tex in METRICS:
                r = idx[(head, pair, metric)]
                out.append(f"{head} & {pair_tex}, {metric_tex} & {fmt(r['delta'])} & "
                           f"[{fmt(r['scene_lo'])}, {fmt(r['scene_hi'])}] & [{fmt(r['comb_lo'])}, {fmt(r['comb_hi'])}] \\\\")
        if head == "e2e":
            out.append("\\midrule")
    out += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(out) + "\n"


def pct(x: float) -> str:
    return f"{100 * x:.1f}\\%"


def signed(x: float, digits: int = 4) -> str:
    return f"{x:+.{digits}f}".replace("-", "$-$")


def macros(rows: list[dict], gate: dict) -> str:
    r = next(x for x in rows if (x["head"], x["pair"], x["metric"]) == ("e2e", "A2-A0", "AP_vt"))
    by_pos = gate["recall_lt8_by_npos"]
    vals = {
        "dAvtAtwo": signed(float(r["delta"])),
        "dAvtAtwoSceneLo": signed(float(r["scene_lo"])),
        "dAvtAtwoSceneHi": signed(float(r["scene_hi"])),
        "dAvtAtwoCombLo": signed(float(r["comb_lo"])),
        "dAvtAtwoCombHi": signed(float(r["comb_hi"])),
        "nCombExcl": str(sum(x["comb_excl0"] == "True" for x in rows)),
        "gateCoef": signed(gate["coef"], 2),
        "gateLo": signed(gate["ci_lo"], 2),
        "gateHi": signed(gate["ci_hi"], 2),
        "recallZero": pct(by_pos["0"][0]),
        "recallOne": pct(by_pos["1"][0]),
        "recallFive": pct(by_pos["5-9"][0]),
    }
    return "".join(f"\\newcommand{{\\{k}}}{{{v}}}\n" for k, v in vals.items())


def main():
    text = notebook_text()
    gate, rows = parse_gate(text), parse_ci(text)
    if len(rows) != 40:
        raise SystemExit(f"expected 40 rows (2 heads x 4 pairs x 5 metrics), got {len(rows)}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "c11x-h2-gate.json").write_text(json.dumps(gate, indent=2) + "\n", encoding="utf-8")
    lines = [",".join(COLS)] + [",".join(r[c] for c in COLS) for r in rows]
    (OUT / "ci_scene_seed.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    TEX.write_text(table(rows), encoding="utf-8")
    TEX.with_name("c11x_macros.tex").write_text(macros(rows, gate), encoding="utf-8")
    n_excl = sum(r["comb_excl0"] == "True" for r in rows)
    print(f"{len(rows)} rows; {n_excl} combined intervals exclude 0; gate go={gate['go']}")


if __name__ == "__main__":
    main()
