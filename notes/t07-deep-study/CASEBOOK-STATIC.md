# CASEBOOK-STATIC — Bốn case về nguyên nhân tiny-object detection

**Anchor:** UAV-view tiny object detection, trong chủ đề #7. **Worker:** evidence_sol, Sol/high. **Ngày:** 2026-10-13. **Phạm vi:** nghiên cứu phương pháp, thí nghiệm và cách phản biện; không triển khai detector, không training, không xếp hạng venue. Mọi kết quả dưới đây là tác giả báo cáo, chưa tái lập độc lập. Các phép thử đề xuất là **[design]**, chưa thực hiện.

Trước khi đọc nguồn, đã dùng corpus R02/G10, N16 trong evidence-update và X01 trong ROOT-SOURCES. Lượt này nâng mức đọc lên **method + experiments + ablations + stated limitations**, nhưng không tự nhận đọc toàn bộ references, audit official code hoặc kiểm chứng mọi chứng minh. Trang ghi dưới đây là **PDF page index bắt đầu từ 1**; số proceedings được thêm khi hữu ích.

## 1. R02 — QueryDet: dùng tính thưa để chi trả cho feature resolution

**Nguồn:** [CVPR 2022 / arXiv v2](https://arxiv.org/abs/2103.09136v2). File cache `notes/t07-fresh-research/sources/resolution/R02.pdf`, 10 trang, metadata CVPR; văn bản R02.txt. Đã đọc §3.1–3.4 p.3–5, §4.1–4.5 p.5–8, Table 1–9, Fig.2–5 và conclusion p.8. ArXiv v2 sửa ngày 24/03/2022; file cache là bản CVF có số proceedings 13668–13677, không tuyên bố hai file byte-identical.

### Task và vấn đề trung tâm

Phát hiện HBB ảnh tĩnh trên COCO và VisDrone; VisDrone là bằng chứng trực tiếp từ UAV, còn COCO là transfer. Vấn đề bài giải là **chi phí detection heads trên feature map phân giải cao**, không phải tạo thêm dữ liệu quan sát. Backbone và FPN vẫn tạo dense feature maps. Nhận diện vị trí thô ở coarse scale đủ để quyết định phần high-resolution head nên tính, ngay cả khi coarse scale chưa đủ để định vị box chính xác.

### Cơ chế từng bước

1. Backbone/FPN tạo nhiều mức, bổ sung mức nông P2 để giữ tín hiệu nhỏ.
2. Query head học heatmap objectness cho vật thể nhỏ từ box centers bằng focal loss. Ngưỡng small được gắn với anchor scale hoặc regression range của từng mức.
3. Inference chọn điểm coarse có query score vượt ngưỡng; ánh xạ sang các vị trí con ở mức fine.
4. Tạo sparse value features, tính classification/regression/query heads ở các vị trí đó và context quanh chúng.
5. Cascade query tiếp tục xuống mức fine, tránh việc mọi coarse query lan xuống toàn bộ cây.
6. Training vẫn dùng detector losses và thêm query supervision; **reweight loss giữa FPN levels** vì thêm P2 thay đổi số lượng và phân bố training samples.

Query threshold, starting layer và context window cùng quyết định quality–runtime. Không có camera thứ hai, geometry multi-view hoặc frame history trong cơ chế này. [§3; §4.4]

### Hai đối chiếu định lượng đã kiểm tra

| Điều kiện | So sánh đọc từ bảng | Phạm vi kết luận |
|---|---|---|
| COCO mini-val, RetinaNet R50, default 1× schedule; loss/sample setup §4.1 | Table 3: baseline **37.46 AP**, thêm HR-only **36.10 AP** | Resolution cao đơn độc có thể giảm AP khi training distribution đổi; không phải định luật HR luôn hại |
| VisDrone val, RetinaNet R50; train ảnh tách thành bốn patch không overlap, 50k iterations, mixed precision; query threshold 0.15/start P4 | Table 2: QueryDet dense HR **28.35 AP / 1.16 FPS** → CSQ **28.32 AP / 2.75 FPS** | CSQ giữ gần như toàn bộ quality của cùng HR model trong setup này; timing 2080Ti không chứng minh onboard streaming |

§4.1 nêu optimizer/schedule và GPU; input resize cụ thể cho Table 2 không được khóa rõ ngay trong đoạn đã đọc, do đó không suy rộng FPS ra resolution khác.

### Ablation có thể và không thể cô lập

| Thành phần | Delta khi ablate | Kết luận nhân quả bài rút ra | Có kiểm soát? |
|---|---|---|---|
| HR/P2 | Table 3 HR-only làm AP giảm | Nhiều samples ở tầng nông cần reweight | Có can thiệp trực tiếp; giải thích sampling cần kiểm tra sâu hơn bằng thống kê |
| Loss rebalance | Table 3 có RB-only và HR+RB | RB hữu ích hơn khi thêm HR | Có, gần thiết kế factorial; chưa tách mọi normalization/assignment choice |
| Query-head training | HR+RB so với thêm QH | Auxiliary objectness supervision cải thiện detector | Có; gain quality không thuộc riêng sparse inference |
| CSQ | Dense QueryDet so với CSQ | Chủ yếu tăng tốc inference với mất AP nhỏ | Có, đối chiếu chất lượng/compute trực tiếp |
| Start level/context/query operator | Table 4–6 | Có điểm cân bằng; quá coarse khó tìm target, quá nhiều context tốn thời gian | Có sweeps trên COCO; không chứng minh quy luật trên mọi UAV density |

**Hạn chế tác giả nêu:** query có thể tìm đúng rough position nhưng detection head vẫn định vị thất bại; query kích hoạt nhầm large-object regions làm inference chậm. Sparse-map construction overhead khiến starting ở mức rất coarse không hiệu quả. [§4.4–4.5]

**[suy luận] Giải thích cạnh tranh có tính quyết định:** tổng AP gain có thể chủ yếu do P2 + rebalance + auxiliary labels; nếu gom tất cả thành “query giúp nhìn thấy tiny tốt hơn”, đã gán nhầm nguyên nhân. CSQ không tái tạo target đã mất trước feature extraction; độ thưa cũng có thể giảm khi cảnh dày.

**Nguyên lý chuyển cho UAV tiny:** coarse representation có thể đủ cho **where-to-compute** mà chưa đủ cho **what/precise-box**. Tuy nhiên selector recall là cổng giới hạn; feature sparsity không đồng nghĩa pixel acquisition tốt hơn.

**[design] Phép thử bác bỏ tối thiểu:** giữ nguyên checkpoint HR QueryDet, so dense heads với CSQ và GT-oracle query. Phân tầng theo object pixel size/density/blur; đo missed-by-selector, missed-after-selector và end-to-end latency gồm sparse construction. Nếu oracle vẫn không cứu nhóm khó, selector không phải bottleneck; nếu sparsity mất lợi ích ở density cao, claim phải giới hạn theo cảnh.

**Tái lập:** [official repo](https://github.com/ChenhongyiYang/QueryDet-PyTorch) đã đọc README, chưa chạy. Repo hiện có cập nhật AMP/spconv/config, nên cần commit pin tương ứng bản báo cáo. Checklist: Environment **partial**, Data **partial**, Training **partial**, Evaluation **partial**, Ablation causality **partial**, Code availability **partial**. Blocker lớn nhất: khóa preprocessing/resize, sparse implementation và timing protocol trước khi chuyển claim speed sang phần cứng khác.

## 2. N16 — SuperYOLO: HR supervision ở training, LR inference

**Nguồn:** [arXiv 2209.13351v2](https://arxiv.org/abs/2209.13351v2), 14 trang; tải vào `notes/t07-deep-study/sources/N16.pdf/.txt`. PDF tự ghi **pre-acceptance version**; liên quan IEEE TGRS 2023, DOI 10.1109/TGRS.2023.3258666. Đã đọc p.3–6 §III–IV, p.7–13 §V–VI/Table I–VIII; xem trực tiếp ảnh p.10 Table V–VI. Không gọi bản đọc này là final publisher PDF.

### Task, dữ liệu và vấn đề trung tâm

HBB detection ảnh remote sensing nhỏ; VEDAI có RGB/IR cùng scene, không phải multi-camera multi-view. Main setup giữ tám lớp sau loại classes quá ít mẫu; labels chuyển sang YOLOv5 HBB, xác nhận cả [official README](https://github.com/icey-zhang/SuperYOLO). Có thí nghiệm single-modal DOTA/NWPU/DIOR; không tự dùng chúng làm proof trực tiếp cho UAV RGB video hoặc OBB.

### Cơ chế từng bước

1. Chọn YOLOv5s làm baseline; bỏ Focus để tăng feature resolution sớm.
2. Pixel-level MF chuẩn hóa RGB/IR, dùng channel/spatial weighting và trộn đối xứng trước backbone.
3. Từ native HR image tạo LR input bằng bilinear downsampling; training reconstruction target vẫn là HR.
4. SR auxiliary branch nhận low/high-level backbone features, hợp nhất và reconstruct HR; detection và reconstruction cùng tối ưu backbone.
5. Bỏ SR branch khi inference; detector nhận LR input.
6. Riêng VEDAI final small-object configuration bỏ PANet và hai scale heads; single-modal datasets có vật thể lớn thì giữ lại chúng. [§IV; Table V; §V-F]

Đây là **privileged HR supervision ở training**, không phải inference SR-image preprocessing, không phải multi-frame SR. SR branch không tạo một quan sát quang học mới lúc test.

### Hai đối chiếu định lượng đã kiểm tra

| Điều kiện | So sánh | Giới hạn |
|---|---|---|
| VEDAI first-fold ablation, YOLOv5s-noFocus; train/test LR 512, SR training có HR target 1024; 300 epochs, SGD, batch 2 | Table IV: noFocus **69.5 mAP50** → noFocus+SR **78.0 mAP50**, inference GFLOPs cùng **20.4** | Cùng inference budget; chưa loại generic auxiliary-training/privileged-target explanation |
| VEDAI, final SuperYOLO, average 10 folds; §V-B cùng SGD/schedule và HBB labels | Table VII: RGB **72.49 mAP50**, RGB+IR **75.09 mAP50** | RGB tự thân đã hoạt động; thêm IR hỗ trợ trong dataset này, không chứng minh multi-view là điều kiện bắt buộc |

First-fold ablation không được trộn với final 10-fold result. Larger-model headline comparison thay đồng thời head configuration, modalities và supervision, nên không dùng làm attribution riêng cho SR.

### Ablation và chỗ diễn giải dễ quá tay

| Thành phần | Delta khi ablate | Kết luận nhân quả bài rút ra | Có kiểm soát? |
|---|---|---|---|
| Focus removal | Table II có/không Focus | Giữ feature resolution giúp small targets | Có; compute cũng tăng mạnh, nên chưa là equal-compute causal proof |
| MF vs concat/feature fusion | Table III | Pixel fusion của họ tốt trong setup VEDAI | Có đối chiếu; không chứng minh mọi feature-fusion family kém |
| SR vs upsample | Table V | Learned reconstruction có lợi hơn upsampling control | Có; chưa matched generic auxiliary task/target control |
| Bỏ large-scale heads/PANet | Table V | Giảm tham số/compute phù hợp VEDAI | Có; đây là task-specific architecture tuning, không quy tắc chung cho multi-scale UAV |
| EDSR/L1 | Table V các row cộng dần | Reconstruction design cùng góp lợi ích | Có sequential ablation; chưa đầy đủ factorial cho interactions |

**Hạn chế tác giả nêu hoặc thừa nhận:** đổi input scale giữa train/test làm quality giảm; thiếu labeled multimodal datasets; final SOTA comparison có khác biệt pretraining ở YOLOFusion; future work là HR-feature extractor nhẹ hơn. [Table IV; §V-E/F; §VI]

**[suy luận] Giải thích cạnh tranh có tính quyết định:** auxiliary loss + thêm HR target có thể regularize representation thay vì thực sự phục hồi chi tiết vật thể không quan sát được. Focus là pixel rearrangement/space-to-depth, không tự động xóa mọi raw pixel; tăng feature resolution/đổi stride và receptive field sau bỏ Focus là một confound. Không diễn đạt lợi ích thành “information bị Focus phá rồi SR lấy lại” khi chưa có phép đo.

**Audit nguồn:** Fig.2 caption nói MSE; §IV-D mô tả L1; Table V có row so lựa chọn loss. Với tái lập phải khóa **row/config** chứ không tự chọn một đoạn. Prose §V-F gọi result tối ưu nhưng Table VIII có detector khác cao hơn trên DOTA; không tái sử dụng claim thắng mọi dataset.

**Nguyên lý chuyển:** learning objective có thể giúp tận dụng quan sát LR mà không tăng inference pixel count. Cần phân biệt **training supervision tốt hơn** với **test-time information mới**. Multimodal là khác nguồn phổ; multi-view là khác viewpoint/geometry.

**[design] Phép thử bác bỏ tối thiểu:** giữ backbone/heads/noFocus/input và training steps cố định, so SR với generic auxiliary reconstruction có cùng HR target/compute và với HR teacher distillation. Thêm test degradation thật thay vì chỉ bilinear LR. Nếu lợi ích SR mất sau matched auxiliary control, kết luận đúng là supervisory signal hữu ích, chưa đủ rằng SR-specific mechanism là nguyên nhân.

**Tái lập:** official repo có labels HBB conversion và SR/non-SR commands; chưa kiểm code/config/seed end-to-end. Checklist cả sáu tiêu chí **partial**. Blocker: exact fold membership, reconstruction loss/weight, HR–LR generation, one-head/multi-head config và bản pre-acceptance cần đối chiếu final paper.

## 3. X01 — UGS: thay mục tiêu localization; tách empirical gain khỏi lập luận gradient

**Nguồn:** [ICCV 2025 main PDF](https://openaccess.thecvf.com/content/ICCV2025/papers/Sun_Uncertainty-Aware_Gradient_Stabilization_for_Small_Object_Detection_ICCV_2025_paper.pdf), 11 trang, `notes/t07-deep-study/sources/X01.pdf/.txt`; [supplement](https://openaccess.thecvf.com/content/ICCV2025/supplemental/Sun_Uncertainty-Aware_Gradient_Stabilization_ICCV_2025_supplemental.pdf), 2 trang, X01-supp.pdf/.txt. Đã đọc main p.1–8 §1–5/Table 1–7, supplement p.1–2; nhìn PDF main p.3–5 và p.8. Chưa đọc references p.9–11 hoặc audit implementation.

### Task và cơ chế

HBB localization/detection trên VisDrone, COCO, VOC; có rotated detection SODA-A. VisDrone là bằng chứng UAV-view trực tiếp, SODA-A là remote sensing OBB, không cho phép gộp HBB và OBB metrics.

Tác giả đặt khó khăn localization tiny một phần ở gradient instability, minh họa bằng gradient maps và curvature analysis. Cơ chế gồm:

1. Chuyển coordinate regression targets sang discrete grids và soft targets ở hai bins lân cận.
2. IN spacing đặt grid dày gần zero để targets tiny/offset nhỏ có biểu diễn hữu ích.
3. Classification localization loss học probability distributions; decode coordinate bằng expectation.
4. UM entropy minimization làm distribution tập trung hơn.
5. UR perturb features theo hướng entropy sensitivity, rồi tối ưu refinement để chịu perturbation.
6. Kết hợp CE, UM và layer-wise UR với loss weights. [§3.2]

Không phải uncertainty calibration cho quyết định deployment, không phải Gaussian geometry head như GauCho.

### Hai đối chiếu định lượng đã kiểm tra

| Điều kiện | Bảng | Kết quả và cách đọc |
|---|---|---|
| Faster R-CNN R50, VisDrone val, input 1333×800, batch16, 1× SGD; không multiscale, §4.1.2 | Table 1/Table 6 | L2 baseline **21.3 AP** → full UGS **24.2 AP**. Đây là empirical package gain |
| Cùng Faster R-CNN R50/VisDrone ablation | Table 6 | CE **22.1 AP** → CE+IN **22.5 AP**. Delta IN phải đọc từ row reference này, không lấy delta prose so với L2 |

DINO có schedule/augment khác; không trộn Table 1 DINO với generic 1× SGD setup. Table 6 cho hyperparameter sweeps nhưng không cung cấp repeated-seed uncertainty trong các đoạn đã đọc.

### Ablation và giới hạn nhân quả

| Thành phần | Delta khi ablate | Kết luận nhân quả bài rút ra | Có kiểm soát? |
|---|---|---|---|
| CE localization | Table 6 so L2/Smooth-L1/IoU/gradient clipping | Classification-based objective cải thiện quality | Có; head dimension/parameterization cũng đổi |
| IN | CE vs CE+IN | Discretization hữu ích | Có; không tự chứng minh imbalance là nguyên nhân duy nhất |
| UM | Sweeps λ, IN giữ bật | Entropy penalty đóng góp | Có conditional effect; entropy giảm chưa là calibration đúng |
| UR | Thêm UR/sweep γ và ρ | Refinement đóng góp | Có; thiếu random-perturbation hoặc matched adversarial-objective control trong bảng |
| Gradient statistics | Fig.6, §4.6 và supplement convergence | UGS đi cùng gradient variance thấp hơn | Đo quan hệ hỗ trợ cơ chế; không tách gradient rescaling/coordinate/head effects |

### Audit toán và ngôn ngữ, không kết án empirical results

**[derived audit] Main Eq.(13), p.5/printed 8411:** derivative entropy được ghi theo logits nhưng biểu thức vế phải là derivative trực tiếp theo probability. Với probability sinh từ softmax cần chain rule. Một sanity check độc lập: ở logits bằng nhau, distribution uniform có entropy cực đại nên đạo hàm entropy theo logits bằng zero; biểu thức in không thỏa điều đó. Đã nhìn trực tiếp PDF, nên không quy cho extraction lỗi. Không chép biểu thức đó như công thức đúng.

**[derived audit] Coordinate mismatch:** supplement §1 ghi curvature L2 theo normalized target là hằng số, rồi mới ánh xạ sang pixel coordinate và xuất hiện anchor-size factor. So curvature theo pixel với CE gradient theo logits chưa tự chứng minh optimizer/network-parameter Hessian ổn định hơn. Jacobian từ feature→logits/coordinates, assignment, normalization và loss scaling còn tham gia.

**[derived audit; chưa kiểm tra độc lập] IoU derivation:** worker tự đối chiếu main Eq.(6–7) và supplement Eq.(8–10) với định nghĩa negative-log IoU ở cùng đoạn; nhận thấy supplement Eq.(8) có dạng derivative của negative IoU thay vì negative-log IoU. Nhận định này chưa có agent/người khác hoặc numerical check xác nhận độc lập. Các hệ số/sign cần re-derive trước khi sử dụng inverse-width exponent như định luật. Không trích công thức này làm bằng chứng định lượng về full-network curvature.

**Hạn chế tác giả nêu:** future work mở sang video hoặc multimodal; các thí nghiệm ở đây chưa chứng minh hai mở rộng đó. [Conclusion p.8] **[suy luận]** Không có calibration test, coverage/risk, uncertainty ranking dưới domain shift trong Tables 1–7 đã đọc; entropy minimization có thể làm sai dự đoán tự tin hơn nếu nhãn/appearance mơ hồ.

**Giải thích cạnh tranh có tính quyết định:** AP gain có thể đến từ distributional coordinate representation, grid design và regularization/adversarial augmentation; gradient visualization giảm có thể phản ánh gradient scale thay đổi. Package AP gain không đủ chọn một trong các nguyên nhân này.

**Nguyên lý chuyển:** tiny khó định vị vì coordinate tolerance nhỏ và supervision/parameterization nhạy; nhưng phải so đạo hàm trên **cùng biến**, không chỉ so hai loss expressions khác hệ tọa độ. Uncertainty useful-for-training không tự thành uncertainty reliable-for-action.

**[design] Phép thử bác bỏ tối thiểu:** trước hết kiểm derivative theo định nghĩa; sau đó dùng cùng backbone, assignment, target normalization và head capacity, so CE+IN, CE+IN+UM/UR và matched gradient-rescale/random perturbation controls. Gradient statistics phải đo cùng layer/parameter coordinates và conditioning. Nếu AP gain tồn tại mà instability measure không đổi hoặc matched rescaling đạt tương đương, lý giải “gradient stabilization là nguyên nhân đặc thù” bị yếu đi; AP result vẫn có giá trị.

**Tái lập:** Environment/Data/Training/Evaluation/Ablation **partial**; Code availability **missing trong nguồn đã đọc** (không tuyên bố toàn internet không có code). Main không dẫn code URL; chưa tìm được official release trong kiểm tra nguồn. Blocker chính: math/implementation alignment của entropy, UR loss definition và normalization; thêm α/β/n khác RPN/R-CNN, λ/γ/ρ phải khóa theo Table 6–7.

## 4. G10 — GauCho: biểu diễn liên tục không tạo thêm hướng không quan sát được

**Nguồn:** [CVPR 2025 / arXiv record](https://arxiv.org/abs/2502.01565). Cache `notes/t07-fresh-research/sources/geometry/G10.pdf/.txt`, 10 trang, CVF accepted version với proceedings 3593–3602. Đã đọc p.1–8: §3.1–3.4, §4/Table 1–3, §5/Fig.3–4 và conclusion; nhìn trực tiếp Table 2 p.7. Không audit supplement proof, code hay pretrained checkpoints.

### Task và vấn đề trung tâm

Oriented object detection với FCOS, RetinaNet, R3Det, RoI Transformer trên DOTA/HRSC/UCAS-AOD. DOTA gồm satellite/aerial imagery; HRSC là Google Earth ships; đây không phải mặc nhiên UAV-view tiny benchmark.

Bài phân biệt hai vấn đề: tham số box/góc có boundary discontinuity; và hình dạng không xác định orientation duy nhất. Gaussian loss trên OBB head chưa loại bỏ tất cả discontinuity. Regress Gaussian trực tiếp có thể giúp tối ưu nhưng Gaussian isotropic từ square box không giữ semantic direction.

### Cơ chế từng bước

1. Biến GT OBB thành Gaussian mean/covariance theo center, kích thước và orientation.
2. Head dự đoán mean offsets và ba Cholesky parameters; diagonal positive qua exponential, off-diagonal có sign.
3. Dùng bounds liên hệ shape scale với feature stride/anchor dimensions để parameterize head cho anchor-free/anchor-based.
4. Tối ưu bằng Gaussian losses GWD/KLD/ProbIoU; detector và các default MMRotate configs giữ tương ứng.
5. Decode covariance qua eigendecomposition thành OBB hoặc oriented ellipse. Isotropic Gaussian→circle tự nhiên; angle OBB không khôi phục duy nhất. [§3]

Covariance ở đây là **spatial extent/shape representation**, không phải predictive error covariance hay epistemic confidence.

### Hai đối chiếu đã kiểm tra

| Điều kiện | Kết quả | Phạm vi |
|---|---|---|
| FCOS R50, DOTA-v1.5, single-scale train/test; 12 epochs/default MMRotate/random flips; same ProbIoU loss | Table 2: OBB head **64.26 AP50** → GauCho **65.09 AP50** | Head representation có lợi trong cấu hình này; không chứng minh tiny-specific/all-detector gains |
| FCOS HRSC, cả OBB/GauCho dùng ProbIoU; test thêm rotations 1°–360°, train HRSC 72 epochs, flip/rotation policy §4 | §5/Fig.4: average orientation error **1.36°** → **1.11°** | Geometrically oriented ships; không áp dụng semantic orientation của near-square planes |

### Ablation / comparison có và không có

| Thành phần | Delta khi ablate | Kết luận nhân quả bài rút ra | Có kiểm soát? |
|---|---|---|---|
| Head OBB→GauCho | Table 1 nhiều detector/loss; Table 2 FCOS | Biểu diễn mới tương thích và có thể cải thiện | Có matched head substitution; gains không đồng đều mọi detector/loss |
| Gaussian loss choice | Table 1–2 GWD/KLD/ProbIoU | Tương thích nhiều losses | Có; chưa tách parameterization scaling khỏi continuity |
| OBB→OE evaluation | Table 1 UCAS-AOD | OE bớt nhạy near-square ambiguity | Metric/representation cùng đổi; không coi AP tăng là localization vật lý tốt hơn |
| Orientation consistency | HRSC rotation sweep Fig.4 | Góc ổn định hơn cho elongated objects | Có same-loss comparison; domain hẹp |
| Cholesky/bounds riêng | Không thấy component-removal table | Có lý thuyết/thiết kế | Không cô lập thực nghiệm từng phần |

**Hạn chế tác giả nêu:** square-like OBB decoding vẫn ambiguous; semantic direction của planes/helicopters không lấy lại từ ellipse; một số head differences có thể do random seed. DOTA-v1.5 chỉ báo FCOS vì anchor settings tiny cho detector khác không có trong benchmark. Họ giữ default hyperparameters và không tune riêng GauCho. [§3.4; §4–5]

**[suy luận] Giải thích cạnh tranh có tính quyết định:** gain AP nhỏ có thể do optimization scaling/seed chứ không chỉ continuity. Nếu đổi OBB evaluation sang ellipse, đã đổi câu hỏi được đánh giá; score tăng không nhất thiết có thêm thông tin orientation. Việc làm covariance positive-definite không đồng nghĩa confidence được hiệu chuẩn.

**Nguyên lý chuyển:** representation nên phản ánh thông tin có thể xác định từ target. Tiny elongated vehicle có geometric axis; tiny near-square object có thể không có axis đáng tin; semantic heading là nhiệm vụ khác cần appearance evidence. Không gán angle loss cho hình tròn như có orientation vật lý duy nhất.

**[design] Phép thử bác bỏ tối thiểu:** cùng backbone/loss/assignment/postprocessing/OBB metric và nhiều seeds; phân tầng size, aspect ratio, geometric vs semantic orientation, blur. Giữ metric cố định để so head. Nếu lợi ích biến mất sau matched scaling hoặc không tập trung quanh các discontinuity cases, continuity chưa là nguyên nhân xác lập; semantic-heading failure không được “giải” bằng đổi metric ellipse.

**Tái lập:** [official repo](https://github.com/jhlmarques/GauCho) có thể truy cập, chưa chạy; sáu checklist đều **partial**. Blocker: pin MMRotate configs, Gaussian scale factor theo loss, anchors, augmentation, decoder/evaluator OBB/OE và seed. Main có tables nhiều regimes; multiscale SOTA table không phải controlled head-only comparison.

## 5. Sáu kết luận chuyển giao, có điều kiện và có thể bác

1. **Feature resolution và effective training balance là cặp phải xét cùng nhau.** QueryDet HR-only giảm AP trong ablation; SuperYOLO noFocus đổi resolution/compute. [R02 Table 3; N16 Table II] **[suy luận]** Không chẩn đoán “thiếu pixel” chỉ bằng AP tăng sau thêm tầng nông; trước hết kiểm positive/negative counts, loss weights và gradients theo scale.
2. **Rough location có thể dễ hơn precise localization.** QueryDet gate tìm được vị trí mà final head vẫn miss. [R02 §4.5] **[suy luận]** Tách gate recall khỏi downstream recall là insight chẩn đoán, không thêm một module attention cho mọi case.
3. **Training-only privileged information khác test-time sensing.** SuperYOLO HR reconstruction supervision bị bỏ khi infer; IR vẫn là input của multimodal model. [N16 §IV/V] **[suy luận]** Multi-view chỉ đáng cân nhắc khi quan sát thứ hai giải ambiguity/occlusion cụ thể. Bốn bài này không chứng minh multi-view cần thiết, cũng không chứng minh nó vô ích.
4. **Coordinate system quyết định cách hiểu “gradient lớn”.** UGS supplement phân biệt normalized và physical coordinates; CE đổi biến đầu ra. [X01 supplement §1; main §3] **[derived/suy luận]** So gradient phải cùng biến/layer/normalization; nhỏ gradient không tự là tốt convergence.
5. **Một distribution không tự là uncertainty dùng được.** GauCho covariance mô tả hình học; UGS entropy mô tả coordinate distribution trong training. [G10 §3; X01 §3.2] **[suy luận]** Calibration, correct error ranking và benefit của uncertainty-guided decisions cần thí nghiệm riêng.
6. **Output/metric phải khớp what-is-observable.** GauCho không khôi phục heading của isotropic near-square objects; ellipse evaluation đổi target geometry. [G10 §3.4/§5] **[suy luận]** Với UAV tiny, cần phân biệt box extent, semantic category, geometric orientation và semantic heading, rồi mới chọn objective.

## 6. Self-critique và cổng kiểm chứng

Đây là bốn case có chủ đích, không comprehensive literature review. Không suy novelty từ thiếu một ablation hoặc từ không thấy code link. Tất cả decisive experiments là proposal chưa chạy; không dự đoán AP gain. Phần UGS audit là suy luận toán kiểm từ công thức in và supplement; cần authors/code clarification trước khi kết luận implementation sai. Phần Focus criticism là reasoning về phép rearrangement, chưa audit exact code path. Các claims về runtime không được nâng thành video/streaming guarantee; không có multi-view comparison trong bốn case.

Machine ledger `static-claims.json` tách **author_result**, **source_fact**, **derived_audit**, **inference**, **proposed_test**. Mọi numerical comparison khóa dataset, detector, table và training regime. Không đánh đồng chép đúng số với tái lập đúng số.

## Thuật ngữ

| English | Tiếng Việt | Ý nghĩa |
|---|---|---|
| Feature resolution | Độ phân giải đặc trưng | Số vị trí trên feature map; khác native sensor information |
| Privileged supervision | Thông tin đặc quyền ở huấn luyện | HR/teacher signal có khi train, không có cùng signal ở inference |
| Selector recall | Recall của bộ chọn | Tỷ lệ target được gate cho phép xử lý tiếp |
| Parameterization | Cách tham số hóa | Biến network dự đoán và phép decode sang hình học |
| Predictive calibration | Hiệu chuẩn dự đoán | Confidence có khớp xác suất lỗi quan sát; chưa chứng minh bởi covariance/entropy đơn thuần |
| Decoding ambiguity | Nhập nhằng giải mã | Nhiều hướng OBB tương ứng cùng isotropic Gaussian |
