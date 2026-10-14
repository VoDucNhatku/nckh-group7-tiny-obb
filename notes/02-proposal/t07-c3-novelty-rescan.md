# t07 / C-3 — Novelty re-scan, resource facts, and reviewer critique

- **Date:** 2026-10-08
- **Worker:** sub-agent B — novelty re-scan & reviewer critique (spawned by admin → research-admin)
- **Subject:** direction C-3 (`notes/claims-ledger.md` row C-3): benchmark YOLOv8/11/26-OBB on AI-TOD-R; diagnose positive-sample coverage of TAL vs YOLO26 STAL for tiny oriented objects; propose OA-STAL (similarity-preserving enlargement of a tiny rotated GT to area `s_ref^2` for candidate selection only, with a long-side cap); generalise on SODA-A.
- **Inputs read first:** `notes/99-archive/t07-proposal.md` (§0–§9), `notes/05-venue-direction/synthesize-gaps-t07-q4-priority.md` (§8 sources of 2026-10-07 + unverified JEIT lead), `notes/claims-ledger.md` (C-3, C-7), `logs/research-log.md` #1–#42, `notes/04-slr/_local/t07-slr-watchlist.md` (W01–W15 cards).
- **Raw evidence / temp files:** `scripts/t07-slr/data/_tmp_scanB/raw/` (API JSON, downloaded open-access PDFs + text, rendered docs pages, Ultralytics source snapshots `tal_main_2026-10-08.py`, `loss_main_2026-10-08.py`). Query helper: `_tmp_scanB/bin/q.py`.
- **Label conventions:** "abstract only" / "full text" / "snippet only" = what was actually opened. `[inference]` = my reasoning, not stated by a source. `[unverified]` = could not be checked this session. No venue-rank claims, no "first"/SOTA claims are made here.
- **Ledger:** this file does **not** edit `claims-ledger.md`. Section "Bottom line" states what the admin should consider revising (C-3) under the revision protocol.

---

## 0. Query log

All queries run 2026-10-08. "Hits" = count returned by the source (OpenAlex `search` is a relevance search, so its count is not a precision measure). "Kept" = records carried into §A tables.

| Date | Source / API | Query | URL (truncated) | Hits | Kept |
|---|---|---|---|---|---|
| 2026-10-08 | arXiv API | `all:"AI-TOD-R"` | http://export.arxiv.org/api/query?search_query=all%3A%22AI-TOD-R%22 | 1 | 0 (only AI-TOD-R itself) |
| 2026-10-08 | arXiv API | `all:AITOD-R OR all:"AITOD R" OR all:AI-TODR` | http://export.arxiv.org/api/query?search_query=all%3AAITOD-R+OR+... | 0 | 0 |
| 2026-10-08 | arXiv API | `abs:"oriented tiny object"` | ...search_query=abs%3A%22oriented+tiny+object%22 | 2 | 0 (AI-TOD-R, DCFL — already in corpus) |
| 2026-10-08 | arXiv API | `abs:"tiny oriented object"` | ...search_query=abs%3A%22tiny+oriented+object%22 | 0 | 0 |
| 2026-10-08 | arXiv API | `abs:"oriented tiny" OR abs:"tiny oriented" OR ti:"oriented tiny"` | ...search_query=abs%3A%22oriented+tiny%22+OR+... | 3 | 0 |
| 2026-10-08 | arXiv API | `abs:"small-target-aware"` | ...search_query=abs%3A%22small-target-aware%22 | 6 | 1 (SDD-YOLO 2603.25218 via next query) |
| 2026-10-08 | arXiv API | `abs:STAL AND abs:YOLO` | ...search_query=abs%3ASTAL+AND+abs%3AYOLO | 6 | 1 (SDD-YOLO) |
| 2026-10-08 | arXiv API | `abs:YOLO26 AND (abs:tiny OR abs:small)` | ...search_query=abs%3AYOLO26+AND+%28abs%3Atiny+OR+abs%3Asmall%29 | 19 | 0 new (none on AI-TOD/AI-TOD-R/SODA-A) |
| 2026-10-08 | arXiv API | `abs:YOLO AND abs:"AI-TOD"` | ...search_query=abs%3AYOLO+AND+abs%3A%22AI-TOD%22 | 3 | 2 (ScopeMamba-YOLO, HDMamba-YOLO — HBB, context) |
| 2026-10-08 | arXiv API | `abs:YOLO AND abs:"SODA-A"` | ...search_query=abs%3AYOLO+AND+abs%3A%22SODA-A%22 | 3 | 1 (LiM-YOLO 2512.09700) |
| 2026-10-08 | arXiv API | `abs:YOLO AND abs:tiny AND (abs:oriented OR abs:rotated)` | ...search_query=abs%3AYOLO+AND+abs%3Atiny+AND+... | 2 | 0 |
| 2026-10-08 | arXiv API | `abs:RTMDet AND (abs:tiny OR abs:small) AND (abs:oriented OR abs:rotated)` | ...search_query=abs%3ARTMDet+AND+... | 2 | 0 |
| 2026-10-08 | arXiv API | `abs:YOLO27` | ...search_query=abs%3AYOLO27 | 3 | 0 (context only: 2510.09653v4) |
| 2026-10-08 | arXiv API | `abs:"label assignment" AND (abs:oriented OR abs:rotated) AND (abs:"aspect ratio" OR abs:elongated OR abs:"aspect-ratio" OR abs:slender)` | ...search_query=abs%3A%22label+assignment%22+AND+... | 5 | 2 (EARL 2301.05856, MSS 2306.16718) |
| 2026-10-08 | arXiv API | `abs:"label assignment" AND (abs:oriented OR abs:rotated) AND (abs:tiny OR abs:small)` | same pattern | 6 | 0 new |
| 2026-10-08 | arXiv API | `(abs:"sample selection" OR abs:"positive sample" OR abs:"candidate selection" OR abs:"sample assignment") AND (abs:oriented OR abs:rotated) AND (abs:"aspect ratio" OR abs:elongated OR abs:shape)` | same pattern | 15 | 0 new |
| 2026-10-08 | arXiv API | `(abs:YOLO OR abs:"real-time") AND abs:"label assignment" AND (abs:oriented OR abs:rotated)` | same pattern | 7 | 0 new |
| 2026-10-08 | arXiv API | `id_list=2606.03748,2412.11582,2509.25164,2510.09653` (version check) | https://export.arxiv.org/api/query?id_list=... | 4 | — (2606.03748 still v1; 2412.11582 still v1) |
| 2026-10-08 | OpenAlex API | `filter=cites:W4405470106` (AI-TOD-R arXiv record) | https://api.openalex.org/works?filter=cites%3AW4405470106 | 1 | 0 (DAR-Det, no abstract in OpenAlex) |
| 2026-10-08 | OpenAlex API | `filter=cites:W4416323921` (AI-TOD-R TPAMI record) | https://api.openalex.org/works?filter=cites%3AW4416323921 | 6 | 1 (MFN-Net) |
| 2026-10-08 | Semantic Scholar API | citations of `arXiv:2412.11582` (merged TPAMI DOI 10.1109/TPAMI.2025.3634161) | https://api.semanticscholar.org/graph/v1/paper/arXiv:2412.11582/citations | 10 | 3 (DIA-YOLO, MFN-Net, CLIQ) |
| 2026-10-08 | OpenAlex API | `search="AI-TOD-R"` and `filter=fulltext.search:"AI-TOD-R"` | https://api.openalex.org/works?search=%22AI-TOD-R%22 | 4 / 4 | 0 (SM-SCAM YOLO only cites; uses PKLot) |
| 2026-10-08 | OpenAlex API | `AITOD-R oriented tiny`, from 2025-01-01 | https://api.openalex.org/works?search=AITOD-R+oriented+tiny | 7 | 0 (all HBB AI-TOD/AI-TODv2 or unrelated) |
| 2026-10-08 | OpenAlex API | `aspect ratio aware label assignment oriented object detection`, from 2022 | https://api.openalex.org/works?search=aspect+ratio+aware+label+assignment+... | 4191 (relevance-ranked; top 50 screened) | 9 (ARA, RDCNet, DRLA-Net, SEDet, SARFA-Net, SASM, ADLA, SA3Det, DynamicOTA) |
| 2026-10-08 | OpenAlex API | `elliptical Gaussian label assignment rotated object detection positive samples`, from 2023 | https://api.openalex.org/works?search=elliptical+Gaussian+... | 113 (top 40 screened) | 2 (FCOSR, AOGC) |
| 2026-10-08 | OpenAlex API | `task-aligned assigner small objects label assignment YOLOv8 tiny`, from 2023-06 | https://api.openalex.org/works?search=task-aligned+assigner+... | 392 (top 50 screened) | 2 (SimD 2407.02394, CLAHR) |
| 2026-10-08 | OpenAlex API | `YOLO oriented bounding box label assignment small objects remote sensing`, from 2024 | https://api.openalex.org/works?search=YOLO+oriented+bounding+box+... | 690 (top 50 screened) | 0 new |
| 2026-10-08 | OpenAlex API | `YOLO26 small object aerial`, from 2026 | https://api.openalex.org/works?search=YOLO26+small+object+aerial | 171 (top 50 screened) | 1 (MD-YOLO, context) |
| 2026-10-08 | OpenAlex API | `orientation-aware label assignment tiny oriented objects positive samples enlarge ground truth`, from 2024 | https://api.openalex.org/works?search=orientation-aware+label+assignment+tiny+... | 41 (top 30 screened) | 0 |
| 2026-10-08 | Semantic Scholar API | `search: small-target-aware label assignment tiny oriented object` (second attempt, after 20 s back-off) | https://api.semanticscholar.org/graph/v1/paper/search?query=small-target-aware+... | HTTP 429 | — not run |
| 2026-10-08 | OpenAlex API | `Learning from the waist aspect-ratio-aware positive sampling oriented ship detection` | https://api.openalex.org/works?search=Learning+from+the+waist+... | 129 | 1 |
| 2026-10-08 | Crossref API | `works/10.11999/JEIT260317` | https://api.crossref.org/works/10.11999/JEIT260317 | 0 (HTTP 404) | — |
| 2026-10-08 | doi.org handle API / RA API | `10.11999/JEIT260317` | https://doi.org/api/handles/10.11999/JEIT260317 ; https://doi.org/ra/10.11999/JEIT260317 | 1 / RA=ISTIC | 1 (lead) |
| 2026-10-08 | jeit.ac.cn (publisher) | CN + EN article pages for JEIT260317 | https://jeit.ac.cn/cn/article/doi/10.11999/JEIT260317 | timeout (no response in 40–100 s, 3 attempts) | — |
| 2026-10-08 | WebSearch (snippet engine) | `"Cross-Domain Collaborative Enhancement for Tiny Object Detection in Remote Sensing Images"` | — | 9 links | 1 (snippet only) |
| 2026-10-08 | WebSearch (extended) | `YOLO11-OBB OR YOLOv8-OBB OR YOLO26-OBB "AI-TOD-R" oriented tiny object benchmark 2026` | — | 9 links | 0 |
| 2026-10-08 | Crossref API | `10.1016/j.eswa.2026.132251`, `10.1080/2150704X.2026.2667240`, `10.1109/LGRS.2024.3432810` | https://api.crossref.org/works/<DOI> | 1 each | metadata |
| 2026-10-08 | Semantic Scholar API | DOI lookups (ESWA waist, MFN-Net, TPAMI AI-TOD-R) | https://api.semanticscholar.org/graph/v1/paper/DOI:<DOI> | 1 each | abstract (MFN-Net only) |
| 2026-10-08 | Semantic Scholar API | `search: AI-TOD-R oriented tiny object detection YOLO` | https://api.semanticscholar.org/graph/v1/paper/search?... | HTTP 429 (rate limit) | — not run |
| 2026-10-08 | IEEE Xplore (OA, CC BY) | PDFs: DIA-YOLO (arnumber 11142761), SARFA-Net (10848126), RDCNet (11495006) | https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=... | 3 PDFs | 3 (full text) |
| 2026-10-08 | arXiv PDF | EARL 2301.05856v2; SDD-YOLO 2603.25218v1; AI-TOD-v2/NWD 2206.13996 | https://arxiv.org/pdf/<id> | 3 PDFs | 3 |
| 2026-10-08 | ScienceDirect | ESWA "Learning from the waist" (pii S0957417426011644) | https://www.sciencedirect.com/science/article/pii/S0957417426011644 | blocked (empty render) | metadata only |
| 2026-10-08 | GitHub API / raw | `ultralytics/ultralytics`: `utils/tal.py`, `utils/loss.py`, `nn/tasks.py`, `nn/modules/head.py`, `cfg/default.yaml` (main); commits on `tal.py` (30); 4 commit diffs; `compare/<sha>...<tag>` ×6; releases (502) | https://api.github.com/repos/ultralytics/ultralytics/... | — | §B.2 |
| 2026-10-08 | PyPI JSON | `ultralytics` | https://pypi.org/pypi/ultralytics/json | 1 | §B.2 |
| 2026-10-08 | Ultralytics docs (WebFetch) | OBB task page | https://docs.ultralytics.com/tasks/obb/ | 1 | §B.2 |
| 2026-10-08 | Kaggle docs (headless-Chrome render; pages are JS-only) | `/docs/notebooks`, `/docs/efficient-gpu-usage`, `/docs/datasets` | https://www.kaggle.com/docs/notebooks etc. | 3 pages | §B.1 |
| 2026-10-08 | GitHub raw / API | `Chasel-Tsui/AI-TOD-R`: README, `index.html` (project page), repo tree, `configs/_base_/datasets/aitodr.py`, `mmrotate/datasets/aitodr_eval/aitodr_eval.py`; Drive "Dataset" link title | https://github.com/Chasel-Tsui/AI-TOD-R | — | §B.3 |
| 2026-10-08 | GitHub raw | `jwwangchn/AI-TOD` README | https://raw.githubusercontent.com/jwwangchn/AI-TOD/master/README.md | 1 | §B.3 |
| 2026-10-08 | Web | xView site; SODA project page; SODA-A OneDrive link (HTTP check) | http://xviewdataset.org/ ; https://shaunyuan22.github.io/SODA/ | — | §B.3–B.4 |

Not used (by rule): Google Scholar (robots.txt), Sci-Hub/LibGen, blogs/aggregators as technical evidence.

---

## A. Novelty re-scan

### A.1 Verdict per research question (short)

| RQ (as in `t07-proposal.md` §2.2) | Gap status on 2026-10-08 | Main evidence |
|---|---|---|
| **RQ1** — YOLO-family OBB detectors benchmarked on AI-TOD-R | **Partly holds.** A peer-reviewed paper already reports a YOLOv11-OBB baseline and a YOLO-based model on an oriented "AITOD" set and places them next to the AI-TOD-R Table II numbers — but under a non-matching, under-specified protocol, with no size-binned AP and no official evaluator. The claim "no YOLO detector has been evaluated on AI-TOD-R" (`t07-proposal.md` §0, §2.1) is **no longer safe as written**. | DIA-YOLO, IEEE Access 13 (2025), DOI 10.1109/ACCESS.2025.3603214 (full text read) |
| **RQ2** — STAL (YOLO26) evaluated / diagnosed on tiny-object datasets | **Holds within this scan.** No work found that isolates STAL on AI-TOD, AI-TOD-R, SODA-A or VisDrone. The only paper found that uses STAL on a small-target dataset bundles it with three other YOLO26 changes in one ablation row, on a private HBB dataset. The Ultralytics YOLO26 paper is still v1 (COCO-only STAL ablation). | SDD-YOLO arXiv 2603.25218v1 (full text read); arXiv 2606.03748 still v1 |
| **RQ3** — orientation/aspect-preserving candidate region (OA-STAL) | **Partly holds.** The mechanism class is well populated: elliptical/shape-aware candidate regions (EARL 2023, SARFA-Net 2025, SEDet 2025, FCOSR 2023), aspect-adaptive assignment inside a YOLOv8-based OBB detector (RDCNet 2026), and small-object region enlargement + adaptive thresholds (SARFA-Net TCM). The exact combination "similarity-preserving enlargement to a minimum area `s_ref^2`, with a long-side cap, inside the TAL/STAL candidate step, for tiny OBB" was **not found**, but the distinguishing element is a narrow parametric choice. | EARL, SARFA-Net, RDCNet (full text read); others abstract only |
| **RQ4** — generalisation on SODA-A | Not a novelty question; feasibility risk (download route, §B.4). One 2026 letter already combines a small-object label-assignment change with aspect-ratio filtering on **SODA-A + AI-TOD** (MFN-Net, abstract only). | MFN-Net, Remote Sensing Letters 17 (2026) 801–813 |

### A.2 Candidate competitors — table

Overlap columns: RQ1 = YOLO/real-time on AI-TOD-R; RQ2 = STAL / positive-coverage diagnosis on tiny data; RQ3 = shape-/orientation-aware candidate selection or tiny-object enlargement.

| # | Title (short) | Venue / year | DOI / arXiv | What I read | RQ1 | RQ2 | RQ3 | Verdict |
|---|---|---|---|---|---|---|---|---|
| K1 | **DIA-YOLO: Diffusion-Based Involution Attention YOLO for Overhead Imagery** (Kim & Park) | IEEE Access, vol. 13, 2025 | 10.1109/ACCESS.2025.3603214 | **Full text** (13 pp.; Tables 3 and 5 read from rendered pages 10–11) | **Yes, partial** — YOLOv11-OBB baseline + DIA-YOLO on an oriented "AITOD" set; Table 5 compares with AI-TOD-R Table II rows (cites AI-TOD-R [43]) | No | No | **Partially overlaps RQ1** |
| K2 | **Cross-Domain Collaborative Enhancement for Tiny Object Detection in Remote Sensing Images** (CDCEDet) | J. Electronics & Information Technology (JEIT), 2026 (per DOI prefix + handle record) | 10.11999/JEIT260317 | **Snippet only** (search-engine summary); DOI handle verified; publisher page unreachable | No YOLO stated in snippet | Partly — label assignment for tiny objects (scale-adaptive anchors + quantile-adaptive IoU thresholds) evaluated on AI-TOD-R (snippet) | Partly (scale, not shape) | **Partially overlaps RQ2-class (lead; unverified content)** |
| K3 | **SARFA-Net: Shape-Aware Label Assignment and Refined Feature Alignment for Arbitrary-Oriented Object Detection** | IEEE JSTARS, vol. 18, 2025 | 10.1109/JSTARS.2025.3532039 | **Full text** (§III-B/C read) | No | No | **Yes** — elliptical candidate region following angle + aspect ratio; TCM lowers IoU threshold for small objects and enlarges their sampling range ×1.1 | **Partially overlaps RQ3 (closest mechanism)** |
| K4 | **EARL: Elliptical Distribution aided Adaptive Rotation Label Assignment** | IEEE TGRS, vol. 61, 2023 | arXiv 2301.05856 | **Full text** (§III-B/C/D) | No | No | **Yes** — dynamic elliptical (inner, contracted) candidate region by angle/aspect; ≥1 positive guaranteed via nearest unassigned anchor | **Partially overlaps RQ3** |
| K5 | **RDCNet: Rotation-Aware Feature Representation and Aspect-Adaptive Label Assignment** | IEEE JSTARS, vol. 19, 2026 | 10.1109/JSTARS.2026.3687230 | **Full text** (§III-C, Algorithm 1) | No (DOTA, HRSC) | No | **Yes** — YOLOv8-based OBB detector; candidate region in the GT's rotated frame + aspect-agnostic centerness in a task-aligned metric + fallback for empty sets | **Partially overlaps RQ3** (same detector family) |
| K6 | **MFN-Net: multi-scale adaptive fusion and flexible label assignment for small object detection in RS images** | Remote Sensing Letters, 17 (2026) 801–813 | 10.1080/2150704X.2026.2667240 | **Abstract only** (S2) | No (not stated) | Partly — "SFLA" label assignment for small objects, on **SODA-A + AI-TOD** | Partly — "aspect ratio filtering" | **Partially overlaps RQ3/RQ4**; full text needed |
| K7 | Aspect-Ratio Aware Dynamic Label Assignment for Oriented Object Detection (ARA + AAL) | IEEE GRSL, 21 (2024) | 10.1109/LGRS.2024.3432810 | Abstract only | No | No | Yes — aspect ratio enters candidate-quality score | Partially (RQ3, generic OBB) |
| K8 | DRLA-Net: Divergence-Aware and Ranking Cost-Based Label Assignment | IEEE GRSL, 2025 | 10.1109/LGRS.2025.3636153 | Abstract only | No | No | Yes — Gaussian OBB modelling + "scale-aware analysis", claims tiny-object benefit; DIOR-R, DOTA-v2 | Partially (RQ3) |
| K9 | SEDet / EALAS: Detecting Large Aspect Ratio Objects with Geometry-Aware… | IJCNN 2025 | 10.1109/IJCNN64981.2025.11229040 | Abstract only | No | No | Yes — ellipse-distance label assignment | Partially (RQ3) |
| K10 | Shape-Adaptive Selection and Measurement (SASM) | AAAI 2022 | 10.1609/aaai.v36i1.19975 | Abstract only | No | No | Yes — shape-aware sample selection; **already a row of AI-TOD-R Table II** | Partially (RQ3); already a baseline |
| K11 | FCOSR: A Simple Anchor-Free Rotated Detector | Remote Sensing 15 (2023) | 10.3390/rs15235499 | Abstract only | No | No | Yes — ellipse centre sampling + multi-level sampling for insufficient positives | Partially (RQ3) |
| K12 | Adaptive Dynamic Label Assignment for Tiny Object Detection in Aerial Images | IEEE JSTARS, 2024 | 10.1109/JSTARS.2024.3379515 | Abstract only | No | Partly — per-GT thresholds by shape/size/position, AI-TOD (HBB) | Partly (HBB) | Partially (RQ2-class, HBB) |
| K13 | SimD: Similarity Distance-Based Label Assignment for Tiny Object Detection | arXiv 2407.02394 (2024) | arXiv 2407.02394 | Abstract only | No | Partly — warns "excessive positive samples may lead to more false positives"; AI-TOD (HBB) | Partly (shape similarity) | Partially (HBB); useful counter-argument |
| K14 | Learning from the waist: Aspect-ratio-aware positive sampling for oriented ship detection | Expert Syst. Appl. 321 (2026) 132251 | 10.1016/j.eswa.2026.132251 | **Title/metadata only** (Crossref, S2; abstract blocked) | — | — | Likely (title) `[unverified]` | Unknown — must read before writing related work |
| K15 | SDD-YOLO: Small-Target Detection Framework for G2A Anti-UAV Surveillance | arXiv 2603.25218v1 (2026) | arXiv 2603.25218 | **Full text** (§4.6, §5.3 Table 3) | No | Partly — uses STAL on a small-target (HBB, private) dataset, but bundled with ¬DFL/NMS-free/MuSGD in one ablation row | No | No real overlap; shows STAL not isolated |
| K16 | CA-DLA (Category-Aware Dynamic Label Assignment with High-Quality Oriented Proposal) | arXiv 2407.03205 (2024) | arXiv 2407.03205 | Full text earlier (watchlist W07, 2026-10-05) | No | No | No — category-aware negative selection; √(w/h) angle-loss weight | No |
| K17 | LiM-YOLO: Pyramid Level Shift for Ship Detection | arXiv 2512.09700v4 | arXiv 2512.09700 | Abstract only | Partly — YOLO on SODA-A (ship subset) | No | No — P2-level shift (≈ the proposal's P2 control) | No (relevant to P2 ablation and RQ4 context) |
| K18 | CLIQ: Cheaper Clicks From Boxes — Interactive Small Object Detection | IEEE TGRS, 2026 | 10.1109/TGRS.2026.3677820 | Abstract only | No (interactive, not YOLO) | No | No | No — but confirms AI-TOD-R is now used by others |
| K19 | MSS: Metric-aligned Sample Selection and Critical Feature Sampling | arXiv 2306.16718 | arXiv 2306.16718 | Abstract only | No | No | Partly — affine-transformed distance selection by shape/rotation | Partially (RQ3, generic) |
| K20 | DCFL (AI-TOD-R paper itself) | IEEE TPAMI 2025 | 10.1109/TPAMI.2025.3634161 / arXiv 2412.11582 | Already read (log #38) | Baseline | **Yes, conceptually** — its "coarse step warrants sufficient and diverse positive samples for each object" (project page) | Partly — dynamic prior + Gaussian-mixture constraint | Baseline that any assignment claim must beat or match |

Context-only hits (HBB or unrelated, screened out): ScopeMamba-YOLO 2609.10156 and HDMamba-YOLO 2609.23061 (YOLO on AI-TOD, HBB), FBRT-YOLO 2504.20670 (AAAI 2025, AI-TOD HBB), LE-YOLO (Eng. Res. Express 2026, AITOD HBB), SCM-YOLO (Remote Sens. 2025, AI-TOD HBB), DCEDet (Remote Sens. 2025, AI-TODv2 HBB, label-assignment metric), MD-YOLO (Algorithms 2026, YOLO26 on VisDrone; abstract does not mention STAL), DORA (TPAMI 2026), SFDNet (2606.29029), SM-SCAM YOLO (J. Comput. Sci. 2025, PKLot; only cites AI-TOD-R), DAR-Det (CCIS 2025, no abstract available). **Implication:** YOLO-on-AI-TOD (HBB) is a crowded line; only the OBB/AI-TOD-R corner is thin.

### A.3 Notes on the closest competitors

**K1 — DIA-YOLO (IEEE Access 2025) — the most important new finding for RQ1.** What the full text says:
- The model is "specifically for oriented bounding box in overhead imagery"; the baseline is "the YOLOv11 oriented object detection model" (Implementation Setup, p. 150577).
- Dataset text: "The open-source satellite dataset AITOD [40] … contains eight classes including airplane, ship, person, bridge, swimming pool, wind-mill, storage-tank, and vehicle … The dataset consists of 18,730 images." Labels are converted to 8-point polygons (x1…y4). [40] is the AI-TOD ICPR 2021 paper, but Table 5 says "latest results … were obtained from the results tables in the following two papers [42], [43]", and [43] is the AI-TOD-R arXiv paper (2412.11582). The 8 classes and polygon labels match AI-TOD-R; **18,730 images ≠ AI-TOD-R's 28,036** and no split is described `[inference: a subset or a different split of AI-TOD-R]`.
- Table 3 (AITOD row): YOLO (YOLOv11-OBB) P 63.7 / R 26.0 / mAP50 34.5 / mAP50-95 17.2; DIA-YOLO 66.1 / 39.6 / 41.0 / 23.1.
- Table 5 lists 19 MMRotate-era methods at 800×800×3, 12 epochs (DCFL 40 epochs, 49.6 mAP50), and DIA-YOLO at 800×800×**4** (RGB + Marigold depth) at 12 / 40 / 815 epochs with 56.1 / 71.5 / 89.9 mAP50. The prose says "56.4% after 40 epochs" while the table shows 56.1 at 12 and 71.5 at 40 — an internal inconsistency in the paper.
- No AP_vt/AP_t/AP_s bins; no mention of the AI-TOD-R evaluator; GTX 3080 ×2, batch 4, "patience 50"; image sizes 256/512/768 in other experiments.
- **Consequence for C-3:** RQ1 can no longer be framed as an empty cell. It can be framed as: *the only YOLO-OBB numbers published against AI-TOD-R so far (that this scan found) mix datasets sizes, input modalities and schedules and report no size bins; a protocol-matched, size-binned evaluation with the official evaluator is still missing.* DIA-YOLO must be cited and its protocol differences tabulated; it is also a ready-made illustration of why protocol matching matters (12-epoch Table II rows vs an 815-epoch, 4-channel row in the same table).

**K2 — CDCEDet (JEIT, DOI 10.11999/JEIT260317) — the lead from 2026-10-07, status: partially resolved.**
- Verified: the DOI exists. `doi.org/api/handles` returns a URL record pointing to `https://jeit.ac.cn/cn/article/doi/10.11999/JEIT260317`, record timestamp 2026-07-19; the DOI registration agency is **ISTIC** (`doi.org/ra`), which explains the Crossref 404 and the absence from OpenAlex.
- Not verified: the article content. The publisher host did not respond (three attempts, 40–100 s timeouts). The only content seen is a search-engine summary: scale-adaptive anchor generation to increase positives for tiny objects, a quantile-adaptive IoU-threshold label assignment, and a frequency-adaptive fusion module; reported gains on AI-TODv2 and AI-TOD-R. **These are snippet claims, not evidence**; no numbers from the snippet are used.
- Overlap: same problem class as RQ2 (too few positives for tiny objects) on the same dataset; mechanism appears to be anchor/IoU-threshold based, not YOLO TAL/STAL and not shape-preserving. **Action:** obtain the PDF (library or the journal site from another network) before writing the introduction; treat as "partially overlapping, unverified" until then.

**K3 — SARFA-Net (JSTARS 2025) — closest mechanism to OA-STAL.** Full text (§III-B/C):
- Shape-Aware Sampling: candidates inside an ellipse in the GT's rotated frame, `a²/(0.5w)² + b²/(0.5h)² < η`, with `η = 1 − 0.5/r` (r = long/short side) — i.e. the region follows angle and aspect ratio and **contracts** for near-square boxes.
- Threshold Compensation Module: for small objects (`scale = ln(h·w)` below a pivot) the IoU threshold is scaled down by `S0·exp(−|scale−ϕ|/γ)`, and the paper "enlarge[s] the sampling ranges of these extreme-scale objects by 1.1 times".
- Datasets: DIOR-R, DOTA-v1.0, HRSC2016, FAIR1M-v1.0, UCAS-AOD — no tiny-object dataset; anchor-based S2A-Net baseline.
- **Difference from OA-STAL:** SARFA uses a fixed ×1.1 enlargement plus an adaptive IoU threshold in an ATSS-like anchor pipeline; OA-STAL uses a size-dependent similarity scale `k = max(1, s_ref/√(wh))` to reach a minimum area inside YOLO's anchor-point candidate test, with a long-side cap. A reviewer will see both as "shape-aware region + small-object compensation". OA-STAL's novelty claim must therefore rest on (i) the tiny-OBB regime (AI-TOD-R) where `k` is large (e.g. a 4×12 box gets k≈2.3), and (ii) the diagnosis, not on the mechanism class.

**K4 — EARL (TGRS 2023).** Full text: DED keeps candidates inside an inner ellipse `a²/(w/2)² + b²/(h/2)² < ξ`, `ξ = 1 − min(h,w)/(2·max(h,w))` (Eq. 4–6) — a **contraction**, not an enlargement; small targets are helped by ADS (sequential top-k across levels P7→P3) and "if a ground truth escapes from any samples, we assign it with the closest unassigned anchor point". **Difference:** EARL never grows the region of tiny boxes; its tiny-object safeguard is a nearest-anchor fallback. That fallback is a cheap, strong control that OA-STAL should be compared against.

**K5 — RDCNet (JSTARS 2026).** Full text: built on YOLOv8; AALA = multiscale centric sampling in the GT's rotated frame (`max(|Δx′|,|Δy′|) < r_l·s_l` **and** inside the GT), aspect-agnostic centerness (`1 − ‖(2Δx′/w, 2Δy′/h)‖/√2`) combined with RIoU and class probability in the task-aligned metric, plus a fallback (best-centerness point) when a GT gets no positive. Evaluated on DOTA-v1.0/v1.5, HRSC2016. **Overlap:** shape/orientation-aware candidate selection *inside a YOLO-family OBB assigner* already exists (2026). **Difference:** candidates must lie inside the (unenlarged) GT, so a sub-stride tiny box relies on the fallback; no tiny-object dataset.

**K6 — MFN-Net (RSL 2026).** Abstract only: "Similarity Distance-based Flexible Label Assignment (SFLA) … employs aspect ratio filtering and a dynamic matching mechanism to assign sufficient high-quality positive samples to small objects", evaluated on SODA-A and AI-TOD. Whether it is OBB on SODA-A, and whether it is YOLO-based, is **not stated in the abstract**. It cites AI-TOD-R. Must be read before claiming anything about "aspect-aware assignment for small objects on SODA-A".

### A.4 What 2025–2026 works citing AI-TOD-R do

- OpenAlex `cites:` gives 1 citing work for the arXiv record (W4405470106) and 6 for the TPAMI record (W4416323921); Semantic Scholar (merged record) gives 10. Union, de-duplicated: 13 works (4 appear in both indexes).
- **Use YOLO:** DIA-YOLO (K1, YOLOv11-OBB on oriented "AITOD"); YOLO NTD tobacco detector (Smart Agric. Technol. 2025, own UAV data; box type not stated in the abstract); SM-SCAM YOLO (PKLot). Only DIA-YOLO touches oriented AI-TOD data.
- **Modify label assignment:** MFN-Net (K6, SODA-A + AI-TOD). No citing work modifies STAL or a YOLO OBB assigner.
- **Use AI-TOD-R as a benchmark:** CLIQ (TGRS 2026, interactive detection on AITOD-R and Tiny-DOTA), DIA-YOLO (protocol unclear), CDCEDet (JEIT, snippet; not in either citation index).
- Coverage caveat: the JEIT paper and DIA-YOLO show that citation indexes miss or under-link relevant work (CDCEDet is in neither index; DIA-YOLO is in S2 but not in OpenAlex's `cites:` list). The re-scan must be repeated before submission.

### A.5 Limits of this scan

- arXiv `abs:` search is phrase-strict; OpenAlex search is relevance-ranked and only the top 40–50 results per query were screened; Semantic Scholar keyword search was rate-limited (HTTP 429) and could not be run. No Chinese-language databases (CNKI/Wanfang) were queried; JEIT shows that relevant Chinese-journal work exists.
- Several competitors are abstract-only (K6–K14). "Not found" in this note means "not found by these queries", not "does not exist".

---

## B. Resource facts (official pages only; all accessed 2026-10-08)

### B.1 Kaggle Notebooks (free tier)

Sources: [Kaggle docs — Notebooks](https://www.kaggle.com/docs/notebooks) ("Technical Specifications", "Adding a free GPU", "Save & Run All", "Modifying a Notebook-specific Environment"); [Kaggle docs — Efficient GPU Usage Tips](https://www.kaggle.com/docs/efficient-gpu-usage); [Kaggle docs — Datasets](https://www.kaggle.com/docs/datasets) ("Technical specifications"). These pages are JavaScript-rendered; they were rendered with headless Chrome and the text saved in `_tmp_scanB/raw/kaggle_docs_*.txt`. Kaggle states the specs hold "at time of writing" (page undated).

| Item | What the official page says (quoted or close paraphrase) |
|---|---|
| GPU types | "You can add a single NVIDIA Tesla P100 to your Notebook for free." Spec table also lists **"T4 x2 GPU Specifications: 2 Nvidia Tesla T4 GPUs, 4 CPU cores, 29 Gigabytes of RAM"** and "P100: 1 Nvidia Tesla P100 GPU, 4 CPU cores, 29 Gigabytes of RAM". TPU v3-8 ("TPU 1VM: 96 CPU cores, 330 GB RAM") also offered. |
| Weekly GPU quota | "You can use up to a quota limit per week of GPU. The quota resets weekly and is **30 hours or sometimes higher depending on demand and resources**." Experimental Colab-link promotion: Colab Pro / Pro+ subscribers get "15 and 30 hours of extra GPU hours per week" (may be ended "without prior notice"). |
| Availability | "Free GPU availability is limited: in busy times, you might be placed in a queue." |
| Max session length | "**12 hours execution time** for CPU and GPU notebook sessions and 9 hours for TPU"; for batch runs: "the entire Notebook must execute within 12 hours". |
| Idle timeout | Notebooks page: "20 minutes of idle time for your interactive session". GPU-tips page: interactive sessions "remain active until they reach the 60 minute idle timeout limit". **The two official pages disagree.** |
| Disk | "20 Gigabytes of auto-saved disk space (/kaggle/working)"; "Additional scratchpad disk space (outside /kaggle/working) that will not be saved outside of the current session" (size not stated). |
| RAM / CPU | GPU sessions: 29 GB RAM, **4 CPU cores**. |
| Internet | "make sure 'Internet' is enabled in the Settings pane (it will be by default if it's a new notebook)"; `!pip install` works with internet on. Phone/identity verification requirements are **not stated** on the pages read `[unverified]`. |
| Dataset storage | "200GB per dataset limit"; "200GB max private datasets". Datasets default to Private. |
| Multi-day training | No single run may exceed 12 h. Outputs saved in `/kaggle/working` can be attached as input to a later notebook ("use output files from another Notebook as a data source"). "The same Notebook can have multiple concurrent batch sessions" (maximum concurrency not stated). Kaggle API can push notebook versions without an interactive session. |

**Compute realism (arithmetic only, `[estimate]`, no measured throughput exists):** the proposal's unit is 1.4 M image-passes per 100-epoch run (14,000 trainval images × 100 — the trainval image count is itself still unverified). GPU-hours per run = 1.4×10⁶ / (r · 3600) for throughput r img/s: r = 100 → 3.9 h; r = 50 → 7.8 h; r = 25 → 15.6 h (exceeds one 12-h session → resume required). At 30 GPU-h/week, a ~20-run plan (14 runs + extra seeds) needs ≈ 2.6 / 5.2 / 10.4 weeks of quota for r = 100 / 50 / 25, before evaluation time. With only 4 CPU cores, on-the-fly mosaic augmentation of 800×800 images is a plausible bottleneck `[inference]`. The Modal-dollar budget in `t07-proposal.md` §4 does not transfer; it must be re-expressed in GPU-hours after a P100 and a T4×2 pilot.

### B.2 Ultralytics — assigner status, releases, checkpoints

Sources: `ultralytics/utils/tal.py`, `utils/loss.py`, `nn/tasks.py`, `nn/modules/head.py`, `cfg/default.yaml` on `main` (snapshots in `_tmp_scanB/raw/`); GitHub commits/compare/releases API; PyPI JSON; [docs — OBB task](https://docs.ultralytics.com/tasks/obb/).

- **Latest release:** `v8.4.174`, GitHub release published 2026-10-06T14:49:41Z; PyPI `8.4.174` uploaded 2026-10-06T14:50:52Z; `main/__init__.py` reads `8.4.174` on 2026-10-08.
- **Current main (last commit touching `tal.py`: `889b4fd659`, 2026-09-27):**
  - `TaskAlignedAssigner.__init__`: `self.stride = stride if stride is not None else [8, 16, 32]`; `self.stride_val = self.stride[1] if len(self.stride) > 1 else self.stride[0]` (= 16 for strides [8,16,32]). The loss passes the **model's** strides (`self.stride = m.stride`).
  - `RotatedTaskAlignedAssigner.select_candidates_in_gts`: on a **clone**, `wh_mask = gt[..., 2:4] < self.stride_val` and those sides are set to `stride_val`; corners via `xywhr2xyxyxyxy` (angle kept); anchor-point-in-rectangle test. **Answer: yes — every side below 16 px is raised to 16 px independently, angle unchanged.** There is no config switch; the floor is in the base assigner, so it applies to YOLOv8-OBB and YOLO11-OBB trained with the current package as well, not only YOLO26.
  - OBB loss: `v8OBBLoss` → `RotatedTaskAlignedAssigner(topk=10, alpha=0.5, beta=6.0, stride=model strides)`; YOLO26 uses `E2ELoss(v8OBBLoss)`: one-to-many `tal_topk=10`, one-to-one `tal_topk=7, tal_topk2=1`, one-to-many weight decays 0.8 → 0.1 over training.
  - `[inference from code]` With a P2 head the model strides become [4, 8, 16, 32], so `stride_val = stride[1] = 8`: **adding P2 silently changes the STAL floor from 16 to 8**. The proposal's "OA-STAL + P2" cell is therefore confounded unless the floor is fixed explicitly. (Main has `yolo26-p2.yaml` for detection but no OBB-P2 config.)
- **Version history of the OBB candidate floor** (each row verified with the GitHub compare API: tag contains commit or not):

| Ultralytics versions | OBB candidate-region rule | Evidence |
|---|---|---|
| ≤ 8.4.7 (includes 8.4.0 = YOLO26 release, 2026-01-14) | **No floor** for OBB (`select_candidates_in_gts` was a `@staticmethod` without enlargement) | diff of `d224aa5970` (PR #23378) removes `@staticmethod` and adds the floor |
| 8.4.8 – 8.4.38 | sides `< stride[0]` (8) set to `stride[1]` (16), **in place on `gt_bboxes`** | `d224aa5970` (2026-01-23); fixed by `4912cff3b6` (PR #24260, 2026-04-17, "Fix in-place obb `gt_bboxes` modification") |
| 8.4.39 – 8.4.127 | sides < 8 → 16, on a clone (= the rule described in the YOLO26 paper: s_min = smallest stride, s_ref = second stride) | `4912cff3b6` |
| ≥ 8.4.128 (current 8.4.174) | sides **< 16 → 16**, on a clone ("Make GT side clamp … monotonic") | `e82c8452d6` (PR #25912, 2026-08-24) |

  Consequences:
  1. The proposal's "paper says threshold 8, code says 16" (`t07-proposal.md` §2.1, log #39) is **a code change dated 2026-08-24**, not a standing paper/code mismatch. RQ2's "STAL-paper vs STAL-code" contrast is reproducible by version pinning, but a flag in one pinned fork is cleaner (same commit for every arm).
  2. `[inference from call order: get_pos_mask → select_candidates_in_gts → get_box_metrics → get_targets all use the same gt_bboxes]` in 8.4.8–8.4.38 the in-place edit probably also enlarged tiny GTs inside the ProbIoU alignment metric and the regression targets. Any YOLO-OBB number produced with those versions is not comparable to later ones.
  3. The public `yolo26*-obb.pt` checkpoints shipped with 8.4.0 (2026-01-14), nine days before the OBB floor appeared in public code; whether they were trained with an OBB floor cannot be told from the public history `[inference]`. The YOLO26 paper's STAL ablation is COCO/HBB only (log #38). → **STAL for OBB has no published evaluation at all.**
- **YOLO26-OBB checkpoints documented:** yes — `yolo26n/s/m/l/x-obb.pt`, trained on DOTAv1 at 1024 px; table columns "mAPtest 50-95 (e2e)", "mAPtest 50 (e2e)" (n: 52.4 / 78.9; x: 56.7 / 81.7). The page shows "Ultralytics YOLO27: Coming soon" and no YOLO27 OBB checkpoint. (arXiv 2510.09653v4 describes "YOLO27"; it is a third-party overview, not an Ultralytics release.)
- **Evaluation defaults that matter for AI-TOD-R:** `default.yaml` `max_det: 300`; detection heads carry `max_det = 300`; OBB val confidence default 0.01. The AI-TOD-R evaluator uses `maxDets = [1500]` (§B.3). Running Ultralytics' own validator with defaults would cap detections per image at 300 in scenes the project page describes as having "thousands of objects per image".

### B.3 AI-TOD-R — download route, evaluator, licence

Sources: [project page](https://chasel-tsui.github.io/AI-TOD-R/) (source `index.html` in the repo), [AI-TOD-R repo](https://github.com/Chasel-Tsui/AI-TOD-R) (README, tree, `configs/_base_/datasets/aitodr.py`, `mmrotate/datasets/aitodr_eval/aitodr_eval.py`), [AI-TOD README](https://github.com/jwwangchn/AI-TOD), [xView](http://xviewdataset.org/), AI-TOD-v2/NWD paper (arXiv 2206.13996, §3 p.5).

- **Download route:** the project page's only data button ("Dataset") links to a Google Drive file whose page title is **`labels.zip`**. No image link on the page; the AI-TOD-R README has installation instructions only (no dataset link, no dataset licence).
- **Images / xView:** AI-TOD-R uses the same 28,036 images as AI-TOD-v2 (AI-TOD-R PDF Table I; NWD paper: AI-TOD and AI-TOD-v2 share images). The AI-TOD README: download "xView training set" + "AI-TOD_wo_xview" (Google Drive) and run `generate_aitod_imgs.py`; "you only need to generate images". xView download is behind registration ("REGISTER … By registering, you agree to the following Terms and Conditions", challenge.xviewdataset.org/signup). **⇒ xView registration is required to rebuild the images** `[inference: labels-only release + AI-TOD image route]`. Not yet tested end-to-end (sizes, time, whether file names match `labels_v1`).
- **Licence:** AI-TOD dataset: CC BY-NC-SA 4.0 (AI-TOD README). AI-TOD-R dataset licence: **not stated** on the project page or README (the CC BY-SA 4.0 notice on the page covers the website template). Code: Apache-2.0. xView-derived images additionally fall under the xView Terms `[unverified content of those terms]` → keep any Kaggle copy **private**.
- **Official evaluator:** `AITODReval` (COCO-style re-implementation for rotated boxes): IoU thresholds 0.50:0.05:0.95; `maxDets = [1500]`; area ranges all / very tiny [2², 8²] / tiny [8², 16²] / small [16², 32²] / medium [32², 64²], where area = w·h of the rotated GT; IoU = `mmcv.ops.box_iou_rotated`. Annotation format: DOTA-style txt folders (`labels_v1/trainval/`, `labels_v1/test/`).
- **Official protocol (config):** train on `trainval`, **val = test = `labels_v1/test/`** (no held-out validation split), `RResize` 800×800, `RRandomFlip` 0.5, 2 images/GPU, SGD lr 0.0025, evaluation every 12 epochs.
- **Source datasets of AI-TOD:** "constructed based on publicly available aerial image datasets (Xia et al., 2018 [DOTA]; Lam et al., 2018 [xView]; Zhu et al., 2018 [VisDrone]; Airbus, 2018; Li et al., 2020b [DIOR])" (AI-TOD-v2 paper p.5). ⇒ DOTA-pretrained OBB checkpoints may have seen source imagery behind some AI-TOD-R test images `[inference; overlap not measured]`.

### B.4 SODA-A availability

Source: [SODA project page](https://shaunyuan22.github.io/SODA/) (Download section).
- Offered via "OneDrvie" (NWPU SharePoint) and BaiduNetDisk; licence **CC BY-NC 4.0**; benchmark/evaluation code in `SODA-mmrotate`.
- On 2026-10-08 the SODA-A OneDrive link redirected to `login.microsoftonline.com` (anonymous download **not** confirmed). BaiduNetDisk not tested (requires a Baidu client/account). ⇒ **SODA-A access is unverified and is a schedule risk for RQ4.**

---

## C. Reviewer critique (strict Q4-journal / Scopus-conference reviewer)

Written against C-3 as it stands in `t07-proposal.md` (2026-10-01) and ledger row C-3. Ordered by how likely each objection is to cause rejection.

**C1. The method is a parametric variant of a crowded mechanism class.**
- *Objection:* Shape/orientation-aware candidate regions (EARL 2023; SARFA-Net 2025 with small-object range enlargement and adaptive thresholds; SEDet 2025; FCOSR 2023; RDCNet 2026 inside a YOLOv8-based OBB assigner) and size floors (STAL) already exist. OA-STAL = "STAL's floor, but similarity-scaled". Where is the new idea?
- *Why it matters:* A T1 change with no insight is the most common rejection reason for assignment papers; reviewers will name SARFA-Net/EARL immediately.
- *What answers it:* (a) A related-work table along explicit axes — region shape (contracted ellipse / GT rectangle / per-side floor / similarity-enlarged rectangle), small-object compensation (none / ×1.1 / nearest-anchor fallback / min-area), detector family, tiny-object dataset. (b) Implement at least three mechanism controls in the *same pinned YOLO code*: per-side floor (STAL), nearest-anchor fallback (EARL-style), elliptical or fixed-×k region (SARFA-style). (c) A pre-declared, falsifiable prediction: OA-STAL helps mainly elongated tiny objects (ship, bridge; aspect-ratio ≥ 2 bins) and is neutral on near-square ones (vehicle, storage-tank). If the gain is not concentrated there, the "aspect-preserving" story fails.

**C2. "No YOLO detector on AI-TOD-R" is no longer true as written.**
- *Objection:* DIA-YOLO (IEEE Access 2025, 10.1109/ACCESS.2025.3603214) trains a YOLOv11-OBB baseline and a YOLO variant on an oriented "AITOD" set and compares with AI-TOD-R Table II. YOLO on AI-TOD (HBB) is also crowded (FBRT-YOLO, SCM-YOLO, LE-YOLO, ScopeMamba-YOLO…).
- *Why it matters:* An overstated gap in the introduction is easy to refute and damages credibility of the whole paper.
- *What answers it:* Cite DIA-YOLO; tabulate its protocol (18,730 vs 28,036 images; RGB+depth 4-channel input; 12/40/815 epochs; P/R/mAP50/mAP50-95 in Table 3 and mAP50 only in the Table II comparison; no size bins; no official evaluator; an internal 56.1 vs 56.4 inconsistency). Reframe RQ1 as "a protocol-matched, size-binned benchmark of YOLOv8/11/26-OBB on AI-TOD-R with the official evaluator and released prediction files". No "first" wording.

**C3. Comparison with MMRotate Table II is not apples-to-apples, even in "P1".**
- *Objection:* Table II = ImageNet-pretrained R50 backbones, 12 epochs, flip-only, 2 img/GPU, SGD lr 0.0025, 800×800. YOLO = different pretraining (COCO or DOTA), EMA, AMP, MuSGD/SGD schedule, one-stage anchor-point head, different NMS/NMS-free decoding. Matching only augmentation and epochs does not make it "protocol-matched".
- *Why it matters:* Any "YOLO is better/worse than DCFL" sentence will be attacked as confounded.
- *What answers it:* (a) Name P1 honestly ("short-schedule, flip-only YOLO recipe"), list every remaining difference in a table. (b) Re-train ≥1 MMRotate baseline from the official AI-TOD-R configs (e.g., RetinaNet-O or Oriented R-CNN) and score it with the same evaluator → an internal anchor that shows whether Table II is reproduced. (c) Add RTMDet-R (MMRotate) as the obvious real-time non-YOLO baseline, or justify its absence. (d) Report params, FLOPs and latency measured on one GPU for every row; never mix P1 and P2 numbers in one ranking.

**C4. Metric pipeline mismatch can silently change the conclusions.**
- *Objection:* Ultralytics' validator defaults (`max_det: 300`, conf 0.01 for OBB, its own mAP code, its angle convention) differ from `AITODReval` (`maxDets = [1500]`, area bins on rotated w·h, `box_iou_rotated`). Dense AI-TOD-R scenes ("thousands of objects per image") make the detection cap decisive for recall.
- *Why it matters:* AP_vt/AP_t are the headline numbers; a capped or differently binned evaluation invalidates them.
- *What answers it:* Export predictions to DOTA-format txt; evaluate **only** with `AITODReval`; set `max_det ≥ 1500` (including the YOLO26 end-to-end head's `max_det` attribute) and conf 0.001; validate the converter by scoring an MMRotate model's outputs and reproducing its AP; publish the converter.

**C5. STAL is a moving target in the code; the "paper vs code" framing is wrong.**
- *Objection:* The OBB floor did not exist in 8.4.0 (YOLO26 release), was added in 8.4.8 with an in-place GT modification, fixed in 8.4.39, and its threshold changed from 8 to 16 in 8.4.128 (§B.2). The floor is in the base assigner, so "TAL" for YOLOv8/11-OBB under the current package is not vanilla TAL; a P2 head changes `stride_val` from 16 to 8.
- *Why it matters:* Without control of these switches, RQ2/RQ3 differences can be version or stride artefacts; reviewers who check the repository will notice.
- *What answers it:* One pinned fork; explicit, stride-independent parameters (`floor_mode ∈ {none, per_side, similarity_min_area}`, `floor_threshold`, `floor_target`, `long_side_cap`); every arm (TAL / STAL-8→16 / STAL-16→16 / OA-STAL / controls) run on the same commit; commit hash and config in the paper. Replace the proposal's "paper vs code discrepancy" text with the dated version history.

**C6. Statistical validity is not established.**
- *Objection:* The plan has 1 seed for most arms (2 for the main pair). The only published STAL effect is +0.6 AP_S on COCO, and it reversed sign at s_ref = 8 and 32 (log #38) — effects of that size are within plausible seed noise for tiny-object AP `[inference; seed variance on AI-TOD-R not measured]`. The official AI-TOD-R config has **no validation split** (val = test), so tuning s_ref or the cap c on it is test-set leakage.
- *Why it matters:* A +0.5 AP claim from one seed tuned on test will not survive review.
- *What answers it:* (a) Carve a fixed validation split from trainval (by source image if crops share sources `[check AI-TOD file naming]`), tune s_ref/c there, touch test once. (b) ≥ 3 seeds for every arm in the main table (use YOLO26n or a shorter fixed schedule to afford it); report mean ± sd. (c) Paired per-image bootstrap CI for ΔAP_vt and ΔAP_t on the primary comparison (OA-STAL vs STAL-16), declared in advance. (d) Small, pre-declared hyper-parameter grid.

**C7. A diagnosis made of positive-sample counts is descriptive, and may be the wrong quantity.**
- *Objection:* "More positives" is not "better" (SimD argues excessive positives raise false positives; dense vehicle scenes add GT conflicts). YOLO26 trains a one-to-one branch with `topk2 = 1` that is used at inference in end-to-end mode (`head.py`: `preds["one2one" if self.end2end else "one2many"]`), while that branch receives **detached** features during training (`head.py` comment: "detach keeps one2one out of the backbone"), so backbone features are shaped by the one-to-many assignment only. Per-GT positive counts in one branch may therefore not explain end-to-end AP. If OA-STAL fails, what is left?
- *Why it matters:* Q4/Scopus-conference reviewers accept analysis papers only when the analysis yields a non-obvious, testable finding.
- *What answers it:* Measure, per size × aspect-ratio bin and per branch (o2m, o2o): zero-positive GT rate, positives per GT, multi-GT ambiguity rate vs local density, and link each to per-GT recall/AP. Then perform an assigner-only intervention that moves these quantities and check AP moves the predicted way. A benchmark + mechanism paper without a working method is a plausible fallback only if such a finding exists (e.g., a 16-px floor helps very tiny objects but hurts elongated tiny ones, or creates conflicts in dense scenes); a plain leaderboard is not enough.

**C8. Generalisation rests on one uncertain dataset.**
- *Objection:* SODA-A access is unverified (OneDrive link → Microsoft login; Baidu untested), images are large (mean 4761×2777) and need cropping, objects are larger (15.6 ± 7.6 px) so a 16-px floor touches a different fraction of objects, and the evaluator differs. MFN-Net (2026) already reports a small-object assignment change on SODA-A + AI-TOD.
- *Why it matters:* The proposal's own Q3 condition needs two datasets; with only AI-TOD-R the claim is single-dataset.
- *What answers it:* Download SODA-A in week 1 (go/no-go). Pre-declare a reduced protocol (fixed crop subset, fixed epochs, internal baseline). Name a fallback second dataset in advance (e.g., DOTA-v2 train→val as in DCFL's ablation) and justify it. Report gains against the fraction of objects under the floor per dataset — a mechanism-consistent pattern is stronger than two AP numbers.

**C9. Compute plan is not realistic yet on Kaggle.**
- *Objection:* Kaggle offers ~30 GPU-h/week (P100 or 2×T4), 12-h sessions, 4 CPU cores, 20 GB persistent output (§B.1). The ~14-run plan plus 3 seeds is ~20+ runs; at assumed 25–100 img/s that is ≈ 2.6–10.4 weeks of quota before evaluation (§B.1 arithmetic). Rebuilding AI-TOD-R images needs xView registration and a generation step. SODA-A crops multiply cost.
- *Why it matters:* A 14-week schedule with an unmeasured denominator is the most likely way the project ends with an incomplete table.
- *What answers it:* Week-1 pilot on P100 and T4×2: img/s, VRAM, one `AITODReval` pass time. Resume-safe training (save `last.pt` every epoch to `/kaggle/working`, chain sessions by attaching the previous version's output). Use YOLO26n for seeds/ablations at a fixed shorter schedule and YOLO26s for headline rows; drop YOLOv8 if YOLO11 covers the "previous generation" point; limit P2 variants. Re-express §4 of the proposal in GPU-hours with explicit go/no-go thresholds.

**C10. Initialisation may leak test imagery and favour YOLO.**
- *Objection:* Official `yolo26*-obb.pt` weights are trained on DOTAv1; AI-TOD (hence AI-TOD-R) is built partly from DOTA images (AI-TOD-v2 paper §3). DOTA-pretrained OBB weights may have seen source imagery of some test tiles, and they are a stronger initialisation than the ImageNet backbones of Table II.
- *Why it matters:* A reviewer can attribute any YOLO advantage to pretraining overlap rather than architecture or assignment.
- *What answers it:* Initialise from COCO detection weights (or ImageNet backbones) for all reported rows; if DOTA-OBB weights are also used, report them separately and evaluate a test subset excluding DOTA-sourced tiles (requires a source mapping — check whether AI-TOD file names encode the source dataset).

---

## Bottom line: does the C-3 gap still hold?

**Partly.**

- **RQ1 (YOLO-OBB on AI-TOD-R): partly.** DIA-YOLO (IEEE Access 2025) already places YOLOv11-OBB-based numbers next to AI-TOD-R Table II, under a non-matching protocol without size bins. A *protocol-matched, size-binned, official-evaluator* benchmark of YOLOv8/11/26-OBB was not found. The sentence "the AI-TOD-R benchmark has no YOLO detector" is true of the AI-TOD-R paper but **not** of the literature; it must be reworded.
- **RQ2 (STAL on tiny data): holds within this scan.** No isolated STAL evaluation on AI-TOD/AI-TOD-R/SODA-A/VisDrone was found; STAL for OBB has no published evaluation at all, and its OBB rule changed three times in 2026 after being absent in the 8.4.0 release (§B.2). This is now the strongest part of C-3, provided the version history is handled as in C5.
- **RQ3 (OA-STAL): partly.** The exact similarity-preserving min-area floor inside YOLO's TAL candidate step was not found, but the mechanism class (shape-aware/elliptical regions, small-object enlargement, YOLO-family aspect-adaptive assignment) is populated; the JEIT lead (CDCEDet, label assignment for tiny objects on AI-TOD-R, snippet only) remains unverified.
- **Tier:** stays **T1**. Nothing found raises it; DIA-YOLO and SARFA-Net/RDCNet narrow it.
- **What the admin should consider (not done here):** a ledger REVISION of C-3 (cause: new evidence — DIA-YOLO; STAL version history; SARFA-Net/RDCNet; JEIT lead), keeping the band "Q4 / Scopus conference, conditional" but replacing "highly feasible" by conditions that are now concrete: (1) RQ1 reframed and DIA-YOLO cited; (2) evaluation through `AITODReval` with `max_det ≥ 1500`; (3) a pinned fork with explicit floor parameters; (4) validation split + ≥3 seeds; (5) Kaggle pilot and xView access confirmed; (6) JEIT and MFN-Net full texts read. Corrections needed in `t07-proposal.md`: §0/§2.1 (RQ1 wording; "paper vs code" → version history), §3 (xView requirement now resolved: labels-only release; dataset licence of AI-TOD-R not stated), §4 (Modal dollars → Kaggle GPU-hours), §4.3 (P2 changes `stride_val`).

## Glossary

| English | Vietnamese | Short note |
|---|---|---|
| candidate selection / candidate region | chọn ứng viên / vùng ứng viên | Anchor points allowed to compete for a GT before task-aligned ranking |
| size floor | ngưỡng sàn kích thước | STAL raises GT sides below a threshold to a target size, for candidate selection only |
| protocol-matched | cùng giao thức | Same data split, schedule, augmentation and evaluator as the reference table |
| official evaluator (`AITODReval`) | bộ đánh giá chính thức | AI-TOD-R's rotated COCO-style AP with very tiny/tiny/small/medium bins, maxDets 1500 |
| one-to-one / one-to-many branch | nhánh một-một / một-nhiều | YOLO26 end-to-end training: o2o (topk2 = 1) is used at inference in end-to-end mode, o2m otherwise / for training |
| test-set leakage | rò rỉ tập kiểm tra | Tuning hyper-parameters on the split used for final reporting |
