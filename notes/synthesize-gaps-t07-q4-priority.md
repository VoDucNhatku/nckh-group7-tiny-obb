# #7 — Những paper đáng dùng làm nền tảng cho mục tiêu Q4

- **Scope:** xếp ưu tiên hướng nghiên cứu từ Excel #7; không xếp hạng chất lượng của chính các paper.
- **Worker:** admin → research-admin → paper-synthesize, mode gaps.
- **Ngày:** 2026-10-07.
- **Nguồn:** `notes/t07-slr-papers.xlsx`, sheet Tổng quan từng bài/Papers/Watchlist; các review đã đối chiếu PDF trong `scripts/t07-slr/data/paper_review_2026-10-06/verified_reviews.json`; `notes/t07-proposal.md`; `notes/t07-tier-upgrade.md`; `notes/claims-ledger.md`.
- **Ràng buộc:** hướng #7, một học kỳ, ngân sách Modal ≤ $100 theo đề xuất đang lưu. Chưa có số đo chạy thử xác nhận ngân sách.
- **Cách hiểu:** “4Q” được hiểu là Q4. Đây là đánh giá có điều kiện, không phải xác suất được nhận bài.

## 1. Lựa chọn ưu tiên

**Ưu tiên AI-TOD-R/DCFL (R1899) + YOLO26 (R0879/W01), dùng RFLA (R2391) và NWD/RKA (R2318) để xây lập luận và đối chứng.** Đây là hướng C-3 đang lưu: benchmark sạch, chẩn đoán gán mẫu dương và thử một sửa đổi nhỏ giữ hình dạng vùng chọn ứng viên. Độ đáng ưu tiên cao là **[suy luận]** từ mức sát đề tài, phạm vi thay đổi và khả năng kiểm tra cơ chế; chưa có thực nghiệm chứng minh OA-STAL có tác dụng.

Thứ tự hướng: **(1) gán mẫu dương cho tiny OBB; (2) nhiễu nhãn tiny OBB, dựa trên DN-TOD; (3) ảnh suy giảm chất lượng, dựa trên ESRTMDet.** Hướng 2–3 là ứng viên dự phòng, không phải việc phải chạy đồng thời.

Phạm vi chứng cứ có giới hạn: 42/80 bài chọn được đối chiếu PDF; 38 bài còn thiếu PDF chưa có đánh giá nội dung đầy đủ. Watchlist có các bản đọc bổ sung. Thứ tự này ưu tiên những nguồn đã có review kiểm chứng, không kết luận đã tìm ra lựa chọn tốt nhất trong toàn bộ văn liệu.

## 2. Các paper và vai trò thực tế

| Ưu tiên đọc | Paper / vị trí trong Excel | Vì sao đáng đọc cho mục tiêu này | Cách dùng và giới hạn |
|---|---|---|---|
| 1 | **R1899 — Oriented Tiny Object Detection: A Dataset, Benchmark, and Dynamic Unbiased Learning**, STT 1 | Sát nhất với bài toán tiny OBB; có AI-TOD-R, benchmark và phân tích learning bias/số mẫu dương | Là nguồn bài toán, dữ liệu và đối chứng. Không cần bắt đầu bằng tái thiết kế toàn bộ DCFL. PDF đọc là arXiv v1 2024; metadata TPAMI 2025 là nguồn xác minh riêng. |
| 2 | **R0879/W01 — Ultralytics YOLO26: Unified Real-Time End-to-End Vision Models**, STT 80 / Watchlist W01 | Có detector OBB và cơ chế STAL để nghiên cứu trực tiếp trên một hệ thống thực | Là baseline triển khai, không phải bài đã chứng minh STAL tốt trên AI-TOD-R. Nguồn đọc là preprint v1. Cần ghim code và tách STAL khỏi các thay đổi khác của YOLO26. |
| 3 | **R2391 — RFLA: Gaussian Receptive Field based Label Assignment for Tiny Object Detection**, STT 71 | Giải thích vì sao tiny object thiếu mẫu dương; dùng prior Gaussian và xếp hạng để gán mẫu | Là nền tảng cơ chế và đối chứng. Review này xét HBB; chuyển cơ chế sang OBB/YOLO cần triển khai lại, không phải tích hợp sẵn. |
| 4 | **R2318 — Detecting tiny objects in aerial images: A normalized Wasserstein distance and a new benchmark**, STT 2 | Giải thích độ nhạy của IoU với sai lệch vài pixel; NWD/RKA cho đối chứng về metric/gán mẫu | Dùng để kiểm tra liệu cải tiến đến từ vùng ứng viên hay từ thước đo. NWD trong bản đọc là HBB; không được gọi là giải pháp góc OBB đã hoàn chỉnh. |
| 5 | **W12 — Robust Tiny Object Detection in Aerial Images amidst Label Noise (DN-TOD)**, Watchlist W12 | Có bài toán nhiễu nhãn rõ, CLC/TLS và quy trình gây nhiễu thực nghiệm | Nền tảng hướng dự phòng về nhiễu vị trí/góc. Bản đọc là preprint HBB; nhiễu góc OBB là đề xuất của chúng tôi, không phải kết quả của DN-TOD. |
| 6 | **R2119 — ESRTMDet: An End-to-End Super-Resolution Enhanced Real-Time Rotated Object Detector for Degraded Aerial Images**, STT 45 | Sát oriented detection; tác giả nêu hạn chế cụ thể về suy giảm ×2, blur và nhiễu | Nền tảng hướng dự phòng về chất lượng ảnh. Không đồng nhất vật thể nhỏ do hạ mẫu nhân tạo với tiny object tự nhiên. Cần tái lập hệ SR/OBB và kiểm tra chi phí. |

Đây là thứ tự **đọc để xây hướng 1 trước**, không có nghĩa RFLA/NWD tự thân dễ thành bài mới hơn DN-TOD. Hai bài đầu mang bài toán và baseline; RFLA/NWD giúp thiết kế thí nghiệm và tránh đề xuất trùng cơ chế.

Nguồn trang PDF: R1899 p8 §IV-D, p9–10 §V và p15 §VII; R0879 p8 §3.3.3, p9 §3.4.3 và p17 §5; R2391 p3 §1, p6–8 §3.1–3.3; R2318 p2 §1, p8–9 §4; W12 p5–6 §4 và p11 §6; R2119 p6 §III và p14 §V–VI. Số trang là trang vật lý của đúng PDF đã lưu, không phải số trang journal.

## 3. Hướng 1 — thiếu mẫu dương ở vật thể tí hon có hướng

**Câu hỏi:** khi cùng model, dữ liệu và lịch huấn luyện, cách mở vùng ứng viên của STAL ảnh hưởng thế nào đến số mẫu dương và chất lượng phát hiện theo kích thước, tỉ lệ cạnh và mật độ vật thể? Giữ tỉ lệ cạnh khi mở vùng có giúp hơn cách mở độc lập hai cạnh không? **[design; cần thực nghiệm]**

Điểm cần nói chính xác: code `RotatedTaskAlignedAssigner.select_candidates_in_gts` đang công khai **giữ tham số góc**, nâng riêng chiều rộng/cao dưới `stride_val`, rồi chuyển hộp sang bốn đỉnh. Vì vậy không được viết “STAL bỏ góc xoay”. Giả thuyết cần kiểm là vùng ứng viên có thể mất tỉ lệ cạnh và trở nên gần vuông; đó chưa phải bằng chứng mất khả năng phát hiện. [Mã nguồn Ultralytics](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/utils/tal.py).

Đóng góp nên tập trung vào một chuỗi chứng cứ: baseline → chẩn đoán → sửa đúng cơ chế → thí nghiệm loại bỏ thành phần (ablation). Đo số ứng viên trước và số mẫu dương sau bước chọn/lọc, tỉ lệ GT không nhận mẫu dương, AP theo bin kích thước và tỉ lệ cạnh; kiểm tra cả cảnh đông vật thể. Không chỉ chứng minh có thêm ứng viên, vì thêm ứng viên cũng có thể tăng xung đột giữa các vật thể. **[đề xuất thiết kế thí nghiệm]**

Thí nghiệm tối thiểu để ra quyết định: giữ một YOLO-OBB cố định; so sánh TAL, STAL và biến thể giữ tỉ lệ cạnh; sau khi có tín hiệu mới thêm biến thể ngưỡng, P2 và dataset thứ hai. Khi so sánh với bảng paper gốc phải khớp giao thức; số không khớp giao thức chỉ đặt ở bảng riêng. Không bắt buộc tái lập mọi paper trong bảng nền tảng ngay từ đầu.

### Venue Claim Card
- **Proposal:** C-3, benchmark YOLO-OBB trên AI-TOD-R, chẩn đoán mẫu dương và OA-STAL, kiểm tra tổng quát hóa trên SODA-A.
- **Novelty tier:** T1 — sửa khâu chọn/gán mẫu lúc huấn luyện; benchmark và chẩn đoán không tự nâng tier. Đây là phân loại theo rubric, không phải khẳng định cơ chế chưa ai làm.
- **Venue band:** Q4 / hội nghị Scopus có điều kiện benchmark sạch và chẩn đoán rõ. Q3 chỉ theo các điều kiện C-3 đang lưu: APvt/APt nhất quán trên hai dataset, hai seed, cơ chế rõ và khảo sát lại đóng góp. Không cam kết được nhận bài.
- **Downgrade triggers:** không có phát hiện chẩn đoán rõ; biến thể không tốt hơn; xuất hiện nghiên cứu cùng đóng góp; không kiểm được dataset thứ hai. Nếu chỉ còn bảng so sánh mặc định, không mặc nhiên đủ thành bài báo.
- **Confidence:** medium cho ưu tiên, thấp cho hiệu quả chưa đo.
- **Ledger:** C-3, giữ nguyên claim đang lưu; không nâng lên C-7.

## 4. Hướng 2 — nhiễu nhãn vị trí/góc của tiny OBB

DN-TOD cho nền tảng về lọc mẫu nhiễu và khai thác xu hướng học qua epoch, nhưng bản đọc dùng hộp ngang. **[design; cần thực nghiệm]** Có thể đặt câu hỏi: cùng mức nhiễu vị trí hoặc góc lúc huấn luyện, mức suy giảm có khác theo kích thước/tỉ lệ cạnh; một quy tắc tái trọng số đơn giản có cải thiện tính vững không?

Chỉ gây nhiễu ở nhãn train; giữ tập đánh giá gốc và chuẩn hóa quy ước góc/đổi cạnh. Có đối chứng không xử lý nhiễu, đối chứng DN-TOD phù hợp và thí nghiệm tách từng loại nhiễu. Không gọi nhiễu tổng hợp là nhiễu thực đã đo trên AI-TOD-R. W10/TOLF đã nghiên cứu bất định định vị tiny object, nên “xử lý nhãn nhiễu cho tiny object” nói chung không còn là khoảng trống. Bản W10 có chi phí suy luận tăng (review p11 §4.6).

**[suy luận]** Hướng này có câu chuyện ứng dụng rõ nhưng xếp sau hướng 1: số mức/loại nhiễu và seed làm tăng số lần chạy; việc chuyển DN-TOD sang OBB chưa được xác minh thực thi.

### Venue Claim Card
- **Proposal:** ứng viên chẩn đoán nhiễu nhãn tiny OBB và thử tái trọng số lúc train, lấy DN-TOD làm nền tảng.
- **Novelty tier:** T1 — nghiên cứu thực nghiệm và điều chỉnh huấn luyện; không tuyên bố module mới hay tính đầu tiên.
- **Venue band:** Q4 / hội nghị phù hợp phạm vi, chỉ nếu có chẩn đoán có giá trị, phương pháp/đối chứng phù hợp OBB, kết quả ổn định và khảo sát lại công trình về nhiễu góc. Chưa có cơ sở nâng tier hoặc dự đoán mức cải thiện.
- **Downgrade triggers:** chỉ gây nhiễu rồi báo bảng; trùng hướng đã có; lợi ích chỉ ở một mức nhiễu; dữ liệu nhiễu tổng hợp không hỗ trợ kết luận ứng dụng.
- **Confidence:** low cho hướng mới; nội dung DN-TOD đã có nguồn PDF.
- **Ledger:** C-8, candidate.

## 5. Hướng 3 — tiny OBB trong ảnh suy giảm chất lượng

ESRTMDet nêu rõ chưa nghiên cứu blur nặng hơn và nhiễu bất quy tắc (p14 §V). **[design; cần thực nghiệm]** Hướng dự phòng là khảo sát sự tương tác giữa blur/nén ảnh/hạ mẫu với kích thước, sau đó thử một thay đổi nhỏ ở trọng số huấn luyện hoặc cách lấy mẫu suy giảm, thay vì mặc định xây lại cả mạng SR.

Giữ đúng hệ tọa độ OBB khi hạ mẫu; đánh giá cả ảnh sạch và suy giảm. Phải so sánh detector trực tiếp trên ảnh suy giảm, ESRTMDet phù hợp và biến thể đề xuất trong cùng setting. Nếu chỉ mở rộng danh sách kiểu suy giảm thì còn là phần kiểm định, chưa có điểm mới phương pháp. **[suy luận]** Tái lập nhánh siêu phân giải và quản lý nhiều mức suy giảm làm hướng này kém gọn hơn hướng 1.

### Venue Claim Card
- **Proposal:** ứng viên chẩn đoán tiny OBB dưới suy giảm chất lượng ảnh và thử điều chỉnh huấn luyện nhẹ, lấy ESRTMDet làm đối chứng.
- **Novelty tier:** T1 — chỉ chấm cho phạm vi chẩn đoán/điều chỉnh train mô tả ở đây; không kế thừa tier của kiến trúc ESRTMDet gốc.
- **Venue band:** Q4 / hội nghị phù hợp phạm vi, nếu có kết luận có cơ chế, cải tiến vượt đối chứng hợp lý trên ảnh sạch/suy giảm và khảo sát lại hướng SR/robust OBB. Thêm vài corruption vào test không tự đủ điều kiện bài báo.
- **Downgrade triggers:** chỉ có bảng robustness; lợi ích mất trên ảnh sạch; setting suy giảm không có lập luận; chưa tái lập được đối chứng SR.
- **Confidence:** low cho hướng mới; hạn chế tác giả ESRTMDet đã có nguồn PDF.
- **Ledger:** C-9, candidate.

## 6. Những bài hấp dẫn nhưng chưa ưu tiên cho Q4 học kỳ này

- **GCD — R1269, STT 20:** có mã nguồn; PDF p5 §V-A nói rotated detection là kỳ vọng tương lai, chưa có thí nghiệm OBB trong bản đọc. Đáng đọc để đối chiếu metric, nhưng chuyển HBB sang OBB chưa chứng minh mới vì đã có các metric Gaussian cho hộp xoay. Không dùng làm hướng chính chỉ vì tác giả viết “future work”.
- **Fourier Series Coder — W03** và hướng **C-7:** bài đọc p11 nêu nhiễu khi dùng harmonic cao; đây là một đầu mối nghiên cứu. Tuy nhiên, thiết kế biểu diễn/gating góc mới cần khảo sát và lập luận mạnh hơn. C-7 vẫn là ứng viên có điều kiện trong ledger, không tự động được nâng tier sau phiên đọc PDF. Với mục tiêu hiện tại, ưu tiên đo lỗi góc từ baseline trước.
- **Thêm P2/attention/backbone:** có thể dùng làm đối chứng. Ghép các thành phần sẵn có chưa tự tạo câu hỏi nghiên cứu hoặc chứng minh đóng góp. Đánh giá này áp dụng cho cách thiết kế đề tài, không kết luận những paper liên quan kém chất lượng.

## 7. Cổng khả thi — cả ba hướng chưa chạy được như mô tả

Kiểm thư mục ngày 07/10: `experiments/` hiện không có file; chưa có baseline nội bộ, throughput/VRAM hoặc kết quả training để xác nhận ngân sách. Không thấy thư mục dataset cấp dự án tên `data/` hoặc `datasets/`; các PDF trong cache không phải dữ liệu ảnh huấn luyện. Không suy ra dataset không tồn tại ở máy/nơi khác.

| Điều cần chốt | Hướng 1 / C-3 | Hướng 2 / C-8 | Hướng 3 / C-9 |
|---|---|---|---|
| Data | AI-TOD-R có OBB; SODA-A dự kiến để kiểm tổng quát hóa. Link công bố có, tải đầy đủ/split/evaluator chưa kiểm trong phiên này. | AI-TOD-R và nhãn OBB train; script nhiễu góc mới chưa có. Tập test giữ nguyên. | AI-TOD-R hoặc SODA-A, script suy giảm và phép đổi hệ tọa độ; chưa chuẩn bị. |
| Compute | ≤ $100 là ràng buộc, không phải kết quả ước tính đã xác nhận. Cần pilot và tính cả đánh giá/seed/dataset thứ hai. | Chưa đo; nhiều mức nhiễu có thể tăng số lần train. | Chưa đo; phần SR và patch ảnh lớn cần đo riêng. |
| Baseline | Có số tham khảo paper, chưa có baseline nội bộ cùng protocol. | Chưa có baseline OBB dưới nhiễu. | Chưa có baseline trên pipeline suy giảm nội bộ. |
| Dependencies / fallback | Repo Ultralytics/DCFL public; docs liệt kê YOLO26-OBB. Chưa cài/chạy hoặc xác minh tải checkpoint đầy đủ. Fallback baseline: YOLO11s-OBB, vẫn phải tái lập. | Repo DN-TOD public; stack MMDetection cũ. Fallback: benchmark ảnh hưởng nhiễu trên baseline YOLO-OBB đã tái lập, chưa gọi đó là DN-TOD tái lập. | Repo AISODET public và nêu stack/links weights. Download weights chưa kiểm. Fallback: detector OBB trực tiếp trên ảnh suy giảm; khi thiếu SR đối chứng phải giảm phạm vi claim. |

Nếu không tải được AI-TOD-R, chỉ khảo sát tiếp SODA-A/DOTA-v1 train→val sau khi kiểm nguồn tải và sửa rõ phạm vi dữ liệu; không xem đó là giữ nguyên benchmark tiny AI-TOD-R. Bất cứ baseline tái lập nào lệch paper đều phải so biến thể với baseline **nội bộ** trong cùng setting, không lấy chênh lệch với số published để quy công cho phương pháp.

Bước quyết định đầu tiên cho hướng 1: tải/kiểm evaluator, ghim commit, chạy thử một baseline YOLO-OBB, đo chi phí và phân bố số mẫu dương. Chỉ khi tín hiệu chẩn đoán có thật mới triển khai OA-STAL. Chưa chạy GPU hoặc bắt đầu implementation trong phiên đánh giá này.

## 8. Xác minh nguồn trực tuyến và tính mới

Đã đọc các nguồn chính thức dưới đây ngày 07/10/2026; kiểm repo/docs là kiểm tính hiện diện, không phải chứng minh code chạy hoặc mọi checkpoint/dataset tải được:

- [AI-TOD-R project](https://chasel-tsui.github.io/AI-TOD-R/) và [DCFL/AI-TOD-R repo](https://github.com/Chasel-Tsui/AI-TOD-R/blob/main/README.md): dataset/code links và hướng dẫn MMRotate.
- [YOLO26 docs](https://docs.ultralytics.com/models/yolo26/): hỗ trợ OBB, STAL và tên checkpoint; [tal.py](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/utils/tal.py): mở vùng chọn ứng viên hộp xoay như mô tả ở §3.
- [RFLA official repo](https://github.com/Chasel-Tsui/mmdet-rfla): code/config và hướng dẫn MMDetection.
- [DN-TOD official repo](https://github.com/ZhuHaoranEIS/DN-TOD): config, script nhiễu và các thành phần CLC/TLS. Phạm vi bản nội dung paper dùng để đánh giá vẫn là preprint đã lưu; không đồng nhất với bản journal mới chưa đọc.
- [ESRTMDet official repo](https://github.com/liufeinuaa/aisodet): xác minh code đã công bố, cập nhật hơn thông tin “will be released” trong Excel nguồn cũ; không sửa Excel trong phiên này.
- [GCD official repo](https://github.com/MArKkwanGuan/mmdet-GCD): code và stack cũ; không chứng minh đã có GCD-OBB.

Tra cứu hẹp với AI-TOD-R/YOLO/STAL không đủ chứng minh “chưa ai làm”. Kết quả tìm còn xuất hiện trang nhà xuất bản về **Cross-Domain Collaborative Enhancement for Tiny Object Detection in Remote Sensing Images**, DOI 10.11999/JEIT260317, có snippet nhắc AI-TOD-R; mở trang bài bị lỗi ở web tool. Đây là **đầu mối phải xác minh**, không dùng snippet để khẳng định cơ chế/so sánh, không thêm vào corpus hay sửa protocol. Trước khi viết introduction phải quét lại công trình mới và đọc các đối thủ gần nhất. Không sử dụng nguồn tổng hợp/blog làm bằng chứng kỹ thuật.

## 9. Claim Conflicts / phạm vi so sánh

Chưa xác nhận hai nguồn trong nhóm ưu tiên đưa ra kết luận trực tiếp trái nhau dưới cùng một setting. NWD/RFLA/DN-TOD bản đọc là HBB, AI-TOD-R/ESRTMDet là OBB; không lấy AP khác dataset, backbone, augmentation hoặc lịch train để kết luận paper nào hơn. Khác setting là giới hạn so sánh, không phải mâu thuẫn đã giải quyết.

Một phần mô tả assignment ở paper YOLO26 và mã nguồn có thể khác phiên bản/tham số; vì vậy báo rõ paper version và commit, đo trên đúng code ghim. Hiệu quả STAL trên COCO không suy ra hiệu quả trên tiny OBB. Không suy ra “gap toàn cầu” từ việc một bài không làm một cơ chế.

## 10. Kiểm khẳng định trước bàn giao

- PID/STT/tên paper/trạng thái PDF đã đối chiếu trực tiếp workbook hiện tại và review JSON; các 54 đường dẫn PDF trong review đều tồn tại.
- Mỗi nhận xét nội dung gắn với source/page của review; nhận xét ưu tiên và đề xuất mới có nhãn suy luận/design.
- Không có số gain dự đoán, xác suất accept, claim SOTA/first hoặc hạng quartile của journal cụ thể.
- Venue claims có tier, điều kiện và ledger; C-3/C-7 không đổi. C-8/C-9 chỉ là ứng viên chưa qua cổng khả thi.
- Chưa có thí nghiệm mới; không kết luận code chạy hoặc kế hoạch vừa ngân sách.

## Thuật ngữ (Glossary)

| English | Tiếng Việt | Giải thích ngắn |
|---|---|---|
| baseline | mô hình đối chứng | Mốc tái lập để so sánh biến thể trên cùng dữ liệu/cài đặt. |
| label assignment | gán mẫu huấn luyện | Chọn điểm/anchor học vật thể nào; khác việc người gán nhãn ảnh. |
| positive sample | mẫu dương | Điểm/anchor được giao học một vật thể cụ thể. |
| OBB / HBB | hộp có hướng / hộp ngang | OBB có góc xoay; HBB song song trục ảnh. |
| ablation | thí nghiệm loại bỏ thành phần | Đổi một thành phần mỗi lần để xác định nguồn tác dụng. |
| seed | hạt giống ngẫu nhiên | Chạy lại với ngẫu nhiên khác để kiểm độ ổn định. |
| T1 | mức mới dạng điều chỉnh | Phân loại trong rubric nội bộ, không phải quy định của journal. |
| Q4 | nhóm quartile thứ tư | Phải ghi hệ xếp hạng, năm và ngành khi chọn journal cụ thể. Không xác định chỉ từ nội dung đề tài. |

**Handoff:** đây là lựa chọn đọc/nghiên cứu; nếu triển khai, bắt đầu pilot và kiểm khoảng trống của C-3 trước. Không triển khai cả ba hướng đồng thời.
