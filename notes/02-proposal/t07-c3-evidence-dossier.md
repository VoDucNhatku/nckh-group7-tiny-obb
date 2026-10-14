# t07 / C-3 — Evidence dossier (oriented tiny objects, YOLO-OBB, STAL, OA-STAL)

- **Date:** 2026-10-08
- **Author role:** sub-agent A — evidence dossier (input for the admin's English proposal; no proposal text, no venue or novelty-tier claims)
- **Proposal checked:** `notes/99-archive/t07-proposal.md` (2026-10-01) and `notes/05-venue-direction/synthesize-gaps-t07-q4-priority.md` §3, §7
- **Rules:** local sources only, no web. Every fact = exact value or short quote + [pid, file, page §]. Page numbers are **physical PDF pages**; for R1899 and R0879 the printed page number equals the physical page (checked with PyMuPDF). "The authors report" = stated in the source; **[inference]** = my reasoning; **[derived]** = computed by me from the code or from geometry (script given); "not stated in the source" = searched for and absent.

## Sources

| Key | pid | Text file (relative to `NCKH/`) | Version / PDF |
|---|---|---|---|
| AITODR | R1899 | `papers/_text/Xu2024-AI-TOD-R.txt` | `papers/Xu2024-AI-TOD-R-oriented-tiny.pdf`, arXiv 2412.11582v1, 18 pp. |
| YOLO26 | R0879 / W01 | `papers/_text/Jocher2026-YOLO26.txt` | `papers/Jocher2026-YOLO26.pdf`, arXiv 2606.03748v1, 31 pp. |
| CODE | — | `papers/_text/ultralytics_tal_main_2026-10-01.py` | `ultralytics/utils/tal.py`, branch main, fetched 2026-10-01 (research-log #26: last commit 2026-09-27) |
| NWD | R2318 | `scripts/t07-slr/data/txt_cache/R2318.txt` | `pdf_cache/R2318.pdf`, ISPRS J. P&RS 190:79–93 (2022), 18 pp. |
| RFLA | R2391 | `scripts/t07-slr/data/txt_cache/R2391.txt` | `pdf_cache/R2391.pdf`, LNCS-format version, 18 pp. |
| GCD | R1269 | `scripts/t07-slr/data/txt_cache/R1269.txt` (path from `shard_S8.json`) | `pdf_cache/R1269.pdf`, arXiv 2510.27649v1, 5 pp. (shard metadata: IEEE GRSL 2025) |
| DN-TOD | W12 | `scripts/t07-slr/data/txt_cache/2401.08056v1.txt` | `pdf_cache/2401.08056v1.pdf`, arXiv v1, 13 pp. ("Preprint submitted to Elsevier") |
| SODA | R2256 | `scripts/t07-slr/data/txt_cache/R2256.txt` (path from `shard_S10.json`) | `pdf_cache/R2256.pdf`, arXiv 2207.14096 (shard metadata: TPAMI 2023), 24 pp. |
| DIA-YOLO | no pid | `scripts/t07-slr/data/_tmp_scanB/raw/dia_yolo.txt` + rendered pages `dia_p10.png`, `dia_p11.png` | IEEE Access vol. 13, 2025 (printed pp. 150574–); found in another agent's scan folder, **not in the SLR corpus** |
| Notes | — | `notes/04-slr/_local/t07-slr-watchlist.md`, `t07-slr-matrix.md`, `t07-paper-overviews.md`, `t07-slr-cards-S6…S13.md`, `t07-slr-benchmark.csv` | distilled notes, reused, not re-derived |
| SIM | — | `scripts/t07-slr/data/_tmp_dossierA/sim_candidates.py` → `sim_candidates_out.txt` | my geometric replication of the code's rotated candidate test, **[derived]** |

---

## 1. AI-TOD-R (R1899)

### 1.1 Dataset facts

| Item | Value / quote | Where |
|---|---|---|
| Images | 28,036; image height 800 | [R1899, AITODR, p3 Table I; p4 §III-B] |
| Instances | 752,460 oriented boxes | [R1899, AITODR, p4 §III-B] |
| Classes and counts | 8: airplane 1,667 · bridge 1,541 · storage-tank 13,771 · ship 35,813 · swimming-pool 1,617 · vehicle 662,929 · person 34,490 · wind-mill 632. Sum = 752,460; vehicle = 88.1%, ship = 4.8%, bridge = 0.2% **[derived]** | [R1899, AITODR, p5 footnote 2] |
| Object size | mean ± std **10.6 ± 4.9** px (AI-TOD-v2 12.7 ± 5.6; SODA-A 15.6 ± 7.6) | [R1899, AITODR, p3 Table I] |
| Size distribution | "most objects are gathered within the tiny scale (<16×16 pixels)"; histogram only in Fig. 2(a), no numbers in text | [R1899, AITODR, p4 §III-B] |
| Angle convention (statistics) | "OpenCV definition … angle between the bounding box and the horizontal axis, with a range of (0, 90°]" | [R1899, AITODR, p4 §III-B] |
| Density | "an image in AI-TOD-R can contain over 2000 objects, with most images featuring over 100 objects" | [R1899, AITODR, p4–5 §III-B] |
| Splits | "divided into the train set, val set, trainval set, and test set". **Per-split image and instance counts: not stated in the source.** | [R1899, AITODR, p4 §III-B] |
| Annotation | semi-automatic: H2RBox-v2 OBB predictions from AI-TOD-v2 HBB → manual refinement by trained volunteers → expert double-check. The authors note H2RBox-v2 on tiny objects "remains far from satisfactory, particularly in scenarios with weak, densely packed objects" | [R1899, AITODR, p4 §III-A] |
| Size bins | **Not defined in the AI-TOD-R text.** Table II reports APvt/APt/APs/APm without edges. Edges come from AI-TOD-v2: very tiny [2,8], tiny [8,16], small [16,32], medium [32,64] (absolute size); AI-TOD-v2 shares 12.4% / 73.4% / 12.4% / 1.8% | [R2318, NWD, p7 §3.2] |
| Per-class aspect-ratio statistics | not stated in the source (Fig. 2(d) shows per-class *size* mean/std only) | [R1899, AITODR, p4 Fig. 2 caption] |

Note: AI-TOD-R class totals differ from AI-TOD-v2 totals (vehicle 662,929 vs 319,441 + 332,604 = 652,045; total 752,460 vs 752,745 in the NWD text, or 752,754 summed from its Table 1) **[derived from R2318 p6 Table 1 and §3.2]**. AI-TOD-v2 split statistics therefore cannot be copied to AI-TOD-R.

### 1.2 Benchmark protocol behind Table II

- Quote: "experiments on the AI-TOD-R are performed following the default setting of AI-TOD series [12], [13]. We use AI-TOD-R's trainval set for training and its test set for evaluation, and retain the image size as 800×800 for training and testing. The batch size and learning rate are set to 2 and 0.0025 respectively. We only use random flipping as data augmentation for all experiments." [R1899, AITODR, p5 §IV-A]
- Schedule: "1× denotes 12 epochs and 40e denotes 40 epochs" [R1899, AITODR, p6 Table II caption]. Rows #1–#22, #24, #26 = 1×; #23, #25, #27 = 40e.
- Optimizer, LR schedule and pretraining for the benchmark: not stated in §IV-A. §VI-A (DCFL experiments) states: one RTX 4090, **batch 4**, SGD **lr 0.005**, momentum 0.9, weight decay 1e-4, ImageNet-pretrained ResNet-50 + FPN, MMDetection/MMRotate, Focal loss + IoU loss, random flipping only [R1899, AITODR, p11 §VI-A]. §IV-A (batch 2, lr 0.0025) and §VI-A (batch 4, lr 0.005) disagree; which one produced DCFL rows #22–#27 is not stated.
- Max detections per image, NMS threshold, score threshold, evaluator implementation: **not stated in the source.** (For comparison, the AI-TOD-v2 benchmark raised proposals and max detections "from 100 to 3000" [R2318, NWD, p11 §6.2]; RFLA and DN-TOD also keep the top 3000 boxes [R2391, RFLA, p10 §4.1; W12, DN-TOD, p7 §5.1].)

### 1.3 Table II, fully-supervised results on AI-TOD-R test [R1899, AITODR, p6]

| ID | Method | Backbone | Sched | AP | AP50 | AP75 | APvt | APt | APs | APm | Params |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | RetinaNet-O | R-50 | 1× | 7.3 | 23.9 | 1.8 | 2.2 | 5.9 | 11.1 | 15.4 | 36.3M |
| 2 | FCOS-O | R-50 | 1× | 11.0 | 33.6 | 3.7 | 3.0 | 8.9 | 15.7 | 22.0 | 31.9M |
| 3 | Faster R-CNN-O | R-50 | 1× | 10.2 | 30.8 | 3.6 | 0.6 | 7.8 | 19.0 | 22.9 | 41.1M |
| 4 | RoI Transformer | R-50 | 1× | 10.5 | 34.0 | 2.2 | 1.1 | 8.8 | 16.9 | 20.3 | 55.1M |
| 5 | Oriented R-CNN | R-50 | 1× | 11.2 | 33.2 | 4.3 | 0.6 | 9.1 | 19.5 | 23.2 | 41.1M |
| 6 | Deformable DETR-O | R-50 | 1× | 8.4 | 26.7 | 2.0 | 4.8 | 9.3 | 8.6 | 7.3 | 40.8M |
| 7 | ARS-DETR | R-50 | 1× | 14.3 | 41.1 | 5.8 | 6.3 | 14.5 | 17.6 | 18.7 | 41.1M |
| 8 | KLD (RetinaNet-O) | R-50 | 1× | 7.8 | 24.8 | 2.3 | 3.1 | 6.7 | 10.3 | 15.8 | 36.3M |
| 9 | KFIoU (RetinaNet-O) | R-50 | 1× | 8.1 | 25.2 | 2.8 | 2.0 | 6.6 | 12.3 | 17.1 | 36.3M |
| 10 | Oriented RepPoints | R-50 | 1× | 13.0 | 40.3 | 4.2 | 5.2 | 12.2 | 16.8 | 21.4 | 36.6M |
| 11 | PSC (RetinaNet-O) | R-50 | 1× | 4.5 | 15.8 | 1.2 | 1.0 | 3.7 | 8.2 | 12.7 | 36.4M |
| 12 | Gliding Vertex | R-50 | 1× | 8.1 | 27.4 | 2.1 | 0.9 | 6.7 | 14.7 | 17.9 | 41.1M |
| 13 | R3Det | R-50 | 1× | 8.1 | 25.8 | 2.2 | 1.9 | 7.3 | 12.0 | 16.8 | 41.7M |
| 14 | S2A-Net | R-50 | 1× | 10.8 | 33.4 | 3.3 | 4.3 | 11.2 | 13.0 | 16.0 | 38.6M |
| 15 | ATSS-O (RetinaNet-O) | R-50 | 1× | 10.9 | 33.8 | 3.1 | 2.7 | 8.9 | 15.5 | 19.4 | 36.0M |
| 16 | SASM (RepPoints-O) | R-50 | 1× | 11.4 | 35.0 | 3.7 | 3.6 | 10.2 | 15.4 | 19.8 | 36.6M |
| 17 | CFA | R-50 | 1× | 12.4 | 38.7 | 4.0 | 5.0 | 11.9 | 16.5 | 18.8 | 36.6M |
| 18 | Oriented R-CNN | R-101 | 1× | 11.2 | 33.0 | 4.1 | 0.5 | 8.9 | 19.8 | 24.4 | 60.1M |
| 19 | Oriented R-CNN | Swin-T | 1× | 12.0 | 34.6 | 4.6 | 0.7 | 9.9 | 20.8 | 25.3 | 44.8M |
| 20 | Oriented R-CNN | LSKNet-T | 1× | 11.1 | 33.4 | 3.8 | 0.6 | 9.2 | 18.9 | 22.6 | 21.0M |
| 21 | ReDet | ReR-50 | 1× | 11.6 | 32.8 | 4.8 | 1.4 | 9.5 | 19.4 | 23.2 | 31.6M |
| 22 | DCFL (RetinaNet-O) | R-50 | 1× | 12.3 | 36.7 | 4.5 | 4.3 | 10.7 | 17.2 | 22.2 | 36.1M |
| 23 | DCFL (RetinaNet-O) | R-50 | 40e | 15.2 | 44.9 | 5.1 | 4.9 | 13.1 | 19.7 | 25.9 | 36.1M |
| 24 | DCFL (Oriented R-CNN) | R-50 | 1× | 15.7 | 47.0 | 5.8 | 6.3 | 14.8 | 19.6 | 22.5 | 41.1M |
| 25 | DCFL (Oriented R-CNN) | R-50 | 40e | 17.1 | 49.0 | 7.2 | 6.4 | 16.0 | 21.6 | 24.9 | 41.1M |
| 26 | DCFL (S2A-Net) | R-50 | 1× | 13.7 | 39.7 | 5.3 | 4.7 | 12.4 | 18.6 | 22.6 | 38.6M |
| 27 | DCFL (S2A-Net) | R-50 | 40e | **17.5** | **49.6** | **7.9** | **6.5** | 15.7 | **22.6** | **27.4** | 38.6M |

- Table II has 27 **rows/configurations**, not 27 distinct methods (rows #18–#20 are backbone swaps of Oriented R-CNN; #22–#27 are DCFL on three baselines × two schedules). No latency/FPS column; only #Params. The string "YOLO" does not occur anywhere in the AI-TOD-R text (grep, 0 hits).
- Text–table inconsistency: the text says "CFA and SASM yield promising performances of 11.4% and 12.4%, respectively" [p7 §IV-B], while Table II gives SASM 11.4 and CFA 12.4. Cite the table.
- Also in the text: "ATSS-O lifts the RetinaNet-O baseline by 3.6 points" [p7]; "oriented tiny object detection does not benefit from deeper backbone architecture (#18 vs. #5) or large convolution kernels (#20 vs. #5)" [p7].
- Label-efficient Table III [p7] (AP / AP50 / APvt / APt): SOOD with 30% OBB labels 13.0 / 38.8 / 3.9 / 11.1; H2RBox-v2 with 100% HBB 11.7 / 38.2 / 4.6 / 9.5.

### 1.4 DCFL best numbers

- Best AP / AP50 / AP75 / APvt / APs / APm: DCFL (S2A-Net) 40e = 17.5 / 49.6 / 7.9 / 6.5 / 22.6 / 27.4 (#27). Best APt: DCFL (Oriented R-CNN) 40e = 16.0 (#25). Best without DCFL: ARS-DETR 14.3 AP / 6.3 APvt (#7). [R1899, AITODR, p6 Table II]
- Authors' claim: "hits a new state-of-the-art performance of 49.6% AP0.5, with a remarkable improvement of 16.2%" [R1899, AITODR, p12 §VI-B].
- SODA-A test (Table IV, 1×, R-50): DCFL (RetinaNet-O) 34.9 AP / APeS 14.2; DCFL (Oriented R-CNN) 36.6 AP / APeS 13.9; RoI Transformer 36.0 [R1899, AITODR, p11 Table IV].
- DCFL mechanism (relevant for §5): GT and priors modelled as 2-D Gaussians with Σ = R(θ)·diag(w²/4, h²/4)·R(θ)ᵀ (Eq. 9); coarse step: top-K GJSD priors across the GT's own and **adjacent FPN levels** form the candidate bag (K = 16); fine step: Q highest PT = 0.5(cls + rotated IoU) (Q = 12), then a 2-component DGMM filter (g = 0.8) [R1899, AITODR, p9–10 §V-B/C; p14 §VI-C]. Ablations are on DOTA-v2 train → val, mAP@0.5 [p14 Table XI; the text calls it "Table XII"].

### 1.5 Positive-sample / learning-bias analysis (§IV-D)

- **What was measured:** "the prior matching degree (input) and posterior confidence scores (output) for different-sized objects when training"; Fig. 5 shows "the prior sample selection results across different detectors by counting the number of positive samples assigned to objects of varying scales (upper line charts), and the model's posterior confidence scores for different-sized objects (lower bar chart)" [R1899, AITODR, p7–8 §IV-D]. Caption: "SOOD [65] is trained with 10% labels under the semi-supervised object detection pipeline" [p8 Fig. 5]. Which detectors are plotted and the numeric values: **not stated in the text** (figure only).
- **What was found:** "At the prior level, tiny-scale objects receive significantly fewer positive samples than larger-scale objects", attributed to "the limited feature map resolution, sub-optimal measurement, and label assignment strategies"; "the stride of prior locations in a typical single-stage detector is at least 8 pixels"; under "MaxIoU, Center Sampling" the count is "further reduced"; tiny objects also have low posterior confidence, which confidence-based selection/re-weighting and pseudo-labelling amplify [R1899, AITODR, p8 §IV-D].
- **Second analysis (§VI-D, Fig. 8):** "we calculate the quantity and quality of positive samples assigned to ground truth (gt) bounding boxes within various angle and scale intervals"; in baselines "the number of positive samples assigned to each object varies periodically with respect to its angle and scale, with objects whose shapes (scale, angle) differ from predefined anchors receiving much fewer positive samples", and "the predicted IoU fluctuates periodically with respect to the gt's scale while remaining invariant with respect to the gt's angle" [R1899, AITODR, p14 §VI-D]. Dataset and numeric values for Fig. 8: not stated in the text ("Results are sampled from the model's last training epoch", Fig. 8 caption).
- [inference] The angle-periodic imbalance in Fig. 8 is described for anchor (box-prior) baselines. YOLO's TAL uses point priors with a point-in-box test; there the expected candidate count depends on area, not angle (see §7, [derived] 0.0205 × area). The DCFL finding should not be transferred to YOLO without measurement (RQ2).

### 1.6 Availability and licence (as written in the paper)

- "The dataset, benchmark, and code are available at https://chasel-tsui.github.io/AI-TOD-R/." [R1899, AITODR, p1 Abstract]
- Evaluator (rotated AP per size bin): not described in the source. Whether test-set annotations are public: not stated in the source. (For AI-TOD-v2: "Images and annotations of the train set and validation set are publicly available" [R2318, NWD, p6 §3.2]; DN-TOD reports on the AI-TOD-v2.0 **val** set [W12, DN-TOD, p8 Tables 3–4]. [inference] Test-label access for AI-TOD-R must be checked before RQ1 is designed.)
- Licence: **not stated in the source.** xView/download procedure: not stated in the source (xView appears only as a row of Table I).

---

## 2. YOLO26 (R0879 / W01)

### 2.1 STAL definition (§3.3.3, Eq. 4–6)

- Motivation: "after feature-map discretization, a tiny box may contain no valid anchor centers at all. In that case, the object receives zero positive candidates" [R0879, YOLO26, p7 §3.3.3].
- Eq. 4–5: "Let a ground-truth box be parameterized as gᵢ = (xᵢ, yᵢ, wᵢ, hᵢ), and let s_min denote the smallest feature-pyramid stride. During candidate filtering only, STAL constructs an assignment surrogate g̃ᵢ = (xᵢ, yᵢ, w̃ᵢ, h̃ᵢ), where each spatial dimension is adjusted independently as d̃ᵢ = s_ref if dᵢ < s_min, dᵢ otherwise, dᵢ ∈ {wᵢ, hᵢ}" [R0879, YOLO26, p7].
- "s_ref is a fixed reference size derived from the feature pyramid. In the current implementation, it is set to the second pyramid stride when available" [p7–8].
- Eq. 6: Mᵢⱼ = 1 "if anchor center aⱼ lies inside g̃ᵢ", else 0 [p8].
- "STAL modifies only the candidate-selection mask. The original box gᵢ is preserved for task-aligned scoring, final target assignment, and box regression" [p8].
- The definition is written for an axis-aligned (x, y, w, h) box. **How STAL treats a rotated box (angle) is not described in the paper.** The code does it (§3).

### 2.2 Defaults (§4.1)

- "For STAL, the current implementation uses the default three-level detection pyramid with strides [8, 16, 32]. Accordingly, the smallest stride is s_min = 8, and the reference size is set to the next stride level, s_ref = 16. In practice, this means that during candidate filtering only, any ground-truth width or height below 8 pixels is clamped to 16 pixels" [R0879, YOLO26, p11 §4.1].
- Because s_min and s_ref are *defined as strides*, a P2 head (strides 4/8/16/32) would by the paper's definition give s_min = 4, s_ref = 8 [inference from p7 + p11].
- §3.3.2 promises "branch-specific assignment settings … in Sec. 4.1" [p7]; §4.1 gives only the Progressive-Loss weights (0.8, 0.2) → (0.1, 0.9) [p11]. **The one-to-one vs one-to-many assignment settings (e.g. top-k) are not stated in the source.**

### 2.3 STAL ablations (all on COCO; no other dataset)

Table 2, step-by-step from YOLO11s, COCO AP [R0879, YOLO26, p12]:

| Step | AP (E2E) | AP (non-E2E) | Params M | FLOPs G | Latency ms |
|---|---|---|---|---|---|
| YOLO11s (baseline) | – | 47.0 | 9.4 | 21.5 | 2.5 |
| − DFL | – | 46.4 | 9.1 | 20.1 | 2.3 |
| + L1 loss | – | 46.6 | 9.1 | 20.1 | 2.3 |
| **+ STAL** | – | **46.8** | 9.1 | 20.1 | 2.3 |
| + backbone/neck refinement | – | 47.0 | 9.5 | 20.7 | 2.5 |
| … + hyperparameter search (final) | 47.8 | 48.6 | 9.5 | 20.7 | 2.5 |

Table 6, "Ablation of the STAL reference size s_ref on COCO using YOLO11s as the baseline" [R0879, YOLO26, p13]:

| Method | s_ref | AP | AP_S | AP_M | AP_L |
|---|---|---|---|---|---|
| TAL (baseline) | – | 46.6 | 29.0 | 51.4 | 63.9 |
| STAL | 8 | 46.6 | 27.7 | 51.6 | 63.8 |
| STAL | 16 | **46.8** | **29.6** | 51.6 | 63.8 |
| STAL | 32 | 46.5 | 28.3 | 51.3 | 63.7 |

- Authors' reading: "Setting s_ref = 8 does not improve overall AP and noticeably reduces AP_S, which suggests that the adjustment is too weak … Increasing the reference size further to 32 also degrades performance, indicating that excessive enlargement begins to distort the intended scale prior" [p13 §4.3.4].
- Only s_ref was varied; whether s_min stayed at 8 in the s_ref = 8 and 32 rows: not stated in the source. Seeds / variance: not stated in the source.
- [inference] The TAL baseline of Table 6 (46.6) equals the "+ L1 loss" row of Table 2, so Table 6 was probably run on the DFL-free + L1 configuration; the paper does not say so.
- Fig. 5 (COCO val, conf 0.25): "STAL improves small-object detection by ensuring sufficient anchor coverage for tiny ground-truth boxes" — qualitative only [p13].

### 2.4 OBB specifics (§3.4.3)

- Angle convention: previous YOLO OBB used OpenCV, "the acute angle between the box width and the positive x-axis, with a range of (0, 90°]"; "In YOLO26, the angle definition is changed to the long-edge definition following MMRotate [99], where the angle range is [−45°, 135°) and the width is constrained to be larger than the height" [R0879, YOLO26, p9].
- Angle decoding: old θ̂ = (σ(z) − 0.25)π (Eq. 12); YOLO26 θ̂ = z (Eq. 13) [p9].
- Angle residual modulo π: Δθ̃ᵢ = Δθᵢ − round(Δθᵢ/π)·π (Eq. 14) [p9].
- **Eq. 15** (checked on the rendered page): L_angle = (1/S) Σ_{i∈F} qᵢ ωᵢ sin²(2Δθ̃ᵢ), S = max(Σ_{i∈F} qᵢ, 1), **ωᵢ = exp(−log²(wᵢ*/hᵢ*) / λ²)**, where "qᵢ is the assignment weight produced by TAL" and ωᵢ is "an aspect-ratio-aware factor"; "Elongated boxes receive smaller ωᵢ and remain primarily constrained by the rotated IoU loss" [p9]. Best λ = 3 (Table 11).
- ProbIoU: "YOLOv8 and YOLO11 introduced OBB heads with a dedicated angle branch trained via ProbIoU [45]" [p4 §2.5]; "For square or near-square objects, the ProbIoU [45] loss used in YOLO11 models becomes insensitive to angle variations because the Gaussian representation is nearly invariant to rotation when width ≈ height" [p9]. The paper does not name the rotated IoU loss of YOLO26 itself (only "the rotated IoU loss", p9). In the code snapshot the **assigner** uses ProbIoU for rotated boxes (CODE L388–390).
- [inference] Because Eq. 15 weights the angle loss by the TAL assignment weight qᵢ, any change in which anchors are positive (STAL / OA-STAL) also changes the angle supervision.

### 2.5 Was STAL evaluated on OBB or on a tiny-object dataset?

- No. STAL appears only in COCO experiments (Table 2 p12, Table 6 p13, Fig. 5 p13). The OBB experiments (DOTA-v1.0) ablate angle definition and angle loss only (Tables 10–11, p15). The text contains no AI-TOD, VisDrone or SODA (grep; consistent with research-log #38).

### 2.6 OBB training recipe

- DOTA-v1.0: "containing 2,806 images and 188,282 instances across 15 categories. We split the images into overlapping 1024×1024 crops and train our models on the training set" [R0879, YOLO26, p15 §4.5.3].
- **OBB epochs, augmentation, crop overlap, pretraining and batch size: not stated in the source.**
- The detailed recipes in the supplement are for detection only: Objects365 pretraining 150 epochs at 640, batch 128, MuSGD lr0 0.01, momentum 0.94, wd 0.0005, close_mosaic 8, mosaic 1.00, fliplr 0.5, degrees 0, translate 0.1, scale 0.5 (n) / 0.9 (s–x), mixup 0.00–0.20, copy-paste 0.10–0.60 [R0879, YOLO26, p24 Tables S2–S3]; COCO fine-tuning 245/70/80/60/40 epochs for n/s/m/l/x, batch 128, "Mosaic is used heavily during most of training … and is disabled near the end" [p11 §4.1].

### 2.7 DOTA-v1.0 results

Table 10, DOTA-v1.0 **val**, YOLO26s without angle loss [p15]: (0, 90°] → 47.7 mAP / 75.0 AP50; [−45°, 135°) → 49.0 / 75.4.

Table 11, angle-loss λ on DOTA-v1.0 val, YOLO26s [p15] (mAP / AP50): none 49.0 / 75.4 · λ=1 49.4 / 75.5 · λ=2 49.5 / 75.4 · **λ=3 50.2 / 76.0** · λ=4 49.8 / 75.7 · λ=5 47.1 / 75.5.

Table S11, DOTA-v1.0 **test**, input 1024, YOLO26 evaluated "using the one-to-one branch without NMS" [R0879, YOLO26, p29]:

| Model | mAP50-95 | AP50 | AP75 | CPU ONNX ms | T4 TRT10 ms | Params M | FLOPs B |
|---|---|---|---|---|---|---|---|
| YOLO11n-obb | 49.7 | 78.4 | 52.1 | 117.6 | 4.4 | 2.7 | 16.8 |
| YOLO26n-obb | 52.4 | 78.9 | 56.8 | 97.7 | 2.8 | 2.5 | 14.0 |
| YOLO11s-obb | 51.4 | 79.5 | 54.4 | 219.4 | 5.1 | 9.7 | 57.1 |
| YOLO26s-obb | 54.8 | 80.9 | 60.4 | 218.0 | 4.9 | 9.8 | 55.1 |
| YOLO11m-obb | 52.8 | 80.9 | 56.1 | 562.8 | 10.1 | 20.9 | 182.8 |
| YOLO26m-obb | 55.3 | 81.0 | 60.7 | 579.2 | 10.2 | 21.2 | 183.3 |
| YOLO11l-obb | 52.9 | 81.0 | 56.6 | 712.5 | 13.5 | 26.1 | 231.2 |
| YOLO26l-obb | 56.2 | 81.6 | 62.2 | 735.6 | 13.0 | 25.6 | 230.0 |
| YOLO11x-obb | 54.1 | 81.3 | 57.8 | 1408.6 | 28.6 | 58.8 | 519.1 |
| YOLO26x-obb | 56.7 | 81.7 | 62.6 | 1485.7 | 30.5 | 57.6 | 516.5 |

- Authors: "YOLO26 improves OBB mAP by +2.5 to +3.4 over YOLO11 across scales, with larger AP75 gains of +4.6 to +6.0" [p15].
- [inference] These gains mix angle definition, angle loss, the DFL-free head, MuSGD, Progressive Loss and STAL; no OBB ablation isolates STAL.

---

## 3. Code: the TAL pipeline in the snapshot (`ultralytics_tal_main_2026-10-01.py`)

### 3.1 Constructor and `stride_val`

- Defaults: `topk=13`, `alpha=1.0`, `beta=6.0`, `stride=None`, `eps=1e-9`, `topk2=None` (L31–40); `self.topk2 = topk2 or topk` (L54).
- `self.stride = stride if stride is not None else [8, 16, 32]` (L58); **`self.stride_val = self.stride[1] if len(self.stride) > 1 else self.stride[0]`** (L59). Docstring: "Minimum ground-truth box side in select_candidates_in_gts; smaller sides are enlarged to it" (L27).
- So in code the **threshold and the target size are the same number** (`stride_val`, = 16 with the default strides), whereas the paper uses threshold s_min = 8 and target s_ref = 16 (§2.2).
- [inference] With a P2 head the caller would pass strides [4, 8, 16, 32] → `stride_val = 8` (L59). Variant (b) "+P2" in the proposal would therefore silently change STAL (and an OA-STAL that reuses `stride_val`) from 16 to 8.
- **Not in the snapshot (must be checked in `ultralytics/utils/loss.py` at the pinned commit):** the `topk`, `alpha`, `beta`, `topk2` and `stride` values that the OBB loss actually passes; whether anchor points are converted from grid units (`make_anchors` returns "Anchor points in grid units", L438) to pixels before the assigner; whether the one-to-one branch uses a separate assigner instance and its top-k.

### 3.2 Forward pipeline (shared by HBB and OBB)

1. `forward` → `_forward` (L64–138; OOM fallback retries per image, L99–138).
2. `get_pos_mask` (L180–204):
   - `mask_in_gts = self.select_candidates_in_gts(anc_points, gt_bboxes, mask_gt)` (L196) — **the STAL/OA-STAL step**.
   - `align_metric, overlaps = self.get_box_metrics(…, mask_in_gts * mask_gt)` (L198): computed only for in-candidate anchors, using the **original** `gt_bboxes` (L227).
   - `mask_topk = self.select_topk_candidates(align_metric, topk_mask=…)` (L200).
   - `mask_pos = mask_topk.mul_(mask_in_gts).mul_(mask_gt.bool())` (L202).
3. `get_box_metrics` (L206–234): `align_values = bbox_scores.pow(self.alpha) * overlap_values.pow(self.beta)` (L228), i.e. t = s^α · u^β with the class score of the GT's class (L226) and IoU u from `iou_calculation` (L227).
4. `iou_calculation`: HBB = CIoU clamped ≥ 0 (L236–246); **rotated = `probiou(gt_bboxes, pd_bboxes)` clamped ≥ 0** (L388–390).
5. `select_topk_candidates` (L248–275): `torch.topk(metrics, self.topk, dim=-1)` over **all** anchors of the image for each GT (L263); anchors picked by more than one top-k list of the same GT row are dropped by `count_tensor.masked_fill_(count_tensor > 1, 0)` (L273).
6. `select_highest_overlaps` (L350–382): anchors claimed by several GTs keep only the GT with the highest `overlaps` (= IoU/ProbIoU between that anchor's prediction and each GT) (L365–371); optional second filter `topk2` on the alignment metric if `topk2 != topk` (L373–379).
7. `get_targets` (L277–315): labels/boxes of the assigned GT; one-hot scores × foreground.
8. Normalisation (L170–176): `align_metric *= mask_pos`; per GT, `align_metric * max_overlap / (max_align + eps)`; the soft classification target of each positive = (its alignment / best alignment of that GT) × best IoU of that GT.

### 3.3 Candidate selection — HBB and rotated

- HBB (L317–348): `wh_mask = gt_bboxes_xywh[..., 2:] < self.stride_val` (L335); sides below `stride_val` replaced by `stride_val` "about their center" (L332, L336–340); inside test with strict margins `> eps` (L344–347).
- **Rotated (L392–425):** `gt_bboxes_clone = gt_bboxes.clone()` (L403); `wh_mask = gt_bboxes_clone[..., 2:4] < self.stride_val` (L404); w and h replaced independently by `stride_val` (L405–409); **the angle (index 4) is not touched**; `corners = xywhr2xyxyxyxy(gt_bboxes_clone)` (L412); parallelogram test with projections on edges ab and ad, inclusive bounds (L414–425).
- Consequence [derived]: with the code, a 4×12 box becomes a 16×16 square (orientation becomes irrelevant); a 5×20 box becomes 16×20 (angle kept, aspect ratio 4 → 1.25). With the paper rule (threshold 8), a 4×12 box becomes **16×12 — the long axis of the candidate region flips by 90°** relative to the object.

### 3.4 Where OA-STAL would be hooked

- **Exact place:** replace L404–409 of `RotatedTaskAlignedAssigner.select_candidates_in_gts` (the `wh_mask` / `torch.where` block) with the similarity scaling, before `xywhr2xyxyxyxy` (L412). The clone at L403 already guarantees that scoring, targets and regression keep the original boxes (consistent with the paper, p8).
- Reference size: reuse `self.stride_val` (L59) or, safer, an explicit hyper-parameter so that a P2 head does not change it.
- For a fair STAL comparison the HBB path (L334–340) is irrelevant; only the rotated assigner is used by OBB models (class at L385).

### 3.5 Code interactions that matter for OA-STAL

- **Top-k is not the binding filter for tiny GTs** [derived]: expected candidate count ≈ 0.0205 × surrogate area (anchor density 1/64 + 1/256 + 1/1024 per px² for strides 8/16/32); a 16×16 surrogate gives ≈ 5.25 candidates (SIM), below the constructor default `topk=13` (L33). Since all non-candidates have metric 0, every in-region anchor with metric > 0 survives L263 + L202. Top-k binds only for large surrogates (e.g. STAL on a 5×60 box: ≈ 19.7 candidates, SIM). The loss's actual `topk` value is not in the snapshot.
- **Quality enters through soft targets, not filtering** [derived from L170–176]: extra low-ProbIoU candidates become positives with small soft targets; whether this helps or hurts is empirical.
- **Conflicts:** an anchor inside two enlarged regions goes to the GT with the highest ProbIoU of its prediction (L366–371). RFLA uses a different rule: "the occluded sample will be assigned to the smaller gt" [R2391, RFLA, p9 §3.3].
- **ProbIoU in the alignment metric (L388–390)** is nearly rotation-invariant for near-square boxes [R0879, YOLO26, p9] → for near-square tiny GTs, the alignment metric does not reward correct angles.
- **Regression targets for out-of-box candidates:** `rbox2dist` returns l, t, r, b relative to the anchor (L537–549) and clamps to `[0, reg_max − 0.01]` when `reg_max` is given (L551–552). A candidate anchor outside the true box needs a negative distance on one side; whether the YOLO26 OBB loss passes `reg_max` (clamping that side to 0) is not in the snapshot. OA-STAL moves candidates beyond the object's ends along the long axis; STAL moves them sideways. [inference] Either way some positives have targets that cannot be represented exactly; this must be checked in `loss.py`.
- **Version drift:** the snapshot is `main` (research-log #26, last commit 2026-09-27), not a tagged release; the paper's threshold (8) and the code's (16) differ (research-log #39). Pin the package version and commit hash.

---

## 4. RFLA, NWD/RKA, GCD, DN-TOD — how they handle tiny-object positives or noise

All four are **HBB** methods built on MMDetection; none is evaluated on AI-TOD-R.

| | RFLA (R2391) | NWD-RKA (R2318) | GCD (R1269) | DN-TOD (W12) |
|---|---|---|---|---|
| Mechanism | Gaussian effective-receptive-field prior per feature point (ERF radius = half the theoretical RF) [p6 §3.1]; Receptive Field Distance RFD = 1/(1 + KLD) between ERF and GT Gaussians (Eq. 8 [p8]; KLD chosen as default [p10 §4.3]); Hierarchical Label Assignment: stage 1 top-k RFD per GT, stage 2 shrinks the ERF by β and adds one positive per GT (Eq. 9; k = 3, β = 0.9) [p8–9, p12]; for FCOS, "we remove the constraint of limiting feature points inside gt box" [p9 §3.4] | GT and anchor boxes as 2-D Gaussians (Σ = diag(w²/4, h²/4)), NWD = exp(−√W₂²/C) with C = 12.7 (mean absolute size of AI-TOD-v2 trainval) (Eq. 7) [p8, p14]; RKA: "assign pos labels to anchors that hold Top k score with a particular gt, and … neg labels to remaining anchors" (k = 2) [p9 §4.2, p14] | Gaussian Combined Distance, a scale-invariant similarity, used both as assignment metric (RPN of Faster R-CNN; RetinaNet) and as regression loss [p1–3; p3 §IV] | Not an assigner: Class-aware Label Correction (class shifts) + Trend-guided Learning Strategy (re-weighting + recurrent box regeneration) for box noise; uses RFLA as assigner (FCOS*, Faster R-CNN*) [p1, p8] |
| Positive-coverage claim | "even though the gt has no overlap with any box prior, some positive samples can be compensated for the gt" [p11 §4.3] | "at least one appropriate training sample can be guaranteed for this gt box" [p10 §5.2]; positives per epoch "increased to 709,060 (490,240 more than baseline)" [p10] | not framed as coverage | — |
| Box type | HBB | HBB | HBB | HBB |
| Dataset version | AI-TOD (v1), trainval → test | AI-TOD-v2, trainval → test | AI-TOD-v2 (split not stated) | AI-TOD-v2.0 **val** (synthetic noise); real noise: train AI-TOD → eval AI-TOD-v2.0 val |
| Key numbers (AP / AP50 / AP75 / APvt / APt / APs / APm) | Table 5 p11: Faster R-CNN 11.1/26.3/7.6/0.0/7.2/23.3/33.6 → **w/ RFLA 21.1/51.6/13.1/9.5/21.2/26.1/31.5**; DetectoRS w/ RFLA **24.8**/55.2/18.5/9.3/24.8/30.3/38.2; RetinaNet 8.7 → 9.1 (APvt 2.4 → 4.1); FCOS* (P2–P6) 15.4 → 16.3 (APvt 6.0 → 7.3) | Table 4 p11: Faster R-CNN 12.8/29.9/9.4/0.0/9.2/24.6/37.0 → **w/ NWD-RKA 21.4/53.2/12.5/7.7/20.7/26.8/35.2**; DetectoRS w/ NWD-RKA **24.7**/57.4/17.1/9.7/24.2/29.8/39.3; RetinaNet 8.9 → 10.5 (APvt 2.7 → 3.5). Ablation Table 7 p13: NWD only 20.2, RKA only 17.9, both 21.4; best tuned IoU thresholds 18.6 (Table 8) | Table I p4 (Faster R-CNN): GIoU 11.1 AP; WD-assign 18.9; NWD-assign 17.8; GCD-assign 19.6; GCD assign + loss **20.1**/48.7/11.8. Table IV p5 (RetinaNet, regression loss): GCD 11.5/31.2/5.7/3.6/9.7/16.0/28.5 vs NWD 8.0, GIoU 6.8 | Table 4 p8 (real noise): Noisy-FCOS* 14.8 mAP / APvt 6.7; DN-TOD 15.5 / 6.8; Clean-FCOS* 15.8 / 7.1. Table 3 p8 (mixed noise 0/10/20/30/40%, metric not named): FCOS* 34.9/33.0/28.5/24.9/12.7 vs DN-TOD 38.1/34.2/31.4/27.2/17.6 |
| Stated limitations | No limitation section. Authors: the one-stage vs multi-stage gap "mainly results from the lack of multi-stage regression" [p12 §4.4]; AI-TOD-v2 results only "listed in GitHub" [p14] | No limitation section (not stated in the source); method stated for anchor-based detectors [p9] | "We have verified the exceptional performance of the Gaussian Combined Distance (GCD) primarily in the realm of horizontal detection" [p5 §V-A] | "the improvement on multi-scale objects is not as obvious as that on tiny objects"; "the improvement … is weakened when confronted with mixed noise"; oriented detection named as a future field [p11 §6] |

Observations [inference, from the tables above]:
- Assignment-only fixes give large gains on **two-stage** detectors and small gains on **one-stage** ones on AI-TOD/AI-TOD-v2 (RetinaNet +0.4 AP with RFLA; +1.6 with NWD-RKA [R2318, NWD, p13 §6.3.1]). YOLO-OBB is one-stage.
- Both RFLA and NWD-RKA **lower APm** of Faster R-CNN (33.6 → 31.5; 37.0 → 35.2) while raising APvt/APt: more tiny positives can cost larger objects.
- The AI-TOD-v2 benchmark already contains a YOLO: YOLOv3 (DarkNet-53) 4.1 AP / APvt 1.1 (HBB) [R2318, NWD, p11 Table 4]. So "no YOLO" is true only for the **oriented** AI-TOD-R benchmark table.
- GCD describes AI-TOD-v2 as "700,621 instances … roughly 12.8 pixels" [R1269, GCD, p3 §IV-A]; those are AI-TOD v1 figures (AI-TOD-v2: 752,745 instances, 12.7 px [R2318, NWD, p6]). Treat GCD's dataset description with care.
- DN-TOD: "the mAP is reduced by nearly half when there is 30% box noise in the dataset" (FCOS with RFLA, synthetic noise, AI-TOD-v2.0) [W12, DN-TOD, p4 §3.3, Fig. 3 p3]; box noise is relative: ŵ = (1 + Δw)·w, Δ ~ U(−a%, a%) (Eq. 1) [p4].

---

## 5. Aspect-ratio-aware / shape-aware assignment in the corpus (positioning OA-STAL)

Search terms used on cards, overviews, watchlist, matrix, benchmark CSV, txt_cache and local arXiv scan records: aspect ratio, shape-aware, shape-adaptive, elongated, ellipse/elliptical, Gaussian assignment, anisotropic, CA-DLA, SARFA, EARL, SASM, GGHL, CFL.

| Work | Evidence level in corpus | What it does | Assignment or loss? | Tiny-targeted? | Source |
|---|---|---|---|---|---|
| **DCFL** (R1899) | full text | GT and priors as 2-D Gaussians with Σ = R(θ)·diag(w²/4, h²/4)·R(θ)ᵀ — an **orientation- and aspect-preserving soft candidate region**; candidate bag = top-K GJSD across adjacent FPN levels; DGMM filter; "assigns samples in a way that balances both quantity and quality across different object shapes" | assignment (+ dynamic prior) | **yes, oriented tiny; evaluated on AI-TOD-R** (AP 17.5) | [R1899, AITODR, p1; p9–10 §V-B/C] |
| **SASM** | inside AI-TOD-R benchmark | "shape-adaptive sample selection and measurement strategy, accurately assigning labels according to the object's shape and orientation" | assignment | generic oriented; **evaluated on AI-TOD-R**: 11.4 AP / 3.6 APvt / 10.2 APt (#16) | [R1899, AITODR, p3 §II-B; p6 Table II] |
| **CFA** | inside AI-TOD-R benchmark | "dynamically assessing the sample quality based on the object's arrangement and shape information" | assignment | generic oriented; **on AI-TOD-R**: 12.4 AP / 5.0 APvt (#17) | [R1899, AITODR, p7 §IV-B; p6 Table II] |
| **GGHL** | described in AI-TOD-R related work | "fitting the main body of an instance with a single 2-D Gaussian heatmap, dividing and reweighting samples in a dynamic manner" | assignment | generic oriented; not on AI-TOD-R (DIOR-R 66.48 mAP, R1899 Table VIII) | [R1899, AITODR, p3 §II-B; p13 Table VIII] |
| **CFL STS / SASM** (survey view) | distilled card | IoU threshold depending on aspect ratio; CFL STS also uses angle difference (ATSS-based) | assignment | generic | [R1438, `notes/04-slr/_local/t07-slr-cards-S12.md` item 12] |
| **EARL** (TGRS 61, 2023, arXiv 2301.05856) | **abstract only** (arXiv API record) | "dynamic elliptical distribution aided sampling (DED) strategy … to fit the shapes and orientations of targets, and filter out low-quality samples"; "adaptive scale sampling (ADS) … among multi-level feature maps"; "in anchor-free detectors" | assignment (+ distance-weighted loss) | generic RS; abstract cites "large variations in scales and aspect ratios", not tiny | `scripts/t07-slr/data/_tmp_scanB/raw/ax_la_aspect.json`; research-log #40 |
| **MAS** (arXiv 2306.16718) | abstract only | "metric-aligned selection (MAS) strategy can dynamically select samples according to the shape and rotation characteristic of objects" (DOTA, FAIR1M, HRSC2016, UCAS-AOD) | assignment | generic | same file |
| **SARFA-Net** (JSTARS 2025, DOI 10.1109/jstars.2025.3532039) | **title only** ("abstract (no legal free full text)") | "Shape-Aware Label Assignment and Refined Feature Alignment for Arbitrary-Oriented Object Detection" — content not verified | assignment (per title) | not stated in the source | `scripts/t07-slr/data/p5_scored.csv` (SFW4406610993) |
| R1858 "Gaussian Assignment Strategy for Tiny Object Detection" | abstract only | GT as 2-D Gaussian, samples encoded by threshold | assignment | yes (tiny); box type not stated | `notes/04-slr/_local/t07-paper-overviews.md` (R1858) |
| R0839 "Normalized Gaussian Label Assignment …" | abstract only | normalized Gaussian label assignment + attention | assignment | yes (tiny RS) | `notes/04-slr/_local/t07-paper-overviews.md` (R0839) |
| Zand et al. 2021 (arXiv 2104.11854, TGRS per comment) | partly read (watchlist §5) | size-gated level assignment: "if the size of a given object is smaller than s/8, then the feature map at scale s will be off for this object" | assignment, **size**-gated | small rotated objects | `notes/04-slr/_local/t07-slr-watchlist.md` §5 |
| YOLO26 ω (W01) | full text | ωᵢ = exp(−log²(w/h)/λ²) on the angle loss | **loss**, not assignment | no | [R0879, YOLO26, p9 Eq. 15] |
| CA-DLA (W07, arXiv 2407.03205) | full text (watchlist) | √(w/h) factor in the **angle loss** (TLF Eq. 5); CDLA = category-aware choice of **negative** samples | **not** aspect-aware assignment | no | `notes/04-slr/_local/t07-slr-watchlist.md` W07 |
| Active-SAOOD (W06) | full text (watchlist) | orientation-uncertainty weight increasing with aspect ratio | active-learning metric | no | `notes/04-slr/_local/t07-slr-watchlist.md` W06, §6 |
| "Aspect-Ratio Aware Dynamic Label Assignment…", "Learning from the waist: aspect-ratio-aware positive sampling for oriented ship detection" (ESWA 2026) | **search snippets only** | not verified | — | ships (per title) | research-log #40 |

Positioning [inference]:
- Shape- and orientation-aware assignment is **not new**, and it has **already been tested on AI-TOD-R itself**: DCFL's Gaussian candidate bag preserves aspect ratio and angle by construction, and SASM/CFA appear in Table II. OA-STAL's distinguishing element is narrow: a hard, area-matched, similarity-preserving surrogate inside YOLO's point-in-box candidate filter, applied only to tiny GTs, training-only, with no extra parameters.
- Variant (a) of the proposal ("soft Gaussian/elliptical region") is mechanistically close to DCFL's coarse step and to EARL's DED; it would need to be positioned against both.
- No source in the corpus evaluates an aspect-ratio-preserving surrogate **for STAL / YOLO-OBB**; this is negative evidence within the searched corpus only.

---

## 6. Statistics on positives per GT and on aspect ratios

### 6.1 Positives per GT by size

| Source | What is reported | Numbers in text? |
|---|---|---|
| AI-TOD-R §IV-D, Fig. 5 | positives per object by scale "across different detectors" + posterior confidence by size; tiny objects "receive significantly fewer positive samples" | **No** (figure only) [R1899, AITODR, p8] |
| DCFL §VI-D, Fig. 8 | quantity and quality (predicted IoU) of positives per GT across angle and scale intervals; periodic with angle and scale for anchor baselines | **No** (figure only) [R1899, AITODR, p14] |
| NWD Fig. 8 | "mean number of positive training samples assigned to each object in a different size range"; under the Faster R-CNN baseline "objects in the scale range of very tiny almost fail to be assigned with any positive sample" | Only totals: NWD-RKA gives **709,060 positives (+490,240 vs baseline) in one epoch** [R2318, NWD, p9–10 §4.2, §5.2] |
| RFLA Fig. 4, §4.5 | synthetic simulation: "we randomly generate different gt in different locations of the image and simulate the process of label assignment"; "gt scales are randomly picked from 0 to 64", "16 intervals"; anchor-based: tiny scales and gaps between anchor scales become outliers; anchor-free "somewhat alleviate" it | **No** (figure only) [R2391, RFLA, p12 Fig. 4; p13 §4.5] |
| YOLO26 | no positive-count statistics; only "prevents pathological zero-positive cases" and qualitative Fig. 5 | No [R0879, YOLO26, p8, p13] |
| SIM (mine) | expected candidates and P(zero candidates) per rule for synthetic tiny boxes (§7.1) | yes, **[derived]**, geometry only |

### 6.2 Aspect ratios of tiny objects

- AI-TOD-R: per-class aspect-ratio statistics **not stated in the source**; Fig. 2(d) gives per-class size mean/std only [R1899, AITODR, p4].
- SODA-A: **not stated in the source**; Fig. 4(b) gives per-category *area* distributions; qualitative only: "The objects of large-vehicle and container with elongated structure challenge the regression branch" [R2256, SODA, p11 Fig. 4; p16 §5.4.2].
- AI-TOD-v2: per-category *size* box plot (Fig. 5(d)), no aspect ratio [R2318, NWD, p6–7].
- Consequence: the aspect-ratio distribution per class and size bin must be **measured from the labels** before OA-STAL is motivated quantitatively (part of RQ2).

### 6.3 SODA-A facts needed for RQ4 [R2256, SODA]

| Item | Value / quote | Page |
|---|---|---|
| Images / instances / classes | 2,513 images; 872,069 instances; 9 classes: airplane, helicopter, small-vehicle, large-vehicle, ship, container, storage-tank, swimming-pool, windmill | p1 Abstract; p10 §4.1 |
| Split | "approximately … 40% : 25% : 35% for SODA-A" (train : val : test) | p10 §4.1 |
| Size subsets (area, px²) | eS (0, 144], rS (144, 400], gS (400, 1024], Normal (1024, 2000]; > 2000 px² → ignore | p9 Table 3; p10 |
| Size | Small-object average absolute size 14.75 px; size range "strikingly [5, 15]"; AI-TOD-R Table I lists 15.6 ± 7.6 | p11; [R1899 p3] |
| Small-subset count | "837512 instances belonging to Small object subset" | p12 |
| Density | 1 to 11,134 instances per image; mean 347.02 | p12 |
| Orientation | "−π/2 to π/2"; DOTA head/tail definition not used "because most objects with tiny size cannot convey sufficient visual cues to determine their head or tail" | p12 |
| Resolution | average 4761 × 2777 | p12 |
| Protocol | MMRotate; "crop original images into a series of 800 × 800 patches with a stride of 650. These patches will be resized to 1200 × 1200 during training and testing"; 1× = 12 epochs | p13 §5.2; p16 Table 9 |
| Licence | text: "freely available under the CC-BY-SA license agreement"; footnote URL: creativecommons.org/licenses/by-nc/4.0 — **internally inconsistent** | p22 §A.3 |
| Best baseline | RoI Transformer 36.0 AP; one-stage Rotated RetinaNet 26.8 | p16 Table 9 |

[inference] The SODA protocol enlarges patches ×1.5 (800 → 1200), so at network input fewer objects fall below 8 or 16 px than in the raw imagery; STAL/OA-STAL effects on SODA-A may be diluted relative to AI-TOD-R (native 800×800). Report the fraction of GTs that trigger each rule **at the training resolution actually used**.

---

## 7. Critical review of the C-3 premises — all items are [inference] unless marked [derived]

### 7.1 Geometry of the four candidate rules [derived]

`scripts/t07-slr/data/_tmp_dossierA/sim_candidates.py` replicates the rotated inside-box test of CODE L403–425 on an anchor grid with centres at (i + 0.5)·stride, strides 8/16/32 (assumes the loss passes pixel-unit anchors). 4,000 random centres (uniform in a 32-px cell) and angles (uniform [0, π)) per row. OA-STAL as written in the proposal: k = max(1, 16/√(wh)), similar scaling, long-side cap c·16 with c = 2; the cap is applied unconditionally because the proposal states it unconditionally; "rescale" keeps the aspect ratio, "clip" cuts only the long side (the proposal does not say which). "Shared side/end" = fraction of a GT's candidates that also fall in the surrogate of an identical neighbour placed side-by-side / end-to-end with a 2-px gap. Full output: `sim_candidates_out.txt`.

| True box (w×h px) | Rule | Surrogate | Mean candidates | P(zero cand.) | Shared side | Shared end |
|---|---|---|---|---|---|---|
| 4×4 | TAL | 4×4 | 0.33 | **0.671** | 0 | 0 |
| 4×4 | STAL-paper / STAL-code / OA-STAL | 16×16 | 5.2–5.3 | 0 | 0.63 | 0.63 |
| 10×10 | TAL | 10×10 | 2.07 | 0.006 | 0 | 0 |
| 10×10 | STAL-paper (no change, sides ≥ 8) | 10×10 | 2.05 | 0.004 | 0 | 0 |
| 10×10 | STAL-code / OA-STAL | 16×16 | 5.2–5.3 | 0 | 0.25 | 0.25 |
| 4×12 | TAL | 4×12 | 0.98 | **0.230** | 0 | 0 |
| 4×12 | STAL-paper | 16×12 (axis flips) | 3.94 | 0 | 0.63 | 0.00 |
| 4×12 | STAL-code | 16×16 | 5.24 | 0 | 0.63 | 0.12 |
| 4×12 | OA-STAL | 9.2×27.7 | 5.25 | 0 | 0.34 | **0.49** |
| 3×10 | TAL | 3×10 | 0.63 | **0.442** | 0 | 0 |
| 3×10 | STAL-code | 16×16 | 5.27 | 0 | 0.69 | 0.24 |
| 3×10 | OA-STAL | 8.8×29.2 | 5.27 | 0 | 0.42 | **0.59** |
| 5×20 | STAL-paper = STAL-code | 16×20 | 6.56 | 0 | 0.56 | 0.00 |
| 5×20 | OA-STAL | 8×32 | 5.25 | 0 | 0.12 | 0.31 |
| 8×14 | STAL-paper (no change) | 8×14 | 2.30 | 0 | 0 | 0 |
| 8×14 | STAL-code | 16×16 | 5.24 | 0 | 0.37 | 0.00 |
| 8×14 | OA-STAL | 12.1×21.2 | 5.24 | 0 | 0.17 | 0.24 |
| 6×40 | TAL | 6×40 | 4.91 | 0.002 | 0 | 0 |
| 6×40 | STAL-paper = STAL-code | 16×40 | 13.1 | 0 | 0.50 | 0.00 |
| 6×40 | OA-STAL rescale / clip | 4.8×32 / 6.2×32 | 3.16 / 4.05 | 0.011 / 0.003 | 0 | 0 |
| 5×60 | TAL | 5×60 | 6.12 | 0.004 | 0 | 0 |
| 5×60 | STAL-paper = STAL-code | 16×60 | 19.7 | 0 | 0.56 | 0.00 |
| 5×60 | OA-STAL rescale / clip | 2.7×32 / 5.0×32 | **1.76** / 3.27 | **0.102** / 0.009 | 0 | 0 |

What the table shows [derived]:
1. Expected candidate count depends on surrogate **area only** (≈ 0.0205 × area). For every box that both rules enlarge to 16×16-equivalent area, **OA-STAL and STAL-code give the same expected count** (≈ 5.25); OA-STAL changes *where* candidates lie, not how many.
2. For boxes with one side ≥ 16 (5×20, 6×40, 5×60), OA-STAL gives **fewer** candidates than STAL, and with the unconditional cap it can give fewer than plain TAL, up to a 10% zero-candidate rate for a 5×60 box.
3. The paper and code versions of STAL differ most for 8–16 px objects (10×10: 2.05 vs 5.22 candidates; 8×14: 2.30 vs 5.24).
4. OA-STAL moves neighbour conflicts from side-by-side to end-to-end configurations (4×12: side 0.63 → 0.34, end 0.12 → 0.49).

### 7.2 Premise check for RQ1 (the benchmark gap)

- True: the AI-TOD-R benchmark (Table II) contains no YOLO (0 hits) [R1899].
- But a published paper already compares a YOLO-OBB-derived detector with AI-TOD-R Table II numbers: **DIA-YOLO** (Kim & Park, IEEE Access vol. 13, 2025): "The comparative training employed the YOLOv11 oriented object detection model", with the input changed to 4 channels in Ultralytics `conv.py` [dia_yolo.txt, §III-B, §IV-B]. Table 5 (printed p. 150580) lists the AI-TOD-R AP50 values (e.g. RetinaNet 23.9, ARS-DETR 41.1, DCFL 49.6) next to DIA-YOLO 56.1 (12 epochs), 71.5 (40 epochs), 89.9 (815 epochs), citing [43] = AI-TOD-R; Table 3 (printed p. 150579) gives a plain "YOLO" on "AITOD": P 63.7, R 26.0, mAP50 34.5, mAP50-95 17.2 (DIA-YOLO 41.0 / 23.1). Their "AITOD" "consists of 18,730 images" (not 28,036), uses 4-channel RGBD input, reports no APvt/APt, and its text contradicts Table 5 ("56.4% after 40 epochs, 71.5% after 400 epochs"). Not in the SLR corpus; found in `_tmp_scanB` (another agent's scan) and read directly from the local text and rendered pages.
- [inference] The defensible gap is narrower: *no protocol-matched benchmark of stock YOLOv8/11/26-OBB on AI-TOD-R with the size-binned metrics (APvt/APt) and an assignment analysis was found in the corpus*. DIA-YOLO must be cited and distinguished; a fresh search before writing remains necessary.

### 7.3 Strongest reasons OA-STAL might not help — and the measurement that would detect each

| # | Risk | Evidence | Measurement in RQ2 / RQ3 |
|---|---|---|---|
| 1 | **Same count, different place.** OA-STAL does not add candidates relative to STAL-code for tiny GTs; any gain must come from candidate placement or conflict patterns, which may be second-order. | [derived] §7.1 items 1–2 | RQ2: per GT, log candidate count, positives after conflict resolution, fraction of positives inside the true OBB, mean offset along the long and short axes, stratified by size bin **and aspect-ratio bin**. Expect no difference in counts; a difference must appear in placement or conflicts or the mechanism is absent. |
| 2 | **Small effect size in a one-stage detector.** STAL itself gave +0.2 AP / +0.6 AP_S on COCO (single numbers, no variance reported). Assignment fixes on one-stage RetinaNet gave +0.4 AP (RFLA, AI-TOD) and +1.6 AP (NWD-RKA, AI-TOD-v2). OA-STAL is a further second-order change. | [R0879 p12–13 Tables 2, 6]; [R2391 p11 Table 5]; [R2318 p13 §6.3.1] | RQ3: ≥ 2–3 seeds for **every** ablation row, mean ± std; estimate run-to-run std in Phase 1 and fix a minimal detectable effect before Phase 3. |
| 3 | **Formula defects as written.** The unconditional long-side cap shrinks non-tiny elongated objects (contradicting the sanity check "k = 1 ⇒ TAL"); the area trigger leaves thin objects with √(wh) ≥ 16 but a side < 8 without STAL's protection. Cap semantics (rescale vs clip) unspecified. | [derived] §7.1 item 2 (5×60: P(zero) 0.102 vs 0.004 for TAL) | Count GTs with min side < 8 and √(wh) ≥ 16 per class; zero-candidate rate per rule; class AP for bridge and ship. Repair before any GPU run: apply the cap only when k > 1, never below the original long side, and keep a minimum-side floor. |
| 4 | **Paper-vs-code threshold confound.** "STAL" means two different rules for 8–16 px objects; 73.4% of AI-TOD-v2 objects are in the tiny [8,16] bin. OA-STAL's trigger (√(wh) < 16) behaves like the code version, so "OA-STAL > STAL-paper" could be a pure threshold effect. | [R0879 p11]; CODE L59, L404–409; [R2318 p7]; [derived] §7.1 item 3 | Factorial ablation: trigger {side < 8, side < 16, √(wh) < 16} × surrogate shape {per-side, similar}. Primary comparison = OA-STAL vs **STAL-code**. Report which rule each released checkpoint used. |
| 5 | **Crowding.** AI-TOD-R images often hold > 100 objects, some > 2000. Enlarged regions overlap neighbours; conflicts go to the GT with the higher prediction ProbIoU (L366–371), which may favour larger or easier neighbours. OA-STAL trades side-by-side conflicts for end-to-end conflicts. | [R1899 p4–5]; CODE L366–371; [derived] §7.1 item 4; RFLA's alternative rule "assigned to the smaller gt" [R2391 p9] | RQ2: per GT, candidates "lost to a neighbour" and post-conflict zero-positive rate, by nearest-neighbour distance (in units of s_ref) and neighbour configuration (parallel vs collinear). RQ3 control: same rules with a "smaller-GT-wins" conflict rule. |
| 6 | **Aspect ratio of 4–12 px boxes may be unreliable.** ±1 px on a 4×12 box moves the ratio between 2.2 (5×11) and 4.3 (3×13) [derived arithmetic]. AI-TOD-R OBBs started from H2RBox-v2, which the authors call "far from satisfactory" on weak, dense tiny objects; tiny objects "cannot convey sufficient visual cues to determine their head or tail" (SODA); ProbIoU is nearly rotation-invariant for near-square boxes; 30% synthetic box noise roughly halves mAP (HBB). | [R1899 p4 §III-A]; [R2256 p12]; [R0879 p9]; [W12 p4 §3.3] | Measure aspect-ratio histograms per class and size bin; consistency check of AI-TOD-R OBB-derived HBBs against AI-TOD-v2 HBBs on the same images; RQ3 ablations: OA-STAL only for aspect ratio ≥ r₀ (e.g. 1.5), and OA-STAL with ±1 px aspect jitter. Report gains separately for elongated classes (ship, bridge, vehicle) and near-square classes (storage-tank, swimming-pool). |
| 7 | **Top-k does not filter tiny GTs; quality enters via soft targets.** With ≈ 5 candidates < top-k, all in-region candidates become positives; low-ProbIoU ones only get small soft targets (L170–176). Changing their location may not change the gradient much. | CODE L200–202, L263, L170–176; [derived] §3.5 | Log alignment metric and soft target per positive by rule and size bin; check whether any GT hits the top-k cap. Read the actual `topk` in `loss.py`. |
| 8 | **Regression targets and the end-to-end branch.** Candidates outside the true box need negative l/t/r/b; `rbox2dist` clamps to ≥ 0 when `reg_max` is passed (L551–552). YOLO26's one-to-one branch uses an undocumented "stricter assignment" whose top-k may make candidate shape decisive or irrelevant. | CODE L537–552; [R0879 p7, p11] | Log the fraction of positives with any negative distance target per rule; report E2E and non-E2E AP separately for every YOLO26 row. |
| 9 | **Stronger comparators exist on the same dataset.** DCFL's Gaussian candidate bag is already orientation- and aspect-aware and is the AI-TOD-R state of the art; SASM/CFA (shape-aware) are in Table II. Reviewers will expect a DCFL-style Gaussian candidate inside YOLO as a baseline, not only as an OA-STAL variant. | [R1899 p6, p9–10] | RQ3: include a Gaussian/KLD-top-k candidate rule (proposal variant (a)) as a baseline row. |
| 10 | **Hidden changes of s_ref.** Adding P2 changes `stride_val` from 16 to 8 in code (L59) and s_min/s_ref to 4/8 in the paper's definition. | CODE L59; [R0879 p7, p11] | Fix s_ref explicitly; log `stride_val` in every run. |
| 11 | **Benchmark-protocol traps for RQ1.** Max detections, evaluator and NMS settings of Table II are not stated (AI-TOD-family papers use 3000 detections); AI-TOD-R images can exceed 2000 objects; Table II backbones are ImageNet-pretrained while YOLO checkpoints are COCO/Objects365-pretrained; test-label access not stated. | [R1899 p4–5, p5, p11]; [R2318 p6, p11]; [R0879 p11] | Before Phase 1, reproduce one Table II row (e.g. RetinaNet-O 1×) with the chosen evaluator; set the YOLO validator's max-detections ≥ 3000 (its default is not in the sources read; verify); state that "protocol-matched" cannot match pretraining. |
| 12 | **SODA-A dilution.** The ×1.5 resize (800 → 1200) lifts many objects above the 8/16 px triggers. | [R2256 p13] | Report the share of GTs triggering each rule at the actual input size; if small, RQ4 tests a different regime and should say so. |

---

## Facts the proposal may cite

(Files: AITODR = `papers/_text/Xu2024-AI-TOD-R.txt`; YOLO26 = `papers/_text/Jocher2026-YOLO26.txt`; CODE = `papers/_text/ultralytics_tal_main_2026-10-01.py`; others in `scripts/t07-slr/data/txt_cache/`.)

| Claim | Value / quote | pid | File | Page / section |
|---|---|---|---|---|
| AI-TOD-R size | 28,036 images, 752,460 OBB instances, 8 classes | R1899 | AITODR | p4 §III-B; p3 Table I |
| AI-TOD-R object size | 10.6 ± 4.9 px (smallest among listed OBB datasets) | R1899 | AITODR | p3 Table I |
| Mostly tiny | "most objects are gathered within the tiny scale (<16×16 pixels)" | R1899 | AITODR | p4 §III-B |
| Class imbalance | vehicle 662,929 of 752,460 | R1899 | AITODR | p5 footnote 2 |
| Density | "can contain over 2000 objects, with most images featuring over 100 objects" | R1899 | AITODR | p4–5 |
| Benchmark protocol | trainval → test, 800×800, batch 2, lr 0.0025, random flip only | R1899 | AITODR | p5 §IV-A |
| Schedules | 1× = 12 epochs, 40e = 40 epochs | R1899 | AITODR | p6 Table II caption |
| Best on AI-TOD-R | DCFL (S2A-Net) 40e: 17.5 AP / 49.6 AP50 / 6.5 APvt / 15.7 APt | R1899 | AITODR | p6 Table II #27 |
| Weak two-stage APvt | Oriented R-CNN 11.2 AP but 0.6 APvt | R1899 | AITODR | p6 Table II #5 |
| Shape-aware assignment already on AI-TOD-R | SASM 11.4 AP / 3.6 APvt; CFA 12.4 / 5.0 | R1899 | AITODR | p6 Table II #16–17 |
| Learning bias | "tiny-scale objects receive significantly fewer positive samples than larger-scale objects" | R1899 | AITODR | p8 §IV-D |
| Prior stride | "the stride of prior locations in a typical single-stage detector is at least 8 pixels" | R1899 | AITODR | p8 §IV-D |
| DCFL candidate geometry | GT/prior Gaussians with Σ = R(θ)diag(w²/4, h²/4)R(θ)ᵀ; top-K GJSD across adjacent FPN levels | R1899 | AITODR | p9–10 §V-B/C |
| Size bins (AI-TOD family) | very tiny [2,8], tiny [8,16], small [16,32], medium [32,64]; AI-TOD-v2 shares 12.4/73.4/12.4/1.8% | R2318 | R2318.txt | p7 §3.2 |
| AI-TOD-v2 split sizes | trainval 376,625 / test 376,129 instances; train+val annotations public | R2318 | R2318.txt | p6 Table 1, §3.2 |
| Zero-candidate failure | "a tiny box may contain no valid anchor centers at all … zero positive candidates" | R0879 | YOLO26 | p7 §3.3.3 |
| STAL rule (paper) | dᵢ < s_min → s_ref, each side independently; s_min = 8, s_ref = 16 | R0879 | YOLO26 | p7 Eq. 4–5; p11 §4.1 |
| STAL scope | "STAL modifies only the candidate-selection mask" | R0879 | YOLO26 | p8 |
| STAL evidence | COCO, YOLO11s: TAL 46.6 AP / 29.0 AP_S → STAL(16) 46.8 / 29.6; s_ref 8: 46.6 / 27.7; s_ref 32: 46.5 / 28.3 | R0879 | YOLO26 | p13 Table 6 |
| STAL step in pipeline | +0.2 AP (46.6 → 46.8) | R0879 | YOLO26 | p12 Table 2 |
| YOLO26 OBB angle | long-edge, [−45°, 135°), w > h; θ̂ = z | R0879 | YOLO26 | p9 §3.4.3 Eq. 13 |
| Angle loss | ωᵢ = exp(−log²(w*/h*)/λ²), weighted by TAL weight qᵢ; best λ = 3 | R0879 | YOLO26 | p9 Eq. 15; p15 Table 11 |
| ProbIoU limitation | ProbIoU "becomes insensitive to angle variations" when width ≈ height | R0879 | YOLO26 | p9 |
| YOLO26s-obb on DOTA-v1.0 test | 54.8 mAP50-95 / 80.9 AP50; 9.8 M params; T4 TRT10 4.9 ms (YOLO11s-obb 51.4 / 79.5) | R0879 | YOLO26 | p29 Table S11 |
| Code threshold | `stride_val = stride[1]` (16 for [8,16,32]); sides < `stride_val` set to `stride_val` | — | CODE | L58–59, L404–409 |
| Code keeps the angle | only `[..., 2:4]` (w, h) of the rotated clone are modified | — | CODE | L403–412 |
| Rotated assigner IoU | `probiou(gt_bboxes, pd_bboxes)` | — | CODE | L388–390 |
| Task-aligned metric | `bbox_scores.pow(alpha) * overlap_values.pow(beta)`; defaults alpha 1.0, beta 6.0, topk 13 | — | CODE | L228; L33–36 |
| Conflict rule | anchors on several GTs keep the highest-overlap GT | — | CODE | L365–371 |
| NWD-RKA gain | Faster R-CNN 12.8 → 21.4 AP, APvt 0.0 → 7.7 (AI-TOD-v2 test, HBB) | R2318 | R2318.txt | p11 Table 4 |
| One-stage gains are small | NWD-RKA: RetinaNet +1.6 AP; RFLA: RetinaNet 8.7 → 9.1 AP (AI-TOD) | R2318; R2391 | R2318.txt; R2391.txt | p13 §6.3.1; p11 Table 5 |
| RFLA gain | Faster R-CNN 11.1 → 21.1 AP, APvt 0.0 → 9.5 (AI-TOD v1, HBB) | R2391 | R2391.txt | p11 Table 5 |
| GCD | Faster R-CNN assign + loss 20.1 AP; "primarily in the realm of horizontal detection" | R1269 | R1269.txt | p4 Table I; p5 §V-A |
| Box-noise sensitivity | "mAP is reduced by nearly half when there is 30% box noise" (HBB, AI-TOD-v2.0) | W12 | 2401.08056v1.txt | p4 §3.3 |
| SODA-A | 2,513 images, 872,069 instances, 9 classes; split ≈ 40:25:35; 800×800 crops (stride 650) resized to 1200×1200 | R2256 | R2256.txt | p1, p10, p13 |
| SODA-A size subsets | eS (0,144], rS (144,400], gS (400,1024], Normal (1024,2000] px² | R2256 | R2256.txt | p9 Table 3 |
| Prior YOLO-OBB vs AI-TOD-R numbers | DIA-YOLO compares a YOLOv11-OBB-based model with AI-TOD-R Table II AP50 values (18,730-image "AITOD", RGBD, mAP50 only) | — | `_tmp_scanB/raw/dia_yolo.txt` | printed pp. 150579–150580, Tables 3 and 5 |

---

## Corrections to `t07-proposal.md`

| # | Proposal says | What the sources show | Source |
|---|---|---|---|
| 1 | §0.2 / §2.1: AI-TOD-R benchmark "(27 phương pháp)" has no YOLO; gap = nobody benchmarked YOLO there | Table II has 27 **rows** (≈ 19 distinct methods + backbone swaps + 6 DCFL variants). "No YOLO" is true for the AI-TOD-R paper, but **DIA-YOLO (IEEE Access 2025)** already reports a YOLOv11-OBB-based model and a plain "YOLO" baseline (mAP50 34.5) on an "AITOD" OBB set and tabulates them against AI-TOD-R Table II AP50 values (DCFL 49.6). Protocol differs (18,730 images, RGBD, up to 815 epochs, AP50 only, internal inconsistencies). Restate the gap as "no protocol-matched, size-binned (APvt/APt) benchmark of stock YOLOv8/11/26-OBB on AI-TOD-R with an assignment analysis was found", and cite/distinguish DIA-YOLO. | [R1899 p6]; `dia_yolo.txt` pp. 150579–150580 |
| 2 | §2.1: size bins vt [2,8] / t [8,16] / s [16,32] / m [32,64] given as AI-TOD-R facts | The AI-TOD-R paper does **not** define the bins; they are defined for AI-TOD-v2 (also used by GCD). The 73.4% "tiny" share (research-log #42) is for AI-TOD-v2 HBB, not AI-TOD-R (whose mean size is smaller, 10.6 vs 12.7). | [R2318 p7]; [R1269 p4]; [R1899 p3] |
| 3 | §2.1: original benchmark is "mostly slow detectors" | Table II reports **no speed**, only #Params. Any speed comparison in RQ1 requires timing the baselines yourself under one setup. | [R1899 p6] |
| 4 | §2.1: STAL on COCO is "rất nhạy với tham số" | Numbers are correct (AP_S 29.0 → 29.6; 27.7 at s_ref 8; 28.3 at 32), but overall AP moves only 46.5–46.8, results are single runs (no variance stated), and only s_ref was varied. Say "AP_S varies by 1.9 points across three s_ref values (single runs)". | [R0879 p13 Table 6] |
| 5 | §2.1: STAL turns a 4×12 ship into a 16×16 region, "losing aspect ratio and the meaning of the angle" | True for the **code** rule only. The **paper** rule (threshold 8) gives 16×12 — the long axis of the region flips by 90°. The code keeps θ (L403–409); orientation becomes meaningless only when the surrogate is square. The paper never describes STAL for rotated boxes; the code applies it to OBB. | [R0879 p7, p11]; CODE L403–412; [derived] §7.1 |
| 6 | §2.3 sanity check: square box (w = h = d < s_ref) → s_ref × s_ref, "identical to STAL" | Identical to **STAL-code**; identical to **STAL-paper only for d < 8** (for 8 ≤ d < 16 the paper rule leaves the box unchanged: 10×10 → 2.05 vs 5.22 expected candidates). | [R0879 p11]; CODE L404–409; [derived] §7.1 |
| 7 | §2.3 sanity check: √(wh) ≥ s_ref → k = 1, "identical to TAL" | False as written: the long-side cap is stated unconditionally and shrinks non-tiny elongated boxes (6×40 → 4.8×32 or 6.2×32; 5×60 → 2.7×32 with a 10.2% zero-candidate rate vs 0.4% for TAL). Also STAL (both versions) enlarges the thin side of such boxes and OA-STAL does not, so OA-STAL equals neither STAL nor TAL there. Whether the cap rescales both sides or clips one is unspecified. | [derived] §7.1 |
| 8 | §2.3 implicit mechanism: OA-STAL gives tiny oriented objects better positive coverage than STAL | For every box both rules enlarge to s_ref² area, expected candidate counts are **identical** (≈ 5.25); for boxes with a side ≥ 16, OA-STAL gives **fewer** (5×20: 5.25 vs 6.56). OA-STAL changes placement and neighbour conflicts, not counts. RQ2's "positives per GT by size bin" alone cannot detect its mechanism. | [derived] §7.1 |
| 9 | §2.3 variant (b): "+P2" as a neutral control | In code `stride_val = stride[1]` (L59) → 8 with a P2 head; in the paper s_min/s_ref are strides → 4/8. Adding P2 silently changes STAL's reference unless s_ref is fixed explicitly. | CODE L59; [R0879 p7, p11] |
| 10 | §2.3 novelty: same class as EARL "and ship papers" | EARL is known in the corpus **only from its abstract** (TGRS 2023); the ship papers only from search snippets (research-log #40). Full-text evidence on the same dataset is stronger: DCFL's Gaussian Σ(w, h, θ) candidate bag and SASM/CFA in AI-TOD-R Table II. Variant (a) is close to DCFL's coarse step. Name DCFL and SASM as the nearest prior art. | [R1899 p3, p6, p9–10]; `_tmp_scanB/raw/ax_la_aspect.json` |
| 11 | §3: protocol = trainval → test, 800×800, batch 2, flip only, **12 epochs** | 12 epochs is the 1× schedule of most rows, but the best rows (DCFL #23/#25/#27) use 40 epochs. §VI-A states batch 4 / lr 0.005 for DCFL experiments, conflicting with §IV-A (batch 2 / lr 0.0025). Table II backbones are ImageNet-pretrained; YOLO checkpoints are COCO/Objects365-pretrained, so P1 cannot match pretraining unless stated. Max detections / NMS / evaluator are not stated in AI-TOD-R (the AI-TOD family uses 3000 detections). | [R1899 p5, p6, p11]; [R2318 p11]; [R0879 p11] |
| 12 | §3: "Dùng công cụ đánh giá chính thức của AI-TOD-R" | The paper describes no evaluator and does not say whether test annotations are public (for AI-TOD-v2 only train/val annotations were public; DN-TOD evaluates on the val split). Mark [phải xác minh] and plan a val-split fallback. | [R1899 p1]; [R2318 p6]; [W12 p8] |
| 13 | §3 licences | AI-TOD-R paper states **no licence**. SODA paper is internally inconsistent: "CC-BY-SA license agreement" in text, by-nc/4.0 URL in the footnote. | [R1899]; [R2256 p22] |
| 14 | §4.2: trainval ≈ 14,000 images inferred from the AI-TOD-v2 instance split | AI-TOD-R per-split counts are not stated; AI-TOD-R class totals differ from AI-TOD-v2 (vehicle 662,929 vs 652,045), so AI-TOD-v2 split statistics do not transfer exactly. Keep as an estimate to replace after download. | [R1899 p5]; [R2318 p6 Table 1] |
| 15 | §2.1: paper does not test STAL on tiny-object data (correct) | Also: STAL is not evaluated on **any OBB** dataset, and the one-to-one branch's assignment settings promised for §4.1 are not given. | [R0879 p7, p11–15] |
| 16 | §3: YOLO default recipe "mosaic, longer training" [suy luận] | Confirmed for detection (heavy mosaic, 245/70/… epochs on COCO); the **OBB** recipe (epochs, augmentation, crop overlap) is not stated in the YOLO26 paper. | [R0879 p11, p15, p24] |
| 17 | `synthesize-gaps-t07-q4-priority.md` §2 page refs "R0879 p8 §3.3.3", "R1899 p8 §IV-D" | §3.3.3 starts on p7 (Eq. 4–5 p7; Eq. 6 and "modifies only the candidate-selection mask" p8). §IV-D starts on p7 (Fig. 5 and the findings on p8). | PDF page check (PyMuPDF) |

Statements in the proposal that the sources **confirm**: AI-TOD-R 28,036 images / 752,460 objects / 8 classes / 10.6 ± 4.9 px; DCFL (S2A-Net, 40e) 17.5 AP; Oriented R-CNN R-50 11.2 AP; 0 occurrences of "YOLO" in the AI-TOD-R PDF; STAL definition and s_ref = 16 default; Table 6 numbers; code threshold 16 vs paper 8; SODA-A 2,513 images / 872,069 instances / 9 classes / 40:25:35 split; YOLO26s-obb 9.8 M parameters; DOTA-v2 train → val ablation protocol of DCFL.

## Thuật ngữ (Glossary)

| English | Tiếng Việt | Giải thích ngắn |
|---|---|---|
| candidate mask / surrogate | mặt nạ ứng viên / hộp thay thế | Vùng hình học dùng riêng cho bước chọn anchor ứng viên; không đổi mục tiêu hồi quy |
| STAL-paper / STAL-code | STAL theo bài báo / theo mã nguồn | Ngưỡng 8 px → 16 px (bài báo) so với ngưỡng 16 px → 16 px (mã `main`) |
| similarity scaling | phóng đồng dạng | Phóng hộp giữ tâm, góc và tỉ lệ cạnh |
| conflict resolution | giải quyết xung đột gán | Anchor thuộc nhiều GT được giao cho GT có ProbIoU cao nhất |
| zero-candidate rate | tỉ lệ không có ứng viên | Tỉ lệ GT không có tâm anchor nào nằm trong vùng ứng viên |
| [derived] | [suy ra tính toán] | Kết quả tính từ mã/hình học, không phải thực nghiệm trên dữ liệu |
