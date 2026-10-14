# Where Do Tiny Oriented Objects Lose Their Positives? Candidate-Region Geometry in Real-Time YOLO-OBB Detectors on AI-TOD-R

> **Interpretation correction, 2026-10-15 (C-19).** See [the research audit](t07-q2-audit-2026-10-15/REPORT.md) and [mathematical critique](t07-q2-audit-2026-10-15/LOGIC-CRITIQUE.md). Equal area gives equal expected candidate count under uniform lattice phase; it does **not** imply equal zero-candidate probability, a second-order effect, or similar AP. The √2s closed-lattice coverage guarantee does not guarantee final TAL positives or an optimal AP floor. A0/A1/A2/A8 remain exploratory contrasts; withdraw deterministic intervention-tier→journal-quartile claims below. Earlier revision boxes and body are retained as historical design, with this correction taking precedence. No new experiments or venue band are established.

**Research proposal: topic #7, direction C-3, revised (v2)**

| Field | Value |
|---|---|
| Course / context | DPL302m (Deep Learning), semester 5; student research project (NCKH) |
| Team / supervisor | [to be filled by the team] |
| Date / version | 2026-10-08 · v2 (supersedes `notes/t07-proposal.md` v1 of 2026-10-01) |
| Ledger entry | C-10, REVISION of C-3 (see §13); **revised → C-11 on 2026-10-13** (see the revision box below) |
| Status | **Not runnable as stated.** Data access (xView registration), throughput and the in-house baseline are unverified until Phase 0 passes (§10). No experiment has been run; **no result in this document is a measured outcome of this project.** |

> **Revision v2.1 (2026-10-13, ledger C-11).** Adopted by the team after the Q2-level critique
> (`notes/t07-critique-q2-2026-10-11.md`). Changes, all marked *[v2.1]* in the text:
> 1. **Primary contrast** is now the threshold/coverage factorial **A0 (TAL), A1 (STAL-8), A2 (STAL-16),
>    A8 (coverage-minimal floor)**; A4 vs A2 becomes a secondary mechanism test (§7.4, §8.5).
>    Reason: Corollary 2 already predicts A4 ≈ A2 in expected candidate count.
> 2. **New arm A8 [design]:** short side < $\sqrt{2}\,s_{\min}$ (11.31 px at $s=8$) is floored to
>    11.31 px. Covering-radius argument [derived, critique §5.1]: any region whose short side is
>    ≥ $\sqrt{2}\,s$ contains at least one anchor centre at every position and angle, so STAL-16 uses
>    2× the minimal guaranteeing area.
> 3. **Detection cap:** AITODReval keeps 1,500 detections **per (image, class)**; YOLO's `max_det` is
>    per image, so we set `max_det = 12,000` (1,500 × 8 classes) (§8.2).
> 4. **Bootstrap unit:** scene-clustered, not image-level, because crops of one scene are not
>    independent (§8.6).
> 5. **Scope for the 4-week plan (11/10 → 08/11/2026, `ROADMAP.md`):** YOLO26n only for ablations;
>    A5–A7 cut; seeds 4–5 for the primary pair; RQ4 only if a second source-independent dataset is
>    ready by 25/10. The 14-week timeline in §11 is superseded.
> 6. Positioning must add **MCSA** (*Sci. Rep.* 2025, oriented-tiny sample assignment) and CDCEDet.
>
> Tier and band are unchanged: **T1**, Scopus conference (ICORE C–B) / Q4, conditional; Q2/Q1 not
> defensible (C-11).

> **Revision v2.2 (2026-10-14, ledger C-16).** Positioning update, design unchanged
> (`notes/t07-venue-assessment-2026-10-14.md`):
> 1. **OSCAR** (Dai et al., IEEE TGRS 2023, DOI 10.1109/tgrs.2023.3243062) already sweeps a square
>    pseudo-box p ∈ {none, s, 1.5s, 2s} for sub-stride targets (HBB, infrared, one level) and reports a
>    non-monotonic optimum. "Floor size matters" is therefore not new; A8 is framed as the
>    **orientation-invariant** coverage condition (short side ≥ √2·s_min, tight for a 45° square;
>    axis-aligned boxes need only s) tested in YOLO's multi-level point-in-box step on dense tiny OBB.
>    Add OSCAR to Table 1.
> 2. **MCSA** full text read (2026-10-14): RetinaNet-OBB with a dynamic prior block, metric t = s + u + d
>    and a DGMM filter, on DOTA-v1.0/1.5/2.0 and DIOR-R; no AI-TOD-R, no YOLO, no STAL. Cite as the
>    closest "oriented tiny sample assignment" work; it does not occupy RQ2.
> 3. Preregistration: the sign of A8 vs A2 is not assumed (OSCAR favours ≈1.5s; YOLO26 Table 6 shows
>    s_ref = 8 below TAL on COCO); predictions are stratified by density.
> 4. Q3 is above the T1 band and additionally requires the √2·s condition to predict the best floor on
>    two source-independent datasets.

**Evidence conventions.**
- Bracketed numbers [n] refer to §16. Every factual statement about a paper is traceable to a page, table or code line in Appendix A.
- Each equation carries one tag:
  - **[cited]** = taken from the named source;
  - **[derived]** = derived here, with a stated sanity check;
  - **[design]** = our design choice, unproven, needs experiments.
- "We expect" or "hypothesis" marks a prediction, never a result.

---

## 1. Abstract

Tiny objects in aerial images (a few to a few tens of pixels) are where dense detectors fail most. For one-stage detectors, the first point of failure is not the classifier but **label assignment**: a ground-truth (GT) box smaller than the feature stride may contain no anchor point at all and receive no training signal [1, p7].
- The Ultralytics YOLO family addressed this with **STAL** (Small-Target-Aware Label Assignment), which enlarges tiny GT boxes during candidate selection only [1].
- STAL was ablated **only on COCO with horizontal boxes** [1, p12–13]. It has never been evaluated on oriented boxes or on any tiny-object dataset.
- Its rule for oriented boxes in the public code changed three times between January and August 2026, ending with a threshold different from the published one [2] (§2.2).
- On AI-TOD-R, the oriented tiny-object benchmark (mean object size 10.6 ± 4.9 px) [3, p3], no protocol-matched, size-binned evaluation of stock YOLO-OBB detectors with the official evaluator was found. The only YOLO-OBB numbers placed next to its benchmark use a different image set, a 4-channel input and no size bins [4].

We propose a three-part study:
1. **An evaluator-matched benchmark** of YOLO11- and YOLO26-OBB on AI-TOD-R. Results are reported per size bin and class, and anchored by an in-house reproduction of a published MMRotate baseline.
2. **A geometric and empirical diagnosis** of candidate-region rules (no floor, the published STAL rule, the current STAL rule). It rests on a simple proposition: the expected number of candidates equals the region's area times $\sum_s s^{-2}$. Hence **rules with equal area differ only in where candidates fall and in how they conflict between neighbouring objects**, not in how many there are.
3. **A training-only, zero-inference-cost intervention.** It combines a shape-preserving minimum-area candidate surrogate (OA-STAL v2), with a short-side floor and a conditional long-side cap, and a conflict-resolution rule. Every test uses pre-declared, falsifiable predictions derived from label statistics *before* training. Generalisation is tested on a second dataset.

The contribution is deliberately modest (an assignment-level change, novelty tier T1). Its value lies in measurement quality: one pinned code fork, the official evaluator, three seeds and paired bootstrap confidence intervals.

---

## 2. Motivation

### 2.1 Why tiny oriented objects, and why real-time detectors

AI-TOD-R provides 28,036 images and 752,460 oriented boxes in 8 classes [3, p3–4].
- Mean size 10.6 ± 4.9 px, the smallest among the oriented datasets in its Table I [3, p3].
- "Most objects are gathered within the tiny scale (<16×16 pixels)" [3, p4].
- An image "can contain over 2000 objects, with most images featuring over 100 objects" [3, p4–5].

Its benchmark of 27 configurations (about 19 distinct methods) shows how hard the regime is [3, p6, Table II]:
- The best entry, DCFL on S2A-Net trained for 40 epochs, reaches 17.5 AP and 6.5 AP on very tiny objects ($AP_{vt}$).
- A standard two-stage detector (Oriented R-CNN, R-50) reaches 11.2 AP but only 0.6 $AP_{vt}$.
- The authors trace this to assignment. "At the prior level, tiny-scale objects receive significantly fewer positive samples than larger-scale objects", because "the stride of prior locations in a typical single-stage detector is at least 8 pixels" [3, p8].

Real-time detectors matter for the applications that motivate tiny-object detection (on-board or edge processing). Yet the AI-TOD-R table reports no speed and contains no YOLO model [3, p6].

### 2.2 STAL: an untested fix that keeps changing

YOLO26 states the failure mode precisely: "a tiny box may contain no valid anchor centers at all. In that case, the object receives zero positive candidates" [1, p7].
- STAL builds a surrogate box for candidate filtering only: each side $d < s_{min}$ is replaced by $s_{ref}$, with $s_{min} = 8$ and $s_{ref} = 16$ [1, p7, p11]. The original box is kept for scoring and regression [1, p8].
- The only evidence is on COCO with YOLO11s [1, p13, Table 6], single runs, no variance reported:

| Variant | AP | $AP_S$ |
|---|---|---|
| TAL | 46.6 | 29.0 |
| STAL ($s_{ref}$ = 16) | 46.8 | 29.6 |
| STAL ($s_{ref}$ = 8) | — | 27.7 |
| STAL ($s_{ref}$ = 32) | — | 28.3 |

For oriented boxes, the public code history of `ultralytics/utils/tal.py` shows (release tags checked; Appendix A, rows A20–A23):

| Ultralytics release | Candidate rule for oriented GT boxes |
|---|---|
| ≤ 8.4.7 (includes the YOLO26 release 8.4.0) | no size floor |
| 8.4.8 – 8.4.38 | sides < 8 → 16, but applied **in place** to the GT boxes (a bug fixed in 8.4.39) |
| 8.4.39 – 8.4.127 | sides < 8 → 16 on a copy (= the published rule) |
| ≥ 8.4.128 (current 8.4.174) | sides **< 16** → 16 on a copy |

Three consequences:
1. **"STAL" names at least three different rules**, and YOLO-OBB numbers obtained with different package versions are not comparable.
2. The floor sits in the base assigner, so YOLOv8- and YOLO11-OBB trained with today's package also use it [2].
3. **Nobody has measured what any of these rules does to tiny oriented objects.** That is the scientific gap this proposal targets.

---

## 3. Related work and positioning

**Label assignment for tiny objects (horizontal boxes).** These methods replace IoU with distribution distances or receptive-field priors. All are HBB methods, evaluated on AI-TOD or AI-TOD-v2:
- NWD-RKA models boxes as 2-D Gaussians and ranks anchors by a normalised Wasserstein distance [5].
- RFLA uses Gaussian effective-receptive-field priors with hierarchical assignment [6].
- GCD proposes a scale-invariant combined distance [7].

The gains are large on two-stage detectors but small on one-stage ones:
- RFLA lifts Faster R-CNN from 11.1 to 21.1 AP but RetinaNet only from 8.7 to 9.1 [6, p11].
- NWD-RKA lifts RetinaNet by 1.6 AP [5, p13].

YOLO is one-stage, so we expect small effect sizes and plan the statistics accordingly (§7.6).

**Oriented tiny objects.**
- DCFL is the state of the art on AI-TOD-R [3]. It models GT and priors as rotated Gaussians, $\Sigma = R(\theta)\,\mathrm{diag}(w^2/4,\,h^2/4)\,R(\theta)^{\top}$ [cited, 3, p9–10], with a coarse-to-fine candidate bag across adjacent pyramid levels. Its candidate region is therefore **already orientation- and aspect-aware**, inside an MMRotate (non-real-time) pipeline.
- SASM and CFA, both shape-aware assigners, are rows of the AI-TOD-R table (11.4 and 12.4 AP) [3, p6].

**Shape-aware candidate regions for oriented objects (no tiny-object dataset).**
- **EARL** contracts candidates to an inner ellipse following angle and aspect ratio. When a GT receives no sample, it falls back to the nearest unassigned anchor [8].
- **SARFA-Net** samples inside an angle- and aspect-following ellipse. It lowers IoU thresholds and enlarges the sampling range of small objects by ×1.1 [9].
- **RDCNet**, built on YOLOv8, selects candidates in the GT's rotated frame and adds a fallback for empty sets [10].
- Other works in this class were found only at abstract level and must be read before submission:
  - MFN-Net [11]: aspect-ratio filtering for small objects on SODA-A and AI-TOD;
  - aspect-ratio-aware dynamic assignment [12];
  - a JEIT 2026 article on tiny-object label assignment evaluated on AI-TOD-R [13] (content unverified; the publisher site was unreachable).

**YOLO-OBB numbers next to AI-TOD-R.** DIA-YOLO [4] trains a YOLOv11-OBB baseline and its own model on an oriented "AITOD" set and tabulates them against AI-TOD-R Table II. Its protocol differs from the benchmark's:
- 18,730 images instead of 28,036;
- RGB plus estimated-depth input;
- up to 815 epochs;
- no size bins;
- its text and table disagree (56.4 vs 56.1).

**Positioning (Table 1).** We claim no new mechanism class. Our distinguishing elements are:
1. the regime (oriented tiny objects, mean 10.6 px), where the enlargement factor is large;
2. the location (YOLO's point-in-box candidate step, where all published STAL variants act);
3. the method of evidence: a geometric account, pre-declared predictions and controlled, version-pinned comparisons.

*Table 1. Candidate-region designs along explicit axes. We will re-verify the abstract-only rows from full text before submission.*

| Work | Region shape | Small-object compensation | Detector family | Tiny OBB dataset? |
|---|---|---|---|---|
| TAL [14] | GT box | none | one-stage (TOOD/YOLO) | — |
| STAL-8 (paper) [1] | per-side floor (sides < 8 → 16) | floor | YOLO | no (COCO HBB) |
| STAL-16 (code ≥ 8.4.128) [2] | per-side floor (sides < 16 → 16) | floor | YOLO | no |
| EARL [8] | contracted ellipse | nearest-anchor fallback | anchor-free | no |
| SARFA-Net [9] | ellipse (angle, aspect) | ×1.1 range, adaptive threshold | anchor-based (S2A-Net) | no |
| RDCNet [10] | rotated-frame square ∩ GT | fallback | YOLOv8-based | no |
| DCFL [3] | rotated Gaussian bag, adjacent levels | dynamic prior | RetinaNet / S2A-Net / O-RCNN | **yes (AI-TOD-R)** |
| **OA-STAL v2 (ours)** | similarity-scaled rectangle with min area, short-side floor, conditional cap | min-area floor + conflict rule | YOLO11/26-OBB | **yes (AI-TOD-R)** |

---

## 4. Research gap

- **G1 — benchmark gap (narrow).** No protocol-matched benchmark of stock YOLO11/26-OBB on AI-TOD-R was found that has all four of:
  - the official evaluator (`AITODReval`, 1,500 detections per image, very-tiny/tiny/small/medium bins) [15];
  - per-class and per-bin results;
  - an in-house anchor baseline;
  - released prediction files.

  DIA-YOLO [4] is related but does not meet these conditions. *Negative evidence within the searched sources (Appendix A, row A30); the scan is repeated in week 13.*
- **G2 — STAL gap (main).** There is no published evaluation of STAL, in any of its versions, on oriented boxes or on a tiny-object dataset [1; 2]. Nor is there a published account of how its threshold changes candidate coverage.
- **G3 — mechanism gap (narrow).** Shape-aware regions exist (Table 1). However, none was evaluated in YOLO's point-in-box candidate step on a tiny oriented benchmark, against the STAL floor it would replace, with conflict effects measured.

---

## 5. Research questions and hypotheses

| RQ | Question | Hypothesis | Falsified if |
|---|---|---|---|
| **RQ1** benchmark | How do stock YOLO11-OBB and YOLO26-OBB perform on AI-TOD-R under a documented recipe, scored by the official evaluator, per size bin and per class? How do they compare with an in-house reproduced MMRotate baseline? | **H1:** a documented YOLO recipe produces a stable ranking across 3 seeds. $AP_{vt}$ remains the weakest bin for every model, as for all Table II rows [3, p6]. | Seed standard deviation exceeds the gap between models (ranking not stable). This is reported as a finding, not hidden. |
| **RQ2** diagnosis | How do candidate rules (no floor, STAL-8, STAL-16) change four quantities, by size bin × aspect-ratio bin × local density? (a) the zero-candidate rate; (b) candidates and positives per GT; (c) cross-GT conflicts; (d) where positives fall relative to the true box. Do these quantities predict per-GT recall? | **H2a:** offline label statistics match Proposition 1 (§6). **H2b:** STAL-16 removes zero-candidate cases for 8–16 px objects but raises conflicts in dense scenes. **H2c:** per-GT positives during training correlate with per-GT recall in the tiny bins. | (a) Measured candidate counts deviate from Proposition 1, indicating an anchor or stride setup we misread. (b) No association between positives and recall, in which case the count is the wrong diagnostic and we say so. |
| **RQ3** intervention | Does OA-STAL v2, alone or with a conflict rule, improve $AP_t$ / $AP_{vt}$ over STAL-16 at zero inference cost? Is any change explained by the RQ2 quantities predicted in advance? | **H3 (pre-declared, §7.5):** gains are concentrated in elongated classes (ship, bridge) and in side-by-side configurations. Near-square classes (storage-tank, swimming-pool) show no change. | No gain at all, or a gain that does not follow the predicted class/configuration pattern. In the second case the "shape" explanation is rejected even if AP rises. |
| **RQ4** generalisation | Do the RQ2 and RQ3 findings transfer to a second dataset, in proportion to the fraction of objects affected by the floors there? | **H4:** effect size scales with the fraction of GTs whose candidate rule differs between arms. | The effect is opposite in sign on the second dataset despite a comparable affected fraction. |

---

## 6. Analysis: what a candidate rule can and cannot change

**Setup.**
- YOLO's assigner tests anchor centres on strides $\mathcal{S}=\{8,16,32\}$. The default strides and the point-in-rotated-box test are in the code [2, L58–59, L392–425].
- A GT box is $g=(x,y,w,h,\theta)$ with $w \ge h$ (long-edge convention) [1, p9].
- A candidate rule maps $g$ to a region $\tilde{R}(g)$. Candidates are the anchor centres inside $\tilde{R}(g)$.

**Proposition 1 (expected candidate count) [derived].** If the region's position relative to the anchor lattice is uniformly random, then

$$
\mathbb{E}\left[N_{\mathrm{cand}}\right] \;=\; |\tilde{R}| \sum_{s \in \mathcal{S}} \frac{1}{s^{2}} \;=\; \frac{21}{1024}\,|\tilde{R}| \;\approx\; 0.0205\,|\tilde{R}|
$$

*Derivation.* On one level, anchor centres form a square lattice of spacing $s$. For any measurable region translated by a uniform random offset over one lattice cell, the expected number of lattice points inside equals $|\tilde{R}|/s^2$ (integrate the indicator over the offset; Fubini). Rotation does not change area. Summing over levels gives the result, because the assigner pools anchors across levels.

*Sanity checks.*
- **Dimensional:** px² · px⁻² = count.
- **Numerical:** an independent geometric simulation of the code's rotated point-in-box test (4,000 random positions and angles per box) gives 5.2–5.3 candidates for a 16×16 region (predicted 5.25) and 2.05–2.07 for a 10×10 box (predicted 2.05) (Appendix A, A12).
- **Degenerate case:** $|\tilde{R}| \to 0$ gives $\mathbb{E}[N] \to 0$.

**Corollary 1 (zero-candidate floor) [derived].** Since $N$ is a non-negative integer, $P(N \ge 1) \le \mathbb{E}[N]$, so $P(N=0) \ge 1 - 0.0205\,|\tilde{R}|$.
- Under plain TAL, a 4×4 px box therefore has $P(N=0) \ge 0.67$; the simulation gives 0.671.
- Any GT with area below about 49 px² can miss all anchors. This is the failure STAL was designed for [1, p7].

**Corollary 2 (equal area ⇒ equal expected count) [derived].** Two rules that map $g$ to regions of equal area yield the same expected number of candidates.
- STAL-16 maps any box with both sides < 16 to 16×16. A shape-preserving surrogate of area 16² therefore adds **no** candidates on average for such boxes.
- **Any effect of preserving shape must come from where candidates fall (inside or outside the true object, along which axis) and from conflicts with neighbouring objects. It cannot come from coverage.**
- RQ2 therefore measures placement and conflicts, not only counts. This corrects the mechanism stated in v1 of this proposal.

**Corollary 3 (the threshold matters more than the shape for the dominant bin) [derived].**
- In the AI-TOD family, the tiny bin [8,16] px holds 73.4% of objects in AI-TOD-v2 [5, p7]. AI-TOD-R's share is not stated and will be measured.
- For such objects STAL-8 changes nothing, while STAL-16 enlarges them to 16×16. For a 10×10 box the expected count is 2.05 vs 5.25, a factor of about 2.5.
- The paper-vs-current threshold is therefore a first-order variable for AI-TOD-R and must be controlled explicitly (§7.4).

**Prediction from geometry (to be checked offline in RQ2) [derived].** In the simulation, for a 4×12 px box with an identical neighbour 2 px away:
- **side-by-side neighbours:** the share of candidates also claimed by the neighbour falls from 0.63 (STAL-16) to 0.34 (similarity surrogate);
- **end-to-end neighbours:** it rises from 0.12 to 0.49.

Whether a shape-preserving surrogate reduces or increases conflicts on AI-TOD-R therefore depends on the **empirical distribution of neighbour configurations**. This is measurable from labels **before any training** and fixes the sign of H3 in advance (§7.5).

---

## 7. Method

### 7.1 OA-STAL v2: a shape-preserving minimum-area surrogate [design]

**Parameters** (all explicit and stride-independent, so that adding a P2 head cannot change them; in the current code, `stride_val = stride[1]` becomes 8 with a P2 head [2, L59]):
- trigger $\tau \in \{\text{side}, \text{area}\}$ with threshold $t$;
- target size $s_{ref}$;
- short-side floor $s_{flo}$;
- long-side cap factor $c$.

**Definition.** For $g=(x,y,w,h,\theta)$ with $w \ge h$:

$$
\text{triggered} \iff \begin{cases} h < t & \text{(side trigger)} \\ \sqrt{wh} < t & \text{(area trigger)} \end{cases}
$$

If triggered:

$$
k=\max\!\left(1,\ \frac{s_{ref}}{\sqrt{wh}}\right),\qquad
\tilde h=\max\!\left(k h,\ s_{flo},\ h\right),\qquad
\tilde w=\max\!\left(\min\!\left(k w,\ \max(w,\ c\,s_{ref})\right),\ w\right)
$$

and $\tilde{R}=(x,y,\tilde w,\tilde h,\theta)$. Otherwise $\tilde{R}=g$. As in STAL, $\tilde{R}$ is used **only** in the candidate mask. Scoring, targets and regression use $g$ [1, p8].

**Default parameters for the primary arm:** area trigger, $t = s_{ref} = 16$, $s_{flo} = 8$, $c = 2$. They are chosen to match the area of STAL-16 (Corollary 2) and are tuned only on the validation split (§7.3).

**Properties [derived] (each checked by direct substitution).**
- **P1 — containment:** $g \subseteq \tilde{R}$ (no side ever shrinks). Hence the candidate set of OA-STAL contains that of TAL, and the zero-candidate rate is never worse than TAL. This repairs the v1 defect, where an unconditional cap shrank long thin boxes (simulated zero-candidate rate 10.2% vs 0.4% for TAL on a 5×60 box, Appendix A, A12).
- **P2 — identity:** if not triggered, $\tilde{R} = g$, which is TAL. No unconditional cap.
- **P3 — square reduction:** for $w = h = d < \min(t, s_{ref})$, $\tilde{R}$ is $s_{ref}\times s_{ref}$, identical to a per-side floor with the same threshold and target.
- **P4 — exact shape preservation:** the aspect ratio $r = w/h$ is preserved iff $k h \ge s_{flo}$ and $k w \le c\,s_{ref}$, i.e. iff $r \le (s_{ref}/s_{flo})^2$ and $r \le c^2$. With the defaults, $r \le 4$. Beyond that, the floor and cap engage: a deliberate trade-off that protects thin objects. *Check:* $k h = s_{ref}/\sqrt{r}$ and $k w = s_{ref}\sqrt{r}$.
- **P5 — area:** when preserved, $|\tilde R| = s_{ref}^2$, so by Corollary 2 the expected candidate count equals STAL-16 for boxes with both sides < 16. For boxes with one side ≥ 16 and $\sqrt{wh} < 16$, OA-STAL gives *fewer* candidates than STAL-16 (which enlarges the short side to 16 along the full long side). This is a known cost, measured in RQ2.
- **P6 — zero inference cost:** training-only. Parameters, FLOPs and latency are unchanged.

### 7.2 Conflict resolution [design]

An anchor inside several regions is currently assigned to the GT with the highest ProbIoU between that anchor's prediction and each GT [2, L365–371]. ProbIoU is nearly rotation-invariant for near-square boxes [1, p9]. We test two alternatives as separate arms:
- **C-inside:** if the anchor lies inside the *original* box of exactly one GT, that GT wins; otherwise the default rule applies.
- **C-smaller:** the smaller GT wins, following RFLA's rule "the occluded sample will be assigned to the smaller gt" [6, p9].

### 7.3 Implementation sketch [design, untested]

All arms run in one pinned fork of Ultralytics (commit recorded). The change replaces the width/height block of `RotatedTaskAlignedAssigner.select_candidates_in_gts` (current code [2, L404–409]) with a mode switch:

```python
# [design] untested sketch; gt: (b, n, 5) = (x, y, w, h, theta), long-edge so w >= h
def surrogate(gt, mode, t, s_ref, s_flo, cap):
    g = gt.clone()                                   # original gt is never modified
    w, h = g[..., 2].clone(), g[..., 3].clone()
    if mode == "none":                               # plain TAL
        return g
    if mode == "per_side":                           # STAL-8 (t=8) or STAL-16 (t=16)
        g[..., 2] = torch.where(w < t, torch.full_like(w, s_ref), w)
        g[..., 3] = torch.where(h < t, torch.full_like(h, s_ref), h)
        return g
    # "similarity" (OA-STAL v2)
    trig = (h < t) if TRIGGER == "side" else (torch.sqrt(w * h) < t)
    k = torch.clamp(s_ref / torch.sqrt(w * h).clamp(min=1e-6), min=1.0)
    h_new = torch.maximum(torch.maximum(k * h, torch.full_like(h, s_flo)), h)
    w_new = torch.maximum(torch.minimum(k * w, torch.maximum(w, torch.full_like(w, cap * s_ref))), w)
    g[..., 2] = torch.where(trig, w_new, w)
    g[..., 3] = torch.where(trig, h_new, h)
    return g
```

Unit tests, written before any training, check P1–P5 on synthetic boxes. Diagnostic hooks log per-GT counts for both YOLO26 branches (one-to-many `tal_topk = 10`; one-to-one `tal_topk = 7`, `topk2 = 1` [2, loss.py]).

### 7.4 Arms

| Arm | Candidate rule | Conflict rule | Purpose |
|---|---|---|---|
| A0 | none (TAL) | default | lower bound; zero-candidate failure |
| A1 | per-side, t = 8 → 16 (STAL-8) | default | published rule |
| A2 | per-side, t = 16 → 16 (STAL-16) | default | current rule; **primary comparator** |
| A3 | TAL + nearest-anchor fallback for empty GTs | default | EARL/RDCNet-style cheap control [8; 10] |
| A4 | similarity, area trigger 16 (OA-STAL v2) | default | **primary intervention** |
| A5 | similarity, side trigger 16 | default | isolates trigger vs shape (A5 vs A2) |
| A6 | OA-STAL v2 | C-inside | conflict effect |
| A7 | STAL-16 | C-inside | conflict effect without shape change |
| **A8** *[v2.1]* | per-side floor, $t = s_{ref} = \sqrt{2}\,s_{\min} \approx 11.31$ | default | coverage-minimal floor; **part of the primary factorial** (A0/A1/A2/A8) |

*[v2.1]* A5, A6 and A7 are cut from the 4-week plan; conflicts are measured through online logs and per-GT recall regression instead.

**Primary comparison (pre-declared):** A4 vs A2 on $AP_t$ and $AP_{vt}$. All other contrasts are secondary and reported as such. A Gaussian candidate region in the spirit of DCFL [3] is added if budget allows. Otherwise its absence is stated as a limitation.

---

## 8. Experimental design

### 8.1 Data

- **AI-TOD-R:** the official release provides labels (`labels.zip`). Images are rebuilt from AI-TOD's route, which requires registered xView access [15; 16] (§10).
- **Splits:** the official configuration uses the test split as its validation split [15]. We therefore carve a **fixed validation split** from trainval (10% of images, fixed seed; grouped by source tile if file names allow). All tuning happens there. The test split is touched once per final arm.
- **Second dataset (RQ4):** SODA-A (2,513 images, 872,069 instances, 9 classes; split ≈ 40:25:35) [17].
  - Its download link redirected to a login page on 2026-10-08 (§10).
  - Pre-declared fallback: DOTA-v2.0 train → val, the protocol DCFL used for its own ablations [3, p14].
  - SODA's protocol resizes 800×800 crops to 1200×1200 [17, p13]. This lifts many objects above the 8/16 px triggers, so we report the fraction of GTs affected at the actual input size.
- **Pretraining:** AI-TOD is partly built from DOTA images [5, p5], and the released YOLO26-OBB checkpoints are trained on DOTA-v1 [2, docs]. To avoid leakage, **all reported YOLO rows start from COCO detection weights.** DOTA-OBB initialisation, if used at all, is reported separately.

### 8.2 Evaluation protocol

- **Scoring:** predictions are exported to DOTA-format text and scored **only** with the official `AITODReval`. Settings: IoU 0.50:0.05:0.95, `maxDets = 1500`, area bins very tiny [2², 8²], tiny [8², 16²], small [16², 32²], medium [32², 64²] [15].
- **Detection cap:** Ultralytics defaults to `max_det = 300` [2]. We set `max_det = 12,000` *[v2.1]* — AITODReval's 1,500 cap applies per (image, class), and AI-TOD-R has 8 classes — including the end-to-end head, and confidence 0.001.
- **Converter validation:** we reproduce one MMRotate row of Table II (RetinaNet-O, 1×) from the official configuration [15]. Pre-declared tolerance: within ±1.0 AP of 7.3 AP [3, p6]; otherwise the evaluator setup is investigated before any comparison is made.
- **Reporting:** AP, AP50, AP75, the four size-bin APs, per-class AP, and parameters/FLOPs/latency measured on one GPU. YOLO26 rows report the end-to-end (one-to-one) and non-end-to-end branches separately.

### 8.3 RQ1: benchmark

- **Models:** YOLO11s-OBB, YOLO26n-OBB and YOLO26s-OBB at input 800. YOLOv8 is dropped as redundant with YOLO11 (both share the assigner [2]).
- **Two recipes, never mixed in one ranking:**
  - **R-short:** flip-only, short fixed schedule. Remaining differences from Table II are listed in a table: pretraining, optimiser, EMA, head design.
  - **R-native:** the documented Ultralytics recipe.
- **Seeds:** three seeds for YOLO26n in both recipes; one seed for the larger models (labelled as such).

### 8.4 RQ2: diagnosis

**Offline (labels only, no GPU, week 3).** For every GT in AI-TOD-R trainval:
- size bin, aspect ratio and class;
- nearest-neighbour distance (in units of $s_{ref}$) and neighbour configuration (side-by-side vs end-to-end, by angle between long axes and the centre-line);
- under each rule A0–A7: candidate count, zero-candidate flag, candidates shared with neighbours, and the fraction of candidates outside the true box.

This tests H2a against Proposition 1 and **fixes the sign of H3 before training** (§8.5).

**Online (during training).** Logged every N iterations for both YOLO26 branches:
- positives per GT, post-conflict zero-positive rate, positives lost to neighbours;
- soft-target values;
- the fraction of positives needing a negative distance target (clamped by `rbox2dist`, [2, L537–552]).

Per-GT recall on the validation split is then related to these quantities (H2c) with a logistic model stratified by size bin.

### 8.5 Pre-registration (written in week 3, before any RQ3 training)

A dated file `experiments/preregistration.md` will fix:
- the primary comparison (A4 vs A2, $AP_t$ and $AP_{vt}$);
- the predicted sign per class and per configuration, derived from the offline statistics;
- the minimal effect size of interest, set to the seed standard deviation measured in RQ1 (no number is assumed now);
- the analysis code.

Deviations are logged with reasons.

### 8.6 Statistics

- Three seeds per arm.
- Report mean ± standard deviation.
- Primary contrast *[v2.1: the A0/A1/A2/A8 factorial]*: paired, **scene-clustered** bootstrap *[v2.1; was image-level]* (10,000 resamples) 95% confidence interval for $\Delta AP_t$ and $\Delta AP_{vt}$, pooled over seeds.
- A difference is called an improvement only if the interval excludes 0 **and** the predicted class/configuration pattern holds (H3).
- Secondary contrasts are reported without significance claims.

### 8.7 RQ4: generalisation

Run A2 and A4 (and A0 for scale) with three seeds on the second dataset under a reduced, pre-declared protocol: fixed crop subset, fixed epochs, internal baseline. Plot the effect against the fraction of GTs whose rule differs between arms (H4).

---

## 9. Compute plan

**Resources (official pages, read 2026-10-08) [18]:**
- Kaggle Notebooks: one free P100 or 2×T4; a weekly GPU quota of "30 hours or sometimes higher depending on demand"; 12-hour sessions; 4 CPU cores; 29 GB RAM; 20 GB persistent output.
- Overflow: Modal (≤ US$100, as in v1), e.g. L40S at US$1.95 per GPU-hour plus CPU/RAM (rates read 2026-10-01; log #35–36 of `logs/research-log.md`).

**Cost model [estimate, no measured throughput exists].**

$$
\text{GPU-hours per run} = \frac{N_{img}\times E}{r \times 3600}
$$

- $N_{img}$ = number of training images (AI-TOD-R per-split counts are not stated [3]; counted after download);
- $E$ = epochs;
- $r$ = measured images per second.

Illustration only: with $N_{img} = 14{,}000$ (estimate from AI-TOD-v2's instance split, to be replaced) and $E = 100$:

| r (img/s) | GPU-h per run | Note |
|---|---|---|
| 100 | 3.9 | |
| 50 | 7.8 | |
| 25 | 15.6 | needs resume across two 12-h sessions |

**Run inventory and shrink rule.**
- RQ1 needs about 9 runs, RQ3 about 24 (8 arms × 3 seeds, YOLO26n, short schedule), RQ4 about 9, plus 2 pilots and 1 MMRotate reproduction.
- Using YOLO26n with short schedules for ablations, and three seeds only where pre-declared, is what makes the plan fit 30 GPU-h/week.
- Training is resume-safe: `last.pt` is saved every epoch to `/kaggle/working`, and sessions are chained by attaching the previous output.

**Go/no-go (end of week 2):** if the pilot throughput implies more than 10 weeks of quota for the core plan (RQ1 + A0/A2/A4 × 3 seeds), we cut in this order:
1. RQ4 to A2/A4 only;
2. A5;
3. A6/A7;

and record the cut in the log.

---

## 10. Feasibility gate (rule: a proposal is runnable or says it is not)

| Item | Status 2026-10-08 | Evidence | Fallback |
|---|---|---|---|
| Data | Labels public (`labels.zip`). Images need xView registration and AI-TOD's generation script. Not yet tested end-to-end. | [15; 16] | If xView access fails within 2 weeks: DOTA-v2.0 train → val (tiny subset), with the claim scope reduced accordingly. |
| Evaluator | `AITODReval` present in the official repository; not yet run by us | [15] | none (blocking) |
| Compute | Kaggle limits verified; throughput unmeasured | [18] | Modal ≤ US$100; smaller model and fewer arms |
| Baseline | Published Table II exists [3]; in-house reproduction pending (§8.2) | [3] | Compare only with internal baselines if the reproduction misses tolerance |
| Dependencies | Ultralytics 8.4.174 (2026-10-06), pinned fork; AI-TOD-R code (Apache-2.0); SODA-A access unverified | [2; 15; 17] | Fork frozen at a recorded commit; DOTA-v2 for RQ4 |

**Verdict: not runnable as stated** until the Phase-0 items (xView access, evaluator run, pilot throughput, converter validation) pass.

---

## 11. Timeline (14 weeks)

> *[v2.1]* **Superseded** by the 4-week plan in `ROADMAP.md` (11/10 → 08/11/2026, gates 0–5). The table below is kept for the record.

| Week | Work | Gate / deliverable |
|---|---|---|
| 1 | xView registration; rebuild AI-TOD-R images; pin the fork; unit tests for the surrogates (P1–P5) | Data present; tests pass |
| 2 | Kaggle pilots (P100, 2×T4); evaluator and converter; MMRotate RetinaNet-O reproduction | **Go/no-go** (§9); converter within tolerance |
| 3 | Offline RQ2 label analysis; pre-registration | `preregistration.md` dated |
| 4–6 | RQ1 runs | Benchmark table |
| 6–9 | RQ3 arms A0–A7 × 3 seeds; online diagnostics | Ablation table + CIs |
| 10–11 | RQ4 on the second dataset | Transfer table |
| 12 | Analysis: RQ2–RQ3 links; error analysis per class/configuration | Figures |
| 13 | Novelty re-scan; read the full texts of [11–13]; write | Draft |
| 14 | Internal review; release of code, configs, prediction files | Submission package |

---

## 12. Risks, fallbacks and what remains publishable

| Risk | Likelihood (judgement) | Mitigation / fallback |
|---|---|---|
| OA-STAL v2 does not beat STAL-16 | medium–high: Corollary 2 implies at most second-order effects; one-stage assignment gains in the literature are ≤ 1.6 AP [5; 6] | The paper becomes a benchmark-and-diagnosis study. It stays publishable only with a non-obvious, mechanism-backed finding (e.g. the 8 vs 16 threshold trades very tiny against elongated tiny objects, or floors create measurable conflicts in dense scenes). A plain leaderboard is not enough. |
| Effects within seed noise | medium | 3 seeds, bootstrap CIs, pre-declared minimal effect; report nulls |
| xView / SODA-A access fails | unknown | Pre-declared DOTA-v2 fallback; reduced claim scope |
| Converter or evaluator mismatch | medium | Reproduce Table II row before any comparison (§8.2) |
| Version drift in Ultralytics | certain (already happened) | One frozen fork; all arms as explicit parameters |
| Closer prior work appears (e.g. [13]) | unknown | Week-13 re-scan; position or narrow the claims; never "first" |
| Quota insufficient | medium | Shrink rule (§9); Modal overflow |

---

## 13. Expected contributions and venue claim

**Planned contributions** (no performance numbers are promised):
1. An evaluator-matched, size-binned benchmark of YOLO11/26-OBB on AI-TOD-R, with released prediction files and converter.
2. A version-controlled account of STAL for oriented boxes: the dated rule history, a geometric analysis (Proposition 1 and Corollaries) and an empirical diagnosis of coverage, placement and conflicts.
3. A training-only, zero-inference-cost surrogate and conflict rule, evaluated against pre-declared predictions.
4. A reproducibility package: pinned fork, configurations and seeds.

### Venue Claim Card
- **Proposal:** C-3 revised. Evaluator-matched YOLO-OBB benchmark on AI-TOD-R; version-controlled STAL diagnosis with a geometric account; OA-STAL v2 + conflict rule against STAL-16 with pre-declared predictions; a second dataset.
- **Novelty tier:** **T1** (an assignment/training-recipe change; the benchmark and the diagnosis do not raise the tier). Shape-aware regions exist [8–10]; the novelty is regime, location and evidence quality, not mechanism class.
- **Venue band:** Q4 journal or Scopus-indexed conference, **conditional on:**
  1. RQ1 framed narrowly, with DIA-YOLO cited;
  2. `AITODReval` with `maxDets = 1500` and a validated converter;
  3. one pinned fork with explicit parameters;
  4. a validation split and ≥ 3 seeds with confidence intervals;
  5. data access and pilot confirmed;
  6. the full texts of [11–13] read and positioned.

  **Q3 only if,** additionally, the primary contrast (A4 vs A2) has a confidence interval excluding 0 and the predicted pattern on **two** datasets. Q1/Q2: not defensible (T1).
- **Downgrade triggers:**
  - closer prior work found (e.g. [13] already evaluates YOLO assignment on AI-TOD-R);
  - no mechanism-backed finding in RQ2;
  - only one dataset;
  - the converter fails tolerance.
- **Confidence:** medium for the benchmark and diagnosis (gaps checked on full text and code); low for the intervention (Corollary 2 bounds its mechanism).
- **Ledger:** C-10, REVISION of C-3. Cause: new evidence (DIA-YOLO; the STAL version history; SARFA-Net/RDCNet; geometric defects of OA-STAL v1).
- *[v2.1]* **Superseded by C-11** (2026-10-13): same tier and band; primary contrast changed to the A0/A1/A2/A8 factorial, `max_det = 12,000`, scene-clustered bootstrap, MCSA/CDCEDet added to the reading list. Q3 only if the primary contrast CI excludes 0 with the predicted density/configuration pattern on 2 source-independent datasets; Q2/Q1 not defensible.

---

## 14. Ethics, licences and data handling

- **Licences:** AI-TOD is CC BY-NC-SA 4.0 [16]. No dataset licence is stated for AI-TOD-R [3; 15]. SODA-A is listed as CC BY-NC 4.0 on its project page, while its paper's text and footnote disagree [17].
- **Use:** non-commercial research only. Kaggle copies of the data are kept **private**, and no images are redistributed.
- **xView:** terms accepted at registration [16].
- **Attribution:** code borrowed from Ultralytics (AGPL-3.0, per its file headers) and AI-TOD-R (Apache-2.0) is attributed, and the fork keeps their licences.

---

## 15. Anticipated reviewer objections (self-review) and our answers

| # | Objection | Answer in this design |
|---|---|---|
| 1 | "OA-STAL is a parametric variant of EARL/SARFA-Net/RDCNet." | Agreed on mechanism class (§3, Table 1). The claim rests on regime, location and evidence: Corollary 2 and the pre-declared class/configuration prediction (§8.5). Cheap controls from those works (fallback, A3) are run in the same code. |
| 2 | "YOLO on AI-TOD-R exists (DIA-YOLO)." | Cited. G1 is narrowed to an evaluator-matched, size-binned benchmark (§4). No "first" claims. |
| 3 | "Your 'protocol-matched' YOLO is not MMRotate's protocol." | Called R-short, with a difference table; in-house MMRotate reproduction; R-short and R-native never mixed (§8.3). |
| 4 | "Ultralytics' validator differs from AITODReval." | Only `AITODReval` is used, with 1,500 detections; the converter is validated (§8.2). |
| 5 | "STAL is a moving target; P2 changes it." | Version history documented (§2.2); one fork; stride-independent parameters (§7.1). |
| 6 | "One seed; test-set tuning." | Validation split; 3 seeds; bootstrap CIs; pre-registration (§8.1, 8.5, 8.6). |
| 7 | "Counting positives is descriptive." | Placement, conflicts and both branches are measured and linked to per-GT recall (§8.4); an assigner-only intervention tests causality (RQ3). |
| 8 | "Generalisation rests on an inaccessible dataset." | Pre-declared fallback; effect plotted against the affected fraction (§8.7). |
| 9 | "Compute is unrealistic on Kaggle." | GPU-hour model, pilot, go/no-go and shrink rule (§9). |
| 10 | "DOTA-pretrained weights may leak test imagery." | COCO initialisation for all reported rows (§8.1). |
| 11 | "Expected counts are equal, so why should shape matter?" | We say so ourselves (Corollary 2). The hypothesis is about placement and conflicts, fixed in sign from label statistics before training. A null result is reported as a result. |

---

## 16. References

Verification status: DOI = checked against Crossref (`scripts/t07-slr/data/p7_crossref_verify.csv` or a direct query on 2026-10-08); arXiv = arXiv API record; URL = official page read on the stated date.

[1] G. Jocher et al., "Ultralytics YOLO26: Unified Real-Time End-to-End Vision Models," [arXiv:2606.03748v1](https://arxiv.org/abs/2606.03748), 2026. *(preprint; full text read)*
[2] Ultralytics, `ultralytics` Python package and repository, release 8.4.174 (2026-10-06); `ultralytics/utils/tal.py` (main, last change 2026-09-27; tags v8.4.38/39/127/128 checked 2026-10-08). <https://github.com/ultralytics/ultralytics>
[3] C. Xu et al., "Oriented Tiny Object Detection: A Dataset, Benchmark, and Dynamic Unbiased Learning," IEEE TPAMI, 2025/2026. DOI: [10.1109/tpami.2025.3634161](https://doi.org/10.1109/tpami.2025.3634161). *(read as [arXiv:2412.11582v1](https://arxiv.org/abs/2412.11582))*
[4] Kim and Park, "DIA-YOLO: Diffusion-Based Involution Attention YOLO for Overhead Imagery," IEEE Access, vol. 13, 2025. DOI: [10.1109/ACCESS.2025.3603214](https://doi.org/10.1109/ACCESS.2025.3603214). *(full text read)*
[5] C. Xu et al., "Detecting tiny objects in aerial images: A normalized Wasserstein distance and a new benchmark," ISPRS J. Photogramm. Remote Sens., vol. 190, pp. 79–93, 2022. DOI: [10.1016/j.isprsjprs.2022.06.002](https://doi.org/10.1016/j.isprsjprs.2022.06.002).
[6] C. Xu et al., "RFLA: Gaussian Receptive Field Based Label Assignment for Tiny Object Detection," ECCV 2022 (LNCS). DOI: [10.1007/978-3-031-20077-9_31](https://doi.org/10.1007/978-3-031-20077-9_31).
[7] Guan et al., "Gaussian Combined Distance: A Generic Metric for Object Detection," IEEE GRSL, 2025. DOI: [10.1109/lgrs.2025.3531970](https://doi.org/10.1109/lgrs.2025.3531970). *(read as [arXiv:2510.27649v1](https://arxiv.org/abs/2510.27649))*
[8] "EARL: Elliptical Distribution aided Adaptive Rotation Label Assignment," IEEE TGRS, vol. 61, 2023; [arXiv:2301.05856](https://arxiv.org/abs/2301.05856). *(full text read)*
[9] "SARFA-Net: Shape-Aware Label Assignment and Refined Feature Alignment for Arbitrary-Oriented Object Detection," IEEE JSTARS, vol. 18, 2025. DOI: [10.1109/JSTARS.2025.3532039](https://doi.org/10.1109/JSTARS.2025.3532039). *(full text read)*
[10] "RDCNet: Rotation-Aware Feature Representation and Aspect-Adaptive Label Assignment," IEEE JSTARS, vol. 19, 2026. DOI: [10.1109/JSTARS.2026.3687230](https://doi.org/10.1109/JSTARS.2026.3687230). *(full text read)*
[11] "MFN-Net: multi-scale adaptive fusion and flexible label assignment for small object detection in RS images," Remote Sensing Letters, 17 (2026) 801–813. DOI: [10.1080/2150704X.2026.2667240](https://doi.org/10.1080/2150704X.2026.2667240). *(abstract only)*
[12] "Aspect-Ratio Aware Dynamic Label Assignment for Oriented Object Detection," IEEE GRSL, 21, 2024. DOI: [10.1109/LGRS.2024.3432810](https://doi.org/10.1109/LGRS.2024.3432810). *(abstract only)*
[13] "Cross-Domain Collaborative Enhancement for Tiny Object Detection in Remote Sensing Images," J. Electronics & Information Technology, 2026. DOI: [10.11999/JEIT260317](https://doi.org/10.11999/JEIT260317). *(DOI handle verified; content unverified)*
[14] C. Feng et al., "TOOD: Task-aligned One-stage Object Detection," ICCV 2021. DOI: [10.1109/iccv48922.2021.00349](https://doi.org/10.1109/iccv48922.2021.00349).
[15] AI-TOD-R project page and repository (`AITODReval`, configs), <https://chasel-tsui.github.io/AI-TOD-R/> and <https://github.com/Chasel-Tsui/AI-TOD-R>, read 2026-10-08.
[16] J. Wang et al., "Tiny Object Detection in Aerial Images," ICPR 2020 (2021). DOI: 10.1109/ICPR48806.2021.9413340; AI-TOD repository (licence, image-generation route) and xView registration page, read 2026-10-08.
[17] G. Cheng et al., "Towards Large-Scale Small Object Detection: Survey and Benchmarks," IEEE TPAMI, 2023. DOI: 10.1109/tpami.2023.3290594; SODA project page read 2026-10-08.
[18] Kaggle documentation: Notebooks, Efficient GPU Usage Tips, Datasets, <https://www.kaggle.com/docs>, read 2026-10-08.
[19] J. Ding et al., "Object Detection in Aerial Images: A Large-Scale Benchmark and Challenges," IEEE TPAMI, 2022. DOI: [10.1109/tpami.2021.3117983](https://doi.org/10.1109/tpami.2021.3117983).
[20] J. M. Llerena et al., "Gaussian Bounding Boxes and Probabilistic Intersection-over-Union for Object Detection," [arXiv:2106.06072](https://arxiv.org/abs/2106.06072), 2021. *(ProbIoU; arXiv record verified)*
[21] C. Lyu et al., "RTMDet: An Empirical Study of Designing Real-Time Object Detectors," [arXiv:2212.07784](https://arxiv.org/abs/2212.07784), 2022. *(arXiv record verified; optional RTMDet-R baseline)*

---

## Appendix A. Evidence trace

All paths are relative to `NCKH/`. Page = physical PDF page.

| ID | Claim used in the proposal | Source (file, page / line) |
|---|---|---|
| A1 | AI-TOD-R: 28,036 images, 752,460 OBB, 8 classes, 10.6 ± 4.9 px; "most objects … <16×16" | `papers/_text/Xu2024-AI-TOD-R.txt`, p3 Table I, p4 §III-B |
| A2 | Density "over 2000 objects … most images featuring over 100 objects" | same, p4–5 |
| A3 | Table II rows (DCFL 17.5/49.6/6.5 APvt; O-RCNN 11.2 AP / 0.6 APvt; SASM 11.4; CFA 12.4; RetinaNet-O 7.3) | same, p6 Table II |
| A4 | "tiny-scale objects receive significantly fewer positive samples …"; "stride … at least 8 pixels" | same, p8 §IV-D |
| A5 | DCFL Gaussian Σ(w, h, θ); candidate bag across adjacent levels | same, p9–10 §V-B/C |
| A6 | STAL definition, s_min = 8, s_ref = 16, "modifies only the candidate-selection mask" | `papers/_text/Jocher2026-YOLO26.txt`, p7–8 Eq. 4–6; p11 §4.1 |
| A7 | STAL ablation on COCO (Tables 2, 6) | same, p12–13 |
| A8 | Long-edge angle convention; ProbIoU insensitivity for near-square boxes | same, p9 §3.4.3 |
| A9 | Code: `stride_val = stride[1]`; rotated floor on a clone; ProbIoU; conflict rule | `papers/_text/ultralytics_tal_main_2026-10-01.py` L58–59, L365–371, L388–425 |
| A10 | Bins [2,8]/[8,16]/[16,32]/[32,64]; tiny share 73.4% (AI-TOD-v2) | `scripts/t07-slr/data/txt_cache/R2318.txt` p7 §3.2 |
| A11 | RFLA and NWD-RKA gains; small one-stage gains; RFLA conflict rule | `R2391.txt` p9, p11 Table 5; `R2318.txt` p11 Table 4, p13 §6.3.1 |
| A12 | Geometric simulation of candidate rules (counts, zero-candidate rate, conflicts) | `notes/t07-c3-evidence-dossier.md` §7.1; `scripts/t07-slr/data/_tmp_dossierA/sim_candidates.py` |
| A13 | SODA-A statistics, protocol, licence inconsistency | `R2256.txt` p1, p10, p13, p22 |
| A20–A23 | STAL version history (8.4.0 / 8.4.8 / 8.4.39 / 8.4.128) | `notes/t07-c3-novelty-rescan.md` §B.2; tags re-checked by admin 2026-10-08 (`logs/t07-slr-log.md`) |
| A24 | YOLO26 loss top-k (o2m 10; o2o 7, topk2 1); `max_det: 300` default | `notes/t07-c3-novelty-rescan.md` §B.2 |
| A25 | `labels.zip` only; xView route; `AITODReval` maxDets 1500 and bins; val = test in config | same, §B.3 |
| A26 | Kaggle limits | same, §B.1 |
| A27 | DIA-YOLO protocol (18,730 images, RGBD, 12/40/815 epochs, no bins, 56.1 vs 56.4) | same, §A.3 K1; `notes/t07-c3-evidence-dossier.md` §7.2 |
| A28 | EARL, SARFA-Net, RDCNet mechanisms | `notes/t07-c3-novelty-rescan.md` §A.3 K3–K5 |
| A29 | AI-TOD built partly from DOTA | `R2318.txt` p5 §3 (via `notes/t07-c3-novelty-rescan.md` §B.3) |
| A30 | Scope and limits of the novelty scan | `notes/t07-c3-novelty-rescan.md` §0 query log, §A.5 |

## Appendix B. Glossary (English — Vietnamese)

| English | Tiếng Việt | Short explanation |
|---|---|---|
| label assignment | gán mẫu huấn luyện | Choosing which anchor points learn which object |
| candidate region / surrogate | vùng ứng viên / hộp thay thế | Geometry used only to pick candidate anchors |
| positive sample | mẫu dương | An anchor point trained to predict a given object |
| zero-candidate rate | tỉ lệ không có ứng viên | Share of GT boxes with no anchor centre inside their candidate region |
| conflict resolution | giải quyết xung đột gán | Rule deciding which GT an anchor shared by several GTs belongs to |
| STAL-8 / STAL-16 | STAL ngưỡng 8 / ngưỡng 16 | Published rule vs current-code rule |
| OA-STAL v2 | — | Our shape-preserving minimum-area surrogate (§7.1) |
| pre-registration | đăng ký trước giả thuyết | Fixing predictions and analysis before running the experiment |
| bootstrap CI | khoảng tin cậy bootstrap | Confidence interval from resampling images |
| T1 tier | mức mới T1 | Internal rubric: training-recipe-level change |
