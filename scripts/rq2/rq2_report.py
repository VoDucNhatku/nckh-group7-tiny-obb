"""Build the RQ2 figure and LaTeX tables of the paper from rq2_summary.json (no hand-typed numbers).

Usage: python rq2_report.py --summary <dir>/rq2_summary.json --paper ../../paper
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ARMS = ("A0", "A1", "A8", "A2")
BINS = (("vt", "very tiny ($<$8 px)"), ("t", "tiny (8--16 px)"), ("s", "small (16--32 px)"))
DENS = (("isolated", "isolated"), ("1-2", "1--2"), (">=3", "$\\geq$3"))


def pct(x: float) -> str:
    return f"{100 * x:.1f}"


def stage_table(s: dict) -> str:
    rows = []
    for b, name in BINS:
        t = s["by_size"][b]
        n = t["A0"]["n"]
        rows.append(f"\\multicolumn{{5}}{{l}}{{\\textit{{{name}}}, $n={n:,}$}} \\\\".replace(",", "{,}"))
        for key, label in (
            ("mean_cand", "candidates / GT"),
            ("zero_cand", "zero candidates (\\%)"),
            ("shared_frac", "shared candidates (\\%)"),
            ("zero_pos_o2m_proxy", "zero positives, proxy (\\%)"),
        ):
            vals = [t[a][key] for a in ARMS]
            cells = [f"{v:.2f}" if key == "mean_cand" else pct(v) for v in vals]
            rows.append(f"\\quad {label} & " + " & ".join(cells) + " \\\\")
    body = "\n".join(rows)
    return (
        "\\begin{tabular}{lrrrr}\n\\toprule\n & A0 & A1 & A8 & A2 \\\\\n\\midrule\n"
        + body
        + "\n\\bottomrule\n\\end{tabular}\n"
    )


def density_table(s: dict) -> str:
    rows = []
    for b, name in BINS[:2]:
        for d, dn in DENS:
            t = s["by_size_density"][f"{b}|{d}"]
            cells = [pct(t[a]["zero_pos_o2m_proxy"]) for a in ARMS]
            rows.append(f"{ {'vt': 'very tiny', 't': 'tiny'}[b]} & {dn} & {t['A0']['n']:,} & ".replace(",", "{,}") + " & ".join(cells) + " \\\\")
    return (
        "\\begin{tabular}{llrrrrr}\n\\toprule\nsize & neighbours & $n$ & A0 & A1 & A8 & A2 \\\\\n\\midrule\n"
        + "\n".join(rows)
        + "\n\\bottomrule\n\\end{tabular}\n"
    )


def figure(s: dict, out: Path):
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.4))
    x = range(len(ARMS))
    for ax, (b, name) in zip(axes, BINS[:2]):
        t = s["by_size"][b]
        zc = [100 * t[a]["zero_cand"] for a in ARMS]
        lc = [100 * t[a]["lost_at_conflict_o2m_proxy"] for a in ARMS]
        ax.bar(x, zc, color="#4c72b0", label="no candidate")
        ax.bar(x, lc, bottom=zc, color="#dd8452", label="lost at conflict (proxy)")
        ax.set_xticks(list(x), ARMS)
        ax.set_title(name.replace("$<$", "<").replace("--", "–"), fontsize=9)
        ax.set_ylabel("GT without positive (%)", fontsize=8)
        ax.tick_params(labelsize=8)
    axes[0].legend(fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", required=True, type=Path)
    ap.add_argument("--paper", required=True, type=Path)
    a = ap.parse_args()
    s = json.loads(a.summary.read_text())
    (a.paper / "tables").mkdir(parents=True, exist_ok=True)
    (a.paper / "figs").mkdir(parents=True, exist_ok=True)
    (a.paper / "tables" / "rq2_stages.tex").write_text(stage_table(s))
    (a.paper / "tables" / "rq2_density.tex").write_text(density_table(s))
    figure(s, a.paper / "figs" / "rq2_stages.pdf")
    tr = s["transitions_vs_A0_o2m_proxy"]
    macros = [f"\\newcommand{{\\rqNgt}}{{{s['n_gt']:,}}}".replace(",", "{,}")]
    for arm, v in tr.items():
        tag = {"A1": "One", "A8": "Eight", "A2": "Two"}[arm]
        macros.append(f"\\newcommand{{\\rqRescued{tag}}}{{{v['rescued']:,}}}".replace(",", "{,}"))
        macros.append(f"\\newcommand{{\\rqStarved{tag}}}{{{v['newly_starved']:,}}}".replace(",", "{,}"))
    vt = s["by_size"]["vt"]
    macros.append(f"\\newcommand{{\\rqZeroCandVtA}}{{{pct(vt['A0']['zero_cand'])}}}")
    (a.paper / "tables" / "rq2_macros.tex").write_text("\n".join(macros) + "\n")
    print("wrote", a.paper / "tables", a.paper / "figs")


if __name__ == "__main__":
    main()
