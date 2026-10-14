# UAV tiny-object perception: chọn đúng nguyên nhân trước khi chọn kiến trúc

**Ngày:** 13/10/2026. **Phạm vi đã chốt với người dùng:** chỉ nghiên cứu sâu; bỏ chi phí khỏi bộ lọc ý tưởng. Giữ định hướng #7 làm gốc, không bị buộc dùng proposal, YOLO, STAL hoặc OBB cũ. Không triển khai thí nghiệm, không train và chưa có kết quả độc lập.

**Kết luận:** UAV-view tiny-object detection đủ làm trọng tâm. Multi-view là một nhánh có điều kiện, không phải thành phần bắt buộc. Câu hỏi mạnh hơn “ghép kiến trúc nào tốt nhất?” là: **vật thể bị mất ở khâu nào, quan sát còn chứa thông tin gì, và can thiệp nào giải được đúng nguyên nhân đó?** Đây là định hướng nghiên cứu, chưa là tuyên bố mới khoa học hay dự đoán đạt Q1/Q2.

## 1. Phạm vi nên giữ và những nhánh chỉ mở khi có lý do

Đề xuất dùng **phát hiện và định vị vật thể nhỏ từ ảnh UAV** làm điểm quy chiếu chung. “UAV” là camera nhìn cảnh từ trên không, không phải phát hiện chính chiếc drone. HBB/OBB, video, segmentation, multi-view là những lựa chọn đầu ra/đầu vào cần được biện minh riêng. HBB phù hợp nếu chỉ cần vị trí và lớp; OBB cần khi hình học xoay đem lại ý nghĩa cho ứng dụng/evaluation. Tiny tự nó không bắt buộc OBB.

| Câu hỏi thực tế | Nhánh phù hợp | Điều kiện để mở nhánh |
|---|---|---|
| Vật thể có trong ảnh gốc nhưng biến mất sau resize/encoding? | Native crop, feature resolution, scale-matched learning | Tách preprocessing khỏi thay đổi assignment/loss và thêm supervision |
| Thấy vật thể nhưng box chệch vài pixel? | Localization representation, targets, annotation | Kiểm nhãn và giữ evaluator cố định |
| Từng thấy target nhưng mất khi camera quay/che khuất? | Causal temporal detection hoặc MOT | Chọn rõ cần tăng detection recall hay giữ identity |
| Kết quả chính xác nhưng trả ra quá muộn? | Streaming perception | Có timestamp, arrival/output policy và endpoint tại thời điểm cần dùng |
| Cần biên từng đối tượng? | Instance segmentation | Tách given-box masks khỏi tự phát hiện rồi segment |
| Ego view thiếu đối tượng nhưng view khác nhìn thấy? | Multi-view/cooperative perception | Paired scenes, visibility/correspondence và protocol hợp task |

**Bốn thứ thường bị gọi chung là zoom:** crop ảnh nguồn; nội suy digital; learned super-resolution; thay đổi phép đo bằng optical zoom/di chuyển camera. Crop giữ chi tiết đã có; nội suy không thêm phép đo; SR khai thác prior học được; optical/viewpoint thay quan sát nhưng có thể đổi vùng nhìn và motion. Không chuyển kết quả của một loại thành bằng chứng cho mọi loại.

**Một UAV không đồng nghĩa một camera.** UAV3D single-UAV dùng năm camera; cooperative dùng năm UAV/25 ảnh. Ba exemplar multi-view đọc ở lượt này có UAV benchmarks mô phỏng và đầu ra 3D/BEV, nên chưa chứng minh tiny 2D ngoài thực tế đã được giải. [MV01–MV03; chi tiết và nguồn trong [phản biện multi-view](MULTIVIEW-AND-CRITIQUE.md)]

## 2. Tám nền tảng nên nắm trước khi thiết kế model

### 2.1. Pixel ở đâu mới là câu hỏi đầu tiên

Ghi riêng kích thước vật thể tại **ảnh native, input mạng, feature map và thế giới thực**; thêm blur, contrast, occlusion. “Tiny” theo diện tích tương đối của ảnh không nhất thiết là vài pixel native. AI-TOD-v2 dùng tiêu chí tiny của benchmark; SOPSeg dùng max-side bins trong một ablation; HARD/DynUAV có thống kê relative size. Không đổi chúng thành một định nghĩa chung. [BASE02; N03/N04/N18]

**[suy ra, ví dụ minh họa]** Một vật thể rộng 12 px trong ảnh 3840 px, resize cả ảnh về 640 px, còn 2 px. Cắt vùng native rộng 512 px rồi resize về 640 px làm nó rộng 15 input px. Đây vẫn là thông tin từ 12 native px, không phải 15 phép đo mới. Ví dụ chỉ xét tỷ lệ ngang, không có blur hoặc letterbox.

Pinhole projection có $u=f_xX/Z+c_x$. Với đoạn ngang dài $L$, cùng độ sâu $Z$, song song image plane, footprint là $s=f_xL/Z$. Khi resize, $f_x$ tính bằng pixel cũng đổi. Ngoài các giả định đó, không dùng công thức này như phép đo altitude/size chính xác cho mọi UAV. [BASE03; phép suy ra từ mô hình chiếu]

### 2.2. Thiếu tín hiệu và học chưa tốt là hai cơ chế khác nhau

Tăng độ phân giải có thể tăng số positive/negative samples, thay effective loss balance, receptive field và compute. QueryDet Table 3 cho thấy thêm HR-only giảm AP trong setup COCO mini-val; loss rebalance và auxiliary query supervision là phần quan trọng. Vì vậy “thêm P2 tăng AP” chưa tự chứng minh bottleneck duy nhất là mất chi tiết. [R02, [casebook static](CASEBOOK-STATIC.md) §1]

SuperYOLO dùng HR reconstruction target ở training rồi bỏ SR branch khi inference. Lợi ích có thể nằm ở representation/supervision; không phải sensor nhìn được thêm chi tiết lúc test. Bỏ Focus cũng đổi feature resolution/compute. Phép pixel rearrangement của Focus không tự làm mất các pixel đầu vào; cần phân biệt nó với các bước convolution/downsampling sau đó. [N16; audit exact code path chưa làm]

### 2.3. Một pixel là sai số lớn khi object rất nhỏ

**[suy ra]** Hai box vuông HBB cùng cạnh $w$, lệch ngang $\delta\in[0,w]$, không lệch dọc: intersection $=(w-\delta)w$, union $=(w+\delta)w$, nên

$$\operatorname{IoU}=\frac{w-\delta}{w+\delta}.$$

Với $\delta=1$, $w=4,16,64$ lần lượt cho IoU $0.600,0.882,0.969$. Đây là ví dụ hình học, không phải kết quả dataset và không chứng minh nên nới box/đổi metric để tăng điểm. Nó giải thích vì sao **chất lượng nhãn, định nghĩa biên và hệ tọa độ loss** đáng nghiên cứu cùng architecture.

GauCho thay OBB parameterization bằng Cholesky Gaussian; Gaussian isotropic không giữ một góc duy nhất. Covariance hình học không tự là covariance sai số dự đoán. Geometric long axis, semantic heading và box extent là ba đầu ra khác nhau. [G10]

### 2.4. Có prior tốt không đồng nghĩa phục hồi chắc chắn sự thật

**[suy ra, toy inverse problem]** Hai mẫu $[1,0,0,1]$ và $[0,1,1,0]$ cùng cho trung bình $0.5$. Với phép đo chỉ là trung bình này, không có phép nghịch đảo duy nhất. Learned SR có thể chọn reconstruction hợp prior và giúp detection, nhưng từ đó chưa bảo đảm mọi chi tiết sinh ra là chi tiết thật. Muốn claim phục hồi quan sát phải có HR reference/physical acquisition thích hợp; muốn claim downstream utility phải đo task outcome.

Supervision đặc quyền từ HR, IR, nhiều view, teacher masks hay pretrained models phải ghi thành nguồn thông tin được dùng. Baseline không có những nguồn này không đủ để cô lập lợi ích kiến trúc. [N16/N05/N18; suy luận về thiết kế đối chứng]

### 2.5. Frame cũ chỉ có ích khi liên kết còn đúng

Video bổ sung bằng chứng thật nhưng scene, camera và identity đều có thể đổi. DynUAV có ablation CMC: association tăng nhưng false positives cũng có thể tăng, mức lợi ích khác nhau giữa trackers. Bài học là đo **alignment, discovery, association, track survival** riêng; không gọi mọi gain temporal là “nhìn tiny rõ hơn”. [N03]

DroneEyes tách semantic anchors và recent tracking memory. Tracking FIFO có giới hạn không tự chứng minh toàn bộ semantic memory có giới hạn. Memory có thể giúp target đã thấy, trong khi first appearance, query change và re-entry cần kiểm tra riêng. [N05]

### 2.6. Đúng ở frame cũ và đúng lúc cần dùng là hai endpoint

Một hệ thống có thể tăng throughput nhưng vẫn xuất trạng thái cũ. HARD ghi end-to-end latency và s-HOTA; một cặp tracker đảo thứ hạng giữa offline HOTA và s-HOTA. Tuy nhiên default là Car, frame interval 2 giây và nhiều full-machine replicas để không queue. Không dùng kết quả này làm chứng cứ hệ một GPU onboard đạt real-time. [N04]

DroneEyes báo edge deployment nhưng tác giả loại trừ high-speed closed-loop/native-camera-rate. Vì thế từ “online” phải đi với causal input và thời điểm output, không thay thế đo capture-to-output age. [N05]

### 2.7. Entropy, confidence và độ tin cậy phải gắn với câu hỏi

Entropy thấp nói distribution sắc; chưa chứng minh box đúng. Gaussian shape covariance nói extent; chưa chứng minh epistemic uncertainty. Muốn dùng uncertainty để quyết định zoom/history/fusion cần chứng minh nó dự đoán **lỗi hoặc lợi ích hành động** tốt hơn score/size/motion baselines, rồi kiểm benefit của policy đó. [X01/G10; thiết kế suy ra]

Có một cảnh báo cụ thể từ UGS: Eq.13 in derivative entropy theo logits nhưng dùng biểu thức derivative theo probabilities. Hai worker đã kiểm tra độc lập trang PDF. Với $p=\operatorname{softmax}(z)$ và $H=-\sum_i p_i\log p_i$, chain rule cho

$$\frac{\partial H}{\partial z_j}=-p_j(\log p_j+H).$$

Ở uniform distribution gradient logits bằng zero. **Đây là vấn đề cục bộ của công thức in; chưa chứng minh code tính sai hoặc AP báo cáo không đúng.** Bound theo logits cũng chưa bound gradient theo toàn bộ weights nếu chưa xét network Jacobian. Chi tiết chứng minh và attribution Table 6 nằm trong [audit độc lập](MULTIVIEW-AND-CRITIQUE.md#8-kiểm-toán-toán-ugs-độc-lập-theo-yêu-cầu-điều-phối).

### 2.8. Ground truth và evaluator là một phần của luận cứ

SOPSeg đo masks khi đã có box; ReSOS masks do teacher tạo rồi filter, không phải tất cả được vẽ tay độc lập. DynUAV có chính sách annotation occlusion/entry riêng. Các điều kiện này quyết định model đang được thưởng cho điều gì. [N03/N18]

Kiểm data lineage và split theo scene/sequence; DOTA/iSAID có quan hệ nguồn ảnh, không tự gọi chúng là hai miền độc lập. Tách uncertainty của dự đoán, ambiguity của nhãn và uncertainty của ước lượng hiệu quả. Confidence interval trên nhiều box cùng scene không thay được đơn vị độc lập phù hợp. [thiết kế; xem dữ liệu và kiểm chứng trong bộ nghiên cứu trước]

## 3. Những case đã làm thay đổi cách chọn đề tài

Các số dưới là **tác giả báo cáo**, chưa tái lập. Không so trực tiếp AP, HOTA và IoU giữa các hàng.

| Case | Đối chiếu đã đọc | Kiến thức rút ra và giới hạn |
|---|---|---|
| QueryDet, CVPR 2022 | COCO mini-val, RetinaNet R50: HR-only 37.46→36.10 AP; Table 3 | Resolution phải đi cùng learning recipe. CSQ inference và auxiliary query supervision là hai tác dụng cần tách. |
| SuperYOLO, TGRS 2023; bản đọc pre-acceptance | VEDAI first-fold, noFocus 69.5→78.0 mAP50 khi thêm train-only SR; inference GFLOPs cùng 20.4; Table IV | Có thể cải thiện sử dụng LR bằng HR training target. Chưa tách hết generic auxiliary supervision khỏi SR-specific benefit. |
| UGS, ICCV 2025 | Faster R-CNN R50/VisDrone: L2 21.3, CE 22.1, CE+IN 22.5, full 24.2 AP; Table 6 | IN increment so CE là +0.4, còn +1.2 là so L2. Attribution và toán phải kiểm riêng với empirical package gain. |
| GauCho, CVPR 2025 | FCOS R50, DOTA-v1.5 single-scale, cùng ProbIoU: 64.26→65.09 AP50; Table 2 | Đổi representation có gain trong setup, chưa chứng minh tiny-specific hoặc uncertainty calibration. |
| DynUAV, CVPR 2026 | AdapTrack CMC toggle, chung detector: AssA 58.97→66.71, FP 19,902→21,489; Table 5 | Giữ identity tốt hơn có thể đi cùng nhiều false outputs. Cần tách compensation khỏi track management. |
| HARD, preprint v2 09/2026 | Faster R-CNN R50+StrongSORT/ByteTrack: HOTA 40.6/37.1, s-HOTA 17.7/19.4; Table 3 | Ranking đảo dưới freshness protocol. Không là matched ReID-only ablation hoặc single-device native-rate proof. |
| DroneEyes, preprint v1 07/2026 | Router bật, no/tracking/both memories: J&F 29.89/35.76/38.10; Table IV | Memory decomposition có conditional evidence. Referring segmentation không phải closed-set detection/MOT toàn cảnh. |
| SOPSeg, CVPR Findings 2026 | Given-box SAM 71.65→RAM 79.40 mIoU; Table 2 | Local detail/context có giá trị, nhưng detector misses và prompt noise còn ngoài contrast này. |

Nguồn, page/table, controls và falsifiers cho từng hàng: [4 static cases](CASEBOOK-STATIC.md), [4 temporal/mask cases](CASEBOOK-TEMPORAL-MASKS.md). Những bất nhất nội bộ như SuperYOLO MSE/L1, SOPSeg table/prose delta, DroneEyes size-bin text/figure được giữ trong casebook, không tự sửa thành một kết quả thống nhất. Các audit ngoài UGS Eq.13/Table 6 chưa đều được reviewer thứ hai kiểm độc lập.

## 4. Ba chương trình nghiên cứu cạnh tranh — chưa chọn kiến trúc thắng

Không đề xuất ghép cả ba thành một hệ thống. Chọn một câu hỏi chính và dùng hai hướng còn lại làm giải thích cạnh tranh hoặc nhánh có điều kiện. Ưu tiên dưới đây dựa trên khả năng chẩn đoán và độ khớp UAV tiny, **không dựa vào tiền train**.

### A. Khi nào tăng scale thực sự cứu thông tin, khi nào chỉ sửa learning recipe?

**Câu hỏi:** với cùng ảnh nguồn, sai số tiny chịu ảnh hưởng riêng và tương tác thế nào của native-detail preservation, object scale ở input và balance của learning objective?

**Giả thuyết [design]:** một phần gain thường gán cho zoom/HR đến từ scale/assignment/loss mismatch. Sau khi recipe được khớp, native detail vẫn mang lợi ích riêng ở một số strata có blur/contrast/context phù hợp. Cần phân biệt hai effect thay vì giả định một trong hai chi phối mọi trường hợp.

**H0 khoa học cần phân biệt:** sau controls, (H0-A1) không có tương tác có ý nghĩa thực dụng giữa detail access và learning recipe; (H0-A2) không còn effect riêng có ý nghĩa thực dụng của native detail trong các strata đã định trước. Hai phần của giả thuyết phải được kiểm riêng; chọn contrast chính và biên thực dụng trước confirmation runs, không tìm strata hậu nghiệm để giữ câu chuyện.

**Giải thích cạnh tranh/điều kiện không cần module:** strong full-detail + scale-matched baseline giải thích đủ gain; adaptive policy mới không có lợi ích thêm. Hoặc auxiliary labels/teacher mới là nguồn gain. Một simple recipe thắng vẫn có thể ủng hộ chẩn đoán khoa học ở trên.

**Phép thử quyết định sau nghiên cứu:** thiết kế factorial native-detail access × training recipe; ghi object pixel size, context, labels, detector capacity và postprocessing. Resize và crop làm đổi nhiều yếu tố, nên thêm context/centering controls. Có full-detail baseline mạnh, native crop đơn giản, HR/P2+rebalance, train-only auxiliary/teacher controls. Không ép equal compute nếu claim là chất lượng tốt nhất; ghi compute như biến để diễn giải.

**Đầu ra đáng nghiên cứu:** một bản đồ failure có thể dự đoán trên scene mới: nhóm nào mất vì preprocessing, nhóm nào do learning, nhóm nào vẫn thiếu bằng chứng. Nếu có vùng chuyển ổn định mới nghĩ đến rule/architecture điều kiện hóa; chưa đặt tên module.

**Bác giả thuyết và dừng module khác nhau:** nếu không còn independent detail effect sau controls, bác phần giả thuyết về detail trong phạm vi thử. Nếu bản đồ chẩn đoán đúng nhưng simple fixed recipe đã đạt hiệu quả tương đương theo ngưỡng thực dụng định trước, dừng adaptive module; phát hiện nguyên nhân vẫn có thể có giá trị. Không gọi p-value không significant là bằng chứng tương đương.

**Prior gần phải đọc tiếp theo claim:** QueryDet, SuperYOLO, SOPSeg; DynamicZoomin/DenseScout trong corpus trước nếu đề xuất region allocation. Dynamic zoom, train-only SR và crop-aware masks đã có prior, chưa được gọi mới. [R02/N16/N18; corpus trước]

**Metric:** AP theo size và scene; recall ở từng stage; false positives; localization error; quality theo blur/context. Pixel-size strata phải được định nghĩa trước ở native và input. **Còn thiếu:** data-level diagnostics, matched full-detail baseline, exact recipe/code configs. Hiện chỉ có căn cứ để ưu tiên câu hỏi, chưa có dự đoán gain.

### B. Khi nào history trở thành bằng chứng sai cho tiny objects?

**Câu hỏi:** camera motion, correspondence error và tuổi thông tin tương tác thế nào để history giúp target đang theo dõi nhưng gây lỗi ở target mới, re-entry hoặc distractor?

**Giả thuyết [design]:** có các điều kiện nhận diện được mà lịch sử cũ làm tăng false persistence hoặc trì hoãn discovery; ích lợi memory cần đánh giá cùng correspondence và output age. Chưa khẳng định có một ngưỡng phổ quát hoặc thuật toán gating mới.

**H0 khoa học:** sau khi khớp detection và track-management controls, không có thay đổi có ý nghĩa thực dụng của effect do real history theo age/alignment ở các strata entry/re-entry đã định trước. Thiết kế xác nhận cần khóa contrast interaction và ngưỡng thực dụng; chưa có dữ liệu để chọn giá trị số.

**Giải thích cạnh tranh/điều kiện không cần module:** CMC + track management + confidence decay đơn giản giải thích đủ; model history/uncertainty mới chỉ thêm capacity hay smoothing. Một khả năng khác là miss từ detector chi phối, không phải association. Simple temporal rule thành công không tự bác giả thuyết history có lúc gây hại.

**Phép thử quyết định:** cùng raw detections, no-history/real-history/repeated-frame controls; CMC bật/tắt và oracle transform chỉ dùng chẩn đoán; age/alignment perturbations có kiểm soát; giữ track-management policy khi cô lập association. Bổ sung same-backbone temporal baseline nếu claim học từ frames. Tách causal input khỏi offline future access và oracle visibility.

**Metric theo claim:** detection AP/discovery delay nếu target là detection; HOTA/DetA/AssA và births/re-entry/false persistence nếu là MOT; capture-to-output age và current-time evaluation nếu là streaming. Không dùng một metric để thay cả ba. Oracle GT/history không là deployable input.

**Bác bỏ:** nếu tác dụng history không thay theo các điều kiện dự đoán sau controls, giả thuyết về interaction yếu đi. Nếu simple CMC/age-decay đạt tương đương, bỏ module mới. Nếu scene/new-entry failures là annotation policy, sửa question thay vì ép temporal architecture.

**Prior gần:** DynUAV; HARD và Towards Streaming Perception; DroneEyes chỉ là nguồn ý tưởng memory/compression có task khác. Cần đọc tiếp prior temporal detection gần đúng endpoint trước khi chốt novelty. **Còn thiếu:** causal sequence protocol, timestamp/policy, independent label audit và evidence dưới absolute tiny bins. [N03/N04/N05/X04]

### C. Định vị tiny đang sai ở model, ở nhãn hay ở đại lượng muốn dự đoán?

**Câu hỏi:** khi biên/góc của target rất nhỏ không rõ, gain localization đến từ representation liên tục, sửa optimization hay thay đổi cách đối xử với ambiguity của ground truth?

**Giả thuyết [design]:** một phần failure phụ thuộc annotation/observable geometry; tối ưu một điểm/angle duy nhất có thể không phù hợp với ambiguity ấy. Distributional target hoặc supervision có xét ambiguity là ứng viên, chưa được coi lời giải đã mới.

**H0 khoa học:** sau khi khớp size/blur/scene và các controls đã nêu, hiệu ứng sửa nhãn/biểu diễn đối với localization không khác có ý nghĩa thực dụng giữa các mức ambiguity/annotator disagreement được định trước. Đây là một contrast có thể kiểm để đánh giá phần giả thuyết về ambiguity, không là kiểm định mọi nguyên nhân localization.

**Giải thích cạnh tranh/điều kiện không cần module:** nhãn sạch + scale-normalized loss/assignment đủ; new distribution head chỉ regularize hoặc có thêm parameters. Nếu covariance chỉ encode shape thì uncertainty claim không đứng. Nhãn sạch xóa gain của head vẫn có thể ủng hộ luận điểm về label bottleneck.

**Phép thử quyết định:** lấy subset theo scene/size/aspect-ratio/blur, có annotators độc lập và policy adjudication; cùng ảnh/cùng evaluator so original/corrected labels và head/loss controls. Synthetic jitter là sensitivity stress, không thay được chứng cứ nhãn thật. Nếu chọn OBB, tách long-axis khỏi semantic heading và thử near-square cases; nếu chỉ HBB, không mang angle vào để làm đề tài phức tạp hơn.

**Metric:** fixed HBB/OBB AP, pixel localization error, agreement giữa annotators, calibration/coverage chỉ khi dự đoán được định nghĩa xác suất rõ; đổi sang ellipse metric phải là analysis phụ, không dùng để chứng minh đã giải cùng bài toán OBB.

**Bác bỏ và dừng:** nếu ambiguity/label quality không liên hệ failure sau controls, hạ giả thuyết. Nếu cleaning xóa gain của head mới, dừng claim kiến trúc; điều này **có thể ủng hộ** giả thuyết về nhãn, không phải bác nó. Nếu effect nằm ở loss scale, báo đúng cơ chế.

**Prior gần:** UGS/GauCho đã đọc sâu; NWD, RFLA, DN-TOD và các angle-distribution/uncertainty papers trong corpus cần audit khớp claim. **Còn thiếu:** multi-annotator evidence và implementation audit; không lấy lỗi công thức cục bộ của một paper làm bằng chứng hướng mới đúng. [X01/G10]

## 5. Multi-view: giữ cửa mở bằng một phép thử thông tin

Trước khi thêm view, trả lời: **view mới cung cấp visibility, resolution, geometry hay coverage?** Nếu chỉ ảnh đẹp hơn, phải so best-single-view; nếu coverage rộng hơn, tách ego-FOV và union-FOV; nếu geometry, so geometry-free fusion cùng inputs và kiểm pose error. Các mục này là thiết kế kiểm chứng, không khẳng định mọi family phải dùng calibration.

| Quan sát từ chẩn đoán | Quyết định làm việc |
|---|---|
| Native crop/recipe đã giải miss ở cùng image | Tiếp tục single-view để cô lập nguyên nhân; chưa có căn cứ mở multi-view |
| Same-object ego occluded nhưng camera khác thấy | Mở visibility-complement study với same-target evaluation |
| Cần 3D/common-world map | Cân nhắc multi-view cùng monocular/known-geometry/depth baselines |
| Hai view có geometry/appearance nhưng sai correspondence/time | Nghiên cứu robustness của fusion; thêm view có thể hại |
| Chỉ có video một camera | Có thể nghiên cứu temporal; không gọi nó là synchronized cooperative setup |

**Dữ liệu cần tùy method:** learned per-view fusion không luôn cần extrinsics chính xác; geometry-based BEV thường cần calibration/pose/reference frame; ID/counting cần correspondence/dedup; online hợp tác cần capture/send/receive/output timestamps và transmission policy. Thiếu metadata là dependency chưa giải quyết, không phải chứng minh mọi multi-view bất khả thi. [MV01–MV03 và [bảng đầy đủ](MULTIVIEW-AND-CRITIQUE.md)]

## 6. Chuẩn làm việc cho tham vọng Q2/Q1

Không tồn tại công thức “50 papers + ba datasets + một module = Q1”. Quartile JCR là thứ hạng **journal trong category**, không phải điểm chất lượng tự động của từng bài. Khi chọn venue thật phải xác minh hệ xếp hạng, năm và category; không đánh đồng JCR với SJR hoặc conference tier. [V02]

CVPR 2026 yêu cầu xem technical soundness, đóng góp, novelty và impact; không vượt SOTA tự nó chưa đủ để reject, và không mặc định nhiều datasets là điều kiện bắt buộc. Đây là guideline của CVPR, không luật cho mọi Q1 journal. [V01]

**Rubric nội bộ đề xuất — không bảo đảm được nhận:**

| Cổng bằng chứng | Đủ để đi tiếp khi nào? | Hiện trạng |
|---|---|---|
| Problem | Một failure có ý nghĩa, task/input/output rõ và có dữ liệu để kiểm | Scope rõ hơn; chưa đo failure độc lập |
| Prior | Khác biệt với prior gần viết được bằng mechanism/assumptions, không bằng tên module | Đã hiểu 8 cases + 3 exemplars; novelty chưa chốt |
| Correctness | Công thức, units, causal access, data/evaluator đúng | Có audit chọn lọc; chưa audit system |
| Attribution | Strong simple baselines và controls loại được giải thích cạnh tranh chính | Mới thiết kế |
| Evidence | Effect ổn định, uncertainty thích hợp và có giá trị thực dụng | Chưa có experiment |
| Generality | Chứng cứ mở rộng đúng phạm vi claim; dataset độc lập khi claim cross-domain | Chưa có experiment |
| Contribution | Người đọc học được điều hữu ích hơn một bộ hyperparameters/module list | Có câu hỏi có thể kiểm; chưa có finding mới |

Muốn nhắm cao hơn, cần một kết luận làm cộng đồng hiểu/chọn phương pháp tốt hơn, hoặc một phương pháp/benchmark/theory có giá trị rõ và chứng cứ tương xứng. Không tự động gán Câu A là Q2 và Câu B là Q1. Số lượng paper giúp phủ prior, nhưng **đơn vị tiến bộ là câu hỏi được phân biệt bằng bằng chứng**, không số PDF tải xuống.

## 7. Flow nghiên cứu được đề xuất sau lượt này

1. Giữ corpus 50 làm bản đồ, không gọi tất cả là đã đọc sâu. Dùng 120 câu hỏi trước để tìm failure, không triển khai 120 experiments.
2. Ưu tiên **A** để tách observation khỏi learning; **C** là giải thích cạnh tranh cho lỗi định vị. Mở **B** khi chọn video endpoint. Multi-view chỉ mở qua §5.
3. Với câu được chọn, đọc supplement/code/config và prior gần đến mức mô tả được điều đã giải, assumption còn yếu và phép thử phân biệt. Không tìm một “gap” chỉ bằng keyword search hoặc vì không thấy một ablation.
4. Chốt một primary claim, một primary comparison, strata/falsifier/stop condition, split/evaluator và ngưỡng thực dụng trước confirmation runs. Không lựa test set để chọn hypothesis.
5. Chỉ sau research gate mới viết code chẩn đoán, rồi mới quyết định cần kiến trúc gì. Bước này **chưa thực hiện**, phù hợp yêu cầu hiện tại.

Prompt dùng lại đã được viết thành [RESEARCH-PROMPT.md](RESEARCH-PROMPT.md): evidence contract, source versions/locators, competing explanations, mathematical sanity checks, task boundaries, falsifiers và limits. Làm prompt rõ và kiểm được quan trọng hơn làm nó dài.

## 8. Coverage và nguồn gốc bằng chứng

Lượt này đọc method/experiments/ablations/limitations của **8 cases**, cộng **3 multi-view exemplars** với phương pháp/evaluation được chọn lọc. Mức đọc chính xác theo từng bài ở casebooks; không phải 11 bài đều audit đầy đủ supplement/code. N04/N05 là preprint; N18 Findings. Chưa đọc sâu toàn bộ 13 axes, đặc biệt domain shift/open-vocabulary/weak labels. Không train, không xác nhận SOTA, không có architecture winner.

| Mức bằng chứng | Điều hiện có | Điều chưa được phép suy |
|---|---|---|
| Đọc trực tiếp nguồn | Method/protocol/ablation và numerical contrasts trong casebooks | Chép đúng bảng không đồng nghĩa tái lập kết quả |
| Suy ra có giả định | Ví dụ resize/IoU, chain rule entropy; giới hạn chuyển task | Toy arithmetic không là empirical finding hoặc novelty theorem |
| Giả thuyết có phép thử | A–C, multi-view information gate, baseline và falsifier | Chưa có bằng chứng giải pháp mới thắng hoặc đủ venue band |
| Chưa biết | Prior sát từng claim, real-data failure, recipe implementation, hiệu quả trên miền mới | Không lấp bằng tên kiến trúc hay dự đoán AP |

Liên kết phần nghiên cứu trước: [bản đồ 13 mục tiêu](../t07-problem-map/PROBLEM-MAP.md), [120 câu hỏi](../t07-problem-map/QUESTION-BANK.md), [corpus 50 và độ sâu thực đọc](../t07-fresh-research/CORPUS-50.md). Chúng là dữ liệu đầu vào cho lượt tổng hợp này, không phải 50 kết quả đã được tái lập.

| Mã | Nguồn chính và nơi tra chi tiết |
|---|---|
| R02 | [QueryDet](https://arxiv.org/abs/2103.09136v2); CASEBOOK-STATIC §1 |
| N16 | [SuperYOLO](https://arxiv.org/abs/2209.13351v2); CASEBOOK-STATIC §2 |
| X01 | [UGS](https://openaccess.thecvf.com/content/ICCV2025/html/Sun_Uncertainty-Aware_Gradient_Stabilization_for_Small_Object_Detection_ICCV_2025_paper.html); CASEBOOK-STATIC §3 |
| G10 | [GauCho](https://arxiv.org/abs/2502.01565); CASEBOOK-STATIC §4 |
| N03 | [DynUAV](https://openaccess.thecvf.com/content/CVPR2026/html/Ye_Breaking_Smooth-Motion_Assumptions_A_UAV_Benchmark_for_Multi-Object_Tracking_in_CVPR_2026_paper.html); CASEBOOK-TEMPORAL-MASKS §2 |
| N04 | [HARD v2](https://arxiv.org/html/2609.18210v2); CASEBOOK-TEMPORAL-MASKS §3 |
| N05 | [DroneEyes v1](https://arxiv.org/html/2607.19857v1); CASEBOOK-TEMPORAL-MASKS §4 |
| N18 | [SOPSeg](https://openaccess.thecvf.com/content/CVPR2026F/html/Wang_Prompt-driven_Small_Object_Instance_Segmentation_in_Earth_Observation_CVPRF_2026_paper.html); CASEBOOK-TEMPORAL-MASKS §5 |
| MV01–03 | [Where2comm](https://proceedings.neurips.cc/paper_files/paper/2022/file/1f5c5cd01b864d53cc5fa0a3472e152e-Paper-Conference.pdf), [UCDNet v1](https://arxiv.org/html/2406.04648v1), [UAV3D](https://papers.neurips.cc/paper_files/paper/2024/file/643ea9b3843bd8f525ad8801437a2022-Paper-Datasets_and_Benchmarks_Track.pdf); MULTIVIEW-AND-CRITIQUE §3 |
| X04 | [Towards Streaming Perception](https://www.ecva.net/papers/eccv_2020/papers_ECCV/papers/123470460.pdf); prior từ lượt problem-map, không tính thêm vào 8 cases |
| BASE01 | [VisDrone official task definitions](https://github.com/VisDrone/VisDrone-Dataset); tham chiếu phân biệt image/video DET, SOT và MOT |
| BASE02 | [AI-TOD-v2 official dataset](https://chasel-tsui.github.io/AI-TOD-v2/); tham chiếu định nghĩa benchmark/annotation fixes, không audit dữ liệu |
| BASE03 | [OpenCV pinhole projection](https://docs.opencv.org/3.0-last-rst/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html); công thức nền, không empirical UAV claim |
| V01 | [CVPR 2026 Reviewer Guidelines](https://cvpr.thecvf.com/Conferences/2026/ReviewerGuidelines), mục Be Mindful/Be Specific, đọc 13/10/2026 |
| V02 | [Clarivate JCR basics](https://clarivate.libguides.com/jcr/basics); quartile/category, không venue-specific selection |

Mỗi claim quan trọng cần được đọc cùng điều kiện trong casebook, không tách một số khỏi dataset/task/input/training. JSON ledgers lưu source facts, author results, derived audits, inference và proposed tests để kiểm lại. Những ý tưởng A–C là **[design]**, chưa xác nhận novelty hoặc superiority.
