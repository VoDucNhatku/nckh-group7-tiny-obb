# Giải thích notebook `C11_colab.ipynb`: code, kết quả và đánh giá

**Ngày:** 26/10/2026 · **Người viết:** Claude Code (Opus 5.5), theo yêu cầu trong một phiên chat · **Đối tượng:** `C11_colab.ipynb` ở commit `58e2805` (21/10/2026, tác giả commit "Ney"), repo `VoDucNhatku/nckh-group7-tiny-obb`, nhánh `main`.

**Kiểm lại ngày 28/10/2026, trước khi đưa lên repo:** nhánh `main` vẫn ở commit `58e2805`. Repo chưa có `scripts/c11/`, `experiments/preregistration.md` hay file kết quả run, nên các nhận định về trạng thái repo trong file này vẫn đúng tới ngày đó.

**Đã đọc lại:**
- toàn bộ 35 ô của notebook: code, markdown, output (log train 12 run đọc các dòng chính);
- proposal v2 (`notes/02-proposal/t07-c3-proposal-v2-EN.md`) §2.2, §5, §6, §7.4, §8, §13;
- `ROADMAP.md`, ledger C-10 → C-19, `REPORT.md` của audit C-19, `RESEARCH-PROMPT.md`;
- mục Q17 và H1 trong `notes/03-foundation/t07-session-qa-2026-10-09.md`.

**Độ sâu đọc:**
- Notebook: đọc đủ.
- Các module `scripts/c11/*.py` mà notebook gọi: **không có trong repo**, nên không đọc được. Mọi mô tả về phần bên trong module là suy ra từ tên hàm, markdown và output, gắn nhãn [suy ra].
- Không chạy lại notebook. Mọi số lấy từ output đã lưu trong file `.ipynb`.

**Không phải:** một dòng ledger. Phần đánh giá venue (§8) là nhận định đề xuất, theo AGENTS.md §6.7.

| Nhãn | Nghĩa |
|---|---|
| [#N] | Đọc trực tiếp từ ô #N. Ô đánh số từ 0, tính cả ô markdown |
| [tính lại] | Tôi tính từ số trong output. Số gốc làm tròn 4 chữ số, nên kết quả có sai số làm tròn |
| [suy ra] | Suy luận từ lời gọi hàm, tên hàm hoặc markdown; chưa kiểm trong mã module |
| [chưa kiểm] | Nghi vấn, cần mở code hoặc chạy lại để xác nhận |
| [nguồn: …] | Lấy từ tài liệu khác trong repo, có ghi vị trí |

**Thang điểm.** Notebook báo AP trên thang 0–1. Trong file này, "1 điểm AP" nghĩa là 0,01 trên thang đó. Ví dụ ΔAP = 0,0035 là 0,35 điểm.

---

## 0. Tóm tắt

- **Notebook làm gì.** Chạy proposal C-11 trên Colab A100, theo thứ tự:
  1. thống kê nhãn (Cổng 0);
  2. kiểm bộ chấm AITODReval (Cổng 2b, 2c);
  3. đếm vùng ứng viên từ nhãn (RQ2 offline, mới thử trên 300 file);
  4. dựng dataset YOLO, chạy pilot đo tốc độ;
  5. train YOLO26n-OBB với 4 quy tắc vùng ứng viên A0/A1/A8/A2, mỗi quy tắc 3 seed;
  6. chấm trên tập test bằng AITODReval gốc, gộp bảng, bootstrap ghép cặp theo cụm cảnh.
- **Giao thức woX:** chỉ dùng ảnh không thuộc xView, tổng 18.730 ảnh: train 8.426, val 936, test 9.261. Kết quả không so được với Bảng II của bài AI-TOD-R.
- **Phần kỹ thuật làm tốt:**
  - khoá cứng phiên bản Ultralytics;
  - 55/55 unit test qua ở lần chạy cuối;
  - oracle cho AP = 0,996;
  - chấm lại một run bằng đường chấm nhanh lệch tối đa 9,4e-7;
  - bootstrap trên GPU khớp bản CPU 0/200 mẫu;
  - 12/12 run train đủ 24 epoch, cùng một recipe.
- **Kết quả (head e2e, 3 seed):**
  - **AP_vt** (vật < 8 px) tăng khi có sàn ứng viên: từ khoảng 0,041 lên 0,048–0,050, tức +17–22% tương đối hay +0,7–0,9 điểm. Đây là kết quả nhất quán nhất: run kém nhất có sàn vẫn cao hơn mọi run A0 [tính lại].
  - **AP tổng** tăng tối đa +0,35 điểm (A2). Mức này nhỏ hơn chênh lệch giữa các seed của riêng A2 (0,92 điểm).
  - **A1, A8, A2 chưa phân biệt được** với nhau. "Chưa phân biệt được" không có nghĩa là "tương đương", vì chưa khoá biên tương đương.
  - **Head nms** của A0 cao hơn head e2e của A0 khoảng 0,6 điểm AP, lớn hơn mọi hiệu ứng của arm.
- **Chưa xong:**
  - preregistration;
  - phân tích cơ chế của RQ2;
  - chấm head nms cho 8/12 run;
  - train A4;
  - seed 4–5.
- **Venue:** chưa đủ để ghi band Q4. Lý do ở §8.

---

## 1. Notebook trả lời câu hỏi gì

### 1.1 Vấn đề: vật tí hon không có ứng viên

YOLO đặt **điểm neo** (anchor point) ở tâm mỗi ô lưới trên ba tầng đặc trưng, bước (stride) 8, 16 và 32 px. Khi train, quá trình gán mẫu diễn ra như sau:

1. Một điểm neo chỉ được xét là **ứng viên** của một GT nếu nằm trong **vùng ứng viên** của GT đó (phép thử điểm-trong-hộp xoay).
2. Bộ gán TAL chọn top-k ứng viên theo điểm căn chỉnh.
3. TAL xử lý **xung đột** khi một điểm neo rơi vào vùng của nhiều GT.

GT nào không có ứng viên thì không có mẫu dương, nên không nhận tín hiệu học.

Mệnh đề 1 của proposal [nguồn: proposal §6]: nếu vị trí của vùng so với lưới là ngẫu nhiên đều, thì số ứng viên kỳ vọng là E[N] = |R| · Σ 1/s² ≈ 0,0205 · |R|, với |R| là diện tích vùng tính bằng px². Ví dụ: hộp 4×4 px dưới TAL có P(N = 0) ≥ 0,67.

### 1.2 STAL và lịch sử quy tắc

**STAL** tạo một hộp thay thế, chỉ dùng ở bước lọc ứng viên: cạnh nào nhỏ hơn `s_min` thì được thay bằng `s_ref`. Hộp gốc vẫn được dùng để tính điểm và hồi quy [nguồn: proposal §2.2, trích bài YOLO26 tr. 7–8].

Với hộp xoay, quy tắc trong Ultralytics đổi nhiều lần [nguồn: proposal §2.2]:

| Phiên bản | Quy tắc |
|---|---|
| ≤ 8.4.7 | không có sàn |
| 8.4.39 – 8.4.127 | cạnh < 8 → 16 (quy tắc trong bài báo) |
| ≥ 8.4.128, gồm bản 8.4.174 notebook dùng | cạnh < 16 → 16 |

Vì vậy notebook khoá cứng bản 8.4.174, rồi vá hàm gán mẫu để chọn quy tắc theo arm [#4].

### 1.3 Các arm

| Arm | Quy tắc vùng ứng viên [nguồn: proposal §7.4] | Vai trò | GT có vùng ứng viên bị đổi, trainval đầy đủ [#12, tính lại] |
|---|---|---|---|
| A0 | không có sàn (TAL gốc) | mốc dưới | 0% |
| A1 | cạnh < 8 → 16 (STAL-8, quy tắc công bố) | quy tắc trong bài YOLO26 | 66,5% (cạnh ngắn < 8) |
| A8 | cạnh < 11,31 → 11,31 (√2·8) | sàn phủ tối thiểu | 92,7% (cạnh ngắn < 11,31) |
| A2 | cạnh < 16 → 16 (STAL-16, mặc định của 8.4.174) | quy tắc hiện hành | 96,8% (cạnh ngắn < 16) |
| A4 | OA-STAL v2 (giữ hình dạng, diện tích tối thiểu) | phép thử phụ; **chưa train** | — |

Tỉ lệ ở cột cuối tính trên toàn bộ trainval, có cả ảnh xView. Tỉ lệ riêng cho phần woX chưa được in ra [chưa kiểm].

Điểm cần nhớ: **A2 đổi vùng ứng viên của gần như mọi GT trong AI-TOD-R**. Vì vậy A2 so với A0 gần như là "đổi toàn bộ cách chọn ứng viên", không phải một sửa đổi nhỏ chỉ cho vài vật.

### 1.4 Định lý phủ √2·s nói gì và không nói gì

[derived; nguồn: ROADMAP; phạm vi theo audit C-19] Một hình chữ nhật đóng có cạnh ngắn ≥ √2·s luôn chứa ít nhất một điểm của lưới vuông bước s, ở mọi vị trí và mọi góc. Với s = 8 thì √2·8 ≈ 11,31 px. Đây là lý do có arm A8.

Định lý này **không** nói:
1. GT sẽ có mẫu dương cuối cùng, vì sau bước ứng viên còn top-k và xử lý xung đột;
2. 11,31 px là sàn cho AP tốt nhất;
3. điều gì về tầng 16 và 32: sàn 11,31 chỉ bảo đảm có điểm neo trên lưới bước 8.

### 1.5 Hai head của YOLO26

YOLO26 có hai nhánh [#24]:

| Nhánh | Cách hoạt động | Tên trong notebook |
|---|---|---|
| one-to-one (o2o) | mỗi GT một dự đoán, suy luận không cần NMS | `e2e`, đặt `nms=False` |
| one-to-many (o2m) | nhiều dự đoán cho mỗi GT, cần NMS | `nms`, mặc định khi `nms=None` |

Proposal §8.2 yêu cầu báo riêng hai nhánh. Quy tắc vùng ứng viên được vá trong assigner nên tác động lên cả hai nhánh lúc train [suy ra từ #22: log chẩn đoán ghi theo từng nhánh o2m/o2o].

### 1.6 AITODReval

Thiết lập của bộ chấm [nguồn: proposal §8.2]:
- IoU từ 0,50 đến 0,95, bước 0,05;
- giữ tối đa **1.500 dự đoán cho mỗi (ảnh, lớp)**;
- bin theo diện tích: very tiny 2²–8², tiny 8²–16², small 16²–32², medium 32²–64².

Ultralytics đặt `max_det` cho cả ảnh, mặc định 300. Vì vậy lúc predict notebook đặt `max_det = 12.000` = 1.500 × 8 lớp [#24].

### 1.7 Giao thức woX

`PROTOCOL = "woX"` bỏ ảnh xView ở **cả** train lẫn test [#1]. Lý do: ảnh xView cần đăng ký riêng, và đây là nhánh dự phòng của Cổng 1 trong ROADMAP.

Hệ quả:
- 18.730 ảnh = 9.379 trainval + 9.351 test không thuộc xView [#12, tính lại]. Số này khớp đúng số PNG đã giải nén ở #10.
- Không so được với Bảng II của bài AI-TOD-R, vì bảng đó dùng đủ 28.036 ảnh.
- woX giữ khoảng 35% số GT của bản đầy đủ: 135.275 so với 380.174 ở trainval [#12, #19, tính lại]. Phần xView đóng góp phần lớn số xe.

**Một trùng hợp cần kiểm.** Hồ sơ của nhóm ghi DIA-YOLO đặt YOLOv11-OBB cạnh Bảng II trên "AITOD" **18.730 ảnh** [nguồn: `t07-c3-evidence-dossier.md` dòng 445; `t07-session-qa-2026-10-09.md` Q2]. Con số này trùng đúng số ảnh của woX.

[suy luận] Nhiều khả năng DIA-YOLO dùng cùng phần ảnh không-xView. Nếu đúng, DIA-YOLO thành đối chứng gần nhất về tập ảnh cho RQ1. Cần kiểm split của DIA-YOLO và định vị lại RQ1. Theo hồ sơ của nhóm, DIA-YOLO dùng ảnh RGB + depth, không tách bin, không dùng evaluator chính thức.

---

## 2. Môi trường, file code và thứ tự chạy

### 2.1 Môi trường

| Thành phần | Giá trị | Nguồn |
|---|---|---|
| GPU | NVIDIA A100-SXM4-40GB (metadata Colab `gpuType: A100`) | #3 |
| ultralytics | 8.4.174, có `assert` kiểm phiên bản | #5 |
| torch / numpy / Python | 2.11.0+cu130 / 2.1.3 / 3.13.15 | #5 |
| Ổ đĩa VM | 236 GB, còn trống 163 GB | #3 |
| Cách tính IoU hộp xoay | shapely (máy không có mmcv) | #14 |

### 2.2 Các file code mà notebook gọi

Danh sách lấy từ lệnh `ls` ở #26. Thư mục này nằm trên Drive (`repo/NCKH/scripts/c11`), **không có trên GitHub**.

| File | Kích thước | Sửa lần cuối | Vai trò [suy ra từ cách notebook gọi] |
|---|---|---|---|
| `aitodr_data.py` | 11,2 KB | 20/10 13:55 | thống kê Cổng 0, danh sách ảnh xView, dựng dataset YOLO, `scene_key` |
| `aitodr_evalkit.py` | 26,5 KB | 21/10 02:55 | nạp AITODReval gốc và vá, `load_gt`, vòng tròn, oracle, chuyển dự đoán sang dạng của evaluator |
| `stal_arms.py` | 24,3 KB | 20/10 07:08 | vá hàm gán mẫu của Ultralytics theo arm, kiểm phiên bản |
| `rq2_offline.py` | 8,7 KB | 20/10 08:29 | đếm ứng viên theo arm, chỉ từ nhãn |
| `c11_pipeline.py` | 7,9 KB | 21/10 02:56 | `RECIPE`, `train_arm`, `predict_and_eval`, `run_name` |
| `c11_bootstrap.py` | 20,9 KB | 21/10 06:10 | `load_cache`, `multi_pair_bootstrap` |
| `diag_bootstrap_device.py` | 3,6 KB | 21/10 06:16 | so engine bootstrap trên GPU với bản tham chiếu CPU |
| `check_geometry_c11.py` | 2,6 KB | 20/10 06:57 | kiểm hình học (đoán từ tên) |
| `build_notebook.py` | 20,2 KB | 20/10 11:31 | sinh ra chính notebook này (đoán từ tên) |
| `test_*.py` (5 file) | — | 20–21/10 | 55 test |

### 2.3 Thứ tự chạy thực tế

Số trong ngoặc vuông là số lần chạy (execution count) Colab hiển thị bên trái mỗi ô.

| Ô | Lần chạy | Việc |
|---|---|---|
| #2 → #23 | [39] → [51] | chạy tuần tự từ cấu hình đến train đủ 12 run |
| #29 | [54] | chấm lại A0_s1 bằng đường chấm nhanh |
| #30 | [56] | chấm head e2e cho các run còn lại |
| #32 | [57] | gộp bảng |
| #28 | [61] | chạy test: 1 test FAIL, trên bản code cũ còn trong `/content/c11` |
| #26 | [63] | liệt kê file code trên Drive |
| #27 | [65] | kiểm engine bootstrap GPU so với CPU |
| #25 | [66] | chép lại code mới, **55/55 test qua**, nạp lại module |
| #34 | [68] | bootstrap |

Hệ quả khi đọc notebook:
1. Output đang thấy là của **lần chạy cuối** của mỗi ô. Thứ tự trên trang không phải thứ tự chạy.
2. Test FAIL ở #28 chạy trên code cũ. Bootstrap ở #34 chạy sau khi 55/55 test đã qua ở #25.
3. Một số file `eval_e2e.json` và `eval_nms.json` được tạo ở các lần chạy không còn output, ví dụ lần [52]–[53] [suy ra: #30 không in A0_s1–s3 và A1_s1–s2, vì các file đó đã có sẵn].
4. Biến `TODAY` được đặt một lần ở #2 (in ra `2026-10-20`). Mọi thư mục và file kết quả vì thế mang ngày 20/10, kể cả file tạo ngày 21/10, ví dụ file bootstrap [suy ra].

### 2.4 Dữ liệu đi đâu

```
Drive/NCKH/data/{labels.zip, aitod_wo_xview_*_imgs.zip}
   │  (giải nén sang đĩa VM, nhanh hơn)
   ▼
/content/aitodr/{labels/, images_raw/, yolo_woX/}     ← dataset YOLO (ảnh được symlink)
   │
   ▼  train
Drive/NCKH/repo/NCKH/experiments/
   ├── 2026-10-20-gate0/gate0_stats.json
   ├── 2026-10-20-gate2-evaluator/gate2_evaluator.json
   ├── 2026-10-20-rq2-offline-woX/
   ├── 2026-10-20-dataset-woX/split_manifest.json
   ├── 2026-10-20-pilot/pilot.json
   ├── runs-woX/c11_<arm>_s<seed>/
   │      weights/{last.pt, best.pt}, c11_stal_arm.json, c11_assign_diag.jsonl, c11_done.json,
   │      eval_e2e.json, eval_nms.json, evalcache_e2e.npz, dota_e2e/
   ├── 2026-10-20-results-table-woX.csv
   └── 2026-10-20-bootstrap-woX-e2e.json
```

Thư mục `runs-woX/c11_<arm>_s<seed>/` không theo quy ước `experiments/<YYYY-MM-DD>-<run>/` của `experiments/README.md`. Khi đưa lên repo cần ánh xạ lại.

---

## 3. Giải thích từng phần

### Phần 0 — Cấu hình, cài đặt, test (#1–#7)

**#2 — cấu hình.**

```python
DRIVE      = Path("/content/drive/MyDrive/NCKH")
CODE_DIR   = DRIVE / "repo/NCKH/scripts/c11"      # bản sao code trên Drive
DATA_DRIVE = DRIVE / "data"                       # labels.zip và zip ảnh
EXP_DRIVE  = DRIVE / "repo/NCKH/experiments"      # kết quả ghi về đây
LOCAL      = Path("/content/aitodr")              # đĩa VM: giải nén và train ở đây
PROTOCOL   = "woX"
VERSION    = "oc"
ARMS       = ["A0", "A1", "A8", "A2"]
SEEDS      = [1, 2, 3]
DIAG_EVERY = 10
TODAY      = time.strftime("%Y-%m-%d")
```

Ý nghĩa từng biến:
- `PROTOCOL`: chọn woX hay full (§1.7).
- `ARMS`, `SEEDS`: tạo ra 4 × 3 = 12 run.
- `DIAG_EVERY = 10`: cứ 10 lần gọi assigner thì ghi chẩn đoán gán mẫu một lần, tốn thêm khoảng 2–3% thời gian theo chú thích trong ô.
- Output in ra: `2026-10-20 woX ['A0', 'A1', 'A8', 'A2'] [1, 2, 3]`.

**`VERSION = "oc"` cần ghi chú.** Đây là quy ước tham số hoá góc khi đổi đa giác 4 đỉnh sang (x, y, w, h, a). Comment trong ô ghi rằng config DCFL của AI-TOD-R dùng `le135`.
- IoU giữa hai **cùng một** hình chữ nhật không phụ thuộc cách tham số hoá.
- [chưa kiểm; dựa trên hiểu biết về mmrotate, cần mở mã nguồn] Các hàm đổi đa giác sang hình chữ nhật của từng version có thể tính khác nhau khi đa giác không vuông góc hoàn hảo: có hàm dùng `cv2.minAreaRect`, có hàm tính từ cạnh. Khi đó GT hình chữ nhật dưới `oc` và `le135` có thể lệch nhau.
- Ở #14, 69% GT có IoU vòng tròn < 0,999, nên đây không phải chi tiết thừa.
- Việc cần làm: chạy `roundtrip_check` và oracle với `le135` một lần, báo chênh lệch, và ghi lý do chọn `oc` vào bài.

**#3 — mount Drive, xem GPU.** A100 40 GB; đĩa còn trống 163 GB.

**#5 — cài đúng phiên bản.**

```python
!pip -q install "ultralytics==8.4.174" shapely gdown
assert ENV["ultralytics"] == "8.4.174"
```

Log train (#21, #23) báo có bản 8.4.183 mới hơn. Bỏ qua là đúng, vì quy tắc STAL thay đổi theo phiên bản (§1.2). `shapely` thay `mmcv` để tính IoU hộp xoay.

**#7 — chép code, chạy test.** Chép `scripts/c11` từ Drive vào `/content/c11` rồi chạy pytest: **44 passed** trong 20,19 giây.

Theo markdown #6, test kiểm:
- A2 trùng với mã gốc của Ultralytics;
- A0 khớp một phép thử độc lập;
- tập ứng viên lồng nhau giữa các arm;
- tính chất P1–P5 của OA-STAL v2 và Mệnh đề 1;
- oracle, vòng tròn và đặc tính id-0 của evaluator;
- dữ liệu và RQ2 offline.

### Phần 1 — Dữ liệu (#8–#10)

**#9 — nhãn.**

```python
if not lab_zip.exists():
    !gdown "1gFaoc5p5whoeDsnsLt6F18O6FHbLGtlK" -O "{lab_zip}" || true
assert lab_zip.exists() and open(lab_zip, "rb").read(2) == b"PK", "...(quota)..."
```

- `b"PK"` là hai byte đầu của mọi file zip. Khi Google Drive hết hạn mức tải công khai, `gdown` tải về một trang HTML; `assert` này bắt đúng trường hợp đó.
- Ngày 20/10 link chính thức báo "Quota exceeded". Cách hợp lệ là một thành viên "Make a copy" vào Drive của nhóm [#8].
- Output liệt kê cả `yolo_woX/` có sẵn từ phiên trước, nên ô này chạy lại được nhiều lần.

**#10 — ảnh.** Chép từng zip sang đĩa VM, giải nén, rồi tạo file đánh dấu `.done` để lần sau bỏ qua. Kết quả: 2 zip OK, **18.730 PNG**.

### Phần 2 — Cổng 0: thống kê nhãn (#11–#12)

```python
g0 = ad.gate0_stats(LABELS, version=VERSION)        # chạy trên toàn bộ nhãn, có cả xView
XVIEW = ad.xview_stems()
EXCLUDE = (XVIEW["trainval"] | XVIEW["test"]) if PROTOCOL == "woX" else set()
```

Số chính, **trên toàn bộ** AI-TOD-R [#12, phần trăm là tính lại]:

| Chỉ số | trainval | test |
|---|---|---|
| Số file nhãn | 14.018 | 14.018 |
| GT gốc / GT giữ lại (bỏ cạnh < 2 px) | 380.991 / 380.174 | 371.469 / 370.413 |
| File nhãn rỗng / file mất hết GT | 17 / 8 | 95 / 3 |
| Ảnh được evaluator chấm | 14.001 | 13.923 |
| File xView / không-xView | 4.639 / 9.379 | 4.667 / 9.351 |
| vehicle | 333.744 (87,8%) | 328.243 (88,6%) |
| very tiny / tiny / small / medium / > 64 px | 23,9% / 68,9% / 6,1% / 1,0% / 19 GT | 20,5% / 71,6% / 6,8% / 1,0% / 32 GT |
| Cạnh ngắn < 8 / < 11,31 / < 16 | 66,5% / 92,7% / 96,8% | 58,0% / 90,6% / 96,7% |
| Tỉ lệ cạnh trung vị / p90 / p99 | 2,0 / 3,01 / 4,98 | 2,0 / 3,05 / 5,0 |
| Số GT lớn nhất trong một ảnh | 1.435 | 2.647 |
| Số (ảnh, lớp) có > 1.500 GT | 0 | 1 |
| Số nhóm cảnh | 8.775 | 8.813 |

Cách đọc:
- **Tổng các bin khớp số GT giữ lại** ở cả hai split [tính lại]. Thống kê vì vậy tự nhất quán.
- **Hai phần ba GT có cạnh ngắn < 8 px.** Ở mức nhãn, câu hỏi về vùng ứng viên là có thật với dataset này.
- **Giới hạn 1.500 dự đoán mỗi (ảnh, lớp) gần như không chạm tới:** chỉ một cặp trong toàn bộ test vượt ngưỡng. Output không cho biết cặp đó có thuộc phần woX không.
- **Danh sách ảnh xView khớp đủ với nhãn:** `n_xview_missing_in_labels = 0`. Bộ lọc woX vì vậy bỏ đúng và đủ ảnh xView.

### Phần 3 — Cổng 2(b)(c): bộ chấm có đáng tin không (#13–#14)

```python
rt = ek.roundtrip_check(LABELS / "test", VERSION)                       # toàn bộ test
infos = ek.load_gt(LABELS / "test", VERSION, exclude_stems=EXCLUDE)     # chỉ test woX
preds = {i["stem"]: (np.array([ek.obb2poly_np(*b) for b in i["bboxes"]]).reshape(-1, 8),
                     i["labels"], np.ones(len(i["labels"]))) for i in infos}
oracle = ek.evaluate(infos, ek.predictions_to_results(preds, infos, VERSION), verbose=True)
```

**Phép thử vòng tròn (c):** đổi đa giác → (x, y, w, h, a) → đa giác, rồi đo IoU với đa giác gốc.

| Chỉ số | Giá trị [#14] |
|---|---|
| Số GT | 370.407 (ít hơn 370.413 GT giữ lại 6 GT; lý do chưa rõ) |
| IoU nhỏ nhất | 0,645 |
| Phân vị 1% | 0,863 |
| Tỉ lệ GT có IoU ≥ 0,999 | 31,4% |

Notebook giải thích: đa giác gốc không phải hình chữ nhật hoàn hảo nên IoU < 1 "một chút". Nhận xét của tôi:
- Với 69% GT dưới 0,999 và 1% GT dưới 0,863, chữ "một chút" chưa tả đúng phần đuôi.
- Nguyên nhân có thể là nhãn vẽ không vuông góc, hoặc toạ độ bị làm tròn trên vật chỉ vài pixel [chưa biết].
- Tiêu chí "IoU = 1" của Cổng 2(c) trong ROADMAP vì vậy **không đạt theo đúng câu chữ**. Cần ghi lại tiêu chí đã sửa.
- Sai lệch này như nhau cho mọi arm, nên không làm lệch phép so giữa các arm. Tuy vậy, nó liên quan trực tiếp tới hướng R1 (độ tin cậy hình học của nhãn).

**Oracle (b):** đưa chính GT vào làm dự đoán, mọi điểm tin cậy = 1, chấm trên 9.261 ảnh test woX.

| | AP | AP50 | AP_vt | AP_t | AP_s | AP_m | AR1500 |
|---|---|---|---|---|---|---|---|
| Oracle [#14] | 0,9963 | 0,9963 | 0,9975 | 0,9963 | 1,0000 | 1,0000 | 0,9984 |

Oracle không đạt đúng 1 vì một đặc tính của AITODReval gốc mà notebook giữ nguyên, không sửa: id của GT và dự đoán bắt đầu từ 0, trong khi cờ "đã khớp" lại dùng chính id. Cặp có id 0 vì thế luôn bị tính là chưa khớp, thành 1 FP và 1 FN. Ảnh hưởng khoảng 1/(số GT của lớp), như nhau cho mọi arm [#13].

Thông tin đi kèm trong file JSON:
- `_official_sha256`: mã băm của file evaluator gốc, dùng để chứng minh dùng đúng bản gốc;
- `_patches`: P1 đổi `np.float` thành `float` cho numpy mới, P2 tính IoU bằng shapely;
- `iou_backend_diff_vs_mmcv: null`: **chưa so shapely với IoU của mmcv**, vì máy không có mmcv. Nên chạy `check_iou_backends()` một lần trong môi trường có mmcv.
- Thời gian: tính IoU 15,8 giây; chấm từng ảnh 470,7 giây. Đường chấm chậm này về sau được thay bằng đường nhanh "P3sparse" (#25, #29).

### Phần 4 — RQ2 offline (#15–#17)

```python
MAX_FILES = 300          # None = toàn bộ
summ = rq.analyze(LABELS / "trainval", OUT, arms=("A0", "A1", "A8", "A2", "A4"),
                  version=VERSION, exclude_stems=EXCLUDE, max_files=MAX_FILES)
```

- Với mỗi GT và mỗi arm, ô này đếm: số ứng viên, có rỗng không, số ứng viên dùng chung với GT khác, số ứng viên nằm ngoài vật, số ứng viên theo từng tầng stride [#15].
- Phép thử điểm-trong-hộp gọi đúng hàm của Ultralytics 8.4.174.
- **Chỉ chạy trên 300 file**, khoảng 3,2% của 9.379 file trainval không-xView [tính lại]. Dòng `[rq2] 0/300 file, 1 GT` là dòng tiến độ in lúc bắt đầu [suy ra].
- Nhãn ô dạng `vt<8|r2-4` nghĩa là nhóm kích thước × nhóm tỉ lệ cạnh. Kích thước đo theo cạnh hay theo √diện tích thì chưa rõ khi không có `rq2_offline.py` [chưa kiểm].

**Tỉ lệ GT không có ứng viên nào** (`zero_cand_rate`) [#16]:

| Ô | A0 | A1 | A2 | A4 | A8 |
|---|---|---|---|---|---|
| vt<8, r<2 | 0,297 | 0 | 0 | 0 | 0 |
| vt<8, r2-4 | 0,262 | 0 | 0 | 0 | 0 |
| vt<8, r≥4 | 0,336 | 0 | 0 | 0 | 0 |
| t8-16, r2-4 | 0,024 | 0 | 0 | 0 | 0 |
| t8-16, r≥4 | 0,118 | 0 | 0 | 0 | 0 |
| mọi ô còn lại | 0 | 0 | 0 | 0 | 0 |

**Tỉ lệ ứng viên dùng chung với GT khác** (`shared_frac`, nguồn của xung đột), các ô tí hon [#16]:

| Ô | A0 | A1 | A2 | A4 | A8 |
|---|---|---|---|---|---|
| vt<8, r<2 | 0,134 | 0,524 | 0,557 | 0,540 | 0,378 |
| vt<8, r2-4 | 0,142 | 0,430 | 0,495 | 0,430 | 0,307 |
| vt<8, r≥4 | 0,154 | 0,532 | 0,576 | 0,431 | 0,444 |
| t8-16, r<2 | 0,145 | 0,191 | 0,300 | 0,278 | 0,183 |
| t8-16, r2-4 | 0,205 | 0,307 | 0,370 | 0,287 | 0,273 |
| t8-16, r≥4 | 0,210 | 0,401 | 0,467 | 0,341 | 0,345 |

Cách đọc:
- Dưới A0, 26–34% vật < 8 px không có ứng viên nào. **Mọi sàn đưa tỉ lệ này về 0.**
- Đổi lại, sàn làm tăng chia sẻ ứng viên. A8 chia sẻ ít hơn A2 rõ rệt; ví dụ ở ô vt<8, r<2 là 0,378 so với 0,557.
- [giả thuyết] Ở bước train (§4), A8 và A2 chưa phân biệt được về AP. Có ba cách giải thích cạnh tranh:
  1. chia sẻ ở mức ứng viên không phải nút thắt;
  2. A2 có thêm ứng viên nên bù lại phần xung đột;
  3. top-k và xử lý xung đột đã làm hai arm giống nhau ở mức mẫu dương.
  
  Muốn phân biệt ba cách này cần log online `c11_assign_diag.jsonl`, chưa được phân tích.
- **Giới hạn (C-19):** đây là tầng ứng viên. Có ứng viên chưa chắc có mẫu dương, và có mẫu dương chưa chắc là giám sát hữu ích [#15].

**#17:** chép lại code, 44 test qua, nạp lại `aitodr_data`. Code được sửa giữa lúc chạy #16 và #19 [suy ra].

### Phần 5 — Dựng dataset YOLO (#18–#19)

```python
man = ad.build_yolo_dataset(LABELS, IMAGES, DS, version=VERSION,
                            exclude_xview=(PROTOCOL == "woX"), val_frac=0.10, seed=0)
```

Quy tắc dựng dataset [#18]:
- lọc đúng như loader gốc: bỏ file nhãn rỗng, bỏ GT có cạnh < 2 px;
- val = 10% trainval, **tách theo nhóm cảnh**;
- ảnh được symlink, không chép.

| Split | Ảnh | GT | Nhóm cảnh | Ảnh/nhóm [tính lại] |
|---|---|---|---|---|
| train | 8.426 | 123.272 | 7.326 | 1,15 |
| val | 936 | 12.003 | 815 | 1,15 |
| test | 9.261 | 128.768 | 8.110 | 1,14 |

Các chi tiết khác:
- Không thiếu ảnh nào. Có 1.345 GT bị bỏ vì cạnh < 2 px.
- 2.188 GT bị cắt về mép ảnh; phần tràn lớn nhất 54 px.
- 8 ảnh train mất hết GT được giữ làm ảnh nền: log train ghi "8 backgrounds" [#19, #21].
- 7 ảnh không có kích thước 800×800, ví dụ 800×787 [#19].
- Log train còn ghi 2 ảnh có nhãn trùng, đã tự bỏ [#23].
- Kiểm chéo: 9.379 − (8.426 + 936) = 17, khớp với 17 file nhãn rỗng ở #12. Điều này giả định 17 file rỗng đều thuộc phần không-xView [tính lại].

**Nhóm cảnh của phần không-xView chưa được xác minh.** Chính markdown #18 ghi: ảnh xView nhóm theo tile gốc, còn "quy ước tên của phần không phải xView chưa xác minh".
- Trên trainval đầy đủ, mỗi nhóm có trung bình 1,60 ảnh. Trên woX chỉ 1,15 ảnh mỗi nhóm.
- Log cho thấy ít nhất hai kiểu tên file: kiểu số (`04755.png`) và kiểu VisDrone có hậu tố vị trí cắt (`9999955_00000_d_0000223__0_0.png`).
- Nếu nhiều ô cắt từ cùng một ảnh gốc không được gộp, thì:
  - val có thể chứa cảnh đã có trong train (ảnh hưởng nhỏ, vì val không dùng để chọn checkpoint);
  - bootstrap ở #34 gần như lấy mẫu theo từng ảnh, nên CI có thể hẹp hơn thực tế.
  
  [chưa kiểm: cần đọc `scene_key`.]

### Phần 6 — Pilot: đo tốc độ (#20–#21)

```python
run = cp.train_arm(DATA_YAML, "A2", seed=0, project=LOCAL / "runs", tag="pilot",
                   diag_every=DIAG_EVERY, recipe_overrides=dict(epochs=1))
pilot = dict(seconds=dt, n_train=n_train, img_per_s=n_train / dt,
             est_gpu_h_per_run=24 * n_train / (n_train / dt) / 3600, ...)
```

**Kết quả [#21]:** 1 epoch mất 168,7 giây, tức 49,9 ảnh/giây, ước 1,12 GPU-giờ cho mỗi run 24 epoch.

**Ước lượng này cao gấp khoảng 2 lần.** Thực tế mỗi run hết 0,55–0,57 giờ, trung bình khoảng 85 giây/epoch kể cả val, tức khoảng 99 ảnh/giây [#23, tính lại]. Lý do: thời gian đo của pilot gồm cả chi phí cố định — quét nhãn (46 + 5 giây), kiểm AMP, tải trọng số, val cuối.

**Recipe** (`cp.RECIPE`, in trong `pilot.json`) [#21]:

| Nhóm | Giá trị |
|---|---|
| Ảnh vào | 800 px, batch 16, 24 epoch |
| Optimizer | SGD, lr0 0,01, momentum 0,937, weight decay 5e-4, warmup 1 epoch, lr tuyến tính, không cosine |
| Augmentation | chỉ lật ngang và dọc (p = 0,5). Tắt mosaic, mixup, copy-paste, scale, translate, xoay, HSV |
| Khác | AMP, `deterministic=True`, `save_period=1` (lưu mỗi epoch để resume), `max_det=300` lúc train |

Chi tiết từ log:
- **Augmentation không hoàn toàn chỉ có lật.** Log in `albumentations: Blur, MedianBlur, ToGray, CLAHE`, mỗi phép p = 0,01. Đây là mặc định của Ultralytics [#23]. Ảnh hưởng nhỏ nhưng nên ghi trong bài.
- **Mô hình:** YOLO26n-obb, 2,65 triệu tham số, 6,4 GFLOPs (sau fuse: 2,45 triệu, 5,6 GFLOPs). Khởi tạo từ `yolo26n.pt` là trọng số **COCO detection**, chuyển được 708/792 tensor; số lớp đổi từ 80 sang 8 [#21, #23]. Cách khởi tạo này đúng proposal §8.1: không dùng trọng số DOTA, để tránh rò rỉ vì AI-TOD lấy một phần ảnh từ DOTA.
- **max_det lúc val trong train:** Ultralytics cảnh báo có ảnh tới 1.027 vật (train) và 355 vật (val), rồi **tự nâng `max_det` lên 1.027** [#21]. Việc này chỉ ảnh hưởng metric val lúc train, không ảnh hưởng phần chấm test (12.000).

### Phần 7 — Train 4 arm × 3 seed (#22–#23)

```python
RUNS = EXP_DRIVE / f"runs-{PROTOCOL}"                     # trên Drive để sống sót khi Colab ngắt
QUEUE = [(a, s) for s in SEEDS for a in ARMS]             # seed ngoài, arm trong
for arm, seed in QUEUE:
    rd = RUNS / cp.run_name(arm, seed)
    if (rd / "c11_done.json").exists():
        continue                                          # run đã xong thì bỏ qua
    cp.train_arm(DATA_YAML, arm, seed, project=RUNS, diag_every=DIAG_EVERY)
```

**Cách hoạt động:**
- Hàng đợi chạy theo thứ tự (A0,1), (A1,1), (A8,1), (A2,1), (A0,2)… Các arm cùng seed chạy sát nhau trên cùng loại GPU.
- Run có `last.pt` mà chưa có `c11_done.json` sẽ được resume.

**Mỗi run ghi ra [#22]:**
- `c11_stal_arm.json`: arm, phiên bản, sha256 của hàm gốc, số lần hàm vá được gọi;
- `c11_assign_diag.jsonl`: theo epoch × nhánh o2m/o2o × ô kích thước/tỉ lệ cạnh — số ứng viên, mẫu dương trước và sau xung đột, tỉ lệ GT không có mẫu dương, mẫu dương "nhận thêm" qua xung đột.

Có callback báo lỗi nếu hàm vá không được gọi trong một epoch. Log không có lỗi nào như vậy, nên vá có hiệu lực ở mọi epoch [suy ra; nội dung `c11_stal_arm.json` chưa được in].

**Kết quả [#23]:** 12/12 run đều xong 24 epoch, mỗi run 0,552–0,570 giờ. Tổng khoảng **6,8 giờ A100** cho phần train [tính lại]. Không run nào bị đổi batch vì thiếu bộ nhớ: #32 không in cảnh báo `batch_changed`.

**mAP50-95 trên val trong lúc train** (metric của Ultralytics, 936 ảnh val) [#23, tính lại]:

| Run | Epoch 24 | Cao nhất (epoch) | TB epoch 21–24 trừ TB epoch 17–20 |
|---|---|---|---|
| A0_s1 / s2 / s3 | 0,283 / 0,288 / 0,269 | 0,287 (22) / 0,289 (20) / 0,272 (23) | +0,010 / +0,008 / +0,016 |
| A1_s1 / s2 / s3 | 0,287 / 0,280 / 0,286 | 0,289 (20) / 0,282 (20) / 0,287 (22) | +0,007 / +0,006 / +0,018 |
| A8_s1 / s2 / s3 | 0,283 / 0,292 / 0,288 | 0,285 (20) / 0,292 (24) / 0,289 (22) | +0,004 / +0,012 / +0,019 |
| A2_s1 / s2 / s3 | 0,292 / 0,284 / 0,294 | 0,295 (20) / 0,284 (20) / 0,294 (19) | +0,007 / +0,008 / +0,008 |

Cách đọc:
- **Không có thứ tự arm nào lặp lại qua cả ba seed:** seed 2 thì A8 cao nhất, A2 thấp thứ hai.
- **Mọi run còn nhích lên ở 4 epoch cuối**, khoảng +0,004 đến +0,019. Recipe 24 epoch chưa bão hoà hẳn, nên kết luận chỉ đúng cho recipe này.
- **Đừng so 0,28 ở đây với AP ≈ 0,13 ở phần test.** Hai con số khác tập ảnh (val 936 so với test 9.261), khác giới hạn số phát hiện, khác cài đặt bộ chấm [suy ra].

### Phần 8 — Predict và chấm bằng AITODReval gốc (#24–#30)

**#25** [66] — chép lại code mới, chạy 5 file test (thêm `test_fastpath.py`): **55 passed** trong 69,93 giây. Nạp lại `aitodr_evalkit`, `c11_bootstrap`, `c11_pipeline`. Evaluator chạy ở chế độ `shapely+P3sparse`, tức thêm bản vá P3 để chấm nhanh.

**#26** [63] — liệt kê file code (§2.2).

**#27** [65] — `diag_bootstrap_device.py`: so engine "weighted" trên GPU với bản tham chiếu numpy trên CPU. Kết quả: **lệch 0/200 mẫu**.

**#28** [61] — chạy test trước khi chép lại code: `FAILED test_bootstrap.py::test_multi_pair_point_equals_official`. Lỗi này thuộc bản code cũ; lần chạy sau ở #25 đã qua hết (§2.3).

**#29** [54] — chấm lại `c11_A0_s1` bằng đường chấm mới:

```python
new = cp.predict_and_eval(ref_dir / "weights" / "last.pt", LABELS / "test", DS / "images" / "test",
                          ref_dir / "eval_e2e_recheck.json", head="e2e", ...)
diff = {k: abs(old[k] - new[k]) for k in ek.STAT_NAMES}
```

Kết quả: mất 337 giây, chênh lệch lớn nhất **9,4e-7**. Đường chấm nhanh cho cùng số với đường cũ. Nhưng ô này **sinh thêm file `eval_e2e_recheck.json`** trong thư mục A0_s1, và file này gây lỗi đếm trùng ở #32.

**#30** [56] — vòng predict + chấm, hiện chỉ cho head `e2e`:

```python
for rd in sorted(RUNS.glob("c11_*_s*")):
    for head in ("e2e",):
        out = rd / f"eval_{head}.json"
        if out.exists(): continue
        st = cp.predict_and_eval(rd / "weights" / "last.pt", LABELS / "test", TEST_IMAGES, out,
                                 head=head, version=VERSION, exclude_stems=EXCLUDE,
                                 save_dota_dir=rd / f"dota_{head}")
```

- Chấm `last.pt`, không chọn `best.pt`. Lựa chọn này đã khai trước trong `c11_pipeline.py` [#24].
- Dự đoán lưu thêm ở dạng DOTA Task1 trong `dota_e2e/` để phát hành.
- Output in 7 run (bảng ở §4.2). 5 run còn lại đã chấm ở lần chạy trước.

### Phần 9 — Gộp kết quả (#31–#32)

```python
for f in RUNS.glob("c11_*_s*/eval_*.json"):      # ← khớp cả eval_e2e_recheck.json
    d = json.loads(f.read_text())
    done = json.loads((f.parent / "c11_done.json").read_text())
    recs.append(dict(arm=done["arm"], seed=done["seed"], head=d["head"], ...))
agg = res.groupby(["head", "arm"])[[...]].agg(["mean", "std", "count"])
```

- Ô này lấy arm và seed từ `c11_done.json`, không đoán từ tên thư mục. Đây là cách làm tốt.
- Ô cũng kiểm `batch_changed`, tức Ultralytics có tự đổi batch vì thiếu bộ nhớ không. Không có cảnh báo nào được in.
- **Lỗi đếm trùng:** mẫu `eval_*.json` khớp cả `eval_e2e_recheck.json` do #29 tạo. Vì thế dòng `e2e A0` có `count = 4` trong khi chỉ có 3 seed.
- Bằng chứng: lấy Δ của bootstrap suy ngược trung bình 3 seed của A0. Cả ba cặp đều cho cùng một số AP = 0,1297, khác với 0,1301 trong bảng [tính lại; chi tiết ở Phụ lục B].
- Lỗi này chỉ làm sai dòng A0 của **bảng mô tả**. Bootstrap đọc file cache nên không bị ảnh hưởng. Cách sửa ở Phụ lục A.
- Head `nms` mới có A0 × 3 run và A1 × 1 run.

### Phần 9.1 — Bootstrap ghép cặp theo cụm cảnh (#33–#34)

```python
HEAD, B, KEYS = "e2e", 1000, ("AP_vt", "AP_t", "AP")
PAIRS = [("A8", "A0"), ("A2", "A0"), ("A2", "A8"), ("A1", "A0")]
boot = cb.multi_pair_bootstrap(by_arm, pairs, scene_key, keys=KEYS, B=B, engine="weighted")
```

**Cách làm [#33]:**
- Mỗi run có `evalcache_e2e.npz`, lưu kết quả khớp của từng (ảnh, lớp, bin) do AITODReval gốc tính.
- Mỗi lần bootstrap lấy mẫu lại theo **cụm cảnh**, dùng **cùng một mẫu cho mọi run**, rồi tính lại AP từ cache.
- Δ = trung bình theo seed của arm X trừ trung bình theo seed của arm Y. Notebook ghi phần tính lại từ cache đã khớp số chính thức tới 1e-12.
- Engine "weighted" chạy trên GPU (đã kiểm ở #27). Hết 570 giây cho B = 1.000. Số `3548` ở cuối output là số ký tự ghi ra file JSON [suy ra].

**Kết quả [#34]** (Δ, khoảng tin cậy 95%; ✓ = CI không chứa 0):

| Cặp | ΔAP_vt | ΔAP_t | ΔAP |
|---|---|---|---|
| A8 − A0 | +0,0071 [−0,0002; 0,0114] | +0,0042 [0,0005; 0,0072] ✓ | +0,0025 [0,0006; 0,0045] ✓ |
| A2 − A0 | +0,0090 [0,0051; 0,0153] ✓ | +0,0062 [0,0043; 0,0084] ✓ | +0,0035 [0,0018; 0,0057] ✓ |
| A2 − A8 | +0,0019 [−0,0030; 0,0124] | +0,0020 [−0,0010; 0,0057] | +0,0011 [−0,0010; 0,0030] |
| A1 − A0 | +0,0074 [0,0033; 0,0161] ✓ | +0,0016 [−0,0005; 0,0032] | +0,0006 [−0,0010; 0,0024] |

**Đã kiểm:** Δ điểm khớp với hiệu trung bình chính thức theo seed. Ví dụ A2 − A8 về AP: 0,13323 − 0,13217 = 0,0011, đúng bằng Δ bootstrap [tính lại].

**CI này phản ánh gì và không phản ánh gì:**
- CI chỉ phản ánh **bất định do chọn ảnh test**, với điều kiện cố định đúng 3 mô hình đã train. CI **không** gồm bất định do seed. Audit C-19 §5 yêu cầu báo riêng hai loại bất định này. §4.2 cho thấy ở AP tổng, độ lệch giữa các seed lớn hơn hiệu ứng.
- Có 12 khoảng tin cậy (4 cặp × 3 chỉ số) mà không hiệu chỉnh cho nhiều phép so.
- B = 1.000, trong khi proposal §8.6 ghi 10.000.
- **Chưa có MEI và preregistration.** Theo chính quy tắc ở #33, chưa được gọi bất kỳ chênh lệch nào là "khác biệt".

---

## 4. Tổng hợp kết quả

### 4.1 Bảng theo arm (head e2e, mean ± sd của 3 seed)

| Arm | AP | AP50 | AP_vt | AP_t | AP_s | AR1500 |
|---|---|---|---|---|---|---|
| A0, bảng #32 (4 dòng, có dòng trùng) | 0,1301 ± 0,0016 | 0,3882 ± 0,0035 | 0,0410 ± 0,0006 | 0,1173 ± 0,0021 | 0,2092 ± 0,0056 | 0,2769 ± 0,0018 |
| A0, 3 seed, suy từ Δ bootstrap [tính lại] | ≈ 0,1297 | — | ≈ 0,0409 | ≈ 0,1174 | — | — |
| A1 | 0,1303 ± 0,0024 | 0,3925 ± 0,0103 | 0,0484 ± 0,0038 | 0,1190 ± 0,0035 | 0,2014 ± 0,0014 | 0,2774 ± 0,0061 |
| A8 | 0,1322 ± 0,0032 | 0,3991 ± 0,0105 | 0,0480 ± 0,0033 | 0,1216 ± 0,0020 | 0,2051 ± 0,0063 | 0,2787 ± 0,0045 |
| A2 | 0,1332 ± 0,0047 | 0,4023 ± 0,0094 | 0,0499 ± 0,0062 | 0,1237 ± 0,0042 | 0,2035 ± 0,0084 | 0,2818 ± 0,0050 |

Head nms [#32]: A0 (3 run) AP 0,1356 ± 0,0031, AP_vt 0,0412 ± 0,0026, AR1500 0,2378 ± 0,0033. A1 mới có 1 run: AP 0,1350.

### 4.2 Nhìn ở mức từng seed

AP trên test, head e2e, từng run. Số in thẳng ở #30; số A0 và A1 có dấu ≈ là suy ra từ mean/sd (Phụ lục B):

| Run | AP | AP_vt | AP_t |
|---|---|---|---|
| A0 s1 (run bị đếm trùng, nên tách ra được) | ≈ 0,131 | ≈ 0,041 | ≈ 0,117 |
| A0, hai seed còn lại (không rõ seed nào) | ≈ 0,130 và ≈ 0,128 | cả hai ≤ 0,042 (cận trên) | ≈ 0,120 và ≈ 0,115 |
| A1 s1, s2 (không ghép được số theo seed) | ≈ 0,133 và ≈ 0,129 | ≈ 0,051 và ≈ 0,044 | ≈ 0,123 và ≈ 0,116 |
| A1 s3 | 0,1293 | 0,0504 | 0,1183 |
| A2 s1, s2, s3 | 0,1321 / 0,1384 / 0,1292 | 0,0456 / 0,0570 / 0,0472 | 0,1242 / 0,1275 / 0,1192 |
| A8 s1, s2, s3 | 0,1304 / 0,1302 / 0,1359 | 0,0453 / 0,0470 / 0,0517 | 0,1198 / 0,1213 / 0,1238 |

Cách đọc:
- **AP_vt — hiệu ứng vượt qua nhiễu seed.** Run thấp nhất có sàn (≈ 0,044, một run A1) vẫn cao hơn cận trên của mọi run A0 (≤ 0,042).
  - Nếu arm không có tác dụng gì, xác suất để 3 run A0 rơi đúng vào 3 vị trí thấp nhất trong 12 run là 1/C(12,3) = 1/220 ≈ 0,5% [tính lại].
  - Phép thử này được đặt ra **sau khi** thấy số, nên chỉ dùng để mô tả.
- **AP tổng — hiệu ứng nằm trong nhiễu seed.** Riêng A2, seed tốt nhất và kém nhất chênh 0,0092, gần gấp 3 lần ΔAP(A2 − A0) = 0,0035. Các run A0 (≈ 0,128–0,131) nằm lẫn giữa các run có sàn.
- **AP_t:** các run chồng lấn nhau, chưa tách bạch được.
- **A2 với A8 từng seed:** về AP, A2 hơn ở seed 1 và 2 nhưng thua ở seed 3. Về AP_vt cũng không có chiều cố định.

### 4.3 Mẫu hình theo kích thước

| Arm | GT bị đổi vùng ứng viên (cạnh ngắn < ngưỡng) | ΔAP_vt so với A0 | ΔAP_t so với A0 |
|---|---|---|---|
| A1 (cạnh < 8 → 16) | 66,5% | +0,0074 ✓ | +0,0016 (CI chứa 0) |
| A8 (cạnh < 11,31 → 11,31) | 92,7% | +0,0071 (CI chạm 0) | +0,0042 ✓ |
| A2 (cạnh < 16 → 16) | 96,8% | +0,0090 ✓ | +0,0062 ✓ |

[suy luận] AP_t chỉ tăng rõ khi sàn chạm tới vật có cạnh 8–16 px (A8, A2). A1 chỉ sửa cạnh < 8 nên chủ yếu tác động AP_vt. Mẫu hình này hợp với cơ chế "sàn giúp đúng nhóm kích thước mà nó chạm tới". Tuy vậy:
1. mẫu hình này được nhận ra sau khi thấy số;
2. bin AP tính theo diện tích, còn ngưỡng sàn tính theo cạnh, nên hai thứ không khớp một-một.

Cần kiểm bằng hồi quy recall của từng GT theo cạnh ngắn (H2c của proposal).

### 4.4 Hai tín hiệu phụ cần theo dõi

- **AP_s (16–32 px) có thể đi ngược chiều.** Mọi arm có sàn thấp hơn dòng A0 khoảng 0,4–0,8 điểm (A1 −0,0078, A2 −0,0057, A8 −0,0041 so với 0,2092) [tính lại].
  - Dòng A0 có lỗi đếm trùng, và AP_s chưa được đưa vào bootstrap. Vì vậy **chưa biết** đây là nhiễu hay một đánh đổi thật (sàn làm vật tí hon chiếm ứng viên của vật nhỏ bên cạnh).
  - Nên thêm `AP_s` và `AP_m` vào `KEYS`.
- **AP50 tăng mạnh hơn AP:** A2 +0,0141 và A8 +0,0109, so với dòng A0 của bảng (dòng có bản trùng; sd của AP50 ở A0 là 0,0035 nên độ lệch do trùng nhỏ) [tính lại]. [suy luận] Sàn giúp **tìm thấy** vật nhiều hơn là giúp định vị chính xác hơn.

### 4.5 Head e2e so với nms

- Với A0, head nms cho AP cao hơn e2e khoảng +0,006, lớn hơn mọi hiệu ứng arm trên AP. Đổi lại AR1500 thấp hơn khoảng 0,039 [tính lại].
- Kết luận theo arm có thể khác giữa hai head. Đây là lý do proposal yêu cầu báo riêng hai head; hiện mới đủ dữ liệu cho e2e.

### 4.6 Chi phí tính toán thực tế

| Việc | Thời gian |
|---|---|
| Train 12 run | khoảng 6,8 giờ A100 |
| Chấm một run, một head (đường nhanh) | khoảng 337 giây |
| Bootstrap B = 1.000, 4 cặp | 570 giây |

**Thêm seed, thêm head hay thêm arm đều rẻ:** mỗi run thêm khoảng 0,56 giờ cộng 6 phút chấm [tính lại].

---

## 5. Kết quả hiện tại cho phép nói gì

Mọi câu dưới đây chỉ đúng cho: **YOLO26n-OBB, recipe 24 epoch, giao thức woX, head e2e, chưa preregistration**. Vì vậy đây là kết quả thăm dò.

| Có thể nói (thăm dò) | Chưa được nói |
|---|---|
| Mọi sàn ứng viên thử ở đây làm AP_vt tăng khoảng 17–22% tương đối, nhất quán ở cả 3 seed | "A2/A8 cải thiện AP": hiệu ứng AP tổng nằm trong dao động seed, và chưa có MEI |
| Trong mẫu 300 file nhãn, mọi sàn đưa tỉ lệ GT < 8 px không có ứng viên từ 26–34% về 0, đổi lại tỉ lệ chia sẻ ứng viên tăng | "A8 tương đương A2", hay "√2·s là sàn tối ưu" |
| Hạ tầng đo (oracle, chấm lại, kiểm engine bootstrap) cho số ổn định tới 1e-6 | Bất cứ câu nào về **nguyên nhân**: cần log online và hồi quy recall |
| | So với Bảng II hay số của bài khác |
| | Bất cứ câu nào về YOLO26s, YOLO11, dataset khác, recipe dài hay head nms |

---

## 6. Các vấn đề, xếp theo mức nghiêm trọng

1. **Chưa có preregistration và MEI.**
   - Bằng chứng: repo không có `experiments/preregistration.md`; markdown #0, #22, #33 tự yêu cầu file này.
   - Hệ quả: 12 run hiện có chỉ là thăm dò, và test set đã bị xem.
   - Cách sửa: viết và commit preregistration **trước** mọi run hay phép chấm mới. Khai 12 run hiện có là thăm dò. Chốt so sánh xác nhận, dấu dự báo, MEI, head chính, cách báo biến thiên seed.
2. **CI bootstrap chỉ phản ánh bất định của ảnh test** (§3, Phần 9.1).
   - Cách sửa: báo riêng chênh lệch theo seed (bảng từng seed, khoảng min–max) bên cạnh CI theo cảnh. Với AP tổng, cần thêm seed trước khi nói về hướng tác động.
3. **RQ2 — trung tâm của bài — gần như chưa làm.**
   - Mới có thống kê offline trên 300 file.
   - Log `c11_assign_diag.jsonl` của 12 run chưa được đọc.
   - Chưa có hồi quy recall theo từng GT (H2c).
   - Thiếu phần này, bài chỉ còn là "STAL giúp vật tí hon một chút", mà đó là điều STAL được thiết kế để làm.
4. **Bảng gộp đếm trùng A0_s1** (Phần 9). Sửa theo Phụ lục A.
5. **Head nms thiếu 8/12 run; A4 chưa train.** Chấm nms mất khoảng 45 phút; A4 × 3 seed mất khoảng 1,7 giờ [ước lượng từ thời gian chấm e2e ở #29 và thời gian train ở #23]. A4 phải được khai trước trong preregistration.
6. **Nhóm cảnh của phần woX chưa xác minh** (Phần 5). Nếu sai, CI có thể quá hẹp.
7. **Recipe ngắn:** val vẫn còn nhích ở 4 epoch cuối, và có albumentations mặc định. Claim phải ghi rõ "recipe 24 epoch". Nếu còn thời gian, chạy một cặp với recipe dài hơn để xem hiệu ứng còn giữ không.
8. **Hai lựa chọn của bộ chấm chưa được đối chiếu:**
   - `VERSION = "oc"` so với `le135` của config gốc [chưa kiểm];
   - IoU tính bằng shapely so với mmcv (`null` ở #14).
   
   Mỗi việc chỉ cần chạy một lần.
9. **Tiêu chí vòng tròn của Cổng 2(c):** chỉ 31% GT đạt IoU ≥ 0,999. Cần ghi lại tiêu chí đã sửa và lý do.
10. **DIA-YOLO dùng đúng 18.730 ảnh** (§1.7). Cần kiểm split của DIA-YOLO và định vị RQ1 với nó.
11. **Code và kết quả chưa lên repo:**
    - `scripts/c11` và các JSON chỉ có trên Drive;
    - `notes/08-c11-execution/` mà #0 nhắc tới chưa có gì trước file này;
    - README và AGENTS vẫn ghi "chưa chạy thí nghiệm nào";
    - ROADMAP chưa tick ô nào.

---

## 7. Việc nên làm tiếp (đến Cổng 5, 08/11)

Trạng thái các cổng trong ROADMAP:

| Cổng | Hạn | Trạng thái 26/10 |
|---|---|---|
| 0 — thống kê nhãn | 13/10 | Xong ngày 20/10 [#12] |
| 1 — có ảnh | 18/10 | Xong theo nhánh dự phòng woX, trên Colab thay vì Kaggle [#10] |
| 2(a) pilot | 21/10 | Xong, trên A100 thay vì P100/T4 [#21] |
| 2(b) oracle | 21/10 | Xong, 0,996 [#14] |
| 2(c) vòng tròn IoU = 1 | 21/10 | Không đạt theo câu chữ (31% ≥ 0,999); cần sửa tiêu chí |
| 2(d) preregistration | 21/10 | **Chưa** |
| 3(a) RetinaNet-O | 25/10 | Chưa; với woX chỉ được claim nội bộ, nên có thể bỏ |
| 3(b) dataset thứ hai | 25/10 | Chưa |
| 3(c) đợt 1 xong ≥ 80% | 25/10 | 12/15 run = 80% (thiếu A4) |
| 4 — đủ seed cặp chính; sai số góc theo kích thước | 01/11 | Chưa |

Thứ tự đề xuất:

1. **Viết preregistration ngay** (mục 1 của §6). Mọi việc dưới đây phải làm sau bước này.
2. Sửa ô #32 theo Phụ lục A, chạy lại bảng.
3. Chấm head nms cho 8 run còn lại (khoảng 45 phút).
4. **RQ2:**
   - chạy offline trên toàn bộ trainval (`MAX_FILES = None`);
   - đọc `c11_assign_diag.jsonl`: tỉ lệ GT không có mẫu dương theo arm × bin × nhánh;
   - hồi quy logistic recall từng GT trên val theo số mẫu dương, cạnh ngắn, mật độ.
   
   Câu hỏi cần trả lời: GT bị mất ở bước nào, và vì sao A8 chia sẻ ít ứng viên hơn mà AP không khác A2.
5. Seed 4–5 cho cặp xác nhận đã khai: 4 run, khoảng 2,3 giờ cộng thời gian chấm.
6. Bootstrap:
   - thêm `AP_s`, `AP_m`;
   - B = 10.000 cho so sánh chính, khoảng 95 phút nếu thời gian tăng tuyến tính [ước lượng];
   - báo riêng CI theo cảnh và chênh lệch theo seed.
7. Đối chiếu `oc` với `le135`, shapely với mmcv; kiểm `scene_key` của phần không-xView.
8. Đo sai số góc theo kích thước trên các run A2 (Cổng 4b, đầu vào quyết định hướng C-7′ / R1).
9. Đưa `scripts/c11` và JSON kết quả lên repo qua PR; cập nhật README, ROADMAP, INDEX; tạo `notes/08-c11-execution/`.
10. Nếu còn thời gian: A4 × 3 seed (đã khai trước); một cặp chạy recipe dài hơn.

---

## 8. Đánh giá venue: đã đủ band Q4 chưa

**Trả lời ngắn: chưa.** Có ba lớp lý do.

### 8.1 Theo quy tắc hiện hành của dự án

- Ledger C-19 (15/10) ghi "No venue band assigned" và rút cách quy đổi tier sang quartile.
- AGENTS.md §6.6–6.7: band chỉ được ghi qua một dòng REVISION trong ledger, kèm loại bằng chứng.
- Kết quả C11 là loại bằng chứng "kết quả chạy", đủ để mở lại câu hỏi. Nhưng chưa ai ghi dòng ledger, và các lớp 8.2, 8.3 dưới đây cho thấy **chưa nên ghi**.

### 8.2 Theo chính điều kiện Q4 nhóm đã đặt

Thẻ venue C-10 (proposal §13) và các cổng C-11 nay là lịch sử, nhưng đó là thước đo nhóm từng cam kết.

| Điều kiện | Trạng thái 26/10 |
|---|---|
| 1. RQ1 viết hẹp, trích DIA-YOLO | Chưa có bản thảo. Vấn đề mới: woX trùng 18.730 ảnh với DIA-YOLO (§1.7) |
| 2. AITODReval maxDets 1.500, converter đã kiểm | Phần lớn đạt (oracle, max_det 12.000); chưa đối chiếu mmcv và `le135` |
| 3. Pin fork, tham số tường minh | Đạt trong notebook; code chưa công khai |
| 4. Val riêng, ≥ 3 seed, CI | Đạt về hình thức; CI chỉ theo cảnh, nhóm cảnh woX chưa xác minh |
| 5. Có dữ liệu, đã chạy pilot | Đạt theo nhánh woX |
| 6. Đọc toàn văn MFN-Net, ARA, CDCEDet; trích OSCAR, MCSA | Theo C-16, MFN-Net và ARA mới đọc abstract, CDCEDet không truy cập được; chưa thấy bằng chứng đọc thêm |
| Preregistration có ngày (Cổng 2d) | Chưa |

### 8.3 Theo nội dung khoa học [nhận định, không phải quy định của venue nào]

**Điều kết quả hiện có cho thấy:** sàn ứng viên tăng AP_vt, nhất quán qua seed; AP tổng không tách khỏi nhiễu seed; các mức sàn chưa phân biệt được.

**Đây là điều STAL được thiết kế để làm.**
- Bài YOLO26 đã báo AP_S trên COCO tăng từ 29,0 lên 29,6 với STAL-16 [nguồn: proposal §2.2; số do tác giả báo, một run].
- OSCAR đã cho thấy kích thước sàn ảnh hưởng tới kết quả [nguồn: ledger C-16].
- Phần mới còn lại vì vậy là: đo trên vật xoay tí hon bằng evaluator chính thức, cộng với **chẩn đoán cơ chế (RQ2)** — mà RQ2 chưa làm.

**Đối chiếu với đánh giá 09/10 của chính nhóm** [nguồn: `t07-session-qa-2026-10-09.md` H1; viết trước C-19]:
- "AP tăng nhưng không đúng mẫu hình dự đoán" → claim yếu;
- "không có phát hiện cơ chế" → "khó đạt mức hội nghị Scopus".

Trạng thái hiện tại gần ô thứ hai nhất, vì RQ2 chưa có kết quả.

**Câu reviewer gần như chắc chắn sẽ hỏi:**
- +0,35 điểm AP có ý nghĩa thực tế không?
- Vì sao chỉ YOLO26n, chỉ 24 epoch, chỉ một phần dataset?
- Khác gì STAL gốc và OSCAR?
- Khác gì DIA-YOLO trên cùng 18.730 ảnh?
- Vì sao không so với các cách gán mẫu cho vật tí hon khác?

### 8.4 Khi nào có thể coi là ứng viên hợp lý

Đây là định hướng, không phải bảo đảm. Hội nghị Scopus hoặc tạp chí Q4 có thể là ứng viên hợp lý nếu đủ các điều sau:
1. RQ2 cho một phát hiện cơ chế đo được: GT mất ở bước nào; số mẫu dương có dự báo recall không; vì sao A8 ít xung đột hơn mà không hơn A2.
2. Kết quả xác nhận theo preregistration (seed mới), báo riêng CI theo cảnh và chênh lệch theo seed.
3. Đủ hai head; có AP_s để kiểm khả năng đánh đổi.
4. Định vị đúng với STAL/YOLO26, OSCAR, MCSA, DIA-YOLO; không dùng chữ "first".
5. Công khai gói tái lập: code, config, seed, file dự đoán.

Về thời gian và chi phí:
- Phần còn thiếu chủ yếu là **phân tích và kỷ luật xác nhận**, không phải hạ tầng. Tính toán thêm chỉ khoảng vài giờ A100.
- **Rủi ro lớn nhất** là RQ2 không cho phát hiện cơ chế rõ. Khi đó bài chỉ còn là một bảng ablation nhỏ.
- Quartile là thuộc tính của tạp chí, thay đổi theo năm và lĩnh vực. Phải kiểm trên SJR ở thời điểm nộp và tránh venue săn mồi [nguồn: QA H1].
- ROADMAP ghi hạn nộp ứng viên vào tháng 1/2027 (IJCNN 2027 ngày 31/01/2027; IGARSS 2027 khoảng 11/01/2027, chưa xác minh). Sau Cổng 5 (08/11) vẫn còn thời gian cho phần xác nhận. Tôi chưa kiểm lại các hạn này.

Nếu nhóm muốn ghi đánh giá này vào ledger: thêm dòng REVISION của C-19, loại bằng chứng "kết quả chạy (thăm dò, chưa preregistration)", và giữ "chưa gán band" cho tới khi đủ §8.4. Đây là đề xuất; file này không sửa ledger.

---

## 9. Thuật ngữ

| English | Tiếng Việt | Giải thích ngắn |
|---|---|---|
| anchor point | điểm neo | tâm ô lưới trên feature map, bước 8/16/32 px |
| candidate | ứng viên | điểm neo nằm trong vùng ứng viên của một GT |
| positive | mẫu dương | ứng viên được chọn sau top-k và xử lý xung đột |
| label assignment | gán mẫu | quy tắc quyết định điểm neo nào học GT nào |
| TAL / STAL | — | bộ gán mẫu gốc / bản có sàn cho vật nhỏ |
| floor | sàn | cạnh tối thiểu của vùng ứng viên |
| o2o / o2m | một-một / một-nhiều | hai nhánh của YOLO26; o2o không cần NMS |
| oracle test | kiểm thử oracle | đưa GT vào làm dự đoán để kiểm bộ chấm |
| round-trip | vòng tròn | đổi đa giác → hộp → đa giác rồi đo IoU |
| scene-clustered bootstrap | bootstrap theo cụm cảnh | lấy mẫu lại theo cảnh, không theo từng ảnh |
| MEI (minimal effect of interest) | hiệu ứng tối thiểu đáng quan tâm | ngưỡng phải khoá trước để gọi là "khác biệt" |
| preregistration | đăng ký trước | file có ngày, khoá dự báo trước khi chạy |
| exploratory / confirmatory | thăm dò / xác nhận | kết quả xem trước khi khoá dự báo / sau khi khoá |

---

## Phụ lục A. Sửa ô gộp kết quả (#32)

Thay vòng `glob("eval_*.json")` bằng tên file cụ thể, và chặn đếm trùng:

```python
recs = []
for rd in sorted(RUNS.glob("c11_*_s*")):
    done_f = rd / "c11_done.json"
    if not done_f.exists():
        continue
    done = json.loads(done_f.read_text())
    for head in ("e2e", "nms"):
        f = rd / f"eval_{head}.json"          # đúng tên, không lấy *_recheck.json
        if not f.exists():
            continue
        d = json.loads(f.read_text())
        recs.append(dict(arm=done["arm"], seed=done["seed"], head=head,
                         batch=done.get("batch_actual"), batch_changed=done.get("batch_changed"),
                         **{k: d[k] for k in ek.STAT_NAMES}))
res = pd.DataFrame(recs)
assert not res.duplicated(["arm", "seed", "head"]).any(), "có run bị đếm hai lần"

# Báo biến thiên theo seed bên cạnh CI theo cảnh
per_seed = res[res["head"] == "e2e"].pivot_table(index="seed", columns="arm", values=["AP", "AP_vt", "AP_t"])
display(per_seed.round(4))
```

Trong #34, nên thêm `"AP_s"` và `"AP_m"` vào `KEYS`.

## Phụ lục B. Cách tính lại các số

1. **Trung bình 3 seed thật của A0.** Bootstrap báo Δ = trung bình(X) − trung bình(A0), và trung bình của A1, A2, A8 trong bảng #32 không bị trùng. Suy ra trung bình(A0) = trung bình(X) − Δ(X − A0):

   | Chỉ số | Suy từ A1 | Suy từ A2 | Suy từ A8 |
   |---|---|---|---|
   | AP | 0,1297 | 0,1297 | 0,1297 |
   | AP_vt | 0,0410 | 0,0409 | 0,0409 |
   | AP_t | 0,1174 | 0,1175 | 0,1174 |

   Ba cách suy cho cùng một số. Điều này xác nhận Δ của bootstrap khớp số chính thức, và dòng A0 trong bảng (0,1301) bị kéo lên bởi bản trùng của s1.

2. **Cận trên của từng run A0.** Với n giá trị có độ lệch chuẩn mẫu s, mọi giá trị cách trung bình không quá s·(n − 1)/√n. Dòng A0 có n = 4 (kể cả bản trùng), AP_vt 0,0410 ± 0,0006, nên mọi run A0 có AP_vt ≤ 0,0410 + 0,0009 ≈ 0,042. Tính cả sai số làm tròn vẫn ≤ 0,0420.

3. **Hai run A1 không in ra.** Biết s3 (in ở #30), trung bình m và sd của A1:
   - s1 + s2 = 3m − s3;
   - (s1 − m)² + (s2 − m)² = 2·sd² − (s3 − m)².
   
   Giải hệ này cho AP_vt ≈ 0,0508 và 0,0440. Sai số làm tròn khoảng ±0,0002.

4. **Số trong bảng 4.2 có dấu ≈** đều suy theo cách 1–3 từ số làm tròn 4 chữ số. Chúng chỉ dùng để thấy khoảng giá trị, không dùng làm số báo cáo. Số báo cáo phải đọc từ các file `eval_*.json`.
