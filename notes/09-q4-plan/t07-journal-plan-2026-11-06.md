# Kế hoạch bài tạp chí: chẩn đoán có xác nhận

**Ngày:** 06/11/2026 · **Người viết:** Claude Code (Opus 5.5), theo yêu cầu của nhóm trưởng · **Thay cho:** lịch và hướng venue trong [t07-q4-plan-2026-11-05.md](t07-q4-plan-2026-11-05.md).

**Đã đọc lại:** `experiments/preregistration.md` (cả A1), output `notebooks/C11x_analysis_colab.ipynb` commit `f7b30f7`, `experiments/2026-11-05-rq2-offline-woX/`, ledger C-19, C-20.

**Độ sâu đọc nguồn trong phiên này:**
- YOLO26 (arXiv 2606.03748): `đọc method + bảng` phần chính; chưa đọc phụ lục.
- AI-TOD-R (arXiv 2412.11582): `đọc method + bảng` khoảng 60%; §VI-B đến hết chưa đọc nguyên văn.
- DIA-YOLO (IEEE Access 2025, bản local): `đọc method + bảng` phần dữ liệu, cài đặt, kết quả.
- NGLA (Remote Sens. 18(3):396), DALA (CAAI TRIT, DOI 10.1049/cit2.70083): `abstract`.
- MFN-Net, ARA, CDCEDet: chưa đọc toàn văn (paywall hoặc không truy cập được).

**Tính mới: chưa xác lập.** **Venue band: chưa gán** (C-19, C-21).

## 1. Quyết định

Đích là tạp chí. Bài trả lời: sàn ứng viên cứu được gì cho vật xoay rất nhỏ, và vì sao lợi ích vẫn nhỏ.

| Hướng | Quyết định | Lý do |
|---|---|---|
| Chẩn đoán có xác nhận | **Chọn** | Có dữ liệu, chi phí vừa, kết quả âm vẫn báo được |
| Module gán mẫu mới, K-floor | Bỏ | Cổng H2 trượt (A2, mục 3); phần GT còn cứu được rất nhỏ theo proxy |
| Viết từ 12 run thăm dò | Bỏ | C-20 không cho kết luận xác nhận từ các run này |
| Sai số góc (C-7′) | Không theo trong bài này | Sai số không giảm đều theo kích thước trên val (`H4`, thăm dò) |

## 2. Cần train gì

**Làm trước, không train:** `notebooks/C11x_explore_val_colab.ipynb`, phân tích 12 run cũ trên val, khoảng 1–1,5 giờ trên L4 hoặc A100 [ước lượng: dựng dữ liệu 15–20 phút; predict suy từ 337 giây/9.261 ảnh; tính lỗi đo trên dữ liệu giả, chưa đo trên dự đoán thật]. Tiêu chí ghi sẵn ở `scripts/rq2/explore_decision.py`: đạt C1 và C2 thì train; đạt một thì nhóm quyết; không đạt thì chưa train; C3 trượt thì bỏ A8, còn 12 run. Bảng dưới là trường hợp đầy đủ.

| Việc | Có train? | Khối lượng [ước lượng] |
|---|---|---|
| A0, A8, A2 × seed 4–9 | **Có**, 18 run | ~10,1 giờ A100 (0,56 giờ/run) |
| R0: A2 seed 1, kiểm tái lập | **Có**, 1 run | ~0,6 giờ A100 |
| Chấm test hai head | Không train | ~3,5 giờ GPU (337 giây/run/head) |
| Bootstrap B = 10.000 hai head | Không | ~5,3 giờ (suy từ 6.348 giây cho 12 run) |
| Phân tích theo GT | Không | CPU, chưa đo |
| A1, A4, K1, K4, YOLO26s, seed 1–3 | **Không chạy** | — |
| SODA-A, xView | Tùy chọn, cần phụ lục riêng | Chưa đo; phụ thuộc tải được dữ liệu |

Tổng phần bắt buộc: khoảng 19,5 giờ. Tốc độ tiêu CU chưa có nguồn chính thức; nguồn thứ ba ghi 5,4–15 CU/giờ, tức khoảng 105–290 CU. Đọc tốc độ thật trong Colab trước khi chạy.

**Cách chạy:** `notebooks/C11x_train_confirm_colab.ipynb`, A100, Run all. Bị ngắt thì Run all lại.

## 3. Việc còn lại, theo thứ tự

1. **Nhóm trưởng:** hỏi trường tính hạng theo SJR hay JCR, mentor có cần nộp gì vào 08/11 không; tra quartile trên trang SCImago. Push nhánh, chạy notebook phân tích val, rồi quyết định có train không và điền kết quả vào phụ lục A2.
2. **Người có quyền thư viện:** lấy toàn văn MFN-Net, ARA, CDCEDet; đọc NGLA, DALA và §VI-D của AI-TOD-R. Nếu đổi giả thuyết thì sửa bằng phụ lục có ngày **trước** khi train.
3. **Nhóm:** duyệt và merge nhánh này vào `main` để khóa preregistration. Đổi `BRANCH = "main"` trong `build_confirm_notebook.py` rồi sinh lại notebook.
4. **Nhóm:** đẩy `scripts/c11/` từ Drive lên GitHub qua PR riêng.
5. **Người chạy:** Run all notebook. Copy `c11x-confirm-results/` (CSV, JSON, không copy trọng số) về `experiments/` qua PR.
6. **Viết bài:** điền phần `[TODO]` trong `paper/main.tex` từ file kết quả.
7. **Mở rộng nếu đủ sức:** xin SODA-A và xView; viết phụ lục trước khi chạy.
8. **Chọn tạp chí:** đọc phạm vi nhận bài và phí đăng trên trang chính thức, chuyển sang mẫu của tạp chí, rà tài liệu tham khảo, nộp.

## 4. Tạp chí để xem (chưa xác nhận)

Số lấy từ nguồn thứ cấp ngày 05/11/2026; SCImago chặn truy cập tự động, nên phải tra lại trên trang gốc. Phạm vi và phí đăng chưa đọc được.

| Tạp chí | JCR | SJR | Ghi chú |
|---|---|---|---|
| Journal of Applied Remote Sensing (SPIE) | Q3 | chưa rõ | Ưu tiên 1 nếu đúng phạm vi |
| Journal of Electronic Imaging (SPIE) | Q4 | Q3 tới 2023 | Dự phòng |
| Signal, Image and Video Processing (Springer) | Q3 | Q2, không rõ năm | Dự phòng |
| Remote Sensing Letters (Taylor & Francis) | Q3 | Q2 | Đã đăng MFN-Net cùng chủ đề; có thể là dạng bài ngắn |

## 5. Điều kiện để xét band (không phải cam kết)

- **Mức Q4:** P1 có kết quả báo đủ, kể cả âm; có M1–M3; định vị với các bài gần nhất đã đọc toàn văn; công khai code và dự đoán.
- **Mức Q3:** thêm mẫu hình lặp lại trên dataset thứ hai, hoặc lý do thuyết phục nếu không có.

Quartile là thuộc tính của tạp chí, không phải của bài. Band chỉ ghi qua dòng REVISION trong ledger sau khi có kết quả.

**Điều kiện dừng:** nếu P1 không xác nhận và M1–M3 không rõ, bài chỉ còn mức mô tả; khi đó hạ kỳ vọng, không đổi luật.

## 6. Chưa kiểm

- Notebook chưa chạy trên Colab; phần gọi `scripts/c11` trên Drive chưa kiểm được, gồm định dạng thư mục `dota_*`. Notebook dừng nếu không đọc được dự đoán hoặc `scene_key` lệch.
- `paper/main.tex` chưa biên dịch (máy viết không có LaTeX).
- Chưa có phản biện độc lập (AGENTS.md §6.8).
