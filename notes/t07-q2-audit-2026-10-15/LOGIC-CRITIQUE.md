# Kiểm toán logic: giữ câu hỏi nghiên cứu, sửa mức khẳng định

Ngày 15/10/2026. Phạm vi: ba note ngày 14–15/10, ledger C-13–18, các dẫn xuất kế thừa và DEEP-REPORT ngày 13/10. Chỉ đọc và lập luận; không train, không tái lập kết quả paper, không sửa note cũ. Đây là phản biện luận cứ, không phải dự báo nhận bài. P1 = lỗi làm mất hiệu lực kết luận chính; P2 = hạn chế cần sửa trước thiết kế xác nhận. Công thức mới ghi [derived]; phép thử là [design], cần thực nghiệm.

Nguồn tắt: VA = `t07-venue-assessment-2026-10-14.md`; QP = `t07-q2-path-2026-10-14.md`; DM = `t07-direction-map-2026-10-15.md`; CQ = `t07-critique-q2-2026-10-11.md`; DP = `t07-deep-study/DEEP-REPORT.md`; PROP = `t07-c3-proposal-v2-EN.md`. Các đường dẫn này nằm trong `notes/`. Code đã đọc là snapshot local `papers/_text/ultralytics_tal_main_2026-10-01.py`, không phải kiểm chứng phiên bản mới nhất.

## Kết luận phản biện

Tôi bác chuỗi suy luận “có định lý hình học → có giới hạn thông tin → cần một head mới → đủ dataset thì đạt Q2”. Từng mắt xích cần bằng chứng khác nhau. Vẫn giữ được hai câu hỏi mạnh: (A) can thiệp vùng ứng viên thay đổi các khâu mất GT như thế nào; (B) độ nhạy nhãn và chất lượng quan sát ảnh hưởng tới việc học hình học tiny như thế nào. Bản deep-study đã đặt controls tốt hơn các note mới: cùng evaluator, annotators độc lập, tách observation khỏi recipe, và cho phép một phương pháp đơn giản giải thích hết gain.

## 1. P1 — Cận phủ không dự báo optimum hoặc bảo đảm TAL positive

**Vị trí:** VA §3.1, §4.2, §6; QP §3.1; C-16 yêu cầu cận dự báo mức sàn tốt nhất trên hai dataset.

**Phần đúng [derived]:** trên lưới vuông vô hạn bước s, bán kính phủ là s/√2. Hình chữ nhật đóng có cạnh ngắn ≥ √2s chứa đĩa bán kính s/√2 nên chứa ít nhất một điểm lưới. Cận đều theo góc/vị trí là chặt: hình vuông xoay 45°, tâm tại tâm một ô lưới, cạnh √2s chạm bốn điểm gần nhất. Đây là cận đồng nhất dựa riêng trên cạnh ngắn; không phải kích thước tối thiểu của mọi hình chữ nhật cụ thể.

Tôi bác claim “√2s dự báo mức sàn AP tốt nhất”: định lý không chứa metric xếp hạng, gradient, chất lượng ảnh, xung đột, số positive hữu ích hay AP. Một vùng lớn hơn có thể cung cấp thêm giám sát; nhỏ hơn có thể đã đủ với phân bố thực. “Tối thiểu bảo đảm phủ worst case” và “tối ưu hiệu năng kỳ vọng” là hai bài toán khác nhau.

Code snapshot dòng 196–202 tiếp tục giao mask ứng viên với top-k; dòng 350–381 giải xung đột/lọc tiếp; dòng 170–174 chuẩn hóa trọng số. Hai GT có cùng ứng viên có thể mất hết positive cho một GT khi xử lý xung đột. Positive có trọng số nhỏ cũng không tương đương giám sát hữu ích. Chỉ có một candidate ở mức stride nhỏ nhất không bảo đảm candidate ở mọi mức.

**Sửa [design]:** đăng ký riêng giả thuyết hình học (tỷ lệ GT rỗng ở candidate mask) và giả thuyết hiệu năng (đường cong AP/recall theo sàn). Ghi số GT còn lại qua eligibility → candidates từng mức → top-k → conflicts → trọng số → dự đoán trước/sau postprocess. Bác cơ chế “chỉ thiếu phủ” nếu sửa phủ không thay đổi sự mất GT ở các khâu sau trong phạm vi kiểm; không tự quy phần còn lại cho features. Sweep sàn quanh √2s trên validation; optimum khác √2s không bác định lý.

## 2. P2 — Biên đóng, bất đẳng thức chặt và code phải tách rõ

VA §3.1 đúng khi nói **OBB snapshot** dùng ≥/≤: dòng 425 đã kiểm trực tiếp. Không được sửa thành “code OBB đang dùng strict”. Ngược lại, HBB cùng snapshot dòng 344–347 dùng khoảng cách tới bốn cạnh **> eps**.

**[derived]** Nếu phép thử loại biên, hình vuông 45° tại đúng cận √2s chỉ chạm điểm lưới và có thể rỗng. Cần cạnh ngắn > √2s để có bảo đảm strict trong toán chính xác. Nếu loại một dải biên Euclid dày ε, điều kiện đủ là cạnh ngắn > √2s + 2ε; epsilon trên dot product có đơn vị khác, không thay thẳng vào công thức này. Tương tự, HBB cạnh đúng s không bảo đảm với phép thử strict ở pha lưới bất lợi.

Biến cố biên có xác suất zero dưới pha liên tục lý tưởng không cứu một phát biểu “mọi vị trí”. Làm tròn số, GT lượng tử hóa và miền feature hữu hạn cũng cần kiểm riêng. Chốt implementation, dtype, margin và vùng trung tâm hợp lệ trước khi đưa guarantee vào bài. Sanity check: ε→0 trả lại cận strict; s có đơn vị pixel.

## 3. P1 — Bằng nhau về kỳ vọng không chặn coverage hoặc AP ở “bậc hai”

**Vị trí:** PROP §6 Hệ quả 2–3; VA §3.1 và QP §1/§5 kế thừa luận điểm “hiệu ứng bị Hệ quả 2 chặn”.

Tôi bác suy luận này. Với pha lưới đều, cùng diện tích cho cùng kỳ vọng số candidate; không cho cùng phân phối, cùng xác suất rỗng hoặc cùng AP.

**Phản ví dụ [derived]:** trên một mức lưới, hình vuông s×s có N=1 hầu chắc chắn. Hình chữ nhật ngang 2s×(s/2), cũng diện tích s², có N=2 với xác suất 1/2 và N=0 với xác suất 1/2. Cả hai E[N]=1 nhưng P(N=0) lần lượt 0 và 1/2. Các pha đúng biên có measure zero trong ví dụ. Sanity check: hai kỳ vọng đều bằng diện tích/s².

**Sửa:** dùng định lý để khớp mean-count control; đo P(N=0), quantiles N, vị trí candidate, conflicts và loss-weight mass riêng. Không gọi hiệu ứng “bậc hai” nếu chưa định nghĩa khai triển/tham số nhỏ và chưa có cận cho endpoint. Ngoài ra uniform phase là giả định cần kiểm trên dữ liệu thật, không phải định luật của mọi annotation pipeline.

## 4. P1 — arctan là độ nhạy có điều kiện, không phải sàn sai số hoặc identifiability

**Vị trí:** CQ §5.2(a) nêu vuông góc; QP §3.1 rút thành “lệch tối đa δ px ở hai đầu” và gán nghĩa giới hạn khả năng xác định; C-17/18 kế thừa.

**[derived]** Với trục thật v=(L,0), hai endpoint chỉ lệch theo phương vuông góc, mỗi đầu ≤δ, trục mới là (L,t), |t|≤2δ. Khi đó |Δθ|≤arctan(2δ/L), có thể đạt cận. Nếu endpoint được nhiễu 2D bất kỳ với chuẩn Euclid mỗi đầu ≤δ, sai phân nhiễu nằm trong đĩa bán kính r=2δ. Khi r<L, tiếp tuyến từ gốc tới đĩa tâm (L,0) cho cận chặt **|Δθ|≤arcsin(2δ/L)**. Với 2δ≥L, trục mới có thể bằng zero và hướng không xác định; không mở rộng asin ra ngoài miền. Sanity checks: δ=0 trả 0; δ/L→0 hai cận cùng xấp xỉ 2δ/L; tỷ số vô thứ nguyên. Với nhiễu chặn từng tọa độ, mô hình và cận lại khác.

Tôi bác claim “sàn loss góc do nhiễu nhãn lớn gấp 10–20 lần” ở CQ. Đây là **cận trên worst case**, không là cận dưới lỗi không thể tránh hoặc kỳ vọng loss. Nhiễu bằng zero, hoặc hai endpoint dịch như nhau, cho sai số góc bằng zero dù cùng δ. Lấy sin² của một góc worst case không cho expected training loss; loss tuần hoàn còn không đơn điệu trên mọi miền góc.

Tôi cũng bác đồng nhất cận này với khả năng xác định hướng vật lý từ ảnh. Muốn nói identifiability phải định nghĩa mô hình tạo ảnh và biến nuisance: blur, contrast, texture, symmetry, PSF, sampling, occlusion; hai hướng khác nhau có tạo phân bố quan sát phân biệt được không? Không có mô hình đó trong dẫn xuất endpoint. Độ dài trục hộp, semantic heading và góc của Gaussian shape không phải một biến. Near-square làm trục hình học không ổn định nhưng texture có thể còn chỉ heading; Gaussian đẳng hướng bỏ thông tin hình dạng có thể vẫn còn hữu ích.

**Sửa [design]:** gọi hướng hiện tại là “độ nhạy và độ tin cậy góc theo scale” cho tới khi có bằng chứng identifiability. Ước lượng δ từ reannotation độc lập hoặc paired acquisition phù hợp; kiểm calibration/coverage của phân phối góc trên nhãn độc lập. Giữ metric OBB chính thức. Nội suy ảnh không thêm phép đo: resize cùng L và δ bởi k giữ tỷ số δ/L; gate dựa chỉ vào input-pixel L với δ cố định có thể phản ứng với phép resize vô hại.

## 5. P1 — Histogram nhãn và “điểm gãy” không là phép thử quyết định

**Vị trí:** QP §3.3(2), §6; DM H-angle; C-17/18.

Góc tụ cụm có thể phản ánh đường/bãi xe thẳng hàng, lớp vật thể, canonicalization w/h, góc ảnh, làm tròn hoặc prior của H2RBox-v2. Tiny và large có thể ở scene/camera khác nhau. Mất tương quan hàng xóm có thể do giao thông khác hoặc association sai. Đó là dấu hiệu audit, chưa chứng minh nhãn ít thông tin.

Phản ví dụ logic: histogram đều ở cả hai bin, nhưng bin tiny là góc ngẫu nhiên còn bin large đúng; histogram giống nhau không bác nhiễu. Ngược lại, mọi xe nhỏ thực sự đỗ cùng hướng nên histogram co mạnh dù nhãn chính xác. Bởi vậy “không khác histogram thì đóng hướng” là falsifier không hợp lệ.

Sai số baseline tăng theo size còn chịu selection: chỉ đo các GT được match làm loại những vật khó nhất. Một đường cong trơn tăng sai số vẫn hỗ trợ độ nhạy scale; không có knee không bác toàn bộ hướng. Knee quan sát cũng có thể đến từ stride, binning, canonicalization hoặc lọc GT.

**Sửa [design]:** stratify/match theo scene, class, aspect ratio, blur, orientation convention; ghi misses riêng; annotators độc lập và adjudication trên subset. So smooth size-effect với change-point trên split xác nhận khác; không bắt buộc tồn tại breakpoint. Cặp HBB/OBB chung ảnh kiểm consistency/lineage, không là hai phép đo độc lập về góc vì OBB được sinh từ HBB. Ghép đúng instance trước khi so, báo những cặp thiếu/khác ontology.

## 6. P1 — Còn recall thấp không chứng minh feature cause; AP50–AP75 không cô lập lỗi góc

**Vị trí:** DM §3(2) khẳng định “Nếu A8 đủ ứng viên mà recall vẫn thấp thì nguyên nhân nằm ở đặc trưng”; DM H-feat/H-loc.

Tôi bác kết luận feature cause. Các khả năng còn lại gồm không có positive sau conflicts, trọng số yếu, class scores, regression, thiếu nhãn, lỗi converter, postprocess/cap, optimization và thiếu thông tin ảnh. P2 hoặc distillation thắng cũng đổi capacity, supervision, teacher information và loss balance. DP §2.2/§4A đã chỉ đúng các confound này.

AP50 và AP75 dùng hai ngưỡng matching: chênh lệch cho thấy độ nhạy với yêu cầu overlap, không xác định lệch tâm, kích thước, góc hay lỗi nhãn. AP là endpoint tổng hợp phụ thuộc score ranking/matching; không đọc hiệu AP như số lỗi góc. Công thức IoU=(w−δ)/(w+δ) đúng cho hai hình vuông cùng kích thước, chỉ dịch một trục, 0≤δ≤w (DP §2.3); không phải công thức chung cho tiny OBB.

**Sửa [design]:** kiểm các stage trước khi mở feature intervention; dùng teacher/auxiliary-loss control tương đương và ghi nguồn thông tin thêm. Với localization, phân tích center/extent/angle trên matching cố định có báo selection; dùng oracle replacement từng thành phần để đo độ nhạy evaluator. Oracle gain là upper-opportunity diagnostic, không phải hiệu quả phương pháp triển khai hoặc tỷ trọng nguyên nhân thật.

## 7. P1 — “Ngân sách lỗi” cộng được chưa được nhận dạng

**Vị trí:** DM §2 nói biết “mỗi nguyên nhân chiếm bao nhiêu”.

Một GT có thể đồng thời thiếu candidate, nhãn sai, feature yếu và bị cap. Các nhóm lỗi chồng nhau; sửa một khâu có thể chỉ hữu ích sau khi sửa khâu khác. Hồi quy observational hoặc oracle gain riêng không phân rã duy nhất AP.

**[derived]** Với hai can thiệp A/B và endpoint Y, tương tác I=Y11−Y10−Y01+Y00. Nếu I khác zero thì gain khi thêm A sau B khác gain khi thêm A trước B; phân bổ gain theo thứ tự không duy nhất. Sanity check: I=0 khôi phục cộng tính cho hai intervention đã định nghĩa, chưa chứng minh chúng tương ứng hai nguyên nhân vật lý độc lập.

**Sửa [design]:** gọi bảng ban đầu là “dấu hiệu lỗi có thể chồng lấn”. Chọn factorial nhỏ với intervention xác định rõ, báo conditional effects và interactions, cùng seed/data splits. Nếu cần Shapley allocation, ghi đó là quy ước phân bổ phụ thuộc tập intervention, không phải ground-truth causal percentages. Chọn ưu tiên phân loại tạo bảng cộng 100% cũng là accounting convention. Không dùng CI theo GT thay cho scene-level independence hoặc biến thiên giữa training runs.

## 8. P1 — Quy tắc tier/venue là rubric nội bộ, đã mâu thuẫn ledger trước

**Vị trí:** QP §1–2/§4/§6; VA §4/§6; C-16–18. C-13 ghi “Do not reuse deterministic tier→quartile mapping”; C-15 ghi quartile không là per-paper method grade. Sau đó C-17/18 lại đặt “without 3 ... datasets the ceiling is Q3”.

Tôi bác việc coi “train-only assignment luôn T1”, “phải đổi kiến trúc”, “≥3 datasets + ≥2 detector families” là định luật editorial. Đây là lựa chọn trong file rubric local, không bằng chứng độc lập về quyết định của tạp chí. Báo cáo này không xác minh ranking hay policy của một venue cụ thể, nên cũng không đưa ra lời hứa Q2 thay thế. Mọi đánh giá venue sau này cần criteria chính thức và scope cụ thể, tách khỏi nhãn loại can thiệp.

Ba dataset có thể là replication target hữu ích cho một claim rộng nhưng không tự đủ, cũng không tự cần cho mọi contribution. Dataset HBB bổ sung không xác nhận claim góc OBB. Chung nguồn ảnh cần audit overlap/scene lineage; tên dataset khác không tự độc lập, và chung nhóm tác giả không tự chứng minh trùng ảnh. Không đọc đủ method/experiment thì “abstract không nói size” chưa chứng minh method không size-aware. Không thấy paper trong scan chỉ là kết quả tìm kiếm có giới hạn.

**Sửa:** khôi phục cách C-13–15: chọn claim, novelty, controls và phạm vi tổng quát trước; dataset count là thiết kế cho claim. Nếu phương pháp đơn giản giải thích hết gain, dừng module nhưng vẫn xem xét giá trị chẩn đoán. Không gắn thành công nghiên cứu với việc buộc phải dựng head mới.

## Bản phát biểu thay thế có thể bác bỏ

**A — Assignment [design]:** “Trong implementation và phân bố đã khóa, giảm candidate starvation bằng vùng theo stride có làm tăng số GT nhận giám sát hữu ích và recall không; effect thay đổi thế nào theo mật độ?” H0 thực dụng: effect và interaction đã chọn không vượt biên hữu ích định trước. Đo mediator nhưng không đồng nhất tương quan mediator với causal mediation. Định lý phủ và optimum hiệu năng là hai kết quả tách biệt.

**B — Annotation/observation [design]:** “Ở cùng scene/class/aspect/blur, disagreement độc lập và chất lượng quan sát có dự báo lỗi góc tốt hơn size-only không; can thiệp nhãn/loss/head thay đổi quan hệ này ra sao?” So original/corrected labels × deterministic/distributional prediction, cùng evaluator. Nếu cleaning/simple loss đạt tương đương theo margin định trước thì dừng head; nếu independent disagreement không liên hệ effect sau controls thì hạ giả thuyết ambiguity. Không có knee không đủ để bác.

**C — Decision criterion [design]:** mở module khi chẩn đoán xác nhận một failure còn lại, simple strong controls không giải thích đủ và prior gần chưa chiếm cơ chế. Báo uncertainty về effect, giới hạn nhận dạng và kết quả null. Không điều kiện hóa việc công nhận khoa học vào thắng AP hoặc nhãn quartile.

## Kiểm chứng và giới hạn của audit

Đã đối chiếu C-13–18 và đọc trực tiếp code snapshot để xác nhận biên OBB/HBB, candidate/top-k/conflict. Các cận sửa có giả định, dẫn xuất ngắn và sanity check; phản ví dụ equal-mean/coverage là phân tích giải tích, không phải run dataset. Không xác minh lại paper ngoài, không chạy phép thử nhãn, không benchmark; kết quả của paper được xem là tác giả báo cáo trong các note. Hai câu hỏi bắt buộc của phản biện vẫn mở: **What is new here?** — chưa có bằng chứng novelty riêng cho size-conditioned mechanism; **Where is the ablation?** — hiện chỉ có thiết kế, chưa có kết quả độc lập.
