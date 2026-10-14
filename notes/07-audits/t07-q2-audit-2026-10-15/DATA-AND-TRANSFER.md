# #7 — Audit dữ liệu, đối chiếu nhãn và chuyển cơ chế (15/10/2026)

**Phạm vi:** audit nghiên cứu có giới hạn; không tải dataset, không chạy train, không sửa các note cũ. Đọc bốn bài chính ở các phần dữ liệu/method/experiment được chỉ rõ dưới đây; tái sử dụng một đoạn toàn văn NWD đã có. Đọc trước `t07-q2-path-2026-10-14.md`, `t07-direction-map-2026-10-15.md`, `t07-c3-evidence-dossier.md` và các dòng đăng ký liên quan trong `INDEX.md`. Không cần dùng scratchpad Temp. Không đánh giá hướng theo chi phí, không suy tier thành quartile.

Nhãn **V** = nguồn nói rõ, đã kiểm ở locator; **I** = suy luận của audit; **U** = chưa xác minh; **D** = thiết kế phép thử, chưa có kết quả. V xác minh phát biểu của nguồn, không chứng nhận dữ liệu ngoài thực địa hay tự tái lập điểm số tác giả.

## 1. Nguồn và độ sâu đọc

| ID | Nguồn gốc và URL | Độ sâu thực tế / locator |
|---|---|---|
| DT01 | [AI-TOD-R, arXiv 2412.11582v1](https://arxiv.org/html/2412.11582v1) | Đọc §III-A/B và Table I; HTML dòng 108–142; đối chiếu bản `papers/_text/Xu2024-AI-TOD-R.txt`, PDF pp.3–5. Không đọc mới toàn bộ method DCFL. |
| DT02 | [AI-TOD-R project](https://chasel-tsui.github.io/AI-TOD-R/) và [repo tác giả](https://github.com/Chasel-Tsui/AI-TOD-R) | Project mục Dataset/Method; repo README Introduction/Installation. Không tải nhãn, không kiểm manifest/hash hay instance IDs. |
| DT03 | [AI-TOD-v2 / NWD project](https://chasel-tsui.github.io/AI-TOD-v2/) — **tái sử dụng toàn văn local** | `scripts/t07-slr/data/txt_cache/R2318.txt`, dòng 510–541 (§3/§3.1); số instance tham khảo dossier §1.1. URL project là URL in trong bài; không kiểm mới nội dung project. |
| DT04 | [CODrone, arXiv 2504.20032v1](https://arxiv.org/html/2504.20032v1) | Đọc §III-A–D, Tables I–III, Fig.5–6; HTML 126–191. Phạm vi đủ kiểm acquisition, labeling và các mâu thuẫn metadata; không đọc hết benchmark 22 methods. |
| DT05 | [CODrone repo tác giả](https://github.com/AHideoKuzeA/CODrone-A-Comprehensive-Oriented-Object-Detection-benchmark-for-UAV) | README Download/tree/Characteristics/splitting; có link Google Drive. Không xác minh archive tải được hay schema bên trong. |
| DT06 | [DroneVehicle, arXiv 2003.02437v2](https://arxiv.org/html/2003.02437v2) | Đọc §III-A–D; HTML 151–182; Table II. Độ sâu đã vượt abstract ở note cũ. |
| DT07 | [DroneVehicle repo chính thức](https://github.com/VisDrone/DroneVehicle) | README Dataset/download/Code; HTML 203–221. Không mở archive Baidu. |
| DT08 | [CSCWD, arXiv 2609.30395v1](https://arxiv.org/html/2609.30395v1) | Đọc §3.1–3.4, §4.1–4.4, Tables2/4/5/6 và §5.1/5.3/availability; HTML82–252,268–312. Không chạy code, không đọc paper trích dẫn như nguồn đã kiểm. |

## 2. Cặp AI-TOD-v2 ↔ AI-TOD-R: mạnh ở kiểm soát ảnh, yếu ở độc lập nhãn

**V:** AI-TOD-R bổ sung hướng trên nền AI-TOD-v2; Table I ghi cả hai có 28.036 ảnh. OBB ban đầu do H2RBox-v2 sinh từ giám sát HBB, sau đó tình nguyện viên sửa, trường hợp không chắc được thảo luận/bỏ phiếu, chuyên gia và tình nguyện viên kiểm lại từng ảnh. Đây là kiểm hai lượt của nhóm; nguồn không nói hai nhóm gán nhãn OBB độc lập và làm mù với nhãn HBB. Các nhãn tự động có lỗi bỏ sót và định vị trước sửa. [DT01 §III-A/B; DT02]

**I:** có cơ sở chắc ở mức mô tả dataset để gọi đây là cùng bộ ảnh, hai dạng nhãn. **U:** chưa đối chiếu filenames, bitwise images, split membership hay mapping instance giữa các archive. Không thể nhảy từ “cùng ảnh” sang “cùng vật và một-một từng ID”. Các tổng nhãn khác nhau trong dossier: vehicle R 662.929 vs v2 652.045; tổng R 752.460 vs v2 752.745 trong prose/752.754 từ Table 1. [DT03; dossier §1.1, dữ liệu đã có]

**D — điều kiện để đối chiếu hợp lệ:**

1. Ghép ảnh bằng tên gốc + kích thước + hash ảnh/ảnh giải mã; ghi rõ đổi tên/crop. Cố định cùng tập ảnh trong cùng split.
2. Giữ nhãn gốc, map lớp minh bạch. Ghép instance theo lớp, vị trí và overlap đa tiêu chí; giải bài toán ghép một-một, đánh dấu unmatched và ambiguous. Không ghép theo thứ tự dòng hoặc chỉ bbox-IoU lớn nhất trong cụm dày.
3. Không dùng chính discrepancy định kiểm làm điều kiện loại cặp: nếu chỉ giữ cặp envelope-IoU cao, phép đo sẽ tự loại trường hợp lệch mạnh. Dùng một tập con được kiểm ảnh để đánh giá độ đúng của matching; báo độ phủ ghép theo lớp/size/density và độ nhạy ngưỡng.
4. Báo riêng unmatched, matched chắc và ambiguous. Cặp matched là một tập con có thiên lệch; không mặc định đại diện toàn dataset.

**HBB-envelope disagreement không phải phép đo nhiễu nhãn đã được xác thực (I).** Lệch tăng khi hộp nhỏ có thể do: quy ước HBB tight so với envelope OBB; OBB sửa hợp lệ; lượng tử tọa độ; ghép nhầm; thêm/bỏ instance; hoặc lỗi gán nhãn. Góc sai vẫn có thể giữ envelope gần đúng; envelope lệch vẫn có thể đúng về vật thể. Hơn nữa cùng nguồn giám sát tạo sai số phụ thuộc: agreement cao không xác nhận độc lập “nhãn sạch”.

**D:** gọi kết quả là *cross-representation inconsistency*, dùng để chọn mẫu audit ảnh có làm mù. Để gọi là noise cần tái gán nhãn độc lập một tập con phân tầng theo size/class/density, quy tắc rõ, độ đồng thuận giữa annotator và phân xử. Histogram góc co cụm cũng chỉ gợi giả thuyết: hướng đường/xe, dạng hộp, chuẩn hóa OpenCV và làm tròn có thể tạo cùng dấu hiệu. So giám sát HBB/OBB trên cùng ảnh giúp khống chế thành phần ảnh, nhưng còn confound chất lượng nhãn, tập instance, loss và evaluator; chưa tự tách tác dụng “thông tin góc”.

## 3. Độc lập nguồn, chồng ảnh và leakage là ba câu khác nhau

**V:** NWD mô tả AI-TOD tạo từ nhiều dataset công khai; AI-TOD-v2 giữ nguyên ảnh/lớp, sửa nhãn AI-TOD. Các nguồn được dẫn gồm Xia/DOTA, Lam/xView, Zhu/VisDrone, Airbus và Li/DIOR. [DT03 §3/§3.1]

**I:** DOTA/DIOR/VisDrone dùng bổ sung vẫn có giá trị mở rộng độ lớn, scene, lớp và giao thức; chưa đủ căn cứ gọi là nguồn chụp hoàn toàn độc lập với AI-TOD-R. Nhưng chia sẻ một phần nguồn dataset **không tự chứng minh leakage** ở một thực nghiệm cụ thể. Leakage cần chỉ ra ảnh hoặc vùng/cảnh liên quan của tập đánh giá đã vào train, adaptation, chọn checkpoint/hyperparameter hay teacher/pretraining trong protocol đang dùng. Một subset có xuất xứ chung vẫn có thể được chia đúng; ngược lại hai tên dataset khác nhau vẫn có thể trùng crop hoặc gần trùng cảnh.

**D:** dựng bảng provenance theo ảnh gốc/cảnh/chuyến bay, map parent–crop–tile, exact/perceptual matches. Split theo parent image và scene/video; kiểm cả teacher/pretraining nếu biết tập dữ liệu. Báo riêng (a) source overlap, (b) confirmed image/scene overlap, (c) demonstrated train–test contamination. Cùng tổ chức/tác giả/GitHub owner không đủ suy ra (b) hoặc (c).

Không dùng “≥3 nguồn độc lập + ≥2 họ detector” làm định luật Q2. Đây có thể là mục tiêu kiểm tra robustness do nhóm chọn; cần độ rộng phù hợp claim và venue cụ thể, không có ánh xạ tất định từ số dataset hay rubric tier sang quartile (I).

## 4. CODrone và DroneVehicle: điều đã biết, điều còn thiếu

| Dataset | Task/nhãn V | Availability V/U | Tiny và independence |
|---|---|---|---|
| CODrone | UAV nhìn xuống/nghiêng, 12 lớp; OBB bốn đỉnh; manual; ignored và difficulty. 10.004 ảnh 3840×2160; DJI Mavic 3 Pro, 30/60/100 m; 30°/90° [DT04] | Repo công khai; Drive link; tree train/val/test có DOTA annfile/VOC labels, split script [DT05]. Archive mở/tải/đọc thành công **U** | §III-C đánh khó nếu nhỏ hơn 32×32, không phải thống kê phần trăm dưới 16. Không có tiny mean/share định lượng trong phần đã đọc **U**. Capture riêng hỗ trợ independence về provenance **I**, chưa kiểm ảnh/cảnh. |
| DroneVehicle | UAV RGB–IR vehicle detection; 28.439 cặp, 5 lớp; quadrilateral bốn đỉnh, 953.087 nhãn cộng hai modality. Tác giả tự thu ảnh; hiệu chỉnh affine/crop; nhãn hai modality có thể khác [DT06] | Repo chính thức có Baidu train/validation/test và link code UA-CMDet; Drive ghi chưa phát hành [DT07]. Archive thực tế **U** | §III-D báo thuộc tính chiếu sáng/góc/độ cao, chưa thấy histogram/bin/share dưới 16 **U**. Không suy trùng VisDrone chỉ vì chung owner **I**. |

**V — lỗi metadata cần giữ mở:** CODrone v1 ghi 443.592 trong §III-C nhưng Table I 596,7k và phần đầu >590k; Table III ghi 90 m, prose 100 m. DroneVehicle primary §III-D ghi 80/100/120 m và nhiều góc; vì thế không thay primary bằng hàng 40 m/30° của Table I CODrone. [DT04, DT06]

**D:** kiểm annotation manifest để chốt count/version; tính size theo polygon area và theo rectangle-fit, tại ảnh gốc **và** sau transform vào detector. Tách difficulty/ignored. Downsample để tạo tiny là một thí nghiệm suy giảm có kiểm soát, không được gọi toàn dataset vốn là tiny tự nhiên. CODrone nhiều độ cao không bảo đảm có ID cùng vật/cùng lúc để paired comparison; phải kiểm mapping, view và scene, tránh diễn giải altitude thành can thiệp duy nhất.

## 5. CSCWD: đối chứng cơ chế có giá trị, bằng chứng chuyển miền còn điều kiện

**V:** task là UAV tầm xa trên Drone-vs-Bird, zero-shot DUT-Anti-UAV; không phải tiny OBB của vật mặt đất trong UAV-view. Teacher YOLO11m-P2, student YOLO11n: chiếu 1×1, upsample bilinear student P3 khớp teacher P2, channel-wise KL; P4/P5 cùng tỉ lệ; bỏ phần phụ khi suy luận. Teacher/student đều qua COCO/VisDrone adaptation. Tables 2/6 báo AP50 47,25→50,17 (+2,92), same-scale với P2 teacher 48,08→50,17 (+2,09). DUT AP50 +1,77 nhưng AP50:95 24,04→24,00. MGD có AP cao hơn CSCWD; nTCR tương quan, không chứng minh nhân quả. Preprint ghi code/config chưa công khai. [DT08 §§3,4,5,availability]

**I:** bài này hỗ trợ khả năng truyền biểu diễn phân giải cao vào student không có P2 inference. Nó chưa xác lập “lỗi dưới-stride của AI-TOD-R đã sửa bằng đặc trưng”, chưa chứng minh áp dụng OBB, angle hay assignment; không cung cấp effect size chuyển nguyên sang #7. “A8 đủ ứng viên nhưng recall thấp ⇒ nguyên nhân nằm ở đặc trưng” trong direction-map quá mạnh: đủ candidates không bảo đảm positives sau conflict, gradient hữu ích, nhãn đúng, localization/angle tốt hoặc postprocessing giữ detection.

**D — comparison để kiểm H-feat trên #7:** factorial coverage {baseline, A8} × transfer {none, same-scale, cross-scale}, cùng dữ liệu/split/teacher/recipe/evaluator; sàn assignment cố định khi thêm P2. Đo candidates, positives sau conflict, target weight/loss rồi recall theo size/density và lỗi box/angle. P2 student là đối chứng riêng cho inference resolution. Nếu transfer cải thiện khi coverage đã đủ và thay đổi target feature có dấu hiệu phù hợp, H-feat được hỗ trợ ở protocol ấy; các giả thuyết nhãn, localization và context vẫn có thể cùng đúng. Thất bại transfer không chứng minh vật bất khả xác định: teacher/optimization có thể yếu. Không loại nhánh vì chi phí.

## 6. Trạng thái kết luận

Đã nâng độ sâu nguồn cho CODrone/DroneVehicle/CSCWD từ abstract sang các phần liên quan. Chưa có phép đo nhãn, hash, matching, tiny statistics tính từ archive hoặc kết quả thực nghiệm của nhóm. Chốt được cách phát biểu thận trọng: *paired representations trên chung tập ảnh*, *inconsistency để triage*, *source overlap chưa đồng nghĩa leakage*, và *CSCWD là prior cơ chế cần kiểm chuyển sang task #7*. Không chốt hướng thắng hoặc venue.
