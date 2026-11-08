"""Build the result tables, macros and figure of the paper from the merged result files (no hand-typed numbers).

Inputs (all in the repo):
- experiments/2026-11-07-c11x-seeds1to5/: results_long.csv, p1_verdict.json, r0_check.json, m1_by_seed_group.json,
  mechanism/fate_by_arm_bin*_e2e_score*.csv, mechanism/recall_iou_by_arm_bin_e2e_score*.csv
- experiments/2026-11-06-c11x-explore-val/decision.json

Outputs: paper/tables/results_*.tex, paper/figs/recall_iou.pdf.

Seeds 1-3 and 4-5 are kept apart wherever a per-seed value exists, because the R0 check did not match
(annex A2, item 5). The fate and recall-by-IoU tables in mechanism/ are means over seeds 1-5 as written by the
notebook; the per-seed files behind them are on Drive only, so those tables cannot be split here.

    python scripts/c11x/export_results.py
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "experiments" / "2026-11-07-c11x-seeds1to5"
VAL = ROOT / "experiments" / "2026-11-06-c11x-explore-val" / "decision.json"
TAB = ROOT / "paper" / "tables"
FIG = ROOT / "paper" / "figs"
FATES = ("detected", "lost_to_neighbour", "cls", "loc", "both", "miss")
FATE_TEX = {"detected": "detected", "lost_to_neighbour": "neighbour", "cls": "class", "loc": "localisation",
            "both": "both", "miss": "missed"}
BINS = (("vt", "very tiny"), ("t", "tiny"), ("s", "small"))


def num(x: float, d: int = 4, sign: bool = True) -> str:
    s = f"{x:+.{d}f}" if sign else f"{x:.{d}f}"
    return s.replace("-", "$-$")


def pct(x: float, d: int = 1) -> str:
    return f"{100 * x:.{d}f}"


def read_multi(path: Path) -> pd.DataFrame:
    """CSV written by pandas from a frame with two-level columns and a multi-index."""
    head = pd.read_csv(path, nrows=2, header=None)
    n_idx = int(head.iloc[0].isna().sum()) if pd.isna(head.iloc[0, 0]) else 0
    df = pd.read_csv(path, header=[0, 1], index_col=list(range(max(n_idx, 1))))
    df.index.names = [str(n) for n in df.index.names]
    return df


def fate_frame(score: str, by: str = "") -> pd.DataFrame:
    df = pd.read_csv(RUN / "mechanism" / f"fate_by_arm_bin{by}_e2e_score{score}.csv", header=[0, 1], skiprows=[2])
    keys = [c for c in df.columns if c[1].startswith("Unnamed") or c[0] in ("fate",) or c[0].startswith("Unnamed")]
    names = ["arm", "bin"] + ([by.strip("_").split("_")[-1] if by else None] if by else [])
    names = [n for n in names if n]
    out = df[keys].copy()
    out.columns = names
    for f in FATES:
        out[f] = df[(f, "mean")].to_numpy()
    out["n"] = df[("n", "mean")].to_numpy()
    return out


def recall_frame(score: str) -> pd.DataFrame:
    df = pd.read_csv(RUN / "mechanism" / f"recall_iou_by_arm_bin_e2e_score{score}.csv", header=[0, 1], skiprows=[2])
    out = df.iloc[:, :2].copy()
    out.columns = ["arm", "bin"]
    for t in ("0.1", "0.25", "0.5", "0.75"):
        out[t] = df[(f"det_{t}", "mean")].to_numpy()
    return out


def per_seed(res: pd.DataFrame, head: str, metric: str) -> pd.DataFrame:
    d = res[res["head"] == head].pivot_table(index="seed", columns="arm", values=metric)
    d["delta"] = d["A2"] - d["A0"]
    return d


def main():
    res = pd.read_csv(RUN / "results_long.csv")
    p1 = json.loads((RUN / "p1_verdict.json").read_text(encoding="utf-8"))
    r0 = json.loads((RUN / "r0_check.json").read_text(encoding="utf-8"))
    m1 = json.loads((RUN / "m1_by_seed_group.json").read_text(encoding="utf-8"))
    val = json.loads(VAL.read_text(encoding="utf-8"))

    vt = per_seed(res, "e2e", "AP_vt")
    assert abs(vt.loc[4, "delta"] - p1["s4"]) < 1e-5 and abs(vt.loc[5, "delta"] - p1["s5"]) < 1e-5, "P1 file and table differ"
    new, old = [4, 5], [1, 2, 3]
    other = {m: per_seed(res, "e2e", m) for m in ("AP", "AP_t", "AP_s", "AP_m")}
    nms_vt = per_seed(res, "nms", "AP_vt")

    # Table: per-seed AP_vt and deltas, seeds 1-3 apart from 4-5.
    rows = ["\\begin{tabular}{llrrrrrrr}", "\\toprule",
            "Seeds & Seed & AP$_{vt}$ A0 & AP$_{vt}$ A2 & $\\Delta$AP$_{vt}$ & $\\Delta$AP$_t$ & $\\Delta$AP$_s$ & $\\Delta$AP$_m$ & $\\Delta$AP \\\\",
            "\\midrule"]
    for label, seeds in (("1--3, exploratory", old), ("4--5, new", new)):
        for i, s in enumerate(seeds):
            cells = [label if i == 0 else "", str(s), num(vt.loc[s, "A0"], sign=False), num(vt.loc[s, "A2"], sign=False),
                     num(vt.loc[s, "delta"])] + [num(other[m].loc[s, "delta"]) for m in ("AP_t", "AP_s", "AP_m", "AP")]
            rows.append(" & ".join(cells) + " \\\\")
        mean = [num(vt.loc[seeds, "delta"].mean())] + [num(other[m].loc[seeds, "delta"].mean()) for m in ("AP_t", "AP_s", "AP_m", "AP")]
        rows.append(" & mean & & & " + " & ".join(mean) + " \\\\")
        rows.append("\\midrule" if seeds == old else "\\bottomrule")
    rows.append("\\end{tabular}")
    (TAB / "results_p1.tex").write_text("\n".join(rows) + "\n", encoding="utf-8")

    # Table: M1 by seed group.
    rows = ["\\begin{tabular}{llrcc}", "\\toprule",
            "Score & Seeds & DiD & Scene 95\\% CI & Scene + seed 95\\% CI \\\\", "\\midrule"]
    for key, score in (("e2e_score0.25", "$\\geq 0.25$"), ("e2e_score0.05", "$\\geq 0.05$")):
        for g in ("1-3", "4-5"):
            r = m1[key][g]
            rows.append(f"{score if g == '1-3' else ''} & {g.replace('-', '--')} & {num(r['delta'], 3)} & "
                        f"[{num(r['scene_ci'][0], 3)}, {num(r['scene_ci'][1], 3)}] & "
                        f"[{num(r['combined_ci'][0], 3)}, {num(r['combined_ci'][1], 3)}] \\\\")
    rows += ["\\bottomrule", "\\end{tabular}"]
    (TAB / "results_m1.tex").write_text("\n".join(rows) + "\n", encoding="utf-8")

    # Table: fate of boxes, very tiny and tiny, both scores.
    rows = ["\\begin{tabular}{lll" + "r" * len(FATES) + "}", "\\toprule",
            "Score & Size & Arm & " + " & ".join(FATE_TEX[f] for f in FATES) + " \\\\", "\\midrule"]
    for score in ("0.25", "0.05"):
        fr = fate_frame(score)
        for b, bname in BINS[:2]:
            for a in ("A0", "A2"):
                r = fr[(fr.arm == a) & (fr.bin == b)].iloc[0]
                first = f"$\\geq {score}$" if (b == "vt" and a == "A0") else ""
                rows.append(f"{first} & {bname if a == 'A0' else ''} & {a} & " + " & ".join(pct(r[f]) for f in FATES) + " \\\\")
        rows.append("\\midrule" if score == "0.25" else "\\bottomrule")
    rows.append("\\end{tabular}")
    (TAB / "results_fates.tex").write_text("\n".join(rows) + "\n", encoding="utf-8")

    # Figure: recall against IoU threshold, score >= 0.05.
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rc05, rc25 = recall_frame("0.05"), recall_frame("0.25")
    ious = [0.1, 0.25, 0.5, 0.75]
    fig, ax = plt.subplots(figsize=(4.2, 3.0))
    for (b, bname), color in zip(BINS, ("#1f4e79", "#c55a11", "#548235")):
        for a, ls in (("A0", "--"), ("A2", "-")):
            r = rc05[(rc05.arm == a) & (rc05.bin == b)].iloc[0]
            ax.plot(ious, [r[str(t)] for t in ious], ls, color=color, marker="o", ms=3, label=f"{bname}, {a}")
    ax.set_xlabel("IoU threshold")
    ax.set_ylabel("recall (score $\\geq$ 0.05)")
    ax.set_xticks(ious)
    ax.legend(fontsize=6, ncol=2, frameon=False)
    fig.tight_layout()
    FIG.mkdir(exist_ok=True)
    fig.savefig(FIG / "recall_iou.pdf")

    # Macros used in the text.
    f25, f05 = fate_frame("0.25"), fate_frame("0.05")
    st25 = fate_frame("0.25", "_starved")

    def fate(fr, a, b, f):
        return fr[(fr.arm == a) & (fr.bin == b)].iloc[0][f]

    def rec(rc, a, b, t):
        return rc[(rc.arm == a) & (rc.bin == b)].iloc[0][t]

    def starved(a, flag, f="detected"):
        r = st25[(st25.arm == a) & (st25.bin == "vt") & (st25.starved.astype(str) == str(flag))].iloc[0]
        return r[f]

    undet25 = 1 - fate(f25, "A2", "vt", "detected")
    undet05 = 1 - fate(f05, "A2", "vt", "detected")
    macros = {
        "pOneSFour": num(p1["s4"]), "pOneSFive": num(p1["s5"]), "pOneMean": num(p1["mean_s4_s5"]),
        "pOneAzeroSFour": num(vt.loc[4, "A0"], sign=False), "pOneAtwoSFour": num(vt.loc[4, "A2"], sign=False),
        "pOneOldMin": num(vt.loc[old, "delta"].min()), "pOneOldMax": num(vt.loc[old, "delta"].max()),
        "pOneNmsSFour": num(nms_vt.loc[4, "delta"]), "pOneNmsSFive": num(nms_vt.loc[5, "delta"]),
        "apNewMean": num(other["AP"].loc[new, "delta"].mean()),
        "apsNewMean": num(other["AP_s"].loc[new, "delta"].mean()), "apmNewMean": num(other["AP_m"].loc[new, "delta"].mean()),
        "apsOldMean": num(other["AP_s"].loc[old, "delta"].mean()), "apmOldMean": num(other["AP_m"].loc[old, "delta"].mean()),
        "rzeroDap": num(r0["d_ap"]), "rzeroDval": num(r0["d_val_ep24"], 3),
        "valCOne": num(val["C1_rescue"]["mean"], 3), "valCOneN": str(val["C1_rescue"]["n_gt"]),
        "valLocShare": pct(val["C2_reason"]["shares"]["loc"]), "valMissShare": pct(val["C2_reason"]["shares"]["miss"]),
        "mOneOld": num(m1["e2e_score0.25"]["1-3"]["delta"], 3), "mOneNew": num(m1["e2e_score0.25"]["4-5"]["delta"], 3),
        "mOneOldLow": num(m1["e2e_score0.05"]["1-3"]["delta"], 3), "mOneNewLow": num(m1["e2e_score0.05"]["4-5"]["delta"], 3),
        "mOneSeedMin": num(min(m1["e2e_score0.25"]["1-5"]["per_seed"].values()), 3),
        "mOneSeedMax": num(max(m1["e2e_score0.25"]["1-5"]["per_seed"].values()), 3),
        "vtDetAzero": pct(fate(f25, "A0", "vt", "detected")), "vtDetAtwo": pct(fate(f25, "A2", "vt", "detected")),
        "vtMissAzero": pct(fate(f25, "A0", "vt", "miss")), "vtMissAtwo": pct(fate(f25, "A2", "vt", "miss")),
        "vtLocAzero": pct(fate(f25, "A0", "vt", "loc")), "vtLocAtwo": pct(fate(f25, "A2", "vt", "loc")),
        "vtMissShareUndet": pct(fate(f25, "A2", "vt", "miss") / undet25),
        "vtLocShareUndetLow": pct(fate(f05, "A2", "vt", "loc") / undet05),
        "vtMissShareUndetLow": pct(fate(f05, "A2", "vt", "miss") / undet05),
        "vtDetAtwoLow": pct(fate(f05, "A2", "vt", "detected")), "vtLocAtwoLow": pct(fate(f05, "A2", "vt", "loc")),
        "vtMissAtwoLow": pct(fate(f05, "A2", "vt", "miss")),
        "starvedAzero": pct(starved("A0", True)), "starvedAtwo": pct(starved("A2", True)),
        "fedAzero": pct(starved("A0", False)), "fedAtwo": pct(starved("A2", False)),
        "recVtOne": pct(rec(rc05, "A2", "vt", "0.1")), "recVtHalf": pct(rec(rc05, "A2", "vt", "0.5")),
        "recVtThreeQ": pct(rec(rc05, "A2", "vt", "0.75")),
        "dropVt": pct(rec(rc25, "A2", "vt", "0.25") - rec(rc25, "A2", "vt", "0.5")),
        "dropT": pct(rec(rc25, "A2", "t", "0.25") - rec(rc25, "A2", "t", "0.5")),
        "recVtHalfAzeroHigh": pct(rec(rc25, "A0", "vt", "0.5")), "recVtHalfAtwoHigh": pct(rec(rc25, "A2", "vt", "0.5")),
    }
    (TAB / "results_macros.tex").write_text("".join(f"\\newcommand{{\\{k}}}{{{v}}}\n" for k, v in macros.items()),
                                          encoding="utf-8")
    print(f"{len(macros)} macros; P1 seeds 4, 5: {macros['pOneSFour']}, {macros['pOneSFive']}")


if __name__ == "__main__":
    main()
