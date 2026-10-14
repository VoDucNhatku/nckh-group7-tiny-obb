# Review bản tổng hợp REPORT.md

Ngày 15/10/2026. Reviewer: logic_critic_astra. Phạm vi: logic/toán, mức khẳng định và tính nhất quán với LOGIC-CRITIQUE, ANGLE-PRIOR, DATA-AND-TRANSFER. Không đọc lại paper ngoài; kết luận về prior dựa vào worker records, không phải xác minh paper độc lập lần hai. Không sửa REPORT, không code/train.

**Kết luận: có thể gửi sau hai bổ sung P2 ngắn dưới đây; không phát hiện P1 còn lại trong phạm vi review.** Ưu tiên R1 được ghi là lựa chọn điều tra, không thành kết luận novelty hoặc lời hứa Q2. Không cần thêm module, dataset hay thí nghiệm trước khi gửi một báo cáo nghiên cứu như hiện tại.

## P2-1 — R3 cần khóa các biến mà crop thay đổi ngoài độ phân giải

**Vị trí:** §3, R3, “Thiết kế quyết định”.

Full image so với crop/tiling còn đổi context, field of view, vị trí object trong crop, phân bố đối tượng và số lần cùng object được dự đoán; fusion/merging có thể tạo gain. Ghi native support, giữ coverage và dùng evaluator chung chưa tự khớp các yếu tố này. Nếu protocol thiếu controls, câu hỏi “zoom giúp vì detail hay learning” chưa nhận dạng được ngay cả khi teacher/loss đã khớp. DP §4A và CASEBOOK-TEMPORAL-MASKS cũng đã nhấn mạnh confound này.

**Sửa tối thiểu đề nghị:** thêm một câu: “Khớp hoặc factorial hóa context/FOV và vị trí đối tượng trong crop; với tiling, ghi repeated views và giữ fusion/postprocessing tương ứng để tách gain từ detail khỏi gain từ crop/context/duplicate scoring.” Đây là thiết kế cần bổ sung, không yêu cầu chạy trong lượt này.

## P2-2 — Không calibration/transfer được không tự suy ra score ranking hữu ích

**Vị trí:** §3, R1, “Quy tắc dừng/hạ claim”: “Nếu quality không calibration/transfer được, hạ về score dùng cho ranking.”

Calibration và ranking khác nhau: score không calibrated vẫn có thể xếp hạng tốt. Nhưng không transfer được có thể làm cả ranking hỏng trên miền đích. Đổi tên output không là bằng chứng rằng công dụng yếu hơn còn đứng.

**Sửa tối thiểu đề nghị:** “Nếu không calibrated, chỉ giữ claim ranking khi usefulness của ranking đã được kiểm riêng; nếu không transfer được thì giới hạn claim vào miền đã xác nhận, không mặc định score vẫn dùng được trên miền mới.”

## Chính xác hóa toán nên đưa cùng lần sửa

§2, hàng √2s đang viết “lưới đóng vô hạn”. Tính đóng cần thuộc **miền ứng viên**. Cách viết đủ điều kiện trong một câu: “Hình chữ nhật đóng có cạnh ngắn ≥√2s luôn chứa ít nhất một điểm của lưới vuông vô hạn bước s, ở mọi vị trí/góc.” Phần phía dưới đã phân biệt đúng OBB ≥/≤ và HBB >eps; không cần thay đổi kết luận đó. Đây là chính xác hóa giả định đã có trong LOGIC-CRITIQUE, không là định lý mới.

## Các điểm đã qua review

- Đã tách coverage khỏi positive/gradient/AP optimum; ví dụ bằng mean nhưng khác xác suất rỗng đúng dưới pha đều, biên measure-zero. Không còn lấy equal-area làm cận “bậc hai” cho AP.
- arctan được giới hạn về perturbation vuông góc; asin có điều kiện 2δ<L. Cả hai không bị dùng làm cận dưới lỗi/expected loss hay physical identifiability.
- Chưa có knee không đóng toàn bộ hướng. Histogram và paired HBB/OBB không bị gọi là chứng cứ độc lập về nhãn đúng hoặc thiếu thông tin.
- R1 giữ metric OBB gốc, misses và mọi GT; calibration/risk–coverage không thay detection utility. Không đồng nhất Gaussian shape covariance với predictive uncertainty.
- O2-DETR được mô tả là distributional refinement có scale hình học, không còn khẳng định tuyệt đối size-blind; AQE prior và phạm vi chưa đọc được giữ đúng theo ANGLE-PRIOR.
- CSCWD khác task được nêu rõ; dữ liệu tiny của CODrone/DroneVehicle chưa được xác nhận. Source overlap, actual overlap và leakage không bị đồng nhất.
- Không còn ngân sách lỗi cộng được hoặc residual recall ⇒ feature cause. Các phương án được giữ cạnh tranh, không cộng thành siêu kiến trúc.
- Mapping T1/T2/T3→quartile và luật ba dataset đã được rút. ATSS chỉ minh họa assignment có thể là đóng góp mạnh, không được dùng làm bảo đảm STAL đủ Q2. Phạm vi nguồn editorial được ghi rõ.

## Điều cần giữ trong C-19/cảnh báo note cũ

Ghi REVISION do sửa luận cứ, không do đã có kết quả thực nghiệm. Nêu rõ ledger C-13–15 từng bác mapping tất định và C-16–18 đã tái đưa vào; tránh coi audit lần này là đổi khẩu vị venue. Cảnh báo phải dẫn tới bản tổng hợp và ba audit; các claim cũ về optimum/identifiability/prior không được tiếp tục dùng như tiền đề đúng. Các note vẫn có giá trị lịch sử và prior đã đọc, nên không cần phủ nhận toàn bộ chúng.

**Giới hạn review:** đã đọc REPORT và ba audit; chưa kiểm cache/hash, metadata 174 ID, paper/website chính thức hoặc việc các chỉnh sửa sau review đã thực sự được áp dụng. Việc xác nhận nguồn/manifest thuộc bằng chứng của các worker và tổng hợp admin.

## Changed-span verdict — sau sửa, 15/10/2026

**PASS trong phạm vi recheck; không còn yêu cầu sửa material trước khi gửi.** Kết luận này thay trạng thái “có thể gửi sau hai bổ sung P2” ở đầu file. Chỉ kiểm các đoạn mới và liên kết sửa claim; không audit lại body lịch sử hoặc nguồn ngoài.

- **P2-1 đã xử lý:** R3 nêu context, FOV, vị trí vật, số lần quan sát chồng lấn và fusion/NMS controls trước khi quy gain cho chi tiết.
- **P2-2 đã xử lý:** R1 chỉ giữ ranking claim khi usefulness/transfer được kiểm riêng; không dùng đổi tên uncertainty thành score để cứu transfer thất bại.
- **Giả định hình học đã rõ:** REPORT §2 ghi hình chữ nhật đóng, cạnh ngắn ≥√2s, lưới vuông vô hạn bước s. Không nâng guarantee thành final-positive hoặc AP optimum.
- **Target gate phù hợp:** đoạn mở §3 hỏi OBB/góc có giá trị cho ứng dụng không, cho phép ưu tiên R2/R3 nếu không. Điều này làm rõ điều kiện của ưu tiên R1 và không bắt buộc đổi target để dựng head. Giữ phân biệt box-axis/heading và evaluator/nhãn khi so HBB–OBB.
- **C-19 đã ghi đúng bản chất revision:** sửa diễn giải toán/nhân quả, prior đọc sâu và mapping venue; không tuyên bố có detector result, novelty hay band Q2/Q1 mới. C-16/C-18 đã trỏ revised→C-19; C-17 giữ chuỗi lịch sử →C-18. Header ledger nhắc C-13–15 research-only vẫn có hiệu lực.
- **Đã kiểm hộp cảnh báo đầu năm file:** venue-assessment, q2-path, direction-map, proposal-v2-EN và tier-upgrade. Các hộp nêu C-19, dẫn REPORT, đánh dấu diễn giải/body cũ là lịch sử hoặc bị thay thế; các lỗi coverage, sensitivity, prior, transfer và venue được rút đúng theo scope từng file.

Giới hạn còn nguyên: PASS là tính nhất quán và mức khẳng định của bản nghiên cứu, không xác nhận giả thuyết thực nghiệm, tính mới toàn lĩnh vực, metadata/cache hoặc triển vọng nhận bài. Không cần mở thêm vòng review chỉ vì chưa có các kết quả mà báo cáo đã ghi rõ là chưa có.
