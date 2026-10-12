"""lab_bridge.py - every number and figure in "Kien thuc DPL302m qua de tai Nhom 7" comes from here.

Run:  python lab_bridge.py > lab_output.txt

Nothing here runs Ultralytics (not installed). Formulas are RE-IMPLEMENTED in numpy/torch from
the official source of ultralytics v8.4.174 (read 2026-10-12/13):
  https://raw.githubusercontent.com/ultralytics/ultralytics/v8.4.174/ultralytics/utils/loss.py
  https://raw.githubusercontent.com/ultralytics/ultralytics/v8.4.174/ultralytics/utils/tal.py
  https://raw.githubusercontent.com/ultralytics/ultralytics/v8.4.174/ultralytics/utils/metrics.py
  (+ engine/trainer.py, utils/torch_utils.py, data/augment.py, utils/ops.py of the same tag)
Project facts (dataset counts, proposal numbers) are copied from
  NCKH/notes/t07-dl-digest-2026-10-11.md and NCKH/notes/t07-c3-proposal-v2-EN.md.
Anything labelled SIMULATED uses synthetic data and is NOT a project result.

Sections: A data (ch.2) | B CNN (ch.3) | C loss (ch.4) | D assignment (ch.5)
          E training run (ch.6) | F evaluation (ch.7)
"""
import math
import os
import time

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import torch  # noqa: E402
import torch.nn.functional as F  # noqa: E402
from matplotlib.patches import Polygon, Rectangle  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figures")
os.makedirs(FIG, exist_ok=True)
NAVY, TEAL, RUST, GREY, AMBER = "#12355b", "#0a7f7a", "#a8341a", "#8a93a2", "#a86400"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9.5, "axes.titlesize": 10,
    "axes.labelsize": 9.5, "legend.fontsize": 8.5, "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5, "axes.spines.top": False, "axes.spines.right": False,
})
np.set_printoptions(precision=4, suppress=True, linewidth=110)
torch.set_printoptions(precision=4, sci_mode=False)
T0 = time.time()


def save(fig, name):
    fig.savefig(os.path.join(FIG, name), dpi=170, bbox_inches="tight")
    plt.close(fig)


def header(tag, title):
    print("\n" + "=" * 78 + f"\n[{tag}] {title}\n" + "=" * 78)


# ============================================================================
# Shared geometry (re-implemented from ultralytics v8.4.174)
# ============================================================================
def corners(x, y, w, h, t):
    """xywhr -> 4 corners, same order as ops.xywhr2xyxyxyxy (pt1..pt4)."""
    c, s = math.cos(t), math.sin(t)
    v1 = np.array([w / 2 * c, w / 2 * s])
    v2 = np.array([-h / 2 * s, h / 2 * c])
    ctr = np.array([x, y])
    return np.array([ctr + v1 + v2, ctr + v1 - v2, ctr - v1 - v2, ctr - v1 + v2])


def poly_area(P):
    x, y = P[:, 0], P[:, 1]
    return 0.5 * (np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


def ccw(P):
    return P if poly_area(P) > 0 else P[::-1]


def clip_poly(subj, clipper):
    """Sutherland-Hodgman clipping of convex polygons (both CCW)."""
    out = list(subj)
    n = len(clipper)
    for i in range(n):
        a, b = clipper[i], clipper[(i + 1) % n]
        inp, out = out, []
        if not inp:
            break

        def inside(p):
            return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) >= -1e-12

        def inter(p, q):
            d1, d2 = q - p, b - a
            den = d1[0] * d2[1] - d1[1] * d2[0]
            tt = ((a[0] - p[0]) * d2[1] - (a[1] - p[1]) * d2[0]) / den
            return p + tt * d1

        s = inp[-1]
        for e in inp:
            if inside(e):
                if not inside(s):
                    out.append(inter(s, e))
                out.append(e)
            elif inside(s):
                out.append(inter(s, e))
            s = e
    return np.array(out)


def poly_iou(b1, b2):
    """Polygon IoU of two rotated boxes (what mmcv box_iou_rotated / AITODReval measures)."""
    P, Q = ccw(corners(*b1)), ccw(corners(*b2))
    I = clip_poly(P, Q)
    inter = abs(poly_area(I)) if len(I) >= 3 else 0.0
    return inter / (abs(poly_area(P)) + abs(poly_area(Q)) - inter)


def cov_t(b, floor=0.0):
    """metrics._get_covariance_matrix: (a, b, c) with w^2/12 + floor."""
    a = b[..., 2:3].pow(2) / 12 + floor
    bb = b[..., 3:4].pow(2) / 12 + floor
    c = b[..., 4:5]
    cos, sin = c.cos(), c.sin()
    return a * cos**2 + bb * sin**2, a * sin**2 + bb * cos**2, (a - bb) * cos * sin


def probiou_t(o1, o2, eps=1e-7, floor=0.0):
    """metrics.probiou (CIoU=False) re-implemented line by line."""
    x1, y1 = o1[..., 0:1], o1[..., 1:2]
    x2, y2 = o2[..., 0:1], o2[..., 1:2]
    a1, b1, c1 = cov_t(o1, floor)
    a2, b2, c2 = cov_t(o2, floor)
    den = (a1 + a2) * (b1 + b2) - (c1 + c2).pow(2) + eps
    t1 = (((a1 + a2) * (y1 - y2).pow(2) + (b1 + b2) * (x1 - x2).pow(2)) / den) * 0.25
    t2 = (((c1 + c2) * (x2 - x1) * (y1 - y2)) / den) * 0.5
    t3 = (((a1 + a2) * (b1 + b2) - (c1 + c2).pow(2))
          / (4 * ((a1 * b1 - c1.pow(2)).clamp(0) * (a2 * b2 - c2.pow(2)).clamp(0)).sqrt() + eps) + eps).log() * 0.5
    bd = (t1 + t2 + t3).clamp(eps, 100.0)
    hd = (1.0 - (-bd).exp() + eps).sqrt()
    return 1 - hd


def probiou(b1, b2, floor=0.0):
    t1 = torch.tensor([b1], dtype=torch.float64)
    t2 = torch.tensor([b2], dtype=torch.float64)
    return float(probiou_t(t1, t2, floor=floor))


def surrogate(w, h, rule):
    """Candidate region (w~, h~) for a long-edge box w >= h. rule = (mode, t, s_ref).
    none: TAL | per_side: STAL-t (side < t -> s_ref) | similarity: OA-STAL v2 (area trigger,
    s_flo=8, cap c=2, PROP 7.1)."""
    mode = rule[0]
    if mode == "none":
        return w, h
    if mode == "per_side":
        t, s_ref = rule[1], rule[2]
        return (s_ref if w < t else w), (s_ref if h < t else h)
    t, s_ref, s_flo, c = 16.0, 16.0, 8.0, 2.0
    if math.sqrt(w * h) >= t:
        return w, h
    k = max(1.0, s_ref / math.sqrt(w * h))
    hn = max(k * h, s_flo, h)
    wn = max(min(k * w, max(w, c * s_ref)), w)
    return wn, hn


RULES = {
    "A0 TAL": ("none",),
    "A1 STAL-8": ("per_side", 8.0, 16.0),
    "A2 STAL-16": ("per_side", 16.0, 16.0),
    "A4 OA-STAL v2": ("similarity",),
    "A8 san phu 11,31": ("per_side", 8 * math.sqrt(2), 8 * math.sqrt(2)),
}


# ============================================================================
# A. Chapter 2 - data, splits
# ============================================================================
header("A1", "AI-TOD-R class counts (digest 2.1) -> imbalance")
classes = ["airplane", "bridge", "storage-tank", "ship", "swimming-pool", "vehicle", "person", "wind-mill"]
counts = np.array([1667, 1541, 13771, 35813, 1617, 662929, 34490, 632])
tot = counts.sum()
print(f"sum of class counts = {tot:,} (digest says 752,460) -> match={tot == 752460}")
for c, n in zip(classes, counts):
    print(f"  {c:14s} {n:8,d}  {100 * n / tot:6.2f}%")
print(f"vehicle / wind-mill ratio = {counts[5] / counts[7]:.0f}x")
print(f"mean objects per image = 752460/28036 = {752460 / 28036:.2f}")
order = np.argsort(counts)
fig, ax = plt.subplots(figsize=(7, 3.0))
ax.barh([classes[i] for i in order], counts[order], color=[RUST if classes[i] == "vehicle" else NAVY for i in order])
ax.set_xscale("log")
for k, i in enumerate(order):
    ax.text(counts[i] * 1.1, k, f"{100 * counts[i] / tot:.2f}%", va="center", fontsize=8.5)
ax.set_xlabel("số hộp OBB (thang log)")
ax.set_title("AI-TOD-R: 8 lớp, vehicle chiếm phần lớn nhãn")
ax.set_xlim(300, 4e6)
save(fig, "ch2_classes.png")

header("A2", "Size bins of AITODReval (area = int(w*h)) and the s_eq vs per-side trap")
bins = {"very tiny": (4, 64), "tiny": (64, 256), "small": (256, 1024), "medium": (1024, 4096)}
for b, (lo, hi) in bins.items():
    print(f"  {b:10s} area [{lo},{hi}]  s_eq in [{math.sqrt(lo):.0f},{math.sqrt(hi):.0f}] px")
for (w, h) in [(25, 4), (12, 4), (10, 10), (4, 4), (60, 5), (3, 1.5)]:
    a = int(w * h)
    bn = [k for k, (lo, hi) in bins.items() if lo <= a <= hi]
    print(f"  box {w}x{h}: area={a}, s_eq={math.sqrt(w * h):.2f} -> bin {bn[0] if bn else 'none(<4 or >4096)'};"
          f" STAL-8 fires={min(w, h) < 8}, STAL-16 fires={min(w, h) < 16}, dropped by loss (<2px)={min(w, h) < 2}")

header("A3", "SIMULATED grouped split: 30 scenes x 4 tiles, 10% dev by scene vs by image")
rng = np.random.default_rng(0)
names = [f"scene{s:02d}_tile{t}" for s in range(30) for t in range(4)]
scene = np.array([int(n[5:7]) for n in names])
perm = rng.permutation(30)
dev_scenes = set(perm[:3].tolist())
dev = np.array([s in dev_scenes for s in scene])
print(f"by scene: train={np.sum(~dev)} dev={np.sum(dev)} scenes split across both = "
      f"{len(set(scene[dev]) & set(scene[~dev]))}")
dev_i = np.zeros(120, bool)
dev_i[rng.permutation(120)[:12]] = True
print(f"by image: train={np.sum(~dev_i)} dev={np.sum(dev_i)} scenes split across both = "
      f"{len(set(scene[dev_i]) & set(scene[~dev_i]))}")

fig, axs = plt.subplots(2, 1, figsize=(7, 2.3))
fig.subplots_adjust(hspace=0.6)
for ax, title, segs in [
    (axs[0], "Config chính thức của AI-TOD-R", [("trainval → train", 0, 50, NAVY), ("test → val (chỉnh tham số) VÀ test (báo số)", 50, 50, RUST)]),
    (axs[1], "Cách dự án dùng", [("train (90% trainval)", 0, 45, NAVY), ("dev 10%", 45, 5, TEAL), ("test: chấm 1 lần/nhánh cuối", 50, 50, GREY)]),
]:
    for lab, x0, wd, col in segs:
        ax.add_patch(Rectangle((x0, 0), wd, 1, color=col, alpha=0.85))
        ax.text(x0 + wd / 2, 0.5, lab, ha="center", va="center", color="white", fontsize=8.5)
    ax.set_xlim(0, 100), ax.set_ylim(0, 1), ax.axis("off"), ax.set_title(title, fontsize=9.5, loc="left")
fig.text(0.5, 0.0, "Độ rộng chỉ minh họa thứ tự; số ảnh mỗi split của AI-TOD-R chưa được nêu [chưa xác minh].",
         ha="center", fontsize=8, color=GREY)
save(fig, "ch2_split.png")

# ============================================================================
# B. Chapter 3 - the model as a CNN
# ============================================================================
header("B1", "Output size formula floor((n+2p-f)/s)+1 for Conv(k=3,s=2,p=k//2) x5")
for n0 in (800, 640):
    n, sizes = n0, []
    for _ in range(5):
        n = (n + 2 * 1 - 3) // 2 + 1
        sizes.append(n)
    print(f"  input {n0}: P1..P5 = {sizes}")
x = torch.zeros(1, 3, 800, 800)
convs = [torch.nn.Conv2d(3 if i == 0 else 4, 4, 3, 2, 1, bias=False) for i in range(5)]
shp = []
with torch.no_grad():
    for cv in convs:
        x = cv(x)
        shp.append(tuple(x.shape[2:]))
print("  torch check (800):", shp)
for img in (800, 640):
    g = [img // s for s in (8, 16, 32)]
    na = sum(k * k for k in g)
    print(f"  img {img}: grids {g} -> anchors {[k * k for k in g]} total {na}")
NA = 13125
print(f"  channels/anchor C=8: YOLO11 4*16+8+1={4 * 16 + 8 + 1}, YOLO26 4+8+1={4 + 8 + 1}")
print(f"  numbers per image: YOLO11 {NA * 73:,}; YOLO26 one branch {NA * 13:,}; slide YOLO 3x3x16 = {3 * 3 * 16}")
print(f"  binary classifiers per image = {NA}*8 = {NA * 8:,}")

header("B2", "Params of one Conv block (conv no bias + BN) vs slide formula")
blk = torch.nn.Sequential(torch.nn.Conv2d(64, 128, 3, 1, 1, bias=False), torch.nn.BatchNorm2d(128))
pc = sum(p.numel() for p in blk[0].parameters())
pb = sum(p.numel() for p in blk[1].parameters())
print(f"  Conv(64->128,3x3,bias=False): {pc:,} ; BN gamma+beta: {pb} ; total learnable {pc + pb:,}")
print(f"  slide formula (f*f*nc+1)*nc' = (3*3*64+1)*128 = {(9 * 64 + 1) * 128:,}")
c_in = c_out = 64
hw = 100 * 100
normal = 9 * c_in * hw * c_out
dws = 9 * hw * c_in + c_in * hw * c_out
print(f"  ILLUSTRATIVE cost at P3 100x100, 64->64 ch: normal {normal:,} mult; dw+pw {dws:,}; ratio {dws / normal:.3f}"
      f" ; slide approx 1/nc'+1/f^2 = {1 / 64 + 1 / 9:.3f}")

header("B3", "Self-attention size: why only at P5")
for name, side in [("P5 (25x25)", 25), ("P4 (50x50)", 50), ("P3 (100x100)", 100)]:
    L = side * side
    print(f"  {name}: positions {L:,}, attention matrix {L * L:,} entries, fp32 {L * L * 4 / 2**20:.1f} MiB per head")
for sz, w in [("n", 0.25), ("s", 0.50)]:
    c1 = int(1024 * w)
    c = int(c1 * 0.5)
    print(f"  YOLO26{sz}-OBB C2PSA: c1={c1}, self.c={c}, num_heads=max(c//64,1)={max(c // 64, 1)}")

header("B4", "Class-bias init ln(5/C/(640/s)^2), C=8 (head.py bias_init)")
for s in (8, 16, 32):
    b = math.log(5 / 8 / (640 / s) ** 2)
    p = 1 / (1 + math.exp(-b))
    print(f"  s={s:2d}: bias={b:.3f}  sigmoid={p:.6f}  BCE of a negative at init = {-math.log(1 - p):.6f}")

# figure: slide rule (cell containing centre) vs project rule (anchor point inside box)
fig, axs = plt.subplots(1, 2, figsize=(7, 3.3))
ax = axs[0]
for k in range(4):
    ax.plot([0, 24], [k * 8, k * 8], color=GREY, lw=0.8)
    ax.plot([k * 8, k * 8], [0, 24], color=GREY, lw=0.8)
ax.add_patch(Rectangle((12.5, 12.5), 5, 5, fill=False, ec=RUST, lw=2))
ax.plot(15, 15, "x", color=RUST, ms=8)
ax.add_patch(Rectangle((8, 8), 8, 8, color=TEAL, alpha=0.25))
ax.set_title("Slide 4.3 s036: vật → ô chứa TÂM vật\n→ luôn có đúng 1 ô chịu trách nhiệm", fontsize=9)
ax.set_xlim(-1, 25), ax.set_ylim(-1, 25), ax.set_aspect("equal"), ax.axis("off")
ax = axs[1]
pts = [(i * 8 + 4, j * 8 + 4) for i in range(3) for j in range(3)]
for k in range(4):
    ax.plot([0, 24], [k * 8, k * 8], color=GREY, lw=0.5, ls=":")
    ax.plot([k * 8, k * 8], [0, 24], color=GREY, lw=0.5, ls=":")
ax.plot([p[0] for p in pts], [p[1] for p in pts], "o", color=NAVY, ms=5, label="điểm neo P3 (stride 8)")
ax.add_patch(Rectangle((12.5, 12.5), 5, 5, fill=False, ec=RUST, lw=2))
ax.add_patch(Polygon(ccw(corners(15, 15, 16, 16, 0.0)), fill=False, ec=TEAL, lw=1.5, ls="--"))
ax.set_title("YOLO11/26: điểm neo nào nằm TRONG hộp?\nhộp 5×5: 0 điểm; vùng STAL-16 (đứt): 4 điểm", fontsize=9)
ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.18), frameon=False, fontsize=8)
ax.set_xlim(-1, 25), ax.set_ylim(-1, 25), ax.set_aspect("equal"), ax.axis("off")
save(fig, "ch3_cell_vs_anchor.png")

# figure: three levels
fig, ax = plt.subplots(figsize=(7, 2.4))
for k, (s, n, col) in enumerate([(8, 100, NAVY), (16, 50, TEAL), (32, 25, AMBER)]):
    x0 = k * 2.4
    ax.add_patch(Rectangle((x0, 0), 2.0, 2.0, fill=False, ec=col, lw=1.5))
    m = 10 if s == 8 else (5 if s == 16 else 3)
    for i in range(m):
        for j in range(m):
            ax.plot(x0 + (i + 0.5) * 2.0 / m, (j + 0.5) * 2.0 / m, ".", color=col, ms=3)
    ax.text(x0 + 1.0, 2.15, f"P{3 + k} · stride {s}\nlưới {n}×{n} = {n * n:,} điểm", ha="center", fontsize=8.5)
ax.text(7.35, 1.0, "ảnh 800×800\n→ 13.125\nđiểm neo", ha="center", va="center", fontsize=9)
ax.set_xlim(-0.1, 8.2), ax.set_ylim(-0.1, 2.8), ax.axis("off")
save(fig, "ch3_levels.png")

# ============================================================================
# C. Chapter 4 - loss
# ============================================================================
header("C1", "Slide BCE (1.2 s010) on single examples and the cost over m=4")
bce = lambda p, y: -(y * math.log(p) + (1 - y) * math.log(1 - p))  # noqa: E731
ex = [(0.9, 1), (0.5, 1), (0.1, 1), (0.2, 0)]
for p, y in ex:
    print(f"  y={y}, yhat={p}: L={bce(p, y):.4f}")
print(f"  cost J = mean = {np.mean([bce(p, y) for p, y in ex]):.4f}")

header("C2", "BCE with a SOFT target s=0.62: minimum is at p=s, not p=1")
s_t = 0.62
for p in (0.30, 0.62, 0.90, 0.99):
    print(f"  p={p:.2f}: BCE={bce(p, s_t):.4f}")
print(f"  minimum value = H(0.62) = {bce(0.62, 0.62):.4f}  (never 0 for a soft target)")
ps = np.linspace(0.01, 0.99, 197)
fig, axs = plt.subplots(1, 2, figsize=(7, 2.9))
axs[0].plot(ps, [bce(p, 1) for p in ps], color=NAVY, label="đích y = 1 (slide)")
axs[0].plot(ps, [bce(p, 0.62) for p in ps], color=TEAL, ls="--", label="đích mềm ŝ = 0,62 (dự án)")
axs[0].axvline(0.62, color=GREY, lw=0.8, ls=":")
axs[0].set_xlabel("xác suất dự đoán p = σ(z)"), axs[0].set_ylabel("BCE")
axs[0].set_ylim(0, 4), axs[0].legend(frameon=False), axs[0].set_title("Cực tiểu nằm tại p = ŝ")
z = np.full(8, -4.6)
sig = 1 / (1 + np.exp(-z))
smx = np.exp(z) / np.exp(z).sum()
xx = np.arange(8)
axs[1].bar(xx - 0.2, sig, 0.4, color=NAVY, label="sigmoid từng lớp")
axs[1].bar(xx + 0.2, smx, 0.4, color=RUST, hatch="//", label="softmax")
axs[1].set_xticks(xx, ["air", "bri", "tank", "ship", "pool", "veh", "per", "wind"], fontsize=7.5)
axs[1].set_title("Điểm neo NỀN, mọi logit = −4,6"), axs[1].set_ylim(0, 0.17)
axs[1].legend(frameon=False, loc="upper center", ncol=2, fontsize=7.5)
save(fig, "ch4_bce_soft.png")

header("C3", "Background anchor: sigmoid vs softmax (8 logits = -4.6)")
print(f"  sigmoid each = {sig[0]:.4f} (sum {sig.sum():.4f}); softmax each = {smx[0]:.4f} (sum {smx.sum():.4f})")
z2 = z.copy()
z2[3] = 2.0
print(f"  ship logit 2.0: sigmoid ship={1 / (1 + math.exp(-2.0)):.4f} others={sig[0]:.4f};"
      f" softmax ship={np.exp(2.0) / np.exp(z2).sum():.4f}")

header("C4", "SIMULATED image: who dominates L_cls, and why we divide by S not N*C")
rng = np.random.default_rng(1)
n_pos = 40
soft = rng.uniform(0.1, 0.6, n_pos)
p_neg, p_pos = 0.005, 0.30
neg_elems = NA * 8 - n_pos
sum_neg = neg_elems * (-math.log(1 - p_neg))
sum_pos = sum(bce(p_pos, s) for s in soft) + n_pos * 7 * (-math.log(1 - p_neg))
S = max(soft.sum(), 1)
print(f"  positives={n_pos}, S=sum soft={S:.3f}")
print(f"  BCE sum: negatives {sum_neg:.2f} | positive anchors {sum_pos:.2f} | total {sum_neg + sum_pos:.2f}")
print(f"  L_cls = total/S = {(sum_neg + sum_pos) / S:.3f} ; total/(N*C) = {(sum_neg + sum_pos) / (NA * 8):.5f}")
soft2 = soft * 0.5
for pn in (0.005, 0.0001):
    sn = (NA * 8 - n_pos) * (-math.log(1 - pn))
    print(f"  background p={pn}: negatives sum={sn:.2f} vs positive anchors sum={sum_pos:.2f} -> L_cls={(sn + sum_pos) / S:.3f}")
print(f"  if soft labels halve (worse matching): S={soft2.sum():.3f}, L_cls={(sum_neg + sum(bce(p_pos, s) for s in soft2) + n_pos * 7 * (-math.log(1 - p_neg))) / soft2.sum():.3f}")

header("C5", "Axis-aligned IoU (slide 4.3 s026): 1-px shift, tiny vs large")
def iou_aa(w, h, dx, dy):
    iw, ih = max(w - abs(dx), 0), max(h - abs(dy), 0)
    return iw * ih / (2 * w * h - iw * ih)
for (w, dx) in [(4, 1), (4, 2), (10, 1), (40, 1), (40, 4)]:
    print(f"  {w}x{w} shifted {dx}px: IoU={iou_aa(w, w, dx, 0):.4f}")

header("C6", "Rotated polygon IoU vs ProbIoU (re-implemented)")
print(f"  identical 10x10: polyIoU={poly_iou((0, 0, 10, 10, 0), (0, 0, 10, 10, 0)):.4f}  ProbIoU={probiou((0, 0, 10, 10, 0), (0, 0, 10, 10, 0)):.5f}")
for dth in (5, 10, 20, 45, 90):
    r = math.radians(dth)
    print(f"  dtheta={dth:2d}deg: 12x4 poly={poly_iou((0, 0, 12, 4, 0), (0, 0, 12, 4, r)):.4f} prob={probiou((0, 0, 12, 4, 0), (0, 0, 12, 4, r)):.4f} | "
          f"10x10 poly={poly_iou((0, 0, 10, 10, 0), (0, 0, 10, 10, r)):.4f} prob={probiou((0, 0, 10, 10, 0), (0, 0, 10, 10, r)):.4f}")
for (w, dx) in [(4, 1), (40, 1)]:
    print(f"  {w}x{w} shift {dx}px: poly={poly_iou((0, 0, w, w, 0), (dx, 0, w, w, 0)):.4f} prob={probiou((0, 0, w, w, 0), (dx, 0, w, w, 0)):.4f}")
# two concrete rotated boxes
bA, bB = (20.0, 20.0, 12.0, 4.0, math.radians(30)), (21.0, 19.5, 11.0, 4.5, math.radians(40))
print(f"  boxes A=(20,20,12,4,30deg) B=(21,19.5,11,4.5,40deg): polyIoU={poly_iou(bA, bB):.4f} ProbIoU={probiou(bA, bB):.4f}"
      f" -> 1-ProbIoU={1 - probiou(bA, bB):.4f}")
sh = np.linspace(0, 4, 41)
dths = np.linspace(0, 90, 91)
fig, axs = plt.subplots(1, 2, figsize=(7, 2.9))
for w, col, ls in [(4, RUST, "-"), (40, NAVY, "-")]:
    axs[0].plot(sh, [poly_iou((0, 0, w, w, 0), (d, 0, w, w, 0)) for d in sh], color=col, ls="-", label=f"IoU đa giác {w}×{w}")
    axs[0].plot(sh, [probiou((0, 0, w, w, 0), (d, 0, w, w, 0)) for d in sh], color=col, ls="--", label=f"ProbIoU {w}×{w}")
axs[0].axhline(0.5, color=GREY, lw=0.8, ls=":")
axs[0].set_xlabel("lệch tâm (px)"), axs[0].set_ylabel("độ trùng"), axs[0].legend(frameon=False, fontsize=7.5)
axs[0].set_title("Lệch 1 px: hộp 4×4 mất gần nửa IoU")
for (w, h), col in [((12, 4), TEAL), ((10, 10), AMBER)]:
    axs[1].plot(dths, [poly_iou((0, 0, w, h, 0), (0, 0, w, h, math.radians(d))) for d in dths], color=col, label=f"IoU đa giác {w}×{h}")
    axs[1].plot(dths, [probiou((0, 0, w, h, 0), (0, 0, w, h, math.radians(d))) for d in dths], color=col, ls="--", label=f"ProbIoU {w}×{h}")
axs[1].set_xlabel("lệch góc Δθ (độ)"), axs[1].legend(frameon=False, fontsize=7.5)
axs[1].set_title("ProbIoU của hộp vuông mù góc")
save(fig, "ch4_iou.png")

header("C7", "eps_f floor=0.01 for sub-stride boxes (grid units) and gradient check")
gt = torch.tensor([[0.0, 0.0, 0.5, 0.5, 0.0]], dtype=torch.float64)  # 4x4 px at stride 8
for floor in (0.0, 0.01):
    pr = torch.tensor([[0.25, 0.0, 0.5, 0.5, 0.0]], dtype=torch.float64, requires_grad=True)  # 2 px shift
    l = 1 - probiou_t(pr, gt, floor=floor)
    l.sum().backward()
    print(f"  floor={floor}: var w^2/12={0.25 / 12:.5f}(+{floor}) ProbIoU={1 - float(l):.4f} |dL/dx|={abs(float(pr.grad[0, 0])):.4f}")
pr0 = torch.tensor([[0.3, -0.1, 0.6, 0.45, 0.2]], dtype=torch.float64, requires_grad=True)
ok = torch.autograd.gradcheck(lambda p: 1 - probiou_t(p, gt, floor=0.01), (pr0,), eps=1e-6, atol=1e-5)
print(f"  torch.autograd.gradcheck(1-ProbIoU) = {ok}")
f = lambda p: float(1 - probiou_t(p, gt, floor=0.01))  # noqa: E731
eps = 1e-7
p_np = pr0.detach().clone()
num = []
for i in range(5):
    e = torch.zeros_like(p_np)
    e[0, i] = eps
    num.append((f(p_np + e) - f(p_np - e)) / (2 * eps))
num = np.array(num)
pr1 = pr0.detach().clone().requires_grad_(True)
(1 - probiou_t(pr1, gt, floor=0.01)).sum().backward()
ana = pr1.grad.numpy()[0]
diff = np.linalg.norm(ana - num) / (np.linalg.norm(ana) + np.linalg.norm(num))
print(f"  analytic grad {ana}\n  numeric  grad {num}\n  slide-2.1 difference = {diff:.2e}")

header("C8", "DFL (reg_max=16) on one side distance")
def dfl(logits, d):
    d = min(max(d, 0.0), 16 - 1 - 0.01)
    tl = int(math.floor(d))
    wl, wr = tl + 1 - d, d - tl
    lp = torch.log_softmax(torch.tensor(logits, dtype=torch.float64), 0)
    return float(-(lp[tl] * wl + lp[tl + 1] * wr)), tl, wl, wr
ideal = np.full(16, 1e-12)
ideal[3], ideal[4] = 0.3, 0.7
l_ideal = dfl(np.log(ideal), 3.7)
peak = np.full(16, 0.1 / 15)
peak[4] = 0.9
uni = np.zeros(16)
print(f"  d=3.7 -> bins ({l_ideal[1]},{l_ideal[1] + 1}) weights ({l_ideal[2]:.2f},{l_ideal[3]:.2f})")
print(f"  ideal p(3)=0.3,p(4)=0.7: DFL={l_ideal[0]:.4f}, decode E[k]={(np.arange(16) * ideal).sum():.4f}")
print(f"  peaked p(4)=0.9: DFL={dfl(np.log(peak), 3.7)[0]:.4f}, decode={(np.arange(16) * peak).sum():.4f}")
print(f"  uniform: DFL={dfl(uni, 3.7)[0]:.4f} (=ln16={math.log(16):.4f}), decode=7.5")
for d in (16.2, -0.8, 0.25):
    print(f"  raw target d={d}: DFL uses clamp -> {min(max(d, 0.0), 14.99):.2f}")
for s in (8, 16, 32):
    print(f"  max representable side distance at stride {s}: 14.99*{s} = {14.99 * s:.1f} px")
fig, ax = plt.subplots(figsize=(7, 2.5))
ax.bar(np.arange(16) - 0.2, ideal, 0.4, color=TEAL, label="đích 'hai nóng' cho d = 3,7")
ax.bar(np.arange(16) + 0.2, peak, 0.4, color=NAVY, hatch="//", label="một phân phối dự đoán (đỉnh ở 4)")
ax.axvline(3.7, color=RUST, ls="--", lw=1)
ax.text(5.0, 0.55, "← d = 3,7", color=RUST)
ax.set_xticks(range(16)), ax.set_xlabel("bin k (đơn vị lưới)"), ax.set_ylabel("xác suất")
ax.legend(frameon=False), ax.set_title("DFL: một khoảng cách = phân phối trên 16 bin")
save(fig, "ch4_dfl.png")

header("C9", "YOLO26 L1 on image-normalised distances")
print(f"  error 0.5 grid unit at stride 8, imgsz 800 -> |0.5*8/800| = {0.5 * 8 / 800:.4f} per side")
print(f"  same error at stride 32 -> {0.5 * 32 / 800:.4f} (4x larger)")
print(f"  negative target d=-0.8 kept: |0.2-(-0.8)|*8/800 = {abs(0.2 + 0.8) * 8 / 800:.4f}")

header("C10", "Angle loss: sin^2(2*dtheta) and omega(r)=exp(-ln^2 r / 9)")
for d in (0, 15, 30, 45, 60, 90, 135, 180):
    r = math.radians(d)
    wr = r - round(r / math.pi) * math.pi
    print(f"  dtheta={d:3d}deg wrapped={math.degrees(wr):6.1f} sin^2(2d)={math.sin(2 * wr) ** 2:.4f}")
for r in (1, 2, 3, 4, 8, 16):
    print(f"  aspect r={r:2d}: omega={math.exp(-math.log(r) ** 2 / 9):.4f}")
fig, axs = plt.subplots(1, 2, figsize=(7, 2.7))
dd = np.linspace(-90, 90, 361)
axs[0].plot(dd, np.sin(2 * np.radians(dd)) ** 2, color=NAVY)
axs[0].set_xlabel("Δθ (độ)"), axs[0].set_title("sin²(2Δθ): 0 tại 0° và ±90°")
rr = np.linspace(1, 16, 200)
axs[1].plot(rr, np.exp(-np.log(rr) ** 2 / 9), color=TEAL)
for r in (1, 2, 4, 8):
    axs[1].plot(r, math.exp(-math.log(r) ** 2 / 9), "o", color=RUST)
axs[1].set_xscale("log", base=2), axs[1].set_xlabel("tỉ lệ cạnh w/h"), axs[1].set_title("ω (λ = 3): hộp vuông nặng nhất")
save(fig, "ch4_angle.png")

header("C11", "YOLO26 progressive weight alpha(e) = 0.1 + 0.7*max(1-e/(E-1),0)")
alpha = lambda e, E: max(1 - e / max(E - 1, 1), 0) * (0.8 - 0.1) + 0.1  # noqa: E731
for E in (100, 24, 12):
    print(f"  E={E}: " + ", ".join(f"e={e}:{alpha(e, E):.3f}" for e in sorted({0, 1, E // 4, E // 2, 3 * E // 4, E - 1})))
fig, ax = plt.subplots(figsize=(7, 2.4))
for E, col, ls in [(100, NAVY, "-"), (24, TEAL, "--"), (12, RUST, ":")]:
    ax.plot(range(E), [alpha(e, E) for e in range(E)], color=col, ls=ls, label=f"E = {E}")
ax.set_xlabel("số epoch đã xong e"), ax.set_ylabel("α(e) (trọng số o2m)"), ax.legend(frameon=False)
ax.set_title("Progressive loss: o2m nặng lúc đầu, o2o nặng lúc cuối")
save(fig, "ch4_alpha.png")

# ============================================================================
# D. Chapter 5 - label assignment
# ============================================================================
header("D1", "TAL alignment t = s^0.5 * u^6")
for s_, u_ in [(0.9, 0.5), (0.1, 0.9), (0.5, 0.7), (0.5, 0.35)]:
    print(f"  s={s_}, u={u_}: t={s_ ** 0.5 * u_ ** 6:.5f}")
t_ = np.array([0.02, 0.01])
u_ = np.array([0.5, 0.4])
print(f"  soft labels for t={t_}, u={u_}: {t_ * u_.max() / (t_.max() + 1e-9)}")

header("D2", "Candidate regions per rule and Prop.1 expectation E[N]=21/1024*area")
K = 21 / 1024
print(f"  21/1024 = {K:.6f}")
for (w, h) in [(4, 4), (12, 4), (10, 10), (25, 4), (60, 5), (12, 8), (20, 5)]:
    row = []
    for nm, rule in RULES.items():
        rw, rh = surrogate(w, h, rule)
        row.append(f"{nm.split()[0]} {rw:.2f}x{rh:.2f}={K * rw * rh:.2f}")
    print(f"  GT {w}x{h}: " + " | ".join(row))

header("D3", "Monte Carlo of Prop.1: random position (uniform in a 32x32 period) and angle")
LAT = {s: np.array([(i + 0.5) * s for i in range(-6, 7)]) for s in (8, 16, 32)}


def mc_counts(w, h, rule, n=20000, seed=0, levels=(8, 16, 32)):
    """Return candidates per GT, candidates inside the true box, P3-only candidates."""
    rng_ = np.random.default_rng(seed)
    cx, cy = rng_.uniform(0, 32, n), rng_.uniform(0, 32, n)
    th = rng_.uniform(0, math.pi, n)
    rw, rh = surrogate(w, h, rule)
    cos, sin = np.cos(th)[:, None], np.sin(th)[:, None]
    tot_, inside_true, p3 = np.zeros(n), np.zeros(n), np.zeros(n)
    for s in levels:
        gx, gy = np.meshgrid(LAT[s] + 32, LAT[s] + 32)
        gx, gy = gx.ravel()[None, :], gy.ravel()[None, :]
        dx, dy = gx - cx[:, None], gy - cy[:, None]
        xr, yr = dx * cos + dy * sin, -dx * sin + dy * cos
        cand = (np.abs(xr) <= rw / 2) & (np.abs(yr) <= rh / 2)
        ing = cand & (np.abs(xr) <= w / 2) & (np.abs(yr) <= h / 2)
        tot_ += cand.sum(1)
        inside_true += ing.sum(1)
        if s == 8:
            p3 += cand.sum(1)
    return tot_, inside_true, p3


MC = {}
for (w, h) in [(4, 4), (10, 10), (16, 16), (12, 4), (25, 4)]:
    for nm, rule in RULES.items():
        if (w, h) == (16, 16) and nm != "A0 TAL":
            continue
        N_, I_, _ = mc_counts(w, h, rule)
        rw, rh = surrogate(w, h, rule)
        MC[(w, h, nm)] = N_
        frac_out = 1 - I_.sum() / max(N_.sum(), 1)
        print(f"  GT {w:2d}x{h:<2d} {nm:17s} region {rw:5.2f}x{rh:5.2f}: E[N] sim={N_.mean():.3f} pred={K * rw * rh:.3f}"
              f" | P(N=0) sim={np.mean(N_ == 0):.3f} bound>={max(0, 1 - K * rw * rh):.3f}"
              f" | frac cand outside true box={frac_out:.3f} (1-|g|/|R|={1 - w * h / (rw * rh):.3f})")
fig, axs = plt.subplots(1, 3, figsize=(7, 2.5), sharey=True)
for ax, (w, h), col in zip(axs, [(4, 4), (10, 10), (16, 16)], [RUST, AMBER, NAVY]):
    N_ = MC[(w, h, "A0 TAL")]
    vals, cnts = np.unique(N_, return_counts=True)
    ax.bar(vals, cnts / len(N_), color=col)
    ax.axvline(K * w * h, color="black", ls="--", lw=1)
    ax.set_title(f"hộp {w}×{h} (TAL)\nE[N] = {N_.mean():.2f}, P(N=0) = {np.mean(N_ == 0):.2f}", fontsize=9)
    ax.set_xlabel("số ứng viên N")
axs[0].set_ylabel("tỉ lệ GT")
save(fig, "ch5_mc_hist.png")

header("D4", "Covering-radius check (critique 5.1 [design]): square side a, random angle, TAL")
for a in (8.0, 10.0, 11.0, 11.31, 12.0, 16.0):
    N_, _, P3 = mc_counts(a, a, ("none",), n=40000, seed=3)
    print(f"  side {a:5.2f}: P(N=0)={np.mean(N_ == 0):.4f}  P(P3 count=0)={np.mean(P3 == 0):.4f}  min P3 count={int(P3.min())}")
print(f"  sqrt(2)*8 = {8 * math.sqrt(2):.4f}; area {2 * 64} px^2 -> E[N] = {K * 128:.3f}")

header("D5", "Conflict prediction: two identical 12x4 boxes, gap 2 px")


def mc_conflict(rule, layout, n=20000, seed=5, w=12.0, h=4.0, gap=2.0):
    rng_ = np.random.default_rng(seed)
    cx, cy = rng_.uniform(0, 32, n), rng_.uniform(0, 32, n)
    th = rng_.uniform(0, math.pi, n)
    rw, rh = surrogate(w, h, rule)
    cos, sin = np.cos(th)[:, None], np.sin(th)[:, None]
    off = np.array([0.0, h + gap]) if layout == "side" else np.array([w + gap, 0.0])
    own = shared = 0
    for s in (8, 16, 32):
        gx, gy = np.meshgrid(LAT[s] + 32, LAT[s] + 32)
        gx, gy = gx.ravel()[None, :], gy.ravel()[None, :]
        dx, dy = gx - cx[:, None], gy - cy[:, None]
        xr, yr = dx * cos + dy * sin, -dx * sin + dy * cos
        inA = (np.abs(xr) <= rw / 2) & (np.abs(yr) <= rh / 2)
        inB = (np.abs(xr - off[0]) <= rw / 2) & (np.abs(yr - off[1]) <= rh / 2)
        own += inA.sum()
        shared += (inA & inB).sum()
    return shared / own


for nm in ("A2 STAL-16", "A4 OA-STAL v2", "A8 san phu 11,31"):
    rule = RULES[nm]
    rw, rh = surrogate(12, 4, rule)
    print(f"  {nm:17s} region {rw:.2f}x{rh:.2f}: side-by-side shared={mc_conflict(rule, 'side'):.3f}"
          f" | end-to-end shared={mc_conflict(rule, 'end'):.3f}")

# figure: regions on the lattice
fig, axs = plt.subplots(1, 2, figsize=(7, 3.6))
for ax, (w, h, thd, title) in zip(axs, [(4, 4, 20, "GT 4×4"), (12, 4, 30, "GT 12×4, θ = 30°")]):
    cxy = (21.0, 19.0)
    for s, mk, ms, col in [(8, "o", 4, NAVY), (16, "s", 6, TEAL), (32, "^", 8, AMBER)]:
        pts_ = [((i + 0.5) * s, (j + 0.5) * s) for i in range(-1, 6) for j in range(-1, 6)]
        pts_ = [p for p in pts_ if 0 <= p[0] <= 42 and 0 <= p[1] <= 40]
        ax.plot([p[0] for p in pts_], [p[1] for p in pts_], mk, color=col, ms=ms, mfc="none" if s > 8 else col,
                label=f"điểm neo stride {s}")
    th = math.radians(thd)
    regs = [("A0 TAL", RUST, "-", 2.0), ("A2 STAL-16", NAVY, "--", 1.3), ("A4 OA-STAL v2", TEAL, "-.", 1.3)]
    for nm, col, ls, lw in regs:
        rw, rh = surrogate(w, h, RULES[nm])
        ax.add_patch(Polygon(ccw(corners(cxy[0], cxy[1], rw, rh, th)), fill=nm == "A0 TAL", fc=RUST if nm == "A0 TAL" else "none",
                             alpha=0.9 if nm == "A0 TAL" else 1, ec=col, ls=ls, lw=lw, label=f"{nm}: {rw:.1f}×{rh:.1f}"))
    ax.set_xlim(0, 42), ax.set_ylim(0, 40), ax.set_aspect("equal"), ax.set_title(title, fontsize=9.5)
    ax.set_xticks([]), ax.set_yticks([])
h_, l_ = axs[1].get_legend_handles_labels()
fig.legend(h_, [lab.replace("A0 TAL: 12.0×4.0", "A0 TAL = hộp thật") for lab in l_], loc="lower center", ncol=3, frameon=False, fontsize=7.5,
           bbox_to_anchor=(0.5, -0.06))
save(fig, "ch5_regions.png")

header("D6", "Toy end-to-end: re-implemented RotatedTAL + v8OBBLoss (YOLO26 L1 branch), SIMULATED predictions")
torch.manual_seed(0)
IMG, C = 128, 8
anc_list, st_list = [], []
for s in (8, 16, 32):
    n = IMG // s
    yy, xx_ = torch.meshgrid(torch.arange(n) + 0.5, torch.arange(n) + 0.5, indexing="ij")
    anc_list.append(torch.stack([xx_, yy], -1).view(-1, 2))
    st_list.append(torch.full((n * n, 1), float(s)))
anc_g = torch.cat(anc_list).double()
stride = torch.cat(st_list).double()
anc_px = anc_g * stride
Nt = len(anc_g)
# GT: (x, y, w, h, theta) pixels, long-edge; labels: 3 ship, 5 vehicle, 2 storage-tank
gts = torch.tensor([
    [37.0, 45.0, 12.0, 4.0, math.radians(30)],   # ship 12x4
    [83.0, 26.0, 5.0, 5.0, math.radians(10)],    # vehicle 5x5
    [101.0, 99.0, 10.0, 10.0, 0.0],              # storage-tank 10x10
    [61.0, 85.0, 5.0, 3.0, math.radians(80)],    # vehicle 5x3
    [61.0 - 5.0 * math.sin(math.radians(80)), 85.0 + 5.0 * math.cos(math.radians(80)), 5.0, 3.0, math.radians(80)],  # neighbour, gap 2 px
], dtype=torch.float64)
labels = torch.tensor([3, 5, 2, 5, 5])
names_gt = ["ship 12x4", "vehicle 5x5", "tank 10x10", "vehicle 5x3 (a)", "vehicle 5x3 (b)"]
M = len(gts)
bias0 = torch.log(5 / C / (640 / stride) ** 2)  # head.py bias_init per level
cls_logits0 = bias0 + 3.0 + torch.randn(Nt, C, dtype=torch.float64)  # "a few hundred steps after init" (SIMULATED)
dist0 = 0.4 + 0.8 * torch.rand(Nt, 4, dtype=torch.float64)
ang0 = 0.3 * torch.randn(Nt, 1, dtype=torch.float64)


def dist2rbox(d, a, anc):
    lt, rb = d[:, :2], d[:, 2:]
    cos, sin = torch.cos(a), torch.sin(a)
    xf, yf = ((rb - lt) / 2).split(1, -1)
    xy = torch.cat([xf * cos - yf * sin, xf * sin + yf * cos], -1) + anc
    return torch.cat([xy, lt + rb, a], -1)


def rbox2dist(tb, anc, ta):
    off = tb[:, :2] - anc
    cos, sin = torch.cos(ta), torch.sin(ta)
    xf = off[:, :1] * cos + off[:, 1:2] * sin
    yf = -off[:, :1] * sin + off[:, 1:2] * cos
    w, h = tb[:, 2:3], tb[:, 3:4]
    return torch.cat([w / 2 - xf, h / 2 - yf, w / 2 + xf, h / 2 + yf], -1)


def inside_rot(pts, boxes):
    """(M,N) closed point-in-rotated-box test, same as select_candidates_in_gts."""
    d = pts[None, :, :] - boxes[:, None, :2]
    c, s = torch.cos(boxes[:, 4:5]), torch.sin(boxes[:, 4:5])
    xr = d[..., 0] * c + d[..., 1] * s
    yr = -d[..., 0] * s + d[..., 1] * c
    return (xr.abs() <= boxes[:, 2:3] / 2 + 1e-9) & (yr.abs() <= boxes[:, 3:4] / 2 + 1e-9)


def assign(rule, pd_scores, pd_px, topk=10, topk2=None):
    reg = gts.clone()
    for m in range(M):
        reg[m, 2], reg[m, 3] = torch.tensor(surrogate(float(gts[m, 2]), float(gts[m, 3]), rule))
    cand = inside_rot(anc_px, reg).double()
    sc = pd_scores[:, labels].T
    u = probiou_t(gts[:, None, :].expand(M, Nt, 5).reshape(-1, 5), pd_px[None].expand(M, Nt, 5).reshape(-1, 5)).view(M, Nt).clamp(min=0) * cand
    t = sc.pow(0.5) * u.pow(6.0) * cand
    ti = torch.topk(t, topk, -1).indices
    cnt = torch.zeros(M, Nt, dtype=torch.float64).scatter_add_(-1, ti, torch.ones_like(ti, dtype=torch.float64))
    cnt[cnt > 1] = 0
    mpos = cnt * cand
    fg = mpos.sum(0)
    multi = (fg > 1)[None].expand(M, Nt)
    is_max = torch.zeros(M, Nt, dtype=torch.float64).scatter_(0, u.argmax(0)[None], 1.0)
    n_conf = int((fg > 1).sum())
    mpos = torch.where(multi, is_max, mpos)
    if topk2 is not None and topk2 != topk:
        am = t * mpos
        idx = torch.topk(am, topk2, -1).indices
        mpos = mpos * torch.zeros(M, Nt, dtype=torch.float64).scatter_(-1, idx, 1.0)
    fgv, gidx = mpos.max(0)
    am = t * mpos
    norm = (am * (u * mpos).amax(-1, keepdim=True) / (am.amax(-1, keepdim=True) + 1e-9)).amax(0)
    ts = torch.zeros(Nt, C, dtype=torch.float64)
    ts[torch.arange(Nt), labels[gidx]] = norm
    ts = ts * fgv[:, None]
    return cand, mpos, fgv.bool(), gts[gidx].clone(), ts, n_conf


def obb_loss(rule, topk=10, topk2=None, verbose=True, grads=False):
    cls_l = cls_logits0.clone().requires_grad_(True)
    dist = dist0.clone().requires_grad_(True)
    ang = ang0.clone().requires_grad_(True)
    pred_g = dist2rbox(dist, ang, anc_g)
    pd_px = pred_g.detach().clone()
    pd_px[:, :4] *= stride
    cand, mpos, fg, tb, ts, n_conf = assign(rule, torch.sigmoid(cls_l.detach()), pd_px, topk, topk2)
    S = torch.clamp(ts.sum(), min=1.0)
    l_cls = F.binary_cross_entropy_with_logits(cls_l, ts, reduction="none").sum() / S
    weight = ts[fg].sum(-1)
    tb[:, :4] /= stride
    iou = probiou_t(pred_g[fg], tb[fg], floor=0.01).squeeze(-1)
    l_box = ((1 - iou) * weight).sum() / S
    tl = rbox2dist(tb[:, :4], anc_g, tb[:, 4:5]) * stride / IMG
    pl = dist * stride / IMG
    l_l1 = ((pl[fg] - tl[fg]).abs().mean(-1) * weight).sum() / S
    log_ar = torch.log((tb[:, 2] + 1e-9) / (tb[:, 3] + 1e-9))
    om = torch.exp(-log_ar**2 / 9)
    dth = pred_g[:, 4] - tb[:, 4]
    dth = dth - torch.round(dth / math.pi) * math.pi
    l_ang = (om[fg] * torch.sin(2 * dth[fg]) ** 2 * weight).sum() / S
    neg_t = int((tl[fg] < 0).any(-1).sum())
    total = 1 * (7.5 * l_box + 0.5 * l_cls + 1.5 * l_l1 + 1.0 * l_ang)
    out = dict(cand=cand.sum(1).tolist(), pos=mpos.sum(1).tolist(), S=float(S), cls=float(l_cls), box=float(l_box),
               l1=float(l_l1), ang=float(l_ang), total=float(total), npos=int(fg.sum()), conf=n_conf, neg_t=neg_t,
               maxsoft=[float(ts[mpos[m].bool()].max()) if mpos[m].sum() > 0 else 0.0 for m in range(M)])
    if grads:
        g = {}
        for nm_, term, leaf in [("cls", l_cls, cls_l), ("box", l_box, dist), ("l1", l_l1, dist), ("ang", l_ang, ang)]:
            gg = torch.autograd.grad(term, leaf, retain_graph=True, allow_unused=True)[0]
            g[nm_] = int((gg.abs().sum(-1) > 0).sum()) if gg is not None else 0
        out["grad_anchors"] = g
    if verbose:
        print(f"  {rule}: candidates/GT={[int(c) for c in out['cand']]} positives/GT={[int(p) for p in out['pos']]}"
              f" conflicts={n_conf}")
        print(f"     max soft label/GT={[round(v, 3) for v in out['maxsoft']]}  S={out['S']:.4f}  positives={out['npos']}"
              f"  positives needing a negative distance target={neg_t}")
        print(f"     L_box={out['box']:.4f} L_cls={out['cls']:.4f} L_l1={out['l1']:.5f} L_ang={out['ang']:.4f}"
              f" -> B*(7.5*box+0.5*cls+1.5*l1+1.0*ang) with B=1 = {out['total']:.4f}")
    return out


print(f"  anchors in 128x128 image: {Nt} (16^2+8^2+4^2); GTs: {names_gt}")
toy = {}
for nm in ("A0 TAL", "A1 STAL-8", "A2 STAL-16", "A4 OA-STAL v2", "A8 san phu 11,31"):
    print(f" arm {nm}")
    toy[nm] = obb_loss(RULES[nm], grads=(nm == "A2 STAL-16"))
print("  anchors with non-zero gradient per term (A2):", toy["A2 STAL-16"]["grad_anchors"], f"of {Nt}")
print(" o2o branch (topk=7, topk2=1) on the same predictions, A2:")
o2o = obb_loss(RULES["A2 STAL-16"], topk=7, topk2=1)
for E, e in [(100, 0), (100, 99)]:
    a_ = alpha(e, E)
    print(f"  E={E} e={e}: alpha={a_:.2f}: L_total = {a_:.2f}*{toy['A2 STAL-16']['total']:.4f} + {1 - a_:.2f}*{o2o['total']:.4f}"
          f" = {a_ * toy['A2 STAL-16']['total'] + (1 - a_) * o2o['total']:.4f}")

# ============================================================================
# E. Chapter 6 - one training run
# ============================================================================
header("E1", "Iterations, optimizer steps and optimizer=auto (trainer.py), N_train=12,600 [estimate]")
Ntr, nbs = 12600, 64
for batch in (16, 8):
    acc = max(round(nbs / batch), 1)
    it_ep = math.ceil(Ntr / batch)
    print(f"  batch {batch}: iterations/epoch={it_ep}, accumulate={acc}, optimizer steps/epoch~{it_ep / acc:.0f}")
for E in (12, 24, 50, 51, 100):
    iters = math.ceil(Ntr / max(16, nbs)) * E
    choice = "MuSGD lr=0.01" if iters > 10000 else f"AdamW lr={round(0.002 * 5 / (4 + 8), 6)}"
    print(f"  E={E:3d}: auto-iterations={iters:6d} -> {choice}; total forward/backward iterations={math.ceil(Ntr / 16) * E}")
for batch in (16, 12, 8):
    acc = max(round(nbs / batch), 1)
    print(f"  weight decay effective (batch {batch}, acc {acc}) = 0.0005*{batch}*{acc}/64 = {0.0005 * batch * acc / nbs:.6f}")

header("E2", "LR schedule lr0*[(1-e/E)(1-lrf)+lrf] vs slide 2.2 s050 decay; warmup")
lf = lambda e, E: max(1 - e / E, 0) * (1 - 0.01) + 0.01  # noqa: E731
for e in (0, 1, 3, 50, 99):
    print(f"  E=100 e={e:3d}: lr={0.01 * lf(e, 100):.6f}")
for e in (1, 2, 3, 4):
    print(f"  slide alpha0=0.2 decay_rate=1 epoch {e}: {0.2 / (1 + e):.4f}")
nb = math.ceil(Ntr / 16)
nw = round(3.0 * nb)
print(f"  warmup iterations = round(3*{nb}) = {nw} (= 3 epochs); for E=12 warmup is {3 / 12:.0%} of training")
fig, axs = plt.subplots(1, 2, figsize=(7, 2.8))
E = 100
ep = np.arange(E)
axs[0].plot(ep, [0.01 * lf(e, E) for e in ep], color=NAVY, label="dự án: tuyến tính, lrf = 0,01")
axs[0].plot(ep, [0.01 / (1 + 0.05 * e) for e in ep], color=GREY, ls="--", label="slide: α₀/(1+0,05·epoch)")
axs[0].set_xlabel("epoch"), axs[0].set_ylabel("learning rate"), axs[0].legend(frameon=False, fontsize=7.5)
axs[0].set_title("Lịch learning rate (E = 100, lr0 = 0,01)")
its = np.arange(0, 4 * nb)
w_lr, b_lr, mom = [], [], []
for ni in its:
    epc = ni // nb
    if ni < nw:
        w_lr.append(np.interp(ni, [0, nw], [0.0, 0.01 * lf(epc, E)]))
        b_lr.append(np.interp(ni, [0, nw], [0.1, 0.01 * lf(epc, E)]))
        mom.append(np.interp(ni, [0, nw], [0.8, 0.937]))
    else:
        w_lr.append(0.01 * lf(epc, E)), b_lr.append(0.01 * lf(epc, E)), mom.append(0.937)
axs[1].plot(its / nb, w_lr, color=NAVY, label="lr trọng số")
axs[1].plot(its / nb, b_lr, color=RUST, ls="--", label="lr bias")
ax2 = axs[1].twinx()
ax2.plot(its / nb, mom, color=TEAL, ls=":", label="momentum")
ax2.set_ylabel("momentum", color=TEAL)
axs[1].set_xlabel("epoch (tính theo iteration)"), axs[1].set_title("Warmup 3 epoch (SGD, không 'auto')")
axs[1].legend(frameon=False, fontsize=7.5, loc="center right")
save(fig, "ch6_lr.png")

header("E3", "ModelEMA decay d(x)=0.9999*(1-exp(-x/2000)), x = optimizer steps; window ~ 1/(1-d)")
steps_ep = math.ceil(Ntr / 16) / 4
for x_ in (197, 1000, 2000, 2364, 4728, 9850, 19700):
    d = 0.9999 * (1 - math.exp(-x_ / 2000))
    print(f"  after {x_:5d} steps (~{x_ / steps_ep:5.1f} epochs): d={d:.4f}, window~{1 / (1 - d):8.1f} steps")

header("E4", "GPU-hours per run = N*E/(r*3600) (PROP 9) and Kaggle 12-h sessions")
for Nimg in (14000, 12600):
    for r in (100, 50, 25):
        gh = Nimg * 100 / (r * 3600)
        print(f"  N={Nimg} E=100 r={r:3d} img/s: {gh:5.2f} GPU-h -> sessions of 12 h: {math.ceil(gh / 12)}; epoch = {Nimg / r / 60:.1f} min")
for E in (12, 24):
    print(f"  N=12600 E={E} r=25: {12600 * E / (25 * 3600):.2f} GPU-h")

header("E5", "R-native scale augmentation s~U(0.5,1.5) on tiny GTs (augment.py L1159)")
for side in (3, 4, 6, 10, 14):
    print(f"  native short side {side:2d}px: P(<8 after scale)={min(max((8 / side - 0.5), 0), 1):.3f}"
          f"  P(<16)={min(max((16 / side - 0.5), 0), 1):.3f}  P(<=2, dropped)={min(max((2 / side - 0.5), 0), 1):.3f}")

# timeline figure
fig, ax = plt.subplots(figsize=(7, 3.0))
ax.add_patch(Rectangle((0, 2.2), 12, 0.5, color=NAVY, alpha=0.85))
ax.add_patch(Rectangle((12, 2.2), 3.6, 0.5, color=TEAL, alpha=0.85))
ax.text(6, 2.45, "phiên Kaggle 1 (≤ 12 h)", color="white", ha="center", va="center", fontsize=8.5)
ax.text(13.8, 2.45, "phiên 2 (resume)", color="white", ha="center", va="center", fontsize=8)
ax.text(15.9, 2.45, "→ test 1 lần\n(AITODReval)", va="center", fontsize=8)
ax.annotate("", xy=(12, 2.05), xytext=(12, 1.6), arrowprops=dict(arrowstyle="->", color=RUST))
ax.text(12, 1.45, "last.pt", ha="center", fontsize=8, color=RUST)
for k in range(0, 101, 10):
    xk = k * 15.6 / 100
    ax.plot([xk, xk], [2.15, 2.75], color="white", lw=0.6)
ax.add_patch(Rectangle((15.6 * 0.9, 2.75), 15.6 * 0.1, 0.12, color=AMBER))
ax.text(15.6 * 0.95, 2.95, "tắt mosaic\n10 epoch cuối", ha="center", fontsize=7.5, color=AMBER)
ax.text(0, 3.05, "1 run R-native, E = 100, r = 25 ảnh/s [ước lượng]: 15,6 GPU-h", fontsize=8.5)
y0 = 0.3
ax.text(0, 1.15, "phóng to 1 epoch:", fontsize=8.5)
for i in range(16):
    ax.add_patch(Rectangle((i * 0.75, y0), 0.7, 0.5, color=GREY if (i + 1) % 4 else NAVY, alpha=0.8))
    if (i + 1) % 4 == 0:
        ax.text(i * 0.75 + 0.35, y0 - 0.22, "step", ha="center", fontsize=7, color=NAVY)
ax.text(12.2, y0 + 0.25, "… 788 iteration (batch 16)\n= 197 bước optimizer\n→ hết epoch: val + lưu last.pt", fontsize=7.8, va="center")
ax.set_xlim(-0.2, 18.5), ax.set_ylim(-0.1, 3.3), ax.axis("off")
save(fig, "ch6_timeline.png")

# ============================================================================
# F. Chapter 7 - evaluation and statistics
# ============================================================================
header("F1", "Slide 3.1 s014 precision/recall/F1")
P_, R_ = 3 / 4, 3 / 5
print(f"  P={P_:.3f} R={R_:.3f} F1={2 / (1 / P_ + 1 / R_):.3f} acc={7 / 10:.2f}")
print(f"  classifier A F1={2 / (1 / 0.95 + 1 / 0.90):.4f}, B F1={2 / (1 / 0.98 + 1 / 0.85):.4f}")

header("F2", "SIMULATED PR curve and COCO 101-point AP")
rng = np.random.default_rng(7)
n_gt = 20
scores = np.sort(rng.uniform(0, 1, 25))[::-1]
tp = (rng.uniform(0, 1, 25) < np.linspace(0.95, 0.25, 25)).astype(float)
tp_c, fp_c = np.cumsum(tp), np.cumsum(1 - tp)
rec, prec = tp_c / n_gt, tp_c / (tp_c + fp_c)


def ap101(rec, prec):
    env = np.maximum.accumulate(prec[::-1])[::-1]
    rt = np.linspace(0, 1, 101)
    idx = np.searchsorted(rec, rt, side="left")
    q = np.where(idx < len(env), env[np.minimum(idx, len(env) - 1)], 0.0)
    return q.mean(), env


ap, env = ap101(rec, prec)
print(f"  detections=25, TP={int(tp.sum())}, GT={n_gt}, final recall={rec[-1]:.3f}, AP(101-pt)={ap:.4f}")
fig, ax = plt.subplots(figsize=(7, 2.6))
ax.plot(rec, prec, "o-", color=GREY, ms=3, lw=0.8, label="precision thô")
ax.step(rec, env, where="post", color=NAVY, label="bao nội suy (max bên phải)")
ax.fill_between(rec, env, step="post", color=NAVY, alpha=0.12)
ax.set_xlabel("recall"), ax.set_ylabel("precision"), ax.set_xlim(0, 1), ax.set_ylim(0, 1.05)
ax.set_title(f"Dữ liệu giả lập: AP (101 điểm) = {ap:.3f}; recall dừng ở {rec[-1]:.2f}"), ax.legend(frameon=False)
save(fig, "ch7_pr.png")

header("F3", "How many of the 10 IoU thresholds 0.50:0.05:0.95 a 1-px error passes")
thr = np.round(np.arange(0.5, 0.951, 0.05), 2)
for w in (4, 10, 40):
    v = poly_iou((0, 0, w, w, 0), (1, 0, w, w, 0))
    print(f"  {w}x{w} shifted 1px: IoU={v:.4f} passes {int(np.sum(v >= thr - 1e-12))}/10 thresholds")
v = poly_iou((0, 0, 12, 4, 0), (0, 0, 12, 4, math.radians(10)))
print(f"  12x4 rotated 10deg: IoU={v:.4f} passes {int(np.sum(v >= thr - 1e-12))}/10")

header("F4", "Detection cap: YOLO max_det is per IMAGE (all classes); AITODReval keeps 1500 per (image,class)")
for n_obj in (27, 300, 1200, 2000):
    caps = {md: min(1.0, md / n_obj) for md in (300, 1500, 12000)}
    print(f"  image with {n_obj:4d} GT (one class): recall ceiling max_det=300 {caps[300]:.3f} | 1500 {caps[1500]:.3f} | 12000 {caps[12000]:.3f}")
print(f"  1500 per (image,class) x 8 classes = {1500 * 8} detections per image")

header("F5", "SIMULATED paired image-level bootstrap of Delta AP (A4 - A2), 3 seeds, 10,000 resamples")
rng = np.random.default_rng(11)
n_img = 300
gt_per = rng.poisson(8, n_img) + 1


def sim_arm(p_det, seed_noise, base_u, fp_u):
    sc, tpf, img = [], [], []
    for i in range(n_img):
        for g in range(gt_per[i]):
            if base_u[i][g] < p_det + seed_noise[i]:
                sc.append(0.4 + 0.6 * base_u[i][g] ** 0.5 * 0.9 + 0.05 * rng.uniform()), tpf.append(1.0), img.append(i)
        for f_ in fp_u[i]:
            sc.append(f_), tpf.append(0.0), img.append(i)
    sc, tpf, img = np.array(sc), np.array(tpf), np.array(img)
    o = np.argsort(-sc)
    return tpf[o], img[o]


base_u = [rng.uniform(0, 1, k) for k in gt_per]
fp_u = [rng.uniform(0, 0.8, rng.poisson(4)) for _ in range(n_img)]
arms = {}
for seed in range(3):
    noise = rng.normal(0, 0.03, n_img)
    arms[("A2", seed)] = sim_arm(0.55, noise + rng.normal(0, 0.01), base_u, fp_u)
    arms[("A4", seed)] = sim_arm(0.57, noise + rng.normal(0, 0.01), base_u, fp_u)


def ap_weighted(tpf, img, wimg):
    w = wimg[img]
    tc = np.cumsum(w * tpf)
    fc = np.cumsum(w * (1 - tpf))
    ngt = np.sum(wimg * gt_per)
    rec_, prec_ = tc / ngt, tc / np.maximum(tc + fc, 1e-12)
    return ap101(rec_, prec_)[0]


ones = np.ones(n_img)
aps = {k: ap_weighted(*v, ones) for k, v in arms.items()}
for a_ in ("A2", "A4"):
    vals = [aps[(a_, s)] for s in range(3)]
    print(f"  {a_}: AP per seed {np.round(vals, 4)} mean={np.mean(vals):.4f} std={np.std(vals, ddof=1):.4f}")
d_point = np.mean([aps[("A4", s)] - aps[("A2", s)] for s in range(3)])
B = 10000
deltas = np.empty(B)
t_b = time.time()
for b in range(B):
    wimg = np.bincount(rng.integers(0, n_img, n_img), minlength=n_img).astype(float)
    deltas[b] = np.mean([ap_weighted(*arms[("A4", s)], wimg) - ap_weighted(*arms[("A2", s)], wimg) for s in range(3)])
lo, hi = np.percentile(deltas, [2.5, 97.5])
print(f"  point Delta AP (mean over seeds) = {d_point:.4f}; 95% CI = [{lo:.4f}, {hi:.4f}]; excludes 0: {lo > 0 or hi < 0}")
print(f"  bootstrap time {time.time() - t_b:.1f} s for {B} resamples x 3 seeds x 2 arms (weights trick, no re-matching)")
fig, ax = plt.subplots(figsize=(7, 2.4))
ax.hist(deltas, bins=60, color=NAVY, alpha=0.8)
ax.axvline(0, color=RUST, lw=1.2, label="Δ = 0")
ax.axvline(lo, color=TEAL, ls="--"), ax.axvline(hi, color=TEAL, ls="--", label="KTC 95%")
ax.set_xlabel("ΔAP (A4 − A2), trung bình 3 seed"), ax.legend(frameon=False)
ax.set_title("Dữ liệu giả lập: phân phối bootstrap ghép cặp theo ảnh (10.000 lần)")
save(fig, "ch7_bootstrap.png")

header("F6", "Slide 3.2 s007 error-analysis ceiling")
print(f"  dev error 10%, 8 of 100 errors are dogs -> best case error {10 * (1 - 0.08):.1f}%")
print(f"  if 50 of 100 errors were dogs -> best case {10 * (1 - 0.5):.1f}%")

print(f"\n[done] total runtime {time.time() - T0:.1f} s; figures in {FIG}")
