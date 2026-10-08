# Đề tài #7 — Nghiên cứu sâu & đề xuất cụ thể

- **Đề tài gốc (sheet Tier 1 #7):** Phân vùng và Phát hiện Đa đối tượng Khẩu độ Nhỏ với ảnh trên không —
  *Multi-scale Aerial Object Detection and Segmentation* (DOTA-v2.0, Open Images)
- **Worker:** admin → research-admin (mode scope, nghiên cứu sâu 1 đề tài)
- **Ngày:** 2026-10-01
- **Ràng buộc từ user:** paper **Q3/Q4 chắc**, Q1 là mục tiêu kéo dài (stretch) · ngân sách Modal **≤ $100** ·
  chỉ nguồn học thuật · không bịa · có log
- **Log tra cứu đầy đủ:** `logs/research-log.md` (mục #1–#42). Mỗi con số trong file này ghi kèm `[log #n]`.

> Quy ước nhãn: `[log #n]` = có nguồn trong log · `[ước lượng]` = tự tính, có công thức ·
> `[suy luận]` = lập luận của tôi, chưa có nguồn trực tiếp · `[phải xác minh]` = chưa kiểm chứng được.

---

## 0. Tóm tắt 5 dòng

1. **Thu hẹp #7 thành:** *phát hiện vật thể tí hon có hướng xoay (oriented tiny object detection) bằng detector thời gian thực (YOLO-OBB)*.
   Bỏ phần segmentation: hướng SAM + hộp xoay đã có OBSeg và SOPSeg làm `[log #16, #17]`.
2. **Khoảng trống đã xác minh trên PDF gốc:**
   - Benchmark AI-TOD-R (27 phương pháp) **không có detector YOLO nào** `[log #18, #38]`.
   - Cơ chế gán nhãn cho vật thể nhỏ STAL của YOLO26 **chỉ được đánh giá trên COCO**, chưa thử trên dataset vật thể tí hon `[log #33, #38]`.
3. **Đóng góp dự kiến:**
   - (i) benchmark YOLOv8/11/26-OBB trên AI-TOD-R;
   - (ii) chẩn đoán vì sao vật thể tí hon có hướng bị bỏ rơi khi gán nhãn;
   - (iii) một sửa đổi nhỏ cho STAL (giữ tỉ lệ cạnh và góc xoay) cùng ablation.
4. **Chi phí:** một lần train YOLO26s-obb 100 epoch trên GPU L40S ước tính **$5–$17** `[ước lượng]`.
   Kế hoạch ~14 lần chạy vừa ≤ $100 cộng $30 credit free/tháng nếu throughput ở mức khá. **Phải đo bằng 1 lần chạy thử trước khi chốt.**
5. **Mức độ mới: T1.**
   - Q4 / hội nghị Scopus: khả thi cao, nếu có bảng benchmark sạch.
   - Q3: có điều kiện.
   - Q1: không bảo vệ được trong ngân sách này. Lộ trình lên cao hơn ở §8.

---

## 1. Vì sao không làm #7 nguyên văn như sheet

| Thành phần trong sheet | Vấn đề | Căn cứ |
|---|---|---|
| "Segmentation" | SAM + prompt hộp xoay cho viễn thám đã có: OBSeg (Machine Intelligence Research 2025); SOPSeg (2025) làm đúng vật thể nhỏ + dựng dataset instance seg từ SODA-A | `[log #16, #17]` |
| DOTA-v2.0 làm dataset chính | Lớn (11,268 ảnh, 1,793,658 instance `[log #2 — snippet, chưa đọc nguồn gốc]`); điểm test chính thức cần server đánh giá, trạng thái server chưa xác minh `[log #4]` → tốn tiền, khó so sánh | `[log #2, #4]` |
| Open Images | Ảnh thông thường, hộp ngang — không phải ảnh trên không có hướng xoay | `[suy luận]` |
| "ViT + FPN vượt họ YOLO" | Mục tiêu mơ hồ, không có baseline số cụ thể; mảng "sửa YOLO cho UAV" (hộp ngang, VisDrone) rất đông | `[log #41]` |

**Giữ lại tinh thần #7** (ảnh trên không, vật thể nhỏ, đa tỉ lệ, hộp có hướng), nhưng chọn một ngách hẹp, đo được, rẻ.

---

## 2. Đề tài đề xuất

**Tên làm việc (EN):** *Do Real-Time Detectors Leave Oriented Tiny Objects Behind? Benchmarking and Improving
Small-Target-Aware Assignment for YOLO-OBB in Aerial Imagery*

**Tên tiếng Việt:** *Phát hiện vật thể tí hon có hướng xoay trong ảnh trên không bằng detector thời gian thực:
đánh giá và cải tiến cơ chế gán nhãn hướng vật thể nhỏ cho YOLO-OBB*

### 2.1 Bối cảnh (đã kiểm chứng)
- **AI-TOD-R** là dataset hộp xoay có vật thể nhỏ nhất hiện nay `[log #6, #38]`:
  - 28,036 ảnh 800×800; 752,460 object; 8 lớp; kích thước trung bình 10.6±4.9 px.
  - Đánh giá theo bin: very tiny [2,8], tiny [8,16], small [16,32], medium [32,64] `[log #37]`.
- **Benchmark gốc chủ yếu là detector chậm (MMRotate):**
  - Tốt nhất là DCFL (S²A-Net, 40 epoch) AP 17.5; Oriented R-CNN R50 chỉ AP 11.2 `[log #18]`.
  - **Không có YOLO, RTMDet-R hay detector thời gian thực nào** (PDF chứa 0 lần chữ "YOLO") `[log #38]`.
- **YOLO26 (Ultralytics, 2026) đưa vào STAL** `[log #33, #38]`:
  - Cạnh hộp nhãn nhỏ hơn ngưỡng thì được phóng lên kích thước tham chiếu `s_ref` (mặc định 16), chỉ trong khâu chọn ứng viên.
  - Trên COCO với YOLO11s, AP vật thể nhỏ tăng từ 29.0 lên 29.6. `s_ref = 8` làm giảm còn 27.7, `s_ref = 32` giảm còn 28.3 → **rất nhạy với tham số**.
  - Paper **không thử STAL trên dataset vật thể tí hon nào** và không mô tả cách STAL xử lý hộp xoay.
- **Mã nguồn hiện tại khác paper:** mã nhánh main phóng mọi cạnh < 16 px lên 16 px, còn paper chỉ phóng cạnh < 8 px `[log #26, #39]`.
  Trên AI-TOD-R, nơi đa số vật thể < 16×16 px `[log #42]`, hai phiên bản này cho hành vi khác hẳn nhau `[suy luận]`.
- **STAL phóng từng cạnh độc lập** `[log #38]`. Một hộp xoay tí hon, ví dụ tàu 4×12 px, sẽ thành vùng chọn ứng viên 16×16:
  mất cả tỉ lệ cạnh lẫn ý nghĩa của góc xoay `[suy luận từ Eq.(5)]`.

### 2.2 Câu hỏi nghiên cứu
- **RQ1 (benchmark):** Detector thời gian thực YOLOv8/11/26-OBB đứng ở đâu so với 27 phương pháp trên AI-TOD-R,
  cả về độ chính xác (AP, APvt, APt) lẫn tốc độ?
- **RQ2 (chẩn đoán):** Với vật thể tí hon có hướng xoay, mỗi vật thể nhận được bao nhiêu mẫu dương (positive), chia theo bin kích thước?
  So sánh 3 cách: gán nhãn task-aligned gốc (TAL), STAL theo paper (ngưỡng 8), STAL theo mã nguồn (ngưỡng 16).
  Vật thể dài và mảnh (tàu, cầu) có bị thiệt không?
- **RQ3 (cải tiến):** Một vùng chọn ứng viên **giữ tỉ lệ cạnh và góc xoay** có cải thiện APvt/APt so với STAL không,
  khi tốc độ suy luận giữ nguyên (sửa đổi chỉ tác động lúc train)?
- **RQ4 (tổng quát hóa):** Kết quả có lặp lại trên SODA-A không (2,513 ảnh lớn, 872,069 instance, 9 lớp) `[log #11, #37]`?

### 2.3 Phương pháp đề xuất — OA-STAL (Orientation-Aware STAL)
**Ý tưởng** `[design]` `[cần thực nghiệm]`: thay vì phóng từng cạnh lên `s_ref`, phóng **đồng dạng** hộp xoay
(giữ tâm, góc và tỉ lệ cạnh) tới khi đạt diện tích tối thiểu `s_ref²`. Chỉ áp dụng trong khâu chọn ứng viên, đúng như STAL.

```
k        = max(1, s_ref / sqrt(w * h))       # hệ số phóng đồng dạng
(w~, h~) = (k * w, k * h)                    # giữ tỉ lệ w/h và góc theta
long-side cap: max(w~, h~) <= c * s_ref      # chặn hộp quá dài lấn sang vật thể bên cạnh (c là siêu tham số ablation)
```

**Kiểm tra hợp lý (sanity check — điều kiện bắt buộc với công thức [design]):**
- Vật thể vuông (w = h = d < s_ref) → thành s_ref × s_ref, **trùng đúng STAL**. Đây là trường hợp suy biến, nên OA-STAL tổng quát hóa STAL.
- Vật thể lớn (sqrt(w·h) ≥ s_ref) → k = 1, không đổi, **trùng TAL gốc**.
- Không ảnh hưởng lúc suy luận → tốc độ (FPS) giữ nguyên.

**Biến thể cho ablation:**
- (a) Vùng mềm dạng Gaussian/elip theo hình học hộp xoay — cơ chế tương tự EARL `[log #40]`.
- (b) Thêm đầu dự đoán P2 (stride 4) — mẹo phổ biến cho vật thể nhỏ, dùng làm đối chứng.

**Mức độ mới (nói thẳng):** cùng lớp cơ chế với gán nhãn theo tỉ lệ cạnh / hình elip đã có (EARL 2023,
một số paper về tàu thuyền 2024–2026 `[log #40]`). Điểm mới chỉ ở chỗ **đưa cơ chế này vào STAL của YOLO cho vật thể tí hon có hướng**,
kèm phân tích chẩn đoán → **T1**.

---

## 3. Dữ liệu

| Dataset | Vai trò | Quy mô | License | Trạng thái |
|---|---|---|---|---|
| **AI-TOD-R** | Chính | 28,036 ảnh 800×800; 752,460 OBB; 8 lớp; 10.6±4.9 px `[log #6, #38]` | Dựng từ AI-TOD (CC BY-NC-SA 4.0 `[log #37]`); trang dự án CC BY-SA cho web `[log #8]` | Link Google Drive trên trang dự án `[log #8]`. **[phải xác minh]** có cần tải xView riêng như AI-TOD gốc không `[log #37]` |
| **SODA-A** | Tổng quát hóa | 2,513 ảnh (TB 4761×2777); 872,069 OBB; 9 lớp; 15.6±7.6 px; split 40/25/35% `[log #11, #37, #38]` | CC BY-NC 4.0 `[log #37]` | OneDrive / BaiduNetDisk `[log #37]` |
| DOTA-v2 (train → val) | Tùy chọn, nếu còn tiền | Theo giao thức ablation của DCFL: train trên tập train, đánh giá trên tập val — **không cần server test** `[log #38]` | Chỉ dùng học thuật `[log #4]` | Tùy chọn |

**Giao thức so sánh công bằng (quan trọng):** benchmark AI-TOD-R gốc dùng trainval → test, ảnh 800×800, batch 2,
**chỉ lật ngẫu nhiên (random flip)**, 12 epoch `[log #38]`. Công thức mặc định của YOLO dùng augmentation mạnh (mosaic) và train lâu hơn `[suy luận]`.
Vì vậy báo cáo **2 chế độ**:
- **(P1) "protocol-matched":** chỉ flip, lịch train ngắn — để đặt cạnh Bảng II.
- **(P2) "công thức gốc của YOLO":** để đo năng lực thực tế.

Không trộn số của hai chế độ trong cùng một so sánh.

**Bắt buộc:**
- Dùng công cụ đánh giá chính thức của AI-TOD-R (rotated AP theo bin vt/t/s/m).
- Ghim phiên bản `ultralytics`, vì định nghĩa STAL khác nhau giữa paper và mã nguồn `[log #39]`.

---

## 4. Thí nghiệm & ngân sách Modal

### 4.1 Giá Modal (trang chính thức, 2026-10-01) `[log #1, #35, #36]`
Giá theo giờ = giá theo giây × 3600 `[ước lượng — phép nhân]`. Chi phí phụ = 8 CPU + 32 GiB RAM ≈ $0.633/giờ.

| GPU | $/giờ (GPU) | $/giờ (kèm CPU+RAM) | Số giờ với $100 |
|---|---|---|---|
| B300 (mạnh nhất) | 7.10 | 7.73 | 12.9 |
| H100 | 3.95 | 4.58 | 21.8 |
| A100-80GB | 2.50 | 3.13 | 31.9 |
| **L40S (48 GB) — khuyên dùng** | **1.95** | **2.58** | **38.7** |
| L4 | 0.80 | 1.43 | 69.8 |

- **Ràng buộc nền tảng:** tối đa 8 GPU/container; mỗi lần gọi hàm **tối đa 24 giờ** → phải lưu checkpoint và resume `[log #35, #36]`.
- **Credit:** gói Starter có **$30/tháng free**. Có **chương trình academics "up to $10k"** `[log #1]` → **nên nộp đơn ngay** (xem §8).
- **Vì sao không dùng "GPU tối đa" (B300):** model YOLO-s nhỏ (9.8M tham số `[log #25]`), nên dễ nghẽn ở khâu nạp dữ liệu (CPU) hơn là ở GPU `[suy luận]`.
  GPU đắt chủ yếu làm đốt tiền nhanh hơn → L40S là điểm cân bằng tốt. Kết luận này sẽ được kiểm lại bằng lần chạy thử.

### 4.2 Ước lượng chi phí 1 lần train `[ước lượng]`
- Số ảnh trainval ≈ 14,000 `[suy luận]`: số instance trainval/test của AI-TOD-v2 gần 50/50 (376,625 so với 376,129 `[log #37]`).
  Số ảnh thật lấy khi tải dataset.
- 100 epoch × 14,000 ảnh = 1.4 triệu lượt ảnh.

| Throughput giả định (L40S) | Thời gian | Chi phí |
|---|---|---|
| 200 ảnh/s | 1.9 giờ | ~$5.0 |
| 100 ảnh/s | 3.9 giờ | ~$10.1 |
| 60 ảnh/s | 6.5 giờ | ~$16.8 |

→ **Throughput chưa có nguồn nào công bố.** Bước 0 bắt buộc: chạy thử 1 epoch cho YOLO11s-obb và YOLO26s-obb (~$1–2) để đo, rồi mới chốt kế hoạch.

### 4.3 Kế hoạch chạy (~14 lần)

| Pha | Nội dung | Số lần chạy | Ghi chú |
|---|---|---|---|
| 0 | Chạy thử 1 epoch, đo ảnh/s và VRAM | 2 (ngắn) | Chốt ngân sách |
| 1 | Benchmark P2: YOLOv8s / YOLO11s / YOLO26s / YOLO26n -obb | 4 | Trả lời RQ1 |
| 1b | Benchmark P1 (protocol-matched): YOLO26s | 1 | So sánh với Bảng II |
| 2 | Chẩn đoán số mẫu dương: TAL / STAL ngưỡng 8 / STAL ngưỡng 16 / OA-STAL | 0 (chỉ chạy assigner, rẻ) | Trả lời RQ2 |
| 3 | Ablation YOLO26s: STAL tắt · s_ref 16 · s_ref 24 · OA-STAL · OA-STAL + P2 | 5 | Trả lời RQ3 (ablation có thể giảm còn 50 epoch) |
| 4 | SODA-A: YOLO26s mặc định so với + OA-STAL | 2 | Trả lời RQ4 (~40k patch 1200² → đắt hơn ~2–5 lần, giảm epoch) `[ước lượng]` |
| 5 | Seed thứ 2 cho cặp so sánh chính | 2 | Độ tin cậy |

**Kịch bản tiền:**
- **Lạc quan** (≥150 ảnh/s): ~$60–80 → vừa $100.
- **Bi quan** (60 ảnh/s): ~$150–200 → phải dùng thêm credit free, giảm epoch ablation, hoặc có academic credits.

---

## 5. Kế hoạch 14 tuần

| Tuần | Việc | Sản phẩm |
|---|---|---|
| 1 | Tải AI-TOD-R + SODA-A; dựng `experiments/` + `modal_app.py`; ghim phiên bản | Dữ liệu sẵn sàng |
| 2 | Pha 0 chạy thử + chuyển dự đoán YOLO sang định dạng đánh giá chính thức | Ngân sách chốt |
| 3–4 | Pha 1, 1b | Bảng benchmark |
| 5 | Pha 2 (chẩn đoán) | Biểu đồ số mẫu dương theo bin |
| 6–8 | Cài OA-STAL + Pha 3 | Bảng ablation |
| 9–10 | Pha 4–5 | Bảng tổng quát hóa |
| 11–14 | Viết bài → kiểm tra trích dẫn → phản biện nội bộ → nộp | Bản thảo |

---

## 6. Rủi ro & cách xử lý

| Rủi ro | Xử lý |
|---|---|
| OA-STAL không hơn STAL | Đổi thành paper benchmark + phân tích. Vẫn có thể nộp Q4/hội nghị nếu RQ1–RQ2 có phát hiện rõ (xem Downgrade triggers) |
| Đã có người benchmark YOLO-OBB trên AI-TOD-R sau 2026-10-01 | Cảnh báo: mới search tới ngày này `[log #19, #40]`. Tìm lại ngay trước khi viết |
| Tải AI-TOD-R cần xView | Đăng ký xView (CC BY-NC-SA) — chỉ mất thời gian |
| Lệch phiên bản Ultralytics | Ghim phiên bản; ghi commit hash vào `experiments/` |
| Vượt ngân sách | Giảm epoch ablation; dùng YOLO26n để sàng lọc; credit free; nộp đơn academic |
| Tốn công chuyển định dạng đánh giá | Ưu tiên ở tuần 2 trước mọi thí nghiệm lớn |

---

## 7. Venue mục tiêu (Q3/Q4)

| Venue | Hạng | Trạng thái xác minh |
|---|---|---|
| Remote Sensing Letters (Taylor & Francis) | Q3 (SJR 2024) | Snippet trang SJR `[log #29]` — **tự mở SJR kiểm lại** |
| Journal of Applied Remote Sensing (SPIE) | SJR 2024 = 0.386, hạng chưa rõ | `[log #29]` |
| Pattern Recognition and Image Analysis | Q3 (theo sheet giảng viên) | Chưa xác minh trên SJR (Cloudflare chặn `[log #28]`) |
| Neural Processing Letters | Q3 (theo sheet) | Chưa xác minh |
| Electronic Letters on Computer Vision and Image Analysis | Q4 (theo sheet) | Chưa xác minh |
| Signal, Image and Video Processing | Sheet ghi **Q1**, nhưng snippet SJR 2024 ghi **Q2** | **Lệch nhau** `[log #27]` → kiểm lại trước khi coi là mục tiêu |

### Venue Claim Card
- **Proposal:** Benchmark YOLOv8/11/26-OBB trên AI-TOD-R + chẩn đoán gán nhãn cho vật thể tí hon có hướng + OA-STAL (STAL giữ tỉ lệ cạnh và góc), kiểm tra lại trên SODA-A.
- **Novelty tier:** **T1** — sửa đổi khâu gán nhãn (mẹo huấn luyện), cùng lớp cơ chế với EARL / gán nhãn theo tỉ lệ cạnh đã có.
  Phần benchmark + chẩn đoán là đóng góp thực nghiệm, không nâng tier.
- **Venue band:** Q4 / hội nghị Scopus — **khả thi cao**, với điều kiện có bảng benchmark RQ1 sạch và chẩn đoán RQ2 rõ.
  Q3 — **có điều kiện:** (1) OA-STAL cải thiện APvt/APt nhất quán trên **cả 2 dataset**, có 2 seed;
  (2) chẩn đoán RQ2 cho thấy cơ chế rõ ràng; (3) khảo sát lại xác nhận chưa ai benchmark YOLO-OBB trên AI-TOD-R.
  **Q1: không bảo vệ được** với đề xuất này (T1 không bao giờ đủ Q1 theo rubric).
- **Downgrade triggers:**
  - OA-STAL ≤ STAL → chỉ còn benchmark/phân tích (Q4/hội nghị).
  - Phát hiện công trình đã benchmark YOLO-OBB trên AI-TOD-R → mất đóng góp (i).
  - Không chạy được SODA-A → chỉ 1 dataset → Q4.
- **Confidence:** medium — khoảng trống đã đối chiếu trên PDF; độ hiệu quả của OA-STAL hoàn toàn chưa biết; chi phí chưa đo.
- **Ledger:** C-3

---

## 8. Lộ trình nếu muốn với tới Q1 (stretch — nói thẳng)

Theo rubric, Q1 cần **T2/T3 + độ rộng (≥2 dataset, ablation đầy đủ, baseline mạnh) + khảo sát mới đã làm**. Đề xuất ở §2 không đạt.
Muốn kéo lên phải có **cả 3** điều sau:
1. **Lên T2:** thiết kế lại hẳn khâu gán nhãn hoặc biểu diễn cho vật thể tí hon có hướng — không chỉ đổi vùng ứng viên.
   Ví dụ (`[design]`, chưa kiểm chứng): một cơ chế gán nhãn xác suất dựa trên trường tiếp nhận Gaussian của chính detector thời gian thực,
   có lập luận vì sao nó bảo đảm đủ mẫu dương cho vật thể có hướng.
2. **Độ rộng:** AI-TOD-R + SODA-A + DOTA-v2 + DIOR-R. Vượt DCFL trên AI-TOD-R (AP 17.5 `[log #18]`) ở tốc độ thời gian thực.
3. **Tài nguyên:** vượt xa $100 → **chương trình academics của Modal (tới $10k `[log #1]`)** là điều kiện tiên quyết thực tế.

→ **Khuyến nghị:** làm bản T1 (Q3/Q4) trước, nộp đơn academic credits song song. Nếu có credit và OA-STAL cho tín hiệu tốt,
mở rộng thành bản T2 làm bài thứ hai.

---

## 9. Bước tiếp theo
1. Bạn chốt đề tài (hoặc nêu điểm muốn đổi).
2. Tôi dựng `experiments/` + `modal_app.py` (skill `run-on-modal`) và chạy Pha 0 để đo chi phí thật.
3. Sau Pha 0 cập nhật lại §4 bằng số đo thật, thay cho ước lượng.

## Thuật ngữ (Glossary)

| English | Tiếng Việt | Giải thích ngắn |
|---|---|---|
| oriented bounding box (OBB) | hộp bao có hướng xoay | Hộp chữ nhật xoay theo góc của vật thể |
| tiny object | vật thể tí hon | Theo AI-TOD: cạnh hiệu dụng < 16 px (very tiny < 8 px) |
| label assignment | gán nhãn mẫu | Quyết định điểm anchor nào là mẫu dương cho vật thể nào khi train |
| TAL (Task-Aligned Assigner) | gán nhãn căn chỉnh tác vụ | Assigner của YOLOv8/11, xếp hạng ứng viên theo điểm phân loại × IoU |
| STAL | gán nhãn hướng vật thể nhỏ | Của YOLO26: phóng hộp nhãn nhỏ lên `s_ref` chỉ khi chọn ứng viên |
| protocol-matched | cùng giao thức | Train/đánh giá đúng cài đặt của benchmark gốc để so sánh công bằng |
| pilot run | chạy thử | 1 epoch để đo tốc độ và chi phí thật |
| ablation | thí nghiệm loại bỏ | Bật/tắt từng thành phần để xem thành phần nào gánh kết quả |
