# 2026-11-07 · C11x: train seed 4–5 (A0, A2) và R0, phán quyết P1, M1/M3 trên test

Ghi ngày 07/11/2026 bởi Claude Code (Opus 5.5), từ các file trong thư mục này, notebook kèm output
`C11x_train_confirm_colab.ipynb` và output đợt 1 người chạy dán lại. Số đã kiểm lại từ file; suy luận chưa có
phản biện độc lập.

## Chạy ở đâu

- Colab, acc Colab của một thành viên, Drive của nhóm mount qua shortcut `NCKH`. Notebook
  `notebooks/C11x_train_confirm_colab.ipynb`, hai đợt (phụ lục A2 của `experiments/preregistration.md`).
- **Đợt 1 (`PHASE = "train"`)**: A100-SXM4-40GB, code commit `d8b9d99` (`main`, phụ lục A2 đã khóa),
  `ultralytics 8.4.174`, torch 2.11.0+cu130, numpy 2.4.6, Python 3.13.16. Train R0 (A2 seed 1, ghi vào
  `runs-woX-R0`) và A0, A2 × seed 4, 5 (ghi vào `runs-woX`), mỗi run 24 epoch, khoảng 0,57 giờ/run; chấm 9 lần trên test.
- **Đợt 2 (`PHASE = "analyze"`)**: A100-SXM4-40GB (không đổi sang L4; đợt 2 không kiểm loại GPU), code commit
  `5934ecb`, torch 2.14.1+cu130, cv2 4.14.0, shapely 2.2.0, numpy 2.4.6 (`env.json`). `5934ecb` là commit
  "Created using Colab" đẩy thẳng lên `main` lúc 06:48 07/11: so với `d8b9d99` chỉ đổi dòng `PHASE` trong notebook,
  không đổi code hay preregistration. PR kèm thư mục này trả notebook trên `main` về bản dựng từ
  `scripts/c11x/build_confirm_notebook.py`.
- Không có run nào bị Ultralytics đổi batch (`batch_changed = False` ở cả 20 dòng `results_long.csv`).

## Sai lệch so với kế hoạch (đều xảy ra trong lúc chạy, trước khi thấy kết quả phân tích tương ứng)

1. **R0 không khớp** (`r0_check.json`): Δ AP test e2e = +0,0015 (ngưỡng 0,005, đạt); Δ mAP50-95 val ở epoch 24
   = −0,0186 (ngưỡng 0,005, trượt). Theo phụ lục A2 mục 5: không gộp seed 1–3 với seed 4–5 trong bài, báo riêng hai
   nhóm và báo độ lệch. Nguyên nhân của độ lệch val chưa kiểm.
2. **Bỏ `test_fastpath.py` ở đợt 2.** Test này trượt ở đợt 2 (AP đường nhanh 0,286052 so với đường cũ 0,285825
   trên dữ liệu giả, ngưỡng 1e-6) dù đã qua ở đợt 1 và ở notebook val. Đợt 2 chạy trong môi trường Colab khác
   (torch 2.14.1 so với 2.11.0 của đợt 1; phiên bản cv2/shapely của đợt 1 không được ghi). Test kiểm
   `predictions_to_results_fast`, đường chấm chỉ dùng ở đợt 1; đợt 2 đọc `eval_*.json` và `evalcache_*.npz` có sẵn.
   48 test còn lại của `scripts/c11`, 51 test của `scripts/c11x` và 11 test của `scripts/rq2` đều qua.
   Nguyên nhân trượt chưa kiểm (giả thuyết: `cv2.minAreaRect` hoặc shapely đổi phiên bản).
3. **Dựng lại head nms của A2 seed 1–3.** Ngày 07/11, trên Drive, 8 run cũ (A1 s2–3, A2 s1–3, A8 s1–3) mất
   `eval_nms.json` và `evalcache_nms.npz` (đa số mất cả `dota_nms/`); chỉ còn `evalcache_nms.unsorted.npz`, bản cache
   gốc giữ lại khi sắp xếp ngày 30–31/10. Thùng rác của acc chủ trống. Ai xóa và khi nào: chưa rõ. Ghi chú
   `notes/08-c11-execution/t07-c11x-handoff-2026-10-30.md` mục 1 ghi nms đã chấm đủ 12/12 run. Một ô thêm vào
   notebook (ô 11) tính lại `eval_nms.json` của A2 s1–3 bằng `c11_bootstrap.stats_fast` trên cache gốc (thêm trường
   `_reconstructed_from`) và chép cache để ô sau sắp lại. Đối chiếu với ghi chú 30/10: AP nms A2 trung bình seed 1–3
   = 0,1366 (ghi chú: 0,1366); Δ AP_vt nms A2 − A0 = +0,0071 (ghi chú: +0,0071). Chỉ ảnh hưởng bảng head nms
   (mô tả); P1 và M1/M3 dùng head e2e.

## Kết quả

### P1 (phụ lục A2 mục 6): Δ AP_vt, A2 − A0, head e2e, seed 4–5

| Seed | A0 | A2 | Δ |
|---|---|---|---|
| 4 | 0,042974 | 0,051482 | +0,008508 |
| 5 | 0,043047 | 0,051774 | +0,008728 |

Trung bình +0,008618 ≥ MEI_vt = 0,006 và cả hai seed > 0: **"Lặp lại được"** (`p1_verdict.json`; tính lại từ
`results_long.csv`, khớp). Phạm vi: AI-TOD-R woX, YOLO26n-OBB, recipe C11, 24 epoch, test woX.

Số gộp seed 1–5 trong `p1_verdict.json` và `ci_scene_seed.csv` (Δ +0,0089, CI gộp [0,0006; 0,0171]) **không được
dùng trong bài** vì R0 không khớp (`pooled_allowed: false`). Δ theo từng seed 1–3 (e2e): +0,0045; +0,0155; +0,0070.

Head nms (mô tả), Δ AP_vt seed 4, 5: +0,0081; +0,0081. Δ AP tổng e2e seed 4, 5: +0,0063; +0,0014.

### M1 (phụ lục A2 mục 8): DiD recall, GT rất nhỏ A0 không cấp ứng viên so với GT rất nhỏ khác, A2 − A0, head e2e, IoU 0,5

Notebook tính trên seed 1–5 gộp (`mechanism/mech_*.json`, `summary.json`). Vì R0 không khớp, `m1_by_seed_group.py`
tính lại riêng từng nhóm seed (`m1_by_seed_group.json`); dòng seed 1–5 trùng đúng với notebook (assert trong script).

| Score | Seed | Δ | CI theo cảnh (B = 10.000) | CI gộp cảnh + seed (t, n − 1 bậc) |
|---|---|---|---|---|
| 0,25 (chính) | 1–3 | +0,068 | [0,055; 0,080] | [0,033; 0,103] |
| 0,25 (chính) | 4–5 | +0,067 | [0,054; 0,078] | [−0,023; 0,157] |
| 0,05 (độ nhạy) | 1–3 | +0,135 | [0,116; 0,152] | [0,094; 0,177] |
| 0,05 (độ nhạy) | 4–5 | +0,136 | [0,118; 0,154] | [−0,005; 0,277] |

- Cả 10 giá trị theo seed đều dương (score 0,25: 0,062 đến 0,078; score 0,05: 0,130 đến 0,143).
- CI gộp của seed 4–5 chứa 0 vì chỉ có 2 seed (hệ số t với 1 bậc tự do là 12,7), không phải vì Δ đổi dấu. Phải
  viết rõ điều này trong bài.
- M1 đã được xem trên val trước khi khóa phụ lục A2 (mục 1), nên trên test là kiểm lại, không phải xác nhận độc
  lập. DiD là so sánh có đối chứng giữa hai nhóm GT, không loại được mọi khác biệt giữa hai nhóm (ví dụ kích thước
  trong bin vt).

### M3 (mô tả)

Bảng số phận GT và recall theo IoU ở `mechanism/fate_by_arm_bin_*.csv` và `mechanism/recall_iou_by_arm_bin_*.csv`.
Chưa đọc kỹ; dùng khi viết phần cơ chế.

## File

- Trong repo: `p1_verdict.json`, `summary.json`, `r0_check.json`, `env.json`, `results_long.csv`,
  `ci_scene_seed.csv`, `bootstrap_e2e_B10000.json`, `bootstrap_nms_B2000.json`, `mechanism/*.csv|json`,
  `m1_by_seed_group.py|json`, notebook kèm output.
- Chỉ ở máy (`_local/`, Git bỏ qua) và trên Drive `NCKH/repo/NCKH/experiments/c11x-seeds1to5-results/mechanism/`:
  `rq2_test/rq2_per_gt.csv.gz` (bảng theo GT, có hình học nhãn) và `fates_e2e_score*/*.parquet` (20 file, khoảng 27 MB).
- Trọng số và dự đoán `dota_*` ở Drive `runs-woX/`, `runs-woX-R0/`.
