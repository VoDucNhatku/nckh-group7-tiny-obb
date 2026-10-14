# Vòng 3 — So sánh cuối 4 đề tài & khuyến nghị chốt

- **Ngày:** 2026-10-02 · **Người tổng hợp:** admin (research-admin)
- **Đầu vào:**
  - `notes/01-topic-selection/_local/r3-ranking.md` — sàng lọc 32 đề tài, 309 dòng log.
  - 3 đề xuất nghiên cứu sâu: `notes/01-topic-selection/_local/r3-deep-T2-6.md`, `r3-deep-T1-3.md`, `r3-deep-T1-16.md` — log riêng 35 + 50 + 52 dòng.
  - `notes/99-archive/t07-proposal.md` — vòng 2, 42 dòng log.
- **Ràng buộc user:** Q3/Q4 chắc, Q1 là stretch · Modal ≤ $100 · nguồn học thuật · không bịa.

## 1. Kiểm tra chéo của admin trên 3 đề xuất nghiên cứu sâu
Admin tự tìm lại trong text PDF đã trích (`papers/_text/`) hoặc API chính thức:

| Khẳng định | Đề xuất | Kết quả | Nguồn kiểm |
|---|---|---|---|
| Cột `attribution` "synonymous with the medical center" | T2-6 | ✅ | `Kurtansky2024-SLICE-3D-dataset.txt` (Sci Data 2024, bảng từ điển trường) |
| Ablation người thắng: ngữ cảnh bệnh nhân pAUC 0.165 → 0.173 | T2-6 | ✅ | `Kurtansky2025-ISIC2024-triage-3DTBP.txt` |
| MatchGen trên RESC: AnoDDPM Dice 25.01 | T1-3 | ✅ | `Ma2025-MatchGen.txt` |
| OCT2017 "nearly saturated" (MTL-MAD) | T1-3 | ✅ | `Bercean2026-MTL-MAD.txt` |
| BenchReAD: "no longer adequate as a standalone benchmark" | T1-3 | ✅ nguyên văn (lần tìm đầu báo động giả do admin chỉ in 2 kết quả đầu) | `Lian2025-BenchReAD.txt` |
| Dataset ViMD trên HF: CC BY-NC-ND 4.0, không gated | T1-16 | ✅ | API `huggingface.co/api/datasets/nguyendv02/ViMD_Dataset` |

→ **7/7 khẳng định then chốt khớp nguồn.** Không phát hiện số bịa.

## 2. Bảng so sánh

| Tiêu chí | **T2-6** Melanoma SLICE-3D | **T1-7** Vật thể tí hon YOLO-OBB | **T1-16** ViMD đa phương ngữ | **T1-3** OCT bất thường |
|---|---|---|---|---|
| Điểm D/B/N/C (sau nghiên cứu sâu) | 3/3/2/3 = **11** | 2/3/2/2 = **9** | 3/3/2*/2 = **10** (*N sát 1) | 3/3/2*/2 = **10** (*N chỉ đúng với góc đã đổi) |
| Khoảng trống mạnh nhất | Leave-one-institution-out trên SLICE-3D: 11 truy vấn + review 2026 không thấy; bài tổng kết cuộc thi kêu gọi đúng việc này | Benchmark AI-TOD-R (27 phương pháp) không có YOLO; STAL chỉ thử trên COCO — **đối chiếu PDF** | Chưa có adapter phương ngữ trên ViMD; nhưng lớp cơ chế đông (GLoRIA, HLoRA, MAS-LoRA) | Chưa ai đặt diffusion đối đầu PatchCore/RD4AD trên cùng giao thức định vị OCT |
| Rủi ro kết quả âm | Trung bình: chỉ 393 ca dương, chênh 0.005–0.01 pAUC khó có ý nghĩa thống kê | Trung bình: OA-STAL có thể không hơn STAL | Trung bình–cao: tầng tỉnh (~1.3 h/tỉnh) có thể không giúp | **Cao:** diffusion-reconstruction trên OCT gần như chắc thua phương pháp đặc trưng |
| Nếu ý chính thất bại vẫn còn gì để nộp | **Mạnh:** benchmark sạch rò rỉ + bảng LOIO đứng độc lập | **Mạnh:** bảng benchmark YOLO-OBB trên AI-TOD-R đứng độc lập | Yếu: chỉ còn phân tích oracle gap | Trung bình: bài chẩn đoán "kết quả âm có giải thích" |
| Chi phí cả kế hoạch `[ước lượng]` | **$43–79** (có 30% dự phòng); lần đắt nhất $2.6–4.4 | ~$60–80 lạc quan / $150–200 bi quan | $51 / $99 / $196 (có 15% dự phòng) | $27–86 lõi (+$10–39 tùy chọn) |
| Độ khó kỹ thuật cho sinh viên | Thấp–vừa (GBDT + CNN ảnh nhỏ 133 px, PyTorch) | Vừa–cao (sửa assigner trong Ultralytics + chuyển định dạng đánh giá) | Vừa–cao (fine-tune Whisper, ~60 GB audio, LoRA routing) | Cao (train diffusion + suy luận nhiều bước + đánh giá pixel) |
| License / tái lập | Theo từng cơ sở (CC-BY / CC-BY-NC / CC-0) — ổn cho nghiên cứu | Học thuật; có thể phải đăng ký xView | **CC BY-NC-ND → không được phát hành model** (giảm khả năng tái lập) | OCT2017 CC BY 4.0; RESC chỉ "research community"; RETOUCH phải đăng ký |
| Khớp nội dung DPL302m | Tốt (CNN, mất cân bằng dữ liệu, chiến lược ML) | **Rất tốt** (object detection, slide 4.3) | Tốt (mô hình chuỗi, Transformer — Part 4) | Yếu (diffusion không có trong slide môn) |
| Tier · Venue | T1 · Q4/Scopus/ISIC@MICCAI khả thi cao · Q3 có điều kiện · không Q1 | T1 · như bên trái | T1 · như bên trái | T1 · Q4/workshop khả thi kể cả kết quả âm · Q3 có điều kiện khó · không Q1 |

## 3. Khuyến nghị

**Xếp theo điểm rubric:** T2-6 (11) > T1-16 = T1-3 (10) > T1-7 (9).

**Xếp theo khuyến nghị của admin** (thêm 3 yếu tố rubric không đo: rủi ro kết quả âm, phương án lùi, độ khó kỹ thuật):

1. **T2-6 — Melanoma SLICE-3D: khuyến nghị chốt.**
   - Điểm cao nhất, rẻ nhất, dễ triển khai nhất.
   - Khoảng trống leave-one-institution-out kiểm chứng tốt.
   - Có phương án lùi mạnh (benchmark sạch rò rỉ vẫn nộp được).
2. **T1-7 — YOLO-OBB vật thể tí hon: phương án thay thế mạnh**, nếu bạn muốn đi hướng thị giác/phát hiện đối tượng.
   - Khoảng trống đối chiếu PDF.
   - Khớp môn học nhất.
   - Có phương án lùi (bảng benchmark).
   - Điểm thấp hơn T1-16 một bậc, nhưng xếp trên vì phương án lùi mạnh hơn và không bị chặn phát hành model.
3. **T1-16 — ViMD:** chỗ đóng góp mới bị nén bởi GLoRIA/HLoRA. Không phát hành được model. Ngân sách kịch bản bi quan vượt $100.
4. **T1-3 — OCT:** rủi ro kết quả âm cao nhất. Diffusion ngoài nội dung môn. Phải bỏ mục tiêu "AUC > 0.95" của sheet.

**Trả lời câu hỏi trước của user ("chốt #7 ngon đúng không"):** #7 **làm được và có căn cứ**, nhưng **không phải lựa chọn tốt nhất** theo bằng chứng vòng 3.
T2-6 hơn #7 ở điểm, chi phí, độ khó và độ chắc của khoảng trống. #7 chỉ hơn T2-6 ở độ khớp với nội dung môn học.

**Điểm chung của cả 4 đề tài** (nói thẳng): đều **T1**. Mục tiêu Q4/hội nghị là thực tế, Q3 cần điều kiện, Q1 không đạt với $100.
Con đường thực tế duy nhất để nhắm cao hơn là xin **Modal academic credits (tới $10k)** rồi mở rộng sang T2.

## 4. Điều chỉnh claim (REVISION theo research-proposal-integrity §3)
- **C-2** (2026-09-29, T2-6): trước đây ghi "ISIC@MICCAI workshop or Q3; Q2 only if module differs from DMT-Quadruplet…".
  → **REVISION**, nguyên nhân **bằng chứng mới**: MelDD, SLIMP, UDA-Net đã có module ngữ cảnh bệnh nhân.
  Bỏ nhánh Q2 → dòng mới **C-4**.
- **C-1** (2026-09-29, T1-16): trước đây ghi "Q2–Q3 only if T2 confirmed by lit scan".
  → **REVISION**, nguyên nhân **bằng chứng mới**: GLoRIA 2026, HLoRA, MAS-LoRA cùng lớp cơ chế. Đường lên T2 gần như đóng → dòng mới **C-5**.
- **T1-3:** claim mới **C-6**.
- **C-3** (#7): giữ nguyên.

## 5. Việc cần user quyết
1. Chốt đề tài: **T2-6 (khuyến nghị)** hay #7, hoặc đề tài khác trong bảng.
2. Nếu chọn T1-3: chấp nhận bỏ mục tiêu "AUC > 0.95 trên OCT2017" của sheet.
3. Nộp đơn **Modal academics** song song (không phụ thuộc đề tài).
4. Sau khi chốt: chạy thử (pilot) trên Modal ($1–3) để thay ước lượng chi phí bằng số đo thật.
