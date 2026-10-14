# Audit / session — 15/10/2026

## Yêu cầu và ranh giới

User yêu cầu đọc lại ngữ cảnh và nghiên cứu ngày14–15/10, nhận xét/phản biện để suy ra đề tài hướng Q2. Giữ #7 làm định hướng; nghiên cứu sâu trước, không implementation/train. Không lọc ý tưởng theo chi phí. Hai Sol và một Astra, reasoning high, theo yêu cầu trước còn hiệu lực. Không mở thêm agent. Không thay đổi visibility, commit hoặc push trong lượt này.

## Điều phối và artifacts

| Worker | Model / effort | Công việc độc lập | File |
|---|---|---|---|
| angle_prior_sol | gpt-6.1-sol / high | AQE/O2 method, experiment và giới hạn novelty | ANGLE-PRIOR.md |
| data_evidence_sol | gpt-6.1-sol / high | Paired labels, data lineage, CODrone/DroneVehicle, CSCWD task transfer | DATA-AND-TRANSFER.md |
| logic_critic_astra | gpt-6-astra / high | Toán/causal/venue reasoning; review bản tổng hợp và changed spans | LOGIC-CRITIQUE.md; REVIEW.md |
| Root | Phiên hiện tại | Đọc ngữ cảnh, venue primary sources, tổng hợp, sửa ledger và ghi chú lịch sử | REPORT.md; AUDIT.md; CACHE-MANIFEST.json |

Ước lượng điều phối trước fan-out: mỗi worker khoảng10–15k input/3–5k output, dự phòng tổng hợp20%. Đây là ước lượng kế hoạch, **không** phải usage đo được hay budget do user đặt. Không có số usage thực để báo.

Skills áp dụng: admin, research-admin, hallucination-guard, token-budget; đọc research-proposal-integrity như rubric nội bộ. Mapping T1/T2/T3→quartile trong rubric không được dùng như bằng chứng editorial. Chỉ ghi điều chỉnh trong dự án, không sửa skill/rule toàn cục.

## Nguồn root kiểm thêm

| ID | Nguồn | Độ sâu / phát biểu dùng được |
|---|---|---|
| RV01 | [CVPR2026 Reviewer Guidelines](https://cvpr.thecvf.com/Conferences/2026/ReviewerGuidelines) | Đọc phần review criteria, đặc biệt novelty/impact/soundness và đánh giá concept dù ít dataset. Dùng chống quy đổi can thiệp/số dataset thành chất lượng; không đại diện policy mọi journal. |
| RV02 | [ATSS accepted record CVPR2020](https://openaccess.thecvf.com/content_CVPR_2020/html/Zhang_Bridging_the_Gap_Between_Anchor-Based_and_Anchor-Free_Detection_via_Adaptive_CVPR_2020_paper.html), [arXiv1912.02424](https://arxiv.org/abs/1912.02424) | CVF search primary accepted metadata/abstract; direct open một lần lỗi, arXiv record mở được. Abstract-level, không audit method/code. Phản ví dụ cho assignment tự động bị coi thấp; không xếp quartile hội nghị. |
| RV03 | [JCR basics](https://clarivate.libguides.com/jcr/basics) | Đọc JIF Quartile: journal trong category. Không tra hay cấp quartile cho venue cụ thể. |
| RV04 | [TGRS scope](https://www.grss-ieee.org/publications/transactions-on-geoscience-remote-sensing/) | Đọc scope về methodological advancement/significant research và experimental description. Không phát biểu TGRS hiện là Q2/Q1, không suy số dataset cần/đủ. |
| RV05 | [TIDE ECCV2020](https://www.ecva.net/papers/eccv_2020/papers_ECCV/html/849_ECCV_2020_paper.php), [official project](https://dbolya.com/tide/), [official repo](https://github.com/dbolya/tide) | Abstract/project/README và selected search excerpt; chưa audit toàn method. Background cho error analysis, không dùng làm causal decomposition hoặc tuyên bố OBB hỗ trợ sẵn. Không cần dựa vào nguồn này để chứng minh phản ví dụ toán trong REPORT. |

Các nguồn AP01–02 và DT01–08 có locator/read-depth ở hai worker notes. Numerical pairs trong worker notes là authors report; root không tái lập độc lập. Các case QueryDet/SuperYOLO/UGS/GauCho kế thừa deep-study, không được gắn nhãn đọc toàn văn mới.

## Ba quyết định cần lưu

1. **Sửa nền trước chọn kiến trúc.** C19 rút venue mapping, cận phủ→optimum và sensitivity→identifiability; giữ lịch sử C16–18, đánh dấu revision và hộp đính chính để truy nguồn.
2. **Ưu tiên R1 có điều kiện về task.** Chưa giả định #7 cần OBB; cần giải thích lợi ích target góc. Giữ R2/R3 cạnh tranh, không ghép module trước khi có failure được chứng minh.
3. **Giữ dữ liệu nguồn, không nâng độ sâu đọc.** Sao lưu7file scan1015, hash source/destination đối chiếu. Manifest ghi recordcounts/uniqueIDs và phân biệt selection≈45 chưa tái dựng.

## Kiểm bịa, phản biện và giới hạn

- Đối chiếu claim↔source↔task: sửa O2 “size-blind”, CSCWD “direct competitor”, AQE “novelty chỉ còn size”, paired labels “independent ground truth”.
- Kiểm toán toán: giải tích square/rectangle counterexample; cận closed lattice và endpoint bounds có giả định; đây không phải thí nghiệm mô hình.
- Không suy nguyên nhân feature từ recall/candidate hoặc góc từ AP50–AP75; không phân chia causal error budget cộng100% thiếu định nghĩa/interventions.
- Astra review REPORT không thấy P1 trong phạm vi đọc, yêu cầu sửa hai P2: context/FOV/centering/overlap/fusion controls cho crop; calibration failure không tự xác nhận ranking/transfer. Root đã sửa, thêm điều kiện task cần OBB và chính xác hóa câu lattice; changed-span recheck ghi ở REVIEW.md.
- Các note lịch sử được giữ nội dung với cảnh báo có quyền ưu tiên. Không thể nói toàn bộ corpus đã hết lỗi. CDCEDet/MFN-Net/ARA và các prior khác vẫn còn khoảng trống độ sâu; novelty search chưa exhaustive.
- Chưa kiểm dataset archive/hash/matching, chưa tính tiny statistics từ annotations, chưa train/benchmark hoặc validate gain/calibration. Không xác nhận lịch nộp bài/khả năng nhận Q2/Q1.
- Thư mục audit và ba note14–15/10 bị whitelist `.gitignore` giữ local; không tự sửa chính sách xuất bản trong lượt review. Cache không được đưa vào Git.

## Xác minh cuối

Kết quả kiểm cấu trúc/link local/manifest/diff được ghi ở `VERIFICATION.json`. Phạm vi là tính toàn vẹn artifacts và thay đổi tài liệu, không xác minh mọi paper claim hoặc kết quả thực nghiệm. Review khoa học có giới hạn được ghi riêng, không thay thế empirical validation.
