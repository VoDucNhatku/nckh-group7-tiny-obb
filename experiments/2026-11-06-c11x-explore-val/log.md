# 2026-11-06 · C11x: 12 run thăm dò trên val, không train

- **Nơi chạy:** Colab, NVIDIA A100-SXM4-80GB, acc Colab của một thành viên ngoài acc giữ Drive. Notebook `notebooks/C11x_explore_val_colab.ipynb`, code commit `ea8b725` (`admin/journal-diagnostic`), `ultralytics==8.4.174`, torch 2.11.0+cu130, Python 3.13.16.
- **Không mount Drive.** Mount bằng acc Colab không xác thực được, nên dữ liệu được tải bằng `gdown` từ link chia sẻ của thư mục `NCKH`: `scripts/c11` (bỏ cache, bản sao `c11/` lồng bên trong và `NCKH.zip`), `labels.zip`, hai zip ảnh woX, `split_manifest.json`, `weights/last.pt` của 12 run. Ô cấu hình đặt `DRIVE = /content/NCKH`. Ô tải không được commit; nó chỉ chép file, không đổi phép tính.
- **Tập dùng:** val (936 ảnh, 12.003 GT). Không chạm tập test, không xem dự đoán test.
- **Kết quả:** `decision.json` ở thư mục này, chép nguyên văn từ ô cuối do người chạy gửi lại. Các bảng CSV và `mech_*.json` nằm trong thư mục `c11x-explore-val` mà người chạy tải về; chưa đưa vào repo.
- **`old_dota_ok = false`:** do cách tải trên không lấy `dota_e2e`, không phải do dữ liệu thiếu. Trên Drive, `runs-woX/c11_A0_s1/dota_e2e/` có 8 file Task1 (liệt kê bằng `gdown`, 06/11). `scripts/c11/c11_pipeline.py` bản trên Drive ghi dự đoán từ `EVAL = dict(max_det=12000, conf=0.001, imgsz=800)` (dòng 36, 113–118). Chưa kiểm bản code này có đúng là bản đã chạy ngày 20–21/10, và chưa kiểm 8 run còn lại.
- **Trạng thái:** thăm dò. Ngưỡng C1–C3 là [design], dùng để quyết định có train hay không, không phải kết luận.
