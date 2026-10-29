# Kế hoạch C11x: các hướng tính mới sau 12 run thăm dò C11

**Ngày:** 30/10/2026 · **Người viết:** Claude Code (Opus 5.5), theo yêu cầu của nhóm trưởng · **Trạng thái:** đề xuất, đi kèm `experiments/preregistration.md` (PREREG-C11X-v1).

**Đã đọc lại:**
- toàn bộ 35 ô của `C11_colab.ipynb` cùng output (commit `58e2805`); tôi tự đọc và đối chiếu số, không dựa vào note giải thích;
- `notes/08-c11-execution/t07-c11-notebook-explained-2026-10-26.md`;
- proposal v2 §8.5–8.6, §13;
- ledger C-10, C-11, C-16, C-19;
- audit C-19 `REPORT.md` §R2, §5, §6;
- `ROADMAP.md`.

**Mã nguồn đã đọc:** `ultralytics==8.4.174`, các file `utils/tal.py`, `utils/loss.py` (`v8OBBLoss`, `E2ELoss`), `nn/modules/head.py`, `engine/predictor.py`.

**Độ sâu đọc nguồn ngoài**, theo 3 mức của AGENTS.md §6.2:

| Nguồn | Mức | Đã kiểm gì |
|---|---|---|
| OSCAR, Dai et al., arXiv 2212.08472v2 (DOI 10.1109/TGRS.2023.3243062) | đọc method + bảng | Eq. 2 (pseudo-box p×p), mục Ablation B.1, Table II |
| DIA-YOLO, Kim & Park, IEEE Access 13 (2025), DOI 10.1109/access.2025.3603214 | metadata (OpenAlex) | tên, tác giả, tập, trang đầu 150570. Con số 18.730 ảnh lấy từ hồ sơ của nhóm (`t07-c3-evidence-dossier.md:381`); **chưa xác minh lại** ở bản gốc |
| ATSS, Zhang et al., CVPR 2020, arXiv 1912.02424 | đọc method | §4.1, Algorithm 1, k = 9 |
| YOLOv10, Wang et al., NeurIPS 2024, arXiv 2405.14458v2 | đọc method + bảng | §3.1, Table 1, Table 3 |
| DeFCN (CVPR 2021, arXiv 2012.03544); One-to-Few (CVPR 2023) | snippet tìm kiếm | **chưa đọc** |

Mọi nhận định về bài trước bên dưới chỉ dùng đúng mức đọc này. "Tìm không thấy" không có nghĩa là "không có".

**Thang AP:** 0–1, như notebook. "1 điểm" = 0,01.

---

## 0. Xuất phát điểm (số từ `C11_colab.ipynb`)

**Đã có:** 12 run YOLO26n-OBB = 4 arm (A0, A1, A8, A2) × seed 1–3, giao thức woX, 24 epoch, A100 (#23).

**Head e2e:**
- AP_vt tăng +0,007 đến +0,009 khi có sàn (#34);
- AP tổng tăng ≤ +0,0035 (#34); sd theo seed của A2 là 0,0047 (#32);
- A1, A8, A2 không phân biệt được với nhau.

**Head nms:** mới chấm 4/12 run. Ở A0, nms cao hơn e2e khoảng 0,006 AP (#32).

**Giới hạn:**
- chưa có preregistration;
- bảng #32 đếm trùng A0_s1;
- CI chỉ phản ánh bất định theo cảnh, chưa gồm bất định theo seed;
- B = 1.000.

**Vì sao cần hướng mới.** Kết quả "sàn ứng viên tăng AP của vật tí hon" gần như đã có trong bài trước:
- **OSCAR** (đã đọc Table II): thay hộp GT tí hon bằng pseudo-box vuông p×p khi h·w < s², trên detector anchor-free một tầng, ảnh hồng ngoại. AP lần lượt 71,9 (không có pseudo-box) / 75,6 (p = s) / 77,6 (p = 1,5s) / 71,2 (p = 2s), tức có điểm tối ưu không đơn điệu.
- **STAL** của YOLO26 đã đặt sàn mặc định.

Phần còn mới chỉ có thể đến từ: (i) **tương tác với head NMS-free**; (ii) **quy luật cơ chế** (GT mất ở bước nào, vì sao các sàn ngang nhau); (iii) một quy tắc gán mẫu khác, có căn cứ từ (ii).

## 1. Thứ tự và cổng

| Bước | Việc | GPU (A100) [ước lượng] | Hạn đề xuất |
|---|---|---|---|
| 0 | Merge PR này: preregistration có ngày trên `main` **trước mọi phép chấm hay run mới** | 0 | 31/10 |
| 1 | Hướng 1: chấm nms cho 8 run; bootstrap B = 10.000 cho hai head | ~4 giờ | 01/11 (Cổng 4) |
| 2 | Hướng 2 (+ hướng 4 đi kèm): gán mẫu tại checkpoint cuối, khớp từng GT trên val | ~1 giờ | 01/11 |
| 3 | Cổng go/no-go cho hướng 3 (preregistration §5) | 0 | 02/11 |
| 4 | Hướng 3: R0 + 15 run + chấm + bootstrap | ~15 giờ | 02–05/11 |
| 5 | Viết (hướng chính, hoặc hướng 5 nếu các hướng trên trượt) | 0 | 06–08/11 (Cổng 5) |

Cách ước lượng: train 0,55–0,57 giờ/run (#23); chấm một head ~337 giây/run (#29); bootstrap 570 giây cho B = 1.000 với 4 cặp, 3 chỉ số (#34), giả định tăng tuyến tính theo B. Bootstrap mới có 5 chỉ số nên có thể lâu hơn.

---

## 2. Hướng 1 — sàn ứng viên tương tác với head NMS-free

**Câu hỏi.** Sàn ứng viên giúp head nào: e2e (o2o, khớp 1-1, không NMS) hay nms (o2m + NMS)? Theo từng nhóm kích thước?

**Cơ chế** (đọc mã 8.4.174, `utils/loss.py`):
- `E2ELoss` có hai assigner dùng **chung** bước chọn ứng viên: o2m `tal_topk=10`; o2o `tal_topk=7, tal_topk2=1`.
- Trọng số loss o2m giảm tuyến tính từ 0,8 xuống 0,1 qua các epoch.
- Sàn đổi tập ứng viên cho cả hai nhánh. Nhưng o2o chỉ cần **một** mẫu dương, còn o2m hưởng thêm khi có **nhiều** mẫu dương. Vì vậy hai head có thể phản ứng khác nhau với sàn. [suy luận]

**Giả thuyết** (khai trong preregistration §3):
- **H1a:** Δ_sàn(AP_vt) > 0 ở **cả hai** head, với A1, A8, A2 so với A0.
- **H1b:** Δ_sàn(AP_vt) ở head nms ≥ ở head e2e (dự báo có hướng, kiểm hai phía). Lý do: o2m hưởng thêm từ số mẫu dương; o2o chỉ cần có ứng viên.
- **H1c:** Δ_sàn(AP_s) ≤ 0 ở cả hai head, tức đánh đổi mà #32 gợi ý.

**Việc làm:** không train thêm.
1. Chấm head nms cho 8 run còn thiếu, bằng `c11_pipeline.predict_and_eval`.
2. Bảng theo seed cho hai head.
3. Bootstrap theo cụm cảnh, B = 10.000, cho hai head, 4 cặp (A1/A8/A2 − A0, A2 − A8), 5 chỉ số (AP_vt, AP_t, AP_s, AP_m, AP).
4. Gộp bất định theo seed (§7).
5. Với từng seed: hiệu của hiệu Δ_nms − Δ_e2e.

**Metric:** AP_vt, AP_t, AP_s, AP_m, AP; AR1500 làm phụ.

**Ngưỡng:**
- *Thành công H1b:* với ≥ 2/3 arm có sàn, Δ_nms − Δ_e2e của AP_vt cùng dấu ở 3/3 seed, và |trung bình| ≥ MEI_vt = 0,006.
- *Thất bại:* ngược lại. Khi đó ghi "không thấy tương tác head × sàn ở 3 seed"; kết quả này vẫn đưa vào hướng 5.

**Chi phí:** khoảng 50 phút chấm + 2 × ~95 phút bootstrap [ước lượng].

**Rủi ro:**
- Dữ liệu e2e đã bị xem. Chỉ điểm nms của 8 run là chưa xem, nên H1 là bán-xác nhận.
- 3 seed cho một hiệu của hiệu là ít.
- Khác biệt có thể đến từ hậu xử lý (NMS IoU 0,7, `max_det`, giới hạn 1.500 mỗi (ảnh, lớp)) chứ không từ gán mẫu: AR1500 của nms thấp hơn e2e khoảng 0,039 ở A0 (#32).

**Bài trước:**
- YOLOv10 (đã đọc §3.1, Table 1, Table 3) đề xuất "consistent dual assignments": train cả o2m lẫn o2o, suy luận bằng o2o. Table 1 báo AP COCO của o2o so với o2m + NMS, ví dụ YOLOv10-N 38,5 so với 39,5. **Không báo AP_S cho head o2m.**
- DeFCN dùng POTO + loss o2m phụ (chưa đọc).
- Một lượt tìm kiếm ngày 30/10 (mức snippet) không thấy bài nào tách riêng ảnh hưởng của khớp 1-1 lên vật nhỏ. **Chưa xác minh** đây là khoảng trống thật.

## 3. Hướng 2 — RQ2 thành quy luật dự đoán được

**Câu hỏi.**
1. Recall của từng GT có dự đoán được từ số mẫu dương và kích thước/stride P3 không?
2. Quy luật đó có giải thích vì sao A1, A8, A2 cho AP ngang nhau không?

**Thiết kế.**
- Với mỗi run, đưa 936 ảnh **val** qua loss của checkpoint cuối, với đúng quy tắc của arm (`c11x_pergt.record_assignment`). Ghi cho mỗi GT và mỗi nhánh o2m/o2o: số ứng viên, mẫu dương trước xung đột, mẫu dương cuối.
- Predict val cho hai head, khớp tham lam theo lớp ở IoU đa giác ≥ 0,5. "Được phát hiện ở τ" nghĩa là dự đoán khớp có điểm ≥ τ. τ chính = 0,25; độ nhạy τ ∈ {0,1; 0,5}.
- Đọc thêm log `c11_assign_diag.jsonl` lúc train (cấu trúc chưa biết vì mã ghi nằm trên Drive; notebook in ra trước).

**Giả thuyết:**
- **H2a:** trong logit(det_τ) ~ log1p(n_pos) + log2(cạnh ngắn/8) + log2(aspect) + log1p(số GT/ảnh) + có-hàng-xóm-trong-16px + lớp, hệ số của log1p(n_pos) > 0, với CI 95% (sai số chuẩn cụm theo ảnh) không chứa 0. Áp dụng cho head nms/nhánh o2m.
- **H2b (bão hoà):** trong nhóm cạnh ngắn < 8 px, recall(n_pos = 1) − recall(n_pos = 0) > recall(n_pos ≥ 2) − recall(n_pos = 1). Đồng thời ≥ 95% GT < 8 px có n_pos ≥ 1 ở cả A1, A8, A2. Nếu đúng, ba sàn ngang nhau vì đều đưa GT tí hon qua điểm bão hoà.
- **H2c:** hệ số của arm (so với A0) giảm ≥ 50% về 0 khi thêm log1p(n_pos) vào mô hình. Đây là mô tả, không phải phép thử nhân quả.

**Phép bác:**
- Nếu A2 cho nhiều mẫu dương hơn A8 rõ rệt ở GT < 8 px, mà recall vẫn tăng theo n_pos sau mức 2, thì H2b sai và sự ngang nhau phải do yếu tố khác. Ứng viên là chia sẻ ứng viên: `shared_frac` ở #16 của A8 thấp hơn A2.
- Nếu H2a chỉ đúng với n_pos nhưng không đúng với n_cand, nghi nhân quả ngược (xem rủi ro).

**Ngưỡng thành công:** H2a qua, **và** có một điểm bão hoà k* ∈ {1, …, 4} đọc được từ bảng recall theo n_pos. Đây cũng là cổng "go" cho hướng 3 (preregistration §5).

**Chi phí:** khoảng 3–5 phút/run × 12 run ≈ 1 giờ [ước lượng; chưa đo].

**Rủi ro:**
- **Nhân quả ngược.** TAL chọn top-k theo điểm căn chỉnh tính từ chính dự đoán của mô hình, nên GT mà mô hình đã làm tốt có thể nhận nhiều mẫu dương hơn. Giảm thiểu:
  - với GT nhỏ, n_cand ≤ 10 nên o2m chọn hết ứng viên, và số mẫu dương chủ yếu do hình học quyết định;
  - chạy thêm biến thể dùng **n_cand** (chỉ phụ thuộc hình học và quy tắc) làm phép kiểm độ vững.
- **Gán mẫu tại checkpoint cuối khác gán mẫu trong lúc train.** Log jsonl lúc train chỉ là số gộp.
- **Val nhỏ** (12.003 GT, #19); các lớp hiếm được gộp (`cls_g`).

**Bài trước:** ATSS (đã đọc §4.1) ghi nhận mỗi vật có khoảng 0,2·k·L mẫu dương, bất biến theo kích thước. Ý "số mẫu dương mỗi vật quan trọng" đã có từ đó. Phần mới, nếu có, là đo trên vật xoay tí hon với hai nhánh của YOLO26.

## 4. Hướng 3 — sàn theo số ứng viên (K-floor)

**Câu hỏi.** Thay sàn kích thước cố định (đổi vùng ứng viên của 96,8% GT ở A2, #12) bằng sàn thích nghi chỉ nới **những GT thiếu ứng viên**. Cách này có giữ được lợi ích AP_vt mà giảm đánh đổi ở AP_s không?

**Quy tắc** (`c11x_assign.py`, quy tắc `K<k>`): mỗi GT bắt đầu với hộp gốc. Nếu số điểm neo (cả 3 tầng) nằm trong hộp < k, thì thử lần lượt các sàn kiểu STAL 8, 8√2, 16, 16√2, 32, 32√2, 64 px (cạnh < f thì thay bằng f, giữ góc và tâm), dừng ở mức đầu tiên đủ k.
- Quy tắc chỉ bảo đảm ≥ k **ứng viên**. Mẫu dương còn qua top-k và xử lý xung đột, nên được đo riêng.
- Đã test: mọi GT hợp lệ có ≥ k ứng viên; GT đã đủ thì giữ nguyên; các mức k lồng nhau; A2 trùng đúng mã gốc 8.4.174.

**Chọn k = 1 và k = 4** (chốt ngay trong preregistration, không chờ kết quả). Căn cứ là Mệnh đề 1 của proposal [cited; derived trong proposal]: E[N] ≈ 0,0205 · diện tích hộp.
- Sàn 8×8 cho E[N] ≈ 1,3; sàn 11,3² ≈ 2,6; sàn 16² ≈ 5,2 [tính lại].
- **K1** là can thiệp nhỏ nhất để không GT nào thiếu ứng viên; so với A8 (sàn cố định đủ cho ≥ 1 ứng viên ở stride 8).
- **K4** cho GT tí hon số ứng viên gần mức A2, nhưng không nới GT 8–16 px đã có ≥ 4 ứng viên; so với A2.
- Nếu hướng 2 cho điểm bão hoà k* ∉ {1, 4}, thêm arm K<k*> bằng một **phụ lục có ngày** của preregistration, trước khi train.

**Run:**
- A0, A8, A2, K1, K4 × seed **4, 5, 6** = 15 run. Mọi arm train bằng cùng `c11x_train.py`, cùng recipe C11.
- Seed mới, nên đây là phần **xác nhận** thật. Không trộn với 12 run thăm dò.
- Trước đó chạy **R0**: A2 seed 1 bằng code mới, so với `c11_A2_s1` cũ để kiểm tái lập. Ngưỡng ở preregistration §6.

**Giả thuyết** (head e2e là chính, nms báo song song):
- **H3a (tái lập):** ΔAP_vt(A2 − A0) > 0 với CI gộp cảnh + seed không chứa 0.
- **H3b:** ΔAP_vt(K4 − A2) ≥ −MEI_vt (−0,006), **và** ΔAP_s(K4 − A2) > 0 với CI gộp không chứa 0.
- **H3c:** ΔAP_vt(K1 − A8) ≥ −MEI_vt.

**Ngưỡng:**
- *Thành công (có đóng góp):* H3a và H3b đều qua.
- *Thất bại:* H3b trượt. Khi đó ghi "sàn thích nghi không hơn sàn cố định" và chuyển sang hướng 5. Nếu H3a trượt, kết quả thăm dò không tái lập; ghi đúng như vậy.

**Chi phí:** R0 0,6 giờ + 15 × 0,56 giờ train + 30 lần chấm × ~6 phút + bootstrap 2 head ≈ 15 giờ A100 [ước lượng].

**Rủi ro:**
- Thời gian mỗi epoch có thể tăng: tối đa 7 lần thử điểm-trong-hộp thêm mỗi lần gọi assigner. Bộ nhớ: mặt nạ (batch × số GT × số điểm neo), với tối đa 1.027 GT/ảnh (#21). Assigner có sẵn đường lui từng ảnh khi hết bộ nhớ. Notebook in thời gian; cần so với A2.
- Sàn thích nghi làm hộp gần vuông. Ý tưởng "mỗi GT ít nhất k ứng viên" gần với **ATSS** (k = 9 ứng viên mỗi tầng theo khoảng cách tâm, ngưỡng IoU = mean + std, tâm phải nằm trong GT; §4.1). Phải trích và phân biệt: K-floor giữ phép thử điểm-trong-hộp xoay của TAL và chỉ nới GT thiếu.
- **Chưa quét prior art** cho "số mẫu dương tối thiểu cho TAL/OBB". Phải quét trước khi viết; tính mới ở mức thấp đến vừa [nhận định].

## 5. Hướng 4 — sai số góc theo kích thước, so giữa các arm

**Câu hỏi.** |Δθ| giữa trục cạnh dài của dự đoán và GT thay đổi thế nào theo kích thước? Sàn ứng viên có đổi sai số góc ở cùng nhóm kích thước không? Đây là đầu vào Cổng 4b của ROADMAP và hướng R1/C-7′.

**Việc làm:** dùng chính bảng khớp từng GT của hướng 2 (val, hai head). Lấy median và p90 của |Δθ| (chu kỳ π) theo arm × head × nhóm cạnh ngắn, chỉ với GT đã khớp và aspect ≥ 1,5.

**Giả thuyết** (thăm dò, không dùng làm claim chính):
- **H4a:** median |Δθ| giảm đơn điệu theo nhóm kích thước ở mọi arm.
- **H4b:** ở cùng nhóm kích thước, các arm lệch nhau ≤ 2°.

**Rủi ro:**
- Chỉ đo được trên GT đã được phát hiện, nên có thiên lệch chọn mẫu.
- Nhãn có nhiễu: phép thử vòng tròn chỉ 31,4% GT đạt IoU ≥ 0,999 (#14), nên có một sàn sai số không đo dưới được.
- Góc của vật gần vuông không xác định.

**Chi phí:** đã gồm trong hướng 2.

## 6. Hướng 5 — dự phòng: bài đánh giá chặt chẽ

**Khi nào dùng:** hướng 1–3 không qua ngưỡng.

**Nội dung:**
- dao động theo seed so với hiệu ứng (bảng theo seed, `seeds_needed`);
- CI theo cảnh so với CI gộp seed;
- head e2e so với nms;
- bootstrap B = 10.000.

Dùng lại 12 run thăm dò và 15 run của hướng 3 nếu có.

**Ví dụ sẵn có:** ΔAP(A2 − A0) = 0,0035 (#34), trong khi chênh lệch giữa seed tốt nhất và kém nhất của riêng A2 là 0,0092 (#30).

**Còn thiếu:** bảng các mức tăng **thường được báo cáo** trên AI-TOD(-R). Việc này cần đọc bảng của từng bài; **chưa làm**, không viết từ trí nhớ.

**Rủi ro:** chỉ một detector, một recipe, một dataset. Đóng góp mỏng nếu không mở rộng.

## 7. Sửa các vấn đề của báo cáo nhận xét

| Vấn đề | Cách sửa trong PR này | File |
|---|---|---|
| Train trước preregistration | Khai 12 run là thăm dò; preregistration có mã PREREG-C11X-v1, phải merge trước mọi phép chấm hay run mới; notebook train kiểm có file | `experiments/preregistration.md`, `notebooks/C11x_train_kfloor_colab.ipynb` |
| Ô #32 đếm trùng | `collect_runs` đọc đúng tên file, `assert` không trùng; có test tái hiện lỗi cũ | `scripts/c11x/c11x_results.py`, `tests/test_c11x_results.py` |
| Thiếu bảng theo seed | `per_seed_table`, `paired_seed_deltas` | như trên |
| B = 1.000, CI chỉ theo cảnh | B = 10.000; `combine_scene_seed` gộp se theo cảnh với se theo seed [design]; luôn báo kèm khoảng t theo seed và min–max | như trên |
| CI lệch | `ci_skew`, báo kèm | như trên |
| `scene_key` của phần không-xView chưa kiểm | `scene_key_audit`: ô cắt cùng ảnh gốc có bị tách nhóm không | như trên |
| Thiếu AP theo lớp, AP_s, AP_m trong bootstrap | thêm AP_s, AP_m vào KEYS. AP theo lớp phụ thuộc `predict_and_eval` trên Drive: **chưa làm** | notebook phân tích |
| README / AGENTS / ROADMAP cũ | cập nhật trạng thái 30/10; ghi C-20 vào ledger | các file gốc |
| Code C11 không có trên GitHub | thêm whitelist `scripts/c11/` vào `.gitignore` để nhóm đẩy lên qua PR sau; **chưa đẩy** (code nằm trên Drive) | `.gitignore` |

## 8. Những gì PR này chưa kiểm

- Chưa chạy trên Colab hay A100. Test chạy trên CPU với Ultralytics 8.4.174, torch 2.15 CPU, Python 3.13 — khác torch 2.11 + CUDA của C11.
- Chưa chạy được 55 test của `scripts/c11` vì code đó chỉ có trên Drive. Notebook chạy lại chúng ở đầu.
- Tên khoá và cấu trúc file của `scripts/c11` (`predict_and_eval`, `multi_pair_bootstrap`, `load_cache`, `evalcache_nms.npz`, `results.csv` của run cũ) chỉ suy ra từ cách `C11_colab.ipynb` gọi. Lần chạy đầu trên Colab sẽ lộ chỗ lệch.
- Thời gian và bộ nhớ của quy tắc K trên A100 chưa đo.
