# Rà soát sổ tay nền `t07-foundation-G7-VI.pdf` (68 trang)

- **Ngày:** 2026-10-09 · **Worker:** admin
- **File được rà:** `notes/t07-foundation-G7-VI.pdf` (giữ nguyên). Bản sửa: `notes/t07-foundation-G7-VI-v2.pdf` (73 trang).
- **Cách rà:**
  - đọc hết 68 trang;
  - đối chiếu các khẳng định then chốt với file nguồn gốc (không dựa vào trí nhớ);
  - chạy lại bằng script mọi phép tính và phản ví dụ hình học.
- **Phạm vi chưa làm:** chưa đọc lại toàn văn NWD/RFLA (R2318, R2391) và các bài EARL/SARFA-Net/RDCNet. Các mục A5 (Hình 2(d)), C2 và mô tả prior trong C3 được giữ theo ghi chú của handbook, **chưa kiểm độc lập**.

## 1. Kết luận

**Về kiến thức:** handbook **chuẩn**. Không phát hiện số liệu hay công thức nào sai so với nguồn. Handbook còn chỉ ra đúng một số chỗ proposal viết quá tay (mục 4).

**Về trình bày và cấu trúc:** có lỗi chính tả hệ thống. Bố cục thì vừa thừa (trang trống, lặp ý, phần giải thích deck 20 slide cũ) vừa thiếu (hướng dẫn thực hành Phase 0, khớp với deck 18 slide và bản `Group7.pdf`).

## 2. Đã kiểm và khớp nguồn

| Khẳng định trong handbook | Nguồn đối chiếu | Kết quả |
|---|---|---|
| Bảng II: RetinaNet-O 7.3/23.9/2.2/5.9; Oriented R-CNN 11.2/33.2/0.6/9.1; ARS-DETR 14.3; SASM 11.4; CFA 12.4; DCFL #22 12.3, #23 15.2, #27 17.5/49.6/6.5/15.7; APt cao nhất 16.0 (#25); S2A-Net AP50 33.4 (+16.2) | `papers/_text/Xu2024-AI-TOD-R.txt`, Bảng II | khớp |
| §IV-A batch 2, LR 0.0025; §VI-A batch 4, LR 0.005, momentum 0.9, wd 0.0001 | như trên, dòng 443–444, 1037–1042 | khớp |
| Văn xuôi gọi "Table XII" nhưng bảng in là "TABLE XI" | như trên, dòng 1161–1280 và 1236 | khớp |
| K = 16, Q = 12, g = 0.8, trọng số 0.7, 59.15 mAP (DOTA-v2) | như trên, dòng 1210–1282 | khớp |
| H2RBox-v2 sinh nhãn OBB ban đầu | như trên, dòng 332, 364 | khớp |
| Paper viết "most images featuring over 100 objects" | như trên, dòng 396–401 | khớp; handbook đúng khi chỉ ra câu này mâu thuẫn với tổng (xem mục 4) |
| YOLO26: topk 10; topk 7, topk2 1; đầu ra (N,300,6); góc [−45°,135°); s_ref = 16; STAL trên COCO 46.6 → 46.8, APS 29.0 → 29.6 (Bảng 6); Progressive Loss (0.8,0.2) → (0.1,0.9) (Bảng 5) | `papers/_text/Jocher2026-YOLO26.txt` | khớp |
| Constructor mặc định topk 13, α 1, β 6; `stride_val = stride[1]`; OBB kiểm điểm bằng ≥/≤; HBB dùng CIoU `clamp_(0)`; STAL làm trên clone | `papers/_text/ultralytics_tal_main_2026-10-01.py` dòng 31–60, 59, 246, 404–425 | khớp |
| Caller OBB: α = 0.5; lọc GT cạnh < 2 px; λ = 3 | `scripts/t07-slr/data/_tmp_scanB/raw/loss_main_2026-10-08.py` dòng 1047, 1093, 1176 | khớp |
| Head detach nhánh one-to-one khi training | `.../raw/ul_head.py` dòng 196 | khớp |
| Evaluator: maxDets = [1500]; cắt theo ảnh-lớp; diện tích int(w·h) | `outputs/.../official_aitodr_eval.py.txt` dòng 110, 130, 356–382, 741 | khớp |
| Rule STAL đổi ngày 24/08/2026 (PR #25912) | `notes/t07-c3-novelty-rescan.md` dòng 193 | khớp |
| Proposal: 3 seed cho YOLO26n, 1 seed cho model lớn | `notes/t07-c3-proposal-v2-EN.md` dòng 316 | khớp |
| Phép tính: đỉnh OBB (14,821; 14,330); HBB 1.136,12 px²; IoU 0,6 và 0,9512; AP_101 = 76/101; E[N] 0,328 / 2,051 / 5,25; cận rỗng 0,671875; 26,84 vật thể/ảnh; 7.450 ảnh ≈ 26,57%; vehicle 88,1%; SD(Δ) = 0,1; ví dụ B4 (2,828; 7,071); OA-STAL 25×4 → 32×8 | tính lại bằng `scratchpad/hb_math.py` | khớp |
| Mô phỏng hình học: 64×4 có P(rỗng) ≈ 0,127 (handbook ghi 0,1247); 16×16 có P(rỗng) = 0; 8×8 và 16×4 trên stride 8 cùng E[N] = 1 nhưng P(rỗng) là 0 và 0,50; STAL-16 luôn có ứng viên ở mọi góc | chạy lại Monte Carlo | khớp |

## 3. Lỗi trong handbook

| # | Mức | Lỗi | Ví dụ (trang) | Trạng thái v2 |
|---|---|---|---|---|
| 1 | Trung bình | 80 chỗ chữ dính vào số hoặc ký hiệu. Lỗi nằm ngay trong văn bản nguồn, bước `final_editorial.py` chỉ sửa được một phần | "lệch ngang1 px", "vuông40×40" (51); "cộng90°" (52); "chung32×32" (13); "Floor8 tác động60×5" (47); "giải thích20thuật ngữ", "trước/saufilter" (65); "Vì sao26,84" (64) | **Đã sửa.** Kiểm bằng diff: chỉ chèn dấu cách, cộng 3 chỗ sửa ký hiệu (Pzero → P(rỗng), sqrt300 → sqrt(300), Max_det → max_det) |
| 2 | Thấp | Dấu thập phân lẫn lộn: "0,6", "10,6" bên cạnh "7.3", "2.828", "k=1.6" | Bảng II (20), B4 (33), C5 (46) | Chưa sửa; cần quyết một quy ước |
| 3 | Trung bình | Khoảng 20 trang gần như trống, vì sau mỗi unit đều ngắt trang | 6, 8, 10, 14, 16, 19, 21, 24, 26, 28, 30, 32, 34, 36, 38, 41, 43, 45, 47, 49, 64, 66 | Chưa sửa (thay đổi bố cục) |
| 4 | Trung bình | Phần D1–D10 giải thích deck 20 slide giới thiệu (`t07-c3-introduction-EN.pptx`), không phải deck bảo vệ proposal 18 slide (`Group7-proposal-presentation.pptx`). Handbook cũng chưa nhắc tới bản nộp `Group7.pdf` và tên đề tài "...Training Signal?" | 50–59 | Chưa sửa |
| 5 | Thấp | Bảng nguồn E4 trỏ tới file không có trên GitHub: `scripts/t07-slr/data/...` và `outputs/...`. Thành viên clone repo sẽ không mở được [S7], [S8], [S11]–[S14] | 67–68 | Chưa sửa |
| 6 | Thấp | Thứ tự: phần tự kiểm tra của F1 dùng số 13.125, nhưng số này đến F3 mới giải thích. A1 nhắc "Hình 4" của paper nhưng không in hình | 6, 17 | Chưa sửa |
| 7 | Thấp | Bìa không ghi mentor | 1 | Chưa sửa |

## 4. Những chỗ handbook đúng và proposal hoặc slide cần sửa theo

1. **">100 vật thể/ảnh".** Paper viết "most images featuring over 100 objects". Nhưng 752.460 / 28.036 ≈ 26,8 vật thể/ảnh, nên nhiều nhất 26,6% số ảnh có từ 101 vật thể; câu "most" của paper không thể đúng.
   - `Group7.pdf` §1.1 và §1.2 mục 5 viết "often more than 100 objects per image".
   - Slide 2 và slide 6 (bản 08/10) cũng dùng ý này.
   - → **Đã sửa slide:** "mean ≈ 27 objects per image, some images over 2,000". `Group7.pdf` vẫn cần sửa.
2. **maxDets.** AITODReval giữ tối đa 1.500 dự đoán **cho mỗi cặp ảnh-lớp**, không phải mỗi ảnh (code dòng 356–382).
   - `Group7.pdf` §1.2 mục 6 và §5.5 viết "1,500 detections per image".
   - Slide 6 và slide 12 cũng viết như vậy.
   - → **Đã sửa slide.** `Group7.pdf` vẫn cần sửa.
3. **"Cùng diện tích thì không thể đến từ coverage".** Câu này trong proposal chỉ đúng cho **số kỳ vọng**; xác suất rỗng vẫn khác nhau (C3). Mục này đã có trong issue #21.
4. **H1 "ranking ổn định qua 3 seed"** chưa kiểm được, vì các model lớn chỉ chạy 1 seed (proposal dòng 316). Phải thêm seed cho các model được xếp hạng, hoặc ghi ranking là thăm dò (C6).
5. **73,4%** là số của AI-TOD-v2, chưa đo trên AI-TOD-R. Bin tính theo √(w·h), trong khi STAL kích hoạt theo từng cạnh, nên từ con số này không suy ngay ra tầm quan trọng của ngưỡng 8 hay 16 (A2, C3).

## 5. Về nhận xét "chưa đủ và có dư"

**Đồng ý một phần.** Kiến thức thì đúng. Cảm giác vừa thừa vừa thiếu đến từ cấu trúc:

**Thừa:**
- Khoảng 20 trang trống.
- 10 trang D1–D10 nói lại F, A, B, C cho một deck không còn là deck thuyết trình chính.
- Cùng một ví dụ lặp nhiều lần: 25×4, 60×5, candidate ≠ positive, E[N] ≠ P(rỗng), max_det ≠ maxDets xuất hiện ở F5, A6, C3, C4, C5, D5–D7 và E2.
- Chi tiết nội bộ DCFL (A5: PCB, GJSD, DGMM, K/Q/g), dù DCFL chỉ là baseline được trích, nhóm không cài lại.
- Chi tiết DFL, ProbIoU và angle loss (B5), detach và Progressive Loss (B6) chỉ cần cho người sửa assigner.
- Dòng nguồn ghi số dòng code ở cuối mọi unit.

**Thiếu, để "bắt đầu nghiên cứu" được:**
- Hướng dẫn thực hành Phase 0:
  - lấy ảnh AI-TOD-R (đăng ký xView rồi chạy script AI-TOD);
  - định dạng nhãn và cách chuyển sang định dạng OBB của Ultralytics;
  - quy trình chạy trên Kaggle (resume qua các phiên 12 giờ);
  - script thống kê nhãn cho RQ2.
- Dataset thứ hai (SODA-A, hoặc DOTA-v2.0 dự phòng): đặc điểm của dataset, và lưu ý resize 800 → 1200 làm thay đổi tỉ lệ GT bị kích hoạt ngưỡng.
- Cách đo tốc độ và latency cho RQ1.
- Hai quy tắc xung đột (inside-box, smaller-GT) và nhánh A3 (fallback điểm neo gần nhất) mới chỉ được nhắc qua.
- Liên kết với deck 18 slide và với `Group7.pdf`.

## 6. Phụ lục tra nhanh

**Bản gốc chưa có phụ lục tra nhanh.** Bản gốc có E1 (thuật ngữ), E2 (20 câu hỏi), E3 (lộ trình) và E4 (nguồn), nhưng không có trang nào gom số liệu và công thức để tra nhanh.

**v2 đã thêm E5 (trang 69–73),** gồm:
1. số liệu then chốt kèm nguồn;
2. công thức một dòng có nhãn [nguồn], [suy ra] hoặc [thiết kế];
3. bảng tính sẵn 4 quy tắc trên 5 hộp mẫu, do script tính;
4. tám nhánh A0–A7;
5. 11 cặp khái niệm dễ nhầm;
6. checklist Phase 0;
7. bảng "hỏi gì thì mở mục nào".

Mọi số trong E5 đã đối chiếu nguồn ngày 09/10/2026.

## Thuật ngữ (Glossary)

| English | Tiếng Việt | Giải thích ngắn |
|---|---|---|
| quick reference | phụ lục tra nhanh | Trang gom số liệu, công thức để tra, không thay phần giải thích |
| maxDets (per image-category) | giới hạn dự đoán theo ảnh-lớp | AITODReval cắt từng cặp (ảnh, lớp), khác max_det toàn ảnh của YOLO |
| zero-candidate probability | xác suất không có ứng viên | Có thể khác nhau dù số ứng viên kỳ vọng bằng nhau |
