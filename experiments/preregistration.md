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

Chỉ train 15 run khi **H2a qua** ở mô hình chính (τ = 0,25). Notebook tự tính bằng `c11x_pergt.h2_gate`, ghi vào `experiments/c11x-h2-gate.json` trên Drive **trước** khi train, và dừng nếu trượt.
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

### A1 · 30/10/2026: cổng H2 theo n_cand, CI gộp dùng t, H1 chỉ mô tả

**Thời điểm.** PR chứa file này chưa merge vào `main` khi nhóm trưởng bắt đầu chạy notebook phân tích (commit `4e7b693` trên nhánh `admin/c11-novelty-plan`, A100, 30/10). Lúc viết phụ lục, notebook đã xong phần 0–2 và đã in điểm test head nms của 3/8 run chưa xem (`c11_A1_s2`, `c11_A1_s3`, `c11_A2_s1`). Chưa có bảng theo GT trên val, cổng H2 hay bootstrap B = 10.000. Cả ba thay đổi dưới đây làm kết luận khó đạt hơn; không thay đổi nào chọn theo các số đã thấy.

**1. Cổng §5 dùng n_cand thay n_pos.**
- Lý do: TAL chọn mẫu dương theo điểm căn chỉnh tính từ chính dự đoán của mô hình, nên GT mà mô hình đã bắt tốt có n_pos cao hơn. Hệ số dương của log1p(n_pos) vì vậy gần như chắc có, kể cả khi không có quan hệ nhân quả, nên không dùng làm cổng được. n_cand chỉ phụ thuộc hình học, vị trí GT so với lưới điểm neo và quy tắc của arm.
- H2a (cổng): mô hình §3 với log1p(n_cand) của nhánh o2m thay cho log1p(n_pos); head nms, τ = 0,25. Qua khi hệ số > 0 và CI 95% không chứa 0.
- Hệ số của log1p(n_pos) vẫn ước lượng và báo, chỉ để mô tả. H2b, H2c giữ nguyên.
- Khi đã cố định kích thước và aspect, n_cand chỉ còn biến thiên theo vị trí trên lưới và theo arm, nên CI có thể rộng. Trượt cổng vì lý do này vẫn tính là trượt.
- Code: `c11x_pergt.h2_gate(count="n_cand")`; file `c11x-h2-gate.json` có khoá `rule = "PREREG-C11X-v1 + A1"`. Notebook train tính lại cổng nếu file thiếu khoá này.

**2. CI gộp §4 dùng t thay z.**
- CI gộp = Δ ± t₀,₉₇₅;ₙ₋₁ · √(se_cảnh² + se_seed²), n = số seed. Với 3 seed, t ≈ 4,30 thay cho 1,96.
- Lý do: se_seed chỉ có 2 bậc tự do, nên z cho khoảng quá hẹp. Lấy bậc tự do của nguồn ít bậc nhất nên khoảng thiên về rộng.
- Áp dụng cho mọi chỗ dùng CI gộp, kể cả H3a, H3b và định nghĩa "cải thiện" ở §4. Code: `c11x_results.combine_scene_seed`.

**3. H1 chỉ mô tả.**
- §3 có khoảng 40 khoảng tin cậy (2 head × 4 cặp × 5 chỉ số), không hiệu chỉnh nhiều phép so. Không gọi một Δ nào của H1 là "có ý nghĩa" chỉ vì CI không chứa 0.
- Tiêu chí "có tương tác" của H1b (cùng dấu ở 3/3 seed và |trung bình| ≥ MEI_vt) giữ nguyên, làm tiêu chí mô tả.

**Hệ quả cho lần chạy đang dở.** Notebook phân tích đang chạy dùng code của `4e7b693` (quy tắc cũ). Hai file `ci_scene_seed.csv` và `c11x-h2-gate.json` của lần chạy đó phải tính lại bằng code có phụ lục này trước khi dùng. Bootstrap và bảng theo GT đã lưu, nên không phải chạy lại phần nặng.

### A2 · 06/11/2026: cổng H2 trượt, hủy K-floor, run xác nhận mới và phân tích theo GT

**Người viết.** Claude Code (Opus 5.5), theo yêu cầu của nhóm trưởng; nhóm duyệt qua PR. **Thời điểm khóa:** commit merge phụ lục này vào `main`, **trước** khi train seed 4–9 và trước mọi phân tích theo GT trên tập test.

**Đích mới của nhóm.** Tạp chí, không phải hội nghị. Phụ lục này không gán band venue (C-19, C-20 giữ nguyên).

**1. Đã xem tới thời điểm này (toàn bộ là thăm dò).**
- Điểm test e2e và nms của cả 12 run seed 1–3; bootstrap B = 10.000 hai head; CI gộp (`experiments/2026-10-30-c11x-analysis/`).
- Bảng theo GT trên val: recall theo số mẫu dương, hệ số arm, sai số góc, dao động theo seed.
- Phân tích chỉ dùng nhãn trên trainval và test (`experiments/2026-11-05-rq2-offline-woX/`); không dùng dự đoán của detector.
- **Trước khi khóa sẽ xem thêm:** số phận GT và recall theo IoU trên **val** của 12 run (`notebooks/C11x_explore_val_colab.ipynb`). Điền kết quả và quyết định vào đây trước khi merge: `[chưa chạy]`.
- **Chưa xem:** mọi kết quả seed 4–9; recall hay số phận theo GT trên tập test của bất kỳ run nào.

**2. Trạng thái §3.** Toàn bộ §3 đã chạy ngày 30–31/10, **trước** khi file này được merge (commit code `e29e3fe`, notebook `f7b30f7`). Vì vậy kết quả §3 báo là **thăm dò**, không gọi là xác nhận hay bán-xác nhận.
Sai lệch so với mô tả ban đầu, đều do lỗi kỹ thuật lúc chạy và ghi trong notebook:
- `predict_and_match` chạy theo nhóm 32 ảnh vì hết bộ nhớ GPU (ô #24);
- sắp lại `evalcache_nms.npz` của 8 run theo thứ tự ảnh của cache e2e, giữ bản gốc `.unsorted.npz` (ô #17); Δ từ cache khớp `eval_*.json` (ô #18).

**3. Cổng H2 và K-floor.** H2a (log1p(n_cand), head nms, τ = 0,25): hệ số −0,333, CI 95% [−0,502; −0,163], `go = false`. Theo §5, **không train K1, K4**, và các giả thuyết H3b, H3c bị hủy. Không mở lại quy tắc K bằng cách đổi cổng.

**4. Run mới.** A0, A8, A2 × seed **4, 5, 6, 7, 8, 9** = 18 run, thay cho §4. Thứ tự: seed ngoài, arm trong. Recipe, dữ liệu woX, chấm `last.pt`, hai head và kiểm R0 (§6) giữ nguyên. Notebook: `notebooks/C11x_train_confirm_colab.ipynb`.
- Lý do chọn 6 seed: với luật CI gộp ở A1, dùng Δ và độ dao động của 12 run thăm dò, A2 − A0 cần khoảng 6 seed; 5 seed cho nửa độ rộng 0,0099 so với Δ = 0,0090 [ước lượng, giả định Δ và độ dao động không đổi]. A8 giữ để kiểm M2.
- A1 không chạy thêm. A4 không chạy.
- **Còn phụ thuộc bước val ở mục 1,** theo tiêu chí ghi trong `scripts/rq2/explore_decision.py`: nếu cả C1 và C2 trượt thì chưa train; nếu C3 trượt thì bỏ A8 và M2, còn 12 run. Sửa mục này theo kết quả trước khi merge; sau khi merge thì không đổi.

**5. Phép chính duy nhất: P1.** Δ(AP_vt, A2 − A0), head e2e, **chỉ seed 4–9**, bootstrap theo cảnh B = 10.000, CI gộp theo A1 (t, 5 bậc tự do).
- **Xác nhận:** CI gộp không chứa 0 **và** Δ ≥ MEI_vt = 0,006.
- **CI loại 0 nhưng dưới MEI:** báo đúng như vậy, không gọi là cải thiện.
- **Không xác nhận:** các trường hợp còn lại; không có nghĩa là hai arm tương đương.
- Không có phép chính nào khác. Không đổi phép chính sau khi thấy kết quả.

**6. Mô tả (không gọi "có ý nghĩa", theo tinh thần A1.3).** A2 − A0, A8 − A0, A2 − A8; AP_vt, AP_t, AP_s, AP_m, AP; hai head. Seed 1–3 chỉ được đặt cạnh để so, không gộp vào phép tính nào của seed 4–9.

**7. Phép thử cơ chế, trên recall theo GT của tập test, chỉ seed 4–9.** Recall: khớp cùng lớp theo thứ tự điểm, IoU xoay ≥ 0,5. Chính: head e2e, score ≥ 0,25. Độ nhạy: e2e score ≥ 0,05; nms score ≥ 0,25. Code: `scripts/rq2/rq2_errors.py`, `scripts/rq2/rq2_did.py`.
- **M1 (từ H1 của bản nháp PR #29).** Trong GT rất nhỏ, hiệu của hiệu Δrecall(A2 − A0) giữa GT có `A0_cand == 0` và GT còn lại. Dự báo: **> 0**.
- **M2 (từ H2 của bản nháp PR #29).** Trong GT rất nhỏ, hiệu của hiệu Δrecall(A2 − A8) giữa GT có ≥ 3 tâm GT khác trong 16 px và GT cô lập. Dự báo: **> 0**. Cơ sở: phân tích nhãn. Lưu ý đã thấy trên val: hệ số arm tổng thể của A8 (0,195) cao hơn A2 (0,167), nên dự báo này có thể trượt.
- **Được ủng hộ** khi đúng dấu **và** CI gộp (scene bootstrap B = 10.000 + seed, theo A1) không chứa 0.
- **M3 (mô tả, không có ngưỡng).** Tỉ lệ số phận của GT theo arm × kích thước × nhóm A0-không-ứng-viên × mật độ, và recall ở IoU 0,1; 0,25; 0,5; 0,75. Dự báo ghi trước:
  - (a) ở GT rất nhỏ chưa được phát hiện dưới A2, "bỏ sót" là nhóm lớn nhất;
  - (b) dưới A2, GT mà A0 không cho ứng viên vẫn có recall thấp hơn các GT rất nhỏ khác;
  - (c) recall(IoU 0,25) − recall(IoU 0,5) ở GT rất nhỏ lớn hơn ở GT tiny.
  - Giới hạn: ở score ≥ 0,25, "bỏ sót" gồm cả hộp đúng chỗ nhưng điểm thấp; đọc kèm kết quả score ≥ 0,05.

**8. Thu hẹp so với bản nháp PR #29.** Bỏ MEI 0,005 AP_vt (không có cách tính đã khai). Bỏ phép H3 trên seed 1–5, vì trộn seed đã xem vào phép xác nhận. Bản nháp giữ làm lịch sử.

**9. Mở rộng cho sau.** Dataset thứ hai (SODA-A nếu tải được) và ảnh xView chỉ chạy sau khi có **phụ lục có ngày** riêng. Không kết quả nào của chúng được dùng để đổi P1, M1, M2.

**10. Báo cáo.** Báo mọi mục ở trên, kể cả kết quả âm (§7). Số trong bài sinh từ file CSV/JSON. Nếu đọc thêm bài trước làm đổi giả thuyết, phải sửa bằng phụ lục có ngày **trước** khi train.
