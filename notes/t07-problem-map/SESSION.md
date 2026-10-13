# T07 — Mở rộng bản đồ vấn đề

Ngày: 13/10/2026. Skill: admin → research-admin → paper-synthesize (expand), hallucination-guard.

## Yêu cầu áp dụng

Chỉ dùng #7 — Multi-scale Aerial Object Detection and Segmentation — làm định hướng. Người dùng yêu cầu bỏ lọc theo chi phí, chia mục tiêu cải tiến, mở nhiều góc nhìn và câu hỏi: nghiên cứu hiện tại đã làm gì, còn điểm nào cần kiểm tra. Không coi phương án H1 của lượt trước là lựa chọn mặc định. Ràng buộc bốn tuần không dùng để loại câu hỏi trong bản đồ khám phá này; chưa sửa lịch triển khai thực tế hoặc cho chạy GPU.

## Phân công theo cấu hình người dùng yêu cầu

| Worker | Model / effort đã gửi tool | Nhiệm vụ | File sở hữu |
|---|---|---|---|
| evidence_sol | gpt-6.1-sol / high | Bổ sung nguồn sơ cấp, đặc biệt video, tracking, streaming, shift | EVIDENCE-UPDATE.md, evidence-update.json |
| questions_sol | gpt-6.1-sol / high | Mở rộng và phân loại câu hỏi, chọn câu hỏi có phép bác bỏ | QUESTION-BANK.md |
| critic_astra | gpt-6-astra / high | Phản biện giả định, nguồn, cách chọn vấn đề; đọc lại bản tổng hợp | CRITIQUE.md, FINAL-REVIEW.md nếu cần |

Chat chính điều phối, kiểm tra nguồn bổ sung X01–X04 và hợp nhất thành PROBLEM-MAP.md. Không có công cụ đổi model chat chính; không báo nó là một model/effort đã được cấu hình lại. Không tạo thêm worker ngoài ba worker trên.

Ước lượng trước dispatch: input chọn lọc 15–25k token, output ba worker 12–18k, tổng hợp/kiểm tra khoảng 20% thêm; đây là ước lượng điều phối, không phải số dùng thực tế hay trần người dùng yêu cầu. Chỉ trả manifest ngắn từ worker; không tải toàn bộ raw PDF vào chat điều phối.

## Bằng chứng nền

[Corpus cũ](../t07-fresh-research/CORPUS-50.md): 50 hồ sơ, 39 abstract/metadata, 10 đoạn phương pháp/thí nghiệm chọn lọc, 1 trích đoạn publisher. Không phải 50 bài đã đọc sâu. [Báo cáo cũ](../t07-fresh-research/REPORT.md) có ưu tiên H1 vì giới hạn 4 tuần/60 USD; ưu tiên đó không quyết định lượt mở rộng này.

Mỗi nguồn mới phải có URL sơ cấp, task, mức đọc, phạm vi đã thử. Mỗi câu hỏi là [design]; không suy từ “chưa có trong corpus” thành “chưa ai giải quyết”. Mọi “vượt trội” cần chỉ rõ endpoint, đối chứng, phạm vi và đánh đổi. Không hứa Q1/Q2, không xếp kiến trúc trước thí nghiệm.

## Quyết định về phạm vi

Ảnh tĩnh detection/segmentation là lõi. Video detection, MOT, SOT, streaming là các nhánh mở rộng rõ ràng, cần nhãn và evaluator tương ứng. Điều khiển camera/zoom quang học là mở rộng active perception, không được giả lập bằng crop rồi gọi là thu thêm thông tin thực. Ground-camera anti-UAV không được gộp với aerial-view detection.

Không chạy training, không chi tiêu, không gửi dữ liệu ra người khác, không push trong lượt này.
