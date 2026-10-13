# T07 deep study — phạm vi và điều phối

Ngày: 13/10/2026. Người dùng xác nhận “hardcode” ở đây là **nghiên cứu hardcore, chưa viết code thí nghiệm**. Mọi công việc implementation/training dừng ở mức ý tưởng; các tool chỉ phục vụ đọc, tra cứu, kiểm toán số học và tạo tài liệu nghiên cứu.

Mục tiêu: UAV-view tiny-object detection làm trục; kiểm tra có cần multi-view; đọc sâu các case thay vì chỉ mở thêm câu hỏi; tự phản biện để gom kiến thức nền. Chi phí không dùng làm bộ lọc khoa học. Chưa thay thế proposal nộp trường, không push, không chạy GPU.

| Worker đã có | Model/effort giữ nguyên | Phạm vi riêng | Output |
|---|---|---|---|
| evidence_sol | gpt-6.1-sol/high | QueryDet, SuperYOLO, UGS, GauCho; đọc method/experiments/ablation | CASEBOOK-STATIC.md; static-claims.json |
| questions_sol | gpt-6.1-sol/high | DynUAV, HARD, DroneEyes, SOPSeg; protocol/ablation/limits | CASEBOOK-TEMPORAL-MASKS.md; temporal-claims.json |
| critic_astra | gpt-6-astra/high | Multi-view primary sources và phản biện toán/logic; final review | MULTIVIEW-AND-CRITIQUE.md; multiview-sources.json; REVIEW.md |

Chat chính giữ scope, dùng nguồn official dataset/camera-model để giải thích nền, tạo RESEARCH-PROMPT.md và DEEP-REPORT.md; không đọc raw PDF hàng loạt. Giữ manifest bounded; ước lượng điều phối ba worker: input chọn lọc 15–30k tokens, output 15–25k + khoảng 20% hợp nhất/kiểm tra; không phải usage đã đo hoặc quota do người dùng đặt.

Không tuyên bố đọc sâu mọi trục trong bản đồ 13 mục tiêu: lượt này chọn các cơ chế nền về thông tin, localization, temporal/streaming, segmentation và multi-view. Domain/open-vocabulary/weak-label methods vẫn cần lượt method audit riêng nếu được chọn làm đóng góp chính.

Trạng thái bàn giao: DEEP-REPORT, hai casebooks, multi-view critique, reusable prompt và ba JSON ledgers đã lưu. Astra final review hai P2 đã sửa và re-review; không còn finding mở trong phạm vi đó. Structural verification 10/10, không scientific validation. Temporal sidecar do root chuyển từ casebook Sol đã hoàn tất, provenance ghi rõ trong JSON/AUDIT. Không có detector runs hoặc git push.
