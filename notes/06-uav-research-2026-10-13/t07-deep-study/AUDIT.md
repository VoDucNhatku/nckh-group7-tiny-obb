# Audit — deep study UAV tiny objects, 13/10/2026

## Quyết định chính

1. Người dùng xác nhận chỉ nghiên cứu sâu trước. Không viết detector/experiment pipeline, không train hoặc sử dụng paid GPU. Công cụ tính toán chỉ dùng kiểm toán công thức/số học và tính toàn vẹn tài liệu.
2. UAV-view tiny detection là điểm quy chiếu; multi-view được giữ như nhánh có điều kiện theo visibility/resolution/geometry/coverage. Không đồng nhất single-UAV với single-camera, 3D synthetic với tiny 2D thực hoặc referring masks với automatic detection.
3. Thu hẹp tổng hợp về ba câu hỏi A–C, tách H0 khoa học khỏi điều kiện dừng module. Không chốt architecture, novelty hay venue band. Chi phí không dùng lọc ý tưởng.

## Provenance và mức đọc

- Hai Sol/high đọc 4+4 cases; Astra/high đọc 3 multi-view exemplars và phản biện. Không tạo worker mới ở lượt tiếp tục này.
- Temporal casebook đã hoàn tất; worker chưa giao JSON sidecar ở bước khép lượt. Root dừng worker và chuyển 11 findings TF01–TF11 từ casebook sang temporal-claims.json, ghi provenance rõ; không gọi thao tác này là một lần đọc nguồn độc lập.
- Static: QueryDet, SuperYOLO, UGS, GauCho. Temporal/masks: DynUAV, HARD, DroneEyes, SOPSeg. Mỗi casebook ghi phần đã đọc, version, page/table, điều kiện số liệu và phần chưa đọc.
- Multi-view: Where2comm, UCDNet, UAV3D; phương pháp/evaluation chọn lọc. X01-audit trong multiview-sources.json là audit lặp của UGS, không phải paper thứ tư mới.
- Tổng lượt này: 8 cases + 3 exemplars; không cộng lại thành 11 papers mới ngoài corpus, không tuyên bố 50 full papers đã đọc.
- Official documentation: VisDrone, AI-TOD-v2, OpenCV pinhole model; Clarivate JCR category/quartile; CVPR 2026 review criteria. Web mở Clarivate blog bị lỗi; kết luận dùng official JCR basics đã mở thành công. Không tuyên bố mọi URL đều HTTP verified.
- Bản đọc SuperYOLO là pre-acceptance, UCDNet arXiv v1; chưa đối chiếu toàn bộ publisher-final differences. HARD/DroneEyes là preprint; SOPSeg thuộc Findings.

## Kiểm toán và giới hạn

- UGS Eq.13/Table 6: hai workers đối chiếu độc lập với rendered pages. Công thức chain rule đúng kiểm thêm bằng central finite differences trên logits [0,0,0] và [1,-0.5,2], step 1e-5; max error khoảng 1.2e-11. Đây là sanity check số học, không kiểm code/experiments của tác giả.
- Toy resize: 12×640/3840=2; 12×640/512=15. IoU lệch một pixel với cạnh 4/16/64: 0.6/0.88235294/0.96923077. Không phải dataset finding.
- UGS derivative issue không chứng minh AP hoặc implementation sai. IoU derivative audit trong static casebook và những source anomalies khác chưa được kiểm độc lập đồng đều; cần nguồn/code clarification nếu thành claim trung tâm.
- Những số trong bảng tổng hợp đối chiếu với casebooks/claim ledgers; không tái lập bằng detector runs. Không trộn metric hoặc so xếp hạng xuyên dataset.
- Review root report/prompt ghi ở [REVIEW.md](REVIEW.md). Hai sửa đổi quan trọng: tách scientific null khỏi no-module alternative; đổi IDs nền tảng sang BASE01–03 để không đè F01–03 của corpus cũ.
- Structural verification cuối đạt 10/10: ba JSON ledgers parse, 27 static claims/11 temporal findings có mã duy nhất, nguồn temporal resolve, ba multi-view exemplars không đếm UGS audit thành paper mới, 15 local links tồn tại, không còn IDs nền trùng, INDEX/C-15 xuất hiện một lần, review có resolution. Kết quả máy đọc ở verification.json. Đây không phải xác nhận đúng toàn bộ nội dung khoa học.

## Tình trạng lưu trữ

Tài liệu lưu local dưới notes/06-uav-research-2026-10-13/t07-deep-study; notes/INDEX.md đăng ký, claims-ledger thêm C-15. Quy tắc .gitignore hiện tại không track thư mục nghiên cứu này. Không đổi whitelist, không commit/push hoặc sửa proposal cũ. PDF/text caches phục vụ đọc local; chưa kiểm license để phân phối lại.

## Những phần còn mở theo bản chất nghiên cứu

Novelty scan khớp một primary claim; supplementary và implementation alignment; data access/split lineage; data-level failure measurements; chọn HBB/OBB/temporal endpoint; thí nghiệm kiểm A–C. Những việc đó chưa được giả vờ hoàn tất bằng literature review. Báo cáo hiện đủ làm cơ sở chọn câu hỏi và phép thử, chưa đủ chứng nhận một kiến trúc hay mức xuất bản.
