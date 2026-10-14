# Audit prior về góc: AQE và O2-DETR

Ngày: 2026-10-15 · Worker: angle_prior_sol · Research-only, không code/train.

**Kết luận:** C-18 cần mở lại câu hỏi novelty. “Phân phối góc + confidence + NMS” đã có prior; nhưng cũng chưa thể nói “chỉ còn size-conditioning là mới”. Phải định nghĩa chính xác *conditioning*, *uncertainty*, *identifiability*, và kiểm tra hiệu quả sau các đối chứng. Không chuyển rubric T1/T2/T3 thành luật nhận bài Q2; quartile của journal không bảo đảm chất lượng hoặc khả năng nhận từng bản thảo.

## Nguồn và độ sâu

| ID | Nguồn chính, phiên bản và locator | Độ sâu thực đọc / giới hạn |
|---|---|---|
| AP01 | Chaowei Li, **Oriented object detection in remote sensing images based on angle quality estimation**, [DOI/HTML](https://www.nature.com/articles/s41598-025-31034-w); published 09-12-2025, volume 16, article 1576 (2026). [Table 1](https://www.nature.com/articles/s41598-025-31034-w/tables/1?error=cookies_not_supported), [Table 2](https://www.nature.com/articles/s41598-025-31034-w/tables/2?error=cookies_not_supported). | Đọc Methods cả bốn mục; Experimental setup; Results analysis/Ablation, Parameter analysis, Comparison; Conclusion. Đọc hàng Table 1–2 trực tiếp. Tables 3–10 và Figures chỉ đọc caption/prose liên quan; chưa audit code, supplement hoặc PDF. HTML lấy được sau redirect cookie; URL có `?error=cookies_not_supported` dùng được cho bảng. |
| AP02 | Ding et al., **Real-Time Oriented Object Detection Transformer in Remote Sensing Images**, [arXiv record](https://arxiv.org/abs/2603.15497), [HTML v1](https://arxiv.org/html/2603.15497v1), [PDF v1](https://arxiv.org/pdf/2603.15497v1), 16-03-2026. Record ghi TGRS DOI 10.1109/TGRS.2026.3671683. | Đọc IV-A–D, V-A–E, VI; trực tiếp equations (1–4), (13–17), Tables VII–X và Fig.10/12/13 captions/prose. PDF truy cập được (15 trang), cơ chế được đọc qua HTML; chưa audit code/supplement. Record hiện liệt kê v1. |

Đầu vào nội bộ đã đọc: `notes/INDEX.md`, `notes/claims-ledger.md` C-12/C-17/C-18; `notes/05-venue-direction/t07-q2-path-2026-10-14.md`; `notes/05-venue-direction/t07-direction-map-2026-10-15.md`; `notes/06-uav-research-2026-10-13/t07-deep-study/CASEBOOK-STATIC.md` §4–6 (GauCho). Không coi casebook thay thế nguồn chính của hai bài mới. Wholly-WOOD không đọc trong lượt giới hạn này.

## AP01 — điều gì thực sự đã có

[Toàn văn] AQE dự đoán mean/std từ ROI features; chất lượng góc = $1-\theta_\sigma$. NMS dùng tổng có trọng số giữa quality và class score. Double-A Loss điều chỉnh bằng aspect ratio và độ khó. [Methods: Angle quality estimation; Non-maximum suppression; Angle loss; Multi-task joint optimization]

[Kiểm bảng] Table 1–2 là thêm module tuần tự; Table 1 chia lớp, không chia kích thước pixel. Table 2: AQE+Double-A **38.94 mAP75** → thêm NMS-AQ **39.97**, DOTA validation [tác giả báo cáo]. Đây là conditional increment, không phải thí nghiệm calibration. Prose “synergy” chưa được thiết kế factorial trong hai bảng này cô lập. [Table 1–2; Ablation]

[Giới hạn nguồn] Phần Methods được đọc không có gate theo pixel size; ảnh/ROI có thể chứa thông tin scale. Tỉ lệ cạnh khác kích thước tuyệt đối. Không thấy reliability/coverage/risk theo size trong phần Results đã đọc; chưa kiểm nội dung số của mọi bảng nên không tuyên bố toàn bài/supplement tuyệt đối không có. [Methods; Results]

## AP02 — phải sửa “size-blind” thành phát biểu có phạm vi

[Toàn văn] ADR dự đoán bốn phân phối cạnh hộp bao ngoài và hai offset đỉnh, refine logits qua decoder. Expectations được nhân $(W_r,H_r)$ ở Eq.(1), và $(W_r,H_r,W_r,H_r)$ ở Eq.(2). OCD box noise cũng tỉ lệ $w,h$; probability noise chuẩn hóa bằng $\max(w,h)$. [IV-B Eq.1–4; IV-D Eq.13–17]

[Kiểm bảng] Table VII: sau OCD **73.72 AP50** → thêm ADR **75.05**, O2-DFINE-s/DOTA-v1.0 [tác giả báo cáo]. Tables VIII–X quét bins, mapping, cost và noise; không chia size. Class “small vehicle” hoặc DOTA-v1.5 không thay cho size-stratified angle ablation. [V-A/C/D]

[Giới hạn nguồn] Eq.(1–4) dùng softmax/expectation để decode hình học; phần đọc không thiết lập confidence góc được calibration hoặc pixel-size identifiability gate. Không thấy size-binned calibration/angle error trong Tables VII–X. [IV-B; V-D/E]

## Phân biệt bốn đại lượng trước khi đặt claim

| Đại lượng | Câu hỏi phải chứng minh [audit/design] | Hệ quả cho #7 |
|---|---|---|
| Geometry covariance | Gaussian mô tả diện tích/hình dạng hộp hay sai số của ước lượng? | Không dùng covariance của GauCho như predictive confidence. Casebook G10 đã cảnh báo điều này. |
| Distribution / confidence | Đầu xuất phân phối để hồi quy tốt hơn, hay score dự báo lỗi đúng? | Entropy/std nhỏ chưa chứng minh calibration; chất lượng dùng được cho ranking khác xác suất đúng. |
| Scale dependence | Nhân tọa độ với kích thước hộp, features mang scale, hay gate nhận trực tiếp pixel length/GSD? | “Size-conditioned” phải chỉ rõ biến, đơn vị và điểm can thiệp. Geometry normalization đã là prior; gate vật vài pixel là câu hỏi khác. |
| Identifiability | Với cùng quan sát ảnh, có nhiều góc phù hợp ngang nhau dưới mô hình đo/nhãn không? | Sai số mô hình cao theo size không tự chứng minh ảnh không có thông tin góc. |

**[Suy luận audit]** Tỉ lệ cạnh là confound quyết định: cùng số pixel, hình dài và gần vuông có tính xác định hình học khác nhau. Ở gần vuông, geometric axis, OBB convention và semantic heading cũng là ba target khác nhau. Isotropize Gaussian có thể bỏ orientation có nghĩa từ appearance; không nên xem việc đổi target là khôi phục tín hiệu.

**[Suy luận audit]** Hai lưu ý implementation cần làm rõ trước tái lập AQE: formula NMS là weighted sum trong mục chính nhưng paragraph comparison mô tả additive form khác; lý giải std có câu mâu thuẫn về xu hướng tiến tới 0/1. Đây là vấn đề văn bản, chưa phải kết luận implementation sai. Dùng equation/author clarification thay vì tự chọn một biến thể và gọi đó là reproducing.

## Novelty còn mở và đối thủ mạnh nhất

**Đối thủ cơ chế sát nhất:** AP01 cho confidence góc dùng ở NMS và shape-adaptive supervision; AP02 cho distributional refinement gắn geometry scale. Vì vậy một nhánh size-aware phải thắng *cả* score-quality và geometry/refinement controls, không chỉ deterministic angle baseline. GauCho là đối chứng target/representation khi đề xuất chuyển sang Gaussian bất biến quay.

**[Chưa xác lập novelty]** Câu hỏi khả thi để điều tra là: *thông tin đo ở độ phân giải hữu hạn có dự báo được lỗi/độ tin cậy góc ngoài aspect ratio, appearance và nhiễu nhãn không; khi đó hành động nào hữu ích?* Hai bài này không đủ là novelty search toàn lĩnh vực. Không thấy phép thử trong phạm vi đọc không chứng minh lĩnh vực trống, và không đủ để chốt một kiến trúc mới.

**[Audit cận]** $\arctan(2\delta/L)$ trong note cũ cần ghi mô hình perturbation: nó mô tả hai đầu trục lệch theo phương vuông góc với trục, mỗi đầu tối đa $\delta$, với khoảng cách dọc trục $L$ giữ cố định. Nếu endpoint có sai số hai chiều, mẫu số/miền perturbation phải xét lại. Ngay cả khi đúng trong mô hình ấy, đây là sensitivity của hình học quan sát, chưa tự là cận thông tin của mọi ảnh. Blur, sampling, contrast, semantic cues, annotation convention và nhiều quan sát có thể đổi bài toán. Không gọi nó “định luật không thể xác định” trước khi khóa giả định và kiểm chứng độc lập.

## Các đối chứng có tính quyết định — đề xuất, chưa chạy

1. **Tách pixel size khỏi aspect ratio:** cùng lớp/cùng aspect ratio/cùng density/contrast, đo circular angle error và quality ranking theo cạnh dài; kiểm geometric axis riêng với semantic heading. Nếu size effect biến mất sau điều kiện này thì gate theo size chưa có cơ sở riêng.
2. **Tách uncertainty khỏi score hữu ích:** so confidence/std/entropy với lỗi góc trên held-out scenes; reliability theo sự kiện “sai số trong tolerance”, interval coverage nếu đầu thực sự xuất predictive distribution, risk–coverage và AP/recall dưới cùng budget. Báo calibration theo size và domain shift; calibration fitted trên validation, không dùng test để chọn tolerance/gate.
3. **Tách geometry normalization khỏi giới hạn pixel:** matched head/compute, direct-angle, AQE-style quality, ADR-style distribution/refinement, shape-only weighting, size-only loss gate và size-aware representation/decoder. Giữ assignment, backbone, augment, loss scale, evaluator, postprocessing tương ứng. So full package khác detector không cô lập cơ chế.
4. **Tách nhiễu nhãn khỏi thiếu tín hiệu ảnh:** nhãn cặp HBB/OBB cùng ảnh chỉ là diagnostic vì OBB sinh yếu từ HBB không độc lập. Cần tập nhỏ được nhiều người annotating lại, blind với model/gate và có native/HR reference khi hợp pháp sẵn có; báo disagreement theo size. Góc bị lượng tử hóa thành vài giá trị chỉ là dấu hiệu nhãn, chưa kết luận image identifiability.
5. **Can thiệp có kiểm soát:** cùng cảnh/đối tượng, degrade resolution/blur và giữ riêng output scale, rồi kiểm dự báo của mô hình đo đã khóa trước. Upsampling không tạo quan sát mới; augment thay size đồng thời có thể thay aliasing. Cần native-resolution real scenes để tránh kết luận chỉ đúng trên synthetic degradation.
6. **Không “thắng” bằng đổi metric:** giữ OBB metric gốc làm endpoint chính; report nhánh ellipse/rotation-invariant như target bổ sung. Kiểm gate giảm angle penalty có đổi recall/NMS/confidence đối với objects thực sự có heading không. Một điểm gãy do IoU/evaluation threshold khác điểm gãy của thông tin đo.

## Trạng thái kiểm chứng và handoff

- Confidence **high cho nội dung/locator đã đọc**; **medium cho khái quát empirical của tác giả**; **low/chưa xác minh cho novelty toàn lĩnh vực hoặc dự báo lợi ích**.
- Không chạy mô hình/thí nghiệm; không xác minh gain, code hay seed reproducibility độc lập. Hai numerical pairs trên là báo cáo tác giả, không so chéo detector/dataset.
- Khuyến nghị sửa C-18 khi tổng hợp: giữ “candidate”; thay câu “phần còn lại chỉ là pixel-size conditioning” bằng “pixel-size observability, calibration và hành động dựa trên uncertainty còn cần được định nghĩa/kiểm; scale dependence hình học và shape-adaptive supervision đã có prior”. Không sửa ledger/notes cũ trong worker này.
- File mới duy nhất: `notes/07-audits/t07-q2-audit-2026-10-15/ANGLE-PRIOR.md`. Không download cache vì HTML đủ cho scope; không push.
