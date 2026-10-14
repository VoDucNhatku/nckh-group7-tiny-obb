# Audit — T07 problem map

Ngày: 13/10/2026. Đây là kiểm tra hồ sơ và logic đề xuất, không phải kiểm chứng thực nghiệm.

## Kết quả thực hiện

- Cấu hình worker thực tế qua spawn_agent: evidence_sol và questions_sol = gpt-6.1-sol/high; critic_astra = gpt-6-astra/high. Ba worker, không sinh thêm worker. Chat chính giữ điều phối, không tự nhận được đổi model.
- Sol bằng chứng bổ sung 18 hồ sơ N01–N18: 7 đọc chọn lọc full text, 3 trích đoạn method/analysis/dataset, 1 abstract+intro, 1 mô tả dataset chính thức, 6 abstract. Không gọi là 18 full-method audits.
- Điều phối viên kiểm thêm X01 UGS, X02 Point2RBox-v2, X03 HOTA và X04 Towards Streaming Perception, mức đọc trong ROOT-SOURCES.md; không đưa chúng ngược vào corpus 50 để tăng độ đọc đã báo của lượt trước.
- Sol câu hỏi đã hoàn thành 120 Q duy nhất, 12 nhóm, 12 thẻ ưu tiên. Một lượt gặp capacity error sau khi ghi file; cùng agent/model được gọi tiếp một lần và đã hoàn tất kiểm tra. Không thay model người dùng chỉ định.
- Astra đưa 20 failure modes và 8 nhóm giả thuyết cạnh tranh trong CRITIQUE.md. Review bản tổng hợp phát hiện 3 P2 và 2 P3; tất cả đã sửa và được cùng reviewer đọc lại các đoạn thay đổi, không còn finding mở trong phạm vi đó.
- PROBLEM-MAP.md: 13 trục cải tiến, 5 chương trình nghiên cứu, 12 câu hỏi tranh luận của điều phối viên. Các trục không được tính như 13 đề tài hoặc 13 module cần triển khai.

## Thay đổi sau phản biện

1. H1 không giữ thứ tự ưu tiên từ giới hạn 4 tuần/60 USD. Bỏ chi phí khỏi tuyển câu hỏi; không tự sửa lịch triển khai đang có.
2. Chốt phân biệt detection/video detection/MOT/SOT/segmentation/streaming và bốn nghĩa zoom.
3. Điều kiện risk-neutral/additive/conditional-mean được ghi đủ; reliability không tự có downstream utility. Không suy lập luận này thành định lý cho AP patch vốn không cộng độc lập.
4. Giới hạn HARD (Car, 2s, replicas/noqueue) và DroneEyes (causal method, offline comparator, chưa high-speed control) đặt ngay trong P3; cả hai được ghi preprint.
5. SOPSeg given-box→mask, ReSOS teacher masks/manual filtering; phân biệt conditional mask quality với automatic mask AP.
6. Tách bác giả thuyết khoa học khỏi bác nhu cầu module. Biên thực dụng/endpoint chưa khóa, không gọi thiết kế là preregistration hay runnable protocol.
7. PointSR temporal ensembling là qua training epochs/iterations; Active-DDC là sequential domain-incremental/replay, không zero-shot domain generalization.

## Kiểm tra tính trung thực

Nguồn/cơ chế đã được ghi ở EVIDENCE-UPDATE, ROOT-SOURCES và corpus nền. Mọi câu hỏi là [design]/suy luận, không nhận khoảng trống đã chứng minh. Không có số tăng hiệu năng dự báo, claim first/SOTA của nhóm hoặc band venue được cấp. Không thay kết quả tác giả báo cáo bằng xác nhận tái lập.

`validate_map.py` đã chạy: 14/14 kiểm tra cấu trúc đạt; 120 Q liên tục, 12 nhóm/12 thẻ, 13 mục tiêu/5 programmes, 18 N-ID unique, không trùng title với 50 hồ sơ cũ, các mã nguồn được dùng giải được và local links tồn tại. Đây không kiểm chứng novelty, độ đúng của mọi paper, khả năng tải dataset, external URL reachability hoặc hiệu năng phương pháp.

Một số CVF page trả 403 khi mở trực tiếp qua web tool; nguồn tương ứng có search-index primary excerpts/PDF và hồ sơ đọc của evidence worker. Không coi lỗi truy cập là thiếu paper, cũng không ghi rằng tất cả URL đã được HTTP-checked thành công.

## Giới hạn còn lại

Chưa audit toàn bộ method/supplement của mọi prior gần; chưa khóa một task hoặc central hypothesis; chưa chọn dữ liệu/checkpoint có thể chạy; chưa có baseline hay training. Optical zoom/closed-loop camera control cần nguồn chuyên biệt thêm nếu được chọn. Các biện pháp chẩn đoán tổng hợp cần kiểm tra cả dữ liệu thực. Các gợi ý ưu tiên phản ánh sức phân biệt của câu hỏi, không dự đoán mức tăng điểm hoặc cơ hội được nhận bài.

File lưu local, không chi GPU và không push trong lượt này. Review này đủ bàn giao một bản đồ vấn đề; không thay thế vòng literature clearance và experimental design của đề tài được chọn sau đó.
