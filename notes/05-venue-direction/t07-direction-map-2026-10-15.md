# Bản đồ hướng nghiên cứu mở rộng cho #7 — quét keyword và abstract, không chốt giả thuyết

> **Đính chính 15/10/2026 — C-19:** giữ tám giả thuyết cạnh tranh; đọc [audit mới](../07-audits/t07-q2-audit-2026-10-15/REPORT.md) để sửa diễn giải. AQE/O2 đã được đọc sâu hơn nhưng chưa chứng minh “chỉ còn pixel-size conditioning là mới”. CSCWD nghiên cứu phát hiện drone, không trực tiếp UAV-view OBB. Đủ candidate mà recall thấp không nhận dạng nguyên nhân feature; các dấu hiệu lỗi có thể chồng lấn, chưa phân rã thành tỷ trọng nhân quả cộng được. Rút mapping tier→quartile và điều kiện cứng ba dataset. Cache scan1015 đã được sao lưu có hash trong thư mục audit.

| Trường | Giá trị |
|---|---|
| Đề tài | #7, vật thể tí hon trên ảnh trên không (nối tiếp hướng A = C-16 và nhánh C-17) |
| Worker | admin → research-admin; quét rộng, không chọn hướng thắng |
| Ngày | 2026-10-15 |
| Phương pháp quét | arXiv API: 16 họ keyword (vòng 1, nộp 2024–10/2026) + 8 góc bổ sung (vòng 2, nộp 2025–10/2026), xếp theo độ liên quan, tối đa 12–15 kết quả mỗi truy vấn. OpenAlex: 7 truy vấn, bài journal từ 2025. Loại trùng với 262 mã arXiv đã có trong `notes/` |
| Mức đọc | **Toàn bộ nguồn mới trong file này chỉ đọc abstract**, trừ O2-DETR (đã quét toàn văn hôm 14/10). Không có nguồn nào được đọc method/experiment đầy đủ trong lượt này |
| Trạng thái | Không chạy thí nghiệm. Số liệu là [tác giả báo cáo, abstract]. **Không gán tier hay venue cho hướng nào trong file này** |

Nhãn: [abstract] · [toàn văn] · [suy luận] · [design] · [chưa xác minh].

---

## 1. Bản đồ keyword → nguồn mới → ý nghĩa cho #7

Cột "Ý nghĩa" là suy luận của người tổng hợp, **không phải kết luận của các bài**.

| Họ | Keyword đã dùng (tiếng Anh) | Nguồn mới đáng chú ý [abstract] | Bài nói gì | Ý nghĩa cho #7 [suy luận] |
|---|---|---|---|---|
| **Gán nhãn / mẫu dương** | label assignment, positive samples, tiny, aerial | DALA (CAAI TIT 2025); DCEDet (Remote Sens. 2025, NDDM); DRLA-Net (GRSL 2025); CEM-FBGTinyDet (arXiv 2506.09897); NRQO (arXiv 2507.19059) | DALA: khoảng cách tương đồng + chọn số mẫu dương theo tỉ lệ, không siêu tham số. DRLA-Net: Gaussian hóa hộp xoay, gán thô-tinh, "scale-aware analysis". CEM-FBGTinyDet: **P5–P6 thường không nhận anchor dương nào** nên đặc trưng mức cao không được huấn luyện | Lớp gán nhãn cho vật tí hon rất đông. Quan sát "mức cao không có mẫu dương" là **mặt kia** của bài toán phủ: hướng A mới đo phủ ở mức thấp. Có thể bổ sung "phủ theo từng mức" vào RQ2 |
| **Biểu diễn / bất định góc** | angle, uncertainty, oriented, small | **AQE-detector** (Sci Rep 2025, DOI 10.1038/s41598-025-31034-w); O2-DETR (TGRS 2026) | AQE: góc mô hình bằng **Gaussian tuần hoàn**, ngầm ước lượng độ tin cậy góc, dùng trong **NMS theo chất lượng góc** (NMS-AQ). Abstract không nói tới kích thước | Thu hẹp thêm C-17: "phân phối góc + dùng độ tin cậy khi giải mã" đã có. Phần còn khác chỉ là **điều kiện theo kích thước pixel** và cận dẫn xuất. Phải thêm AQE vào đối chứng (→ C-18) |
| **Giám sát yếu HBB→OBB, điểm** | horizontal box supervised, weakly supervised oriented, point-supervised | Wholly-WOOD (TPAMI 2025); ABBSPO (arXiv 2512.10031); RSAR/UCR (arXiv 2501.04440); PointOBB-v2 (arXiv 2410.08210); Point Teacher (ISPRS 2025, arXiv 2412.05837); HODet (Sci Rep 2026, miền ký tự thước mớn nước tàu, không phải ảnh trên không) | Wholly-WOOD: chỉ dùng HBox vẫn gần bằng mô hình train bằng RBox. ABBSPO: dùng tiền nghiệm **đối xứng** để học góc. UCR: ràng buộc vòng tròn đơn vị cho mã hóa sin/cos. Point Teacher: điểm cho vật tí hon, xử lý nhiễu do mơ hồ tỉ lệ, chạy trên AI-TOD-v2, SODA-A, TinyPerson | Nhãn OBB của AI-TOD-R vốn sinh bằng H2RBox-v2 (giám sát yếu). Câu hỏi mở: **giám sát góc yếu có kém đi theo kích thước không**, khi tín hiệu đối xứng/hình dạng biến mất ở vật vài pixel? Cặp AI-TOD-v2 (HBB) / AI-TOD-R (OBB) là chỗ thử tự nhiên |
| **Nhiễu nhãn** | label noise, noisy annotations, tiny | Point Teacher; RGBT position shift (arXiv 2502.09311) | Lệch vị trí nhỏ giữa modality được coi như nhiễu nhãn ở vật tí hon | Củng cố giả thuyết "lỗi định vị một phần do nhãn" (deep-study chương trình C, C-8) |
| **Độ phân giải / SR / chưng cất** | super-resolution, distillation, high-resolution features, tiny | **CSCWD** (arXiv 2609.30395); **CoLR-Det** (arXiv 2601.12507); DPNet (IEEE IoT J 2025); **VGTok** (arXiv 2608.28706); B2BDet (arXiv 2401.14661) | CSCWD: chưng cất từ **teacher YOLO11m-P2 sang student YOLO11n ở P3**, không đổi kiến trúc suy luận; +2,92 mAP@0.5 trên Drone-vs-Bird. CoLR-Det: SR chỉ dùng khi train như bộ điều chuẩn, phê phán kiểu "phục hồi ảnh trước rồi mới phát hiện". DPNet: hệ số giảm mẫu thích nghi theo ảnh. VGTok: chọn độ mịn token theo vùng; **AI-TOD-v2 37,27 AP, 19,51 AP_vt** với Co-DETR + ViT-L | **Giải thích cạnh tranh trực tiếp với hướng A**: lỗi dưới-stride có thể sửa ở mức **đặc trưng** (chưng cất P2→P3, SR khi train) thay vì nới vùng ứng viên. VGTok cho thấy detector mạnh ở độ phân giải gốc nâng mốc rất cao, nên claim "kiến trúc tốt hơn" trên AI-TOD-v2 rất khó với GPU Kaggle |
| **Mật độ / NMS / truy vấn** | dense, crowded, counting, density map, query | DQ-DETR (arXiv 2404.03507); DRMNet (arXiv 2512.22949); D³R-DETR (arXiv 2601.02747); Dome-DETR (đã có trong notes) | Dùng bản đồ mật độ / đếm để chỉnh số query và tập trung tính toán; báo cáo trên AI-TOD hoặc AI-TOD-v2 | Giả thuyết "lỗi do mật độ / xung đột" có prior mạnh ở họ DETR. Với YOLO, mật độ tác động qua xung đột gán nhãn và `max_det`, đã nằm trong RQ2 |
| **Ngữ cảnh / nền** | context, background, tiny | RareSpot+ (arXiv 2604.20000); DCEDet (GSCEM); PRNet (arXiv 2510.09531) | Nhất quán đa tỉ lệ, augmentation theo ngữ cảnh; giữ thông tin nông gốc | Chưa thấy phép thử tách "ngữ cảnh giúp" khỏi "nền đi tắt" (deep-study đã nêu) |
| **Metric / hồi quy** | metric, IoU, Wasserstein, similarity measure | InterpIoU (arXiv 2507.12420); GCD, SimD (đã có trong notes); Tiny Focal Loss (Traitement du signal 2026) | InterpIoU: penalty hình học của các loss IoU nhạy với kích thước, có hại cho vật nhỏ. TFL: trọng số theo diện tích tuyệt đối | Độ nhạy IoU của vật vài pixel (lệch 1 px ⇒ IoU 0,6 với w = 4) là vấn đề chung. Đổi metric để thắng là bẫy (deep-study §2.3) |
| **Chuyển miền / GSD** | ground sample distance, cross-domain, small | VehAnchor (arXiv 2603.04277); 2504.06330 (LoRA few-shot, chỉ tiêu đề); VFM-guided source-free (arXiv 2508.11167, chỉ tiêu đề) | VehAnchor: suy GSD từ **độ dài modal của xe nhỏ trong OBB**, sai số GSD trung vị 6,87% trên DOTA-v1.5 | OBB của vật nhỏ mang thông tin **thang đo vật lý**. Gợi một hướng phụ: kích thước pixel so với kích thước thật (deep-study §2.1) |
| **Foundation / open-vocabulary** | open-vocabulary, foundation model, SAM, vision-language | DisDop (arXiv 2605.24639); DroneFINE (arXiv 2607.00338, chỉ tiêu đề); SegEarth-OV3 (arXiv 2512.08730, chỉ tiêu đề); **AVODDiag** (arXiv 2607.02718) | AVODDiag: dùng mô hình sinh ảnh tạo testbed có thuộc tính kiểm soát; xu hướng trên dữ liệu tổng hợp **khớp** điểm yếu thực ở 3 detector, 3 dataset | Công cụ chẩn đoán có kiểm soát (kích thước, góc, nền) có thể dùng để dựng "đường cong khả năng xác định". Nhưng dữ liệu tổng hợp không thay được dữ liệu thật |
| **Augmentation / phân bố** | augmentation, copy-paste, sampling, tiny | AD-Det (Remote Sens. 2025); 2509.17078; DPNet | Copy-paste cân bằng lớp đuôi quanh cụm vật nhỏ; phóng ảnh + augmentation giúp YOLOv8 | AI-TOD-R lệch lớp mạnh (vehicle ≈ 88%). Mất cân bằng lớp là một giải thích cạnh tranh cho AP_vt thấp, chưa có trong RQ |
| **Video / UAV / event** | video, temporal, tracking, tiny, UAV | RGBT-Tiny (TPAMI 2025); PointEvent (arXiv 2609.20066); frame dynamics tracker (arXiv 2505.04917) | RGBT-Tiny: 115 cặp chuỗi, 93K frame, 1,2M nhãn, **> 81% vật < 16×16**, có ID | Dataset tiny có thời gian, nhưng là **HBB**. Liên quan chương trình B của deep-study, không phải OBB |
| **Miền tần số / module** | frequency, wavelet, spectral | FMC-DETR (tiêu đề), EFSI-DETR, D³R-DETR, FANet (tiêu đề), dual-stream spectral distillation (TGRS 2025, tiêu đề) | Nhiều module tần số mới 2025–2026 | Lớp module rất đông; khó là đóng góp riêng |
| **YOLO trên dữ liệu nhỏ dày** | YOLO26, YOLOv8, VisDrone, oriented small | **YOLO26 vs YOLOv8** (arXiv 2605.24831); SPOD-YOLO (Remote Sens. 2025) | Trên VisDrone (> 75% vật dưới 2.000 px²), YOLO26-x 0,224 so với YOLOv8-x 0,214 mAP50:95: khác biệt nhỏ. SPOD-YOLO dựng dataset máy bay nhỏ có OBB | Bằng chứng gián tiếp: gói thay đổi của YOLO26 (trong đó có STAL) **không tạo khác biệt lớn** trên dữ liệu nhỏ dày dạng HBB. Bị nhiễu vì nhiều thay đổi cùng lúc. Nhất quán với dự báo của hướng A là hiệu ứng gán nhãn nhỏ |

**Thống kê quét:** vòng 1 có 16 truy vấn; vòng 2 có 8 (truy vấn "SODA-A" hỏng vì arXiv tách chữ, bỏ qua); OpenAlex 7. Khoảng 45 nguồn mới chưa có trong `notes/`: 35 mã arXiv và 10 bài journal (OpenAlex) đọc abstract, số còn lại chỉ xem tiêu đề (đã ghi rõ ở từng dòng). Truy vấn F02 (angle × tiny) chủ yếu trả bài ngoài lĩnh vực. Đây là giới hạn của keyword `abs:`, không có nghĩa lĩnh vực trống.

---

## 2. Bảng giả thuyết cạnh tranh cho hiện tượng "vật tí hon thất bại" — không xếp thắng thua

Mỗi giả thuyết có một **dấu hiệu** phân biệt và một **phép thử rẻ nhất** dùng được với dữ liệu hiện có. Cột chi phí giúp chọn thứ tự đo, **không** phải mức độ quan trọng.

| Mã | Giả thuyết [design] | Dấu hiệu nếu đúng | Phép thử rẻ nhất | Chi phí | Prior liên quan |
|---|---|---|---|---|---|
| H-cov | Thiếu ứng viên / mẫu dương (hướng A) | Recall tăng mạnh ở bin 2–8 px khi đổi A0 → A2/A8; GT rỗng giảm | RQ2 offline + giai thừa A0/A1/A2/A8 | nhãn: 0 GPU; run: ~15 run | STAL, OSCAR, MCSA, DALA |
| H-feat | Đặc trưng P3 quá thô, kể cả khi đã đủ ứng viên | Có ứng viên (A8) mà recall vẫn thấp; chưng cất P2→P3 hoặc đầu P2 cải thiện thêm | A8 so với A8 + chưng cất từ teacher P2 (kiểu CSCWD) | 2–4 run + 1 teacher | CSCWD, QueryDet, CoLR-Det, VGTok |
| H-loc | Định vị lệch vài pixel làm rớt IoU cao | AP50 ổn nhưng AP75 sụp ở bin tí hon; FP do định vị kém chiếm ưu thế | Tách AP theo ngưỡng IoU × bin từ output AITODReval của baseline | 0 GPU thêm | InterpIoU, NWD, GCD |
| H-angle | Góc không xác định được ở vật nhỏ (C-17) | Sai số góc có điểm gãy theo cạnh dài; nhãn góc co về vài giá trị ở bin nhỏ | Thống kê góc nhãn theo bin (0 GPU); sai số góc theo bin trên run A2 | 0 GPU → G4 | IGOFormer, O2-DETR, AQE, CODrone |
| H-label | Nhãn tí hon nhiễu (H2RBox-v2 sinh OBB) | Lệch giữa HBB của AI-TOD-v2 và bao ngoài OBB của AI-TOD-R tăng ở bin nhỏ; lỗi tập trung ở lớp khó gán nhãn | So cặp nhãn AI-TOD-v2/AI-TOD-R trên cùng ảnh (0 GPU, có confound vì OBB sinh từ HBB) | 0 GPU | DN-TOD, Point Teacher, Wholly-WOOD |
| H-dense | Mật độ: xung đột gán nhãn, giới hạn phát hiện, NMS | Recall giảm theo mật độ cục bộ ở cùng kích thước | Hồi quy recall từng GT theo mật độ × kích thước (đã có trong RQ2) | 0 GPU thêm | DQ-DETR, DRMNet, AITODReval maxDets |
| H-imb | Mất cân bằng lớp / gradient | AP_vt thấp do lớp hiếm, không do kích thước | AP theo lớp × bin; so lớp vehicle với lớp hiếm cùng bin | 0 GPU thêm | AD-Det (DCC), TFL, CEM-FBGTinyDet |
| H-ctx | Nền và ngữ cảnh đánh lừa | FP tập trung ở loại nền nhất định; che ngữ cảnh làm đổi điểm | Phân loại FP theo vùng nền; phép thử che ngữ cảnh | thấp | RareSpot+, DCEDet |

**Nhận xét cấu trúc** [suy luận]:
- Từ **một baseline + nhãn** đo được sáu dấu hiệu (H-cov phần offline, H-loc, H-angle phần nhãn, H-label, H-dense, H-imb). Chỉ H-feat và phần run của H-cov cần thêm GPU.
- Vì vậy thứ tự hợp lý là **đo phân rã lỗi trước, chọn giả thuyết sau**. Cách này khớp quy trình deep-study ("chọn đúng nguyên nhân trước khi chọn kiến trúc") và không buộc nhóm cược vào C-16 hay C-17.
- Các giả thuyết **không loại trừ nhau**: nhiều nguyên nhân có thể cùng góp phần. Kết quả hữu ích là một "ngân sách lỗi" cho biết mỗi nguyên nhân chiếm bao nhiêu, ở bin nào.

---

## 3. Những điều lượt quét làm thay đổi (và không thay đổi)

**Thay đổi:**
1. **C-17 hẹp hơn.** AQE-detector (Sci Rep 2025) đã có phân phối góc tuần hoàn + NMS theo chất lượng góc. Cộng thêm O2-DETR (ADR) và Unc-SOD (chọn mẫu theo bất định), phần còn lại của C-17 chỉ là **điều kiện theo kích thước pixel** (cận dẫn xuất + đo điểm gãy). Ghi REVISION C-18.
2. **Hướng A có thêm một đối thủ giải thích.** Chưng cất chéo tỉ lệ P2→P3 (CSCWD) xử lý cùng triệu chứng "vật dưới stride" ở mức đặc trưng, không đụng tới gán nhãn. Nếu A8 đủ ứng viên mà recall vẫn thấp thì nguyên nhân nằm ở đặc trưng. Đề nghị thêm nhánh đối chứng này **nếu còn GPU**. Đây là gợi ý thiết kế, không đổi claim C-16.
3. **Mốc SOTA trên AI-TOD-v2 rất cao** (VGTok 37,27 AP với ViT-L ở độ phân giải gốc). Củng cố nhận định 14/10: đua "kiến trúc tốt hơn" không hợp nguồn lực của nhóm.

**Không thay đổi:**
- Không có bài nào trong lượt này đo các phiên bản STAL trên OBB hoặc AI-TOD-R. RQ2 của hướng A vẫn trống trong phạm vi quét (abstract).
- Không có bài nào gắn khả năng xác định góc với kích thước pixel (abstract).
- Nút thắt dữ liệu tiny OBB vẫn còn. Dataset tiny mới tìm thấy (RGBT-Tiny) là HBB; dataset máy bay nhỏ của SPOD-YOLO chưa xác minh.

---

## 4. Danh sách đọc tiếp đề xuất (theo câu hỏi, không theo hướng thắng)

| Ưu tiên | Bài | Vì sao | Trả lời câu hỏi nào |
|---|---|---|---|
| 1 | AQE-detector (Sci Rep 2025, open access?) [chưa xác minh OA] | Đối chứng sát nhất cho C-17: phân phối góc + NMS theo chất lượng | Đầu góc có độ tin cậy đã làm tới đâu; có phân tích theo kích thước không |
| 2 | CSCWD (arXiv 2609.30395) | Đối chứng mức đặc trưng cho hướng A, cùng họ YOLO11 | Lỗi dưới-stride sửa bằng đặc trưng được bao nhiêu |
| 3 | CEM-FBGTinyDet (arXiv 2506.09897) | Quan sát "P5–P6 không có mẫu dương" | Phủ theo từng mức có nên vào RQ2 không |
| 4 | Wholly-WOOD (TPAMI 2025) và ABBSPO | Giám sát góc yếu; nhãn AI-TOD-R sinh bằng H2RBox-v2 | Góc học từ HBB có kém đi theo kích thước không |
| 5 | YOLO26 vs YOLOv8 (arXiv 2605.24831) | Bằng chứng độc lập về YOLO26 trên dữ liệu nhỏ dày | Kỳ vọng hiệu ứng của gói YOLO26/STAL |
| 6 | VGTok (arXiv 2608.28706) | Mốc trần ở độ phân giải gốc; cách cấp token theo vùng | Chương trình A của deep-study (thiếu chi tiết hay học kém) |
| 7 | AVODDiag (arXiv 2607.02718) | Chẩn đoán có kiểm soát bằng ảnh sinh | Có dựng được đường cong khả năng xác định có kiểm soát không |

---

## 5. Nguồn (đã truy cập 14–15/10/2026)

- arXiv API (`https://export.arxiv.org/api/query`): 24 truy vấn; kết quả thô và abstract lưu ở scratchpad phiên (`scan.json`, `scan2.json`), không đưa lên repo.
- OpenAlex (`https://api.openalex.org/works`): 7 truy vấn, abstract dựng lại từ inverted index (`oa.json`, scratchpad).
- DOI đã thấy trong OpenAlex: AQE-detector 10.1038/s41598-025-31034-w; DRLA-Net 10.1109/lgrs.2025.3636153; DCEDet 10.3390/rs17162876; HODet 10.1038/s41598-026-58703-8; RGBT-Tiny 10.1109/tpami.2025.3544621; SPOD-YOLO 10.3390/rs17243963; Tiny Focal Loss 10.18280/ts.430124; HITL rotation-aware small object 10.1038/s41598-026-72931-y; WSOOD-GAEN 10.3390/rs18081253.
- Mã arXiv đã đọc abstract: 2605.24831, 2502.09471, 2512.10031, 2501.04440, 2410.08210, 2608.05858, 2412.05837, 2502.09311, 2601.12507, 2504.05601, 2609.30395, 2404.03507, 2604.20000, 2405.11276, 2603.04277, 2607.02718, 2605.24639, 2509.17078, 2505.02797, 2409.05624, 2601.02747, 2601.18597, 2506.09897, 2507.13120, 2505.04917, 2609.20066, 2401.14661, 2507.00825, 2608.28706, 2603.05905, 2510.09531, 2512.22949, 2505.21868, 2507.19059, 2507.12420.

## Thuật ngữ (Glossary)

| English | Tiếng Việt | Giải thích ngắn |
|---|---|---|
| competing hypotheses | giả thuyết cạnh tranh | Nhiều nguyên nhân có thể cùng giải thích một hiện tượng; cần phép thử phân biệt |
| failure budget / error decomposition | ngân sách lỗi / phân rã lỗi | Chia tổn thất hiệu năng cho từng nguyên nhân (phủ, đặc trưng, định vị, góc, nhãn, mật độ…) |
| cross-scale distillation | chưng cất chéo tỉ lệ | Teacher có đầu độ phân giải cao (P2) truyền tri thức cho student ở mức thô hơn (P3) |
| weakly supervised oriented detection | phát hiện có hướng giám sát yếu | Học hộp xoay từ nhãn hộp ngang hoặc điểm |
| angle quality estimation | ước lượng chất lượng góc | Mô hình độ tin cậy của góc dự đoán và dùng nó (ví dụ trong NMS) |
| native resolution | độ phân giải gốc | Xử lý ảnh không thu nhỏ trước khi vào mạng |
