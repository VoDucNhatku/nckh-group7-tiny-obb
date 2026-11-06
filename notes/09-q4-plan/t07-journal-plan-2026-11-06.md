# Kế hoạch bài tạp chí: chốt ngày 06/11/2026

**Ngày:** 06/11/2026 · **Người viết:** Claude Code (Opus 5.5), theo yêu cầu của nhóm trưởng · **Thay cho:** lịch và hướng venue trong [t07-q4-plan-2026-11-05.md](t07-q4-plan-2026-11-05.md).

**Đã đọc lại:** `ROADMAP.md`, `experiments/preregistration.md` (cả A1), output `notebooks/C11x_analysis_colab.ipynb` commit `f7b30f7`, `experiments/2026-11-05-rq2-offline-woX/`, ledger C-11, C-19, C-20.

**Độ sâu đọc nguồn trong phiên này:**
- YOLO26 (arXiv 2606.03748): `đọc method + bảng` phần chính; chưa đọc phụ lục.
- AI-TOD-R (arXiv 2412.11582): `đọc method + bảng` khoảng 60%; §VI-B đến hết chưa đọc nguyên văn.
- DIA-YOLO (IEEE Access 2025, bản local): `đọc method + bảng` phần dữ liệu, cài đặt, kết quả.
- NGLA (Remote Sens. 18(3):396), DALA (CAAI TRIT, DOI 10.1049/cit2.70083): `abstract`.
- MFN-Net, ARA, CDCEDet: chưa đọc toàn văn (paywall hoặc không truy cập được).

**Tính mới: chưa xác lập.** **Venue band: chưa gán** (C-19, C-21).

## 1. Quyết định

Đích là tạp chí. Bài trả lời: sàn ứng viên cứu được gì cho vật xoay rất nhỏ, và vì sao lợi ích vẫn nhỏ.

| Việc | Quyết định | Lý do |
|---|---|---|
| Thêm A0, A8, A2 × seed 4–5 | **Làm** | ROADMAP (đợt 2) có "cặp so sánh chính thêm seed 4–5" và C-11 có "5 seed cho cặp chính", nhưng cả hai **không nêu cặp nào**; C-11 lấy cả factorial làm phép so chính. Cặp A2 − A0 được chọn sau khi đã xem seed 1–3 (đính chính 06/11, xem preregistration A2 §6) |
| 6 seed hoàn toàn mới (18 run) | Không | Luật do AI đề xuất, không tạp chí nào đã đọc yêu cầu; để dành nếu mentor đòi |
| Module mới, K-floor | Bỏ | Cổng H2 trượt; phần GT còn cứu được rất nhỏ theo proxy |
| Sai số góc (C-7′) | Không theo trong bài này | Sai số không giảm đều theo kích thước trên val |

**Đổi lại:** bài chỉ được viết "lặp lại trên 2 seed mới", không viết "xác nhận độc lập".

## 2. Thời gian và compute unit

Tốc độ CU là số cộng đồng đo, Google không công bố: A100 khoảng 5,4 CU/giờ, L4 khoảng 1,7 CU/giờ ([bảng cập nhật 03/2026](http://mccormickml.com/2024/04/23/colab-gpus-features-and-pricing/)). Bài cũ hơn ghi A100 13–15 CU/giờ, nên có cột trường hợp xấu. **Đọc tốc độ thật trong Colab ở phút đầu.**

| Bước | Runtime | Giờ [ước lượng] | CU thường | CU xấu | Cơ sở |
|---|---|---|---|---|---|
| 1. Notebook val, không train | L4 | 1,5–2 | 3 | 10 | dựng dữ liệu, predict suy từ 337 giây/9.261 ảnh |
| 2. R0 + 6 run | A100 | 3,9 | 21 | 59 | 0,56 giờ/run |
| 3. Chấm 13 lần | A100 | 1,2 | 7 | 18 | 337 giây/lần |
| Dựng dữ liệu 2 phiên A100 | A100 | 0,6 | 3 | 9 | 15–20 phút/phiên |
| 4. Bootstrap | L4 | 4,2 | 7 | 21 | 0,93 giây/vòng với 12 run, nhân 15/12, cộng dựng dữ liệu |
| 5. Phân tích theo GT | L4 | 5–15 | 9–26 | 25–75 | chỉ đo trên dữ liệu giả, sai số lớn |
| **Tổng** | | **khoảng 16–26 giờ máy** | **khoảng 50–70** | **khoảng 140–190** | |

Với 300 CU: đủ, còn dư ít nhất khoảng 110 CU. Dùng phần dư cho chạy lại khi lỗi, rồi mới tới SODA-A. Không dùng để thêm seed sau khi đã thấy kết quả.

## 3. Lịch

| Mốc | Việc | Ai | Thời gian [ước lượng] |
|---|---|---|---|
| A | Hỏi trường SJR hay JCR; hỏi mentor về 08/11 và số seed | Nhóm trưởng | 1–2 ngày |
| B | Chạy notebook val, gửi ô cuối | Nhóm | 1 ngày |
| C | Điền kết quả vào A2; đọc MFN-Net, ARA, CDCEDet, NGLA, DALA; duyệt; merge để khóa | Nhóm + Claude | 2–4 ngày |
| D | Đưa `scripts/c11/` lên GitHub qua PR riêng | Nhóm | Song song |
| E | Đợt 1: train + chấm | Nhóm | 1–2 ngày |
| F | Đợt 2: bootstrap + phân tích theo GT | Nhóm | 1–2 ngày |
| G | Điền kết quả, viết thảo luận và kết luận, biên dịch | Claude + nhóm | 1–2 ngày |
| H | Mentor đọc, sửa | Mentor, nhóm | 1–2 tuần |
| I | Chọn tạp chí, chuyển mẫu, rà tham khảo, nộp | Nhóm + Claude | 2–3 ngày |

**Tổng:** có bản thảo đủ số sau khoảng 1–1,5 tuần; sẵn sàng nộp sau khoảng 2–3 tuần. Thời gian tạp chí phản hồi chưa kiểm, thường tính bằng tháng và không có gì bảo đảm được nhận.

**Mốc 08/11:** nếu mentor cần, nộp bản nháp chỉ có phân tích nhãn và 12 run thăm dò.

## 4. Nhánh quyết định

| Kết quả | Làm gì |
|---|---|
| Val: đạt C1 hoặc C2 | Train (sửa 06/11: bỏ nhánh "nhóm quyết"; C2 không tính `miss`) |
| Val: không đạt cái nào | Chưa train, xem lại hướng |
| Val: C3 trượt | Bỏ A8, còn 4 run, bỏ M2 |
| R0 không khớp | Không gộp seed; báo riêng từng nhóm; tìm nguyên nhân môi trường |
| P1 không lặp lại | Vẫn báo; bài dựa vào phân tích giai đoạn và số phận GT; hạ kỳ vọng venue |

## 5. Tạp chí để xem (chưa xác nhận)

Số lấy từ nguồn thứ cấp ngày 05/11/2026; SCImago chặn truy cập tự động, nên phải tra lại trên trang gốc. Phạm vi và phí đăng chưa đọc được.

| Tạp chí | JCR | SJR | Ghi chú |
|---|---|---|---|
| Journal of Applied Remote Sensing (SPIE) | Q3 | chưa rõ | Ưu tiên 1 nếu đúng phạm vi |
| Journal of Electronic Imaging (SPIE) | Q4 | Q3 tới 2023 | Dự phòng |
| Signal, Image and Video Processing (Springer) | Q3 | Q2, không rõ năm | Dự phòng |
| Remote Sensing Letters (Taylor & Francis) | Q3 | Q2 | Đã đăng MFN-Net cùng chủ đề; có thể là dạng bài ngắn |

Điều kiện để xét band (không phải cam kết): **Q4:** P1 và M1–M3 báo đủ, kể cả âm; các bài gần nhất đọc toàn văn; công khai code và dự đoán. **Q3:** thêm mẫu hình lặp lại trên dataset thứ hai, hoặc lý do thuyết phục nếu không có. Band chỉ ghi qua dòng REVISION trong ledger sau khi có kết quả.

## 6. Chưa kiểm

- Hai notebook chưa chạy trên Colab; phần gọi `scripts/c11` trên Drive chưa kiểm được, gồm `train_arm` và định dạng thư mục `dota_*`. Notebook dừng nếu thiếu tham số, không đọc được dự đoán hoặc `scene_key` lệch.
- `paper/main.tex` chưa biên dịch (máy viết không có LaTeX).
- Chưa có phản biện độc lập (AGENTS.md §6.8).
