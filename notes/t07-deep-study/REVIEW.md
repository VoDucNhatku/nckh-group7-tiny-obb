# Final review — DEEP-REPORT và RESEARCH-PROMPT

**Ngày:** 2026-10-13. **Reviewer:** Astra/high, cùng reviewer ở các lượt trước. **Phạm vi:** `DEEP-REPORT.md`, `RESEARCH-PROMPT.md`; đối chiếu các claim/bảng số được trích với `CASEBOOK-STATIC.md`, `CASEBOOK-TEMPORAL-MASKS.md`, `MULTIVIEW-AND-CRITIQUE.md` và source context đã kiểm trong lượt này. Không audit code hay tái lập 11 cases; không xem đây là rà soát toàn bộ literature. V02/JCR đang được điều phối viên xác minh riêng, reviewer chưa xác nhận nội dung trang đó.

**Disposition ban đầu:** không có P1. Hai P2 cần sửa ngắn trước giao. Không tìm thấy sai số của tám hàng case-summary so với casebooks; công thức UGS đã kiểm độc lập trước đó, các ví dụ IoU/projection kiểm được theo giả định đã ghi. Không có claim novelty/superiority hoặc quy tắc tier→quartile được tái áp dụng.

## P2-01 — A/B/C đặt tên “Null” cho một mệnh đề không đối lập giả thuyết khoa học

**Spans chính xác:**

- A, đoạn **“Null cạnh tranh: strong full-detail + scale-matched baseline giải thích đủ gain; adaptive policy mới không có lợi ích thực dụng thêm.”**
- B, đoạn **“Null cạnh tranh: CMC + track management + confidence decay đơn giản giải thích đủ; model history/uncertainty mới chỉ thêm capacity hay smoothing.”**
- C, đoạn **“Null cạnh tranh: nhãn sạch + scale-normalized loss/assignment đủ; new distribution head chỉ regularize hoặc có thêm parameters.”**

**Vì sao cần sửa:** đây là các giải thích cạnh tranh rất hữu ích cho gain và nhu cầu module, nhưng không là scientific null đối lập trực tiếp với mệnh đề của mỗi chương trình. A có thể đúng rằng detail/recipe tác động riêng, đồng thời adaptive policy vô ích. B có thể đúng rằng stale history gây hại và confidence decay đơn giản khắc phục được. C có thể đúng rằng nhãn gây lỗi và cleaning đủ giải quyết. Do đó chấp nhận các “null” như hiện tại không bác các giả thuyết khoa học. Phần “bác bỏ/dừng” phía sau đã phân biệt đúng nhiều trường hợp; lỗi còn lại nằm ở nhãn và quan hệ logic của thẻ.

**Sửa tối thiểu:** đổi ba nhãn hiện tại thành **“Giải thích cạnh tranh / null về nhu cầu module”**. Thêm một dòng scientific H0 cho claim chính được chọn, ví dụ [design, chưa preregister]:

- **A:** sau kiểm soát recipe/context/supervision, native-detail access không tạo tác động riêng vượt biên thực dụng trong strata đã định trước. Nếu chọn recipe×detail interaction làm primary claim thì H0 phải nhắm đúng interaction, không thay bằng policy thắng/thua. Cụm “ở một số strata ... phù hợp” trong giả thuyết phải gắn strata được khóa trước confirmation, tránh chọn nhóm sau khi nhìn kết quả.
- **B:** trong protocol/strata đã định trước, hiệu ứng real history so no/repeated history lên endpoint chính không có interaction thực dụng với age/alignment như dự đoán. Tách H0 này khỏi “không cần learned gate”.
- **C:** sau các controls định trước, annotation ambiguity/label-quality intervention không giải thích phần failure có ý nghĩa thực dụng. Đây khác H0 “new distribution head không cần thiết”.

Các H0 này chỉ là cách viết phù hợp ở giai đoạn nghiên cứu; chưa yêu cầu điền ngưỡng số, chạy test hoặc khóa phương pháp thống kê trong lượt hiện tại. Có thể thay ví dụ bằng formulation khác miễn H0/scientific hypothesis thật sự đối lập theo endpoint và phạm vi.

**Sửa đồng bộ nhỏ ở RESEARCH-PROMPT §9:** trong yêu cầu “prior, prediction, null, control, endpoint và điều kiện dừng”, ghi **“scientific null riêng với null về nhu cầu module”**. §8 đang phân biệt bốn loại bác bỏ tốt; giữ nguyên.

## P2-02 — Trùng source IDs F01–F03 với corpus đang được tái sử dụng

**Spans chính xác:** DEEP-REPORT §2.1 trích **“[F02; N03/N04/N18]”**, projection trích **“[F03; phép suy ra từ mô hình chiếu]”**; bảng nguồn §8 định nghĩa:

- `F01 | VisDrone official task definitions`
- `F02 | AI-TOD-v2 official dataset`
- `F03 | OpenCV pinhole projection`

**Vì sao cần sửa:** cùng dự án/corpus nền đã dùng F01 = RiO-DETR, F02 = ASAHI, F03 = RWDS. Báo cáo vẫn tái sử dụng R02/N16/X01/G10 và dẫn corpus cũ; vì vậy đây là namespace chung có collision, dễ dẫn người đọc hoặc agent tới sai paper khi lần theo claim. Nội dung projection không bị sai, nhưng provenance ID không còn duy nhất.

**Sửa tối thiểu:** đổi ba nguồn nền thành `BASE01`, `BASE02`, `BASE03` hoặc prefix tương đương chưa tồn tại; thay toàn bộ in-text IDs, bảng nguồn và ledger mới tương ứng. Không sửa IDs lịch sử trong corpus. URLs và mô tả nguồn hiện tại có thể giữ.

## Những phần kiểm tra không phát hiện lỗi cần sửa

| Hạng mục | Kết quả kiểm tra và giới hạn |
|---|---|
| Tám numerical case summaries | Các cặp QueryDet, SuperYOLO, UGS, GauCho, DynUAV, HARD, DroneEyes, SOPSeg khớp casebooks và giữ metric/task/comparator căn bản. Đây là kiểm tra consistency, không là tám independent replications. |
| UGS Eq.13/Table 6 | Derivative sửa theo softmax chain rule đúng; report giữ giới hạn printed formula ≠ implementation error/AP invalid. Increment IN +0.4 so CE và +1.2 so L2 đúng. |
| Tiny geometry examples | Resize 12→2→15 input pixels đúng theo giả định ngang; IoU ngang cho w=4/16/64 đúng khi δ=1; pinhole footprint có điều kiện same-depth/parallel-plane được công khai. |
| Multi-view | Không bắt buộc; single-UAV ≠ single-camera; không universalize calibration; synthetic 3D/BEV không biến thành tiny 2D real proof; coverage/resolution/geometry/visibility được phân biệt. |
| Temporal/streaming | HARD Car/2s/replicas được giữ; DroneEyes referring/causal không bị coi là native-rate all-object MOT; semantic-memory storage không bị suy bounded từ FIFO tracking. |
| Segmentation | SOPSeg given-box mIoU không bị biến thành automatic mask AP; teacher-generated masks và prompt provenance có caveats. |
| Novelty và phạm vi | A–C được gọi [design], có prior gần/còn thiếu; không lấy sai công thức UGS làm bằng chứng hướng mới đúng. Không mở tất cả 13 axes hoặc khóa kiến trúc. |
| Venue/rubric | Nội bộ rubric được đánh dấu rõ, không deterministic tier→quartile, không acceptance promise. V01/V02 nằm ngoài 11-case source audit này; V02 do root kiểm riêng. |
| Research prompt | Yêu cầu evidence contract, selected-read limits, source contradictions, task boundaries và checkable reasoning; không yêu cầu hidden chain-of-thought hoặc triển khai trái scope. |

**Bước tiếp theo trong review:** đọc chỉ các spans đã sửa cho P2-01/P2-02 rồi ghi disposition. Không cần mở thêm nguồn/mở rộng task để khép hai finding này.

## Resolution sau sửa — 2026-10-13

Đã đọc các spans sửa của A–C, source table/in-text IDs, evidence-level table và RESEARCH-PROMPT §8.

- **P2-01: đã xử lý ở mức thiết kế nghiên cứu.** A–C hiện có H0 khoa học riêng theo effect/interaction, controls và strata; các null cũ được đổi thành giải thích cạnh tranh/điều kiện không cần module. Prompt yêu cầu đúng sự phân biệt này. Các thẻ chưa là preregistration: endpoint, primary contrast, strata cụ thể, biên thực dụng và độ chính xác cần thiết sẽ được khóa trước xác nhận, không bị diễn giải là đã chọn số hoặc đã chạy phép kiểm định.
- **P2-02: đã xử lý.** Ba nguồn nền đổi thành BASE01–BASE03; các trích dẫn trong nội dung và source table được cập nhật, không còn F01–F03 trong DEEP-REPORT. Prompt thêm quy tắc source namespace nhất quán, không đè IDs lịch sử.
- **Evidence levels:** bảng bổ sung phân biệt đọc nguồn, suy ra, giả thuyết và chưa biết; không biến literature synthesis thành replication hoặc novelty confirmation.

**Disposition cuối: không còn finding mở trong phạm vi review này; đủ điều kiện bàn giao research report và reusable prompt.** Điều phối viên báo đã mở nguồn sơ cấp V02; reviewer không tính đó là lượt kiểm V02 độc lập của mình.

**Residual limits:** review kiểm tính nhất quán của numerical summaries với casebooks, tự kiểm các ví dụ toán và đã kiểm trực tiếp UGS pages; không tái audit toàn bộ method/supplement/code của 11 cases. Chưa có benchmark độc lập, causal evidence của các giả thuyết A–C, xác nhận gap/novelty, hay bằng chứng superiority. Những giới hạn đó đã được công khai trong deliverable và không là lỗi còn phải sửa ở lượt research-only hiện tại.
