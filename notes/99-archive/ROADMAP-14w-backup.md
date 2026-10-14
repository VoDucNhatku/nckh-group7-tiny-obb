# ROADMAP: kế hoạch 14 tuần (12/10/2026 → 17/01/2027)

Nguồn kế hoạch: proposal §9–§11 (`notes/02-proposal/t07-c3-proposal-v2-EN.md`) và Bảng 5 trong bản nộp trường. M1–M4 là bốn thành viên. Nhóm tự phân công rồi điền tên vào bảng dưới.

Cách dùng:
- tick `[x]` khi xong, trong cùng PR với kết quả;
- mỗi giai đoạn tương ứng một **Milestone** trên GitHub; mỗi mục lớn là một **Issue**.

| Vai | Thành viên |
|---|---|
| M1 | _(điền)_ |
| M2 | _(điền)_ |
| M3 | _(điền)_ |
| M4 | _(điền)_ |

---

## Việc cần chốt ngay (trước tuần 1)

- [ ] Chốt **một** tên đề tài. Bản md ghi "Lose Their *Positives*", bản PDF nộp trường ghi "Lose Their *Training Signal*".
- [ ] Phân công M1–M4. Điền vào bảng trên và vào ô Team của proposal md.
- [ ] Mỗi thành viên có tài khoản Kaggle đã xác minh số điện thoại (cần để dùng GPU).

## Giai đoạn 1 · Tuần 1 (12/10 – 18/10) · Dữ liệu và code nền: M1, M2

- [ ] Đăng ký xView. Dựng lại ảnh AI-TOD-R theo script chính thức (`labels.zip` + ảnh xView).
- [ ] Pin một fork Ultralytics (8.4.174 hoặc commit đã ghi lại). Mọi nhánh thí nghiệm là tham số tường minh.
- [ ] Unit test cho 4 quy tắc ứng viên (TAL, STAL-8, STAL-16, OA-STAL v2), tức các thuộc tính P1–P5 trong §7.
- **Cổng:** có đủ dữ liệu và test pass. Nếu sau 2 tuần vẫn không có xView thì dùng DOTA-v2.0, thu hẹp phạm vi claim và ghi lại.

## Giai đoạn 2 · Tuần 2 (19/10 – 25/10) · Pilot và go/no-go: M2, M3

- [ ] Chạy pilot trên Kaggle (P100, 2×T4) và đo số ảnh/giây thực tế.
- [ ] Viết converter dự đoán sang AITODReval (maxDets 1500).
- [ ] Tái lập RetinaNet-O của MMRotate, khớp Bảng II của AI-TOD-R trong khoảng ±1,0 AP.
- **Cổng go/no-go (§9).** Nếu tốc độ đo được cho thấy cần hơn 10 tuần quota cho kế hoạch lõi thì cắt theo thứ tự:
  1. RQ4 chỉ chạy A2/A4;
  2. bỏ A5;
  3. bỏ A6/A7.

  Ghi lại quyết định cắt.

## Giai đoạn 3 · Tuần 3 (26/10 – 01/11) · RQ2 offline và pre-registration: M1, M4

- [ ] Thống kê từ nhãn: số ứng viên theo bin kích thước × tỉ lệ cạnh × mật độ, đối chiếu với Proposition 1.
- [ ] Viết `experiments/preregistration.md`, **có ngày**, trước mọi lần train RQ3. Dấu của dự đoán H3 được chốt tại đây.

## Giai đoạn 4 · Tuần 4–6 (02/11 – 22/11) · RQ1 benchmark: M2, M3

- [ ] YOLO11s / YOLO26n / YOLO26s-OBB, 2 recipe, 3 seed.
- [ ] Bảng benchmark theo bin kích thước và theo lớp, chấm bằng AITODReval.

## Giai đoạn 5 · Tuần 6–9 (16/11 – 13/12) · RQ3 ablation: cả nhóm

- [ ] Các nhánh A0–A7 × 3 seed, kèm chẩn đoán online (số mẫu dương mỗi GT, xung đột).
- [ ] So sánh chính **A4 với A2**, khoảng tin cậy bootstrap ghép cặp. Kết quả âm tính cũng báo cáo.

## Giai đoạn 6 · Tuần 10–11 (14/12 – 27/12) · RQ4 dataset thứ hai: M3, M4

- [ ] SODA-A (cần kiểm quyền truy cập), dự phòng DOTA-v2.0 train → val.
- [ ] Báo cáo tỉ lệ GT chịu tác động ở kích thước đầu vào thực tế.

## Giai đoạn 7 · Tuần 12 (28/12 – 03/01) · Phân tích: M1, M4

- [ ] Nối chẩn đoán RQ2 với độ chính xác RQ3. Phân tích lỗi theo lớp và cấu hình xếp cạnh nhau.
- [ ] Vẽ hình cho bài.

## Giai đoạn 8 · Tuần 13 (04/01 – 10/01) · Quét lại tài liệu và viết: cả nhóm

- [ ] Quét lại độ mới. Đọc toàn văn MFN-Net, ARA và JEIT (hiện mới đọc abstract hoặc chưa đọc được).
- [ ] Bản thảo trong `paper/`.

## Giai đoạn 9 · Tuần 14 (11/01 – 17/01) · Review và phát hành: cả nhóm

- [ ] Review nội bộ với mentor.
- [ ] Phát hành code, config và file dự đoán. Báo cáo cuối.

---

## Tồn đọng không chặn tiến độ

- [ ] Vòng tự phản biện đầy đủ cho proposal v2. Hiện mới có §15, tự trả lời 11 phản biện.
- [ ] SLR #7 **tạm dừng**: còn 28 bài main chưa có full text và chưa có file synthesis. Mở lại nếu cần cho phần Related Work ở giai đoạn 8.
