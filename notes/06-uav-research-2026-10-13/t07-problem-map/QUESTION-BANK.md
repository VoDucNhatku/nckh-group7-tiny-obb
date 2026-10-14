# T07 — Ngân hàng câu hỏi nghiên cứu mở rộng

**Phạm vi:** đề tài gốc #7, *Multi-scale Aerial Object Detection and Segmentation*. **Worker:** paper-synthesize, mode expand; question-generation agent. **Ngày:** 2026-10-13. **Nguồn:** [REPORT](../t07-fresh-research/REPORT.md), [corpus-50.csv](../t07-fresh-research/corpus-50.csv), [INDEX](../../INDEX.md). Bỏ ràng buộc tài chính khi xây bản đồ; tính khả thi dữ liệu và phép đo vẫn cần xác minh.

**120 câu hỏi dưới đây đều là [design, cần thực nghiệm].** Chúng là đề xuất kiểm tra, không phải 120 khoảng trống đã được chứng minh, không phải lời khẳng định tác giả chưa giải quyết. Corpus gốc hiện có 39 bài ở mức abstract/metadata, 10 bài đọc chọn lọc phương pháp/thí nghiệm, 1 bài qua trích đoạn publisher. Các neo nguồn cho biết dòng nghiên cứu liên quan; không chứng minh từng câu hỏi chưa có prior. Đã đối chiếu 18 hồ sơ N-series trong [EVIDENCE-UPDATE](EVIDENCE-UPDATE.md): 12 hồ sơ vượt abstract, 6 hồ sơ abstract; không cộng thành 18 full-method audits. X-series đối chiếu tại [ROOT-SOURCES](ROOT-SOURCES.md). Cần audit prior gần trước khi tuyên bố novelty, kể cả khi đã có nguồn đúng task. Không giữ H1 như hướng mặc định.

## Cách dùng ngân hàng

Mỗi câu hỏi có mã Q001–Q120 và một kiểu chính: **CD** chẩn đoán, **CC** cơ chế, **BG** biên giới/bác bỏ, **DG** đánh giá, **UD** ứng dụng. Quy trình chọn: **task → triệu chứng lỗi → nguyên nhân cạnh tranh → phép thử phân biệt → đối chứng → metric → giới hạn kết luận**. Hai câu hỏi chỉ khác tên model hoặc dataset không được coi là hai đóng góp. Có thể gộp các câu thuộc cùng một chuỗi nhân quả thành một nghiên cứu.

Phân biệt task trước khi dùng metric:

| Task | Đầu ra và thông tin cho phép | Metric cần khớp |
|---|---|---|
| Still-image detection | HBB/OBB của một ảnh độc lập | AP/AR theo chuẩn evaluator và nhóm kích thước |
| Video object detection | Box mỗi frame; có thể dùng lịch sử, không tự có ID | AP video/frame, độ ổn định, thời gian phát hiện; công bố causal/offline |
| MOT | Box và ID của nhiều vật thể qua thời gian | HOTA, IDF1, DetA/AssA và độ trễ theo protocol |
| SOT | Theo một mục tiêu được khởi tạo, thường bằng box | Success/AUC, precision, failure và recovery theo benchmark |
| Semantic segmentation | Nhãn lớp mỗi pixel, không phân biệt cá thể | mIoU và metric biên theo lớp |
| Instance segmentation | Mask riêng cho mỗi cá thể | Mask AP, split/merge, metric biên; box AP nếu có |
| Interactive segmentation | Mask khi được cung cấp prompt của người dùng | Chất lượng theo số/lượng prompt; không so trực tiếp với tự động |

“Zoom” có bốn nghĩa cần giữ riêng: **crop từ ảnh gốc** giữ các pixel gốc trước khi toàn ảnh bị resize; **digital interpolation** phóng to cùng tín hiệu bằng nội suy; **learned super-resolution (SR)** suy đoán chi tiết từ prior; **physical sensor zoom** thay đổi quang học/khoảng cách/cách lấy ảnh và có thể thay đổi GSD, FOV, blur, thời gian. Không quy lợi ích của bốn thao tác cho cùng một nguyên nhân.

## A. Thông tin quan sát, độ phân giải và bốn nghĩa zoom — Q001–Q010

**Neo:** R04 SAHI, R10 AdaZoom, R13 Dynamic Zoom-in, F06 Visual Accommodation, S07 Scale-MAE, D06 FAIR1M; N13 LEGNet cho low-quality detection, N16 SuperYOLO và N17 RSSOD/MCGR cho SR-assisted detection. SuperYOLO dùng SR auxiliary branch bỏ khi inference, không đồng nhất dựng ảnh SR rồi detect. Joint SR–detection đã có tiền lệ; câu hỏi đặt vào native/synthetic/physical information và đối chứng. **Physical zoom là mở rộng thăm dò**, chưa có prior trực tiếp đủ trong corpus gốc.

1. **Q001 · CD:** Với vật thể rất nhỏ, lỗi chủ yếu do thiếu pixel gốc, blur hay cách resize; tách từng yếu tố trên cùng cảnh có đổi thứ tự khó của mẫu không?
2. **Q002 · CC:** Giữ FOV và kích thước đầu vào tương đương, native crop, nội suy, learned SR và physical zoom thay đổi recall, định vị và phân loại khác nhau ở những mức pixel nào?
3. **Q003 · DG:** Đường đáp ứng chất lượng theo số pixel/vật thể có giống nhau khi thay GSD thật và khi downsample nhân tạo; nếu khác thì benchmark synthetic scale đại diện đến đâu?
4. **Q004 · BG:** Có lớp vật thể mà phóng to tăng confidence nhưng không tăng thông tin phân biệt hoặc precision; kiểm tra distractor giống hình có bác lợi ích của zoom không?
5. **Q005 · CC:** SR giúp nhờ phục hồi cấu trúc quan sát hay nhờ sinh texture hợp prior; đổi prior SR và dùng ảnh thật đồng đăng ký có phân biệt được hai giải thích không?
6. **Q006 · CD:** Blur do chuyển động và aliasing do lấy mẫu gây lỗi tương tự hay khác nhau; detector có phục hồi sau crop trong cả hai trường hợp không?
7. **Q007 · BG:** Khi vật thể chỉ còn vài pixel, có ngưỡng mà thêm độ phân giải suy luận không giúp vì tín hiệu gốc đã mất; ngưỡng đó phụ thuộc contrast/shape ra sao?
8. **Q008 · DG:** Định nghĩa “vật thể nhỏ” bằng diện tích pixel, chiều ngắn, GSD hay kích thước vật lý dự báo lỗi tốt hơn trên nhiều cảm biến?
9. **Q009 · CC:** Anti-aliasing trước resize giúp detection nhờ giảm nhiễu hay làm mất chi tiết có ích; hiệu ứng đổi theo mật độ và hướng vật thể thế nào?
10. **Q010 · UD:** Với physical zoom, khi nào FOV hẹp làm bỏ sót mục tiêu mới nhiều hơn số mục tiêu đang thấy được nhận rõ hơn; cần đo recall theo toàn vùng quan sát thế nào?

## B. Scale, receptive field và ngữ cảnh — Q011–Q020

**Neo:** B01 FPN, R03 CEASC, R06 RFLA, S07 Scale-MAE, S05 RS-SAM; N15 MessDet đã trực tiếp đối chiếu strict/approximate rotation equivariance, có same-head controls (§5.4 trong evidence update). FPN, context và equivariance đều có tiền lệ; Q019 cần kiểm tiny/GSD/crop/shift cụ thể, không hỏi như thể equivariance chưa ai nghiên cứu.

11. **Q011 · CD:** Small-object recall giảm do feature stride, receptive field hay assignment; can thiệp riêng từng phần có định vị được nút thắt không?
12. **Q012 · CC:** Feature nhiều tỷ lệ cung cấp tín hiệu bổ sung hay chỉ lặp lại tín hiệu; bỏ từng mức trong cùng scale bin ảnh hưởng thế nào?
13. **Q013 · BG:** Có vùng scale mà feature pyramid làm lẫn nền nhiều hơn giúp vật thể; giữ backbone và độ phân giải cố định có lặp lại hiện tượng không?
14. **Q014 · CC:** Tăng context quanh một crop trong khi giữ pixel/vật thể cố định giúp nhận dạng thật hay khai thác tương quan nền; thay nền có làm lợi ích biến mất không?
15. **Q015 · DG:** Cùng lượng context theo pixel và theo kích thước vật thể cho kết quả khác nhau thế nào khi chuyển GSD/cảm biến?
16. **Q016 · CC:** Global context giúp cụm xe/tàu bằng hiểu cảnh hay bằng củng cố class prior; giữ cấu trúc cảnh nhưng đổi lớp/density có phân biệt được không?
17. **Q017 · CD:** Vật thể lớn bị cắt và vật thể nhỏ thiếu context có đòi hỏi crop khác nhau; một policy chung gây xung đột ở scale nào?
18. **Q018 · BG:** GSD positional encoding còn giúp khi metadata thiếu/sai; nhiễu GSD có khiến mô hình nhạy hơn baseline không dùng metadata không?
19. **Q019 · CC:** Scale equivariance có làm box/mask nhất quán sau resize thật sự, hay chỉ giảm lỗi trung bình; đo sai lệch sau biến đổi hình học ra sao?
20. **Q020 · UD:** Cần bao nhiêu vùng ngữ cảnh để phân biệt công năng của vật thể nhìn gần giống nhau, chẳng hạn xe dân dụng và phương tiện ở công trường?

## C. Chọn vùng, crop, tính toán thưa và ghép — Q021–Q030

**Neo:** R01 ClusDet, R02 QueryDet, R04 SAHI, R05 AutoFocus, R09 ESOD, R11 YOLC, R12 UFPMP-Det, R13 Dynamic Zoom-in, R14 Remix, F02 ASAHI, F04 DenseScout, F05 AFWD-Net. Heatmap, clustering, gain prediction, sparse features và downstream closure đã có; cần đối chứng trực tiếp.

21. **Q021 · CD:** Bỏ sót đến từ selector không chọn vùng, detector không nhận trong vùng hay merge loại box; truy vết từng vật thể cho thấy khâu nào chi phối?
22. **Q022 · CC:** Chọn theo density và theo expected task gain khác nhau nhất ở cảnh nào; vùng nhiều vật thể dễ có chiếm chỗ vật thể hiếm khó không?
23. **Q023 · DG:** Coverage của vùng chọn dự báo final AP đến đâu sau false positives, boundary và merge; có policy coverage cao nhưng AP thấp không?
24. **Q024 · BG:** Dự đoán lợi ích có độ tin cậy còn thêm thông tin ngoài density, size và confidence khi đổi miền; gain-only hoặc heatmap có giải thích hết lợi ích không?
25. **Q025 · CC:** Lỗi ở biên crop do mất context, truncation nhãn hay merge; dịch lưới crop qua cùng vật thể có tách được ba nguyên nhân không?
26. **Q026 · BG:** Overlap lớn hoặc crop ownership đơn giản có giải quyết hiện tượng biên tương đương module mới; khi nào module không còn lý do tồn tại?
27. **Q027 · CC:** Packing foreground thành mosaic gây đổi context và lân cận nhân tạo tới mức nào; giảm nền có còn lợi sau kiểm soát các hiệu ứng đó không?
28. **Q028 · DG:** Sparse feature processing và crop inference khác nhau thế nào về recall vật thể ngoài vùng quan tâm khi khớp độ phân giải và latency thực?
29. **Q029 · CC:** Cấp thêm độ phân giải cho một vùng ảnh hưởng quyết định ghép ở vùng khác thế nào; utility từng patch có cộng được thành utility toàn ảnh không?
30. **Q030 · UD:** Policy tối ưu đếm số vật thể, tìm lớp hiếm và tối ưu AP có chọn vùng khác nhau không; cần objective nào cho nhiệm vụ cụ thể?

## D. Hình học OBB, góc và tính nhận diện được — Q031–Q040

**Neo:** G01–G03 aligned/oriented detectors, G04 GWD, G05 KLD, G06 KFIoU, G07 PSC, G08 RHINO, G09 AO2-DETR, G10 GauCho, G11 GSDet, G12 O2-family, F01 RiO-DETR, R08 AI-TOD-R/DCFL. Loss phân bố và mã hóa góc đã có; Gaussian shape không mặc định là uncertainty hiệu chuẩn.

31. **Q031 · CD:** AP OBB thấp do sai tâm, chiều cạnh, góc hay class; sửa oracle từng thành phần cho biết dư địa nào thực sự lớn?
32. **Q032 · CC:** Với cùng số pixel, vật thể dài và gần vuông chịu nhiễu góc khác nhau thế nào; loss/representation hay chính tín hiệu ảnh tạo khác biệt?
33. **Q033 · DG:** Sai số góc nên tính modulo đối xứng hình học nào; quy ước góc khác nhau có đổi xếp hạng detector dù polygon giống nhau không?
34. **Q034 · BG:** Với vật thể tiny hoặc gần vuông, góc có còn suy ra đáng tin từ ảnh; tăng pixel và nhãn nhiều người có tách ambiguity quan sát khỏi lỗi học không?
35. **Q035 · CC:** GWD/KLD/KFIoU cải thiện nhờ gradient phù hợp hay nhờ bớt nhạy với nhiễu nhãn; thử nhãn sạch và nhiễu có thay kết luận không?
36. **Q036 · BG:** Cholesky/Gaussian representation có giúp khi object shape lệch xa hình chữ nhật; mask-derived OBB và quadrilateral có đưa ra kết quả trái nhau không?
37. **Q037 · CC:** Angle distribution và periodic refinement sửa lỗi tuần hoàn hay biểu diễn ambiguity; calibration theo aspect ratio có phân biệt được hai vai trò không?
38. **Q038 · DG:** Hungarian matching theo polygon, Hausdorff hoặc Chamfer có đổi lỗi gán trong cụm đông; đo assignment churn thay vì chỉ AP có giải thích được không?
39. **Q039 · CD:** Rotated feature alignment giúp tiny objects vì định hướng đúng hay vì lấy mẫu feature khác; angle shuffle và alignment oracle cho thấy điều gì?
40. **Q040 · UD:** Khi mục tiêu là đếm hoặc bám mục tiêu, OBB chính xác có quan trọng hơn HBB/mask đến mức nào; metric task có thưởng cải thiện góc vô ích không?

## E. Cảnh dày đặc, mất cân bằng và assignment — Q041–Q050

**Neo:** R06 RFLA, R07 NWD-RKA, R08 DCFL, R01 ClusDet, R11 YOLC, G08–G09 matching, G11 dynamic Gaussians, D01–D02 DOTA. Cơ chế assignment cho tiny và anti-bias đã có trong corpus; còn cần kiểm tra boundary và nguyên nhân cạnh tranh.

41. **Q041 · CD:** Recall trong cảnh đông giảm do ít query/positive samples, feature không tách được hay NMS; oracle từng khâu phân rã lỗi ra sao?
42. **Q042 · CC:** Khoảng cách giữa hai vật thể theo pixel hay theo chiều ngắn dự báo merge failure tốt hơn khi thay scale?
43. **Q043 · BG:** Tăng query/candidate chỉ giúp đến ngưỡng nào; sau đó nút thắt có chuyển sang feature, matching hoặc nhãn thiếu không?
44. **Q044 · CC:** Assignment phù hợp tiny objects có tăng recall lớp hiếm hay chủ yếu tăng positive của lớp đông; phân tầng theo class và density cho thấy gì?
45. **Q045 · DG:** NWD scale parameter hoặc assignment radius có chuyển được giữa GSD/dataset; tuning theo pixel có che giấu sự phụ thuộc miền không?
46. **Q046 · CC:** Ở cụm vật thể sát nhau, thất bại chủ yếu do thông tin ảnh không tách nổi hay suppression; dùng nhãn GT làm box candidates và ảnh chi tiết hơn có phân biệt được không?
47. **Q047 · BG:** Không dùng NMS có loại bỏ bỏ sót cụm hay đổi thành duplicates; detector end-to-end còn giới hạn nào do query capacity?
48. **Q048 · CD:** Mẫu khó được gán ít positive vì nhỏ hay vì label ambiguity; relabel một subset có làm apparent class/scale bias giảm không?
49. **Q049 · CC:** Crowding augmentation giúp khả năng phân biệt thật hay chỉ khớp density training; giữ occlusion và nearest-neighbor distance độc lập cho kết quả gì?
50. **Q050 · UD:** Trong kiểm kê tàu/xe, giảm double-count hay giảm missed-count quan trọng hơn; model tốt theo AP có tốt theo sai số đếm và lớp hiếm không?

## F. Segmentation, biên và liên hệ box–mask — Q051–Q060

**Neo:** S01 Mask R-CNN, S02 Mask2Former, S03 SAM, S05 RS-SAM, S06 ROS-SAM, S11 SegEarth-OV, D04 iSAID; N05 DroneEyes/SkyAnchor (streaming referring segmentation), N07 UAVScenes (camera–LiDAR semantic segmentation), N10 OpenRSD (open-prompt HBB/OBB detection), N18 SOPSeg/ReSOS. N10 không phải segmentation baseline. N18 đánh giá given-box→mask; ReSOS có teacher-generated/manual-filtered masks, không mặc định GT mask độc lập vẽ tay. Open-vocabulary/open-prompt đã có; Q060/Q090 hỏi boundary và kiểm leakage/distractor, không khẳng định cơ chế mới. DOTA và iSAID dùng chung ảnh, không phải hai miền độc lập.

51. **Q051 · CD:** Mask vật thể nhỏ sai vì không phát hiện được instance, biên không rõ hay mask resolution thấp; conditional mask quality và end-to-end AP khác nhau thế nào?
52. **Q052 · CC:** Tăng mask-head resolution khi giữ image feature cố định còn giúp bao nhiêu; upsampling có chỉ làm biên trơn hơn mà không chính xác hơn không?
53. **Q053 · DG:** Pixel IoU có che giấu việc nhập hai cá thể nhỏ; boundary và split/merge metrics có đổi kết luận khi cảnh đông không?
54. **Q054 · CC:** Mask supervision cải thiện OBB vì bổ sung tín hiệu hình dạng hay vì thêm nhãn/regularization; cùng backbone và lượng nhãn có tách được không?
55. **Q055 · BG:** Ràng buộc box–mask consistency có gây hại với vật thể lõm, occluded hoặc nhãn box rộng; khi nào hai loại nhãn không nên ép khớp?
56. **Q056 · DG:** SAM với GT prompts, predicted prompts và tự động proposals khác nhau bao nhiêu; lợi ích có còn sau tính false prompts và missing objects không?
57. **Q057 · CC:** LoRA/multiscale adaptation giúp biên tiny vì scale matching hay vì domain adaptation; chỉ thay scale và chỉ thay appearance có tách vai trò không?
58. **Q058 · BG:** Pseudo-mask tạo từ foundation model có mang sai lệch nhỏ-vật-thể vào detector; confidence cao có đảm bảo biên/instance đúng không?
59. **Q059 · UD:** Khi ứng dụng cần diện tích vật thể hoặc vùng bị che, mask quan sát và mask đầy đủ cần nhãn/metric khác nhau ra sao?
60. **Q060 · DG:** Open-vocabulary segmentation phân biệt lớp mới nhờ prompt semantics hay nhờ dataset overlap; paraphrase và held-out class/scene có làm kết luận thay đổi không?

## G. Video detection và thông tin theo thời gian — Q061–Q070

**Neo:** D05 VisDrone; bổ sung N01 UAVDT, N04 HARD cho detection/MOT/streaming; N03 DynUAV cho ego-motion UAV MOT. S08 SatMAE là temporal representation, S06 ROS-SAM là interactive segmentation; không thay video detection baseline. N09 PointSR dùng temporal ensembling không mặc định là video method; N14 Nano-VID-weather dùng static elevated camera, không mặc định UAV ego-motion. Câu hỏi temporal fusion vẫn cần full-method audit prior đúng task trước novelty claim.

61. **Q061 · CD:** Box/mask nhấp nháy do vật thể ít pixel, exposure thay đổi, motion blur hay camera motion; phân tầng chuỗi có tách các nguyên nhân không?
62. **Q062 · CC:** Temporal fusion bổ sung quan sát độc lập hay chỉ làm mượt confidence; so frame lặp, frame thật và shuffled history cho thấy gì?
63. **Q063 · BG:** Alignment sai của vật thể nhỏ có khiến dùng lịch sử tệ hơn single-frame; ngưỡng motion/blur nào đảo dấu lợi ích?
64. **Q064 · DG:** Causal detector chỉ dùng quá khứ thua offline detector dùng tương lai ở đâu; bao nhiêu chất lượng được đổi bằng look-ahead delay?
65. **Q065 · CC:** Với cùng mức chi tiết và số quan sát, temporal fusion có cải thiện phát hiện tiny hơn chọn frame nét nhất; lợi ích còn sau khớp blur và camera motion không?
66. **Q066 · DG:** AP trung bình frame có giấu phát hiện muộn của mục tiêu mới; time-to-first-detection và thời gian mất dấu đổi xếp hạng không?
67. **Q067 · BG:** Scene tĩnh có giúp temporal model chỉ vì lặp lại nền; đổi background hoặc camera trajectory có làm lợi ích mất không?
68. **Q068 · CC:** Lịch sử độ phân giải cao có tái dùng cho frame mới mà không kéo theo ghost objects; change detection có phân biệt reuse an toàn không?
69. **Q069 · UD:** Với đối tượng xuất hiện ngắn, số frame cần tích lũy làm bỏ lỡ sự kiện nào; một policy dành cho vật thể lưu lâu có phù hợp không?
70. **Q070 · DG:** Temporal mask consistency nên thưởng biên ổn định hay phạt lag khi vật thể thật đổi hình; metric dựa trên motion có tránh thưởng mask cũ không?

## H. MOT, SOT và zoom để bám mục tiêu — Q071–Q080

**Neo:** D05 VisDrone, N01 UAVDT (MOT/VID), N02 UAV123/UAV20L (SOT), N03 DynUAV (ego-motion MOT), N04 HARD (detection/MOT/streaming), N06 MUST/UNTrack (multispectral SOT); X03 HOTA cho metric. R10/R13/R14/F04 chỉ là cơ chế chuyển giao, **không là prior MOT/SOT trực tiếp**. Phạm vi task đã có nguồn riêng; zoom phục vụ association/SOT cần audit đầy đủ, không mặc định là gap mới.

71. **Q071 · CD:** MOT thất bại do detector miss, association nhầm hay track termination; oracle detections/IDs riêng cho biết phần nào cần nghiên cứu?
72. **Q072 · CC:** Zoom giúp giữ ID nhờ appearance rõ hơn hay nhờ box chính xác hơn; thay riêng embedding và box cho thấy vai trò nào?
73. **Q073 · BG:** Policy ưu tiên track đã biết có làm chậm phát hiện mục tiêu mới; track recall và discovery recall có xung đột không?
74. **Q074 · CC:** Ở MOT, cấp resolution theo khó association có giữ ID tốt hơn theo density/gain detection; lợi ích còn khi khóa detector recall và update frequency không?
75. **Q075 · DG:** OBB/mask giúp association trong cảnh đông hơn HBB đến đâu sau kiểm soát detection quality; DetA và AssA có chỉ cùng một hướng không?
76. **Q076 · BG:** SOT crop theo mục tiêu dễ drift sang distractor khi zoom mạnh đến mức nào; đo recovery sau mục tiêu ra khỏi crop thay vì chỉ success trung bình được không?
77. **Q077 · CC:** Kết hợp vùng search rộng độ phân giải thấp và vùng hẹp chi tiết cao giúp SOT vì tái phát hiện hay vì local localization; thử occlusion và fast motion riêng ra sao?
78. **Q078 · DG:** Track sống lâu nhưng vị trí cập nhật chậm có được HOTA/IDF1 thưởng quá mức cho ứng dụng điều khiển; cần thêm spatial error theo timestamp nào?
79. **Q079 · UD:** Có thể giữ dấu nhiều mục tiêu và vẫn điều khiển physical zoom phục vụ một mục tiêu ưu tiên; sự đánh đổi FOV–identity–discovery biểu hiện ra sao?
80. **Q080 · BG:** Chuyển policy từ MOT sang SOT có còn hợp lý khi SOT được cho mục tiêu ban đầu còn MOT phải tự tìm mọi mục tiêu; thí nghiệm nào bác sự chuyển giao?

## I. Domain shift, cảm biến và pretrained representation — Q081–Q090

**Neo:** F03 RWDS, S07 Scale-MAE, S08 SatMAE, S10 RemoteCLIP, D03 DIOR, D05 VisDrone, D06 FAIR1M; N11 Active-DDC cho domain-incremental, N08 ATR-UMOD/PCDF cho RGB–IR, N06 multispectral SOT. Đã có shift, scale-aware pretraining và fusion; UAV–satellite, metadata/overlap và chuyển task cần kiểm riêng.

81. **Q081 · CD:** Chuyển miền thất bại chủ yếu vì scale/GSD, appearance, class prior hay annotation policy; chuẩn hóa từng yếu tố có đổi độ sụt chất lượng không?
82. **Q082 · CC:** Pretraining có GSD giúp chuyển scale thật hay ghi nhớ sensor-specific texture; giữ vùng địa lý ngoài training cho biết điều gì?
83. **Q083 · BG:** Model bền với resize augmentation có bền với native sensor/GSD shift; paired acquisitions có bác tính đại diện của synthetic shift không?
84. **Q084 · CC:** Scale-aware representation có giảm lỗi GSD shift độc lập với augmentation và exposure to target; khớp dữ liệu/nhãn có còn lợi không?
85. **Q085 · DG:** Train trên DOTA rồi kiểm trên FAIR1M/DIOR cần làm sạch class mapping và scene overlap thế nào để kết quả phản ánh chuyển miền thực?
86. **Q086 · CC:** Temporal/multispectral pretraining giúp detection hình học hay chỉ phân loại; oracle class và localization diagnostics có tách được không?
87. **Q087 · BG:** Adaptation trên unlabeled target có overfit thời tiết/nền mà giảm recall lớp hiếm; evaluation held-out target scenes có phát hiện được không?
88. **Q088 · DG:** Vùng địa lý, thời gian và cảm biến nào nên giữ lại để đo extrapolation; random image split có đánh giá quá lạc quan đến đâu?
89. **Q089 · UD:** Sau thiên tai, vật thể hư hỏng và scene layout đổi khác có cần task khác regular detection; đo object existence và category ambiguity thế nào?
90. **Q090 · BG:** Open-vocabulary detector/segmenter có nhận tên lớp mới nhưng nhầm distractor địa phương; unknown rejection và class hierarchy có làm kết luận chính xác hơn không?

## J. Bất định, chất lượng nhãn và cách thu thập nhãn — Q091–Q100

**Neo:** G10 GauCho cho shape representation; R07 AI-TOD-v2 cho nhãn tiny; S12 active learning; D01/D04/D06 nhãn box/mask; X01 UGS cho uncertainty trong tối ưu localization, X02 Point2RBox-v2 và N09 PointSR/N12 LLM sparse annotation cho nhãn thưa. Uncertainty để tối ưu không mặc định là calibrated OBB uncertainty; point→OBB đã có tiền lệ. Decomposition/calibration dưới shift vẫn cần prior scan riêng.

91. **Q091 · DG:** Class confidence có dự báo localization/mask quality đồng đều theo size, aspect ratio và density; calibration aggregate có giấu tiny failures không?
92. **Q092 · CC:** Sai số do thiếu tín hiệu quan sát và do mô hình chưa học đủ có thể tách qua repeated annotation, repeated acquisitions và model ensemble không?
93. **Q093 · BG:** Distribution parameter của Gaussian OBB có phản ánh prediction error; empirical coverage test có bác việc gọi covariance là uncertainty không?
94. **Q094 · CC:** Uncertainty tăng vì miền lạ hay vì nhãn mâu thuẫn; retrain với nhãn đồng thuận có làm tín hiệu OOD suy giảm không?
95. **Q095 · DG:** Tỷ lệ nhãn thiếu/sai góc theo scale/density làm đảo thứ hạng detector hoặc policy đến đâu khi audit và relabel một tập cố định?
96. **Q096 · BG:** Giảm loss ở mẫu “uncertain” có bỏ qua vật thể thật khó và lớp hiếm; label audit độc lập có phân biệt robustness với né mẫu khó không?
97. **Q097 · CC:** Active learning theo uncertainty chọn mẫu nhiều thông tin hay mẫu không thể gán nhất quán; chọn theo diversity và annotation disagreement cho kết quả khác gì?
98. **Q098 · DG:** Mask/box từ foundation model giảm công sửa nhưng gây lỗi hệ thống nào ở tiny objects; phải đo quality sau human correction hay trước correction?
99. **Q099 · UD:** Hệ thống có thể từ chối hoặc yêu cầu ảnh chi tiết hơn ở mẫu khó; coverage–risk và thời gian hoàn thành task thay đổi ra sao?
100. **Q100 · BG:** Uncertainty có còn calibrated sau thay crop, SR, quantization hoặc sensor; calibration tại detector gốc có đủ cho toàn pipeline không?

## K. Protocol, metric và kết luận nhân quả — Q101–Q110

**Neo:** D01–D06 benchmarks, R04 slicing, F03 shift evaluation, F04 closure, G04–G08 geometry metrics. Đây là câu hỏi đánh giá phương pháp; không khẳng định benchmark hiện hành sai chỉ từ suy luận.

101. **Q101 · DG:** Báo AP toàn ảnh thay AP patch làm xếp hạng thay đổi bao nhiêu; duplicates và vật thể ở biên giải thích phần nào?
102. **Q102 · CD:** Hai evaluator OBB khác nhau về quy ước góc, difficult flags hoặc polygon clipping gây chênh lệch kết quả tới đâu trên cùng predictions?
103. **Q103 · DG:** Bin kích thước dựa trên ảnh gốc và trên input resized tạo kết luận trái nhau không; chuẩn nào phù hợp với claim “tiny detection”?
104. **Q104 · BG:** Lợi ích module mới còn sau đối chứng khớp train data, resolution, checkpoint, augmentation và preprocessing; yếu tố nào đủ giải thích gain?
105. **Q105 · DG:** Seed, scene sampling và class mix tạo biến thiên lớn hơn chênh lệch method ở nhóm nào; bootstrap theo scene cho kết luận khác bootstrap theo box không?
106. **Q106 · DG:** Policy dẫn đầu AP có dẫn đầu mục tiêu ứng dụng như missed-event, counting error hoặc time-to-detection; benchmark đa task có đổi thứ hạng không?
107. **Q107 · BG:** Chọn hard subset sau xem test có biến discovery thành apparent validation; kiểm trên subset và miền giữ lại trước có lặp kết luận không?
108. **Q108 · DG:** Boundary stress test bằng dịch crop/resize có dự báo lỗi cảnh thật; correlation trên held-out scenes cho biết giá trị chẩn đoán đến đâu?
109. **Q109 · CC:** Khi can thiệp nhiều module, factorial ablation có cho thấy interaction khiến lợi ích từng module không cộng được; module nào chỉ tốt cùng điều kiện khác?
110. **Q110 · DG:** Chứng minh “không giúp” cần interval đủ hẹp và margin ý nghĩa nào cho task; negative result có phân biệt thiếu power với không có utility không?

## L. Streaming thời gian thực và mục tiêu ứng dụng — Q111–Q120

**Neo:** B05 RT-DETR, G12 O2-family, F01 RiO-DETR, R14 Remix, F04 DenseScout, D05 VisDrone; X04 Towards Streaming Perception đã nghiên cứu scheduling/forecasting và trạng thái tại thời điểm output; N04 HARD có streamingHOTA, N05 streaming referring segmentation. Không gọi freshness-aware scheduling là ý tưởng mới. Q113/Q115 đặt vào UAV motion, crop và bursty arrivals; **closed-loop sensing là mở rộng thăm dò**. Không còn trần tài chính, nhưng độ trễ vẫn là thuộc tính khoa học của streaming.

111. **Q111 · CD:** Thời gian từ thu ảnh đến output bị chi phối bởi decode, crop, inference, merge, association hay queue; FPS model có phản ánh pipeline không?
112. **Q112 · DG:** Throughput trung bình giống nhau nhưng latency p95/p99 khác có làm số deadline misses và missed events khác nhau thế nào?
113. **Q113 · CC:** Under bursty streams, bỏ frame cũ và xử lý frame mới có cho vị trí hiện tại đúng hơn xử lý mọi frame theo FIFO; accuracy–freshness thay đổi ra sao?
114. **Q114 · BG:** Temporal reuse giúp tốc độ nhưng sinh output cũ khi cảnh đổi; kiểm sudden entry/exit và camera turn có làm ưu thế biến mất không?
115. **Q115 · CC:** Dynamic shape, batching và pipeline scheduling đổi latency của adaptive zoom thế nào; policy đo trên offline batches còn tốt khi streaming không?
116. **Q116 · DG:** So dense/sparse/crop methods cùng deadline và hardware có đổi frontier AP–latency so với so cùng FLOPs; memory transfer giải thích bao nhiêu?
117. **Q117 · BG:** Quantization giảm thời gian nhưng mất calibration/góc/mask của tiny objects trước nhóm khác không; giữ overall AP có che giấu lỗi task-critical không?
118. **Q118 · UD:** Trong tìm kiếm cứu nạn, ưu tiên recall, discovery delay và xác nhận mục tiêu cần objective khác AP như thế nào; false alarm ảnh hưởng quy trình ra sao?
119. **Q119 · UD:** Điều khiển camera/gimbal theo detection uncertainty có thu thêm thông tin hữu ích hay gây vòng lặp nhìn mãi vùng dễ; exploration policy cần kiểm chứng nào?
120. **Q120 · DG:** Khi có thể thêm cảm biến hoặc nhiều UAV, fusion cải thiện coverage, resolution hay reliability; tách các nguồn lợi ích và thất bại đồng bộ thế nào?

## 12 câu hỏi ưu tiên cho thiết kế nghiên cứu

Đây là **12 câu mạnh theo độ rõ của cơ chế, khả năng bác bỏ và ý nghĩa khoa học**, không phải xếp hạng novelty đã xác nhận. Chúng trải đều các trục, không chọn theo chi phí. Mỗi thẻ chỉ nên trở thành proposal sau full-method scan của prior gần và xác minh dữ liệu/checkpoint. **Tất cả chưa chạy được end-to-end như mô tả; chưa có baseline nội bộ hay kết quả train.** Dữ liệu nêu là ứng viên; không mặc định đã tải hoặc có đủ metadata/nhãn. Prior thiếu được nói rõ, không thay bằng tên paper suy đoán.

### P01 — Q002: Zoom cung cấp thông tin mới hay chỉ đổi cách biểu diễn?

- **Task/triệu chứng:** still detection OBB/HBB; tăng zoom nhưng recall/định vị đáp ứng không đều theo size.
- **Giả thuyết cạnh tranh:** pixel gốc được giữ lại; input scale phù hợp model; SR sinh prior; cảm biến thu tín hiệu mới.
- **Phép thử/đối chứng:** cùng scene, đồng đăng ký, so native crops, bicubic interpolation, SR, physical acquisition; giữ vùng nhìn và apparent object size khi so được. R04 SAHI, R10/R13 cho zoom; N17 RSSOD/MCGR cho joint SR–detection. N16 SuperYOLO là auxiliary SR feature-learning control, không phải inference image-SR pipeline. Cần full-method audit và physical-sensing prior. Không gọi bốn nhánh là so sánh nhân quả sạch nếu FOV, blur, exposure chưa kiểm soát.
- **Đo:** AP/AR theo size/contrast, center error và IoU; chất lượng SR chỉ là biến trung gian, không thay task metric.
- **Bác bỏ:** lợi ích biến mất khi khớp input scale/blur, hoặc native detail không thêm utility so nội suy trong phạm vi kiểm; bác claim khái quát “zoom thêm thông tin”.
- **Nhãn/dữ liệu:** box/OBB trên ảnh gốc, paired high/low native resolution và metadata quang học; DOTA chỉ hỗ trợ phần crop/synthetic, không tự cung cấp physical pairs.
- **Ý nghĩa:** xác định bản chất quan sát cần bổ sung, tránh quy mọi cải thiện cho SR hoặc xử lý đa tỷ lệ.

### P02 — Q014: Context giúp hình dạng hay tạo shortcut theo nền?

- **Task/triệu chứng:** vẫn một đối tượng nhưng đổi crop margin làm đổi class/box.
- **Giả thuyết:** ngữ cảnh ngữ nghĩa có ích; nền mang class prior; crop làm đổi pixel/object.
- **Phép thử/đối chứng:** thay margin nhưng khóa pixel/object; background replacement có kiểm tra realism, context masking và natural held-out backgrounds. B01 FPN, R03 CEASC là prior đa tỷ lệ/context; native full-image/crop baseline bắt buộc.
- **Đo:** AP/AR, class-confusion và calibration theo context/scale; chất lượng box khi class đúng.
- **Bác bỏ:** lợi ích được giải thích hoàn toàn bằng pixel/object hoặc mất trên background thật giữ lại; không bảo vệ claim context reasoning.
- **Nhãn/dữ liệu:** DOTA/FAIR1M với scene IDs, boxes và vùng background/context audit; masks hữu ích cho edit, không mặc định có ở FAIR1M.
- **Ý nghĩa:** hiểu phần nào của scale–context trade-off tổng quát được sang cảnh mới.

### P03 — Q024: Độ tin cậy của lợi ích zoom có giá trị dưới shift?

- **Task/triệu chứng:** still OBB; selector chọn vùng nhưng final utility đôi lúc giảm dưới domain/scale shift.
- **Giả thuyết:** uncertainty về gain có thông tin bổ sung; chỉ confidence/density/size đã đủ; lỗi thật nằm ở merge.
- **Phép thử/đối chứng:** khóa backend/merge; oracle per-region outcomes chỉ dùng cho chẩn đoán hoặc nhãn train riêng; so fixed tiling, density/heatmap, gain-only và calibrated-risk policy. Prior sát: R13 Dynamic Zoom-in, R14 Remix, F04 DenseScout; F05/F06 cần full-method check. F04 đã đo closure, không gán cho nó thiếu downstream evaluation.
- **Đo:** final whole-image AP/AR, calibration của gain/risk, coverage–risk, measured latency; không cộng patch AP thành delta AP.
- **Bác bỏ:** reliability không cải thiện utility ngoài các feature đơn giản hoặc không chuyển miền; bỏ claim cơ chế reliability dù selector tổng thể tốt.
- **Nhãn/dữ liệu:** box/OBB và paired coarse/detail outputs trên train-selector split; scene/domain held-out, không GT test trong policy.
- **Ý nghĩa:** kiểm tra quyết định thu thêm chi tiết có thể tin cậy đến đâu; đây chỉ một hướng trong 12, không mặc định ưu tiên cao nhất.

### P04 — Q034: Góc của vật thể tiny có suy ra được từ ảnh?

- **Task/triệu chứng:** OBB góc dao động, nhất là vật thể gần vuông hoặc ít pixel.
- **Giả thuyết:** parameterization/loss yếu; label convention mâu thuẫn; chính ảnh không chứa đủ thông tin hướng.
- **Phép thử/đối chứng:** cùng cảnh nhiều scale, nhiều người gán nhãn độc lập; so G07 PSC, G04–G06 losses và G10 GauCho dưới cùng backbone. Thay cách mã hóa không mặc định thay uncertainty.
- **Đo:** angle error modulo đối xứng, agreement giữa annotators, OBB IoU/AP và empirical uncertainty coverage theo aspect ratio/size.
- **Bác bỏ:** representation tốt giải quyết lỗi dưới ảnh low-resolution mà disagreement nhãn thấp; bác việc quy phần lỗi đó cho bất định quan sát. Ngược lại, thất bại model đơn lẻ không chứng minh bất khả thi thông tin.
- **Nhãn/dữ liệu:** R08 AI-TOD-R hoặc DOTA, repeated OBB/quadrilateral labels và high-resolution counterparts nếu có; nhãn hướng vật lý riêng nếu task đòi hỏi heading.
- **Ý nghĩa:** phân biệt mục tiêu hình học đo được với mục tiêu không xác định duy nhất, từ đó đặt metric/loss hợp lý.

### P05 — Q046: Cụm sát nhau mất vì quan sát hay suppression?

- **Task/triệu chứng:** nhiều vật thể gần nhau bị nhập hoặc bỏ sót.
- **Giả thuyết:** thiếu chi tiết; assignment/query capacity; suppression loại vật thể thật; nhãn thiếu.
- **Phép thử/đối chứng:** oracle GT candidates kèm scores chẩn đoán; giữ raw predictions và thay suppression; tăng native detail riêng. So G03 Oriented R-CNN và G08/G09 end-to-end, R06/R07/R08 assignment. Oracle không là phương pháp deploy.
- **Đo:** recall theo nearest-neighbor distance/scale, duplicate rate, assignment churn, count error và AP.
- **Bác bỏ:** hiệu ứng biến mất sau relabel hoặc không xuất hiện khi giữ số pixel/occlusion; bác claim crowding mechanism chung.
- **Nhãn/dữ liệu:** cảnh đông DOTA/iSAID/VisDrone, audit đầy đủ instance và trạng thái occlusion; đối sánh size/density cần thiết.
- **Ý nghĩa:** xác định có cần ảnh tốt hơn, assignment mới hay hậu xử lý khác, tránh chữa sai khâu.

### P06 — Q054: Mask supervision có đóng góp hình học riêng?

- **Task/triệu chứng:** box đủ nhận lớp nhưng hình học tiny/elongated objects kém.
- **Giả thuyết:** mask truyền shape; thêm nhãn và training signal; regularization/multi-task chung.
- **Phép thử/đối chứng:** detector box-only, cùng backbone với mask branch, auxiliary task có lượng giám sát tương đương, và mask-derived box baseline. S01 Mask R-CNN là prior gần; S02/S05 chỉ so khi task/output khớp.
- **Đo:** OBB AP/IoU theo size/shape, mask AP, boundary và split/merge; phân tích gradient/task conflict nếu claim cơ chế.
- **Bác bỏ:** thêm nhãn hoặc regularization baseline giải thích hết lợi ích, hoặc chỉ tăng class AP không tăng geometry; bỏ claim shape-specific transfer.
- **Nhãn/dữ liệu:** iSAID + DOTA cùng source images và scene split khóa chung; kiểm box–mask correspondence. Không dùng hai bộ này để chứng minh cross-domain.
- **Ý nghĩa:** kiểm tra khi nào giám sát hình dạng giúp detection, thay vì chỉ ghép detection với segmentation.

### P07 — Q065: Thời gian thực sự bổ sung tín hiệu tiny?

- **Task/triệu chứng:** video detection; vật thể tiny chỉ nhận được ở một số frame.
- **Giả thuyết:** lịch sử thêm quan sát độc lập; chỉ chọn frame nét; smoothing làm ổn định score; alignment tạo artifact.
- **Phép thử/đối chứng:** causal temporal fusion, single frame, causal best-frame selection, duplicated frame và shuffled history; khớp số lần quan sát/latency khi phù hợp. D05/N01 là dữ liệu, N04 là nguồn bổ sung detection/streaming cần audit temporal mechanism; S08 không thay baseline video detection. Không dùng temporal ensembling của N09 làm video prior.
- **Đo:** video/frame AP, AR theo blur/size, time-to-first-detection, false persistence và latency.
- **Bác bỏ:** lợi ích biến mất so best-frame hoặc lịch sử giả cho lợi tương đương; không bảo vệ claim bổ sung thông tin thời gian.
- **Nhãn/dữ liệu:** video VisDrone với frame boxes/timestamps, motion/blur strata; IDs chỉ cần nếu phân tích track-conditioned, không mặc định dùng MOT metric.
- **Ý nghĩa:** phân biệt nhận thức từ nhiều quan sát với làm mượt dự đoán, và tìm boundary của temporal fusion.

### P08 — Q074: Zoom cho association có khác zoom cho detection?

- **Task/triệu chứng:** MOT; detector thấy đối tượng nhưng ID đổi trong cụm/occlusion.
- **Giả thuyết:** cần appearance chi tiết; box alignment; discovery/update frequency quan trọng hơn resolution.
- **Phép thử/đối chứng:** khóa detector và tracker, so fixed-scale, density/gain-detection routing và association-difficulty routing; phân rã bằng oracle detections/association. D05/N01 là nguồn task; N03 DynUAV và N04 HARD là tracking priors cần audit; R13/F04 là transfer prior. Chọn tracker gần theo ego-motion/association setup trước novelty claim.
- **Đo:** HOTA, DetA, AssA, IDF1, ID switches, discovery delay, recall và frame age; report cả toàn hệ lẫn association-conditioned analysis.
- **Bác bỏ:** khi khớp recall và update frequency, lợi ích ID biến mất hoặc mục tiêu mới bị bỏ sót đủ làm task utility giảm.
- **Nhãn/dữ liệu:** video có IDs, boxes, timestamps và occlusion; paired resolution nếu muốn claim thêm detail thay vì chỉ input-scale effect.
- **Ý nghĩa:** biến zoom thành lựa chọn phục vụ identity, không suy tracking tốt chỉ từ AP tăng.

### P09 — Q084: Scale-aware representation tổng quát sang GSD thật?

- **Task/triệu chứng:** still detection/segmentation tốt trên scale đã thấy nhưng giảm khi đổi cảm biến/GSD.
- **Giả thuyết:** learned scale semantics; augmentation coverage; sensor texture; pretraining/data overlap.
- **Phép thử/đối chứng:** S07 Scale-MAE đối chiếu backbone/pretraining và scale augmentation khớp; tách synthetic resize khỏi native GSD shift; metadata corrupted ablation. F03 hướng dẫn held-out shift; S08/S10 là representation alternatives, không mặc định kiến trúc ngang nhau.
- **Đo:** AP/mIoU theo GSD, worst-domain performance, calibration và geometry; chênh paired scenes nếu có.
- **Bác bỏ:** augmentation khớp hoặc kiểm overlap xóa lợi ích, hoặc hiệu quả chỉ tồn tại với synthetic resize; giới hạn claim tương ứng.
- **Nhãn/dữ liệu:** geographic/sensor held-out boxes/masks và GSD đáng tin; FAIR1M là ứng viên metadata cần kiểm. Domain class mapping phải khóa trước.
- **Ý nghĩa:** kiểm tính vật lý của biểu diễn scale thay vì robustness với một phép resize nhân tạo.

### P10 — Q095: Nhãn tiny làm thay đổi kết luận nghiên cứu bao nhiêu?

- **Task/triệu chứng:** apparent false positives, sai góc và xếp hạng detector nhạy dataset version.
- **Giả thuyết:** method thực sự khác; nhãn thiếu/không nhất quán; audit ưu ái một method.
- **Phép thử/đối chứng:** chọn subset trước theo scene/scale/density, annotators không biết predictions/method, adjudication; đánh giá cùng predictions trên nhãn cũ/mới. R07 AI-TOD-v2 là prior chỉnh nhãn; S12 liên quan annotation, không chứng minh ranking reversal ở OBB.
- **Đo:** missing-label/geometry disagreement, AP ranking và interval, FP taxonomy, class/scale-stratified error.
- **Bác bỏ:** audit sạch và interval loại trừ ranking change đáng kể; bác claim label noise là nguyên nhân chính trong phạm vi đã audit.
- **Nhãn/dữ liệu:** corpus tiny với ảnh native, multi-annotator box/OBB, adjudicated GT và change log; version nhãn tách rõ.
- **Ý nghĩa:** xác định phần tiến bộ là modeling và phần nào đến từ mục tiêu đánh giá; có giá trị dù không tạo kiến trúc mới.

### P11 — Q106: AP có dự báo thành công ứng dụng?

- **Task/triệu chứng:** method AP cao nhưng đếm sai hoặc phát hiện sự kiện muộn.
- **Giả thuyết:** AP phù hợp; weighting/threshold không khớp task; temporal/rare-event errors không được AP thể hiện.
- **Phép thử/đối chứng:** khóa outputs của nhiều detector/policy; sweep threshold theo validation, so rank theo AP với count error/missed event/time-to-detection. D01/D05/D06 là task data; R04/F04 là policies, không mặc định cùng annotation.
- **Đo:** AP và calibration; count MAE/bias theo scene; event recall và discovery-delay distribution với định nghĩa sự kiện trước.
- **Bác bỏ:** rankings đồng nhất và AP cải thiện dự báo utility trên held-out application distribution; không bảo vệ claim metric mismatch trong phạm vi đó.
- **Nhãn/dữ liệu:** full-scene counts, event/timestamp labels hoặc video tracks; không suy missed event chỉ từ image boxes.
- **Ý nghĩa:** nối benchmark với mục tiêu thật, làm rõ khi một tiến bộ hình học có hoặc không có giá trị vận hành.

### P12 — Q113: Tối ưu streaming theo độ mới hay xử lý đủ frame?

- **Task/triệu chứng:** video detection/MOT hiển thị box đúng cho frame cũ, sai cho trạng thái hiện tại.
- **Giả thuyết:** FIFO bảo toàn thông tin; freshness quan trọng hơn; drop frames làm mất target; temporal reuse giảm cả delay lẫn miss.
- **Phép thử/đối chứng:** cùng input stream/timestamps và detector, so FIFO, latest-frame, deadline-aware sampling và reuse; replay bursty arrival trace cùng nhau. R14/F04 cho latency/selection; X04 đã scheduling/forecasting cho streaming, N04 có streamingHOTA. Kiểm protocol N04: replicated workers/no queue không tương đương FIFO queue thực. G12/F01 là detector candidates; không tuyên bố freshness scheduling mới.
- **Đo:** capture-to-output p50/p95/p99, frame age, deadline-miss rate, AP tại frame được xử lý và position/event utility tại thời điểm output; MOT thêm HOTA/IDF1 theo protocol công bố.
- **Bác bỏ:** advantage mất sau tính target discovery/failure hoặc chỉ đến từ lượng compute khác; không claim scheduling tốt hơn toàn hệ.
- **Nhãn/dữ liệu:** video timestamps, arrival/processing trace, frame boxes/IDs, hiện tượng target xuất hiện ngắn; hardware pipeline đo thật chưa xác minh.
- **Ý nghĩa:** xác định “real-time” bằng kết quả kịp thời, tách inference FPS khỏi khả năng phản ánh thế giới đang diễn ra.

## Biên giới bằng chứng và handoff

Không tìm thấy cặp claim thực nghiệm trái nhau được kiểm đầy đủ trong lần viết này; không tạo consensus hay Claim Conflicts giả. Các **tension cần kiểm** gồm chi tiết–context, recall–duplicates, AP–association, smoothness–lag và coverage–freshness; chúng là thiết kế câu hỏi, không phải mâu thuẫn đã xác nhận giữa hai paper.

Để chuyển một câu thành research gap, cần: đọc full-method 3–5 prior sát cùng task; tìm prior ngoài corpus khi đánh dấu thăm dò; xác minh annotation, split và evaluator; đo baseline nội bộ; đăng ký trước câu hỏi, đối chứng và falsifier. Không có expected numeric gain, best architecture hoặc kết luận venue trong ngân hàng này. → Handoff cho điều phối viên tích hợp bằng chứng temporal/MOT mới; dùng paper-method cho audit prior sát và thiết kế protocol riêng cho 1–3 câu được chọn.

## Thuật ngữ (Glossary)

| English | Tiếng Việt | Giải thích ngắn |
|---|---|---|
| Native crop | Crop từ ảnh gốc | Giữ tín hiệu gốc trước resize toàn ảnh |
| Digital interpolation | Phóng to bằng nội suy | Tạo pixel mới từ tín hiệu đang có |
| Learned super-resolution | Siêu phân giải học được | Suy đoán chi tiết theo prior của model |
| Physical zoom | Zoom qua cảm biến/quang học | Thay cách thu ảnh, có thể đổi GSD và FOV |
| GSD | Kích thước mặt đất ứng với pixel | Liên hệ scale ảnh với kích thước vật lý |
| HBB / OBB | Box ngang / box có hướng | Hai cách biểu diễn và đánh giá khác nhau |
| Identifiability | Tính nhận diện được | Quan sát có đủ xác định đại lượng cần dự đoán không |
| Causal video model | Model video nhân quả | Chỉ dùng frame hiện tại và quá khứ |
| MOT / SOT | Bám nhiều / một mục tiêu | MOT tự phát hiện/giữ IDs; SOT theo mục tiêu đã khởi tạo |
| Calibration | Hiệu chuẩn | Mức tin cậy dự đoán khớp tần suất đúng/sai quan sát |
| Falsifier | Điều kiện bác bỏ | Kết quả khiến giả thuyết/cơ chế không còn đứng vững |
| Frame freshness | Độ mới của frame | Output phản ánh thời điểm thu ảnh cách hiện tại bao lâu |
