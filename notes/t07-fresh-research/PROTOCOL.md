# T07 — nghiên cứu lại từ đầu

Ngày bắt đầu: 2026-10-13. Điểm xuất phát duy nhất: T1-7 trong `notes/r3-topics-source.md`. Proposal v2.1 là lịch sử, không phải ràng buộc phương pháp. Giữ bài toán ảnh trên không, đa tỷ lệ, vật thể nhỏ/dày; kiểm tra riêng detection, OBB và segmentation.

## Ràng buộc người dùng

- 4 tuần từ 13/10/2026; mốc kết thúc kế hoạch 09/11/2026 (28 ngày gồm ngày bắt đầu).
- Kaggle nếu có quota; tối đa khoảng 60 USD chạy Modal. Không giả định GPU/quota Kaggle hoặc tốc độ train khi chưa đo.
- AI hỗ trợ tìm, đọc, code, phân tích; không thay thế thực nghiệm hay phản biện độc lập.

## Quy trình

1. Xác định failure mechanism trước khi chọn kiến trúc.
2. Tuyển 50 tài liệu có vai trò rõ: trực tiếp, cơ chế chuyển giao, dữ liệu/baseline; không gọi tất cả là 50 bài gần nhất theo thứ hạng tuyệt đối.
3. Dự kiến ban đầu: ba shard 12 bài và 14 bài do điều phối viên xử lý. **Amendment 13/10:** worker bị ngắt do usage limit. Điều phối viên tiếp quản; thay 5 bài nền bằng prior sát hơn. Corpus cuối và mức đọc thực tế trong DECISIONS.md; không nhận 3 shard đã hoàn thành.
4. Metadata phải có nguồn sơ cấp, năm, trạng thái công bố, URL, mức đã đọc, đóng góp, giới hạn suy luận, vai trò trong nghiên cứu mới. DOI chỉ ghi khi đã xác minh; không có DOI không đồng nghĩa bài không thật.
5. Mục tiêu ban đầu ít nhất 3 full-text reads/shard. **Mức đạt ở lượt khảo sát này:** 10 bài đọc đoạn phương pháp/thực nghiệm từ full text, 39 abstract/metadata, 1 publisher excerpts. Chưa đạt mục tiêu full-paper reads ban đầu; không dùng khảo sát này như full-method novelty clearance. Dùng bản OA hợp pháp; không đồng nhất tìm được PDF với đọc toàn bài.
6. Tổng hợp claim conflicts, 3–5 hướng cạnh tranh, closest prior art và phép thử loại bỏ. Điểm xếp ưu tiên là phán đoán thiết kế, không phải xác suất được nhận.
7. Kiểm chứng Q1/Q2 theo hệ xếp hạng, năm, category; kiểm chứng tiêu chí venue bằng hướng dẫn chính thức. Không dùng tier nội bộ thay tiêu chuẩn ban biên tập.
8. Chốt khuyến nghị có điều kiện theo 4 tuần/60 USD, protocol và budget cap; không bịa kết quả hoặc hứa Q1.

## Search và selection

Kênh: CVF Open Access, arXiv (tác giả), OpenReview, PMLR, publisher, website/code tác giả và dataset chính thức. Từ khóa: aerial/remote sensing + small/tiny/multi-scale + detection/oriented/instance segmentation; adaptive resolution, sparse computation, query allocation, Gaussian representation, scale-aware pretraining. Citation chaining từ bài then chốt; kiểm tra lại 2025–2026 cho prior art mới.

Giữ bài nếu giúp định nghĩa bài toán/dữ liệu, là baseline/counter-baseline, hoặc trực tiếp kiểm tra một cơ chế. Loại bài ngoài optical aerial 2D nếu không có cơ chế chuyển giao cụ thể; loại bản trùng arXiv/journal, chỉ chọn theo tên mà chưa đọc nguồn, và thông tin sau ngày 13/10/2026. Ghi nhận search không phải systematic review vét cạn.

## Chi phí đọc dự kiến

Ba worker độc lập, mỗi worker tối đa khoảng 12k token đọc/tổng hợp, bản ghi 12 bài và ghi chú chuyên sâu >=2k token; manifest trả về <=2k token. Điều phối khoảng 12k cho dữ liệu/venue và tối thiểu 20% dự phòng tổng hợp. Đây là ước tính lập kế hoạch, không phải số usage đo được. Không chạy GPU trả phí trong giai đoạn nghiên cứu tài liệu.

## Chuẩn bằng chứng

- [nguồn]: tác giả báo cáo; không tự nâng thành kết quả đã tái lập.
- [suy luận]: suy từ nhiều bài, cần kiểm tra.
- [design]: đề xuất cần thực nghiệm, chưa khẳng định novelty hay hiệu quả.
- Không có run thật => mọi hướng ở trạng thái chưa xác nhận tính khả thi end-to-end.
- Nêu rõ giả thuyết nào chết nếu baseline/đối chứng đơn giản giải thích được lợi ích.
