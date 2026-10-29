# Preregistration — PREREG-C11X-v1

**Ngày viết:** 30/10/2026. Ngày khoá là ngày commit merge vào `main`. **Người viết:** Claude Code (Opus 5.5), theo yêu cầu của nhóm trưởng; nhóm duyệt qua PR.
**Kế hoạch đầy đủ:** `notes/08-c11-execution/t07-c11-novelty-plan-2026-10-30.md`.
**Quy tắc:** sau khi merge, không sửa file này. Mọi thay đổi ghi thành **phụ lục có ngày** ở cuối file, kèm lý do. Phụ lục chỉ hợp lệ nếu commit **trước** phép chấm hay run mà nó ảnh hưởng.

## 1. Trạng thái dữ liệu đã có

- 12 run `runs-woX/c11_<arm>_s<seed>` (A0, A1, A8, A2 × seed 1–3), train 20–21/10/2026, **trước** khi có preregistration. Toàn bộ là **thăm dò**. Không câu xác nhận nào được dựa trên chúng.
- Đã xem:
  - điểm test head e2e của cả 12 run;
  - điểm test head nms của A0 × 3 run và A1 × 1 run;
  - bootstrap e2e với B = 1.000 (`C11_colab.ipynb` #30, #32, #34).
- Chưa xem: điểm nms của 8 run còn lại; mọi phân tích theo GT trên val; log `c11_assign_diag.jsonl`.

## 2. Giao thức chung (giữ như C11)

- **Mô hình và train:** YOLO26n-OBB khởi tạo từ `yolo26n.pt` (COCO); `ultralytics==8.4.174`; recipe `RECIPE_C11` trong `scripts/c11x/c11x_train.py`, phải khớp `c11_pipeline.RECIPE` (notebook kiểm); 24 epoch; chấm `last.pt`.
- **Dữ liệu:** AI-TOD-R, giao thức woX; split dựng lại bằng `build_yolo_dataset(seed=0)` và phải khớp `split_manifest.json` ngày 20/10.
- **Chấm:** AITODReval gốc qua `c11_pipeline.predict_and_eval`, `max_det = 12.000`, hai head e2e và nms.
- **Head chính** cho mọi giả thuyết là **e2e** (head suy luận mặc định của YOLO26). nms báo song song, không dùng để chọn kết luận.

## 3. Giả thuyết trên 12 run sẵn có (bán-xác nhận: dữ liệu chưa xem, nhưng run là thăm dò)

**MEI**, theo proposal §8.5: lấy độ lệch chuẩn theo seed của A2, head e2e (#32), làm tròn lên. MEI_AP = 0,005; MEI_vt = 0,006; MEI_t = MEI_s = 0,005.

**H1 — head × sàn.** Cặp: A1 − A0, A8 − A0, A2 − A0, A2 − A8. Chỉ số: AP_vt, AP_t, AP_s, AP_m, AP. Bootstrap theo cụm cảnh, B = 10.000, cho mỗi head.
- **H1a:** Δ(AP_vt) > 0 ở cả hai head cho A1, A8, A2 so với A0.
- **H1b** (dự báo có hướng, kiểm hai phía): Δ_nms(AP_vt) − Δ_e2e(AP_vt) ≥ 0. "Có tương tác" chỉ khi, với ≥ 2/3 arm có sàn, hiệu này cùng dấu ở 3/3 seed **và** |trung bình| ≥ MEI_vt.
- **H1c:** Δ(AP_s) ≤ 0 cho các arm có sàn so với A0.

**H2 — số mẫu dương → recall.** Trên val (936 ảnh). Mô hình:

    logit(det_τ) ~ log1p(n_pos) + log2(cạnh ngắn/8) + log2(aspect) + log1p(số GT/ảnh) + 1[hàng xóm < 16 px] + lớp (lớp < 200 GT gộp lại)

  - SE cụm theo ảnh; dữ liệu gộp 12 run, có biến arm.
  - τ chính = 0,25; độ nhạy τ ∈ {0,1; 0,5}.
  - Mô hình chính: head nms với n_pos của nhánh o2m. Phụ: head e2e với nhánh o2o; head nms với n_cand thay n_pos (kiểm nhân quả ngược).

- **H2a:** hệ số của log1p(n_pos) > 0, CI 95% không chứa 0.
- **H2b:** ở GT có cạnh ngắn < 8 px: recall(1) − recall(0) > recall(≥ 2) − recall(1); và ≥ 95% GT < 8 px có n_pos(o2m) ≥ 1 ở cả A1, A8, A2.
- **H2c** (mô tả): hệ số arm (so với A0) giảm ≥ 50% về 0 khi thêm log1p(n_pos).

**H4 (thăm dò):** median |Δθ| theo nhóm cạnh ngắn giảm đơn điệu ở mọi arm (GT đã khớp, aspect ≥ 1,5).

## 4. Run mới — hướng 3 (xác nhận)

- **Arm:** A0, A8, A2, K1, K4 (định nghĩa ở `scripts/c11x/c11x_assign.py`; K_LADDER = 8, 8√2, 16, 16√2, 32, 32√2, 64 px).
- **Seed:** 4, 5, 6. Thứ tự: seed ngoài, arm trong. Tổng 15 run, ghi vào `runs-woX-c11x/`, một đường code (`c11x_train.py`).
- **Cặp xác nhận:** K4 − A2 và A2 − A0. **Cặp phụ:** K1 − A0, K1 − A8, K4 − A0, A8 − A0.
- **Chỉ số:** AP_vt, AP_t, AP_s, AP_m, AP. Head e2e là chính.
- **Thống kê:**
  - bootstrap theo cụm cảnh, B = 10.000, Δ = trung bình theo seed;
  - CI gộp = Δ ± 1,96·√(se_cảnh² + se_seed²), với se_cảnh = (hi − lo)/3,92 từ CI percentile và se_seed = sd(Δ theo seed)/√3;
  - luôn báo kèm khoảng t theo seed (2 bậc tự do) và min–max theo seed;
  - không hiệu chỉnh nhiều phép so cho cặp phụ; cặp phụ chỉ mô tả.
- **H3a:** Δ(AP_vt, A2 − A0) > 0, CI gộp không chứa 0.
- **H3b:** Δ(AP_vt, K4 − A2) ≥ −MEI_vt **và** Δ(AP_s, K4 − A2) > 0 với CI gộp không chứa 0.
- **H3c:** Δ(AP_vt, K1 − A8) ≥ −MEI_vt.
- **Gọi là "cải thiện"** chỉ khi CI gộp không chứa 0 **và** |Δ| ≥ MEI của chỉ số đó.

## 5. Cổng go cho hướng 3

Chỉ train 15 run khi **H2a qua** ở mô hình chính (τ = 0,25). Ghi kết quả này vào ô `GO_H2` của notebook train trước khi chạy.
- Nếu H2a trượt: không train hướng 3; chuyển sang hướng 5.
- Nếu bảng recall theo n_pos cho điểm bão hoà k* ∉ {1, 4}: được thêm **một** arm K<k*> bằng phụ lục có ngày, trước khi train. Không bỏ K1 hay K4.

## 6. Kiểm tái lập R0 (trước 15 run)

Train A2 seed 1 bằng `c11x_train.py`, so với `c11_A2_s1` cũ.
- **Khớp** nếu |Δ mAP50-95 val ở epoch 24| ≤ 0,003 và |Δ AP test e2e| ≤ 0,002.
- **Không khớp:** vẫn chạy hướng 3 (cùng một đường code), nhưng không gộp run mới với run cũ trong bất kỳ bảng nào, và báo độ lệch.

## 7. Quy tắc dừng và báo cáo

- Run bị Ultralytics đổi batch (`batch_changed`) thì loại khỏi so sánh và báo.
- Run lỗi thì chạy lại cùng seed; không thay seed.
- Báo cáo **mọi** giả thuyết ở §3–§4, kể cả kết quả âm.
- Số trong bài sinh từ file CSV/JSON mà notebook ghi ra; không gõ tay.

## Phụ lục

_(chưa có)_
