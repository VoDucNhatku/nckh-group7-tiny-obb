# experiments/

One folder per run: `experiments/<YYYY-MM-DD>-<run-name>/`, containing

- `config.yaml` — every hyper-parameter and the candidate-rule arm (A0–A7), seed, Ultralytics commit;
- `log.md` — where it ran (Kaggle P100 / 2×T4 / Modal), wall-clock time, images/sec, issues;
- `metrics.json` — AITODReval output (AP, AP_vt, AP_t, AP_s, AP_m, per class);
- `predictions/` link (not the file itself if > 50 MB).

Do not commit images, datasets or weights (`*.pt`); `.gitignore` blocks them.
`preregistration.md` (week 3) lives directly in this folder and is never edited after RQ3 training starts.
