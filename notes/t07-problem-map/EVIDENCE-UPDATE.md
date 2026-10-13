# T07 — Evidence update: mở rộng bản đồ vấn đề

Ngày kiểm tra: **2026-10-13**. Worker: evidence_sol (Sol/high). Anchor duy nhất: **Multi-scale Aerial Object Detection and Segmentation (#7)**. Bổ sung **18 nguồn sơ cấp**, không thay lựa chọn kiến trúc hoặc xếp hạng phương án. Corpus cũ `notes/t07-fresh-research/corpus-50.csv` và `REPORT.md` được dùng để tránh trùng; giới hạn bốn tuần/60 USD trong báo cáo cũ **không áp dụng** cho lượt này.

**Mức bằng chứng:** đọc chọn lọc nguồn, không đọc/audit toàn văn mọi bài. Có 12 hồ sơ vượt mức chỉ abstract (bao gồm official dataset description), 6 hồ sơ abstract; không train, chạy benchmark hay xác minh kết quả độc lập. Mỗi “đã làm” dưới đây nghĩa là **tác giả đã thiết lập hoặc báo cáo trong phạm vi được ghi**, không phải bài toán được giải hoàn toàn. Câu hỏi còn lại đều đánh dấu **[suy luận]**, không xác lập novelty hoặc tuyên bố chưa ai thử. JSON song hành chứa title đầy đủ, năm/status, URL, task, mechanism, scope, depth và locator.

## Phân biệt bài toán trước khi tổng hợp

| Nhánh | Dữ liệu/nhãn đúng | Nguồn | Tránh suy rộng |
|---|---|---|---|
| Phát hiện video / MOT từ UAV | Box từng frame; MOT cần track ID | N01, N03, N04 | Accuracy từng ảnh không chứng minh giữ ID hoặc đáp ứng deadline |
| Tracking một mục tiêu | Target khởi tạo/template; box theo thời gian | N02, N06 | SOT không đo phát hiện mọi mục tiêu và association nhiều ID |
| Segmentation có ngôn ngữ | Query + mask từng frame, causal stream | N05 | Không đồng nhất với closed-set automatic instance segmentation |
| Semantic scene perception | Nhãn lớp từng pixel/point, pose | N07 | Không suy thành instance masks hoặc MOT identities |
| Multimodal oriented detection | RGB/IR OBB riêng + condition labels | N08 | Không mặc định modalities đăng ký hoàn hảo |
| Prompted instance masks | Given box → mask; nguồn mask có thể teacher-generated | N18 | mIoU với box có sẵn khác mask AP của detector→segmenter |
| Video camera tĩnh trên cao | Box; wind/rain/haze | N14 | Chỉ transfer; không đại diện camera UAV ego-motion |

## Sổ bằng chứng bổ sung

### N01 — [UAVDT](https://arxiv.org/abs/1804.00518) (2018)

**Task:** UAVDT; aerial RGB video DET/SOT/MOT; vehicle boxes + attributes. **Status/depth:** ECCV 2018; selected_full_text.
**Đã làm:** Benchmark chung ba nhiệm vụ và đánh giá theo thuộc tính quan sát. Đã cung cấp dữ liệu xe từ UAV, box và các thuộc tính như thời tiết/độ cao/occlusion; không cung cấp instance masks.
**Câu hỏi:** [suy luận] Khả năng phát hiện xe nhỏ và giữ ID thay đổi thế nào khi độ cao, mật độ và camera motion cùng biến đổi?
**Locator:** CVF PDF Introduction, pp.1–2; https://openaccess.thecvf.com/content_ECCV_2018/papers/Dawei_Du_The_Unmanned_Aerial_ECCV_2018_paper.pdf.

### N02 — [UAV123 / UAV20L](https://ivul.kaust.edu.sa/benchmark-and-simulator-uav-tracking-dataset) (2016)

**Task:** Aerial RGB SOT; upright box; long-term UAV20L subset. **Status/depth:** ECCV 2016; official UAV123/UAV20L dataset page; official_dataset_description.
**Đã làm:** Benchmark tracking một mục tiêu; có biến thể giảm frame rate. Nhãn upright boxes và các protocol UAV123/UAV20L/UAV123_10fps đã được mô tả trên trang chính thức; đây không phải bài toán tìm mọi vật thể/giữ nhiều ID.
**Câu hỏi:** [suy luận] Thiếu frame và biến đổi tỷ lệ làm mất một mục tiêu đã khởi tạo khác với làm mất nhiều mục tiêu mới xuất hiện ra sao?
**Locator:** Official dataset page Details and Resources; publication ECCV 2016.

### N03 — [DynUAV](https://openaccess.thecvf.com/content/CVPR2026/html/Ye_Breaking_Smooth-Motion_Assumptions_A_UAV_Benchmark_for_Multi-Object_Tracking_in_CVPR_2026_paper.html) (2026)

**Task:** DynUAV; aerial RGB MOT; HBB + category + frame + track ID. **Status/depth:** CVPR 2026; selected_full_text.
**Đã làm:** Benchmark chủ động tạo ego-motion, đổi viewpoint/scale, blur và cảnh đêm. Tác giả kiểm tra nhiều tracker; nhãn giữ vị trí trong occlusion khi có thể suy từ trajectory. Dataset có nhiều nhóm xe/người nhưng không có extreme-weather do an toàn bay.
**Câu hỏi:** [suy luận] Bao nhiêu lỗi do detector bỏ sót và bao nhiêu do association khi UAV đổi hướng/zoom mạnh, đặc biệt sau occlusion?
**Locator:** PDF §3.1–3.3 pp.2–3; §4.2–4.3/Table 3 p.6; downloaded and extracted with pypdf.

### N04 — [HARD / s-HOTA](https://arxiv.org/abs/2609.18210v2) (2026)

**Task:** HARD; ultra-high-resolution aerial DET/MOT/VQA; HBB + identity + QA. **Status/depth:** arXiv preprint 2609.18210v2, revised 2026-09-29; peer review not established; selected_full_text.
**Đã làm:** Đánh giá toàn pipeline tiling/fusion/association và metric s-HOTA tính tuổi kết quả. Kết quả tác giả: ranking offline có thể đổi khi tính latency. MOT streaming thí nghiệm chính trên Car, frame interval 2s; policy mặc định dùng các worker máy đầy đủ nhân bản để không queue.
**Câu hỏi:** [suy luận] Kết luận về pipeline còn giữ khi một thiết bị phải queue/drop frame, có jitter và deadline thay đổi?
**Locator:** https://arxiv.org/html/2609.18210v2 §3, §4, §5 Level 1/2; Table 1–3; default availability policy Eq.1.

### N05 — [DroneEyes / SkyAnchor](https://arxiv.org/abs/2607.19857v1) (2026)

**Task:** DroneEyes/SkyAnchor; aerial online language-referring video segmentation; masks + query/description. **Status/depth:** arXiv preprint 2607.19857v1, submitted 2026-07-22; peer review not established; selected_full_text.
**Đã làm:** Token router giữ tín hiệu mục tiêu nhỏ; semantic memory và tracking memory; VLM chạy anchor frames, SAM2 chạy mỗi frame. Tác giả có ablation router/memory, cross-domain và deployment Jetson AGX Orin 64GB. Baselines MLLM trong Table II dùng native offline mode; tác giả nói chưa phù hợp high-speed closed-loop/native frame rate.
**Câu hỏi:** [suy luận] Multi-target referring, active camera control và memory khi mục tiêu tái xuất hiện cần đánh giá thế nào với cùng causal protocol?
**Locator:** https://arxiv.org/html/2607.19857v1 §IV-A/B/C; Table II; §V-D/E/F; §VI future work.

### N06 — [MUST / UNTrack](https://openaccess.thecvf.com/content/CVPR2025/html/Qin_MUST_The_First_Dataset_and_Unified_Framework_for_Multispectral_UAV_CVPR_2025_paper.html) (2025)

**Task:** Aerial multispectral SOT; spectrum/template/search; not generic MOT. **Status/depth:** CVPR 2025; First là từ trong title, không xác minh priority độc lập; abstract_and_intro.
**Đã làm:** UNTrack học spectral-spatial-temporal features và cập nhật spectrum prompt. Tác giả cung cấp MUST và báo cáo cải thiện trên tracking; setup theo dõi một target có template ban đầu, không chứng minh detection mọi đối tượng hay MOT.
**Câu hỏi:** [suy luận] Lợi ích phổ còn giữ khi co-registration sai, band bị mất, hoặc chuyển sang phát hiện/tracking nhiều mục tiêu tiny?
**Locator:** CVF Abstract; PDF p.1 Introduction: https://openaccess.thecvf.com/content/CVPR2025/papers/Qin_MUST_The_First_Dataset_and_Unified_Framework_for_Multispectral_UAV_CVPR_2025_paper.pdf.

### N07 — [UAVScenes](https://openaccess.thecvf.com/content/ICCV2025/html/Wang_UAVScenes_A_Multi-Modal_Dataset_for_UAVs_ICCV_2025_paper.html) (2025)

**Task:** Frame-wise camera/LiDAR semantic segmentation; poses; depth/localization/NVS. **Status/depth:** ICCV 2025; abstract.
**Đã làm:** Bổ sung nhãn semantic từng frame và LiDAR vào MARS-LVIG, kèm pose 6-DoF. Đã mở benchmark scene perception trên camera và 3D points; abstract không xác lập benchmark tiny instance masks hoặc MOT IDs.
**Câu hỏi:** [suy luận] Hình học/pose giúp segmentation mục tiêu nhỏ bao nhiêu khi depth thưa và camera chuyển động?
**Locator:** CVF Abstract and task list.

### N08 — [ATR-UMOD / PCDF](https://openaccess.thecvf.com/content/ICCV2025/html/Chen_Fusion_Meets_Diverse_Conditions_A_High-diversity_Benchmark_and_Baseline_for_ICCV_2025_paper.html) (2025)

**Task:** ATR-UMOD; aerial RGB-IR OBB; per-image condition labels. **Status/depth:** ICCV 2025; selected_full_text.
**Đã làm:** PCDF dùng condition text prompts và task-oriented gating; condition-decoupling module hỗ trợ khi không có condition annotation. RGB/IR có OBB được gán riêng sau homography/crop và timestamp alignment. Bao phủ độ cao/góc/thời tiết/ánh sáng/cảnh; đánh giá PCDF trên ATR-UMOD.
**Câu hỏi:** [suy luận] Reliability gating có giữ lợi ích với sai lệch đăng ký, modality hỏng và tổ hợp điều kiện chưa thấy?
**Locator:** PDF §3.1–3.3 pp.3–4; §4.1 overview; CVF Abstract; downloaded/extracted with pypdf.

### N09 — [PointSR](https://openaccess.thecvf.com/content/CVPR2025/html/Li_PointSR_Self-Regularized_Point_Supervision_for_Drone-View_Object_Detection_CVPR_2025_paper.html) (2025)

**Task:** Point-supervised aerial object detection; pseudo boxes. **Status/depth:** CVPR 2025; selected_method_excerpt.
**Đã làm:** MIL pseudo-box prediction; dynamic anchor ratios + informative negative sampling. Đánh giá trên DroneVehicle/UAVDT/VisDrone. Temporal-Ensembling Encoder gom pseudo-box shape qua epoch/iteration huấn luyện, KHÔNG phải tổng hợp frame video.
**Câu hỏi:** [suy luận] Nhãn point lệch/tập object thiếu ảnh hưởng recall và calibration khác với box supervision thế nào?
**Locator:** CVF PDF §4.2 Temporal-Ensembling Encoder; Fig.3, printed p.11710; source-search excerpt explicitly states each epoch.

### N10 — [OpenRSD](https://openaccess.thecvf.com/content/ICCV2025/html/Huang_OpenRSD_Towards_Open-prompts_for_Object_Detection_in_Remote_Sensing_Images_ICCV_2025_paper.html) (2025)

**Task:** Open-prompt RS object detection; HBB and OBB. **Status/depth:** ICCV 2025; abstract.
**Đã làm:** Multimodal prompts, multi-task detection heads và multi-stage training. Tác giả báo cáo đánh giá nhiều public datasets và inference real-time trong setup của họ; abstract không chứng minh uncertainty-calibrated unknown rejection cho mọi miền.
**Câu hỏi:** [suy luận] Tiny novel classes và prompts mơ hồ ảnh hưởng localization/false alarms thế nào khi địa lý, scale và tên lớp đổi đồng thời?
**Locator:** CVF Abstract, model/task/experimental scope paragraphs.

### N11 — [Active-DDC](https://openaccess.thecvf.com/content/ICCV2025/html/Sun_Dual_Domain_Control_via_Active_Learning_for_Remote_Sensing_Domain_ICCV_2025_paper.html) (2025)

**Task:** Sequential domain-incremental RS detection; known categories; replay memory. **Status/depth:** ICCV 2025; selected_full_text.
**Đã làm:** Active Learning Example Replay chọn sample; Active Domain Shift Control căn chỉnh DETR queries bằng optimal transport. Thử HRRSD/LEVIR/DIOR/DOTA, prune classes để khớp miền; Table 1 và sequence ablations. Không gọi kết quả thắng trên từng dataset: table có baseline cao hơn ở một số cột.
**Câu hỏi:** [suy luận] Retention và forward transfer còn giữ khi không có nhãn miền mới hoặc xuất hiện novel classes, khác protocol class-pruned hiện tại?
**Locator:** PDF §3.1–3.2 p.3; §4.1–4.2/Table1–3 p.6; downloaded/extracted with pypdf.

### N12 — [LLM-assisted sparse labels](https://openaccess.thecvf.com/content/ICCV2025/html/Liao_LLM-Assisted_Semantic_Guidance_for_Sparsely_Annotated_Remote_Sensing_Object_Detection_ICCV_2025_paper.html) (2025)

**Task:** Sparsely annotated RS object detection; unlabeled instances/images. **Status/depth:** ICCV 2025; abstract.
**Đã làm:** LLM semantic priors, class-aware dense pseudo-label assignment và hard-negative reweighting. Tác giả báo cáo thí nghiệm DOTA và HRSC2016 với sparse annotations. Sparse missing labels khác sai nhãn lớp hoặc box lệch.
**Câu hỏi:** [suy luận] Priors/ngưỡng confidence tạo confirmation bias nào với rare classes và vùng nhỏ bị bỏ nhãn có hệ thống?
**Locator:** CVF Abstract, mechanism and named evaluation datasets.

### N13 — [LEGNet](https://openaccess.thecvf.com/content/ICCV2025W/SEA/html/Lu_LEGNet_A_Lightweight_Edge-Gaussian_Network_for_Low-Quality_Remote_Sensing_Image_ICCVW_2025_paper.html) (2025)

**Task:** Low-quality RS detection; image degradations. **Status/depth:** ICCV 2025 workshop SEA; không phải main conference paper; abstract.
**Đã làm:** Orientation-aware Scharr edges và Gaussian-prior feature refinement. Tác giả đánh giá DOTA-v1.0/v1.5, DIOR-R, FAIR1M-v1.0, VisDrone2019; không suy rằng đã xử lý hết real sensor degradation hoặc temporal blur.
**Câu hỏi:** [suy luận] Edge enhancement giữ được vật thể thật hay khuếch đại noise/aliasing khi tiny objects chỉ còn ít pixel?
**Locator:** CVF Abstract: EGA subcomponents and five-benchmark scope.

### N14 — [Nano-VID-weather / TYOLOv8](https://openaccess.thecvf.com/content/WACV2025W/RWS/html/van_Lier_Evaluation_of_Spatio-Temporal_Small_Object_Detection_in_Real-World_Adverse_Weather_WACVW_2025_paper.html) (2025)

**Task:** Nano-VID-weather; STATIC elevated ground camera video; small-object HBB detection. **Status/depth:** WACV 2025 workshop RWS; transfer source; selected_dataset_excerpt.
**Đã làm:** Đối chiếu spatial YOLOv8, temporal TYOLOv8, 3FN; haze augmentation. Có video weather thực Wind/Rain/Haze; weather subsets chủ yếu camera tĩnh trên cao. KHÔNG dùng làm aerial-view/ego-motion benchmark.
**Câu hỏi:** [suy luận] Temporal cues vừa giúp tiny targets vừa tăng false motion từ mưa/gió; điều gì đổi khi camera UAV cũng chuyển động?
**Locator:** PDF §3.1 Dataset: static cameras mounted at 30m, weather subsets; publisher/CVF Abstract.

### N15 — [MessDet](https://openaccess.thecvf.com/content/ICCV2025/html/Wu_Measuring_the_Impact_of_Rotation_Equivariance_on_Aerial_Object_Detection_ICCV_2025_paper.html) (2025)

**Task:** MessDet; static aerial oriented detection. **Status/depth:** ICCV 2025; selected_analysis_excerpt.
**Đã làm:** Strict-equivariant downsampling/backbone/neck, channel attention và multi-branch head. DOTA-v1.0/v1.5/DIOR-R; §5.4 dùng cùng head để kiểm tra rotated validation và equivariance. Rotation robustness có bằng chứng cụ thể, không phải giả thuyết hoàn toàn mới.
**Câu hỏi:** [suy luận] Equivariance còn hữu ích bao nhiêu với continuous scale/viewpoint change, interpolation và low-quality tiny targets?
**Locator:** PDF §5.4 Analysis printed p.7336/Fig.5–6; primary excerpt verified; official repo also checked.

### N16 — [SuperYOLO](https://arxiv.org/abs/2209.13351v2) (2023)

**Task:** Multimodal RS small-object detection; assisted SR feature learning. **Status/depth:** IEEE TGRS 2023; arXiv2209.13351v2 2023-04-08, related DOI supplied; abstract.
**Đã làm:** Compact multimodal fusion và SR branch học high-resolution representation từ low-resolution input. SR branch bỏ ở inference; tác giả báo cáo VEDAI trade-off. Khác pipeline dựng ảnh SR rồi detect và khác video SR nhiều frame.
**Câu hỏi:** [suy luận] Lợi ích đến từ thông tin phổ, auxiliary supervision hay phục hồi chi tiết; có giữ khi degradation thật khác LR training?
**Locator:** arXiv Abstract and related DOI 10.1109/TGRS.2023.3258666.

### N17 — [RSSOD / MCGR](https://arxiv.org/abs/2111.03260v1) (2022)

**Task:** RSSOD; satellite image SR-assisted detection; hand-labeled instances. **Status/depth:** Expert Systems with Applications 2022; arXiv2111.03260v1 submitted 2021-11-05; abstract.
**Đã làm:** MCGR super-resolution model với auxiliary YOLOv5 detection; joint benchmark. Tác giả cung cấp RSSOD với nhiều tần suất lớp và real geometric distortions; abstract báo SR/detection metrics nhưng chúng không chứng minh causal video restoration.
**Câu hỏi:** [suy luận] Pixel fidelity, object geometry và downstream recall có đồng biến khi restoration hallucinate texture hoặc shift miền sensor?
**Locator:** arXiv Abstract; journal ref and related DOI 10.1016/j.eswa.2022.116793.

### N18 — [SOPSeg / ReSOS](https://openaccess.thecvf.com/content/CVPR2026F/html/Wang_Prompt-driven_Small_Object_Instance_Segmentation_in_Earth_Observation_CVPRF_2026_paper.html) (2026)

**Task:** SOPSeg/ReSOS; prompted aerial small-instance masks; supplied box input. **Status/depth:** CVPR Findings 2026; distinct from main-track proceedings; selected_full_text.
**Đã làm:** Region-adaptive magnification, orientation point prompts, edge-aware progressive decoder. §4.1 đánh giá GIVEN bounding box→mask trên iSAID rồi NWPU-VHR10/SAT-MTB. ReSOS masks sinh từ SODA-A OBB và manual filtering, không phải mọi mask vẽ thủ công.
**Câu hỏi:** [suy luận] Lỗi detector/prompt box lan sang mask thế nào; dataset teacher-generated có thiên lệch đánh giá cùng loại model không?
**Locator:** PDF p.2 ReSOS provenance; §3.2 pp.4–5; §4.1 p.5 provided box protocol; downloaded/extracted with pypdf.

## Cách dùng bằng chứng để hình thành câu hỏi rộng

- **Quan sát và tích lũy thông tin:** xác định khi nào thêm độ phân giải, thông tin phổ hoặc frame history giúp còn khi nào chỉ thêm tín hiệu không đáng tin. N04/N05/N06/N08/N16/N17 cung cấp các protocol khác nhau; không cộng headline improvements giữa chúng.
- **Khả năng giữ mục tiêu theo thời gian:** cần tách detector recall, association/ID continuity và mask boundary stability. N03 cho ego-motion; N04 cho tuổi kết quả; N05 cho causal referring masks. Memory không đồng nghĩa mọi frame được xử lý đúng deadline.
- **Tổng quát hóa:** open-prompt recognition (N10), sequential domain adaptation (N11), degradation robustness (N13/N14) và rotation equivariance (N15) là các cơ chế/prior khác nhau. “Robust” phải kèm loại shift, dữ liệu train và điều kiện test.
- **Nhãn và tính tin cậy:** point labels (N09), sparse/missing annotation (N12), masks do teacher sinh (N18) và calibration lỗi prompt là các vấn đề khác nhau. Thí nghiệm cần phân biệt thiếu nhãn, sai lớp, box lệch và mask boundary không chắc chắn.

## Audit trước handoff

Các trường JSON đều có locator nguồn; các câu hỏi được đánh dấu suy luận. Không có numerical performance delta trong tài liệu này. Thông số protocol như frame interval của HARD dùng để giới hạn claim. Hai preprint 2026 khóa version trước ngày chốt. LEGNet/Nano-VID-weather ghi workshop, SOPSeg ghi Findings. Không lặp X01 UGS/X02 Point2RBox-v2/X03 HOTA/X04 streaming perception mà root đang quản lý.

**Các giới hạn cần giữ khi trích:** N04 benchmark hai site và thí nghiệm MOT streaming chính Car; default policy giả định worker replicas để không queue. N05 baseline offline và proposed online có protocol khác nhau, chưa phù hợp control tốc độ cao; chưa kiểm tra download/release mọi dataset. N11 Table1 không hỗ trợ diễn đạt thắng từng dataset. N14 camera tĩnh. N18 prompted given box và mask provenance. Độ tin cậy: cao cho định danh/loại task/đoạn đã đọc; trung bình cho kết quả tác giả báo cáo; câu hỏi là suy luận cần kiểm tra.
