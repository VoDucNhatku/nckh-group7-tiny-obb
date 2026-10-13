# T07 — Focused final review

Ngày: 2026-10-13. Reviewer: Astra/high, cùng reviewer của `CRITIQUE.md`.

**Đối tượng:** bản `PROBLEM-MAP.md` 207 dòng được đọc trong lượt này. **Nguồn kiểm tra:** `EVIDENCE-UPDATE.md` N01–N18; `ROOT-SOURCES.md` X01–X04; corpus và critique đã đọc ở lượt trước. Đây là kiểm tra tính nhất quán với hồ sơ bằng chứng, không tự nhận audit lại toàn văn nguồn sơ cấp. Không đánh giá QUESTION-BANK đang được worker khác sửa.

**Kết luận:** không thấy lỗi P1 ngăn bàn giao. Bản đồ đủ rộng, không khóa H1/kiến trúc, có segmentation và phân biệt task đúng. Có ba sửa P2 nên hoàn tất trước giao và hai sửa P3 ngắn. Các số dòng là vị trí ở bản draft đã đọc, có thể đổi sau edit.

## P2-1 — Giới hạn của bằng chứng streaming chưa được giữ ngay ở phần tổng hợp

**Vị trí:** M07/M09, dòng 53/55; P3 dòng 91–95; dữ liệu dòng 194/196.

**Vấn đề cụ thể:** P3 đã cảnh báo HARD có scheduling assumptions, nhưng không ghi giả định nào; DroneEyes được dùng hỗ trợ câu “aerial streaming đã có prior” mà giới hạn causal/offline comparator và tốc độ chưa đi cùng. Bản map không khẳng định sai số liệu, nhưng người chỉ đọc nó chưa thấy phạm vi rất hẹp của bằng chứng được viện dẫn cho chương trình ưu tiên P3.

**Đối chiếu nguồn:** N04 ghi thí nghiệm MOT streaming chính **Car, frame interval 2s, replicated full-machine workers/no queue**; N05 ghi SkyAnchor causal, MLLM baselines ở Table II dùng native offline mode, tác giả chưa coi hệ thống phù hợp high-speed closed-loop/native frame rate. Cả N04/N05 là preprint, chưa xác lập peer review.

**Sửa tối thiểu:** sau đoạn phép thử P3 thêm: “HARD là preprint với thí nghiệm streaming MOT chính trên Car, chu kỳ frame 2 giây và default worker replicas tránh queue; đây không phải chứng cứ trực tiếp cho một GPU onboard xử lý luồng frame nhanh. DroneEyes/SkyAnchor là causal referring segmentation, nhưng bảng so sánh có offline baselines và tác giả chưa đạt high-speed closed-loop/native frame rate. Các kết quả này là prior về formulation, chưa xác nhận hiệu quả của protocol P3.”

Không cần mở rộng tìm kiếm hay thêm task để sửa điểm này.

## P2-2 — Metric segmentation cần gắn trực tiếp với supplied-box protocol

**Vị trí:** M06 dòng 52, P5 dòng 115–117, bảng dữ liệu dòng 193.

**Vấn đề cụ thể:** map đã phân biệt GT/predicted prompt và đã nhắc teacher masks, nhưng dòng M06 đặt chung “Mask AP” cạnh N18 mà không nói kết quả N18 là **given box→mask**. Điều này dễ biến bằng chứng conditional mask quality thành bằng chứng end-to-end instance segmentation. Đây là thiếu điều kiện sát citation, không phải cáo buộc tác giả N18 báo sai.

**Đối chiếu nguồn:** N18 §4.1 dùng supplied bounding boxes; ReSOS masks được sinh từ SODA-A OBB rồi manual filtering, không phải toàn bộ masks được vẽ thủ công. N18 là **CVPR Findings 2026**, không là main-track.

**Sửa tối thiểu:** cột evidence M06 viết rõ “SOPSeg đánh giá given-box→mask; ReSOS dùng masks sinh bởi teacher và lọc thủ công [N18]”. Cột metric tách “conditional mask IoU/boundary quality khi box có sẵn; mask AP cho pipeline automatic/predicted-box có protocol confidence và matching đầy đủ”. Không dùng mask AP mới để so trực tiếp với headline conditional result của N18. Giữ phần cùng supervision/teacher đang có.

## P2-3 — “Bác module” chưa phải “bác giả thuyết” ở P1/P2/P5

**Vị trí:** P1 dòng 71/75; P2 dòng 81/85; P5 dòng 113/117.

**Vấn đề cụ thể:** giả thuyết P2 nói annotation ambiguity giải thích một phần bất ổn; điều kiện dừng là “chuẩn hóa nhãn ... đã xóa khác biệt”. Kết quả đó thực ra có thể **ủng hộ** giả thuyết annotation và chỉ bác nhu cầu head mới. Tương tự, P5 nói chất lượng nhãn giải thích khác biệt gán cho kiến trúc; sửa nhãn làm lợi ích kiến trúc biến mất cũng ủng hộ P5. P1 mạnh hóa resize/full detail giải thích gain cũng không tự bác mệnh đề đáp ứng phụ thuộc scale mismatch. Map đã phân biệt insight/module một phần, nhưng nhãn “giả thuyết có thể bác” vẫn chưa có kết quả nào thực sự bác mệnh đề khoa học.

**Sửa tối thiểu:** giữ các cổng “dừng module”, thêm riêng một dòng “Kết quả bác giả thuyết khoa học” cho mỗi programme, hoặc đổi nhãn hiện tại thành “giả thuyết định hướng — cần operationalize”. Các dòng có thể dùng:

- **P1:** “Sau kiểm soát size/density/context, thêm biến chất lượng quan sát hoặc scale mismatch không cải thiện giải thích/dự đoán response ngoài ngưỡng tương đương thực dụng được khóa trước xác nhận.”
- **P2:** “Bất đồng annotation/biểu diễn tương đương thấp ở nhóm được tuyên bố, không dự báo instability, và phép chuẩn hóa/reannotation không đổi kết quả ngoài ngưỡng đã khóa.”
- **P5:** “Sau audit độc lập, thay đổi chất lượng nhãn không tạo tác động có ý nghĩa thực dụng; chênh lệch giữa kiến trúc vẫn giữ trên cùng annotation access.”

Đây là design suggestions, không gán ngưỡng số tùy ý. Không dùng “p>0.05” đơn thuần như bằng chứng không có tác động; phép thử phải có độ chính xác đủ cho kết luận tương đương thực dụng.

## P3-1 — PointSR: thay lời dè dặt bằng mô tả đã xác minh

**Vị trí:** M07 dòng 53, “không được mặc nhiên coi là video fusion”.

N09 §4.2 đã xác minh temporal ensembling xảy ra qua epoch/iteration, không phải frame. Sửa thành: “Temporal-Ensembling Encoder của PointSR gom pseudo-box shapes qua quá trình huấn luyện, không fuse các frame video [N09].” Câu hiện tại không sai nhưng để mở một sự mơ hồ mà nguồn đã giải quyết.

## P3-2 — N11 đang được trích nhưng cơ chế không nằm trong câu evidence M10

**Vị trí:** M10 dòng 56; P4 dòng 107.

Câu M10 liệt kê RWDS, RGB–IR, multimodal tracking, camera–LiDAR, sau đó trích thêm N11. N11 là **sequential domain-incremental detection, replay và class-pruned known-category protocol**, không thuộc ba cơ chế multimodal kia. Sửa bằng cách thêm đúng cụm mô tả này hoặc bỏ N11 khỏi riêng dòng M10; P4 có thể giữ như prior chuyển giao. Không suy N11 đã chứng minh zero-label adaptation hoặc thắng mọi dataset; draft hiện chưa phạm hai claim đó.

## Các điểm đã kiểm tra và không cần sửa

- Không còn ưu tiên theo $60 hay cost; H1 đã trở về câu hỏi ngang hàng. Câu ghi lịch cũ chưa sửa là mô tả trạng thái tài liệu, không được dùng làm bộ lọc khoa học trong draft.
- 13 mục tiêu được gọi đúng là diagnostic axes; 5 programmes tránh yêu cầu thực hiện tất cả. P1/P2/P3 được ưu tiên phân tích với lý do rõ, không dự đoán mức tăng điểm.
- Detection/instance/semantic segmentation, video detection/MOT/SOT, streaming và active observation được phân biệt. Dữ liệu camera mặt đất không bị gán nhầm là UAV ego-motion.
- Segmentation có M06/P2, box–mask controls, teacher/annotation controls và nhánh referring video; không bị làm fallback sau H1.
- Zoom native, interpolation, SR-assisted learning và quan sát quang học được phân biệt. SuperYOLO training-only SR branch được mô tả đúng với N16.
- Không có claim “gap đã xác nhận”, firstness, SOTA hay venue-worthiness; độ đọc và chưa chạy thí nghiệm được công khai.
- F04 không bị gán strawman “chỉ coverage”; geometry covariance không bị gọi calibrated epistemic uncertainty; DOTA+iSAID không bị coi hai miền độc lập.
- MessDet được dùng như prior rotation equivariance đã tồn tại, không nhận strict-versus-approximate equivariance là câu hỏi chưa ai nghiên cứu.
- OpenRSD được giữ là open-prompt HBB/OBB prior; không suy unknown rejection đã được giải. X04 được dùng cho scheduling/forecasting, không nhận latency-aware perception là ý tưởng mới.
- Reliability lập luận ở dòng 144 có đủ điều kiện additive/risk-neutral/true conditional mean và cảnh báo AP không additive; không cần sửa.

**Sau sửa:** chỉ cần đọc lại các đoạn đổi và kiểm tra câu source-boundary giữ đúng evidence. Không cần mở thêm scope hoặc chạy thực nghiệm để hoàn tất bản đồ vấn đề này.

## Disposition sau sửa — 2026-10-13

Đã đọc lại các đoạn sửa của `PROBLEM-MAP.md`, không mở rộng phạm vi review.

| Finding | Trạng thái | Căn cứ đóng |
|---|---|---|
| P2-1 — giới hạn streaming | **Đã xử lý** | P3 ghi rõ HARD preprint, Car, frame interval 2 giây, replicated workers/no queue; SkyAnchor causal nhưng MLLM baselines offline và chưa phù hợp high-speed closed-loop/native capture rate. Không suy runtime onboard. |
| P2-2 — supplied-box segmentation | **Đã xử lý** | M06 tách conditional IoU/boundary với given box và mask AP của pipeline tự động; phần nguồn N18 nêu teacher-generated masks từ OBB và lọc thủ công, không đồng nhất GT prompt với automatic segmentation. |
| P2-3 — scientific falsifier khác module rejection | **Đã xử lý ở mức bản đồ thiết kế** | P1/P2/P5 đã có điều kiện phản bác mệnh đề khoa học riêng; P3/P4 cũng tách giả thuyết và phương pháp. Quy ước chung nói endpoint/nhóm điều kiện/biên thực dụng chưa khóa, không dùng nonsignificance làm equivalence. Không diễn giải đây là preregistration hay protocol đã kiểm định. |
| P3-1 — PointSR | **Đã xử lý** | M07 ghi rõ ensembling qua epoch/iteration huấn luyện, không phải video fusion. |
| P3-2 — Active-DDC mapping | **Đã xử lý** | M10/P4 ghi domain-incremental sequential detection có replay, không zero-shot/source-free/unlabeled adaptation mặc định; quyền thích nghi miền đích phải khai báo. |

**Finding còn mở: không có trong phạm vi review này.** Bản đồ có thể bàn giao với trạng thái câu hỏi/thiết kế sơ bộ đã công khai. Khóa metric, effect margin, split và phép kiểm định là công việc thực nghiệm tương lai, không phải lỗi phải hoàn tất trong deliverable hiện tại. Không có xác nhận mới về novelty, superiority hoặc khả năng chạy end-to-end.
