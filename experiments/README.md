# experiments/

One folder per run: `experiments/<YYYY-MM-DD>-<run-name>/`, containing

- `config.yaml` — every hyper-parameter and the candidate-rule arm (A0, A1, A2, A8, A4, K<k>), seed, Ultralytics version;
- `log.md` — where it ran (Kaggle P100 / 2×T4 / Modal), wall-clock time, images/sec, issues;
- `metrics.json` — AITODReval output (AP, AP_vt, AP_t, AP_s, AP_m, per class);
- `predictions/` link (not the file itself if > 50 MB).

Do not commit images, datasets or weights (`*.pt`); `.gitignore` blocks them.
`preregistration.md` (PREREG-C11X-v1, 30/10/2026) lives directly in this folder. After it is merged it is never edited;
changes go into a dated appendix committed before the run or scoring they affect.

The C11 runs (`runs-woX/`) and C11x runs (`runs-woX-c11x/`) are written by the Colab notebooks to the team Drive
(`NCKH/repo/NCKH/experiments/`); weights stay there. Copy the JSON/CSV outputs here through a PR.
