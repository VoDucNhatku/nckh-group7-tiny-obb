# #7 — Có thể nâng lên mức mới T2 / T3 không?

> **Đính chính 15/10/2026 — C-19:** [audit mới](t07-q2-audit-2026-10-15/REPORT.md) thay thế cách dùng tier để suy quartile và kết luận phải đổi head. arctan(2δ/L) là cận trên sensitivity với giả định nhiễu vuông góc, chưa là sàn loss hay giới hạn thông tin ảnh. O2-DETR có phụ thuộc kích thước hình học; AQE có quality góc và loss theo aspect ratio. Novelty riêng theo size/calibration chưa được xác lập. Nội dung và mốc thời gian phía dưới là lịch sử, không phải đánh giá venue hiện hành.

> **Cập nhật 2026-10-13 (ledger C-12, REVISION của C-7).** "Gated angle supervision" nếu chỉ đổi trọng số một loss có sẵn thì là **T1** theo rubric, không phải T2 — đây là lỗi áp rubric lúc đề xuất. Hướng T2 thật (C-7′) phải đổi **đầu dự đoán/biểu diễn góc** (đầu góc xuất thêm độ tập trung + cổng đổi cả giám sát lẫn giải mã) và thắng đối chứng "chỉ gate loss". Bằng chứng mới thu hẹp độ mới: TOLF (arXiv 2601.00617), oriented DETR thời gian thực (arXiv 2603.15497). Mở hay đóng C-7′ tại Cổng 4 (01/11/2026); không đạt được trước 08/11/2026. Chi tiết: `notes/t07-critique-q2-2026-10-11.md` §5.2.

> **Cập nhật 2026-10-14 (ledger C-17, REVISION của C-12).** C-7′ được mở rộng thành bài toán *phát hiện vật tí hon có hướng theo mức khả năng xác định*: ba cận [derived] (phủ vị trí √2·s, IoU (w−δ)/(w+δ), góc arctan(2δ/L)); hướng A (C-16) thành chương "giới hạn vị trí". Bằng chứng mới thu hẹp độ mới: Unc-SOD (TIP 2026, chọn mẫu theo bất định cho vật nhỏ trên SODA-A); phân phối góc của O2-DETR không phụ thuộc kích thước (đã kiểm toàn văn). Thêm phép thử chỉ cần nhãn (phân bố góc theo bin kích thước) trước G4, và dùng cặp nhãn AI-TOD-v2 (HBB) / AI-TOD-R (OBB) trên cùng ảnh. Nút thắt Q2: hiện chỉ 1 dataset tiny OBB chắc chắn. Chi tiết: `notes/t07-q2-path-2026-10-14.md`.


- **Ngày:** 2026-10-02 · **Câu hỏi của user:** "t muốn mức mới T2 T3 của #7 thì theo m nghĩ có thể k"
- **Căn cứ:** `notes/t07-proposal.md` (đề xuất T1, claim C-3); `logs/research-log.md` #1–#42 và U-01…U-04 (4 lượt tra mới, mức snippet).
- **Nhắc lại thang mức mới** (rubric research-proposal-integrity §1):
  - **T1** = cải tiến nhỏ (mẹo train, loss, benchmark).
  - **T2** = một module/biểu diễn mới, chính nó là đóng góp, kiến trúc thay đổi thật sự.
  - **T3** = đặt lại bài toán hoặc cách biểu diễn, có nền tảng toán học.

## 1. Trả lời ngắn
- **T2:** **có thể, nhưng khả năng thấp–trung bình** `[suy luận]`, và chỉ theo một hướng cụ thể (hướng B bên dưới).
  Điều kiện: quét độ mới kỹ, ≥ 2–3 dataset, ngân sách vượt $100 (cần academic credits). Nhiều khả năng cần hơn 1 học kỳ.
- **T3:** **không thực tế trong học kỳ này.** Hướng B có "mầm" T3 nếu phần toán đứng vững, nhưng đó là việc cho bài thứ hai hoặc luận văn.

## 2. Ba hướng nâng cấp đã cân nhắc

| Hướng | Ý tưởng | Đã có ai làm? (bằng chứng) | Mức thật sự | Đánh giá |
|---|---|---|---|---|
| **A. Thêm module** | Thêm đầu dò vật thể tí hon (P2), attention, lọc tần số cho YOLO-OBB | **Rất đông:** RS-TOD (đầu dò tí hon + attention, có số trên SODA-A), DyFrDet, SFDNet, FDA-DETR `[log U-04, #10]` | Hình thức là T2, nhưng reviewer sẽ coi là "thêm một module nữa" | **Không khuyên** |
| **B. Biểu diễn góc theo độ phân giải** | Với vật thể ~10 px, góc xoay có thể **không xác định được** do lưới pixel. Thiết kế đầu dự đoán + loss + cách chấm điểm **biết khi nào góc có nghĩa** (theo kích thước và tỉ lệ cạnh) | Một phần đã có: mơ hồ góc ở hộp gần vuông là vấn đề đã biết `[log U-01]`; YOLO26 đã giảm trọng số loss góc theo **tỉ lệ cạnh** `[log #38]`. Phần **theo kích thước pixel** chưa thấy (chỉ 4 lượt tra, mức snippet) `[log U-01…U-03]` | **T2 nếu mới thật**; có mầm T3 nếu chứng minh được giới hạn toán học và đề xuất cách đánh giá mới được cộng đồng chấp nhận | **Hướng duy nhất đáng thử** — rủi ro cao |
| **C. Thiết kế lại khâu gán nhãn** | Gán nhãn xác suất theo trường tiếp nhận Gaussian, có chứng minh đủ mẫu dương (ý ở `t07-proposal.md` §8) | Đông: RFLA, DCFL, STAL, NWD, "Multi-factor sample assignment for oriented tiny" (Sci Rep 2025) `[log #12, #21, #33, U-01]` | Nhiều khả năng vẫn là T1 | Không khuyên làm hướng chính |

## 3. Hướng B — cần chứng minh những gì để thành T2
1. **Giả thuyết `[design]`, chưa kiểm chứng:** với vật thể cạnh L pixel, độ chính xác góc mà ảnh còn "nhìn thấy được" giảm khi L nhỏ.
   Dưới một ngưỡng (phụ thuộc L và tỉ lệ cạnh), nhãn góc chủ yếu là nhiễu, và ép model học góc làm hại cả vị trí.
   - Việc cần làm: **dẫn xuất** quan hệ này (gắn nhãn `[derived]`, có kiểm tra hợp lý) thay vì chỉ nêu giả thuyết.
2. **Module:** đầu dự đoán có "cổng xác định được" — chỉ giám sát góc khi góc có nghĩa.
   Phần chấm điểm đánh giá cũng nhất quán: không phạt góc ở vật thể mà góc không xác định được.
3. **Thực nghiệm:** AI-TOD-R + SODA-A + DOTA-v2 (≥ 3 dataset), cải thiện nhất quán, ablation đầy đủ, nhiều seed.
4. **Phải đọc trước khi tin là mới:**
   - arXiv 2602.13728 (detector query-based cho vật thể tí hon có hướng, 2026)
   - "Multi-factor consideration sample assignment for oriented tiny object detection" (Sci Rep 2025)
   - Fourier Series Coder (arXiv 2604.20281)
   - Phần loss góc của YOLO26 (Eq. 15)
   - Nhãn AI-TOD-R được sinh thô bằng H2RBox-v2 rồi sửa tay `[log #8]` → độ nhiễu nhãn góc theo kích thước là thứ **đo được** trên chính dataset.

## 4. Lộ trình khuyến nghị (bậc thang, không đánh cược ngay)
1. **Học kỳ này: làm bản T1** (`t07-proposal.md`).
   Nhưng mở rộng phần chẩn đoán RQ2 để **đo thêm**: sai số góc của baseline theo kích thước, và phân bố tỉ lệ cạnh theo kích thước.
   Chi phí gần như $0 vì dùng lại các lần train đã có.
2. **Nếu số đo cho thấy góc thật sự vô nghĩa dưới một ngưỡng kích thước rõ ràng** → đó là bằng chứng để mở hướng B (T2).
   Khi đó: quét độ mới đầy đủ, xin Modal academic credits, viết bài thứ hai.
3. **Nếu số đo không cho thấy gì** → dừng ở T1 (Q3/Q4), không tốn thêm tiền.

## 5. Ledger
- C-3 (bản T1) giữ nguyên.
- Thêm **C-7** — ứng viên hướng B, **chưa phải đề xuất**, chưa chấm chính thức. Xem `notes/claims-ledger.md`.
