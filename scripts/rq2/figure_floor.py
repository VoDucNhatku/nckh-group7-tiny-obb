"""Figure 1 of the paper: how a candidate floor turns a starved tiny box into one with candidates.

Uses geometry.candidates_one, the same candidate test as the label-only analysis (checked against Ultralytics 8.4.174
by test_geometry.py), on one synthetic very tiny box. Writes paper/figs/floor_example.pdf (and .png with --png).

    python scripts/rq2/figure_floor.py [--png]
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Polygon  # noqa: E402

import geometry as g  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
BOX = (15.5, 17.5, 6.0, 3.0, math.radians(30))  # cx, cy, w, h, theta: a 6 x 3 px very tiny box with no candidate under A0
VIEW = (0, 32)
PANELS = (("A0", "no floor"), ("A8", "floor $8\\sqrt{2}$ px"), ("A2", "floor 16 px (library)"))
STYLE = {0: dict(marker="o", s=14, label="stride-8 anchor"), 1: dict(marker="s", s=34, label="stride-16 anchor"),
         2: dict(marker="D", s=50, label="stride-32 anchor")}


def anchors_in_view():
    pts = []
    for li, s in enumerate(g.STRIDES):
        c = (np.arange(0, 800 // s) + 0.5) * s
        c = c[(c >= VIEW[0]) & (c <= VIEW[1])]
        for x in c:
            for y in c:
                pts.append((li, x, y))
    return pts


def main(png: bool):
    cx, cy, w, h, t = BOX
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.6), sharey=True)
    all_pts = anchors_in_view()
    for ax, (arm, title) in zip(axes, PANELS):
        a = g.ARMS[arm]
        fw, fh = g.floor_sides(np.array([w, h]), a)
        ids = g.candidates_one(BOX, a)
        chosen = {(int(i // 10_000_000), *map(float, xy)) for i, xy in zip(ids, g.anchor_xy(ids))}
        for li, st in STYLE.items():
            xs = [(x, y) for l, x, y in all_pts if l == li]
            if not xs:
                continue
            on = [(x, y) for x, y in xs if (li, x, y) in chosen]
            off = [(x, y) for x, y in xs if (li, x, y) not in chosen]
            if off:
                ax.scatter(*zip(*off), facecolors="none", edgecolors="#9a9a9a", linewidths=0.8, marker=st["marker"], s=st["s"])
            if on:
                ax.scatter(*zip(*on), color="#c55a11", marker=st["marker"], s=st["s"], zorder=3)
        if arm != "A0":
            ax.add_patch(Polygon(np.array(g.corners(cx, cy, fw, fh, t)), closed=True, fill=False, ls="--", ec="#1f4e79", lw=1.0))
        ax.add_patch(Polygon(np.array(g.corners(cx, cy, w, h, t)), closed=True, fc="#1f4e79", alpha=0.85, ec="none"))
        ax.set_title(f"{arm}: {title}\n{len(ids)} candidate{'s' if len(ids) != 1 else ''}", fontsize=8)
        ax.set_xlim(*VIEW), ax.set_ylim(*VIEW)
        ax.set_aspect("equal")
        ax.invert_yaxis()
        ax.set_xticks([0, 8, 16, 24, 32]), ax.set_yticks([0, 8, 16, 24, 32])
        ax.tick_params(labelsize=7)
        ax.set_xlabel("x (px)", fontsize=7)
    axes[0].set_ylabel("y (px)", fontsize=7)
    handles = [plt.Line2D([], [], ls="none", marker=STYLE[i]["marker"], mfc="none", mec="#9a9a9a", label=STYLE[i]["label"])
               for i in (0, 1, 2)]
    handles += [plt.Line2D([], [], ls="none", marker="o", color="#c55a11", label="candidate"),
                plt.Line2D([], [], ls="--", color="#1f4e79", label="floored region")]
    fig.legend(handles=handles, loc="lower center", ncol=5, fontsize=7, frameon=False, bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    out = ROOT / "paper" / "figs" / "floor_example.pdf"
    fig.savefig(out)
    if png:
        fig.savefig(out.with_suffix(".png"), dpi=200)
    counts = {arm: len(g.candidates_one(BOX, g.ARMS[arm])) for arm, _ in PANELS}
    print("candidates per arm:", counts)
    return counts


if __name__ == "__main__":
    main("--png" in sys.argv)
