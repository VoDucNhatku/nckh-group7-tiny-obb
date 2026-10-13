# Tiny-object detection từ UAV: có cần multi-view và nên tin điều gì?

**Ngày:** 2026-10-13. **Reviewer:** Astra/high; `ieee-q1-devil-advocate` + `paper-synthesize`. **Scope:** nghiên cứu tài liệu, không triển khai, không chạy benchmark. **Anchor:** ảnh **từ UAV** nhìn vật thể trong cảnh; không đánh đồng với camera mặt đất/air-to-air phát hiện chính chiếc drone. **Nguồn máy đọc:** [multiview-sources.json](multiview-sources.json).

## 1. Trả lời trực tiếp

**Multi-view không phải điều kiện bắt buộc của UAV tiny-object detection.** Nó đáng nghiên cứu khi quan sát khác cung cấp bằng chứng mà ảnh hiện tại thiếu, hoặc đầu ra cần bao quát/định vị qua nhiều điểm nhìn. Trước tiên phải biết lỗi nào không giải quyết được bằng khai thác tốt hơn cùng ảnh. Chọn single-view làm bài toán lõi là lựa chọn thiết kế phạm vi, không phải kết luận rằng multi-view vô ích hay một ý tưởng mới.

Chỉ được gọi một nguồn quan sát bổ sung là **cần thiết trong phạm vi đã đặc tả** nếu đầu ra cần thông tin không thể phân biệt từ nguồn hiện có theo các giả định của bài toán. Kể cả vậy, nguồn cần thêm có thể là thời gian, sensor khác hoặc thay điểm nhìn; chưa chứng minh phải có nhiều UAV. Đây là lập luận về thông tin [suy luận], không là kết quả của một benchmark.

Bỏ giới hạn tiền train không xóa deadline, độ trễ truyền, vùng nhìn, occlusion hoặc hạn chế phép đo. Ngược lại, không được áp một latency budget tùy ý chỉ để tạo lý do cho selector. Giữ đối chứng xử lý toàn ảnh chi tiết bằng mô hình mạnh khi câu hỏi là chất lượng tốt nhất; giữ end-to-end latency khi use case thực sự online.

## 2. Sáu nghĩa “nhiều view” cần phân biệt [taxonomy thiết kế]

| Thiết lập | Quan sát nào mới? | Điểm phải khóa |
|---|---|---|
| Crop/multi-scale cùng ảnh | Không thêm phép đo ngoài ảnh nguồn; có thể giữ chi tiết trước resize | Vùng nguồn, interpolation, context, mapping về ảnh gốc. |
| Test-time augmentation | Biến đổi cùng phép đo, có thể đổi đáp ứng mô hình | Biến đổi khả nghịch, merge, số lần nhìn; không gọi là bổ sung bằng chứng occlusion. |
| Video một camera di chuyển | Thêm phép đo ở thời điểm/pose khác; đồng thời scene có thể đổi | Causal window, camera/object motion, timestamps, vật thể xuất hiện/biến mất. |
| Nhiều camera trên một UAV | Nhiều hướng nhìn cùng platform; có thể tăng coverage hoặc overlap | Số camera, overlap, đồng bộ, calibration nếu cơ chế sử dụng hình học. |
| Nhiều UAV cùng quan sát | Nhiều vị trí quan sát và nhiều đường truyền | Ego/global/per-view output, hợp nhất instance, truyền thông, pose/sync uncertainty. |
| Multi-view khi train, một view lúc test | Thêm supervision/prior học được; test không có camera thứ hai | Quyền truy cập dữ liệu/nhãn khi train, distillation, split theo scene; không quảng bá như inference fusion. |

**Một UAV ≠ một view; nhiều ảnh ≠ nhiều góc nhìn độc lập; một track ≠ một detection được quan sát trực tiếp.** Không dùng những cặp từ đó thay nhau trong problem statement.

## 3. Ba exemplar sơ cấp: cơ chế có thật, phạm vi có giới hạn

Các nguồn được chọn vì cho phép kiểm tra mechanism + evaluation, không vì là “ba bài tốt nhất” đã xếp hạng. Đã đọc chọn lọc method/evaluation; không audit code. **Các benchmark UAV ở ba exemplar là mô phỏng và đầu ra chính 3D/BEV; chưa cung cấp bằng chứng trực tiếp rằng tiny 2D detection ngoài thực tế đã được giải.**

### MV01 — Where2comm / CoPerception-UAVs

[NeurIPS 2022 paper](https://proceedings.neurips.cc/paper_files/paper/2022/file/1f5c5cd01b864d53cc5fa0a3472e152e-Paper-Conference.pdf), §3–5; [dataset tác giả](https://siheng-chen.github.io/dataset/coperception-uav/).

**[source]** BEV chung, confidence/request maps và sparse feature messages điều khiển fusion. UAV benchmark dùng ảnh mô phỏng đồng bộ; đánh giá 3D AP và lượng message, so no-collaboration/late-fusion. §5.2/Fig.5 cho thấy localization noise làm giảm hiệu năng; Fig.6 minh họa cứu vật thể bị tòa nhà che. Đây là chứng cứ cho bổ sung quan sát và rủi ro alignment; byte count không phải measured network latency. Không coi confidence map là uncertainty được hiệu chuẩn.

### MV02 — UCDNet / AeroCollab3D

[arXiv v1](https://arxiv.org/html/2406.04648v1), §3.1–3.5, §4.1–4.4, Appendix A; [publisher record](https://ieeexplore.ieee.org/document/10802930/). Method audit dựa trên v1, không tự nhận đã đối chiếu toàn bộ bản journal.

**[source]** Ground-depth prior dùng camera intrinsics/extrinsics và ground height; homologous-point consistency hỗ trợ ánh xạ feature sang 3D. Đánh giá AeroCollab3D/CoPerception-UAVs mô phỏng, metric theo khoảng cách tâm; có ablation mapping/loss. Appendix vẫn ghi bỏ sót do vật thể nhỏ. §4.3 bỏ hai agent không overlap. §4.2 nói key frames, §4.3 lại nói two-frame setting: không mô tả đây là bằng chứng single-frame thuần cho đến khi giải quyết khác biệt protocol. Không sao chép headline gain.

### MV03 — UAV3D

[NeurIPS 2024 paper](https://papers.neurips.cc/paper_files/paper/2024/file/643ea9b3843bd8f525ad8801437a2022-Paper-Datasets_and_Benchmarks_Track.pdf), §3.1–3.3, §4.1/4.3, Tables 7–8; [author project](https://huiyegit.github.io/UAV3D_Benchmark/).

**[source]** Một UAV có năm camera; năm UAV cung cấp 25 ảnh đồng bộ/sample, kèm camera geometry. Benchmark gộp vehicle categories thành car và dùng 3D metrics. So intermediate-message collaboration với một-UAV baseline và all-images reference. Table 8: When2Com có mAP 0.547 so baseline 0.542 nhưng NDS 0.505 so 0.558. Multi-agent không thắng mọi endpoint. Tên “upper-bound” của paper là empirical all-input reference, không là giới hạn toán học.

**Giới hạn tuyển nguồn:** chỉ ba exemplar này không chứng minh không tồn tại real-world/uncalibrated/asynchronous UAV fusion. Bản PDF “Dual-View Drone Dataset” được tìm thấy là draft ẩn danh có cả ground/aerial views; không dùng như benchmark multi-UAV đã xác minh. Không lấy các kết quả phát hiện UAV từ ground/air-to-air thay cho scene detection từ UAV.

## 4. Bảng quyết định: cần, hữu ích hay chưa có lý do? [design]

| Tình huống | Đánh giá multi-view | Kiểm tra quyết định |
|---|---|---|
| Task chỉ hỏi box của vật thể nhìn thấy trong một ảnh cung cấp sẵn | **Không bắt buộc** | Single-view strong baseline hợp lệ. Multi-view sẽ đổi thông tin đầu vào, cần protocol riêng. |
| Crop native đã cứu vật thể nhỏ bị mất khi resize | **Chưa có lý do chuyển task** | Phân biệt giữ pixel với góc nhìn mới; so scale-matched training và full-detail trước. |
| Vật thể bị che trong ego view nhưng hiện ở view khác | **Hữu ích có căn cứ cơ chế** | Same-scene paired views; visibility annotation; đánh giá cùng target universe. Không tính lợi ích coverage như lợi ích localization. |
| Task phải biết vật thể hoàn toàn không quan sát được từ ego và không có prior/history đủ phân biệt | **Cần thông tin bổ sung theo giả định** | Một view khác là một cách cung cấp; chưa chứng minh phải là nhiều UAV thay sensor/time/action. |
| Cần tọa độ 3D hoặc map chung có độ chính xác xác định | **Có ích, không luôn bắt buộc** | So monocular + known geometry/prior hoặc depth sensor; multi-view phải chứng minh giảm ambiguity, không suy 2D AP sang 3D. |
| Nhiều view mở rộng vùng nhìn nhưng không overlap | **Hữu ích cho coverage; chưa chắc cho cùng-object fusion** | Tách union-FOV evaluation và overlap-only evaluation; dedup khi cùng instance có thể xuất hiện ở biên. |
| Camera thứ hai thấy mục tiêu lớn/sắc hơn | **Có thể hữu ích; lý do chưa chắc là geometry** | So best single-view selector, quality/resolution-matched views, rồi mới claim cross-view reasoning. |
| Chỉ có các frame một UAV không đồng thời | **Nghiên cứu temporal trước** | Causal vs offline, motion và age; không tự gọi synchronised multi-view. |
| View bổ sung trùng, lệch thời gian, quá nhiễu hoặc sai correspondence | **Có thể không giúp/có thể hại** | Duplicate-view, time-offset, wrong-pair và alignment perturbation controls; dự đoán trước vùng failure. |
| Chỉ muốn thêm attention/fusion để đề tài nghe mạnh hơn | **Chưa được biện minh** | Chưa có observed failure và discriminating test thì dừng tuyên bố cần multi-view. |

Mọi từ “cần” trong bảng là có điều kiện vào task, không là tuyên bố phổ quát về aerial perception.

## 5. Dữ liệu phải có: phụ thuộc đầu ra và cơ chế

| Thiết kế | Tối thiểu để kiểm tra claim [design] | Không được bắt buộc sai |
|---|---|---|
| Multi-view training / single-view testing | Scene/view linkage, train/test scene split, nguồn nhãn và quyền truy cập teacher | Không tự cần calibration/đồng bộ chính xác nếu chỉ học representation từ các view. |
| Per-view 2D detection và semantic feature exchange | Camera/view identity, per-view boxes, cặp scene; thời gian hoặc protocol tolerance nếu scene động | Intrinsics/extrinsics không luôn bắt buộc nếu model học correspondence; phải đánh giá failures của sự liên kết học được. |
| Geometry-based 3D/BEV fusion | Intrinsics, pose/extrinsics theo thời gian, hệ tọa độ/quy ước, ground/depth nếu method giả định, 3D labels đúng timestamp | Không suy geometry GT có sẵn trong simulator thành sensor pose hoàn hảo ngoài thực tế. [MV02/MV03 minh họa geometry-dependent methods] |
| Global counting / identity fusion | Cross-view instance correspondence hoặc world GT cho matching/dedup; visibility/FOV masks | Track IDs không bắt buộc cho mọi detector; cần khi claim ID continuity hoặc thống kê cùng-object recovery. |
| Moving-camera temporal detection | Frame timestamp, causal history, boxes/visibility theo thời gian, sequence split; pose/motion estimation nếu model dùng | GT track IDs không nhất thiết là input; không đưa future frame vào causal baseline. |
| Online multi-agent perception | Capture/send/receive/output time, payload schema, bytes, topology, queue, drop/jitter, stale-message handling, compute placement | Không dùng communication bytes/FPS thay end-to-end age; không giả định sync tuyệt đối nếu task cho asynchronous. |

Nếu camera chưa hiệu chuẩn, vẫn có thể nghiên cứu learned association, set-level fusion, hoặc cross-view supervision. **Không có calibration không đồng nghĩa không nghiên cứu được multi-view**; nó thay đổi claim có thể bảo vệ và cách ground truth kiểm tra alignment/metric-scale. Nếu thời gian chưa đồng bộ, phải biết/ước lượng offset hoặc xem offset là biến nhiễu có protocol; không tự coi mọi view là cùng trạng thái vật thể.

## 6. Gain đến từ đâu? Các phép phân rã có thể bác giả thuyết

Các dòng sau là **[causal hypotheses/design]**, không là chứng minh novelty. MV01–MV03 cung cấp prior gần; phạm vi tiny 2D vẫn cần nguồn/dữ liệu khớp.

| Cơ chế ứng viên | Giải thích cạnh tranh | Phép thử phân biệt và kết quả bác |
|---|---|---|
| **Bổ sung visibility**: view B thấy phần A bị che | B chỉ có pixel đẹp hơn; model nhận thêm data | Same-object visible/occluded strata; match quality; nếu gain không tập trung theo visibility complement sau kiểm soát, bác giải thích occlusion-specific. |
| **Thêm resolution hữu dụng**: B giữ chi tiết discriminative | Scale mismatch/teacher supervision mới là nguyên nhân | B downsample tới quality của A; A native crop/train-scale match; nếu gain tồn tại chỉ khi B sắc hơn thì không gán cho geometry. |
| **Ràng buộc geometry** giảm ambiguity định vị | Ensemble/late fusion đủ | So calibration-correct với pose perturbations có kiểm soát và geometry-free baseline cùng views. Không dùng random camera mismatch làm bằng chứng độc lập nếu đồng thời phá semantic correspondence. |
| **Coverage** mở rộng target universe | Recall tăng vì mẫu test/denominator đổi | Báo cùng ego-FOV, overlap-only và union-FOV riêng. Gain ngoài ego-FOV không chứng minh tiny localization tốt hơn trong ego image. |
| **Thời gian** cung cấp bằng chứng mới còn giá trị | Smoothing giữ prediction cũ hoặc future leakage | Duplicate/shuffled/causal controls; first appearances và disappears; tính kết quả ở timestamp đích. Nếu gain mất ở targets mới, claim continuity không được biến thành detection tốt tổng quát. |
| **Hợp nhất có chọn lọc** tránh thông tin sai | Chỉ mean confidence/ranking đơn giản đã đủ | Fixed fusion, best-view, post-hoc score calibration và wrong-pair detection; nếu confidence policy tương đương thì không cần uncertainty module. |

**Các trường hợp âm phải dự đoán trước:** baseline giữa camera quá nhỏ có thể ít bổ sung; baseline lớn có thể tăng appearance mismatch và correspondence ambiguity; parallax có thể làm homography phẳng lệch vật thể nổi; time jitter ở target chuyển động có thể tạo duplicate/ghost; correlated noise hoặc cùng occluder có thể làm cả hai view thiếu thông tin. Đây là suy luận hình học/thời gian cần kiểm chứng, **không gán tất cả là kết quả đã đo của ba paper**. Nguồn trực tiếp cho việc alignment noise có thể hạ hiệu năng là MV01; các rủi ro còn lại ở đây là điều kiện thí nghiệm đề xuất.

## 7. Phản biện nền tảng: gom bốn tầng, không ghép một rừng module

### A. Thông tin quan sát

“Tiny” cần định nghĩa ở ảnh nguồn và đầu vào mạng: width/height/area, blur, occlusion, contrast; không gộp vật thể rất nhỏ nhưng sắc với lớn hơn nhưng mất nét. Xác định target universe trước metric. Hai cảnh có cùng pixel footprint vẫn có thể khác khả năng phân biệt; chưa được dùng size như chứng cứ duy nhất cho thiếu thông tin.

**Giả thuyết nhân quả ứng viên:** một phần lỗi do bỏ mất thông tin trong preprocessing, phần còn lại do ambiguity quan sát. Cần đối chứng cùng sensor observation với preprocessing khác và observation giàu hơn. Cải thiện AP do crop chưa chứng minh sensor resolution là giới hạn căn bản; thất bại của một mô hình chưa chứng minh thông tin không tồn tại.

### B. Học và định vị

Phân biệt information bottleneck với assignment, representation, optimization và label ambiguity. “Gradient nhỏ đi” không tự đồng nghĩa localization tốt hơn: có thể do saturation, loss scale hoặc model bỏ qua ví dụ khó. Bounded derivative theo logits không tự bound gradient theo weights; cần xét Jacobian network. Entropy thấp đo phân bố sắc, không tự đo xác suất box đúng. Cần loss-normalized comparisons, chất lượng dự đoán cuối và các alternative explanations.

**Giả thuyết ứng viên:** khi giữ dữ liệu nhìn thấy và supervision cố định, một cơ chế học làm giảm lỗi có hệ thống trong một nhóm quan sát. Nếu scale-matched recipe, normalization hoặc nhãn sạch giải thích hết thì bác nhu cầu module; không phủ nhận giá trị chẩn đoán.

### C. Thời gian

Causal detection, tracking và streaming có endpoint khác nhau. Memory có thể cứu target đã thấy nhưng bỏ sót birth; latency có thể đảo lợi ích của thêm view/frame. Thiết lập online chỉ có nghĩa khi định nghĩa thời điểm trạng thái cần dự đoán, dữ liệu đã đến hệ thống và dữ liệu đến muộn.

**Giả thuyết ứng viên:** lợi ích thông tin của quan sát bổ sung giảm hoặc đổi dấu theo tuổi và sai alignment; phải tìm interaction được dự đoán trước, không chỉ so trung bình AP. Đây là question, chưa claim quy luật phổ quát hay chưa ai thử.

### D. Độ tin cậy của kết luận

Ba thứ cần tách: uncertainty của dự đoán, uncertainty của nhãn/quan sát và uncertainty của ước lượng hiệu quả phương pháp. Một distribution head không giải quyết cả ba. Scene/sequence là đơn vị độc lập phù hợp hơn crop/box trong nhiều setup; cần tránh leakage giữa các view cùng scene. Hiệu quả phải giữ khi evaluator/threshold/merge không bị đổi để thuận phương pháp.

**Quy tắc dừng ở research stage:** nếu chưa có source-level evidence cho task hoặc phép thử phân biệt, ghi chưa biết; không bổ sung module để lấp câu hỏi chưa trả lời. Không chọn model qua venue tier hay số paper đã đọc.

## 8. Kiểm toán toán UGS độc lập theo yêu cầu điều phối

**Nguồn đã xem trực tiếp:** X01, [UGS ICCV 2025 PDF](https://openaccess.thecvf.com/content/ICCV2025/papers/Sun_Uncertainty-Aware_Gradient_Stabilization_for_Small_Object_Detection_ICCV_2025_paper.pdf); local rendered pages `sources/X01-p4.png`, `X01-p5.png`, `X01-p8.png` và text. Đây là kiểm tra độc lập của reviewer trên Eq.11–13 và Table 6, không audit implementation.

**[source]** Fig.4/Eq.11 dùng logits $l_i$ và softmax probabilities $p_i$. Eq.12 là entropy. Eq.13 in đạo hàm theo $l_i$ bằng $-(\log p_i+1)$. Vế phải này là đạo hàm theo xác suất, không phải logits như notation hiện tại.

**[derived — chain rule, với $K$ bins, finite logits]** Đổi tên logits thành $z$ để tránh lẫn:

$$
p_i=\frac{e^{z_i}}{\sum_{k=1}^{K}e^{z_k}},\qquad
H(p)=-\sum_{i=1}^{K}p_i\log p_i.
$$

$$
\frac{\partial p_i}{\partial z_j}=p_i(\delta_{ij}-p_j),\qquad
\frac{\partial H}{\partial p_i}=-(\log p_i+1).
$$

$$
\frac{\partial H}{\partial z_j}
=-\sum_i(\log p_i+1)p_i(\delta_{ij}-p_j)
=-p_j(\log p_j+H).
$$

**Sanity check 1:** ở uniform $p_i=1/K$, $H=\log K$, gradient logits bằng 0. Eq.13 như in cho $\log K-1$, nhìn chung khác 0.

**Sanity check 2:** cộng một hằng số vào tất cả logits không đổi softmax; đạo hàm đúng thỏa $\sum_j\partial H/\partial z_j=0$. Dùng derivative theo probabilities thay derivative theo logits không bảo toàn tính chất này.

**Hệ quả giới hạn:** Eq.13 cần sửa biến đạo hàm hoặc thêm softmax Jacobian. Không được tái sử dụng nó như chứng minh bounded logit gradient; vế in còn diverge khi $p_i\to0$. Gradient đúng có bound hữu hạn khi $K$ cố định: $p_j|\log p_j|\le1/e$ và $0\le H\le\log K$ cho một bound thô $1/e+\log K$ [derived]. Điều đó vẫn **không tự chứng minh** weight-gradient ổn định hay uncertainty được hiệu chuẩn. Sai công thức này không tự phủ định AP tác giả báo cáo, cũng không xác nhận code tính gradient sai; autograd trên entropy có thể dùng chain rule đúng.

**Ablation attribution [source + arithmetic]:** Table 6 ghi $L_2$: 21.3 AP; CE: 22.1; CE+IN: 22.5. Do đó incremental IN so CE là **+0.4 AP**, còn CE+IN so $L_2$ là **+1.2 AP**. Prose nói IN “further” tăng 1.2 gây mơ hồ baseline; báo đúng hai contrast, không cáo buộc dữ liệu bịa và không gán +1.2 là isolated effect của IN. Đây cũng là ví dụ tại sao cần đọc bảng, không chỉ abstract/conclusion.

## 9. Hợp đồng bằng chứng cho prompt nghiên cứu sâu hơn

Khối dưới có thể thêm vào prompt điều phối. Nó yêu cầu lập luận kiểm tra được và kết luận có nguồn, không yêu cầu xuất suy nghĩ nội bộ.

> Nghiên cứu UAV-view tiny-object detection; chỉ nghiên cứu, không code/train/deploy. Bỏ chi phí tính toán khỏi bộ lọc chọn câu hỏi. Tập trung bốn tầng: thông tin quan sát; học/định vị; thời gian; độ tin cậy. Không mặc định YOLO/Transformer/SAM, single-view hay multi-view là lời giải mới.
>
> Với mỗi claim quan trọng, cung cấp source ID, primary URL, version/date, task/input/output, đoạn/Equation/Table đã đọc, nội dung tác giả báo cáo, và phần suy luận riêng. Không gọi tải PDF là đã đọc; không lấy snippet thay method audit. Đánh dấu contradiction/unresolved thay vì tự sửa nguồn thành consensus.
>
> Phân biệt số UAV, số camera, số thời điểm và số crops. Nếu bàn multi-view, xác định gain cần đến từ complementary visibility, resolution, geometry hay coverage. Đưa best-single-view, same-information strong baseline và relevant fusion prior vào đối chứng; không chỉ so với model yếu nhận ít thông tin. Không áp calibration/sync/track IDs như điều kiện phổ quát—ghi điều kiện theo task và mechanism.
>
> Trước khi đề xuất kiến trúc, đưa 2–3 giải thích cạnh tranh của một failure, một causal intervention đủ phân biệt, metric chính và kết quả có thể bác giả thuyết. Tách falsifier của giả thuyết khoa học khỏi kill condition của module. Dùng practical-equivalence criterion ở thiết kế xác nhận; không gọi p-value không có ý nghĩa là bằng chứng tương đương.
>
> Đọc method và evaluation của prior gần nhất. Kiểm tra cùng thông tin, supervision, data lineage, frame protocol, label access và evaluator; tách synthetic/real, 2D/3D, HBB/OBB, detection/MOT/SOT, prompted/automatic, offline/causal/streaming. Không chuyển AP giữa các loại này thành xếp hạng.
>
> Mọi công thức đề xuất ghi [cited], [derived] hoặc [design]. Với công thức trung tâm, kiểm tra biến đạo hàm, chain rule, units, symmetry và ít nhất một trường hợp suy biến. Báo lỗi cục bộ đúng phạm vi; không suy sai công thức thành sai mọi thí nghiệm.
>
> Không cam kết novelty/superiority/venue. Khi chưa đọc đủ để loại prior, ghi “chưa xác nhận khác biệt”; khi thiếu dữ liệu paired views/metadata, ghi dependency chưa xác minh chứ không bảo task không thể nghiên cứu. Không mở thêm các nhánh chỉ để đủ số paper; dừng mở rộng khi đã có competing explanations và prior đủ để thiết kế phép thử, đồng thời công khai phần chưa bao phủ.
>
> Deliverable: kết luận phạm vi; bảng evidence/unknown; cơ chế nền tảng; 2–3 question cards có null/alternative/controls/falsifier; danh sách nguồn đã thực đọc; research-only next steps. Trình bày kết luận, giả định, bằng chứng và phản biện ngắn gọn có thể kiểm tra, không cung cấp hidden chain-of-thought.

## 10. Kết luận làm việc

**Giữ single-image UAV tiny detection làm điểm quy chiếu là hợp lý [design], nhưng để cửa multi-view mở theo chẩn đoán.** Chuyển sang multi-view khi chứng minh được hiện tượng cần thông tin bổ sung và protocol có thể tách gain do view mới khỏi gain do pixels/labels/coverage. Ba exemplar đủ bác claim “multi-UAV fusion chưa có”; chúng chưa đủ kết luận câu hỏi tiny 2D ngoài thực tế còn mới hoặc đã được giải. Bước nghiên cứu tiếp theo là chọn hiện tượng có phép phản bác rõ, không là chọn thêm một fusion block.
