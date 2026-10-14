# T07 — Đọc sâu bốn trường hợp temporal và mask

**Ngày chốt:** 2026-10-13. **Scope:** UAV-view tiny objects; N03 DynUAV, N04 HARD, N05 DroneEyes/SkyAnchor, N18 SOPSeg/ReSOS. **Worker:** Sol/high; paper-method critique và paper-read think. Đầu vào: [EVIDENCE-UPDATE](../t07-problem-map/EVIDENCE-UPDATE.md), [evidence-update.json](../t07-problem-map/evidence-update.json); đọc tiếp PDF sơ cấp. Không triển khai model, train, benchmark hoặc chạy code tác giả. Không áp dụng trần tài chính. Các falsifier là **[design, cần thực nghiệm]**.

**Kết luận có thể bảo vệ:** temporal information, camera-motion compensation và crop trước tokenization có giá trị trong những protocol đã kiểm. Chưa có bằng chứng từ bốn bài rằng thêm memory/zoom luôn giúp mọi UAV tiny object, rằng một hệ thống đạt native camera rate, hoặc rằng chất lượng mask với box được cho sẽ chuyển nguyên vẹn sang automatic detection→segmentation. Bài học sâu là tách *sự hiện diện của vật thể, định danh, hình dạng và độ mới của output* trước khi suy cơ chế từ điểm tổng.

## 1. Phạm vi đã đọc và task thật

| Case | Nguồn/phiên bản | Đã đọc thực tế | Task và biên áp dụng |
|---|---|---|---|
| N03 | [DynUAV — CVPR 2026 PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Ye_Breaking_Smooth-Motion_Assumptions_A_UAV_Benchmark_for_Multi-Object_Tracking_in_CVPR_2026_paper.pdf) | Main body PDF pp.1–8: §1–6, toàn bộ Tables 1–5; xem hình Table 5 ở p.8. PDF có 10 trang, hai trang cuối là references; không audit bibliography/code. | UAV **MOT**, HBB + class + track ID; không phải SOT, không đo OBB/masks. |
| N04 | [HARD arXiv 2609.18210v2, 29/09/2026](https://arxiv.org/pdf/2609.18210v2), [HTML](https://arxiv.org/html/2609.18210v2) | Main body pp.1–7: §1–6, Tables 1–3, định nghĩa metric và text ablations; xem Table 3 p.7. PDF 9 trang; supplementary được main text dẫn nhưng **chưa đọc**. | DET/MOT/VQA trên UAV ultra-high-resolution; streaming MOT chính **Car, P=2s**, replicated workers để **không queue**. |
| N05 | [DroneEyes/SkyAnchor arXiv 2607.19857v1, 22/07/2026](https://arxiv.org/pdf/2607.19857v1), [HTML](https://arxiv.org/html/2607.19857v1) | Main body pp.1–13, §I–VI; Tables I–VII, equations/algorithm, results/ablations/limitations; xem p.8 để tách Tables III–V khỏi text extraction lỗi và kiểm Fig.6. PDF 14 trang, references bắt đầu p.13; không audit toàn bibliography. | Online **language-referring video segmentation** và object description; không đo MOT ID toàn cảnh. L1 cho target region; L2 tìm/segment mục tiêu theo query. |
| N18 | [SOPSeg/ReSOS — CVPR Findings 2026 PDF](https://openaccess.thecvf.com/content/CVPR2026F/papers/Wang_Prompt-driven_Small_Object_Instance_Segmentation_in_Earth_Observation_CVPRF_2026_paper.pdf) | Main body pp.1–8: §1–6, Tables 1–6, method/ablation/data provenance; xem Tables 1–3 p.6. PDF 10 trang; supplementary **chưa đọc**. | SOPSeg: **given-box→instance mask** trên remote-sensing ảnh tĩnh. ReSOS: teacher-generated masks rồi confidence/manual filtering; benchmark automatic instance methods riêng. Không mặc định UAV-video benchmark. |

Mức đọc trên vượt abstract/selected excerpt ở lượt trước, nhưng **không gọi “full paper + supplements + code audit”**. Text PDF và ảnh bảng kiểm tra lưu ở [sources](sources); tọa độ trang dưới đây là **PDF page**, không phải số proceedings in dưới chân trang. Số liệu là tác giả báo cáo, chưa tái lập. N04/N05 vẫn là preprint; N18 là Findings, không đổi nhãn thành main-track.

## 2. N03 DynUAV — Camera motion không chỉ làm khó association

### Failure và protocol

DynUAV thiết kế chuyến bay để phá giả định chuyển động êm: hovering/cruising, variable speed, rotation, zoom và orbital/fly-in/pull-away tạo apparent trajectory, scale/viewpoint changes và blur. DJI Mini 4 Pro, 1080p, độ cao 80–120m; 42 sequences, split 30/5/7 (§3.1–3.2, pp.2–3). Dataset có tám lớp gồm xe/người và phương tiện công nghiệp, cảnh campus/city-road/night. Không có extreme weather vì an toàn bay; tác giả cũng thừa nhận giới hạn scale dữ liệu (§3.1, pp.2–3).

Annotation bắt đầu khi vật thể **fully visible**; occluded vị trí vẫn được gán nếu suy được từ trajectory. Nhãn này đánh giá track continuity, không đồng nhất “visible detection at entry”. Quy trình initial/review/refinement kiểm box và ID (§3.1). Nhỏ ở đây được mô tả cả bằng **diện tích tương đối so frame** (§3.3/Table 2), không cung cấp một kết quả riêng đã xác minh cho toàn bộ vật thể dưới 16 pixel.

§4.1/p.5 dùng **YOLOv11** chung, train 100 epochs, input 1280×1280, RTX 4090; main text không chốt variant detector. Trackers dùng detections chung nhưng có ReID khác: OSNet/MSMT17 cho một nhóm; FastReID/MOT17 cho TrackTrack/AdapTrack. Vì vậy Table 3 so *pipelines/tracker implementations*, không là ablation sạch cho từng thành phần appearance/memory. §4 nói các số báo đều từ fine-tuned models; cross-dataset degradation Table 4 còn khác dữ liệu/protocol, không tự cô lập ego-motion.

### Hai phát hiện sâu

**TF01 — CMC có bằng chứng can thiệp trực tiếp, nhưng tác dụng phụ và tương tác tracker còn quan trọng.** §4.5/Table 5, pp.7–8 bật/tắt camera-motion compensation (CMC) với unified CMC parameters. Chuỗi tác giả đề xuất: camera-induced displacement → motion prediction/matching lệch → compensation ổn định association → ít ID switches. Với AdapTrack, **AssA 58.97→66.71, HOTA 56.99→62.33; FP 19,902→21,489**. Với U2MOT, **AssA 53.34→53.90, HOTA 50.95→51.47**; đây là hai cặp đại diện, cùng dataset/common detector và CMC intervention. Table 5 cho thấy tác dụng không đồng đều, dù direction association là dương trong ba tracker được thử.

Bằng chứng **đủ** cho “CMC toggle giúp các cấu hình này”; **mỏng** cho “CMC gain đo trực tiếp cường độ ego-motion” hoặc “FP tăng chắc do image warping”. Bài diễn giải warping artifacts và kết quả sequence-level ở Fig.5, nhưng main text không mô tả đủ warp implementation/stage để loại track birth/termination hoặc prediction/gap-filling như nguyên nhân FP. **Giải thích khác:** transform làm đổi matching và track survival, sinh thêm output tracks dù raw detector boxes không đổi. **Falsifier [design]:** cache cùng raw detections, khóa thresholds và track-management; đối chiếu no-CMC, estimated CMC và oracle camera transform, tách coordinate compensation khỏi image warping. Nếu association gain mất khi khóa track-management, claim compensation geometry là nguyên nhân chính cần hạ mức. Nếu FP tăng chỉ ở track extrapolation, bỏ giải thích ảnh warping. **Insight dùng được:** coi CMC là chẩn đoán ego-motion có điều kiện, không thêm nó như module “luôn tốt”.

**TF02 — Tiny, occlusion và motion cần phân rã; benchmark khó không chứng minh một nguyên nhân duy nhất.** §3.3 dùng adjacent-GT-box IoU, relative size và fragmentation để mô tả khó; §4.4/Fig.4 chỉ ra sequences 009/016 đồng thời có camera motion, occlusion và small objects. Adjacent-box IoU trộn object motion, camera motion, scale và pose; low IoU không riêng là camera dynamics. Authors đưa CMC ablation mạnh hơn so tracker tổng, nhưng “association bottleneck” cần giữ cùng phân bố visibility và raw detections. **Giải thích khác:** class/scene mix và nhãn occlusion khiến tracker có memory được thưởng dù ảnh lúc đó không chứa tín hiệu mục tiêu. **Falsifier [design]:** phân tầng trước theo absolute pixel size, occlusion và measured camera displacement; chạy oracle detection diagnostic cùng tracker/CMC. Nếu association gap mất khi detections hoàn hảo, vấn đề chính là observation/detection, không phải association model. **Insight:** cải thiện detector recall và giữ ID là hai câu hỏi; không dùng MOTA/HOTA đơn lẻ để quyết định cần zoom hay memory.

### Ablation causality

| Thành phần | Delta khi ablate | Kết luận nhân quả bài rút ra | Có kiểm soát? |
|---|---|---|---|
| CMC trong AdapTrack/TrackTrack/U2MOT | Table 5: association cải thiện khác mức; FP cũng tăng | Decouple camera jitter giúp motion prediction/association | **Có** cho toggle trong pipeline; implementation/stage chưa đủ rõ để tách warp artifacts với track management |
| Appearance, adaptive memory, uncertainty | Table 3 so tracker khác nhau, không bỏ từng module trong cùng tracker | Tác giả dùng kết quả để diễn giải ưu/nhược từng family | **Không** như component causality; khác ReID/pretraining/implementation |
| CMC gain theo scene | Fig.5 và §4.5: lợi ích lớn hơn ở một số cảnh động | Gain như proxy độ khó ego-motion | **Gián tiếp**; scene còn khác density/occlusion/size |

**Giới hạn suy luận của người đọc:** chưa thấy pixel-size-conditioned CMC ablation, noise/calibration test cho U2MOT hay detector-oracle decomposition trong main body. Không gọi đây là bằng chứng một thuật toán uncertainty nói chung thất bại.

## 3. N04 HARD — Độ mới của kết quả thay đổi kết luận về tracker

### Failure, metric và deployment policy

HARD giữ native detail trên 12768×9564 frames nhưng cần tiling; target nhỏ theo tỷ lệ vùng nhìn có thể còn nhiều pixel native. §3 nói tiny+small chiếm đa số và dùng relative area; không suy rằng đây là benchmark toàn vật thể vài pixel. Data hai sites, 21 sequences, năm test sequences; bốn lớp với car dominant. Annotation cùng HBB+ID dùng cho DET/MOT. Bài kiểm ba tasks riêng; VQA cross-frame identity findings không thay MOT evidence (§3–5).

§4/p.4 định nghĩa end-to-end latency gồm load, tile, detection, NMS và association. Default availability:

$$
k_t=\max\left(1,\left\lceil\frac{\Delta t_t}{P}\right\rceil\right).
$$

**[cited: N04 Eq.1]** Output của frame $t$ chỉ available tại $t+k_t$. Với **$P=2$ giây**, mỗi frame bắt đầu khi arrival; có **$K$ workers, mỗi worker là full replica của máy benchmark**, đủ để không frame nào queue và không contention. s-HOTA ghép current GT với latest available output, bỏ warm-up trước output đầu. Dù latency nhỏ, policy vẫn ít nhất một-frame lag; không gọi s-HOTA là offline HOTA ở latency zero. Queue/drop/jitter của single-device là policy khác, chưa được main benchmark này chứng minh.

### Ba phát hiện sâu

**TF03 — Tiling là can thiệp accuracy–latency thật, nhưng không tự chứng minh adaptive selector.** §5 Level 1/Table 2, pp.5–6 giữ tile input 640×640, COCO initialization; main configuration overlap 100px. Sweep overlap **0→150px** làm **mean AP 0.166→0.213**, tiles **300→520**, mean forward time **3.31→5.90s**. AP được average qua 20 detectors; time qua **18 detectors có timings trực tiếp**, không phải 20; time là Infer, không phải Total. Chuỗi tác giả: overlap cứu border-fragmented objects → AP tăng, nhưng tính nền lặp tăng. Native full-scene sparsity khiến phân bổ vùng có ý nghĩa, không phải bài đã thử mọi sparse/zoom policy.

**Giải thích khác:** overlap tạo nhiều candidates/views và đổi fusion, ngoài cứu truncation. **Falsifier [design]:** giữ unique scene pixels/model calls và fusion cố định, đối chiếu boundary-owned crops, duplicated-view control và overlap; nếu gain tồn tại chỉ khi duplicate scoring/merge đổi, bác giải thích boundary recovery là nguyên nhân đầy đủ. **Insight:** frame-level closure và biên crop cần đo; tiny theo relative frame size không bảo đảm thông tin sensor bị thiếu.

**TF04 — Offline winner có thể đảo dưới stale outputs; không từ đó suy appearance intrinsically gây hại.** §5 Level 2/Table 3, pp.6–7 dùng cùng detector với bốn tracker, official defaults; StrongSORT giữ sparse-optical-flow CMC, ba tracker khác không external compensation. Trên **Car/P=2s, TrackEval combined**, Faster R-CNN **ResNet-50** + StrongSORT có offline **HOTA 40.6** so ByteTrack **37.1**, nhưng s-HOTA **17.7** so **19.4**; end-to-end latency **15.85s** so **14.36s**. Đây là so thứ hai đại diện của N04. Whole-pipeline order đổi là bằng chứng trực tiếp, không phải phép đo ReID module riêng.

Tác giả cũng sweep frame interval giữ predictions cố định (§5 Finding 3): hợp lý cho effect của availability/evaluation, không mô phỏng lại detection/association khi *camera thật* quay ở cadence khác. **Giải thích khác:** reversal do latency bucket, CMC overhead/defaults, detector candidate statistics; không đủ gọi appearance features gây drift. **Falsifier [design]:** equalize measured latencies và CMC, toggle ReID trong cùng tracker; nếu order không đảo khi matched age, claim appearance-specific fragility cần bỏ. **Insight:** chọn pipeline theo timestamp và task, không theo offline HOTA hoặc detector FPS.

**TF05 — Association retention ratio cần absolute base và motion strata để đọc đúng.** §5 Finding 2/p.6 tự lưu ý DeepSORT giữ tỷ lệ AssA cao nhưng từ offline base thấp; retention cao không là robustness ngang model base tốt. Bài cũng thừa nhận cần vary appearance/CMC/motion separately để cô lập cơ chế. s-HOTA có quantization theo $P$, warm-up exclusion và hai-site/Car scope. **Giải thích khác:** low denominator hoặc motion/visibility mix tạo retention ratio “đẹp”; stale box cũng mất localization rồi làm association match khác. **Falsifier [design]:** report absolute DetA/AssA cùng paired degradation trên cùng scoring horizon, cùng age buckets và pre-registered motion strata. Nếu advantage retention mất khi base/horizon khớp, bác claim robustness theo ratio. **Insight:** kết luận “association chịu latency không đều” có cơ sở mô tả; “association là nguyên nhân duy nhất” vượt bằng chứng.

### Ablation causality và limits

| Thành phần | Delta khi ablate | Kết luận nhân quả bài rút ra | Có kiểm soát? |
|---|---|---|---|
| Tile overlap | Table 2/Fig.3d: quality và forward time cùng tăng | Border recovery và redundant compute | **Có** sweep pipeline; chưa tách duplicate views khỏi fusion effect |
| Frame interval trong evaluator | §5 Finding 3/Fig.4b: order thay khi predictions cố định | Load ratio quyết định streaming ranking | **Có** cho availability test; không là acquisition-rate experiment |
| ReID, CMC, motion model | Main §5 nói cần isolate; CMC ablation được dẫn supplementary | Appearance utility dưới latency | **Không** cho kết luận module trong phần đã đọc; supplement **chưa đọc**, không nhận là absent toàn bài |

Authors nêu hai hướng ở §6: giảm end-to-end latency và persistent cross-frame identity. Người đọc bổ sung **[suy luận]**: benchmark chưa chứng minh generalization sang mọi lớp, địa lý, native-high-FPS UAV, một thiết bị queue, hoặc frame-drop policy. Hardware/deployment details đầy đủ và CMC supplement chưa xác minh, nên không chuyển số latency thành cam kết thời gian thực cho hệ khác.

## 4. N05 DroneEyes/SkyAnchor — Giữ token, giữ identity và giữ output là ba việc

### Dữ liệu, formulation và mechanism chain

DroneEyes lấy Pexels drone videos native 1080p/4K; split 8:1:1 (§III/§V-A). Data engine: YOLO proposals tại keyframes → human verification → **SAM3 bidirectional propagation** → giữ high-confidence outputs → manual sampling inspection; descriptions từ VLM/context prompting rồi LLM refinement (§III-B, pp.3–4). Đây là teacher-generated/filter-verified masks, không phải mọi pixel mask vẽ tay. Không có detectable object bị loại; do đó đây không là benchmark đầy đủ negative-scene false alarms. Split isolation theo original video/duplicate scene chưa mô tả đủ trong phần đã đọc.

L1 mô tả target region có sẵn; L2 language-referring video mask. Method causal không dùng future frame, nhưng data annotation offline/bidirectional **không tự là inference leakage**: chỉ trở thành leakage nếu test input/model dùng annotation/future-frame state. Ngược lại, teacher selection có thể tạo annotation bias cần audit.

§IV-A–D/Algorithm 1: Qwen2.5-VL-3B ở anchor frames → Semantics-Aware Token Router → segmentation token → SAM2 mask decoder mỗi frame. Router **không thay số token theo từng vùng**: mỗi block $k\times k$ vẫn merge thành một token; softmax content weights thay cách aggregation, mask-supervised routing loss hướng salience. Nó giữ thông tin feature trước compression, không thu thêm sensor pixels/SR.

Semantic memory lưu permanent anchors; tracking memory FIFO recent spatial states. §IV-B Eq.4 tập semantic anchors chứa previous anchors; Eq.5 giới hạn tracking window. Main text chưa cho quy tắc prune/evict semantic anchors. **Chỉ tracking-memory bound là minh thị**; không suy toàn bộ storage/attention cost hằng số cho infinite stream. “Reference masks when available” tại VLM-side memory đòi kiểm prompt provenance nếu tái lập; không tự cho model GT masks ở L2 test.

Training §V-A: Qwen2.5-VL-3B + SAM2, LoRA r128/alpha256, general referring prealignment rồi DroneEyes/router stage; H800 benchmark. SAM2 memory và auxiliary routing supervision cũng là can thiệp, không chỉ “MLLM nhỏ hơn”.

### Ba phát hiện sâu

**TF06 — Router có replacement controls mạnh hơn so parameter count, nhưng không khôi phục tín hiệu đã mất.** Tables III/V và Fig.8 kiểm bỏ router/memory và thay Average Pooling/Pixel-Unshuffle, cùng architecture skeleton. Fig.8 có all-token control: near-quality-preserving compression là claim hợp với phép thử; lợi ích không đồng nhất detection gains từ native crop. **Giải thích khác:** auxiliary mask supervision/learnable projection cải thiện representation, không riêng semantic weighting; token quality phụ thuộc high-resolution encoder input. **Falsifier [design]:** khớp labels, projection capacity và input tokens; compare uniform pooling với auxiliary foreground loss, random weights và learned semantic weights; thêm native-vs-downsample conditions. Nếu uniform supervised control đạt tương đương, bỏ claim weighting-specific mechanism. **Insight:** tìm nút mất tiny signal trước khi compression; nhiều parameters không chữa đúng nút thắt.

**TF07 — Hai loại memory có vai trò khác nhau, song indefinite bounded streaming chưa được chứng minh.** Table IV/p.8, Token Router active ở mọi row: **no memory J&F 29.89 → tracking-only 35.76 → both 38.10**; cùng Qwen2.5-VL-3B/SAM2 và DroneEyes, benchmark H800. Đây là comparison đại diện thứ nhất. Semantic-only thiên về description; tracking-only tăng mask quality; both tốt nhất trong setup. Table III có factorial router×memory, mạnh hơn cumulative-only ablation. Fig.7/§V-D cho thấy thêm memory không mãi tăng quality; Fig.9 sweep anchor interval.

**Giải thích khác:** improvements từ SAM2 temporal smoothness và nhiều supervised observations, không chứng minh identity recovery sau occlusion/re-entry hoặc indefinite storage bound. **Falsifier [design]:** swap semantic anchors giữa distractors cùng lớp, compare repeated-frame vs real-history và pre-registered long-stream memory/latency traces; giữ tracking FIFO fixed. Nếu swapping không đổi target identity hoặc semantic storage tăng liên tục, hạ respective identity/bounded-memory claim. **Insight:** long-term “what” và short-term “where” là decomposition hữu ích, nhưng phải đo semantic-anchor growth và drift/recovery riêng.

**TF08 — Online là causal protocol; đạt deadline native-rate là claim khác.** Table II caption nói existing MLLM baselines **native offline**, SkyAnchor **online streaming**. FT variants giúp giảm training-data confound cho một số baselines nhưng không khớp future access/interface, visual prompting và schedule toàn bộ. Offline có thêm thông tin không tự khiến comparison công bằng: chưa trả lời online adaptation của baseline gần có đạt ngang không.

§V-F/Table VII, NVIDIA Jetson AGX Orin 64GB + DJI Matrice 4E: **vanilla 1.9 FPS → TensorRT/CUDA Graph/async VLM full system 5.8 FPS**. Đây là comparison đại diện thứ hai; là deployment chain/schedule, không isolate model reasoning improvement. Authors nói rõ **không intended cho high-speed closed-loop hoặc native-camera-rate**. Heavy VLM tại anchors, per-frame SAM2 path và async cached token giảm stall, nhưng output có thể dùng semantic anchor cũ.

**Giải thích khác:** throughput tăng do batching/kernel/static shapes hoặc stale conditioning, không đồng nghĩa vị trí hiện tại chính xác hơn. **Falsifier [design]:** giữ arrival timestamps và causal baseline adapters; đo capture-to-mask latency/age, sudden target entry, query change và occlusion recovery tại native stream, cùng compute/backend. Nếu update nhanh nhưng discovery/identity lag tăng, bác claim native-rate timely understanding, không bác claim latency-tolerant monitoring của tác giả. **Insight:** query-guided segmentation phù hợp operator assistance; chưa là closed-set detector mọi object hoặc điều khiển gimbal đã xác minh.

### Ablation causality và những số không nên trích như kết quả chắc

| Thành phần | Delta khi ablate | Kết luận nhân quả bài rút ra | Có kiểm soát? |
|---|---|---|---|
| Router × Memory | Table III có đủ bốn tổ hợp | Hai can thiệp bổ sung nhau | **Có** cho architecture rows; không tách router weights khỏi auxiliary labels/capacity |
| Semantic vs tracking memory | Table IV, router giữ active | Identity semantics và recent spatial history khác vai trò | **Có** module toggle; chưa direct identity-swap/recovery proof |
| Token compression/memory alternatives | Table V; Fig.8 | Thiết kế phù hợp tiny hơn alternatives | **Có** replacement; memory capacity/labels cần matched để claim cơ chế mạnh |
| Deployment optimization | Table VII cumulative chain | Efficient online output trên thiết bị thử | **Có** implementation chain; không isolate mọi interaction, không native-rate claim |

**Source anomaly:** Fig.6/p.8 có **bốn** methods và labels gain **8.9/4.8/5.9/2.1**, trong khi caption/prose nói ba models, prose smallest bins ghi **9.5/10.8**. Đơn vị relative-area bins cũng ghi `%`, cần kiểm evaluator/data trước đổi sang absolute pixels. Không dùng các per-size gain đó làm numerical evidence đã thống nhất. Table VII/§IV-D ghi BF16 engines nhưng §V-F giải thích FP16; precision thực thi cần xác minh, không tự sửa thành một loại.

Authors future work §VI: matching native capture rate, active camera/navigation và multi-target/compositional queries. **[Suy luận]** data teacher confidence filtering có thể loại hard tiny/occluded cases; SkyFind static maritime transfer không chứng minh temporal association dưới miền mới; permanent semantic anchors cần long-duration audit. Những caveat này giới hạn claim, không xóa bằng chứng module/deployment trong scope.

## 5. N18 SOPSeg/ReSOS — Crop cứu feature; prompt và teacher masks đặt biên kết luận

### Failure, mechanism và objective

SOPSeg nhắm information loss khi tiny object xuống SAM token grid thô. §3.1: lấy region quanh **provided instance box**, resize region về 256×256; region scale dựa vào max box side, tiny expansion và context control; position-embedding interpolation cho SAM encoder. Đây là **native local crop trước global downsampling + resize**, không physical zoom và không SR phục hồi chi tiết không có.

§3.2: horizontal box cộng ba orientation-derived points; với axis ambiguity, thử hai candidate axes và chọn mask theo predicted IoU. §3.3: edge token dự đoán biên song song mask, progressive refinement kết hợp shallow/deep features, ảnh và predictions nhiều scale. Mask/edge BCE+Dice và IoU Smooth-L1 cùng train; edge GT từ masks Gaussian-smoothed. Frozen **SAM-Large image/prompt encoders**, train decoder/refinement; §4.1 32 epochs, AdamW/cosine/batch24. Không là finetuning toàn backbone.

§4.1/p.5 viết rõ **bounding box provided**; iSAID train/eval với selected classes, NWPU-VHR10/SAT-MTB transfer. SAM-related baselines cũng box prompts/frozen encoder, UGBS dùng proposed RAM extraction (§4.2). Model mới nhận **oriented-derived points** ngoài HBB; additional prompt information cần được tính vào attribution, dù điểm được suy từ OBB chứ không người click riêng. iSAID không tự chứng minh UAV video tiny; khả năng chuyển là **[suy luận]**.

### Ba phát hiện sâu

**TF09 — RAM là thành phần lớn trong cumulative ablation; effect gồm scale và context.** Table 2/p.6: cùng base SAM decoder/frozen encoder, **SAM 71.65 → +RAM 79.40 → +RAM+OPM 81.69 → full EDE 82.96 mIoU**. Đây là comparison đại diện thứ nhất, given-box segmentation; không chuyển delta thành mask AP hoặc detection recall. Table 2 cô lập incremental gain trên predecessor, không full factorial interactions. Table 4/p.7 giữ setup và đổi crop expansion: **Tiny(max side<16px) k0=2 IoU 80.7 so k0=1.2 IoU 79.7**. Comparison thứ hai cho thấy mạnh hơn magnification không tự tốt hơn: k0 nhỏ thu ít context hơn.

**Giải thích khác:** benefits từ foreground centering/context distribution hoặc tránh global resize, không từ “new detail”; learned decoder tương tác crop. **Falsifier [design]:** match object pixels/input size, dịch object position và thay crop context; fixed-scale native crop với same context/labels đối chiếu RAM. Nếu nonadaptive matched crop đạt tương đương, hạ adaptive-policy claim nhưng giữ local-detail preservation insight. **Insight:** không tối đa zoom; kiểm mức context cần cho shape, nhất là với tiny không gian sát nhau.

**TF10 — OPM/EDE cải thiện conditional masks; deployment còn chịu prompt-box error.** Tables 2/5 và §3.2–3.3 hỗ trợ oriented prompts và refined boundaries trong given-box task. Table 5 thay decoder, chưa isolate edge-token/loss riêng với multiscale refinement/capacity. IoU-head chọn axis/mask chưa là uncertainty calibrated. **Giải thích khác:** oriented points cung cấp thêm geometry và oracle target localization; mask gain không phải perception tốt hơn khi detector thiếu object hoặc angle sai. **Falsifier [design]:** common noisy/predicted boxes với same oriented information cho baselines, sweep center/angle/size error và missing-target prompts, report detection→mask AP lẫn conditional IoU. Nếu conditional advantage biến mất hoặc pipeline misses chi phối, không claim automatic UAV tiny segmentation tốt hơn. **Insight:** chọn task before metric; supervision shape có giá trị nhưng phải kiểm detector–prompt–mask error chain.

**TF11 — ReSOS tạo tài nguyên lớn, đồng thời làm thay đổi population được đánh giá.** §5.1/p.8: SODA-A crops 512×512, SOPSeg teacher tạo mask từ OBB; bỏ **cả patch** nếu minimum predicted mask-IoU thấp hơn class threshold; manual low-quality masks đánh ignore. Thus pixel labels không mọi cái vẽ tay, filtering không chỉ xóa một mask xấu. §5.2/Table 6 train/eval automatic MaskDINO/Mask2Former/SparseInst bằng COCO AP, **khác SOPSeg given-box IoU benchmark**.

**Giải thích khác:** teacher shape prior và selection theo confidence làm hard samples/miền khó bị ít đại diện; model đo fit-to-teacher nhiều hơn independent boundary truth. **Falsifier [design]:** trước filtering lấy random size/scene-stratified patches, human redraw blind-to-teacher; so rankings/boundary errors trên corrected kept và rejected subsets. Nếu detector/segmenter ranking đổi hoặc errors concentrated ở removed patches, hạn chế claim general tiny segmentation trên ReSOS. **Insight:** provenance và rejected data cần là một phần kết quả; tài nguyên hữu ích không đồng nghĩa independent fully-manual GT.

### Ablation causality và source anomalies

| Thành phần | Delta khi ablate | Kết luận nhân quả bài rút ra | Có kiểm soát? |
|---|---|---|---|
| RAM→OPM→EDE | Table 2, cumulative rows | Mỗi stage nâng conditional segmentation | **Có** incremental, không full factorial |
| Context expansion/input resolution | Table 4/Fig.5 | Detail–context có optimum trong setup | **Có** parameter sweep; crop scale/context không tách độc lập |
| Decoder | Table 5 | Enhanced decoder giữ biên tốt hơn | **Có** decoder replacement; edge-only causality **không** cô lập |
| Prompt noise và teacher-mask independent audit | Không thấy trong main body | Không đủ kết luận robustness của automatic pipeline/GT | **Không** trong phần đã đọc; không khẳng định supplementary không có |

**Source anomalies:** Table 2 +RAM delta là **79.40−71.65=7.75pp**, prose §4.3 ghi **7.84%**; giữ table values và báo khác biệt. Table 1 SOPSeg Plane cell **86.63** nhưng Table 2 full row **80.63** trong PDF render; không chọn một số sửa hộ tác giả. Table 4/Table 5 All-IoU quanh 85 khác Table 2 class-mIoU 82.96; aggregation chưa giải thích đủ để trộn bảng. Không suy hai loại IoU là cùng statistic.

Authors không có standalone limitations section trong main body; §3.2 thảo luận axis ambiguity và §5.2 vẫn khó với một số small categories. **[Suy luận]** predicted prompt noise, confidence-filtered teacher GT và camera/video transfer là biên chưa được phần đã đọc chứng minh. Không nói model không có giá trị chỉ vì cần box; đó là một task hợp lệ, phải trình bày đúng.

## 6. Insight giữ được sau protocol audit

| Case | Bài học dương giữ được | Kết luận cần tránh | Alternative explanation quyết định |
|---|---|---|---|
| DynUAV | CMC trực tiếp giúp association trong pipelines thử; motion/occlusion/tiny stress đáng đo riêng | Tracker tốt chứng minh memory/uncertainty nói chung tốt; CMC gain là ego-motion meter độc lập | Track management, detector misses và annotation visibility |
| HARD | Frame-level tiling và output staleness có thể đổi ranking | Replicas-noqueue tương đương single-device FIFO; relative tiny = vài sensor pixels | Latency bucket/default CMC, base-score và scoring horizon |
| DroneEyes | Content-weighted compression và hai memory layers có conditional evidence; edge deployment được báo | Online = native-rate closed-loop; FIFO tracking bound = toàn memory bounded; referring mask = MOT | Auxiliary mask labels, stale semantic state, teacher filtering |
| SOPSeg | Crop trước mất detail giúp conditional tiny masks; context vừa đủ quan trọng | Given-box IoU = detection→mask AP; ReSOS = wholly manual GT; zoom lớn luôn tốt | Prompt geometry, local centering, teacher/patch selection |

Không cần multi-view để kiểm 11 phát hiện trên. Chọn nghiên cứu tiếp bằng **failure đã thấy + phép thử loại giải thích cạnh tranh**, không bằng ghép cả CMC, router, SR và mask head. Đây là casebook của bốn cases; không đại diện deep survey mọi trục của ngân hàng câu hỏi.

## 7. Reproducibility audit — tài liệu đủ để hiểu khác với runnable

| Case | Environment | Data | Training | Evaluation | Ablation causality | Code availability |
|---|---|---|---|---|---|---|
| N03 | partial: RTX4090, chưa versions/seeds/dependencies | partial: split/annotation có, release chưa download | partial: detector config cơ bản, tracker/ReID defaults | partial: metrics/common detector, visibility policy cần giữ | partial: CMC direct; tracker families confounded | partial: link repo tác giả có, chưa cài/chạy |
| N04 | partial: main latency policy rõ, machine details dẫn supplement chưa đọc | partial: sites/splits có, data chưa download | partial: tile/pretrain có, full schedules chưa xác minh | partial: Eq.1–3/Table3 rõ; supplement/hardware còn thiếu | partial: overlap và evaluator-P sweeps, CMC supplement chưa đọc | missing verification: chưa kiểm environment/code thực thi |
| N05 | partial: H800/Orin có, precision prose chưa thống nhất | partial: data-engine/split có, masks/split isolation chưa audit | partial: optimization/LoRA/loss có, full schedules/release chưa xác minh | partial: causal/offline scopes rõ, figure/prose anomalies | partial: factorial/replacements khá tốt; mask loss/capacity còn confound | missing verification: project page, chưa kiểm executable code |
| N18 | partial: main chưa đủ hardware/software/seeds | partial: selected classes/provenance có, split/masks release chưa audit | partial: optimizer/epochs/loss/frozen modules có | partial: given-box protocol rõ, aggregation/anomalies còn thiếu | partial: cumulative/decoder controls, prompt-noise chưa thấy | partial: source code link có, chưa cài/chạy |

**Phán quyết:** cả bốn **tái lập một phần từ tài liệu**, không được gán “runnable” hoặc “đã tái lập”. Blocker lớn: không xác minh code/data/deps và supplementary; benchmark conclusions có thể được đọc có điều kiện nhưng chưa có run độc lập. → Handoff root tích hợp 11 findings với cases không temporal; không yêu cầu triển khai hay training.

## Thuật ngữ

| English | Tiếng Việt | Nghĩa trong casebook |
|---|---|---|
| Ego-motion / CMC | Chuyển động camera / bù chuyển động camera | Tách apparent displacement do UAV khỏi object motion |
| Association | Gán danh tính qua thời gian | Không đồng nhất tìm được box mỗi frame |
| Output staleness | Độ cũ của output | Trạng thái được báo đến từ frame đã qua |
| Given-box segmentation | Segmentation với box được cho | Chất lượng mask có điều kiện target localization |
| Referring segmentation | Segmentation theo query | Tìm/segment target được mô tả, không mọi object trong scene |
| Conditional / factorial ablation | Ablation tăng dần / đầy đủ tổ hợp | Incremental effect khác module interaction độc lập |
| Teacher-generated labels | Nhãn do model tạo | Cần provenance và independent audit, kể cả có manual filtering |
