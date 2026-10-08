"""Figures for the C-3 v2 proposal (school template version).
Fig 1: research framework. Fig 2: candidate regions of four rules for one 4x12 px rotated box (anchor
counts computed geometrically for one placement; expected counts follow Proposition 1 of the proposal).
Output: notes/figs/fig1_framework.png, notes/figs/fig2_regions.png"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon
from common import ROOT

OUT = ROOT / "notes" / "figs"
OUT.mkdir(exist_ok=True)
plt.rcParams["font.family"] = "Times New Roman"
NAVY, ACC, GREY, GREEN = "#1A2B47", "#C8553D", "#E9EDF3", "#4F7A3A"

# ---------------- Figure 1: framework ----------------
fig, ax = plt.subplots(figsize=(11, 6.2))
ax.set_xlim(0, 110)
ax.set_ylim(0, 64)
ax.axis("off")


def box(x, y, w, h, text, fc=GREY, ec=NAVY, fs=9, bold=False, tc="#111"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.0", fc=fc, ec=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc, weight="bold" if bold else "normal")


def arrow(x1, y1, x2, y2, c=NAVY, ls="-"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color=c, lw=1.3, ls=ls))


box(1, 47, 18, 11, "AI-TOD-R\nlabels + images\n(xView route)", bold=True)
box(1, 30, 18, 11, "Data preparation\nfixed validation split\nDOTA-format labels")
box(1, 13, 18, 11, "Second dataset (RQ4)\nSODA-A, or\nDOTA-v2.0 train→val")
arrow(10, 47, 10, 41.4)
ax.add_patch(FancyBboxPatch((24, 20), 50, 41, boxstyle="round,pad=0.4,rounding_size=1.4", fc="white", ec=NAVY, lw=1.6))
ax.text(49, 58.6, "Training: YOLO11 / YOLO26-OBB\n(one pinned Ultralytics fork, COCO initialisation)", ha="center", va="center",
        fontsize=9.3, weight="bold", color=NAVY)
box(26, 43, 13, 9, "Backbone\n+ Neck")
box(42, 43, 14, 9, "OBB head\n(class, box,\nangle)")
box(59, 43, 13, 9, "Loss\n(class, rotated\nbox, angle)")
arrow(39.4, 47.5, 41.6, 47.5)
arrow(56.4, 47.5, 58.6, 47.5)
ax.add_patch(FancyBboxPatch((26, 22), 46, 17, boxstyle="round,pad=0.3,rounding_size=1.0", fc="#FBEAE5", ec=ACC, lw=1.6))
ax.text(49, 36.6, "Label assigner — the part this project studies", ha="center", fontsize=9.3, weight="bold", color=ACC)
box(27.5, 23.5, 21, 10.5, "(1) Candidate-region rule\nTAL · STAL-8 · STAL-16\nOA-STAL v2 (ours)", fc="white", ec=ACC, fs=8.8)
box(50.5, 23.5, 20, 10.5, "(2) Conflict rule\ndefault (max ProbIoU)\ninside-box · smaller-GT", fc="white", ec=ACC, fs=8.8)
arrow(49, 39.4, 49, 42.6, c=ACC)
arrow(65, 39.4, 65, 42.6, c=ACC)
arrow(19.4, 35.5, 23.6, 35.5)
arrow(19.4, 18.5, 23.6, 24, c="#8a96a8")
box(80, 47, 28, 11, "Inference (unchanged cost)\npredictions, max_det ≥ 1500")
box(80, 30, 28, 11, "Official evaluator AITODReval\nAP, AP50, AP75, APvt, APt, APs, APm\nper class + measured latency", fs=8.6)
box(80, 9, 28, 15, "Statistics\n3 seeds, paired bootstrap CI\nRQ1 benchmark\nRQ3 intervention · RQ4 transfer", fs=8.8)
arrow(74.4, 52.5, 79.6, 52.5)
arrow(94, 47, 94, 41.4)
arrow(94, 30, 94, 24.4)
box(24, 2, 50, 12, "RQ2 diagnosis\noffline label geometry: candidates, zero-candidate rate,\nconflicts, neighbour layout"
    " + online logging (both YOLO26 branches)\npredictions pre-registered BEFORE the RQ3 runs",
    fc="#EEF3E8", ec=GREEN, fs=8.6)
ax.plot([19.4, 21.6, 21.6], [32, 32, 6], color=GREEN, lw=1.3, ls="--")
arrow(21.6, 6, 23.6, 6, c=GREEN, ls="--")
arrow(49, 14.4, 49, 19.6, c=GREEN, ls="--")
plt.savefig(OUT / "fig1_framework.png", dpi=220, bbox_inches="tight")
plt.close()

# ---------------- Figure 2: candidate regions (computed) ----------------


def rect(cx, cy, w, h, th):
    c, s = np.cos(th), np.sin(th)
    pts = np.array([[-w / 2, -h / 2], [w / 2, -h / 2], [w / 2, h / 2], [-w / 2, h / 2]])
    return pts @ np.array([[c, s], [-s, c]]) + [cx, cy]


def inside(px, py, cx, cy, w, h, th):
    c, s = np.cos(th), np.sin(th)
    dx, dy = px - cx, py - cy
    u, v = dx * c + dy * s, -dx * s + dy * c
    return (np.abs(u) <= w / 2) & (np.abs(v) <= h / 2)


w, h, th, cx, cy = 12.0, 4.0, np.deg2rad(30), 21.0, 19.0
k = 16 / np.sqrt(w * h)
rules = [("TAL (no floor)", w, h),
         ("STAL-8 (published rule)\nsides < 8 px → 16 px", w, 16.0),
         ("STAL-16 (current code)\nsides < 16 px → 16 px", 16.0, 16.0),
         ("OA-STAL v2 (ours)\nsame area as STAL-16, same shape", min(k * w, max(w, 32)), max(k * h, 8, h))]
fig, axs = plt.subplots(1, 4, figsize=(12, 3.3))
grid = {s: np.array([[(i + .5) * s, (j + .5) * s] for i in range(0, 48 // s + 1) for j in range(0, 40 // s + 1)])
        for s in (8, 16, 32)}
for ax, (name, rw, rh) in zip(axs, rules):
    ax.set_xlim(4, 38)
    ax.set_ylim(6, 32)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.add_patch(Polygon(rect(cx, cy, rw, rh, th), closed=True, fc="#FBEAE5", ec=ACC, lw=1.6))
    ax.add_patch(Polygon(rect(cx, cy, w, h, th), closed=True, fc=NAVY, ec=NAVY, lw=1, alpha=.85))
    n = 0
    for s, mk, sz in ((8, "o", 16), (16, "s", 32), (32, "D", 42)):
        P = grid[s]
        m = inside(P[:, 0], P[:, 1], cx, cy, rw, rh, th)
        n += int(m.sum())
        ax.scatter(P[~m, 0], P[~m, 1], s=sz * .5, marker=mk, c="#B8C0CC")
        ax.scatter(P[m, 0], P[m, 1], s=sz, marker=mk, c="#2E7D32", edgecolors="k", linewidths=.4)
    ax.set_title(f"{name}\nregion {rw:.1f} × {rh:.1f} px · candidates here: {n}", fontsize=9)
plt.tight_layout()
plt.savefig(OUT / "fig2_regions.png", dpi=220, bbox_inches="tight")
plt.close()
print("saved", OUT, "k =", round(k, 3))
