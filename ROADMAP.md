# ROADMAP: kế hoạch 4 tuần (11/10/2026 → 08/11/2026)

> **Thay cho kế hoạch 14 tuần cũ** (12/10/2026 → 17/01/2027, lưu ở [ROADMAP-14w-backup.md](ROADMAP-14w-backup.md)).
> Cập nhật 2026-10-13 theo quyết định của nhóm trưởng: **cả đề tài gói trong 4 tuần**.
> Căn cứ: phản biện [notes/t07-critique-q2-2026-10-11.md](notes/t07-critique-q2-2026-10-11.md) §4 (ngân sách), §6 (kế hoạch, cổng, danh sách cắt).

## Đọc trước khi làm

- **Mức kỳ vọng không đổi: T1 → hội nghị Scopus (ICORE C–B) hoặc Q4, có điều kiện.** Phản biện kết luận **Q2 không bảo vệ được trong 4 tuần**: chưa có ứng viên T2 nào đứng vững, và đường găng *dữ liệu → bằng chứng → cài đặt* dài hơn 4 tuần. Hướng Q2 (C-7′, đổi đầu/biểu diễn góc) chỉ **thu bằng chứng** trong 4 tuần; mở hay đóng ở Cổng 4. Xem `notes/claims-ledger.md` (C-10, C-12).
- **GPU không phải nút thắt** (lõi cần khoảng 55–106 GPU-giờ, cung khoảng 250 nếu đủ 4 tài khoản Kaggle — [ước lượng]). **Nút thắt là dữ liệu và bộ chấm điểm.** Mọi việc chỉ cần nhãn phải làm ngay, song song với việc chờ xView.
- Tuần thực tế: T1 = 12–18/10 · T2 = 19–25/10 · T3 = 26/10–01/11 · T4 = 02–08/11.
- Milestone G0–G9 trên GitHub vẫn theo kế hoạch 14 tuần cũ. Các **Cổng 0–5** dưới đây là mốc mới; nhóm cần sửa lại milestone/due date trên GitHub.

## Quyết định nhóm phải chốt trước khi commit preregistration (hạn 21/10)

- [ ] **So sánh chính.** Phản biện đề xuất đổi từ "A4 so với A2" (Hệ quả 2 của proposal dự báo hiệu ứng chỉ bậc hai) sang **giai thừa ngưỡng/độ phủ A0/A1/A2/A8**. Trong đó A8 là sàn phủ tối thiểu: cạnh ngắn < 11,3 px thì nâng thành 11,3 px = √2·8, vì hộp có cạnh ngắn ≥ √2·s luôn chứa ít nhất một điểm neo. A4 so với A2 lùi thành phép thử phụ. Nếu nhóm đồng ý: ghi dòng **C-11** vào ledger (văn bản soạn sẵn ở phản biện §8.2) và sửa proposal §7.4, §8.2, §8.5, §13.
- [ ] Chốt **một** tên đề tài (#1): "Lose Their *Positives*" (md) hay "Lose Their *Training Signal*" (PDF nộp trường).
- [ ] Phân vai (#2). Bảng dưới là đề xuất.

| Vai | Phụ trách | Thành viên |
|---|---|---|
| M-Data | xView, dựng ảnh AI-TOD-R, dataset trên Kaggle, tách val theo cảnh | _(điền)_ |
| M-Code | pin fork Ultralytics, hàm `surrogate` + A8, unit test, converter, kiểm thử oracle cho AITODReval | _(điền)_ |
| M-Run | 4 tài khoản Kaggle, pilot, xếp lịch run, ghép cặp cùng GPU, log | _(điền)_ |
| M-Analysis | RQ2 offline, preregistration, đọc prior art, bootstrap, viết bài | _(điền)_ |

## Cổng go/no-go

| Cổng | Ngày | Điều kiện "go" | Nếu trượt |
|---|---|---|---|
| **0** | **13/10 (T3)** | Mở `labels.zip`: (a) có nhãn test không; (b) đếm ảnh/instance theo split; (c) tỉ lệ bin kích thước, tỉ lệ cạnh, số GT < 2 px, số GT/ảnh lớn nhất; (d) tên file có mã hóa cảnh nguồn không | (a) trượt → bỏ neo Bảng II và RetinaNet-O, chấm trên test tự cắt, claim chỉ nội bộ. (d) trượt → bootstrap cụm theo hash/lân cận |
| **1** | **18/10 (CN)** | Ảnh AI-TOD-R dựng đủ, có trên Kaggle cho ≥ 2 tài khoản | xView chưa duyệt đến 16/10 → chạy giao thức rút gọn **AI-TOD-R-woX** (chỉ ảnh không thuộc xView), khai báo trước, không so với Bảng II. Đến 18/10 không có ảnh nào → thu hẹp còn RQ2 offline + luật phủ + tập con DOTA-v2, mức workshop/Q4 |
| **2** | **21/10 (T4)** | (a) Pilot đo được ảnh/giây trên P100 và T4; (b) kiểm thử oracle: đưa GT qua converter + AITODReval cho AP ≈ 100; (c) converter vòng tròn đạt IoU = 1; (d) `experiments/preregistration.md` **commit có ngày** | (b)/(c) trượt → dừng mọi so sánh, sửa evaluator trước. Tốc độ < 15 ảnh/giây → giữ 3 seed, bỏ seed 4–5 và nhánh thăm dò model s |
| **3** | **25/10 (CN)** | (a) RetinaNet-O trong 7,3 ± 1,0 AP; (b) dataset thứ hai (ưu tiên SODA-A) đã tải và kiểm trùng ảnh với AI-TOD-R; (c) đợt 1 xong ≥ 80% | (a) trượt → chỉ claim so sánh nội bộ. (b) trượt → bài một dataset, bỏ RQ4. (c) trượt → A1 còn 1 seed |
| **4** | **01/11 (CN)** | (a) Đủ seed cho so sánh chính; (b) sai số góc theo kích thước trên run A2 (median \|Δθ\| theo cạnh dài) | (b) không có điểm gãy theo kích thước → **đóng C-7′**, ghi ledger. Có điểm gãy → mở C-7′ **sau 08/11** (hướng T2, sớm nhất nộp quý I/2027) |
| **5** | **08/11 (CN)** | Bản nháp 6 trang (khuôn IEEE) + gói tái lập (commit fork, config, seed, file dự đoán, script sinh bảng từ `metrics.json`) + cập nhật ledger | Thiếu kết quả → nộp bản RQ2 + luật phủ cho hội nghị hạn tháng 1/2027, bổ sung số trong tháng 11–12 |

---

## Tuần 1 · 12/10 – 18/10 · Dữ liệu, nhãn, code nền

- [ ] **Đăng ký xView ngay** (#4). Song song: tải gói `AI-TOD_wo_xview` và `labels.zip`.
- [ ] Xác minh 4 tài khoản Kaggle đã xác thực số điện thoại (#3).
- [ ] **Cổng 0 (13/10):** mở `labels.zip`, chạy thống kê nhãn (bin, tỉ lệ cạnh, GT < 2 px, số GT/ảnh lớn nhất, có nhãn test không).
- [ ] **RQ2 offline ngay**, vì chỉ cần nhãn (#10): số ứng viên theo quy tắc A0/A1/A2/A4/A8, tỉ lệ GT không có ứng viên, cấu hình hàng xóm (cạnh nhau / nối đuôi), đối chiếu Proposition 1.
- [ ] Pin fork Ultralytics 8.4.174 (#5). Viết hàm `surrogate` có thêm A8. Unit test P1–P5 + test "luật phủ" (#6).
- [ ] Converter dự đoán → AITODReval (#8). **`max_det` ≥ 12.000**, vì AITODReval giới hạn 1.500 phát hiện **mỗi (ảnh, lớp)** × 8 lớp, còn `max_det` của Ultralytics tính cho cả ảnh.
- [ ] Đọc toàn văn các bài gần nhất (#16): MCSA (*Sci. Rep.* 2025), CDCEDet, MFN-Net, ARA, JEIT. Cập nhật Bảng 1 định vị.
- [ ] Sửa câu chữ `Group7.pdf` theo #21 (nếu còn phải nộp lại).
- **Cổng 1 (18/10):** có ảnh trên Kaggle.

## Tuần 2 · 19/10 – 25/10 · Pilot, preregistration, đợt run 1

- [ ] Pilot P100 / 2×T4, đo ảnh/giây thực tế (#7).
- [ ] **Commit `experiments/preregistration.md` trước 21/10** (#11): so sánh chính, dấu dự báo theo mật độ/cấu hình (lấy từ RQ2 offline), hiệu ứng tối thiểu, code phân tích.
- [ ] **Cổng 2 (21/10):** kiểm thử oracle + converter vòng tròn.
- [ ] Đợt 1: YOLO26n × {A0, A1, A2, A4, A8} × seed 1–3 = **15 run**. 24 epoch, `optimizer` ghi tường minh, `max_det` = 12.000, 1 GPU/run. Mỗi cặp cùng seed chạy cùng tài khoản và cùng loại GPU. Bật log chẩn đoán online (số mẫu dương/GT, xung đột) cho cả hai nhánh o2m/o2o.
- [ ] RetinaNet-O (MMRotate) trên một tài khoản riêng (#9).
- [ ] Tải dataset thứ hai (SODA-A; dự phòng DOTA-v2.0), kiểm trùng nguồn ảnh (#14).
- **Cổng 3 (25/10).**

## Tuần 3 · 26/10 – 01/11 · Đợt run 2 và phân tích

- [ ] Đợt 2: cặp so sánh chính thêm seed 4–5. YOLO11s và YOLO26s mỗi model 1 seed, **gắn nhãn thăm dò** (#12).
- [ ] Dataset 2: 3 quy tắc chính × 3 seed — **chỉ khi** Cổng 3(b) qua.
- [ ] Chấm mọi run bằng AITODReval. Bootstrap **theo cụm cảnh** (không theo ảnh, vì các ô cắt cùng cảnh không độc lập).
- [ ] Hồi quy logistic recall từng GT theo số mẫu dương, theo tầng kích thước/mật độ (H2c, H3) (#15).
- [ ] Đo sai số góc theo kích thước trên run A2 (đầu vào Cổng 4, quyết định C-7′).
- **Cổng 4 (01/11).**

## Tuần 4 · 02/11 – 08/11 · Viết và phát hành

- [ ] Phân tích lỗi theo lớp, mật độ, cấu hình hàng xóm. Vẽ hình (script sinh từ `metrics.json`, không gõ số tay).
- [ ] Bản thảo 6 trang trong `paper/` (#17). Lấy **RQ2 làm trung tâm**; tiêu đề hẹp, nêu rõ "YOLO26n"; không claim "first".
- [ ] Review nội bộ với mentor; phát hành converter, config, seed, file dự đoán (#18).
- [ ] Cập nhật ledger theo kết quả thật (thủ tục REVISION, không sửa thầm).
- **Cổng 5 (08/11).**

---

## Cắt khỏi phạm vi 4 tuần

1. A5, A6, A7 và luật xung đột C-smaller. Thay bằng log xung đột online + hồi quy recall.
2. Recipe R-native 100 epoch; mọi model s/l quá 1 seed. Viết lại H1 thành "chỉ YOLO26n", hoặc bỏ claim "xếp hạng ổn định".
3. YOLOv8, tái lập DCFL, mọi biến thể đầu P2.
4. RQ4 nếu Cổng 3(b) trượt; họ detector thứ hai.
5. Cài đặt C-7′. Trong 4 tuần chỉ đo bằng chứng và viết nháp dẫn xuất.
6. Nộp ACIIDS 2027 (hạn 31/10/2026) — mặc định **không**, trừ khi Cổng 1 qua trước 15/10 và đợt 1 xong trước 26/10.
7. SLR (#20), cập nhật handbook/slide, Modal (chỉ dùng khi tràn quota).

## Thứ tự ưu tiên khi thiếu thời gian

1. **RQ2** — chẩn đoán offline + online (trung tâm của bài).
2. **RQ3a** — ngưỡng/độ phủ A0/A1/A2/A8 (nếu nhóm chốt so sánh chính mới).
3. **RQ3b** — hình dạng: A4 so với A2.
4. **RQ1** tối thiểu — hàng YOLO26n lấy từ A2; hai model s thăm dò; neo RetinaNet-O.
5. **RQ4** — chỉ khi Cổng 3(b) qua.

## Venue ứng viên (đã kiểm trong phản biện §2.2; kiểm lại trước khi nộp)

| Venue | Hạng | Hạn nộp | Ghi chú |
|---|---|---|---|
| IJCNN 2027 | ICORE2026 B | 31/01/2027 | trang chính thức |
| IGARSS 2027 | ICORE2026 C | khoảng 11/01/2027 | **chưa xác minh** trên trang chính thức |
| ACIIDS 2027 | ICORE B, kỷ yếu LNCS/LNAI | 31/10/2026 | rơi giữa kế hoạch, mặc định không nộp |

"Kỷ yếu in trong series LNCS (SJR Q2)" là nhãn của **bộ sách**, không phải mức đóng góp Q2 của bài.

## Tồn đọng không chặn tiến độ

- [ ] Sửa milestone/due date trên GitHub theo Cổng 0–5 (milestone hiện vẫn theo kế hoạch 14 tuần).
- [ ] Proposal §11 và Bảng 5 của `Group7.pdf` vẫn ghi timeline 14 tuần. Ghi chú thay đổi nếu mentor hỏi; không sửa bản đã nộp.
- [ ] Vòng tự phản biện (#19): đã có [notes/t07-critique-q2-2026-10-11.md](notes/t07-critique-q2-2026-10-11.md). Đóng issue sau khi nhóm đọc và chốt so sánh chính.
