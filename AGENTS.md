# AGENTS.md: quy tắc cho AI và thành viên khi làm việc trong repo này

Đọc file này **trước khi** thêm tài liệu, viết nghiên cứu hoặc trả lời về hướng đề tài. Mọi AI agent (Claude Code, Codex, Antigravity, Copilot…) và mọi thành viên đều theo các quy tắc ở đây. `CLAUDE.md` chỉ trỏ về file này.

## 1. Dự án trong 5 dòng

- NCKH nhóm 7, môn DPL302m, FPTU. Đề tài gốc #7: *Multi-scale Aerial Object Detection and Segmentation*.
- Bản đã nộp trường: `notes/02-proposal/Group7.pdf` (C-10: YOLO-OBB trên AI-TOD-R, chẩn đoán STAL). Không thay bản nộp này.
- Từ 13/10 nhóm mở lại nghiên cứu theo hướng phát hiện vật thể tí hon nhìn từ UAV (UAV-view tiny-object detection). Hướng này không bắt buộc dùng YOLO, OBB hay STAL.
- **Trạng thái hiện hành** là C-20 (30/10), REVISION của C-19 (15/10, `notes/07-audits/t07-q2-audit-2026-10-15/REPORT.md`):
  - đã chạy 12 run **thăm dò** của C-11 (A0/A1/A8/A2 × 3 seed, woX), trước preregistration: `C11_colab.ipynb`, `notes/08-c11-execution/`;
  - kế hoạch C11x và preregistration PREREG-C11X-v1 (`experiments/preregistration.md`): không chấm hay train mới trước khi file này có trên `main`;
  - chưa có kết quả xác nhận; chưa có band venue.
- Repo **public**.

## 2. Bản đồ thư mục

| Đường dẫn | Chứa gì | Trạng thái |
|---|---|---|
| `README.md` | Cổng vào cho người: đề tài, trạng thái, đọc gì trước | Hiện hành |
| `ROADMAP.md` | Kế hoạch 4 tuần, các cổng go/no-go | Hiện hành |
| `notes/RESEARCH-START-HERE.md` | Thứ tự đọc bộ nghiên cứu | Hiện hành |
| `notes/claims-ledger.md` | Sổ claim về novelty/venue (C-1 → C-19), **chỉ thêm, không sửa** | Hiện hành |
| `notes/INDEX.md` | Sổ đăng ký mọi tài liệu (id · worker · path · tóm tắt) | Hiện hành |
| `notes/01-topic-selection/` | Chọn đề tài (vòng 1–3) | Lịch sử |
| `notes/02-proposal/` | Proposal đã nộp và bằng chứng đi kèm | Bản nộp (cố định) |
| `notes/03-foundation/` | Kiến thức nền: sổ tay, digest DL, hỏi đáp | Tham khảo |
| `notes/04-slr/` | SLR 80 bài, **tạm dừng**, toàn bộ ở `_local/` | Lịch sử, chỉ có ở máy |
| `notes/05-venue-direction/` | Phản biện venue và hướng nâng cấp (11–15/10) | Lịch sử; đã bị C-19 sửa |
| `notes/06-uav-research-2026-10-13/` | Corpus 50 bài, problem map, deep study | Nền nghiên cứu hiện hành |
| `notes/07-audits/` | Audit C-19, phân tích lỗi | Hiện hành cho phần venue/hình học |
| `notes/08-c11-execution/` | Giải thích notebook C11, kế hoạch C11x | **Hiện hành** |
| `notes/99-archive/` | Bản đã bị thay (proposal v1, roadmap 14 tuần…) | Lưu trữ |
| `notes/MOVED-2026-10-15.json` | Bảng ánh xạ đường dẫn cũ → mới sau lần sắp xếp 15/10 | Tra cứu |
| `scripts/` | Script dựng hình và docx; `scripts/c11x/` code C11x + test; script SLR ở local | `scripts/c11/` vẫn chỉ ở Drive |
| `C11_colab.ipynb`, `notebooks/` | Notebook Colab C11 (đã chạy) và C11x (phân tích, train sàn K) | Hiện hành |
| `experiments/` | `preregistration.md`; mỗi lần chạy một thư mục `YYYY-MM-DD-<run>/` | Run C11 ở Drive, chưa đồng bộ |
| `paper/` | Bản thảo bài báo | Chưa bắt đầu |
| `papers/`, `logs/`, `scripts/t07-slr/data/` | PDF bài báo, log, cache | **Chỉ có ở máy, không lên Git** |

Ledger và các note cũ ghi đường dẫn cũ (`notes/t07-…`). Khi gặp đường dẫn không tồn tại, tra `notes/MOVED-2026-10-15.json`.

## 3. Đọc gì trước khi làm việc

**Trước khi trả lời về hướng, novelty hoặc venue,** đọc đủ các mục sau, không chỉ dòng ledger liên quan:

1. `README.md`, mục "Trạng thái hiện hành".
2. `notes/claims-ledger.md`: header và **mọi dòng còn active**, kể cả các dòng quy định phạm vi (C-13 → C-15, C-19).
3. `notes/07-audits/t07-q2-audit-2026-10-15/REPORT.md`.
4. `notes/06-uav-research-2026-10-13/t07-deep-study/RESEARCH-PROMPT.md`: hợp đồng bằng chứng của dự án.
5. `notes/07-audits/t07-error-analysis-2026-10-15/ANALYSIS.md` §6: các lỗi đã từng mắc, không lặp lại.

**Nhãn có hai nghĩa:** "hướng A" từng được dùng cho hai việc khác nhau: tách scale khỏi cách học (13/10) và STAL/coverage (14/10). Khi người dùng dùng một nhãn có thể hiểu hai nghĩa, **hỏi lại một câu** trước khi làm.

## 4. Thêm tài liệu mới: đặt ở đâu, đặt tên thế nào

| Loại | Đặt ở | Tên |
|---|---|---|
| Một note nghiên cứu hoặc phản biện | Thư mục số phù hợp ở bảng §2 | `t07-<chủ-đề>-<YYYY-MM-DD>.md` |
| Một đợt nghiên cứu ≥3 file | Thư mục con `t07-<chủ-đề>-<YYYY-MM-DD>/` | Có `REPORT.md` hoặc `README.md` làm cổng vào |
| Audit hoặc phản biện một kết luận cũ | `notes/07-audits/t07-<chủ-đề>-<YYYY-MM-DD>/` | `REPORT.md` cùng các file chi tiết |
| Nhóm việc mới chưa có thư mục | Tạo `notes/0N-<tên-tiếng-Anh>/` kèm `README.md` | Số tiếp theo |
| Kết quả chạy | `experiments/YYYY-MM-DD-<run>/` | Theo `experiments/README.md` |
| Tài liệu chỉ để ở máy (nháp, bản render, dữ liệu riêng) | Thư mục `_local/` trong thư mục số tương ứng | Git tự bỏ qua mọi `_local/` |
| PDF bài báo | `papers/` (chỉ ở máy) | `<Họ><Năm>-<tiêu-đề-ngắn>.pdf` |
| Cache tải về (HTML, text, JSON tìm kiếm) | `sources/` trong thư mục của đợt | Kèm `sources/README.md` giải thích; Git bỏ qua nội dung |
| Script | Cạnh tài liệu nó sinh ra, hoặc `scripts/` | Tên tiếng Anh, dùng `Path(__file__)` thay vì đường dẫn tuyệt đối |

**Sau khi thêm file:**

1. Thêm một dòng vào `notes/INDEX.md`.
2. Nếu file có claim về novelty hoặc venue, thêm dòng vào ledger (§6).

**Mở đầu mỗi note nghiên cứu** bằng: ngày · người hoặc model viết · đã đọc lại những gì · độ sâu đọc của từng nguồn.

**Khi tài liệu bị thay:**

- Không xóa. Thêm hộp đính chính ở đầu file, dẫn tới bản thay thế.
- Chỉ chuyển vào `99-archive/` khi toàn bộ nội dung đã được thay.
- Sau khi chuyển, cập nhật link và `INDEX.md`.

## 5. PDF và bản quyền

- **Không đưa PDF bài báo lên repo.** Repo public, phần lớn bài có bản quyền của nhà xuất bản.
- Trong note, ghi URL nguồn gốc của bài: arXiv, DOI, hoặc trang nhà xuất bản, kèm phiên bản.
- Chỉ PDF do nhóm tự làm (proposal, sổ tay, hình) được lên repo.

## 6. Quy tắc bằng chứng và claim

1. **Không bịa.** Mỗi con số phải có nguồn: URL kèm mục/bảng/trang, hoặc thư mục run. Chưa xác minh thì ghi `[chưa xác minh]`; số ước lượng thì ghi `[ước lượng]` kèm cách tính.
2. **Ghi đúng độ sâu đọc**, dùng 3 mức: `abstract` / `grep từ khóa` / `đọc method + bảng`.
   - Câu dạng "không có", "chỉ còn", "không phụ thuộc" cần mức thứ 3.
   - Grep từ khóa không bắt được sự phụ thuộc viết bằng ký hiệu toán. Ví dụ đã gặp: Eq.1–2 của O2-DETR.
3. **Nguồn trích phải cùng loại bài toán.**
   - UAV nhìn xuống vật dưới mặt đất **khác** bài phát hiện chính chiếc drone (anti-UAV, Drone-vs-Bird).
   - Ảnh vệ tinh/hàng không tổng hợp **khác** ảnh UAV.
4. **Toán:** mỗi công thức gắn đúng một nhãn `[cited]`, `[derived]` hoặc `[design]`. Với `[derived]`:
   - ghi một câu "định lý này **không** nói gì";
   - thử một phản ví dụ nhỏ bằng số trước khi dùng nó làm điều kiện.
   
   Ba trường hợp đã bị nhầm:
   - Bảo đảm có ứng viên ≠ AP tối ưu.
   - Cùng kỳ vọng ≠ cùng phân phối.
   - Cận trên của độ nhạy ≠ giới hạn khả năng xác định.
5. **Nhân quả:** không suy nguyên nhân từ một chỉ số. Câu dạng "nếu X thì nguyên nhân là Y" phải kèm can thiệp có đối chứng. Các nguyên nhân thường chồng lên nhau, nên không có cách chia phần trăm duy nhất.
6. **Venue:**
   - Tier T1/T2/T3 chỉ mô tả loại can thiệp, **không quy ra quartile**.
   - Chưa có bằng chứng thì ghi "chưa gán band".
   - Không nói "đủ Q1/Q2", "đầu tiên", "SOTA" khi chưa có kết quả.
7. **Ledger chỉ thêm, không sửa.** Đổi claim thì thêm dòng `REVISION` mới, ghi nguyên nhân và **loại bằng chứng** (kết quả chạy / đọc method / abstract / suy luận / phản biện của người dùng). Chỉ có abstract hoặc suy luận thì ghi "đề xuất sửa" trong note, không đổi điều kiện venue.
8. **Kiểm bịa không phải kiểm suy luận.** Một lượt kiểm nguồn chỉ cho biết claim có nguồn. Khi báo kết quả, ghi rõ: "đã kiểm nguồn; đã / chưa kiểm suy luận". Kết luận quan trọng nên có phản biện độc lập (người khác hoặc model khác) trước khi coi là chắc.
9. **Khi tóm tắt một báo cáo do người hoặc model khác làm,** ghi đúng người làm theo header của file đó.

## 7. Git

- Repo **public**. Không commit dữ liệu ảnh, trọng số (`*.pt`), `kaggle.json`, `.env`, API key, hay đường dẫn máy cá nhân.
- Quy trình: branch `<tên>/<việc>` → Pull Request → merge. Không push thẳng `main`.
- Commit message viết tiếng Anh, ngắn gọn. Không thêm dòng `Co-Authored-By` của AI.
- `.gitignore` dùng kiểu whitelist ở thư mục gốc. Trong `notes/`, mọi file **được chia sẻ mặc định**, trừ `_local/` và `sources/`.
  - Thêm file ở **thư mục gốc** thì phải thêm dòng `!/<tên-file>`.
  - Trước khi commit, chạy `git status` để chắc không có file riêng tư nào lọt vào.
