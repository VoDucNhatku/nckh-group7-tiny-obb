# Decisions and claim cards — T07 fresh research

Ngày 13/10/2026. Nguồn ràng buộc: người dùng yêu cầu nghiên cứu lại từ #7, 4 tuần, Kaggle/60 USD Modal. Không tiếp nối giả định phương pháp của proposal cũ.

## D1 — Giữ câu hỏi trước kiến trúc

Không khóa YOLO26, ViT, FPN, AI-TOD-R hay segmentation như điều kiện bắt buộc. Thứ tự: failure mechanism → prior gần → phép thử bác bỏ → baseline → phần thay đổi tối thiểu → bằng chứng → venue. Lý do: R13 đã dự đoán accuracy gain; F04 đã có selector theo budget và downstream closure; G10 đã có Gaussian head.

## D2 — Ưu tiên H1 để kiểm tra, chưa xác nhận là đóng góp mới

| Candidate | Loại can thiệp theo thiết kế | Claim hiện tại | Điều kiện nâng mục tiêu | Điều kiện hạ/dừng |
|---|---|---|---|---|
| H1 | T1 nếu chỉ tổ hợp policy; T2 chỉ khi có module/cơ chế khác được xác minh | [design] đáng thử trước vì cache inference và predictor nhỏ; chưa có band được bảo vệ | Phân biệt với R13/R14/F04–F06; reliability thêm giá trị ngoài gain-only; bền theo scene/scale shift và đúng budget | Prior đã bao phủ hoặc calibration không thêm giá trị |
| H2 | T1 nếu chỉ chỉnh score; T2 nếu có representation khác và chứng minh cơ chế | [design] dự phòng, không đồng nhất covariance shape với uncertainty | Vượt hiệu chỉnh score đơn giản, GauCho/O2-related controls; calibration được đo đúng | Chỉ tăng AP50 do hậu xử lý hoặc không còn lợi ở AP75 |
| H3 | T1 nếu overlap/merge tweak | [design] dễ đo nhưng novelty hẹp | Chẩn đoán biên crop có ích và giải pháp vượt fixed-overlap/crop-ownership ở compute khớp | Tăng overlap rẻ giải quyết hết |
| H4 | T2 về dạng multi-task module nhưng novelty chưa xác minh | [design] có dữ liệu mask/box song hành; chưa phù hợp triển khai ngay | So cùng supervision/cost, không privileged GT prompts; miền độc lập | Thêm nhãn/teacher giải thích hết gain, hoặc không đủ budget |
| H5 | T1 adapter/training recipe trừ khi có cơ chế mới được xác minh | [design] chỉ transfer checkpoint, không pretrain foundation model | Kiểm tra scale metadata và pretraining leakage; hơn multi-scale augmentation | GSD thiếu, checkpoint không phù hợp, hoặc baseline đơn giản đạt ngang |

**Venue Claim Card chung (C-13):** chưa đủ bằng chứng gán venue band; Q2 chỉ là mục tiêu xét sau các cổng thực nghiệm và novelty. Q1/top conference đòi hỏi mức insight, ý nghĩa và kiểm chứng phù hợp với claim. Các tier trên mô tả kiểu thiết kế, không ánh xạ máy móc sang quartile. Confidence về tính mới/hiệu quả: thấp. Cả 5 candidate chưa được xác nhận runnable end-to-end.

## D3 — Giới hạn phạm vi thực nghiệm

Chỉ một track, một backend ở pilot; không train 50 paper, không song song cả detection và segmentation. Trần 60 USD; giữ 15 USD dự phòng. Quota Kaggle lấy từ tài khoản thật. Không có chi phí Modal nào được phát sinh trong lượt survey.

## Screening và reading amendment

Protocol ban đầu dự tính 3 shard × 12 và ít nhất 3 full-text reads/shard. Các worker bị ngắt do usage limit trước khi hoàn thành. Kết quả thực tế là 50 hồ sơ: 39 A, 10 M (đoạn chọn lọc từ full text), 1 E (publisher excerpts). Không đánh dấu full read cho file chỉ mới tải về.

Corpus cuối tuyển 6 data + 2 baseline detection + 6 frontier/diagnostic + 12 geometry + 14 resolution + 10 representation/segmentation = 50. Các bài generic ViTDet, Deformable DETR, DINO, SAM2, SkySense nhường chỗ cho prior sát hơn về allocation. Số lượng paper là công cụ kiểm soát phạm vi, không phải tiêu chí thành công khoa học.

Các phát hiện sau khi khóa corpus (UGS, oriented calibration, PWOOD) được ghi là watchlist ở REPORT, chưa nhập như các bài đã đọc sâu.

## Việc chưa biết

- H1 có khác biệt khoa học đủ mạnh hay đã bị prior chiếm hoàn toàn.
- Checkpoint nào tái lập thuận lợi trên Kaggle/Modal; không suy từ repo tồn tại.
- Một run mất bao nhiêu giờ và bao nhiêu USD.
- Trường chấp nhận hệ quartile nào; RSL Q2 hiện mới xác minh nhãn publisher CiteScore Best Quartile, chưa đủ bộ year/category.
- Dữ liệu độc lập nào tải được và không trùng nguồn.
- Không có ước lượng xác suất được nhận Q2/Q1.
