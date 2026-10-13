# Kế hoạch thử nghiệm 28 ngày — T07 fresh research

Ngày lập 13/10/2026. Đây là protocol đề xuất [design], **chưa có run GPU**, chưa xác minh detector/checkpoint/dataset chạy end-to-end. Tài liệu không thay đổi ROADMAP lịch sử. Khung mới: 13/10–09/11/2026.

## 1. Câu hỏi và điều kiện bắt đầu

RQ1: Khi giữ detector, checkpoint và hậu xử lý cố định, vùng ảnh nào được lợi hoặc chịu hại nếu được xử lý ở mức chi tiết hơn?

RQ2: Sau khi đã có density/heatmap và predicted gain, độ tin cậy của dự đoán lợi ích có thêm giá trị cho quyết định phân bổ tài nguyên không?

RQ3: Cơ chế có giữ được lợi ích trên cảnh giữ lại và điều kiện scale/blur khác calibration split không?

Các RQ là thiết kế. RQ2 **không mặc định mới**: phải đọc kỹ R13 Dynamic Zoom-in, R14 Remix, F04 DenseScout, F05 AFWD-Net, F06 Visual Accommodation và các nguồn uncertainty trong REPORT trước khi gắn novelty.

G0 chỉ qua khi có: data đúng phiên bản và quyền sử dụng; ảnh gốc/nhãn/split manifest; checkpoint tải được và checksum; một lượt inference hợp lệ; evaluator qua kiểm tra hình học; thời gian/VRAM thực đo. Nếu thiếu, ghi NOT READY, không lên lịch hàng chục run tưởng tượng.

## 2. Chọn một track

| Track | Dữ liệu pilot | Backend ứng viên | Dependency chưa xác minh | Fallback |
|---|---|---|---|---|
| OBB ưu tiên | DOTA-v1.0, sau đó tiny-OBB hoặc miền độc lập đã audit | Oriented R-CNN nhỏ/ResNet-50 hoặc checkpoint OBB nhẹ có recipe tái lập | Checkpoint, stack CUDA/MMCV, latency, label conversion | Chọn OBB stack đã chạy ổn; không đổi backend giữa các selector |
| HBB nếu tooling OBB chặn quá 2 ngày | VisDrone DET | Detector nhẹ với pretrained checkpoint; SAHI/heatmap làm đối chứng | Dataset mirror, checkpoint, preprocessing | HBB-only claim; bỏ kết luận về góc |
| Segmentation | iSAID | Mask R-CNN/RS-SAM | Bộ nhãn mask, prompt protocol, tài nguyên | Chỉ triển khai nếu H1/H2 đã bị loại và nhóm chấp nhận đổi câu hỏi |

Không train cả ba track trong bốn tuần. Không có “baseline number đáng tin” của nhóm ở thời điểm lập plan. Số trong paper chỉ là tham chiếu; đối chứng chính phải là internal reproduction cùng protocol.

## 3. Split và dữ liệu

Chọn nguyên ảnh/cảnh gốc trước khi crop. Mỗi record lưu source_dataset, version, original_image_id, scene_group_id, split, width/height, annotation hash, image hash, class map và GSD nếu có. GSD thiếu phải để thiếu; không suy GSD từ số pixel.

Tách phần train detector, train selector và calibration/tuning theo cảnh. Có thể chia tập train thành các phần nhỏ hoặc dùng cross-fitting nếu đủ tài nguyên; không dùng official validation labels để huấn luyện selector rồi báo AP trên cùng tập. Official val chỉ dùng theo vai trò đã khóa; nếu cần tuning ở val thì tách một calibration subset và báo rõ phần held-out còn lại. Official test chỉ mở ở cuối.

DOTA các phiên bản và iSAID có ảnh chung; khóa group theo nguồn ảnh, không theo tên file crop. Dataset thứ hai cũng cần audit trùng nguồn; tên khác không đủ đảm bảo độc lập. DOTA cho phép GSD=None; không áp một bài toán cần native GSD lên toàn bộ ảnh nếu không có metadata. [DOTA](https://captain-whu.github.io/DOTA/dataset.html), [iSAID](https://captain-whu.github.io/iSAID/dataset.html).

Pilot dùng một số cảnh được lấy theo quy tắc có seed và đủ phủ size/density/class. Không chọn riêng cảnh “trông có lợi cho crop”. Kết quả subset chỉ gọi pilot, không báo như kết quả full benchmark.

## 4. Phân biệt ba thao tác resolution

- **Crop từ ảnh gốc rồi đưa vào detector:** có thể giữ lại chi tiết mà full-image resize bỏ mất.
- **Upsample cùng một ảnh đã thấp phân giải:** không bổ sung phép đo ảnh gốc; có thể thay đổi đáp ứng của mạng.
- **Giảm phân giải có kiểm soát:** là stress test tổng hợp; không tự đại diện cho khác sensor/GSD ngoài thực tế.

Mỗi thí nghiệm ghi rõ đang làm thao tác nào. S07 Scale-MAE và R04 SAHI là nguồn cơ chế tham khảo; phân biệt trên là cách kiểm soát thí nghiệm [design], không phải định lý về mọi detector.

## 5. Các arms tối thiểu

Cùng detector, checkpoint, input normalization, class map, candidate pool, merge/evaluator và phần ảnh được phép nhìn. Không dùng tên A0/A1 từ proposal cũ.

| Arm | Mục đích |
|---|---|
| P0: full-image coarse | Mốc accuracy/latency |
| P1: uniform tiling / fixed SAHI-style | Đối chứng “chỉ tăng chi tiết đã đủ” |
| P2: random hoặc grid selection cùng budget | Đối chứng lợi ích từ chọn vùng |
| P3: density/heatmap top-K | Đối chứng selector đơn giản nhưng mạnh |
| P4: gain-only selector | Đối chứng trực tiếp chống novelty giả của H1 |
| P5: gain + reliability/risk-aware | Can thiệp đề xuất |
| O: oracle lựa chọn dùng GT | Chẩn đoán headroom chỉ; không xếp như phương pháp deployable |

Nếu chỉ đủ tài nguyên cho bốn arms, giữ P0/P1/P3/P4 trước; chưa có quyền kết luận P5. Không bỏ đối chứng khó để giữ module mới.

DenseScout đã cho thấy raw heatmap có thể là baseline mạnh và có closure với backend chung; đọc full text §4.2, supplement §2.7 trước khi cài. Dynamic Zoom-in đã dùng predicted accuracy gain. Bản cài rút gọn phải ghi **proxy implementation**, không nhận là tái lập tác giả. [F04](https://arxiv.org/abs/2604.25300), [R13](https://arxiv.org/abs/1711.05187).

## 6. Nhãn lợi ích và predictor nhỏ

Trên split dành cho selector, chạy cùng detector ở coarse và các crop/scale cho phép. Cố định matching class + rotated IoU, ghi các thay đổi TP/FP/localization sau merge. Lưu cả negative gain; không chỉ học trên ví dụ zoom thành công.

AP là metric tổng hợp phụ thuộc ranking, matching và toàn bộ tập. Một utility cộng theo patch chỉ là surrogate [design], không gắn nhãn “AP marginal” nếu chưa chứng minh tương đương. Đánh giá cuối vẫn phải recompute AP toàn ảnh/tập.

Bắt đầu predictor từ feature cache: confidence thống kê, scale/shape dự đoán, texture/detail proxy và coarse features. Không đưa kích thước GT, số GT hoặc góc GT vào input inference. So MLP với mô hình cây đơn giản để biết cần học biểu diễn mới hay chỉ cần calibration.

Reliability phải có định nghĩa kiểm tra được: ví dụ xác suất utility dương hoặc interval của utility, calibration trên split riêng, đánh giá Brier/reliability curve hoặc coverage khi phù hợp. Covariance shape từ GauCho không tự dùng làm uncertainty. Chưa có đảm bảo thống kê dưới distribution shift; nếu muốn claim coverage guarantee cần chứng minh giả định và nguồn phương pháp riêng.

Các input, loss và threshold chỉ chốt sau pilot và ghi timestamp trước run xác nhận. Không vừa thấy test result vừa thay utility.

## 7. Metric, fairness và thống kê

**Metric khoa học chính [design]:** rotated AP75 tại một budget end-to-end đã khóa từ profiling. Báo song song metric chuẩn dataset (thường AP50 ở DOTA), các IoU khác nếu evaluator hỗ trợ, recall và AP theo size/aspect/density. Không đổi metric chuẩn để làm bài “đẹp hơn”.

Budget chính chọn từ mức chi phí có ít nhất hai phương án thực thi được. Dùng một budget chính và hai budget phụ để vẽ frontier. Không đặt 40 ms hoặc số crop trước khi biết hardware. So cả equal-pixel, equal-call và equal-wall-time khi có thể; ba điều kiện này không tương đương.

Latency gồm preprocessing, selector, crop/copy, detector, map coordinates, merge. Báo hardware/software/precision/batch, warmup và median/p95; tách thời gian tải dataset khỏi inference nhưng tính vào chi phí tiền nếu bị tính phí. Không đối chiếu FPS của paper ở GPU khác như cùng một benchmark.

Báo max detections và kiểm tra saturation. Không kế thừa max_det=12000 của proposal cũ khi chưa có lý do từ dataset/implementation mới. Capacity, score threshold và NMS không thay đổi giữa selector nếu claim chỉ về chọn crop.

Đơn vị bootstrap là cảnh/ảnh gốc, không crop hay từng box như các quan sát độc lập. Resample cùng danh sách scene cho cặp mô hình rồi **tính lại AP trên dự đoán gộp**, không trung bình “AP từng ảnh”. Nếu chỉ có image_id mà không có true scene groups, nói rõ đó là proxy còn nguy cơ phụ thuộc.

Ba seed cho predictor là mục tiêu xác nhận [design]; nếu detector giữ nguyên thì đây không đo biến thiên do train detector. Muốn claim tổng quát qua training seed cần tái train detector tương ứng. Không nhân số crop để tạo cỡ mẫu giả. Chỉ một contrast chính P5–P4; các so sánh khác là chẩn đoán hoặc exploratory.

## 8. Kill tests và cổng

- **K1, ngày 16/10:** nếu crop chi tiết không cải thiện định vị ở nhóm vấn đề, H1 thiếu headroom.
- **K2, ngày 19/10:** nếu predicted gain không hơn density/heatmap ngoài split học, không thêm uncertainty để che lỗi.
- **K3, ngày 23/10:** nếu phần reliability không thêm lợi ích ngoài gain-only, H1 như mô tả bị bác; bỏ module hoặc chuyển câu hỏi.
- **K4, ngày 26/10:** nếu lợi ích mất sau khi khớp latency/merge/checkpoint, không claim phương pháp hiệu quả.
- **K5, ngày 02/11:** nếu chỉ có lợi ở scene/scale được chọn sau, thu hẹp claim; chưa có căn cứ cross-domain.
- **K6, ngày 09/11:** nếu chưa có reproducible results và đối thủ gần, đầu ra là pilot/negative result và kế hoạch tiếp, không gọi submission-ready.

Mức cải thiện hữu ích cần đăng ký sau đo nhiễu baseline và trước xác nhận. Có thể lấy 0.5 điểm AP75 làm **ví dụ ngưỡng kỹ thuật để thảo luận**, nhưng không xem đó là tiêu chuẩn Q2/Q1 và không tự kết luận đủ với CI vừa loại 0. Báo cả effect size và CI.

## 9. Ngân sách

Giá tham chiếu từ [Modal pricing](https://modal.com/pricing), kiểm tra 13/10/2026; thay đổi được theo thời gian. Ví dụ dưới đây gồm GPU + **2 physical CPU cores và 16 GiB RAM**. Chưa tính mọi khoản storage/network/thuế; không tính free credits chưa xác nhận vào ngân sách.

| GPU | GPU USD/giờ | Cộng CPU/RAM USD/giờ | 45 USD mua được khoảng |
|---|---:|---:|---:|
| T4 | 0.5904 | 0.812592 | 55.4 giờ |
| L4 | 0.7992 | 1.021392 | 44.1 giờ |
| A10 | 1.1016 | 1.323792 | 34.0 giờ |
| A100 40GB | 2.0988 | 2.320992 | 19.4 giờ |

[derived, phép đổi đơn vị] Giá giờ = 3600 × (giá GPU/giây + 2 × giá CPU core/giây + 16 × giá GiB/giây). Giá CPU là 0.0000131/core/giây, RAM 0.00000222/GiB/giây. Kiểm tra: 1 giờ = 3600 giây; budget/giá giờ cho số giờ. Đó là thời gian thuê, **không phải ước tính đủ số run**.

Kaggle công bố quota GPU theo tuần, tài liệu hiện nêu 30 giờ hoặc cao hơn tùy nguồn lực. Lấy quota thực trong tài khoản làm đầu vào; không bảo đảm bốn tuần đều có đủ 30 giờ hoặc cùng GPU. [Kaggle GPU usage](https://www.kaggle.com/docs/efficient-gpu-usage).

| Phong bì chi [design] | Trần USD | Dùng cho |
|---|---:|---|
| Pilot/profiling | 5 | Setup, kiểm tra data/checkpoint, đo throughput |
| Đối chứng/gain labels | 15 | Coarse/fine inference cache và selector |
| Xác nhận | 20 | Repeat quan trọng, held-out, can thiệp duy nhất |
| Packaging/last checks | 5 | Lần đánh giá cuối cần thiết |
| Dự phòng | 15 | Chỉ dùng khi đã có bằng chứng cần chạy tiếp |
| Tổng | 60 | Không tự tăng |

Dùng GPU cho inference/training cần thiết; tiền xử lý/lập bảng thực hiện CPU khi hợp lý. Checkpoint định kỳ và resume, lưu log chi phí theo job. Không giả định Kaggle miễn phí đồng nghĩa công sức debug miễn phí.

Trước chạy dài: warmup rồi đo số bước/giây, VRAM và thời gian validation. Dự toán từng job từ số bước, số validation và hệ số dự phòng 1.25 [design]. Chỉ xếp batch job nếu tổng chi dự kiến nằm trong phong bì còn lại; dừng phát sinh job mới khi chạm trần.

Chọn GPU bằng **USD để hoàn thành cùng job**, không theo USD/giờ đơn lẻ. Ước tính hiện chưa có cơ sở throughput; con số cụ thể sẽ chỉ xuất hiện sau pilot.

## 10. Run manifest bắt buộc

Mỗi run lưu: run_id, hypothesis, arm, data/split hash, code commit, environment lock, checkpoint hash, seed, image scale/crop/overlap, preprocessing, score/NMS/max_det, evaluator version, trainable params, GPU/precision/batch, start/end, measured cost, config và predictions.

Artifacts cần có cuối tuần 1: smoke inference, overlay OBB, kiểm tra roundtrip rotation/coordinates, bản phân bố size/density, profile.csv và baseline-results.json. Cuối tuần 2: selected-patches.json cùng predictions coarse/fine và phân tích errors. Cuối tuần 3: frozen-config và paired CI. Cuối tuần 4: bảng chính, failure gallery, limitations và reproduction commands.

Đây là tiêu chí thực hiện bước nghiên cứu thực nghiệm tiếp theo. Lượt hiện tại chưa tạo các artifact run này và chưa tiêu ngân sách GPU.
