# Prompt nghiên cứu sâu — UAV tiny-object perception

Ngày thiết kế: 13/10/2026. Prompt này cụ thể hóa yêu cầu người dùng; không phải bản chép suy luận nội bộ. Mục đích là buộc đầu ra kiểm chứng được, thay vì chỉ làm câu lệnh dài hơn.

## 1. Nhiệm vụ và phạm vi

Đóng vai nhóm nghiên cứu computer vision gồm người kiểm chứng bằng chứng, người tổng hợp cơ chế và người phản biện độc lập. Nghiên cứu **vật thể rất nhỏ được quan sát từ UAV**, ưu tiên phát hiện và định vị. Phân biệt rõ bài này với phát hiện chính chiếc drone bằng camera mặt đất.

Chỉ dùng định hướng #7 *Multi-scale Aerial Object Detection and Segmentation* làm điểm xuất phát. Không bị buộc giữ YOLO, OBB, STAL, dataset, timeline kỹ thuật hoặc phương án H1 của proposal cũ. Lượt hiện tại chỉ nghiên cứu sâu; người dùng đã xác nhận chưa muốn viết code thí nghiệm. Bỏ chi phí tính toán khỏi lọc ý tưởng; không tự mua dịch vụ hay chạy GPU.

Trả lời trực tiếp: multi-view có cần cho câu hỏi cụ thể không? Tách single-image, single-camera video, multi-camera một UAV, nhiều UAV hợp tác, multi-scale crop và augmentation. Không đặt multi-view như điều kiện để đề tài có giá trị. Không mặc định mọi fusion đều cần calibration chính xác: nêu giả định của từng phương pháp.

## 2. Câu hỏi dẫn đường

Đối với một lỗi quan sát được, hãy phân biệt ít nhất hai giải thích:

- Không còn đủ tín hiệu trong ảnh hay preprocessing/mô hình làm mất tín hiệu đang có?
- Kích thước vật thể ở ảnh gốc, sau resize, trong feature map và ngoài thế giới khác nhau thế nào?
- High-resolution features giúp nhờ chi tiết, thay assignment, thay loss balance hay thêm supervision?
- Localization kém vì loss/representation, annotation ambiguity hay metric quá nhạy với một pixel?
- Vật thể dày bị mất trong nhận biết, gán mẫu, ranking, NMS, crop merge hay detection cap?
- Thông tin temporal/multi-view có thật sự bổ sung quan sát, hay chỉ thêm compute, ensemble hoặc một view tốt hơn?
- Mô hình theo dõi đúng identity hay chỉ giữ box cũ? Chất lượng output tại thời điểm xuất kết quả khác chất lượng frame gốc thế nào?
- Mask quality được đo sau một box/prompt hoàn hảo hay trong pipeline tự tìm mọi vật thể?
- Confidence nói về lớp, hình học, ambiguity, miền lạ hay utility của hành động? Quyết định nào thực sự thay đổi nhờ confidence đó?
- Kết quả thay đổi bởi kiến trúc hay nhãn, teacher, pretraining, nguồn ảnh và protocol?

Không trả lời mười câu bằng mười module. Hãy tìm các cơ chế nền giải thích được nhiều hiện tượng cùng lúc.

## 3. Hợp đồng bằng chứng

Gán một trong các nhãn cho mỗi nhận định quan trọng:

- **[nguồn]**: tác giả/nguồn sơ cấp nói hoặc đo điều này. Ghi URL, phiên bản/ngày, section/table/page, điều kiện.
- **[suy ra]**: suy luận từ giả định/định nghĩa được trình bày. Với công thức, trình bày phép suy ra ngắn và kiểm tra trường hợp biên/đơn vị.
- **[giả thuyết]**: đề xuất cần thực nghiệm, có giải thích cạnh tranh và kết quả có thể bác.
- **[chưa biết]**: nguồn chưa đọc, thiếu chi tiết hoặc có xung đột chưa giải được.

Không biến abstract thành full-method audit. Không lấy kết quả search snippet làm kiểm chứng toàn bộ bảng. Khi chỉ đọc đoạn chọn lọc, nói rõ phần đã đọc và chưa đọc. Một paper được chấp nhận không miễn kiểm tra công thức/protocol. Sai ở một phương trình không tự làm sai toàn bộ kết quả thực nghiệm.

Không tuyên bố “chưa ai làm”, “đầu tiên”, “SOTA”, “đủ Q1/Q2” hay gain dự kiến khi chưa có bằng chứng tương ứng. “Không thấy trong tập bài đang đọc” phải giữ đúng nghĩa đó.

## 4. Chiến lược đọc

1. Dùng corpus và notes hiện có làm seed. Đừng tìm lại đủ 50 bài chỉ để đạt số lượng.
2. Chọn các bài trực tiếp kiểm tra cơ chế cạnh tranh; có cả baseline, diagnostic/benchmark và phương pháp mới. Giữ một nguồn có thể bác ý tưởng ưa thích.
3. Đọc method, experimental protocol, bảng so sánh, ablation và limitations. Mở supplement khi claim phụ thuộc nó; nếu chưa mở, ghi giới hạn.
4. Kiểm repo chính thức khi cần giải quyết mâu thuẫn implementation. Repo tồn tại không có nghĩa checkpoint tải được, môi trường chạy được hoặc kết quả đã tái lập.
5. Chỉ tìm thêm nguồn khi nó có thể thay đổi câu trả lời hoặc đóng một lỗ hổng cụ thể. Giữ log tìm theo vấn đề; phân biệt nguồn UAV trực tiếp với satellite/ground-view/3D chuyển giao.

## 5. Thẻ case study bắt buộc

Mỗi case cần có:

1. Task/input/output, đơn vị mẫu và điều kiện thông tin được phép.
2. Vấn đề trung tâm và giả định giúp phương pháp hoạt động.
3. Chuỗi cơ chế từ input tới decision; không chỉ kể tên module.
4. Bằng chứng số liệu được chọn lọc. Mỗi số phải có metric, dataset/split, detector/backbone/config và comparator đúng.
5. Ablation cô lập trực tiếp điều gì, không cô lập điều gì. Hai dòng đổi nhiều thành phần không chứng minh riêng một thành phần.
6. Hạn chế tác giả nêu, hạn chế do người đọc suy ra và điều chưa đọc — ghi riêng.
7. Giải thích cạnh tranh mạnh nhất cho gain.
8. Kiến thức nền có thể chuyển sang UAV tiny; điều kiện khiến chuyển giao thất bại.
9. Phép thử phân biệt tối thiểu và kết quả bác giả thuyết trung tâm.
10. Trạng thái tái lập: environment/data/train/evaluator/ablation/code; không đánh dấu đủ chỉ từ một link GitHub.

Khi prose và table không khớp, bảo toàn cả hai, tính chênh lệch từ đúng hàng và gọi đó là xung đột/khác baseline. Không âm thầm chọn con số thuận câu chuyện. Không so AP50 với AP50:95, HBB với OBB, 2D với BEV/3D, prompted IoU với automatic mask AP, offline với streaming, simulated với thực như cùng một benchmark.

## 6. Kiểm tra nền tảng và toán

Các công thức cần phân biệt biến và miền áp dụng. Với gradient, xác định đạo hàm theo probability, logits, feature hay toàn bộ parameters; dùng chain rule đúng. Bounded gradient theo logits không tự chứng minh mọi gradient trong backbone bị chặn. Uncertainty giảm không tự chứng minh calibration tốt.

Các ví dụ giáo khoa phải gắn nhãn minh họa/suy ra; không trình bày như thí nghiệm dataset. Kiểm tra trường hợp uniform/zero/identity hoặc số nhỏ khi thích hợp. Không đặt một “giới hạn vật lý 11 px/16 px” chỉ từ rule assignment hoặc một benchmark.

## 7. Cổng multi-view

Chỉ nâng multi-view thành nhánh chính khi nêu được:

- Lỗi single-view nào cần quan sát bổ sung: occlusion, viewpoint ambiguity, coverage hoặc depth/3D.
- Vì sao temporal/single-view tốt hơn, full-resolution hoặc chọn một view tốt nhất chưa đủ giải thích lợi ích.
- Đầu ra muốn tối ưu: box trên ego image, scene/world frame, BEV hay 3D.
- Loại view, mức đồng bộ/pose/correspondence phương pháp cần và cách kiểm tolerance với sai lệch.
- Tập dữ liệu có nhãn và geometry phù hợp; tiny strata được đo trực tiếp nếu claim tiny.
- Metric cuối khớp ứng dụng và các tình huống mất camera/message hoặc view không bổ sung thông tin.

Không yêu cầu mọi nhánh phải có 3D labels hoặc known extrinsics; yêu cầu cụ thể phải xuất phát từ formulation đã chọn. Cũng không biến việc bỏ ngân sách tiền thành bỏ qua latency, bandwidth hoặc synchronization khi chúng là phần định nghĩa bài toán.

## 8. Tự phản biện có đối thủ cụ thể

Reviewer phải thử bác các claim trung tâm bằng: đối chứng mạnh đơn giản; thêm supervision/compute; sai đơn vị/metric; leakage scene/sequence; ưu thế một view; future-frame access; calibration/ranking khác nhau; cap/NMS/evaluator; nguồn nhãn không độc lập; hoặc prior gần hơn đã có.

Phân biệt **bác cơ chế**, **bác tính mới**, **bác nhu cầu module** và **bác hiệu quả triển khai**. Một kết quả sửa nhãn làm mất gain kiến trúc có thể ủng hộ giả thuyết nhãn là nút thắt. Không dùng p>0.05 như chứng minh tương đương; cần precision và biên thực dụng khóa trước.

Viết H0 khoa học khớp prediction/contrast của từng hypothesis riêng với điều kiện không cần module. “Baseline đơn giản đã đủ” có thể đúng đồng thời với giả thuyết khoa học; không dùng nó làm H0 thay cho claim về cơ chế. Chọn endpoint, effect/interaction, strata và biên thực dụng trước xác nhận. Dùng source IDs nhất quán xuyên corpus; nguồn mới cần namespace không đè mã cũ.

Không tự coi kết luận của ba agent là ba thí nghiệm độc lập. Review độc lập làm giảm lỗi đọc/suy luận, không tạo bằng chứng thực nghiệm mới.

## 9. Đầu ra mong muốn

- Một quyết định scope rõ: trọng tâm UAV tiny, vai trò multi-scale/temporal/multi-view và đầu ra còn cần chốt.
- Khoảng 6–8 nguyên lý nền giải thích được các case, có nguồn và giới hạn.
- Casebook đọc sâu có nguồn theo bảng/section, không phải catalogue abstract.
- Tối đa 3 giả thuyết giải pháp cạnh tranh sau tổng hợp; mỗi giả thuyết có prior, prediction, null, control, endpoint và điều kiện dừng.
- Một bảng “biết chắc từ nguồn / suy luận có điều kiện / cần kiểm nghiệm”.
- Danh sách phát hiện sau phản biện và câu đã sửa.
- Những câu hỏi còn mở và lượng đọc thực tế; tuyệt đối không bù chỗ trống bằng một kiến trúc được đặt tên cho đẹp.

Định nghĩa hoàn tất lượt nghiên cứu: người đọc hiểu cần đo gì để chọn hoặc loại một hướng, hiểu vì sao multi-view cần hoặc chưa cần, và có thể truy ngược các kết luận trung tâm tới nguồn. Không cần có mô hình mới hoặc hứa mức tăng điểm để coi lượt đọc sâu là hữu ích.
