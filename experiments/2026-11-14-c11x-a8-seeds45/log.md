# 2026-11-14 · C11x phụ lục A3: R1 và A8 × seed 4–5 (đợt 1), phán quyết P2 tạm thời

Ghi ngày 14/11/2026 bởi Claude Code (Opus 5.5), chạy thay người dùng khi người dùng vắng (đã được giao quyền chạy
và mở PR, không merge). Số trong file này lấy từ log đợt 1 trên Colab và từ `experiments/2026-11-07-c11x-seeds1to5/results_long.csv`.
**Đợt 2 (phân tích chính thức) chưa chạy**; xem mục "Chưa làm".

## Chạy ở đâu

- Colab A100-SXM4-40GB, acc Colab của người dùng, Drive nhóm (`NCKH`) gắn bằng Colab CLI 0.8.0 (`colab drivemount`).
- Code: `main` commit `dff1b65` (phụ lục A3 đã khoá, ngày 10/11). `ultralytics 8.4.174`, **torch 2.14.1+cu130**,
  numpy 2.4.6, Python 3.13.16. Seed 4–5 ngày 07/11 dùng torch 2.11.0+cu130.
- Bắt đầu 13/11 14:53 UTC, kết thúc đợt 1 lúc 17:53 UTC.

## Sai lệch so với cách chạy ghi trong notebook

1. **Không chạy bằng "Run all".** Notebook `notebooks/C11x_train_a8_colab.ipynb` được điều khiển từ máy Windows qua Colab CLI.
   Chạy notebook qua `jupyter nbconvert` bị treo vì các dòng `!` của Colab gửi `colab_request` tới giao diện. Notebook
   được chuyển sang script `a8_phase1_run.py` bằng `nb2py.py` (cả hai trong thư mục này), với đúng ba thay đổi:
   - `drive.mount("/content/drive")` → `assert Path("/content/drive/MyDrive").exists()` (Drive gắn trước bằng CLI);
   - mỗi dòng `!lệnh` → `subprocess.run(lệnh, shell=True)` (không kiểm mã lỗi, giống `!`);
   - `display(x)` → `print(x)`.
   Logic, luật, đường dẫn ghi kết quả, `PHASE = "train"`, `BRANCH = "main"` giữ nguyên.
2. **Thời gian:** 0,77–0,80 giờ/run train (A2 s4 0,80; A8 s4 0,78; A8 s5 0,77), so với 0,57 giờ ở log 07/11. Nguyên nhân chưa kiểm.
3. Không có sai lệch nào khác so với phụ lục A3. Không thêm seed, không đổi luật.

## Kiểm trước khi train

- Phụ lục A3 có trên `main`; preregistration của nhánh trùng `main`; Ultralytics 8.4.174; GPU A100.
- Test: `scripts/c11` (gồm `test_fastpath.py`), `scripts/c11x/tests`, `scripts/rq2` (2 file): **qua hết**. Lưu ý
  `test_fastpath.py` từng trượt ở đợt 2 ngày 07/11 (cũng torch 2.14.1); lần này qua. Nguyên nhân khác biệt chưa kiểm.
- Split dataset dựng lại trùng `split_manifest.json` ngày 20/10.
- Trước khi chạy đã kiểm Drive: chưa có `runs-woX-A8` và `c11x-a8-results`, tức A8 seed 4–5 chưa ai chạy.

## R1 (phụ lục A3 mục 3)

A2 seed 4 train lại vào `runs-woX-A8/c11_A2_s4`, so với `runs-woX/c11_A2_s4` (07/11):

| | Δ | Ngưỡng | |
|---|---|---|---|
| AP test, head e2e | −0,00098 | ≤ 0,005 | đạt |
| mAP50-95 val, epoch cuối | −0,00009 | ≤ 0,005 | đạt |

**Khớp** (`c11x-a8-results/a8_env_check.json` trên Drive). Theo mục 3: train A8 × seed 4, 5 vào `runs-woX`, so với A0, A2
seed 4–5 ngày 07/11. R1 chỉ chấm head e2e (đúng notebook khi khớp): AP 0,1360; AP_vt 0,0552; AP_t 0,1288; AP_s 0,1984.

## Kết quả A8 (head e2e, test; in ra 4 chữ số bởi `train_eval`)

| Seed | AP | AP_vt | AP_t | AP_s |
|---|---|---|---|---|
| 4 | 0,1346 | 0,0429 | 0,1243 | 0,2022 |
| 5 | 0,1304 | 0,0405 | 0,1191 | 0,2035 |

Head nms (mô tả): seed 4 AP 0,1367, AP_vt 0,0486; seed 5 AP 0,1299, AP_vt 0,0387. AP_m của A8 không in trong log đợt 1.

## P2 tạm thời (phụ lục A3 mục 4) — `p2_verdict_provisional.json`

A0, A2 lấy từ `2026-11-07-c11x-seeds1to5/results_long.csv` (6 chữ số); A8 từ bảng trên (4 chữ số).

| | Seed 4 | Seed 5 | Trung bình |
|---|---|---|---|
| Δ AP_vt (A8 − A0) | −0,00007 | −0,00255 | −0,00131 |
| Δ AP_vt (A8 − A2) | −0,00858 | −0,01127 | −0,00993 |

- **P2a: "Không lặp lại".** Cả hai seed không > 0. Với sai số làm tròn ±0,00005 của A8, cận trên của Δ (A8 − A0) vẫn âm
  ở cả hai seed (−0,00002; −0,00250), nên phán quyết không đổi khi có số đủ chữ số.
- **P2b: không đạt** (trung bình −0,0099 < −0,006).
- Theo mục 4, bài **không được** viết rằng sàn tối thiểu đủ cho mức tăng AP_vt.
- Phụ lục A3 đã ghi trước: P2a đạt khoảng 65% nếu hiệu thật bằng +0,0071 như seed 1–3 (thăm dò), khoảng 1,4% nếu hiệu thật
  bằng 0. Kết quả ở đây gần 0 ở cả hai seed.

## Chưa làm

- **Đợt 2** (`PHASE = "analyze"`): `p2_verdict.json` chính thức, `results_long.csv` đầy đủ chữ số (có AP_m), bootstrap theo
  cảnh, số phận GT, M1/M2 cho A8. Bị chặn vì phiên Colab mới cần người dùng cấp lại quyền Drive trên trình duyệt (lần thử
  tự động trả 400). Notebook đợt 2 tự đọc các run ở `runs-woX` theo `a8_env_check.json`.
- Head nms của R1 không chấm (notebook chỉ chấm khi R1 không khớp).

## File

- Trong repo: `log.md`, `p2_verdict_provisional.json`, `a8_phase1_run.py`, `nb2py.py`.
- Trên Drive `NCKH/repo/NCKH/experiments/`: `runs-woX-A8/c11_A2_s4/` (R1), `runs-woX/c11_A8_s4/`, `runs-woX/c11_A8_s5/`
  (trọng số, `eval_*.json`, `dota_*`), `c11x-a8-results/a8_env_check.json`.
