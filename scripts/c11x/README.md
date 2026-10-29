# scripts/c11x — code cho kế hoạch C11x

Kế hoạch: [`notes/08-c11-execution/t07-c11-novelty-plan-2026-10-30.md`](../../notes/08-c11-execution/t07-c11-novelty-plan-2026-10-30.md).
Preregistration: [`experiments/preregistration.md`](../../experiments/preregistration.md).

Mọi module viết cho `ultralytics==8.4.174` và có kiểm phiên bản.

## Các file

| File | Việc | Dùng `scripts/c11` (Drive)? |
|---|---|---|
| `c11x_assign.py` | Quy tắc vùng ứng viên A0/A1/A8/A2 và sàn theo số ứng viên `K<k>`; vá `RotatedTaskAlignedAssigner`; `PositiveRecorder` ghi số ứng viên / mẫu dương theo GT cho nhánh o2m, o2o | không |
| `c11x_train.py` | Train một run với recipe C11, tự resume, ghi `c11x_arm.json`, `c11x_kstats.jsonl`, `c11x_done.json` | không (notebook so `RECIPE_C11` với `c11_pipeline.RECIPE`) |
| `c11x_pergt.py` | Hướng 2 và 4: gán mẫu tại checkpoint cuối trên val, khớp từng GT, mô hình recall, sai số góc | không |
| `c11x_results.py` | Gộp run (sửa đếm trùng ô #32), bảng theo seed, gộp CI theo cảnh với seed, kiểm `scene_key`, gọi bootstrap | gọi `c11_bootstrap` qua tham số |
| `build_notebooks.py` | Sinh `notebooks/C11x_analysis_colab.ipynb` và `notebooks/C11x_train_kfloor_colab.ipynb` | — |
| `tests/` | 39 test (pytest) | không |

## Chạy test

```bash
pip install "ultralytics==8.4.174" shapely statsmodels pytest nbformat
cd scripts/c11x && python -m pytest -q tests -p no:cacheprovider
```

- `tests/test_c11x_train.py` train thật 2 epoch trên CPU (khoảng 6 phút): ngắt sau epoch 1, chạy lại để resume, rồi kiểm file done.
- Notebook bỏ file test này cho nhanh.

## Sửa notebook

Sửa `build_notebooks.py`, rồi chạy `python scripts/c11x/build_notebooks.py`. Không sửa tay file `.ipynb`.
