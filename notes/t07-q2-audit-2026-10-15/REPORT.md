# #7 — Phản biện nền tảng và các đề tài có thể hướng tới Q2

Ngày 15/10/2026 · Research-only · Tổng hợp admin, hai Sol/high và một Astra/high.

**Nhận định:** ba note 14–15/10 mở rộng được prior và câu hỏi, nhưng chưa đủ căn cứ để kết luận “muốn Q2 phải đổi sang head góc”, “thiếu ba dataset thì trần Q3”, hoặc “chỉ còn conditioning theo pixel là mới”. Có thể giữ hướng assignment và hướng độ tin cậy hình học làm hai chương trình cạnh tranh. Ưu tiên nghiên cứu tiếp độ tin cậy hình học vì nó nối được quan sát, nhãn và quyết định của detector; đây là lựa chọn điều tra, chưa phải xác nhận novelty hay dự báo nhận bài.

## 1. Đã đọc gì và điều gì có thể tin

Đã đối chiếu ba note mới, ledger C-13–18, proposal với hộp v2.2, tier-upgrade, INDEX và các phần liên quan của deep-study trước. Hai Sol đọc thêm phần method/experiment của AQE và O2-DETR; data/method của AI-TOD-R, CODrone, DroneVehicle và CSCWD. Astra kiểm toán lập luận và snapshot TAL. Độ sâu, phiên bản, locator và giới hạn nằm trong [ANGLE-PRIOR](ANGLE-PRIOR.md), [DATA-AND-TRANSFER](DATA-AND-TRANSFER.md), [LOGIC-CRITIQUE](LOGIC-CRITIQUE.md).

Không coi 50 record cũ là 50 bài đã đọc toàn văn: corpus gốc ghi 39 abstract/metadata, 10 trích đoạn toàn văn chọn lọc và một publisher excerpt. Không coi khoảng 45 nguồn chọn thêm là 45 phương pháp đã được audit. Cache scan1015 được sao lưu và đối chiếu SHA256; manifest ghi 174 ID arXiv duy nhất trong kết quả trả về, **không phải** 174 bài liên quan mới. Số khoảng 45 là kết quả chọn lọc của phiên trước, chưa tái dựng bằng một bảng selection đầy đủ.

Các việc đáng giữ từ phiên 14–15/10:

- OSCAR khiến claim “tăng sàn vùng ứng viên là mới” không đứng được; MCSA là đối thủ cần đọc theo cơ chế, không chỉ theo tên.
- Tám giả thuyết cạnh tranh tốt hơn chọn ngay một head rồi tìm tài liệu ủng hộ.
- AI-TOD-v2/R là tài sản đối chiếu trên chung bộ ảnh; giá trị của nó nằm ở kiểm soát ảnh và truy nguồn nhãn.
- Phân biệt abstract với toàn văn và để mở khả năng dữ liệu chưa sẵn sàng là đúng.

Tên “hướng A” đang bị dùng hai nghĩa: note 14/10 chỉ STAL/coverage C-16; deep-study 13/10 chỉ scale/learning attribution. Báo cáo này dùng tên cơ chế, không nhập hai hướng làm một.

## 2. Những kết luận cần sửa trước khi phát triển đề tài

| Kết luận cũ | Kết luận sau kiểm chứng | Ý nghĩa nghiên cứu |
|---|---|---|
| Assignment/loss chỉ T1 nên không thể Q2 | Loại can thiệp không xác định quartile. ATSS là một ví dụ assignment được công bố CVPR; không chứng minh STAL hiện tại có cùng giá trị. | Đánh giá insight, prior và bằng chứng, không bắt buộc thêm module. |
| Phải có ≥3 nguồn dataset mới vượt Q3 | Đây không phải quy tắc editorial đã được chứng minh. Độ rộng bằng chứng phải phù hợp claim. | Hai tên dataset chưa chắc độc lập; thêm HBB chưa tái lập claim góc OBB. |
| Sàn √2s phải dự đoán AP tối ưu | Hình chữ nhật đóng có cạnh ngắn ≥√2s chứa một điểm trên lưới vuông vô hạn bước s, theo mọi vị trí/góc. | Đo cả top-k, conflict và trọng số; optimum AP khác cận không bác định lý. |
| Cùng diện tích ⇒ hiệu ứng shape chỉ bậc hai | Cùng diện tích cho cùng kỳ vọng N dưới pha đều, không cho cùng xác suất rỗng. | Square s×s: P(N=0)=0; rectangle 2s×s/2: P(N=0)=1/2, cùng E[N]=1. Đây là phản ví dụ giải tích, không phải kết quả dataset. |
| arctan(2δ/L) là giới hạn không thể vượt của sai số góc | Đây là cận trên sensitivity với endpoint chỉ nhiễu vuông góc. Nhiễu Euclid 2D cho asin(2δ/L) khi 2δ<L. | Cả hai đều chưa là cận dưới lỗi, expected loss hoặc giới hạn thông tin ảnh. |
| O2-DETR không phụ thuộc kích thước | ADR Eq.1–2 nhân với Wr/Hr; OCD cũng dùng kích thước. Chưa thấy gate theo độ tin cậy ở số pixel tuyệt đối trong phần đọc. | Phải phân biệt chuẩn hóa hình học, features mang scale và reliability gate. |
| HBB-envelope discrepancy đo nhiễu nhãn | Đây là inconsistency giữa biểu diễn; có thể do convention, matching, thêm/bỏ instance hoặc sửa nhãn hợp lệ. | Cần audit độc lập trước khi gọi noise. Agreement cao cũng không chứng minh sạch. |
| A8 đủ candidate nhưng recall thấp ⇒ feature yếu | Có thể còn lỗi assignment, regression, nhãn, ranking, postprocess hoặc evaluator. | Cần can thiệp có đối chứng; một chỉ số không nhận dạng nguyên nhân. |
| CSCWD là đối thủ trực tiếp tiny UAV-view OBB | Bài phát hiện drone trên Drone-vs-Bird/DUT-Anti-UAV; cơ chế transfer đáng thử nhưng khác task. | Không chuyển nguyên gain hoặc kết luận của bài sang #7. |

Chi tiết toán và biên: [LOGIC-CRITIQUE §1–7](LOGIC-CRITIQUE.md). Snapshot OBB dùng ≥/≤; HBB dùng >eps. Không cáo buộc OBB snapshot dùng strict. Lưới hữu hạn, dtype và tọa độ ở biên ảnh vẫn cần xác nhận khi triển khai.

**Cơ sở venue:** [JCR basics](https://clarivate.libguides.com/jcr/basics) mô tả quartile theo xếp hạng journal trong category; không phải cấp phương pháp của từng bài. [CVPR 2026 reviewer guidelines](https://cvpr.thecvf.com/Conferences/2026/ReviewerGuidelines) đánh giá technical soundness, novelty và impact; không coi số dataset nhiều hay SOTA là điều kiện đủ. [TGRS scope](https://www.grss-ieee.org/publications/transactions-on-geoscience-remote-sensing/) yêu cầu tiến bộ phương pháp và dữ liệu/thực nghiệm được mô tả đầy đủ. Đây không phải bằng chứng TGRS thuộc Q2, cũng không phải chính sách chung của mọi journal. [ATSS accepted record](https://openaccess.thecvf.com/content_CVPR_2020/html/Zhang_Bridging_the_Gap_Between_Anchor-Based_and_Anchor-Free_Detection_via_Adaptive_CVPR_2020_paper.html) chỉ được dùng làm phản ví dụ cho việc tự động đánh thấp mọi cải tiến assignment; lượt này không audit toàn văn ATSS.

## 3. Ba đề tài ứng viên, kèm cách tự bác

**Câu hỏi trước khi ưu tiên OBB:** ứng dụng cần trục hộp/góc để làm gì — định vị footprint, phân biệt vật sát nhau, heading hay chỉ đếm/phát hiện? #7 không bắt buộc OBB. Nếu không chứng minh được giá trị của target góc cho task đã chọn, ưu tiên R2/R3 hoặc so HBB/OBB như hai target khác nhau; không ép bài toán góc chỉ để có head mới. So HBB/OBB cũng phải giữ rõ evaluator, nhãn và tập instance khác nhau.

### R1 — Khi nào nên tin góc của vật tí hon trong ảnh trên không?

**Tên làm việc:** *Resolution- and Annotation-Aware Geometric Reliability for Tiny Aerial Object Detection*. “Aware” là mục tiêu nghiên cứu, chưa phải tên một phương pháp đã hoàn thiện.

**Câu hỏi chính:** chất lượng quan sát và độ bất đồng nhãn có dự báo lỗi hình học ngoài ảnh hưởng của kích thước/aspect ratio không; detector có dùng được thông tin đó để ra quyết định tốt hơn không?

**Đã có:** AQE dự đoán mean/std, angle quality NMS và loss theo aspect ratio; O2-DETR dùng distributional refinement có scale hình học; GauCho là prior biểu diễn Gaussian. Vì vậy “thêm uncertainty head + gate” chưa đủ khác biệt. [AQE Methods/Tables1–2](https://www.nature.com/articles/s41598-025-31034-w), [O2-DETR IV-B/IV-D, VII–X](https://arxiv.org/html/2603.15497v1); GauCho được đọc trong casebook trước, không đọc lại toàn văn ở lượt này.

**Giả thuyết có giá trị nếu đúng:** sau khi khống chế hình dạng, scene và nhãn, một đại lượng chất lượng quan sát đo được vẫn dự báo rủi ro góc trên cảnh mới; hành động dựa trên dự báo đó cải thiện detector dưới metric OBB gốc. Không gọi nó physical identifiability nếu chưa có mô hình tạo ảnh tương ứng.

**Bằng chứng cần thiết, chưa thực hiện:**

1. Định nghĩa target: góc OBB/trục hình học hay semantic heading? Chốt periodicity, hoán vị w/h và đối xứng. Đánh giá góc gần vuông phải nói rõ convention.
2. Audit nhãn độc lập trên subset phân tầng size/aspect/class/density/blur. Annotator không nhìn output phương pháp hoặc gate. Disagreement là dữ liệu về annotation; đồng thuận không tự là ground truth.
3. Can thiệp resolution/blur trên cùng ảnh có reference, tách khỏi native-scene validation. Theo dõi native pixel support và toàn bộ resize/crop. Upsample không bổ sung phép đo, nên gate chỉ dựa vào pixel sau resize có thể bị đánh lừa.
4. So baseline trực tiếp, shape-only, size-only loss, AQE-style quality, distributional refinement và label-cleaning controls. Khớp detector/recipe cho ablation cơ chế; benchmark toàn hệ khác detector báo riêng.
5. Đo AP/recall OBB tiêu chuẩn, misses, lỗi tâm/cạnh/góc và calibration theo scene/size. Với confidence score, định nghĩa sự kiện như “angle error dưới tolerance” rồi kiểm reliability; chỉ kiểm interval coverage khi thật sự có predictive interval. Fit calibration và chọn tolerance trên validation, không test.
6. Kiểm utility của hành động: reweight, decoder, hoặc refinement. Risk–coverage riêng có thể đẹp vì loại vật khó; luôn báo AP/recall trên tất cả GT theo protocol cố định. Không đổi sang metric bất biến quay để làm mất lỗi mà benchmark yêu cầu.

**Quy tắc dừng/hạ claim:** size-only hoặc cleaning đạt tương đương trong biên hữu ích định trước thì chưa có cơ sở thêm head. Nếu calibration thất bại, chỉ giữ claim score dùng cho ranking khi usefulness và transfer của ranking được kiểm độc lập; transfer thất bại không được cứu bằng đổi tên uncertainty thành score. Nếu size effect biến mất sau controls, bỏ claim cơ chế độc lập theo size. Không có “điểm gãy” không tự bác mọi liên hệ scale.

**Vì sao ưu tiên điều tra [nhận định]:** R1 đặt một câu hỏi nối dữ liệu với hành động, có phép bác rõ và prior đủ sát để tránh thắng đối chứng yếu. Rủi ro lớn nhất là uncertainty chỉ lặp lại AQE hoặc học proxy size; chưa xác lập novelty toàn lĩnh vực.

### R2 — Có candidate rồi, vì sao vật tí hon vẫn không nhận giám sát hữu ích?

**Tên làm việc:** *From Candidate Coverage to Effective Supervision in Dense Tiny Oriented Detection*.

**Câu hỏi chính:** mất GT xảy ra trước hay sau chọn ứng viên, và quan hệ đó thay đổi thế nào theo mật độ/shape/stride? Đây là cách nâng câu hỏi C-16 về cơ chế, không phải chỉ quét ngưỡng rồi đặt tên module.

**Đã có:** OSCAR quét pseudo-box floor, MCSA thay đổi assignment và kiến trúc, STAL/shape-aware assignment đã có nhiều prior. Các đọc này kế thừa note 14/10; chưa tái lập code/điểm số ở lượt audit. √2s là control hình học hữu ích, không tự tạo novelty.

**Thiết kế quyết định:** ghi đường đi GT qua eligibility → candidate từng mức → top-k → conflict → loss-weight mass → detection trước/sau NMS/cap. So A0/A1/A2/A8 và equal-area shapes nhưng giữ phân phối N và zero-count như endpoint riêng. Kiểm tương tác floor × conflict policy ở cùng recipe; đối chứng thêm positives ngẫu nhiên/đơn giản cần hợp lệ theo assigner, không tự coi mọi positive là tốt.

**Chỉ mở phương pháp nếu:** có failure lặp lại sau coverage mà quy tắc đơn giản chưa xử lý được. Ví dụ phân bổ positives giữa GT cạnh tranh là một giả thuyết thiết kế, chưa được nhận là mới; cần quét prior adaptive assignment/capacity/dynamic matching trước.

**Cách bác:** nếu bookkeeping/evaluator giải thích hết, đó là sửa benchmark; nếu floor sweep và strong prior giải thích hết, không tuyên bố nguyên lý/phương pháp mới. Nếu không tìm được cơ chế ngoài đổi sàn thì vẫn có kết quả hữu ích nhưng chưa đủ bằng chứng cho một câu chuyện đóng góp mạnh.

### R3 — Zoom giúp vì thêm chi tiết, hay vì thay đổi cách học?

**Tên làm việc:** *Separating Observation Resolution from Training Effects in Tiny Aerial Detection*.

**Câu hỏi chính:** gain đến từ chi tiết native được giữ lại, scale vào mạng, teacher supervision hay recipe? Phân biệt bốn hành động: phóng ảnh nội suy, crop giữ chi tiết gốc, đầu đặc trưng độ phân giải cao, và bổ sung frame/view.

**Prior cần đối chiếu:** QueryDet, SuperYOLO, UGS trong deep-study; CSCWD là prior transfer khác task. QueryDet không tự tạo thông tin cảm biến; train-only SR có thể giúp học dù module bỏ khi suy luận. Không suy có SR module ⇒ phục hồi chi tiết thật.

**Thiết kế quyết định:** full image vs crop/tiling với native support được ghi; cùng resolution với loss/teacher controls; coverage fixed vs changed; direct high-resolution student vs distilled student; cùng evaluator và báo thông tin/compute của từng nhánh. Crop còn đổi context, field of view, vị trí vật trong khung và số lần quan sát chồng lấn; cần controls cho các yếu tố đó cùng quy tắc fusion/NMS trước khi quy gain cho chi tiết. Không loại nhánh vì chi phí, nhưng phải công khai sự khác nhau về tài nguyên để giải thích gain đúng.

**Cách bác:** nếu upsample/recipe control đạt tương đương, không gọi gain là khôi phục thông tin. Nếu teacher mạnh hơn hoặc nhận thêm dữ liệu, đó là alternative explanation cần tách. Cơ chế chuyển từ anti-UAV chưa được chứng minh trên UAV-view.

R3 là nhánh cạnh tranh và cũng có thể cung cấp phép thử quan sát cho R1. Không ghép R1+R2+R3 thành một “siêu kiến trúc” trước khi biết failure nào chi phối.

## 4. Dữ liệu: tài sản tốt nhưng chưa phải chứng cứ hoàn chỉnh

[AI-TOD-R §III](https://arxiv.org/html/2412.11582v1) mô tả cùng nền 28.036 ảnh AI-TOD-v2, OBB từ H2RBox-v2 rồi sửa/kiểm thủ công. Có paired representations ở mức thiết kế dataset; chưa xác minh archive, matching instance, split và hash. Hai bộ không phải hai phép đo góc độc lập, cũng không phải hai dataset độc lập để tăng số lượng benchmark.

CODrone/DroneVehicle mở thêm hướng kiểm tra ngoài AI-TOD-R, nhưng phần đã đọc chưa chốt tỷ lệ tiny theo bin phù hợp. CODrone v1 có bất nhất count và altitude; phải kiểm version/nhãn thay vì chọn con số thuận lợi. UAV-view cũng không đồng nghĩa mọi ảnh AI-TOD-R đều do UAV chụp: đây là bộ aerial tổng hợp nhiều nguồn. Nếu claim dành riêng UAV cần subset có provenance phù hợp hoặc dataset UAV xác nhận, và giới hạn claim khi provenance thiếu. [CODrone §III](https://arxiv.org/html/2504.20032v1), [DroneVehicle §III](https://arxiv.org/html/2003.02437v2).

Chung nguồn DOTA/DIOR/VisDrone tạo nhu cầu kiểm parent scene/crops; không tự chứng minh leakage. Leakage cần chỉ ra contamination trong train/test/teacher/adaptation/chọn hyperparameter của protocol cụ thể. Tên khác không bảo đảm độc lập, tên chung không tự làm một split hợp lệ thành vô dụng.

Multi-view chưa cần là điều kiện của đề tài. Chỉ mở khi câu hỏi là “quan sát thứ hai giảm ambiguity còn lại đến đâu” và có dữ liệu đồng bộ/association/calibration phù hợp phương pháp. Video/tracking cũng là task khác với static detection; thêm chúng lúc này làm rộng bằng chứng phải chứng minh.

## 5. Chuẩn nội bộ để chuẩn bị bài hướng Q2/Q1

Đây là **cổng chất lượng do nhóm đề xuất**, không phải quy định nhận bài hoặc công thức quy đổi quartile:

| Cổng | Bằng chứng cần đạt | Dấu hiệu chưa đạt |
|---|---|---|
| Task/claim rõ | Một câu hỏi và target/evaluator rõ; phân biệt UAV-view, aerial, anti-UAV | Đổi task/dataset giữa chừng nhưng giữ nguyên claim |
| Gap thực | So cơ chế với các prior gần, đọc method+ablation và version | “Abstract không nói” hoặc “scan không thấy” được coi là mới |
| Mechanism | Can thiệp và controls loại được giải thích cạnh tranh quan trọng | AP tăng rồi gán nguyên nhân cho module |
| Measurement | Label audit, data lineage, evaluator/ignore/cap đúng; tránh leakage | Cặp nhãn phụ thuộc được gọi hai ground truth độc lập |
| Utility | Hơn đối chứng đơn giản theo biên hữu ích định trước, dưới metric chính | Chỉ hơn baseline yếu hoặc thay metric để thắng |
| Robustness | Claim-specific transfer; bất định theo scene và biến thiên training runs báo riêng | Một seed hoặc bootstrap từng GT như độc lập |
| Reproducibility | Version, configs, splits, licenses, logs và null results rõ | Chỉ có bảng điểm cuối |

Với tham vọng Q1/hội nghị mạnh, mục tiêu nghiên cứu nên là insight có sức khái quát hoặc thay đổi cách cộng đồng hiểu/đo/giải quyết vấn đề, và bằng chứng tương xứng. Đây là định hướng, không điều kiện đủ hoặc bảo đảm. Chọn journal cụ thể sau khi chốt câu chuyện đóng góp; kiểm đúng hệ xếp hạng, năm và category tại thời điểm chọn, không gắn nhãn Q2 cho venue chỉ từ tên.

## 6. Luồng tiếp theo được khuyến nghị

1. **Hoàn thiện evidence matrix theo claim**, ưu tiên prior có khả năng bác R1/R2. Đọc sâu ít bài sát cơ chế có ích hơn tăng số bài để đủ 50. Các họ còn mở: size/shape-aware uncertainty, label-noise OBB, circular calibration, weak-supervision OBB, assignment competition. Không coi danh sách hiện tại là exhaustive.
2. **Chốt data contract và kế hoạch audit nhãn**: ảnh gốc, biến đổi scale, bbox convention, matching, scene split, quyền sử dụng. Đây là điều kiện để diễn giải kết quả, không phải lý do phải có ba dataset.
3. **Viết protocol pilot có phép bác**, chưa chạy trong lượt này: R1 ưu tiên, R2 giữ cạnh tranh, R3 dùng tách thông tin/recipe. Chốt endpoint, margin hữu ích, controls và quy tắc dừng trước kết quả; chưa chọn architecture thắng.
4. **Sau pilot mới chọn can thiệp nhỏ nhất** xử lý failure được chứng minh. Nếu simple loss/cleaning thắng thì giữ kết luận đó; không ép xây head để hợp rubric.

Các câu hỏi mạnh nhất cần giữ trên bàn: Resize thuần túy có làm gate đổi quyết định dù thông tin không tăng? Góc đang là trục hộp hay heading? Nhãn độc lập có còn disagreement khi có reference tốt hơn? Gain còn sau size/aspect-only controls không? Mất GT ở bước nào sau candidate? Cùng nguồn ảnh có làm transfer quá dễ không? Nếu phương pháp không thắng AP nhưng chỉ ra lỗi đánh giá/nhãn, insight đó có đủ mới và được xác minh độc lập không?

**Trạng thái:** chưa có kết quả detector, chưa tái lập gain tác giả, chưa xác nhận kiến trúc tốt nhất, chưa có bằng chứng để cấp band Q2/Q1. Đã có cơ sở sửa các kết luận quá mạnh và chọn những phép thử phân biệt được các hướng. Các ngày/venue dự báo trong note trước là lịch sử, không được xác nhận lại bởi audit này.
