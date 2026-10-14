# Đọc bộ nghiên cứu UAV tiny objects

Cập nhật 13/10/2026. Đây là đầu ra nghiên cứu tài liệu, chưa có detector runs. Người dùng đã yêu cầu đưa các đầu ra nghiên cứu lên GitHub và giữ repo public. Bản proposal nộp trường được giữ để đối chiếu; các hướng dưới đây chưa thay thế nó.

## Cập nhật 15/10/2026 — đọc trước

Các lượt nghiên cứu ngày 14–15/10 (ledger C-16 → C-18) đã được audit lại và sửa bằng **C-19**. Bản đúng hiện hành là [REPORT của audit](07-audits/t07-q2-audit-2026-10-15/REPORT.md).

- Ba đề tài ứng viên (R1, R2, R3) và các phép thử phân biệt chúng: xem REPORT §3.
- Những kết luận cũ đã bị rút: xem REPORT §2.
- [Phân tích lỗi của phiên 14–15/10](07-audits/t07-error-analysis-2026-10-15/ANALYSIS.md): sai ở đâu, vì sao, và việc nào đáng giữ.

Hướng dẫn đọc bên dưới (13/10) vẫn còn hiệu lực. "Ưu tiên A" ở đây là **tách tác động của scale khỏi cách học**. Đây không phải "hướng A" trong các note ngày 14/10 (STAL/coverage, C-16).

## Thứ tự đọc

1. [DEEP-REPORT](06-uav-research-2026-10-13/t07-deep-study/DEEP-REPORT.md): kết luận hiện tại, tám nền tảng, ba chương trình nghiên cứu và khi nào cần multi-view.
2. [CASEBOOK-STATIC](06-uav-research-2026-10-13/t07-deep-study/CASEBOOK-STATIC.md) và [CASEBOOK-TEMPORAL-MASKS](06-uav-research-2026-10-13/t07-deep-study/CASEBOOK-TEMPORAL-MASKS.md): tám cases có method, table/page, controls và giới hạn.
3. [MULTIVIEW-AND-CRITIQUE](06-uav-research-2026-10-13/t07-deep-study/MULTIVIEW-AND-CRITIQUE.md) và [REVIEW](06-uav-research-2026-10-13/t07-deep-study/REVIEW.md): kiểm tra multi-view, toán và phạm vi kết luận.
4. [PROBLEM-MAP](06-uav-research-2026-10-13/t07-problem-map/PROBLEM-MAP.md) và [QUESTION-BANK](06-uav-research-2026-10-13/t07-problem-map/QUESTION-BANK.md): 13 mục tiêu/120 câu hỏi, dùng để tìm hiện tượng cần giải thích.
5. [CORPUS-50](06-uav-research-2026-10-13/t07-fresh-research/CORPUS-50.md): bản đồ tài liệu nền, kèm CSV/JSON. Mức đọc của corpus gốc là 39 abstract/metadata, 10 selected full-text excerpts, 1 publisher excerpts; casebooks sau đó nâng độ sâu một số nguồn. Không gọi đây là 50 full-method audits.
6. [RESEARCH-PROMPT](06-uav-research-2026-10-13/t07-deep-study/RESEARCH-PROMPT.md): yêu cầu bằng chứng và phản biện để tiếp tục nghiên cứu.

## Đề xuất bước tiếp theo — vẫn nghiên cứu trước

**Ưu tiên A: tách tác động của scale khỏi cách học; dùng C về nhãn/định vị làm giải thích cạnh tranh.** B về temporal chỉ mở khi chọn video endpoint. Multi-view chỉ mở khi chứng minh view bổ sung cung cấp visibility, geometry, resolution hoặc coverage cần thiết. Đây là ưu tiên nghiên cứu, chưa có novelty hoặc superiority claim.

| Việc tiếp theo | Đầu ra cụ thể | Điều kiện để chốt |
|---|---|---|
| 1. Khóa một câu hỏi có thể bác | Problem statement một trang: ảnh từ UAV, input/output, native/input tiny definition, hiện tượng và primary endpoint | Không dùng detection, tracking và segmentation thay nhau; chưa đưa tên kiến trúc vào làm kết luận |
| 2. Đọc sát cơ chế của A/C | Ma trận prior về detail preservation, scale/assignment/loss và annotation/geometry; bắt đầu từ QueryDet, SuperYOLO, UGS, GauCho cùng NWD/RFLA/DN-TOD đã có trong corpus | Mỗi dòng ghi task, mechanism, supervision, controls, assumption, phần đã đọc và chưa đọc; thêm paper chỉ khi đóng một lỗ hổng cụ thể |
| 3. Kiểm dữ liệu và protocol trên tài liệu gốc | Data/evaluator specification: nguồn ảnh và scene lineage, nhãn, splits, size bins, preprocessing, NMS/cap, data access; một bảng failure taxonomy | Xác định điều gì có thể kiểm trên dữ liệu và điều gì chỉ là giả thuyết; không đổi metric để thuận model |
| 4. Viết thiết kế phân biệt nguyên nhân | Factorial detail access × learning recipe, strong full-detail baseline, simple crop controls và label/normalization alternatives; scientific H0 riêng với module-stop | Chọn contrast chính, strata và biên thực dụng trước confirmation runs; dự đoán rõ kết quả nào khiến bỏ hướng |

Sau bốn đầu ra đó mới quyết định kiến trúc và code thí nghiệm. Đích gần là **một giả thuyết mạnh có thể kiểm**, không phải ghép nhiều module từ 50 bài. Không cam kết một kiến trúc mới hoặc Q1/Q2 trước khi có bằng chứng.

## Phạm vi chia sẻ và tái lập

- Ba thư mục t07-fresh-research, t07-problem-map, t07-deep-study chứa toàn bộ đầu ra tổng hợp/metadata/kiểm chứng được chia sẻ của đợt mới.
- PDF bài báo, raw HTML/text và rendered pages trong sources là cache local. Nguồn sơ cấp và locators nằm trong casebooks/JSON. GitHub chỉ chứa README giải thích cache; không có bản sao papers.
- Python scripts ở fresh-research/problem-map phục vụ thu thập và kiểm cấu trúc, không phải code model. Một số scripts đọc cache local và cần tải nguồn trước; không tuyên bố mọi script chạy được từ một clone rỗng cache.
- AUDIT/SESSION ghi trạng thái tại thời điểm từng lượt nghiên cứu hoàn tất. Các câu “chưa push” ở đó là lịch sử; cập nhật chia sẻ hiện tại nằm ở trang này và PR bổ sung bộ nghiên cứu.
- Registry INDEX có cả lịch sử local; không đồng nhất toàn bộ registry với danh sách files trên GitHub.

Kết quả kiểm tra cấu trúc không xác nhận novelty, tính đúng của toàn bộ paper hay hiệu năng. Mọi con số từ paper vẫn là tác giả báo cáo, chưa được nhóm tái lập.
