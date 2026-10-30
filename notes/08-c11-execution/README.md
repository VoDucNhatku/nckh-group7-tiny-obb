# 08 — Chạy C-11 trên Colab

**Trạng thái:** hiện hành. Các run trong notebook là **thăm dò**: chưa có `experiments/preregistration.md`.

| File | Nội dung |
|---|---|
| [t07-c11-notebook-explained-2026-10-26.md](t07-c11-notebook-explained-2026-10-26.md) | Giải thích từng ô của [`C11_colab.ipynb`](../../C11_colab.ipynb) (commit `58e2805`); kết quả A0/A1/A8/A2 × 3 seed trên giao thức woX; các vấn đề cần sửa; việc tiếp theo; nhận định venue (không đổi ledger) |
| [t07-c11-novelty-plan-2026-10-30.md](t07-c11-novelty-plan-2026-10-30.md) | Kế hoạch C11x: 5 hướng (head × sàn, số mẫu dương → recall, sàn theo số ứng viên K, góc theo kích thước, đánh giá chặt chẽ); câu hỏi, giả thuyết, ngưỡng, chi phí GPU, rủi ro; đi cùng `experiments/preregistration.md`, `scripts/c11x/`, `notebooks/` |
| [t07-c11x-handoff-2026-10-30.md](t07-c11x-handoff-2026-10-30.md) | Bàn giao C11x (30/10): notebook phân tích đã chạy tới đâu, kết quả sớm của hướng 1, vấn đề Colab bị ngắt khi bootstrap, việc tiếp theo, cách chạy tiếp trên Colab của người khác |

Code mà notebook C11 gọi (`scripts/c11/`) và các file kết quả (`experiments/runs-woX/`, JSON) hiện chỉ có trên Drive của nhóm, chưa có trên GitHub. Từ 30/10 `.gitignore` đã cho phép `scripts/c11/`; đẩy lên qua PR. Code C11x (`scripts/c11x/`) độc lập với `scripts/c11`, trừ các bước chấm và bootstrap mà notebook gọi qua Drive.
