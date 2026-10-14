# Hướng A (C-11) đủ khả thi cho claim Q4 chưa, có lên được Q3 không?

> **Đính chính 15/10/2026 — C-19:** đọc [audit mới](../07-audits/t07-q2-audit-2026-10-15/REPORT.md) trước khi dùng kết luận dưới đây. Giữ phần prior OSCAR/MCSA; rút cách suy venue từ T1 và yêu cầu √2s dự báo sàn AP tối ưu. Cận phủ chỉ nói về candidate với giả định lưới/biên; cùng kỳ vọng số candidate không bảo đảm cùng xác suất rỗng hoặc hiệu ứng AP nhỏ. Nội dung phía dưới được giữ để truy lịch sử, không phải đánh giá venue hiện hành.

| Trường | Giá trị |
|---|---|
| Đề tài / claim | #7, hướng A = C-11 (YOLO-OBB trên AI-TOD-R, giai thừa A0/A1/A2/A8, OA-STAL v2 là phép thử phụ) |
| Worker | admin → research-admin; đánh giá theo `research-proposal-integrity.md` §1–§5 |
| Ngày | 2026-10-14 |
| Nguồn nội bộ đã đọc lại | `notes/claims-ledger.md` (C-10, C-11, C-12); `notes/02-proposal/t07-c3-proposal-v2-EN.md` (v2.1); `notes/05-venue-direction/t07-critique-q2-2026-10-11.md`; `notes/02-proposal/t07-c3-novelty-rescan.md`; `notes/02-proposal/t07-c3-evidence-dossier.md`; `notes/03-foundation/t07-dl-digest-2026-10-11.md`; `ROADMAP.md`; 21 issue trên GitHub |
| Nguồn mới trong phiên | MCSA toàn văn (Europe PMC); OSCAR toàn văn (arXiv 2212.08472v2, Crossref xác minh TGRS 2023); abstract MFN-Net, ARA, DALA (Semantic Scholar/Crossref); arXiv API 6 truy vấn; OpenAlex + Semantic Scholar danh sách bài trích AI-TOD-R; trang JEIT (CDCEDet) thử lại, không truy cập được |
| Trạng thái dự án | **Chưa chạy thí nghiệm nào.** Mọi số AP dưới đây là [tác giả báo cáo] |

Nhãn: [tác giả báo cáo] · [đã kiểm trong phiên] · [derived] · [suy luận] · [chưa xác minh].

---

## 1. Kết luận ngắn

**Q4 / hội nghị Scopus: thiết kế đủ tầm, nhưng CHƯA khả thi theo nghĩa của cổng §5.**
- Về nội dung, lõi C-11 vẫn bảo vệ được ở dải T1 (workshop / hội nghị Scopus / Q4). Lần quét này không tìm thấy công trình nào đã đo các phiên bản STAL trong bước điểm-trong-hộp của YOLO trên AI-TOD-R.
- Về thực thi, 4/4 mục của cổng khả thi (dữ liệu, tính toán, baseline, phụ thuộc) chưa được xác minh ngày 14/10. Cổng 0 (hạn 13/10) đã quá hạn. Vì vậy claim Q4 hiện là **claim có điều kiện chưa được thỏa**, không phải claim đã đạt.
- Có một prior mới phải thêm vào định vị: **OSCAR (IEEE TGRS 2023)** đã quét kích thước pseudo-box {không, s, 1,5s, 2s} cho mục tiêu nhỏ hơn stride và thấy tối ưu không đơn điệu. Điều này **không hạ tier** nhưng thu hẹp phần mới của so sánh chính, nên ghi REVISION C-16 (§6).

**Q3: có thể về nguyên tắc, khả năng thấp, không thể trước 08/11/2026.**
- Theo rubric §1, dải bảo vệ được của T1 dừng ở Q4. Q3 là nấc **trên dải**, chỉ hợp lệ khi kèm điều kiện nêu ngay trong claim.
- Điều kiện thực tế: hiệu ứng có ý nghĩa thống kê, đúng mẫu hình dự báo trên **2 dataset độc lập nguồn**, và luật phủ √2·s dự báo đúng mức sàn tốt nhất trên cả hai. Dataset thứ hai hiện chưa có phương án đã xác minh (§4.2).
- Đường lên Q3 thực tế hơn là nhánh T2 C-7′ (C-12), không phải thêm độ rộng cho bản T1.

---

## 2. Hướng A đứng ở đâu so với các bài cạnh tranh (đọc lại 14/10)

| Bài | Mức đọc | Kiến trúc / cơ chế | Dataset | Chạm vào phần nào của hướng A |
|---|---|---|---|---|
| **MCSA**, Sci. Rep. 15:22455 (2025), DOI 10.1038/s41598-025-05772-w | **toàn văn** (Europe PMC PMC12216963) [đã kiểm trong phiên] | Khung RetinaNet-OBB (MMRotate, R50-FPN pretrain ImageNet, chỉ lật ngang; 12 epoch trên DOTA-v1.0/v2.0, 40 epoch trên DOTA-v1.5 và DIOR-R). Ba phần: (1) DPB: dilated conv (hệ số 3) + 2 dynamic snake conv + offset guidance ở các lớp cuối của head, dịch vị trí prior vào trong vật thể; (2) metric chọn mẫu t = s + u + d (điểm lớp + IoU + khoảng cách tâm chuẩn hóa), top-k = 12; (3) DGMM lọc mẫu xa tâm (như DCFL), g = 0,6 | DOTA-v1.0/1.5/2.0, DIOR-R. **Không** AI-TOD-R, **không** YOLO, **không** STAL | Cùng lớp "gán mẫu cho vật thể tí hon có hướng", nhưng đổi cả kiến trúc head (DPB) và dùng anchor box. **Không chiếm RQ2.** Ablation DOTA-v2 val: baseline 51,70 → chỉ AAM 55,40 → đủ 3 phần 61,68 mAP; test 51,86 so với RetinaNet-O 46,68 [tác giả báo cáo; bài không nêu số seed hay phương sai] |
| **OSCAR**, IEEE TGRS 2023, DOI 10.1109/tgrs.2023.3243062 (arXiv 2212.08472v2) | **đọc §IV-A và §V-B Bảng II** [đã kiểm trong phiên] | Detector anchor-free cascade cho mục tiêu hồng ngoại nhỏ; ablation ASPB dùng FCOS rút gọn chỉ 1 mức dự đoán. **ASPB**: nếu h·w < s² thì thay GT bằng pseudo-box p×p cùng tâm, chỉ cho phép gán vị trí. Tác giả viết: khi p = s thì "at least one feature point will be labeled as positive" | SIRST-V2 (hồng ngoại, HBB; mật độ mục tiêu thấp hơn AI-TOD-R [suy luận, chưa đo]) | **Gần nhất với so sánh chính A0/A8/A2**: Bảng II quét p ∈ {không, s, 1,5s, 2s} → AP 71,9 / 75,6 / **77,6** / 71,2 [tác giả báo cáo]. Pseudo-box quá lớn (2s) còn kém hơn không làm gì. Đây là prior trực tiếp cho câu hỏi "sàn bao nhiêu là đủ" |
| **YOLO26 Bảng 6** (arXiv 2606.03748v1) | toàn văn (đã đọc trước) | STAL với s_ref ∈ {8, 16, 32}, YOLO11s, COCO | COCO, HBB | AP_S: TAL 29,0; s_ref 8: 27,7; 16: 29,6; 32: 28,3 [tác giả báo cáo, không báo phương sai]. Cũng không đơn điệu |
| **MFN-Net**, Remote Sens. Lett. 17 (2026) 801–813 | **abstract** (Semantic Scholar); toàn văn sau paywall | MFEAF (hợp nhất đa tỉ lệ có trọng số thích nghi) + **SFLA**: gán nhãn theo khoảng cách tương đồng, lọc theo tỉ lệ cạnh, ghép động để vật nhỏ có đủ mẫu dương | **SODA-A, AI-TOD** | +1,9 AP (SODA-A), +1,1 AP (AI-TOD) so với SOTA [tác giả báo cáo]. Chạm OA-STAL (phép thử phụ, tỉ lệ cạnh) và **chiếm đúng dataset thứ hai dự kiến (SODA-A)**. Họ detector và loại hộp không nêu trong abstract [chưa xác minh] |
| **ARA**, IEEE GRSL 21 (2024), DOI 10.1109/LGRS.2024.3432810 | abstract | Đưa tỉ lệ cạnh GT vào điểm chất lượng ứng viên + angle loss căn theo tỉ lệ cạnh | DOTA, HRSC2016 | Chạm OA-STAL; không tiny, không AI-TOD-R |
| **DALA**, CAAI Trans. Intell. Technol. (2025), DOI 10.1049/cit2.70083 | abstract (trang Wiley trả 403) | Khoảng cách tương đồng + chọn số mẫu dương theo tỉ lệ + loss trọng số động, "không siêu tham số" | "four widely used datasets", không nêu tên trong abstract | Cùng lớp gán nhãn cho tiny; loại hộp và dataset [chưa xác minh] |
| **CDCEDet**, J. Electron. Inf. Technol. 2026, DOI 10.11999/JEIT260317 | **không đọc được** (ngày 14/10: 3 lần curl tới jeit.ac.cn timeout + 1 lần WebFetch timeout; ngày 08/10: 3 lần timeout) | Theo snippet ngày 08/10: anchor thích nghi tỉ lệ + ngưỡng IoU theo phân vị cho tiny | AI-TOD-R (theo snippet) | **Rủi ro chồng lấn lớn nhất còn mở.** Vẫn là downgrade trigger của C-11 |

**Quét độ mới 14/10** [đã kiểm trong phiên]:
- arXiv (sắp theo ngày nộp): `abs:STAL AND abs:YOLO` 6 kết quả, `abs:"small-target-aware"` 6, `"label assignment" AND tiny AND (oriented OR rotated)` 2, `"label assignment" AND stride AND (tiny OR small)` 0, `YOLO26 AND (oriented OR OBB OR rotated)` 5, `"oriented tiny" OR "tiny oriented"` 3. **Không có bài mới nào sau 12/10**, không bài nào đo STAL trên OBB hoặc AI-TOD-R.
- Bài trích AI-TOD-R (OpenAlex 7 + Semantic Scholar 10): mới so với 08/10 có DORA (TPAMI 2026, phục hồi đặc trưng), SFDNet (tách phổ), SCON (change detection, chỉ xem tiêu đề, không có abstract), TinySet-9M/DEAL (point prompt), UAVNet-MS. **Không bài nào thay đổi bước gán nhãn của YOLO-OBB trên AI-TOD-R** (đọc abstract).
- Giới hạn: không truy cập CNKI/Wanfang; CDCEDet vẫn chưa đọc. "Không thấy" ở đây nghĩa là không thấy trong các truy vấn này.

---

## 3. Câu 1 — Đủ khả thi cho claim Q4 chưa?

### 3.1 Về nội dung (nếu chạy được thì có đáng một bài Q4/hội nghị không)

**Có, với một điều chỉnh định vị.** Lý do:

1. **RQ2 vẫn trống** trong phạm vi đã quét: không công trình nào đo các phiên bản STAL (không sàn → < 8 → < 16) trong bước điểm-trong-hộp nhiều mức của YOLO, trên một benchmark tiny OBB, với evaluator chính thức. MCSA dùng anchor box + đổi head; OSCAR là HBB hồng ngoại, ablation 1 mức; MFN-Net/ARA không nhắm STAL.
2. **So sánh chính A0/A1/A2/A8 có prior hỗ trợ là sẽ ra tín hiệu**, không phải đo trong nhiễu:
   - OSCAR thấy chênh 6,4 AP giữa p = 1,5s và p = 2s, và 3,7 AP giữa không sàn và p = s [tác giả báo cáo, SIRST-V2, ablation 1 mức].
   - YOLO26 Bảng 6 thấy AP_S dao động 1,9 điểm theo s_ref [tác giả báo cáo, COCO].
   - Trên AI-TOD-R, hộp 4×4 dưới TAL có P(không ứng viên) ≥ 0,67 [derived, Proposition 1; mô phỏng 0,671]. Bin very tiny vì vậy gần như chắc nhạy với sàn [suy luận].
   - Hai prior cho dấu khác nhau ở đoạn giữa (OSCAR: p = s tốt hơn không sàn; COCO: s_ref = 8 kém hơn TAL). **Dấu của A8 so với A2 trên AI-TOD-R thật sự chưa biết**, đúng loại câu hỏi đáng chạy [suy luận].
3. **Điểm yếu nội dung phải sửa trước khi viết:**
   - "Sàn quan trọng và có tối ưu không đơn điệu" **không còn là phát hiện mới** (OSCAR 2023, YOLO26 Bảng 6). Phần có thể mới chỉ là: (a) điều kiện phủ **bất biến theo góc** cho hộp xoay, (b) kiểm nó trong cảnh dày với đo xung đột, (c) lịch sử phiên bản STAL.
   - OA-STAL v2 (giữ dáng) nằm trong lớp cơ chế đã đông (EARL, SARFA-Net, RDCNet, ARA, MFN-Net) và theo Hệ quả 2 chỉ cho hiệu ứng bậc hai; giữ làm phép thử phụ là đúng.

**Điều kiện phủ cho hộp xoay [derived].** Điểm neo nằm trên lưới vuông bước s (lệch nửa ô không ảnh hưởng vì phép tịnh tiến).
- Hộp **ngang** có cả hai cạnh ≥ s luôn chứa ít nhất 1 điểm neo: mỗi đoạn chiếu dài ≥ s trên trục x và trục y chứa ít nhất một tọa độ lưới. Đây là điều OSCAR dùng (p = s).
- Hộp **xoay** thì không đủ. Hình vuông cạnh a xoay 45° đặt tâm tại điểm xa lưới nhất (đỉnh ô) là tập |x| + |y| ≤ a/√2; các điểm lưới gần nhất cách nó s theo chuẩn L1. Hình vuông chứa điểm lưới khi và chỉ khi a/√2 ≥ s, tức a ≥ √2·s.
- Ngược lại, mọi hình chữ nhật có cạnh ngắn ≥ √2·s chứa hình tròn bán kính ≥ s/√2 (bằng bán kính phủ của lưới), nên luôn chứa điểm neo ở mọi vị trí và mọi góc.
- Vậy **√2·s là sàn theo cạnh nhỏ nhất bảo đảm có ứng viên với mọi góc**, và cận này chặt (trường hợp hình vuông 45°). Với s_min = 8: 11,31 px.
- Kiểm tra hợp lý: (i) s → 0 thì sàn → 0; (ii) thứ nguyên px; (iii) mô phỏng cũ: 10×10 dưới TAL có P(rỗng) = 0,006 > 0 (10 < 11,31), 16×16 có P(rỗng) = 0 [DOS §7.1]; (iv) code OBB dùng bất đẳng thức không chặt ≥/≤ [FREV §2], nên điểm nằm đúng trên biên được tính.
- Giới hạn: đây là điều kiện **đủ** cho mọi hình; với hộp dài, cạnh ngắn nhỏ hơn có thể vẫn đủ tùy góc và chiều dài. Bỏ qua biên ảnh và bước lọc GT < 2 px.

Hệ quả định vị: A8 nên trình bày là **"phiên bản bất biến theo góc của pseudo-box p = s trong OSCAR"**, không phải "ý tưởng sàn phủ tối thiểu" mới.

### 3.2 Về thực thi (cổng khả thi §5, trạng thái 14/10)

| Mục | Trạng thái | Nguồn |
|---|---|---|
| Dữ liệu | `labels.zip` chưa mở (Cổng 0 hạn 13/10 đã qua); có nhãn test không: chưa biết; đăng ký xView: chưa thấy ghi nhận (issue #4 mở) | ROADMAP; issue #4 |
| Tính toán | Tốc độ chưa đo; tài khoản Kaggle chưa xác minh (issue #3 mở) | issue #3, #7 |
| Baseline | Chưa có baseline nội bộ; RetinaNet-O chưa tái lập | issue #9 |
| Phụ thuộc | AITODReval chưa chạy; converter chưa viết; SODA-A chưa tải được | issue #8, #14 |

**→ Nhãn: "chưa chạy được như mô tả (not runnable as stated)".** Claim Q4 không bị bác, nhưng **chưa được kiếm**. Thời điểm sớm nhất biết claim Q4 đứng được là Cổng 2 (21/10). Điều kiện đọc toàn văn của C-11: MCSA xong 14/10; MFN-Net, ARA, CDCEDet chưa.

---

## 4. Câu 2 — Có lên Q3 được không?

### 4.1 Theo rubric

- Rubric §1: T1 → workshop / hội nghị Scopus / Q4; T2 → Q2–Q3. Q3 cho một bài T1 là **nâng trên dải**, chỉ chấp nhận khi điều kiện nâng nêu cùng claim. C-11 đã làm đúng điều này ("Q3 only if …").
- Độ rộng (2 dataset, nhiều seed) **không nâng tier** (critique §5.4). Muốn Q3 với T1 thì bài phải cho người đọc một **nguyên lý chuyển được**, không chỉ một bảng xếp hạng.

### 4.2 Điều kiện cụ thể và mức khả thi

| Điều kiện cho Q3 (C-16) | Khả thi? | Căn cứ |
|---|---|---|
| Khoảng tin cậy của so sánh chính không chứa 0, đúng mẫu hình mật độ/cấu hình đã đăng ký trước | có thể (prior §3.1 cho thấy sàn tạo khác biệt cỡ vài AP ở dữ liệu tiny) | OSCAR Bảng II; YOLO26 Bảng 6 [tác giả báo cáo] |
| Lặp lại trên **dataset thứ hai độc lập nguồn** | **yếu**: SODA-A chưa tải được (OneDrive đòi đăng nhập, 08/10) và MFN-Net đã làm gán nhãn trên SODA-A; DOTA-v2 không độc lập nguồn với AI-TOD; CODrone (UAV, OBB, 10.004 ảnh 3840×2160) không công bố thống kê kích thước vật thể nên chưa biết phần GT bị sàn tác động | RESCAN §B.4; MFN-Net abstract; CODrone arXiv 2504.20032v1 [đã kiểm trong phiên] |
| Luật √2·s dự báo đúng mức sàn tốt nhất trên **cả hai** dataset (nguyên lý, không phải thắng một cấu hình) | chưa biết; là chỗ có thể biến bài T1 thành bài phân tích đáng đọc | §3.1 [derived + suy luận] |
| Đọc toàn văn MFN-Net, ARA, CDCEDet và định vị rõ | chưa (paywall / không truy cập được) | §2 |
| Thời gian | **không thể trước 08/11/2026**; sớm nhất quý I/2027 | đường găng ở critique §4.5 |

**Kết luận Q3:** khả thi về nguyên tắc, **xác suất thấp** [suy luận], phụ thuộc chủ yếu vào việc có dataset thứ hai đúng chế độ tiny và độc lập nguồn. Không nên đặt Q3 làm mục tiêu kế hoạch; giữ làm mức nâng nếu kết quả cho phép.

**Đường thay thế:** nhánh C-7′ (C-12, đổi đầu/biểu diễn góc theo kích thước) mới là ứng viên T2, dải Q3–Q2 có điều kiện, mở hay đóng ở Cổng 4 (01/11). Bản T1 nên được viết sao cho đo sai số góc theo kích thước "miễn phí" từ các run A2 (đã có trong ROADMAP).

---

## 5. Việc nên làm ngay (theo thứ tự)

1. **Qua Cổng 0 trong tuần này**: mở `labels.zip`, đếm nhãn test, phân bố kích thước, số GT < 2 px, số GT/ảnh lớn nhất. Không cần xView.
2. **Đăng ký xView ngay** nếu chưa làm; nếu đến 16/10 chưa duyệt thì chuyển giao thức AI-TOD-R-woX đã khai báo trong ROADMAP.
3. **Thêm OSCAR vào Bảng 1** của proposal và phần định vị; viết lại A8 thành "điều kiện phủ bất biến theo góc (√2·s)" kèm dẫn xuất §3.1.
4. **Preregistration (trước 21/10)**: vì hai prior cho dấu ngược nhau ở đoạn giữa, khai báo dự báo A8 so với A2 **theo tầng mật độ** (cảnh thưa: A8 ≈ A2; cảnh dày: A8 ≥ A2 do ít xung đột) và chấp nhận kiểm định hai phía, không đoán một dấu chung [design, cần thực nghiệm].
5. **Lấy toàn văn MFN-Net, ARA, CDCEDet** qua thư viện trường hoặc liên hệ tác giả; đặc biệt CDCEDet (cùng AI-TOD-R).
6. **Chốt dataset thứ hai trước 25/10**: thử lại SODA-A (BaiduNetDisk), kiểm thống kê kích thước của CODrone; nếu không có, khai báo bài một dataset (dải Q4/hội nghị).

---

## 6. Venue Claim Card

- **Proposal:** C-11 giữ nguyên thiết kế; so sánh chính A0/A1/A2/A8 được định vị lại là phép thử **điều kiện phủ bất biến theo góc** (√2·s_min) trong bước điểm-trong-hộp nhiều mức của YOLO trên tiny OBB dày đặc, có kiểm soát phiên bản STAL; OA-STAL v2 so với STAL-16 là phép thử phụ.
- **Novelty tier:** **T1** — chỉ đổi quy tắc gán nhãn khi train. Prior gần cho so sánh chính: OSCAR (pseudo-box p ∈ {s, 1,5s, 2s}, HBB hồng ngoại, ablation 1 mức); MCSA không chiếm RQ2.
- **Venue band:** workshop / hội nghị Scopus (ICORE2026 C–B, ví dụ IGARSS 2027, IJCNN 2027) / Q4. **Điều kiện:** qua Cổng 0–2 của C-11; RetinaNet-O trong 7,3 ± 1,0 hoặc chỉ claim nội bộ; trích và phân biệt OSCAR; đọc toàn văn MFN-Net, ARA, CDCEDet. **Q3 (trên dải T1) chỉ khi** thêm: khoảng tin cậy của so sánh chính không chứa 0, đúng mẫu hình mật độ/cấu hình đăng ký trước, trên 2 dataset độc lập nguồn, **và** điều kiện √2·s dự báo đúng mức sàn tốt nhất trên cả hai. Không đạt trước 08/11/2026. **Q2/Q1: không bảo vệ được.**
- **Downgrade triggers:** CDCEDet đã đo gán nhãn kiểu YOLO trên AI-TOD-R; `labels.zip` không có nhãn test; không có ảnh sau 21/10; mọi nhánh nằm trong nhiễu seed và RQ2 không có phát hiện cơ chế; dataset thứ hai không độc lập nguồn hoặc không có.
- **Confidence:** medium cho định vị (MCSA và OSCAR đọc toàn văn; CDCEDet chưa); **low** cho khả thi thực thi (chưa qua cổng nào); low cho Q3.
- **Ledger:** C-16, REVISION của C-11.

---

## Nguồn đã kiểm trong phiên (14/10/2026)

- MCSA: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12216963/fullTextXML (toàn văn; §Method, Bảng 3–12)
- OSCAR: https://arxiv.org/abs/2212.08472 (v2, §IV-A Eq.2, §V-B Bảng II); Crossref DOI 10.1109/tgrs.2023.3243062
- MFN-Net, ARA, DALA, "Learning from the waist": Semantic Scholar Graph API theo DOI + Crossref (abstract / metadata)
- CDCEDet: https://jeit.ac.cn/en/article/doi/10.11999/JEIT260317 — timeout, không đọc được
- CODrone: https://arxiv.org/html/2504.20032v1
- arXiv API: https://export.arxiv.org/api/query (6 truy vấn, sắp theo ngày nộp)
- OpenAlex `cites:W4416323921`, `cites:W4405470106`; Semantic Scholar citations của arXiv:2412.11582

## Thuật ngữ (Glossary)

| English | Tiếng Việt | Giải thích ngắn |
|---|---|---|
| pseudo-box (ASPB) | hộp giả | Hộp vuông cùng tâm thay GT nhỏ, chỉ dùng để chọn vị trí dương (OSCAR) |
| covering radius | bán kính phủ | Khoảng cách xa nhất từ một điểm tới điểm lưới gần nhất; lưới vuông bước s là s/√2 |
| orientation-invariant coverage condition | điều kiện phủ bất biến theo góc | Cạnh ngắn ≥ √2·s thì luôn có điểm neo ở mọi góc; hộp ngang chỉ cần ≥ s |
| above-band upgrade | nâng trên dải | Mức venue cao hơn dải mặc định của tier, chỉ hợp lệ kèm điều kiện |
| source-independent dataset | dataset độc lập nguồn ảnh | Không chung ảnh gốc với dataset chính (DOTA-v2 không độc lập với AI-TOD) |
| feasibility gate | cổng khả thi | Dữ liệu, tính toán, baseline, phụ thuộc phải được xác minh trước khi gọi đề xuất là chạy được |
