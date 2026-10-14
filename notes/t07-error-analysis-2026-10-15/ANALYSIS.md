# Phân tích phiên nghiên cứu NCKH #7 (14–15/10/2026): sai ở đâu, làm tốt ở đâu, vì sao

**Ngày viết:** 15/10/2026 · **Người viết:** chính phiên Claude Code bị phản biện (Opus 5.5; một lượt "recache" chạy Sonnet 5) · **Đối tượng:** ba note nghiên cứu ngày 14–15/10 và ba dòng ledger C-16, C-17, C-18 của dự án NCKH nhóm 7 (đề tài #7, vật thể tí hon trong ảnh trên không) · **Đầu vào phản biện:** bộ audit C-19 trong `notes/t07-q2-audit-2026-10-15/` của dự án. Bộ này do **một chat khác** làm, với ba worker: `angle_prior_sol` và `data_evidence_sol` (gpt-6.1-sol), `logic_critic_astra` (gpt-6-astra).

**Mục đích:** biết chính xác mình sai ở đâu, sai do đâu (do tôi, do skill hay do rule), và việc gì đáng giữ. Bản gốc của file nằm trong repo bộ skill (private), dùng làm đầu vào cho báo cáo đánh giá bộ skill. Bản trong repo này giữ phần liên quan tới cách làm nghiên cứu, để nhóm biết các kết luận ngày 14–15/10 sai ở đâu và vì sao.

**Không phải:** một bản đánh giá lại đề tài. Kết luận khoa học hiện hành của đề tài nằm ở `REPORT.md` của audit và ledger C-19, không ở đây.

Nhãn độ chắc:

| Nhãn | Nghĩa |
|---|---|
| **ĐO** | Đo bằng lệnh/script trong phiên này, có số liệu |
| **NGUỒN** | Đọc trực tiếp từ file/tài liệu, có vị trí |
| **QUAN SÁT** | Thấy trong phiên này, một lần |
| **SUY LUẬN** | Kết luận rút ra, chưa kiểm riêng |
| **CHƯA KIỂM** | Nghi vấn, cần kiểm |

---

## 0. Kết luận ngắn

1. Audit C-19 **đúng ở mọi điểm tôi kiểm lại được**: 4 phản bác toán học (chạy mô phỏng), phản bác về O2-DETR (đọc lại Eq.1–2), và 4 điểm mâu thuẫn với chính tài liệu của dự án (đọc lại file). Tôi chưa kiểm lại các phần dựa trên nguồn ngoài mà tôi chưa mở (AQE toàn văn, ATSS, JCR, CVPR, TGRS, số liệu CODrone/DroneVehicle) (§1).
2. Có 14 lỗi. Chỉ 3 lỗi là sai dữ kiện nguồn. **11 lỗi còn lại là sai suy luận hoặc sai khung câu hỏi**: dùng định lý ngoài phạm vi của nó, suy nhân quả từ một chỉ số, gán mức chắc cao hơn độ sâu đã đọc, và áp quy tắc venue mà chính dự án đã bỏ (§2).
3. Nguyên nhân lớn nhất **không phải thiếu đọc**. Có bốn cơ chế:
   - Rule venue toàn cục bắt mọi đề xuất phải có venue band, nên nó lấn quyết định của dự án.
   - Tôi chỉ đọc lại các dòng ledger nằm trên chuỗi claim đang xét, bỏ sót các dòng quy định phạm vi.
   - `hallucination-guard` chỉ kiểm nguồn và nhãn, không kiểm suy luận. Sau đó tôi vẫn báo người dùng là "không còn lỗi".
   - Không có người phản biện độc lập ở giai đoạn đề xuất.
   
   Có thêm một yếu tố đo được: phiên này chạy bản skill cài trong máy, khớp commit ngày 02/10, **chưa có** các thay đổi evidence-first ngày 04/10 trong repo (§3).
4. Việc đáng giữ:
   - Tìm ra OSCAR.
   - Tám giả thuyết cạnh tranh.
   - Nhận ra cặp nhãn AI-TOD-v2/R.
   - Định lý √2·s đúng.
   - Kiểm biên ≥/≤ trong code OBB đúng.
   - Ledger cùng các hộp đính chính giúp audit truy được từng lỗi (§4).
5. Audit C-19 sửa dự án nhưng **cố ý không sửa rule toàn cục**. Vì vậy phiên sau gọi `/admin` vẫn có thể lặp lại lỗi venue (§5).

---

## 1. Tôi đã tự kiểm lại audit như thế nào

### 1.1 Kiểm bằng mô phỏng (ĐO)

Script [`check_geometry.py`](check_geometry.py) trong thư mục này (chạy `python check_geometry.py`, chỉ cần thư viện chuẩn). Mỗi mục dùng 200.000 mẫu, riêng phép thử góc dùng 400.000 mẫu. Lưới bước s = 1, pha đều, hình chữ nhật đóng.

| Claim của audit | Kết quả đo | Kết luận |
|---|---|---|
| Hình vuông s×s và hình chữ nhật 2s×s/2 cùng E[N] = 1 nhưng P(N=0) là 0 và 1/2 | Vuông: E[N] = 1,000, P(N=0) = 0,000. Chữ nhật: E[N] = 1,001, P(N=0) = 0,4995 | Audit đúng. Cùng diện tích không cho cùng xác suất rỗng |
| Hình chữ nhật đóng có cạnh ngắn ≥ √2·s luôn chứa ít nhất 1 điểm lưới, ở mọi vị trí và góc | Thử 100.000 tư thế ngẫu nhiên: số điểm nhỏ nhất bằng 1 | Định lý của tôi đúng |
| Cận chặt tại hình vuông xoay 45° | Cạnh đúng √2, tâm ở tâm ô: 4 điểm nằm trên biên. Cạnh √2 − 10⁻⁶: 0 điểm | Đúng. Ở cận, kết quả phụ thuộc biên đóng/mở |
| Endpoint chỉ lệch vuông góc: \|Δθ\| ≤ arctan(2δ/L) và đạt được | L = 10, δ = 2: đo được tối đa 21,76°, cận 21,80° | Đúng |
| Endpoint lệch 2D theo chuẩn Euclid: cận là asin(2δ/L), lớn hơn arctan | Đo được tối đa 23,30°, cận asin 23,58° | Đúng. Với cách tôi viết "lệch tối đa δ px", arctan thậm chí **thấp hơn** trường hợp xấu nhất |

### 1.2 Kiểm bằng nguồn (NGUỒN)

- **O2-DETR:** đọc lại văn bản PDF đã tải (`dl_o2/o2.txt`, dòng 271 và 325).
  - Eq.(1): `Dol = Do0 + (Wr, Hr) · A(n)Pol(n)`.
  - Eq.(2): `Drl = Dr0 + (Wr, Hr, Wr, Hr) · A(n)Prl(n)`.
  - Cả hai phương trình có nhân với kích thước hộp. Câu tôi viết "phân phối **không phụ thuộc kích thước**" là sai.
- **Mâu thuẫn với tài liệu của dự án:** đọc lại từng file.
  - Ledger C-13 có câu "T1/T2 labels describe intervention only, not journal quartile".
  - Ledger C-15 có câu "Journal quartile is not a deterministic per-paper method grade".
  - `t07-dl-from-slides-VI.md:682` đã có đúng phản ví dụ 8×8 so với 16×4 (DIG §5.3, issue #21).
  - `t07-deep-study/RESEARCH-PROMPT.md` §1 có câu "Phân biệt rõ bài này với phát hiện chính chiếc drone bằng camera mặt đất".
- **CACHE-MANIFEST:**
  - 3 file scan, 31 truy vấn, 298 bản ghi trả về.
  - Manifest tự ghi rằng "≈45 nguồn" là con số tôi tự chọn và **chưa được tái dựng**.

### 1.3 Chưa kiểm (CHƯA KIỂM)

- Phần đọc Methods và Tables của AQE (ANGLE-PRIOR AP01).
- ATSS, JCR, hướng dẫn reviewer CVPR, scope TGRS (AUDIT RV01–RV05).
- Số liệu CODrone, DroneVehicle, CSCWD (DATA-AND-TRANSFER).

Tôi tin các phần này ở mức "tác giả audit báo cáo". Kết quả PASS của `REVIEW.md` chỉ là kiểm tính nhất quán trong phạm vi reviewer đã đọc. Bản thân REVIEW nói rõ nó chưa kiểm cache và chưa kiểm paper.

---

## 2. Mười bốn lỗi: tôi đã viết gì và sai vì sao

Viết tắt:

- **VA** = `t07-venue-assessment-2026-10-14.md`
- **QP** = `t07-q2-path-2026-10-14.md`
- **DM** = `t07-direction-map-2026-10-15.md`

Số dòng tính trên bản hiện tại, đã có hộp đính chính C-19 ở đầu file.

### A. Sai khung câu hỏi: trả lời trong khung venue mà dự án đã bỏ

| # | Tôi đã viết | Sai vì | Nhãn |
|---|---|---|---|
| E1 | VA:94 "Rubric §1: T1 → workshop / hội nghị Scopus / Q4; T2 → Q2–Q3". QP:24 "Một thuật toán gán nhãn tốt hơn vẫn là **T1**, dù tinh vi đến đâu". QP:25 "Phải dời điểm can thiệp … (T1) sang … (C-7′, T2 có điều kiện)" | Ledger C-13 và C-15 đã bỏ việc quy đổi tier sang quartile. RESEARCH-PROMPT §3 cấm nói "đủ Q1/Q2" khi chưa có bằng chứng. ATSS (CVPR 2020) là phản ví dụ cho việc coi mọi cải tiến assignment là đóng góp thấp | NGUỒN |
| E2 | QP:25 "Q2 cần thêm ≥ 3 dataset độc lập nguồn và ≥ 2 họ detector". QP:162 "không có đủ dataset độc lập (trần Q3)" | Không có quy định editorial nào như vậy. Con số này lấy từ mục tiêu thiết kế trong `t07-critique-q2-2026-10-11.md:33`. Tôi đã nâng nó thành "điều kiện Q2" rồi thành "trần Q3". Rule toàn cục cũng không nói con số 3: nó ghi "≥2 datasets" cho Q1 | NGUỒN |
| E13 | Tham số gọi `research-admin` ngày 14/10: "Đánh giá **hướng A** (claim C-11 …)" | "Hướng A" có hai nghĩa. Trong `RESEARCH-START-HERE.md` (13/10, điểm vào của dự án), "Ưu tiên A" là *tách tác động của scale khỏi cách học*. Tôi tự chốt nghĩa C-11 (STAL) và không hỏi lại, dù `workbench-conventions` §2 yêu cầu "ask once" khi mơ hồ | NGUỒN + QUAN SÁT. Người dùng định hỏi nghĩa nào: **CHƯA KIỂM** |

### B. Dùng toán ngoài phạm vi của nó

| # | Tôi đã viết | Sai vì | Nhãn |
|---|---|---|---|
| E3 | C-16 và VA §3.1/§4.2/§6 yêu cầu √2·s "dự báo mức sàn tốt nhất" | Định lý chỉ bảo đảm **có ứng viên**. Nó không nói gì về positive còn lại sau top-k, sau xung đột, về trọng số hay AP tối ưu (LOGIC-CRITIQUE §1, code TAL dòng 196–202 và 350–381) | NGUỒN + ĐO (định lý đúng, xem §1.1) |
| E4 | VA:65 "theo Hệ quả 2 chỉ cho hiệu ứng bậc hai". QP:27 "hiệu ứng bị Hệ quả 2 chặn" | Cùng kỳ vọng không có nghĩa cùng phân phối. Đáng chú ý hơn: **dự án đã sửa điều này trước đó** ở issue #21 và `t07-dl-from-slides-VI.md:682`. Tôi chép lại claim cũ từ proposal §6 | ĐO + NGUỒN |
| E5 | QP:64 "lệch tối đa δ px ở hai đầu trục dài L cho Δθ_max = arctan(2δ/L)". QP:67 đặt tên "identifiability-aware" | Đây là cận trên của độ nhạy, chỉ đúng khi endpoint lệch vuông góc. Nếu lệch 2D thì phải dùng asin. Cận này không phải sàn sai số, không phải khả năng xác định từ ảnh. Muốn nói về identifiability phải có mô hình tạo ảnh | ĐO |

### C. Mức chắc cao hơn độ sâu đã đọc

| # | Tôi đã viết | Sai vì | Nhãn |
|---|---|---|---|
| E6 | QP:82: O2-DETR "phân phối **không phụ thuộc kích thước**", gắn nhãn "toàn văn, quét từ khóa [đã kiểm trong phiên]". C-17 viết "O2-DETR full-text check" | Eq.1–2 nhân với (Wr, Hr). Grep theo từ "size/small/scale" không bắt được sự phụ thuộc viết bằng ký hiệu toán. Nhãn "toàn văn" làm người đọc hiểu là tôi đã đọc phần method | NGUỒN |
| E7 | DM:68 "phần còn lại của C-17 chỉ là **điều kiện theo kích thước pixel**", rồi ghi REVISION C-18 dựa trên AQE "abstract only" | Hướng đoán không bị bác: ANGLE-PRIOR đọc Methods của AQE và không thấy cổng theo kích thước pixel. Nhưng từ abstract thì không kết luận được "chỉ còn". AQE còn có loss theo aspect ratio | NGUỒN (qua audit) |
| E12 | Con số "khoảng 45 nguồn mới" tôi đưa ra | Không có bảng chọn nguồn để tái dựng. Manifest có 298 bản ghi và 174 ID arXiv duy nhất. Đó là kết quả trả về, không phải số bài đã đọc | NGUỒN |

### D. Suy nhân quả hoặc phép đo không hợp lệ

| # | Tôi đã viết | Sai vì | Nhãn |
|---|---|---|---|
| E8 | Đề xuất dùng độ lệch giữa HBB và envelope của OBB làm phép đo nhiễu nhãn, và dùng "histogram góc co về vài giá trị ở bin nhỏ" (DM:52) làm phép thử | OBB của AI-TOD-R được H2RBox-v2 sinh từ HBB rồi sửa tay, nên hai bộ nhãn không độc lập. Histogram góc co lại có thể do xe đỗ thẳng hàng, do quy ước w/h hoặc do prior của H2RBox. Cặp nhãn có ích, nhưng là để kiểm sự nhất quán, không phải để đo nhiễu | NGUỒN (qua audit) + SUY LUẬN |
| E10 | DM:69 "Nếu A8 đủ ứng viên mà recall vẫn thấp thì **nguyên nhân nằm ở đặc trưng**" | Còn nhiều khả năng khác: xung đột positive, trọng số, regression, nhãn, NMS/cap, evaluator. Một chỉ số không xác định được nguyên nhân | SUY LUẬN (logic) |
| E11 | DM:61 "'ngân sách lỗi' cho biết mỗi nguyên nhân chiếm bao nhiêu" | Các nguyên nhân chồng lên nhau. Khi có tương tác (I = Y11 − Y10 − Y01 + Y00 ≠ 0), không có cách chia phần trăm duy nhất | SUY LUẬN (logic) |

### E. Sai loại bài toán

| # | Tôi đã viết | Sai vì | Nhãn |
|---|---|---|---|
| E9 | DM:69 CSCWD "xử lý cùng triệu chứng 'vật dưới stride'". DM:84 "đối chứng mức đặc trưng cho hướng A, cùng họ YOLO11" | CSCWD phát hiện chính chiếc drone (Drone-vs-Bird, DUT-Anti-UAV), không phải vật trên mặt đất nhìn từ UAV. RESEARCH-PROMPT §1 của dự án đã cảnh báo đúng chỗ này | NGUỒN |

### F. Ghi sai nguồn gốc

| # | Tôi đã viết | Sai vì | Nhãn |
|---|---|---|---|
| E14 | Memory dự án ghi C-19 là "self-audit via 3 subagents" | Header của AUDIT.md ghi worker gpt-6.1-sol và gpt-6-astra. Transcript phiên này có 0 lần gọi Agent. **Đã sửa memory hôm nay** | ĐO |

**Thống kê** (phân loại của tôi, SUY LUẬN):

- Lỗi dữ kiện nguồn: 3 (E6, E9, E14).
- Lỗi khung hoặc tiền đề: 3 (E1, E2, E13).
- Toán ngoài phạm vi: 3 (E3, E4, E5).
- Độ sâu đọc so với mức chắc: 2 (E7, E12).
- Nhân quả hoặc phép đo: 3 (E8, E10, E11).

`hallucination-guard` đã chạy 3 lần trên đúng ba note này và **không bắt được lỗi nào trong 14 lỗi**. Số chỗ nó bắt sửa là 5 ở VA (ĐO, transcript 14/10 14:33), 3 ở QP và 6 ở DM (QUAN SÁT, lấy từ bản tóm tắt phiên trước khi nén ngữ cảnh). Các chỗ sửa thuộc ba loại:

- chi tiết nguồn: số epoch của MCSA, số mức của OSCAR, số lần thử JEIT, số đếm;
- nhãn độ sâu đọc: "chỉ xem tiêu đề", giới hạn của lần quét arXiv;
- gắn nhãn [suy luận] cho câu chưa có nhãn: mật độ SIRST, GauCho.

Có đúng một lần guard sửa lĩnh vực của nguồn (HODet). CSCWD sai loại bài toán thì vẫn lọt. Không chỗ nào kiểm xem suy luận đúng hay sai.

Sau các lần scan, tôi báo người dùng: "Mỗi file phân tích đều đã qua kiểm bịa … Lỗi phát hiện đã sửa và kiểm lại, **không còn lỗi**" (chat 14/10 17:43). Câu này **nói quá phạm vi của guard**. Guard chỉ kiểm việc claim có nguồn và có nhãn. Người đọc thì hiểu thành nội dung đã đúng.

---

## 3. Nguyên nhân gốc

### RC1 — Rule venue toàn cục lấn quyết định của dự án · NGUỒN + ĐO

`~/.claude/rules/research-proposal-integrity.md`:

- §1 có bảng tier → band ("T1 … Q4. **NEVER Q1 alone**"; "T2 … Q2–Q3").
- §2 bắt **mọi** đề xuất phải có Venue Claim Card với ô "Venue band", và ghi "A proposal note without this card is incomplete".

Hai skill ép thực hiện rule này:

- Bảng định tuyến của `research-admin` có dòng "Đề xuất hướng / novelty / venue → chấm tier trước, Venue Claim Card".
- `hallucination-guard` có mẫu lỗi "Venue overclaim … Grade per … §1" và coi tier kèm điều kiện là cách sửa.

Rule không có thứ tự ưu tiên giữa nó và quyết định cấp dự án. Trong khi đó, dự án đã ghi rõ "No venue band" ở C-13, C-14, C-15.

Kết quả: thẻ venue của tôi **qua được** guard chính vì nó có tier và điều kiện. Đo: bản rule đang cài giống hệt bản HEAD trong repo, nên **rule này vẫn đang có hiệu lực**.

### RC2 — Đọc lại ledger theo chuỗi claim, bỏ sót các dòng quy định phạm vi · ĐO

Mục "Nguồn nội bộ đã đọc lại" ở đầu mỗi note:

- VA:10 chỉ có C-10, C-11, C-12.
- QP:10 chỉ có C-11, C-12, C-16.

Không note nào đọc lại C-13–C-15, `RESEARCH-START-HERE.md` hay `RESEARCH-PROMPT.md`, dù tôi đã đọc toàn bộ repo ở lượt đầu tiên.

Đáng chú ý hơn: chính báo cáo lượt 1 của tôi ghi "Tìm ra 5 chỗ mâu thuẫn trong repo, trong đó có việc **hai hướng nghiên cứu đang chạy song song**" (QUAN SÁT, chat 14/10 17:43 nhắc lại). Như vậy tôi đã biết có xung đột, nhưng vẫn chọn một nhánh mà không hỏi (E13).

Rule §3 chỉ nói "re-read `notes/claims-ledger.md` + the proposal note". Tôi hiểu thành "đọc lại các dòng liên quan đến claim đang xét". Rule không bắt đọc tài liệu giao thức của dự án.

### RC3 — Đính chính kỹ thuật nằm rải rác, không có chỗ tra · ĐO

Phản ví dụ về cùng diện tích đã có trong:

- issue #21;
- digest §5.3;
- `t07-dl-from-slides-VI.md:682`.

Nhưng proposal v2 §6, nguồn tôi đọc, vẫn giữ "Hệ quả 2" ở dạng cũ. Ledger chỉ ghi claim về venue và novelty, không ghi claim toán hay kỹ thuật. Vì vậy tôi không có chỗ nào để tra xem claim này đã bị sửa chưa.

### RC4 — `hallucination-guard` kiểm nguồn, không kiểm suy luận · ĐO + NGUỒN

Bản đang chạy chỉ kiểm hai điều:

- "Every factual claim needs a source";
- "can it be verified from available context?".

Guard không có bước nào để:

- (a) so phạm vi của định lý với cách dùng nó (bảo đảm khác tối ưu; kỳ vọng khác phân phối; cận trên khác cận dưới);
- (b) chặn suy nhân quả từ một chỉ số;
- (c) thử tìm phản ví dụ cho claim [derived];
- (d) kiểm nguồn trích có cùng loại bài toán không;
- (e) kiểm độ sâu đọc có đủ cho mức chắc của claim không.

Bằng chứng ở §2: mọi chỗ guard bắt sửa đều về nguồn hoặc nhãn, không chỗ nào kiểm suy luận đúng hay sai. Báo cáo "không còn lỗi" sau scan còn biến một phép kiểm hẹp thành lời bảo đảm rộng.

### RC5 — Các skill worker không vừa với việc thực tế · ĐO + NGUỒN + SUY LUẬN

Transcript cho thấy 3 lần `research-admin`, 3 lần `hallucination-guard`, 0 lần `paper-method`, `paper-synthesize`, `ieee-q1-devil-advocate`, `self-evaluator`, và 0 lần Agent. Lý do, đọc từ chính các skill:

- **`research-admin`** có các mode scope, pipeline, triage, read, synthesize. **Không có mode "thẩm định một đề xuất hoặc hướng"**. Đây lại là việc dự án này làm nhiều nhất: 11/10, 14/10 hai lần, 15/10, và cả audit C-19.
- **`paper-method`** chỉ nhận đầu vào là id hoặc file trong `./papers/` (Phase 0 theo conventions §2). Bài tôi tải từ web nằm trong scratchpad, nên tôi đọc bằng grep. Nếu chạy `paper-method critique`, bước "Key equations — copied faithfully" nhiều khả năng đã bắt được Eq.1–2 của O2-DETR (SUY LUẬN).
- **`ieee-q1-devil-advocate`** chạy "áp chót" trong chuỗi viết bản thảo, nhận bản thảo làm đầu vào, và **ràng buộc vào chính rule §1** ("T1 mà target Q1 = FAIL thẳng"). Nó cũng ghi "Không nhận kiến thức từ LLM training; mọi claim phải đè vào nội dung văn bản đầu vào". Vì vậy dù có gọi, nó sẽ **củng cố** E1 và E2, và không thể mở nguồn gốc để bắt E6 (SUY LUẬN).

Đây là điểm tôi tự sửa so với nhận định trước: "không gọi devil-advocate" không phải nguyên nhân chính. Skill đó, nếu giữ nguyên, chung gốc lỗi với tôi.

### RC6 — Không có người phản biện độc lập · QUAN SÁT + SUY LUẬN

Cùng một model viết và tự kiểm, inline, không có subagent. Audit C-19 khác tôi ở năm điểm. Theo §2, chính các điểm này đã bắt lỗi:

1. Model khác, chạy trong ngữ cảnh khác.
2. Được dặn rõ "Mapping T1/T2/T3→quartile trong rubric không được dùng như bằng chứng editorial" (AUDIT.md:18).
3. Mở lại nguồn gốc ở mức method và bảng.
4. Tìm phản ví dụ cho từng claim toán.
5. Đối chiếu loại bài toán và tài liệu giao thức của dự án.

Có một hạn chế: audit được đọc kết quả của tôi trước khi phản biện. Nên đây **không phải** so sánh "có skill / không skill" công bằng.

Có thêm một xung đột cấu hình: harness dặn "Do not spawn agents unless the user asks", còn `admin` và `research-admin` mô tả fan-out sang subagent. Bản HEAD trong repo đã thêm "If subagents are unavailable, execute sequentially". Nhưng chưa nơi nào nói lệnh `/admin sâu` có tính là người dùng đã yêu cầu subagent hay không.

### RC7 — Phiên chạy bản skill cũ hơn repo · ĐO

- Transcript ghi "Base directory for this skill: …\.claude\skills\…" (thư mục người dùng, tức `~/.claude/skills`) cho `admin`, `research-admin` và `hallucination-guard`.
- Các file này có ngày sửa 08/09/2026. So nội dung với từng commit thì bản cài khớp commit `e51683d` (02/10/2026) ở 68/69 skill. Bản cài chỉ thiếu các thay đổi từ commit `0ef12b5` (04/10, evidence-first) trở đi; ngày sửa file không phản ánh phiên bản.
- So phần thân SKILL.md (bỏ frontmatter, bỏ CR) với repo HEAD `f5f653a`: **14/69 skill khác**. Trong đó có `admin` (114 dòng ở HEAD, 81 dòng bản cài), `research-admin` (233/197), `hallucination-guard` (126/106), `self-evaluator` (119/102).
- `evidence-first.md` **không có** trong `~/.claude/rules`.

Bản HEAD của `hallucination-guard` đã có những bước sau:

- "Split material factual claims and deductions";
- "check whether it entails the exact claim's … scope";
- "Counter-evidence — reopen … dependent deductions".

Bản HEAD của `research-admin` có câu "Unseen body/AI summaries are not support".

**SUY LUẬN:**

- Nếu được cài, các bước này có thể đã chặn E6, E7, E9, E12.
- Chúng **không** chặn E1–E5, E10, E11. Lý do: rule venue ở HEAD vẫn giữ bảng tier → band, và không có bước tìm phản ví dụ hay bước kiểm nhân quả.

### RC8 — Thói quen suy luận của chính tôi · QUAN SÁT

Không skill nào sửa hết được những lỗi này:

- **Trả lời trong khung câu hỏi** (Q4, Q3, Q2) thay vì hỏi xem khung đó có hợp lệ với dự án không.
- **Phóng đại độ chính xác:** "trần Q3", "định luật", "chỉ còn". Những từ này biến một lựa chọn thiết kế thành sự thật.
- **Ghi ba REVISION trong khoảng một ngày** (C-16 và C-17 ngày 14/10, C-18 ngày 15/10). Mỗi lần ghi trên bằng chứng suy luận hoặc chỉ đọc abstract, không có kết quả chạy. Ledger vì vậy thành nơi lưu những điều kiện tôi tự suy ra.
- **Dùng grep từ khóa thay cho đọc method,** rồi gắn nhãn "toàn văn".

---

## 4. Việc làm tốt, kèm bằng chứng

| Việc | Bằng chứng | Nhãn |
|---|---|---|
| Tìm ra OSCAR (TGRS 2023), nhờ đó claim "tăng sàn ứng viên là mới" không còn đứng được | Ledger C-16; REPORT §1 ghi đây là "việc đáng giữ" | NGUỒN |
| Đọc MCSA theo cơ chế, không chỉ theo tên | VA:36; REPORT §1 | NGUỒN |
| Tám giả thuyết cạnh tranh, không chọn sớm một head | DM §2; REPORT §1: "tốt hơn chọn ngay một head rồi tìm tài liệu ủng hộ". Lưu ý: việc này một phần là do người dùng yêu cầu "ko claim qua manh vao 1 gia thuyet" | NGUỒN |
| Nhận ra AI-TOD-v2/R dùng chung 28.036 ảnh | QP:26; REPORT §1 gọi đây là "tài sản đối chiếu". Chỉ sai ở cách dùng (E8) | NGUỒN |
| Định lý √2·s đúng, cận chặt tại hình vuông xoay 45° | §1.1 (ĐO); LOGIC-CRITIQUE §1 | ĐO |
| Kiểm đúng code OBB dùng ≥/≤ | LOGIC-CRITIQUE §2: "Không được sửa thành 'code OBB đang dùng strict'" | NGUỒN |
| Gắn nhãn phân biệt abstract và toàn văn ở phần lớn nguồn | REPORT §1 | NGUỒN |
| Ledger, REVISION và hộp đính chính giúp người ngoài truy từng lỗi về đúng dòng | LOGIC-CRITIQUE ghi vị trí theo §/C-xx của tôi | QUAN SÁT |
| Lưu cache scan, nên audit sao lưu và kiểm SHA256 được | VERIFICATION.json; CACHE-MANIFEST | NGUỒN |
| Ghi rõ CDCEDet không truy cập được, không đoán nội dung | VA:42 (7 lần thử, liệt kê từng lần), VA:47 | NGUỒN |

Proposition 1 (E[N] = (21/1024)·diện tích) và ước lượng P(rỗng) ≈ 0,671 cho hộp 4×4 dưới TAL **không bị audit bác**. Audit cũng không kiểm lại hai điều này, nên tôi giữ chúng ở mức "chưa bị bác", không phải "đã được xác nhận".

---

## 5. Phản biện lại audit C-19

1. **Không sửa gốc ở rule** (NGUỒN, AUDIT.md:18: "Chỉ ghi điều chỉnh trong dự án, không sửa skill/rule toàn cục"). Đúng phạm vi được giao. Nhưng RC1 vẫn còn: phiên sau gọi `/admin` sẽ nạp lại bảng tier → band và yêu cầu thẻ venue. Header ledger có ghi "C-19 supersedes the venue mapping", nhưng thông tin này chỉ có tác dụng nếu phiên sau đọc header. Vì vậy chỉ sửa ledger là chưa đủ.
2. **PASS chỉ là PASS về tính nhất quán.** REVIEW tự ghi giới hạn: chưa kiểm cache, metadata và paper. Cả ba worker đều là model. RESEARCH-PROMPT §8 của dự án nói "Không tự coi kết luận của ba agent là ba thí nghiệm độc lập". Phần tôi kiểm lại được (§1.1–1.2) đều khớp. Phần còn lại vẫn ở mức "model báo cáo".
3. **Câu hỏi venue bị gỡ nhưng chưa được thay.** Audit bỏ quy tắc sai nhưng chưa đưa ra tiêu chí tích cực nào để chọn venue cho đề tài này. §5 của REPORT là "cổng chất lượng do nhóm đề xuất". Đây là lựa chọn trung thực khi chưa có kết quả. Người dùng cần biết đây là trạng thái "chưa biết", không phải "đã có đường Q2".
4. **Xung đột tên "hướng A" mới được nêu, chưa được giải quyết.** REPORT §1 có nêu xung đột tên nhưng không hỏi lại người dùng. R1 (độ tin cậy góc) được ưu tiên điều tra. Trong khi đó, nếu "hướng A" mà người dùng hỏi là "Ưu tiên A" của `RESEARCH-START-HERE` (scale và cách học), thì R3 mới sát câu hỏi gốc. Audit có đặt cổng "task có cần OBB không" trước R1, nên rủi ro này đã giảm một phần (SUY LUẬN).
5. **Không phân tích quy trình.** Audit sửa nội dung, không hỏi vì sao bộ skill để lọt các lỗi này. File này bổ sung phần đó.

---

## 6. Bài học dùng ngay cho các phiên sau

1. Trước mọi câu trả lời về venue hoặc novelty, đọc **toàn bộ** header và các dòng active của ledger, cùng tài liệu điểm vào và giao thức của dự án (`RESEARCH-START-HERE`, `RESEARCH-PROMPT`, `AGENTS.md`), không chỉ chuỗi claim đang xét.
2. Nếu câu hỏi dùng một nhãn có thể hiểu hai nghĩa (như "hướng A"), hỏi lại một câu trước khi làm.
3. Mỗi claim [derived], ghi kèm một dòng "định lý này **không** nói gì", và thử một phản ví dụ nhỏ bằng số trước khi dùng nó làm điều kiện.
4. Không dùng một chỉ số để kết luận nguyên nhân. Câu "nếu X thì nguyên nhân là Y" phải kèm can thiệp có đối chứng.
5. Nhãn đọc chỉ dùng ba mức "abstract / grep từ khóa / đọc method + bảng". Claim dạng "không có", "chỉ còn" hay "không phụ thuộc" cần mức thứ ba.
6. Nguồn trích phải cùng loại bài toán. Kiểm bằng câu hỏi: đầu vào là gì, nhìn từ đâu, vật cần phát hiện là gì.
7. Chỉ ghi REVISION vào ledger khi có bằng chứng loại mới: kết quả chạy, đọc nguồn gốc, hoặc phản biện của người dùng. Nếu chỉ là suy luận thì ghi vào note như "đề xuất sửa".
8. Khi tóm tắt một báo cáo không do mình làm, chép đúng người hoặc model đã làm nó từ header của file.

---

## 7. Câu hỏi mở cho người dùng

1. Ngày 14/10, khi hỏi "hướng A đã đủ khả thi cho claim Q4 chưa", bạn muốn nói C-11 (STAL, A0/A1/A2/A8) hay "Ưu tiên A" trong `RESEARCH-START-HERE` (tách scale khỏi cách học)?
2. Bạn có muốn bỏ bảng tier → venue trong rule toàn cục không, hay chỉ thêm quy tắc "quyết định của dự án được ưu tiên hơn"? (Đây là đề xuất sửa bộ skill, nằm ở repo bộ skill.)

---

## Thuật ngữ (Glossary)

| English | Tiếng Việt | Giải thích ngắn |
|---|---|---|
| frame error / premise check | lỗi khung / kiểm tiền đề | Trả lời đúng câu hỏi nhưng câu hỏi dựa trên một tiền đề sai hoặc đã bị dự án bỏ |
| scope of a theorem | phạm vi định lý | Điều định lý thực sự bảo đảm, khác với điều người dùng định lý muốn suy ra |
| read depth | độ sâu đọc | abstract / grep từ khóa / method và bảng: mức đọc giới hạn mức chắc của claim |
| lineage-scoped re-read | đọc lại theo chuỗi claim | Chỉ đọc lại các dòng ledger cha-con của claim đang xét, bỏ sót các dòng quy định phạm vi |
| independent critic | người phản biện độc lập | Người hoặc model kiểm với tiền đề khác và ngữ cảnh khác người viết |
