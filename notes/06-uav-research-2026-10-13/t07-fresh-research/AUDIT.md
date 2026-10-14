# Audit — phạm vi bằng chứng và kiểm tra bàn giao

Ngày 13/10/2026. Áp dụng hallucination-guard và verification-before-completion.

## Đã kiểm tra nội dung

| Claim | Kết quả | Căn cứ |
|---|---|---|
| Có 50 hồ sơ không trùng ID/title/primary URL | Kiểm tra bằng validate_deliverables.py | corpus-50.json và CSV |
| Đã đọc 50 full papers | Không được khẳng định | 39 A, 10 M, 1 E; M chỉ đoạn chọn lọc |
| 32 Crossref matches | Đếm lại bằng script | crossref-audit.json; các kết quả title mismatch/timeouts không dùng |
| AFWD-Net là nguồn thật | Primary publisher search + Crossref DOI/title khớp | Direct HTML bị chặn; chưa xác minh kết quả thực nghiệm |
| Dự đoán accuracy gain là gap mới | Bị bác | Dynamic Zoom-in CVPR2018 R13 |
| Gaussian head hoặc dynamic candidate count chưa có | Bị bác | G10 GauCho; G11 GSDet |
| DenseScout chỉ đánh giá coverage | Bị bác | Full text supplement §2.7 có frozen-backend closure |
| DOTA và iSAID là dữ liệu độc lập | Bị bác | iSAID official ghi dùng cùng ảnh DOTA-v1.0 |
| Q1 cần đổi architecture, Q2 cần đủ số module | Không có cơ sở là quy định venue | CVPR guidelines; journal quartile là metric ở cấp journal |
| Giá thuê GPU suy ra đủ số run | Không được khẳng định | Chưa profiling; bảng chỉ đổi giá/giây thành giá/giờ |
| H1 mới và chạy được trong 60 USD | Chưa được chứng minh; giữ nhãn candidate/design | Không có GPU run hoặc pilot baseline |
| RSL Q2 theo đúng hệ/năm/category trường yêu cầu | Chưa xác nhận | Publisher chỉ mới kiểm tra nhãn CiteScore Best Quartile; không đổi thành JCR/SJR |
| CVPR2027 registration/submission dates | Đã đọc lịch chính thức | 10/11 và 16/11/2026 AoE; không coi CFP snippet “final decisions Nov10” là đúng |

## Giới hạn kiểm chứng

Crossref title match xác minh hồ sơ bibliographic, không xác minh chất lượng hay đúng/sai kết quả. Một DOI có thể trỏ bản journal mở rộng sau conference; corpus ghi year/version note. Chưa rà soát retraction/correction toàn bộ 50 bài. Chưa đọc trọn full methods của mọi closest prior, chưa cài/chạy code tác giả, chưa xác minh tải trọn dataset/checkpoint.

Mọi novelty còn lại và ưu tiên feasibility là suy luận có điều kiện. Không có số mAP, confidence interval, runtime huấn luyện hoặc acceptance probability của nhóm được tạo giả. Không có kết luận “không ai làm” dựa vào tìm kiếm vắng kết quả.

## Các sửa chữa sau scan

1. Nhận ra R13 đã có gain prediction → bỏ claim gain-router nói chung là novelty.
2. Nhận ra DenseScout có closure → ghi rõ, không dựng đối thủ yếu.
3. Crossref trả nhiều bài không đúng title hoặc timeout → không lấy DOI của chúng.
4. Nhận ra một số paper đã xuất bản sau bản arXiv → dùng publication metadata khi khớp, giữ thời điểm phiên bản.
5. Giới hạn subagent làm giảm đọc full text → sửa PROTOCOL, DECISIONS và REPORT khớp mức thực tế.
6. Phân biệt quarter/quartile với chất lượng bài → loại suy luận T1/T2/T3 quyết định Q1/Q2.
7. Mục tiêu 4 tuần mới là 13/10–09/11, không lấy deadline roadmap cũ.
8. Nhãn gốc GSD có thể thiếu và iSAID chung ảnh DOTA → ghi vào protocol kiểm soát dữ liệu.
9. Không dùng số ảnh/crop làm số scene độc lập; không tính AP như trung bình AP ảnh.
10. Ngân sách giữ CPU/RAM và dự phòng, không ghi 60 USD = số giờ GPU thuần.

Scan lại các đoạn đã sửa: claim thực tế có nguồn; inference/design được gắn nhãn; các unknown được nói rõ. **Không nâng kết quả scan văn bản thành scientific validation.**

## Bàn giao

REPORT.md là cửa vào; CORPUS-50.md là bản đọc; corpus-50.csv/JSON cho lọc và tiếp tục đọc; EXPERIMENT-PLAN.md là các cổng thực nghiệm; DECISIONS.md giữ assumptions/claim cards.

verification.json ghi kết quả kiểm tra cấu trúc mới nhất. scripts thu thập/kiểm tra và source cache phục vụ truy vết, không phải code model. Chưa push, chưa nộp bài, chưa chạy paid GPU.
