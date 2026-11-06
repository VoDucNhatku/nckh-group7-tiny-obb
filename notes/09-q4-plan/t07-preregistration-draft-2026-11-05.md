# Preregistration (DRAFT) — C-11 confirmatory runs

> **Đã thay thế 06/11/2026** bằng phụ lục A2 của `experiments/preregistration.md`. Không chép file này sang `experiments/`. Lý do bỏ MEI 0,005 và phép H3 trên seed 1–5 ghi ở A2, mục 8.

**Status:** draft written by Devin on 2026-11-05 at the team's request. It becomes the preregistration only when the team agrees, copies it to `experiments/preregistration.md` and commits it **before** any new training or test-set evaluation. After that the file is not edited (AGENTS.md, `experiments/README.md`).

**Already seen (exploratory, declared as such):** 12 runs A0/A1/A8/A2 × seeds 1–3, e2e head, woX test set (`C11_colab.ipynb`, explained in `notes/08-c11-execution/`). The predictions below are derived from the label-only analysis (`experiments/2026-11-05-rq2-offline-woX/`), which used no detector output.

## 1. Fixed design

- Data: AI-TOD-R woX; train/val/test split of `split_manifest.json` (2026-10-20). Test touched once per run.
- Model/recipe: YOLO26n-OBB, Ultralytics 8.4.174, `c11_pipeline.RECIPE` unchanged (24 epochs, SGD, imgsz 800, flips only, batch 16). Evaluate `last.pt`.
- Evaluator: AITODReval as in Gate 2, `max_det = 12000`, `conf = 0.001`.
- Heads: **e2e is primary**; nms reported as secondary for every run.
- New seeds: **4 and 5** for A0, A8, A2 (6 runs). A1 not extended.

## 2. Hypotheses and predicted signs

| ID | Hypothesis | Test | Predicted |
|---|---|---|---|
| H1 | The AP_vt gain of a floor comes from GTs that A0 leaves without candidates | Per-GT recall (IoU ≥ 0.5, score ≥ 0.05; `rq2_recall.py`) on test very tiny GTs, split by `A0_cand == 0`; Δrecall(A2 − A0) | Δ on A0-starved GTs > 0 and larger than Δ on non-starved GTs |
| H2 | Smaller floors lose more dense GTs at the conflict stage | Δrecall(A2 − A8) on very tiny GTs with ≥ 3 GT centres within 16 px vs isolated | Δ(dense) > Δ(isolated); proxy predicts 3.5 % vs 5.7 % zero positives (test, dense vt) |
| H3 | Floors raise AP_vt | Paired scene-clustered bootstrap, B = 10,000, seeds 1–5, A2 − A0 and A8 − A0 | Δ > 0, CI excludes 0 **and** Δ ≥ MEI |
| H4 | No claim on overall AP | Reported, not tested | — |

**MEI (minimal effect of interest):** 0.005 AP_vt (0.5 points). Differences below MEI are reported as "no practically relevant difference", not as equivalence.

## 3. Analysis code

`scripts/rq2/rq2_recall.py` (per-GT recall, logistic model `detected ~ arm * starved_A0 + log(short) + log1p(nn16) + C(cls)`, SEs clustered by `scene_key`), `c11_bootstrap.multi_pair_bootstrap` with `KEYS = (AP_vt, AP_t, AP_s, AP)`. Report both the scene-clustered CI and the per-seed min–max.

## 4. Decision rules

- H1/H2 supported only if the sign matches **and** the 95 % cluster-bootstrap CI of the difference-in-differences excludes 0.
- Any deviation from this file (crash, OOM batch change, missing seed) is listed in the paper.
