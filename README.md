# Nhóm 7 · NCKH DPL302m — Tiny Oriented Object Detection (YOLO-OBB)

> **Where Do Tiny Oriented Objects Lose Their Positives / Training Signal?**
> Candidate-Region Geometry in Real-Time YOLO-OBB Detectors on AI-TOD-R

Đây là repo nghiên cứu khoa học của Nhóm 7, môn DPL302m (Deep Learning), kỳ 5, FPTU. Repo là **nơi theo dõi tiến độ chung**:
- proposal và các quyết định đã chốt nằm trong `notes/`;
- công việc được chia thành Issues và gom theo Milestones;
- kết quả chạy thí nghiệm sẽ nằm trong `experiments/`.

| | |
|---|---|
| Mentor | Hà Anh |
| Thành viên | Võ Đức Nhật · Trần Lợi Kiều Nhi · Trần Nguyễn Minh Hải · Nguyễn Tấn Tài |
| Đề tài gốc | Tier 1 #7 trong danh sách đề tài của giảng viên: *Multi-scale Aerial Object Detection and Segmentation* |
| Hướng đã chốt | **C-10**: benchmark YOLO-OBB trên AI-TOD-R, chẩn đoán quy tắc chọn vùng ứng viên (STAL), thử OA-STAL v2 |
| Thời gian | **4 tuần, 11/10/2026 → 08/11/2026** (đổi ngày 2026-10-13; kế hoạch 14 tuần cũ lưu ở `ROADMAP-14w-backup.md`) |

## Trạng thái hiện tại (cập nhật 2026-10-08)

**Proposal đã viết xong. Chưa chạy thí nghiệm nào.** Proposal tự ghi là *chưa chạy được như mô tả* cho tới khi qua **Pha 0**, gồm 4 việc:
- đăng ký xView;
- chạy được bộ đánh giá AITODReval;
- đo tốc độ pilot trên Kaggle;
- kiểm converter.

Tiến độ chi tiết xem [ROADMAP.md](ROADMAP.md) và tab **Issues / Milestones**.

## Đề tài trong 1 phút

- **Vấn đề.** Vật thể trong AI-TOD-R rất nhỏ (trung bình 10,6 px). Một hộp nhỏ hơn bước lưới (stride) có thể không chứa điểm neo nào. Khi đó nó không được gán mẫu dương và mô hình không học được từ vật thể đó.
- **STAL** (Small-Target-Aware Label Assignment) là bản sửa của Ultralytics cho vấn đề này. STAL mới chỉ được thử trên COCO với hộp ngang. Quy tắc của nó cho hộp xoay đã đổi 3 lần trong năm 2026.
- **Bốn câu hỏi nghiên cứu:**

| RQ | Nội dung |
|---|---|
| RQ1 | Benchmark YOLO11/26-OBB trên AI-TOD-R bằng bộ đánh giá chính thức, tách theo kích thước |
| RQ2 | Chẩn đoán các quy tắc ứng viên: không có sàn, STAL-8, STAL-16 |
| RQ3 | OA-STAL v2 kèm quy tắc giải quyết xung đột. So sánh chính: **A4 với A2** |
| RQ4 | Kiểm lại trên dataset thứ hai (SODA-A, dự phòng DOTA-v2.0) |

- **Mức kỳ vọng:** novelty tier **T1** → Q4 hoặc hội nghị Scopus, **có điều kiện**. Điều kiện ghi trong `notes/claims-ledger.md`, dòng C-10. Không có claim Q1/Q2.

## Đọc gì trước

1. [notes/Group7.pdf](notes/Group7.pdf): bản nộp trường, 11 trang, theo mẫu AITA Lab. Slide thuyết trình đi kèm: [notes/Group7-proposal-presentation.pptx](notes/Group7-proposal-presentation.pptx), 18 slide, khoảng 15 phút, có speaker notes.
2. [notes/t07-c3-proposal-v2-EN.md](notes/t07-c3-proposal-v2-EN.md): bản đầy đủ có công thức, 8 nhánh thí nghiệm, cổng khả thi (§10), timeline (§11), rủi ro (§12) và danh mục tham khảo có link.
3. [ROADMAP.md](ROADMAP.md): checklist Pha 0 và 9 giai đoạn.
4. [notes/claims-ledger.md](notes/claims-ledger.md): mọi khẳng định về novelty/venue và lịch sử sửa đổi.
5. [notes/t07-foundation-G7-VI-v3.pdf](notes/t07-foundation-G7-VI-v3.pdf): sổ tay nền kiến thức tiếng Việt, 61 trang (detection, AI-TOD-R, TAL/STAL, OA-STAL v2, thiết kế thí nghiệm, thực hành Phase 0 ở phần P, bảo vệ proposal ở phần D). Phụ lục tra nhanh ở mục E5, cuối sổ tay. Bản v2 cũ hơn vẫn giữ để đối chiếu. Kết quả rà soát nằm ở [notes/t07-foundation-review-2026-10-09.md](notes/t07-foundation-review-2026-10-09.md).
6. [notes/t07-session-qa-2026-10-09.md](notes/t07-session-qa-2026-10-09.md): hỏi đáp về đề tài (chủ đề, gap, RQ, luồng hoạt động, chống rò rỉ dữ liệu, venue) và vòng tự phản biện về claim Q4 và số lần train.

## Cấu trúc repo

```
├── README.md                    ← file này
├── ROADMAP.md                   ← kế hoạch 4 tuần + cổng go/no-go + checklist (tick khi xong)
├── ROADMAP-14w-backup.md        ← kế hoạch 14 tuần cũ (đã thay)
├── notes/
│   ├── t07-c3-proposal-v2-EN.md        ← proposal đầy đủ (bản gốc)
│   ├── Group7.pdf                      ← proposal theo mẫu trường (bản nộp)
│   ├── Group7-proposal-presentation.pptx ← slide thuyết trình proposal (18 slide)
│   ├── t07-c3-proposal-template-EN.docx← nguồn của Group7.pdf
│   ├── t07-c3-introduction-EN.pptx     ← 20 slide giới thiệu chủ đề cho cả lớp
│   ├── figs/                           ← hình 1–2 của proposal
│   ├── t07-c3-evidence-dossier.md      ← bằng chứng theo trang/bảng/dòng code
│   ├── t07-c3-novelty-rescan.md        ← quét độ mới + 10 phản biện giả định
│   ├── claims-ledger.md                ← sổ khẳng định (append-only)
│   ├── t07-critique-q2-2026-10-11.md   ← phản biện mức Q2 + kế hoạch 4 tuần (cổng 0–5)
│   ├── t07-dl-digest-2026-10-11.md     ← dự án qua lăng kính DL: dữ liệu, mô hình, loss (kiểm trong code 8.4.174), train, đánh giá
│   ├── t07-dl-from-slides-VI.pdf       ← sổ tay 54 trang: khái niệm slide DPL302m → dự án (nguồn + lab ở t07-dl-from-slides/)
│   ├── r3-final-comparison.md          ← vì sao chọn #7 (so sánh 4 đề tài)
│   ├── t07-tier-upgrade.md             ← hướng nâng cấp C-7 (ứng viên)
│   ├── synthesize-gaps-t07-q4-priority.md ← hướng dự phòng C-8, C-9
│   └── t07-proposal.md                 ← proposal v1 (đã thay thế, giữ để đối chiếu)
├── scripts/t07-slr/
│   ├── p12_proposal_figures.py  ← vẽ notes/figs/*.png
│   └── p13_build_proposal_docx.js ← dựng file .docx theo mẫu trường
├── experiments/                 ← mỗi lần chạy 1 thư mục (xem experiments/README.md)
└── paper/                       ← bản thảo bài báo (khi bắt đầu viết)
```

**Không có trong repo:** PDF bài báo (có bản quyền), thẻ đọc paper và các file của bài tổng quan tài liệu có hệ thống (SLR). Các file này giữ ở máy của người làm SLR. Vì vậy một số đường dẫn trong proposal, như `papers/...`, `logs/...` và `scripts/t07-slr/data/...`, chỉ tồn tại ở bản local.

## Cách làm việc nhóm

- **Mỗi việc là 1 Issue.** Tự assign khi nhận. Khi đóng Issue, ghi kết quả và link tới file.
- **Branch → Pull Request → merge.** Không push thẳng lên `main`. Đặt tên branch `<tên>/<việc>`, ví dụ `hai/pilot-kaggle`. PR ghi `Closes #<số issue>`.
- **Commit message** viết tiếng Anh, ngắn gọn, ví dụ `Add AITODReval converter test`.
- **Tiến độ:** khi xong một mục trong [ROADMAP.md](ROADMAP.md), tick ô đó trong cùng PR.
- **Không commit:** dữ liệu (ảnh xView/AI-TOD), trọng số `*.pt`, `kaggle.json`, `.env`, API key. `.gitignore` đã chặn sẵn. Repo này **public**.
- **Thêm file mới vào `notes/` hoặc `scripts/`:** `.gitignore` dùng kiểu whitelist, nên phải thêm dòng `!/notes/<tên-file>` thì file mới được theo dõi.

## Quy tắc nghiên cứu (bắt buộc)

1. **Không bịa.** Mọi con số (mAP, kích thước dataset, giờ GPU) phải có nguồn: URL, trang/bảng của bài, hoặc thư mục run trong `experiments/`. Chưa xác minh thì ghi `[chưa xác minh]`. Số ước lượng thì ghi `[ước lượng]` kèm cách tính.
2. **Chỉ dùng nguồn học thuật hoặc chính thức:** arXiv, CVF, IEEE, Springer, Elsevier, OpenReview, trang dataset, GitHub chính thức. Không lấy số liệu từ blog, Medium hay bản tóm tắt AI.
3. **Ghi giả thuyết trước khi train RQ3.** Ghi vào `experiments/preregistration.md` ở tuần 3, có ngày. Sau đó không sửa dự đoán.
4. **Claim venue** (Q1–Q4) phải theo novelty tier T1/T2/T3 kèm điều kiện, và ghi vào `notes/claims-ledger.md`. Khi đổi claim thì thêm dòng mới, **không sửa thầm**.
5. **Đặt tên:** ghi chú là `notes/t07-<chủ đề>.md`; mỗi lần chạy là một thư mục `experiments/<YYYY-MM-DD>-<run-name>/`.

## Lịch sử

| Ngày | Việc | File |
|---|---|---|
| 2026-09-29 | Vòng 1: sàng lọc 32 đề tài | (local) |
| 2026-10-01 | Vòng 2: nghiên cứu sâu #7, proposal v1 (C-3) | notes/t07-proposal.md |
| 2026-10-02 | Vòng 3: sàng lọc lại công bằng 32 đề tài, so sánh 4 đề tài; nhóm chọn #7 | notes/r3-final-comparison.md |
| 2026-10-05 → 07 | SLR #7: chốt 80 bài; benchmark, PRISMA, Excel cho nhóm. **Tạm dừng** sau khi chốt proposal | (local) |
| 2026-10-07 | Xếp ưu tiên hướng Q4; các hướng dự phòng C-8, C-9 | notes/synthesize-gaps-t07-q4-priority.md |
| 2026-10-08 | Proposal v2 (C-10, REVISION của C-3), bản theo mẫu trường, slide giới thiệu | notes/t07-c3-* |
| 2026-10-08 | Tạo repo GitHub, ROADMAP, Issues/Milestones | README.md, ROADMAP.md |
| 2026-10-08 | Group7.pdf thành bản nộp duy nhất; slide thuyết trình proposal | notes/Group7.pdf, notes/Group7-proposal-presentation.pptx |
| 2026-10-11 → 13 | Digest DL của dự án; phản biện mức Q2 (kết luận: Q2 không bảo vệ được trong 4 tuần); ledger C-12 (REVISION của C-7); ROADMAP nén còn 4 tuần | notes/t07-dl-digest-2026-10-11.md, notes/t07-critique-q2-2026-10-11.md, ROADMAP.md |
