# T07 — Phản biện độc lập quy trình chọn câu hỏi nghiên cứu

**Ngày:** 2026-10-13. **Phạm vi:** Multi-scale Aerial Object Detection and Segmentation (#7), mở lại không gian vấn đề; bỏ ràng buộc chi phí tính toán. **Worker:** ieee-q1-devil-advocate + paper-synthesize (expand). **Nguồn đầu vào:** REPORT.md, DECISIONS.md, EXPERIMENT-PLAN.md và corpus-50.csv trong `notes/t07-fresh-research/`; `notes/claims-ledger.md` C-3, C-7–C-13. Đây là phản biện quá trình lập đề tài, không phải chấm bản thảo hay dự đoán venue.

**Kết luận:** lựa chọn H1 trước đây có lý do thực dụng dưới 4 tuần/60 USD, nhưng chưa có lý do khoa học để H1 tiếp tục đứng đầu khi bỏ chi phí. Phải mở lại cả định nghĩa đầu ra, chế độ quan sát và hiện tượng cần giải thích trước khi chọn kiến trúc. Không chạy thí nghiệm trong lượt phản biện này.

## 1. Bằng chứng nào đã có, điều gì chỉ là suy luận

Các nhận định về paper dưới đây kế thừa **hồ sơ đã đọc**, không tự nhận đã kiểm tra lại toàn văn. Corpus có 39 abstract/metadata, 10 đoạn chọn lọc full text, 1 trích đoạn publisher [REPORT §2; DECISIONS “Screening”]. Mức đọc này đủ chặn một số claim mới rộng; chưa đủ xác nhận toàn bộ khoảng trống.

| Bằng chứng có trong đầu vào | Hệ quả suy luận của reviewer |
|---|---|
| H1 được ưu tiên vì có thể dùng cache inference và predictor nhỏ; H4/H5 bị hạn chế bởi nguồn lực [REPORT §5; DECISIONS D2–D3] | Không giữ thứ tự H1–H5 sau đổi mục tiêu; thứ tự cũ không phải xếp hạng ý nghĩa nghiên cứu. |
| Corpus có 14 mục resolution, 12 geometry, 10 representation/segmentation; các mục SAM2/SkySense/generic transformer đã nhường chỗ cho allocation [DECISIONS] | Bản đồ mới khởi đi từ corpus này sẽ dễ tái tạo ưu tiên allocation. Đây là thiên lệch tuyển tài liệu có thể kiểm tra, không phải lỗi của từng paper. |
| R13 đã dự đoán accuracy gain; R14 điều phối theo latency; F04 có fixed-backend closure; F05 mới ở mức publisher excerpts | Generic gain routing đã có tiền lệ. Không được kết luận novelty đã đóng hoàn toàn, cũng không được dùng phần chưa đọc làm gap. |
| G10 biểu diễn Gaussian bằng Cholesky; G12 có angle distribution trong hồ sơ | Covariance hình học, bất định góc và độ tin cậy của quyết định là ba đối tượng phải định nghĩa riêng. |
| D04/iSAID dùng ảnh DOTA-v1.0; D05 bao gồm detection/tracking; S05–S06 có protocol segmentation khác automatic detection | Đếm dataset hoặc gộp chữ “video/segmentation” không tạo ra bằng chứng độc lập/cùng task. |
| R07 ghi AI-TOD-v2 sửa nhãn thiếu/sai vị trí; F03 nghiên cứu domain shift | Nhãn và shift cần là giả thuyết cạnh tranh với “thiếu module đa tỷ lệ”; chưa biết yếu tố nào trội trong bài toán mới. |

Các phần “câu hỏi”, “đối chứng”, “quy trình” bên dưới là **[design]/[suy luận]**, không phải kết quả thực nghiệm hay tuyên bố chưa ai làm.

## 2. Hai mươi điểm dễ làm lệch kết luận

Nhiều điểm đã được kế hoạch cũ phòng ngừa đúng. Chúng được giữ làm cổng kiểm tra, không mô tả sai rằng tác giả đã phạm tất cả.

| # | Giả định hoặc failure mode | Câu hỏi red-team và thay đổi cần làm |
|---|---|---|
| 1 | **Neo vào H1 sau khi bỏ chi phí.** REPORT §5 xếp H1 theo khả năng chạy rẻ. | Nếu không phải tiết kiệm phép tính, vì sao không xử lý toàn bộ chi tiết? Tách mục tiêu chất lượng tối đa và mục tiêu đáp ứng deadline; chỉ giữ allocation khi có lợi ích khoa học/use case rõ. |
| 2 | **#7 bị thu hẹp thành tiny OBB.** Detection/segmentation và multi-scale rộng hơn lựa chọn đó. | Người dùng cần phân biệt instance, diện tích, đếm vật thể, hình học hay định danh theo thời gian? Giữ HBB, OBB, instance/semantic segmentation như lựa chọn đầu ra; không coi segmentation là fallback sau H1. |
| 3 | **Corpus tự củng cố câu hỏi.** R/G chiếm 26/50, còn video/tracking không có cụm phương pháp riêng. | Có thể câu hỏi hay nằm ngoài từ khóa đã tìm? Bổ sung tìm theo hiện tượng và từng nhánh task, có log tuyển/loại; không buộc giữ con số 50. |
| 4 | **Không thấy trong abstract → chưa ai giải.** REPORT đã thừa nhận độ đọc hạn chế. | Bài gần nhất thực sự thiếu điều gì ở method/supplement? Dùng ba nhãn: đã thấy giải trong phạm vi X; còn lỗi đã đo trong X; chưa biết. Không gắn “open gap” cho ô chưa đọc. |
| 5 | **Giải được benchmark → giải được vấn đề.** | Điều kiện nào của benchmark làm bài toán dễ hơn triển khai: ảnh tĩnh, known classes, đủ nhãn, resize, prompt? Ghi “đã chứng minh trong setup X”; không nói “tiny detection đã giải quyết”. |
| 6 | **Multi-scale là một cơ chế duy nhất.** | Tách scale của vật thể theo pixel, GSD, khoảng cách/độ cao, mức feature pyramid, kích thước crop và biến đổi theo thời gian. Một can thiệp vào FPN không tự trả lời câu hỏi GSD. [B01, S07; phân tích thiết kế] |
| 7 | **Zoom luôn thu thêm thông tin.** EXPERIMENT-PLAN §4 đã tách crop và upsample. | Thêm phân biệt optical zoom/thay đổi điểm quan sát với digital crop. Crop giữ chi tiết ảnh sẵn có; SR dùng prior; quan sát mới có thể thêm phép đo. Kiểm soát cùng vùng nhìn, nguồn pixel, interpolation, blur và context. |
| 8 | **Zoom có lợi nghĩa là cần selector mới.** | Lợi ích có chỉ do mạng được thấy kích thước vật thể quen thuộc, nhiều pixel, hoặc ensemble nhiều view? So resizing/tiling toàn ảnh và huấn luyện scale-matched. Không gán gain cho “thông minh chọn vùng” trước phân rã này. [R04, R13, F04] |
| 9 | **Reliability luôn thêm giá trị sau predicted gain.** | Nếu mục tiêu chỉ tối đa kỳ vọng utility cộng độc lập, conditional mean đã chứa thông tin quyết định cần thiết; variance không mặc nhiên cải thiện policy. Định nghĩa tail risk, deadline, ràng buộc thất bại hoặc tương tác vùng để biện minh reliability; đây là điều kiện mô hình, không kết quả đã chứng minh cho AP. |
| 10 | **Hiệu chuẩn tốt → AP hoặc policy tốt.** | Calibration error nhỏ có thể do score co lại; ranking/chọn vùng vẫn không đổi. Báo calibration, discrimination và utility quyết định riêng; so hiệu chỉnh hậu nghiệm đơn giản, mean-only, uncertainty-shuffled và matched-coverage khi phù hợp. |
| 11 | **Fixed backend chứng minh tổng quát.** F04 đã có closure, không được dựng strawman. | Backend cố định tốt cho cô lập cơ chế, nhưng có thể chỉ đo lỗi của checkpoint đó. Sau cơ chế nội bộ, xác nhận ở một họ detector/recipe khác; không yêu cầu nhiều backbone vô mục đích. |
| 12 | **Sai góc luôn là lỗi có nghĩa.** | Với hình vuông, đối xứng, tiny/blur hoặc OBB suy từ polygon, angle error có phản ánh sai hình học quan sát được? Kiểm tra quy ước góc/cạnh, biểu diễn tương đương, chất lượng polygon và strata aspect/size. So rotated overlap và ảnh overlay; không chọn representation thắng chính metric được thiết kế cho nó. [G04–G10; thiết kế kiểm chứng] |
| 13 | **Box–mask nhất quán chứng minh multi-task tốt.** | Gain đến từ nhãn mask giàu hơn, teacher mạnh hơn hay regularization mới? So cùng annotation access, box-only + teacher control, mask-supervised baseline; đánh giá cả box và mask theo protocol riêng. DOTA+iSAID không phải cross-domain. [D04, S01–S06] |
| 14 | **Video detection, MOT, SOT là một.** | Video detection cần boxes từng frame; MOT cần duy trì ID nhiều đối tượng; SOT thường nhận target khởi tạo. Khóa đầu vào được phép, initialization, births/deaths và output; không dùng kết quả SOT chứng minh phát hiện vật thể mới. [D05 chỉ là điểm vào; cần corpus phương pháp riêng] |
| 15 | **Thông tin thời gian luôn giúp.** | Thêm frame cải thiện nhờ averaging hay chuyển động thật? Thử single-frame nhiều phép tính, duplicate/shuffled frame, camera-motion compensation, occlusion và causal-only. Future frames phải được đánh dấu offline; không so trực tiếp như online. |
| 16 | **FPS cao là real-time.** | Deadline nào, tốc độ camera nào, queue và frames rơi thế nào? Đo từ frame capture/arrival đến output hữu ích, p95/p99, deadline misses, batch=1 nếu ứng dụng online. Có thể throughput cao nhưng kết quả cũ; báo cả độ trễ và chất lượng theo thời gian. [B05/F01/G12 chỉ gợi ý đối thủ, chưa xác minh pipeline] |
| 17 | **Mọi so sánh công bằng phải cùng compute.** | Bỏ chi phí nghĩa là cần cả chất lượng ở cấu hình tốt nhất hợp lý; equal-compute chỉ bắt buộc khi claim hiệu quả. Tách đối chứng cô lập cơ chế, best-quality reference và deadline-matched deployment. Không trộn ba câu hỏi trong một bảng thắng/thua. |
| 18 | **AP tăng là hình học/recall tốt hơn.** | Score calibration, NMS, duplicate removal, max detections hoặc crowd filtering có giải thích gain? Giữ evaluator/version; tách recall, localization, ranking và merge. Kiểm tra oracle input/perfect predictions, coordinate roundtrip, size bins và cap saturation. EXPERIMENT-PLAN §7 đã yêu cầu phần lớn. |
| 19 | **Nhiều crop/box/seed là nhiều bằng chứng độc lập.** | Resample đơn vị cảnh/sequence/geography phù hợp; paired CI tính lại metric toàn tập. Seed predictor không thay seed detector; DOTA versions/iSAID không tăng số miền. Khóa contrast chính trước confirmatory run; các strata tìm sau là exploratory. |
| 20 | **Nhiều module hoặc empirical scaling là đóng góp khái niệm.** | What is new here? Where is the ablation? Nếu mô hình lớn, recipe mạnh, thêm nhãn hoặc thêm frame giải thích hết gain, kết luận đó trước. Một diagnostic/scaling result vẫn có thể giá trị nếu dự đoán điều kiện thất bại và kiểm chứng được; không cần ép thành kiến trúc hay gán quartile. |

## 3. Năm claim bị bác ở trạng thái hiện tại

1. **Tôi bác claim “H1 là hướng khoa học tốt nhất”** vì bằng chứng chọn H1 hiện tại là ưu tiên dưới ràng buộc cũ, không phải so sánh câu hỏi ngang hàng [REPORT §5; DECISIONS D2].
2. **Tôi bác claim “gain-aware zoom là phần mới”** vì R13 đã nằm ngay trong corpus như prior cùng ý tưởng; khác biệt phải cụ thể hơn.
3. **Tôi bác claim “prior selector chỉ tối ưu coverage, chưa đo detector cuối”** vì hồ sơ F04 nêu closure với backend cố định. Không được hồi sinh strawman này.
4. **Tôi bác claim “Gaussian covariance chứng minh epistemic uncertainty”** vì hồ sơ G10 mô tả encoding hình học; chưa có kiểm định bất định nhận thức nào trong bằng chứng đầu vào.
5. **Tôi bác claim “50 bài đã xác nhận gap, nên vượt trội chỉ còn là xây model”** vì mức đọc và trạng thái chưa có run được REPORT §2 công khai. Đây không phải phủ định triển vọng của mọi candidate; là bác mức chắc chắn không có chứng cứ.

## 4. Các giả thuyết cạnh tranh mạnh nhất phải sống sót

| Hiện tượng cần giải thích | Giả thuyết chính có thể chọn | Giả thuyết cạnh tranh mạnh | Phép thử phân biệt [design] |
|---|---|---|---|
| Vật thể nhỏ bị bỏ sót | Thiếu thông tin ở quan sát thô | Scale mismatch/assignment/nhãn thiếu mới là yếu tố chính | Factorial native detail × train-scale matching; audit nhãn và assignment trước thay backbone. [R04, R06–R08] |
| Crop chi tiết cải thiện AP | Allocation tìm vùng thực sự hữu ích | Xử lý mọi vùng ở độ phân giải cao đã đạt ngang; gain do ensemble/context | Full-detail reference, matched-view ensemble, fixed-grid và context-matched crops. [R04, R13, F04] |
| Reliability policy tốt hơn | Risk estimate dự báo lỗi ngoài mean | Mean predictor/calibration của baseline yếu; proxy density đủ | Mean-only mạnh, post-hoc calibration, density, shuffled uncertainty; khóa loss/risk target. |
| OBB thiếu ổn định | Representation/loss chưa phù hợp | Đối xứng hình học, quy ước nhãn hoặc giới hạn quan sát | Equivalent-box tests, polygon audit, controlled perturbation theo size/aspect; không chỉ raw angle error. [G04–G10] |
| Mask giúp tiny boxes | Hình học box–mask bổ trợ | Thêm supervision/teacher mới là nguyên nhân | Supervision-matched controls; báo mask và detection đều có ích hay chỉ một đầu ra. [D04, S01] |
| Video vượt single-frame | Temporal evidence bù occlusion/motion | Nhiều compute, smoothing hoặc future-frame leakage | Causal frames, duplicate/shuffled controls, first appearance/reappearance và camera motion. |
| Mô hình thất bại ngoài miền | Scale representation chưa invariant | Class prior/background/sensor/label protocol thay đổi | Stratify/match scale; cross-domain tests có kiểm soát ontology, foreground/background, metadata. [F03, S07] |
| AP tăng sau pipeline mới | Chất lượng nhận biết tăng | Merge/ranking/cap/evaluator đổi tạo artifact | Frozen evaluator, error decomposition, identical postprocessing hoặc factorial swap. |

## 5. Quy trình chọn câu hỏi mạnh hơn

**Bước 1 — Lập task cards trước method.** Tạo tối thiểu các nhánh độc lập: ảnh tĩnh detection; instance/semantic segmentation; video detection; MOT; quan sát chủ động/zoom vật lý. Mỗi card ghi người dùng đầu ra, loại nhãn, input được phép, online/offline, miền mục tiêu, biến scale, hiện tượng lỗi và đại lượng thành công. Không yêu cầu thực nghiệm hết các nhánh.

**Bước 2 — Tìm nguồn phản bác theo từng nhánh.** Corpus cũ là seed, không là universe. Tìm cả paper khẳng định giải tốt hiện tượng, nghiên cứu dữ liệu/đánh giá và baseline mạnh ít module. Ghi query, ngày, lý do tuyển/loại, mức đọc và phiên bản. Chỉ dừng mở rộng khi các cơ chế/giả định chính đã có đối thủ đại diện và tìm kiếm đối nghịch không bổ sung lớp giải pháp mới; đây là tiêu chí thực dụng, không chứng minh vét cạn.

**Bước 3 — Viết question cards không tên kiến trúc.** Mẫu: “Trong điều kiện X, nguyên nhân A hay B giải thích lỗi Y; can thiệp Z có tạo thay đổi dự đoán trước không?” Mỗi card bắt buộc có prior gần nhất, khác biệt chưa xác minh, null hypothesis, biến nhiễu mạnh nhất, phép thử bác bỏ và giá trị của kết quả âm.

**Bước 4 — Khảo sát hiện tượng trước thi phương pháp.** Đo tỷ lệ lỗi và response theo scale/context/blur/density/occlusion trên dữ liệu phù hợp. Không chọn nhóm con chỉ vì proposal có lợi ở đó. Oracle headroom phải được ghi là chẩn đoán; có headroom không chứng minh policy học được.

**Bước 5 — Chọn 2–3 câu hỏi bằng bằng chứng, không điểm giả chính xác.** So độ quan trọng của lỗi, sức phân biệt giữa các giải thích, khoảng cách với prior đã đọc, khả năng đo đúng, và phạm vi giá trị khi câu trả lời âm. Ghi “chưa biết” thay cho điểm thấp ở nhánh thiếu nguồn. Bỏ cả chi phí và thời gian khỏi bộ lọc khoa học ở lượt lập bản đồ này.

**Bước 6 — Định nghĩa “vượt trội” trước run xác nhận.** Chọn rõ: chất lượng tốt hơn trong cùng task/input/supervision; tốt hơn dưới deadline online; hoặc chuyển miền tốt hơn. Đăng ký metric chính, baseline gần nhất, effect size hữu ích theo use case, CI theo scene/sequence và điều kiện không được kém. Không có ngưỡng AP phổ quát; không hứa trước kết quả.

**Bước 7 — Chỉ sau đó chọn kiến trúc.** Một phương pháp phải gắn với một failure mechanism có bằng chứng. Chạy đối chứng đơn giản mạnh, kiểm tra alternative explanations, rồi tái lập trên điều kiện có thể bác claim tổng quát. Claim cuối cùng không rộng hơn tập điều kiện đã kiểm tra.

## 6. Câu hỏi mở để thảo luận mà không ưu ái H1

- Khi giữ pixel nguồn cố định, đa tỷ lệ đang bù thông tin mất do resize, bù scale mismatch của mô hình, hay bù thiếu context?
- Có miền size/aspect/blur mà OBB orientation không phải đầu ra đáng tin, nhưng mask/occupancy/count vẫn hữu ích không?
- Khi cùng supervision, box và mask thực sự giúp nhau ở vật thể nào; negative transfer xảy ra ở đâu?
- Một mô hình mạnh xử lý toàn bộ chi tiết còn thất bại ở loại cảnh nào? Lỗi đó có đáng nghiên cứu hơn allocation không?
- Temporal evidence cứu được false negatives nào mà single-frame thêm compute không cứu được? Đổi lại có bỏ sót vật thể mới xuất hiện không?
- Tracking giữ ID tốt hơn có cải thiện đầu ra người dùng cần, hay chỉ làm đường đi trông mượt nhưng duy trì box sai?
- Real-time trong ứng dụng này yêu cầu phát hiện mới, định vị hiện tại hay cảnh báo trước deadline? Worst-case scene có khác average scene không?
- Optical zoom/chọn điểm quan sát đổi field of view và rủi ro mất đối tượng thế nào? Dữ liệu có thật sự chứa hành động/quan sát cần kiểm chứng không?
- Shift về scale có còn giải thích lỗi khi đã khớp class mix, cảnh nền, sensor và chất lượng nhãn không?
- Kết quả nào buộc ta bỏ toàn bộ đề xuất module và chuyển sang nghiên cứu dữ liệu/evaluation?

## 7. Yêu cầu đối với bản tổng hợp kế tiếp

Giữ một bảng “bằng chứng / suy luận / câu hỏi chưa biết”; đặt segmentation và video trên cùng tầng lựa chọn với detection. Không nhập deadline từ lịch cũ nếu người dùng chưa giữ lại; không đưa bảng giá. Không dùng bảng tier→quartile của skill như luật publisher. Cần thêm nguồn chuyên biệt video/MOT/SOT/active observation trước khi mô tả mức đã giải quyết ở các nhánh đó. Bản tổng hợp đạt khi người đọc có thể **chọn một câu hỏi và hiểu điều gì sẽ bác nó**, chưa cần chọn một network.

## 8. Gom các trục thành chương trình nghiên cứu có thể bác bỏ

**Phản biện cấu trúc:** 12–14 trục là bản đồ chẩn đoán tốt nhưng sẽ thành danh mục rời rạc nếu mỗi trục được gọi là một đề tài. “Pixel”, “calibration” và “MOT” không cùng cấp phân loại: lần lượt là điều kiện quan sát, tính chất của dự đoán và nhiệm vụ. Không cộng điểm độ phủ để suy chất lượng đề tài. Đề xuất dùng năm chương trình dưới đây, bên trong chọn đúng một output/task cho thí nghiệm. Đây là các **mệnh đề ứng viên [design]**, chưa phải gap xác nhận.

| Chương trình | Một mệnh đề trung tâm có thể bác bỏ | Can thiệp và phép bác | Các trục được quy về đây |
|---|---|---|---|
| P-A: Điều kiện quan sát quyết định khả năng nhận biết | Trong nhóm lỗi X đã định nghĩa, thông tin ảnh nguồn quyết định chất lượng nhiều hơn việc biểu diễn cùng dữ liệu ở nhiều tỷ lệ. | Factorial thêm chi tiết nguồn × scale-matched representation, giữ context thích hợp; bác nếu representation/augmentation trên cùng pixel loại bỏ lỗi ngang nhau. Optical zoom là phiên bản task riêng có thêm hành động, không gộp vào crop benchmark. | Pixel, SR, crop/zoom, representation/context. |
| P-B: Đầu ra hình học phải phù hợp khả năng quan sát | Biểu diễn đối xứng/khả năng phân biệt hình học giải thích bất ổn OBB hoặc tách instance tốt hơn giả thuyết chỉ thiếu capacity. | Chọn OBB **hoặc** instance masks làm output chính; can thiệp representation và kiểm tra size/aspect/occlusion đã khóa; bác nếu quy ước nhãn hoặc baseline mạnh giải thích hết. | OBB geometry, crowd separation, mask boundaries. |
| P-C: Thông tin thời gian có ích khi tính cả tuổi của kết quả | Với tác vụ online đã khóa, lợi ích thêm frame không còn đơn điệu sau khi xét độ trễ và tính mới của output. | Vary temporal evidence/latency độc lập bằng replay đo được; so causal single-frame và temporal methods trên timestamp đích, kiểm tra missed births/ID nếu task yêu cầu. Bác nếu ordering chất lượng không đổi trong miền deadline đã chọn. | Video detection, MOT, streaming freshness. |
| P-D: Scale transfer dưới thay đổi miền | Một yếu tố scale xác định trước giải thích phần lỗi chuyển miền còn lại sau khi kiểm soát khác biệt lớp, cảnh nền và sensor. | Matching/stratification và can thiệp scale; bác nếu domain label/background/sensor giải thích lỗi còn lại. Open-vocabulary là task extension riêng, phải khóa vocabulary/prompts trước; không mặc định là cùng giả thuyết. | Domain/sensor shift, scale metadata; open-world như nhánh mở rộng. |
| P-E: Chất lượng supervision quyết định giới hạn đang quan sát | Trong nhóm lỗi X, sửa loại sai nhãn cụ thể tạo cải thiện bền hơn thêm mô hình phức tạp dưới annotation access đã kiểm soát. | Audit/reannotation có protocol; factorial label quality × model; bác nếu gain chỉ từ thêm số nhãn hoặc không vượt annotation-matched baseline. | Weak/sparse labels, annotation noise, teacher/prompt access. |

**Calibration là trục kiểm định xuyên suốt**, không tự là chương trình thứ sáu. Chỉ tách thành đề tài nếu câu hỏi chính là một quyết định sử dụng confidence: chọn quan sát, abstain, phát cảnh báo hoặc giữ track; phải đo downstream utility riêng với calibration. Real-time cũng là điều kiện đánh giá trừ khi mệnh đề nghiên cứu nằm chính ở age/latency như P-C.

**Tránh ba cách gom sai:** (i) gộp OBB và mask chỉ vì đều có từ geometry mà không chọn đầu ra chính; (ii) gộp video detection/MOT/SOT vì dùng frame; (iii) gom mọi shift/open-world vào “generalization” rồi không còn một null hypothesis đủ rõ. Chương trình là khung tìm câu hỏi, không là lời hứa thực hiện năm dự án.

**Kiểm tra nguồn mới khi bản evidence đến:** nếu paper gần như HARD hoặc Towards Streaming Perception đã trực tiếp đặt vấn đề latency/freshness, không được claim P-C mới chỉ nhờ thêm chữ streaming. Nếu equivariance đã là đối tượng của MessDet, không được gọi strict-versus-approximate equivariance một gap dựa trên nhãn chủ đề. Phải chỉ ra điều kiện và phép thử còn chưa biết sau khi đọc nguồn; tên paper do điều phối viên cung cấp chưa tự là bằng chứng phương pháp trong bản phản biện này.

## Thuật ngữ

| English | Tiếng Việt | Nghĩa trong phản biện |
|---|---|---|
| Alternative explanation | Giải thích cạnh tranh | Nguyên nhân khác cũng tạo được kết quả đang quan sát. |
| Causal online inference | Suy luận trực tuyến nhân quả | Chỉ dùng thông tin đã có tại thời điểm ra kết quả. |
| Headroom | Dư địa cải thiện | Khoảng cách tới đối chứng chẩn đoán; không bảo đảm có phương pháp thực thi đạt được. |
| Epistemic uncertainty | Bất định nhận thức | Bất định liên quan tri thức/mô hình; khác tham số hình học của box. |
| Ground sampling distance | Độ phân giải mặt đất | Kích thước trên mặt đất tương ứng một pixel; không suy ra chỉ từ số pixel ảnh. |
