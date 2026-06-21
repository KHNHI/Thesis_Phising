# ĐỀ CƯƠNG KHÓA LUẬN / THESIS OUTLINE

**UEH University** — Trường Đại học Kinh tế TP. Hồ Chí Minh

- **Sinh viên / Student:** Lê Quốc Bảo *(cần xác nhận — bài báo đứng tên Khai Nhi Thieu)*
- **GVHD / Supervisor:** TS. Nguyễn Quốc Hưng / Dr. Nguyen Quoc Hung

**Tên đề tài:** "Khung Trí tuệ Nhân tạo Khả diễn giải cho Phát hiện Email Lừa đảo Đáng tin cậy: Xây dựng Bộ dữ liệu Đa nguồn, Diễn giải bằng SHAP–LIME và Phân tích Tính bền vững trước Tấn công Đối kháng"

**Title:** "An Explainable AI Framework for Trustworthy Phishing Email Detection: Multi-Source Dataset Construction, SHAP–LIME Interpretability, and Adversarial Robustness"

---

## Kế hoạch theo tuần / Weekly plan

| Tuần | Nội dung công việc / Content |
|------|------------------------------|
| **1** (khởi động) | Chốt hướng mở rộng + 4 câu hỏi nghiên cứu; khảo sát & chọn dataset; dựng môi trường + repo + version control. |
| **2** | Hợp nhất nguồn → corpus đa nguồn; chuẩn hóa schema; khử trùng lặp, cân bằng nhãn, kiểm soát rò rỉ theo sender-domain (GroupShuffleSplit). |
| **3** | Tiền xử lý văn bản (làm sạch HTML, URL/email → token); trích đặc trưng TF-IDF (1–2 gram, max_features=20k, sublinear_tf). |
| **4** | Huấn luyện 5 ML cổ điển (LR, NB, DT, RF, Linear SVM); đánh giá đa chỉ số + StratifiedKFold (k=3). |
| **5** | Fine-tune transformer (BERT-base, DistilBERT, RoBERTa); so sánh vs. TF-IDF; McNemar's Test + bootstrap CI 95%. |
| **6** | Khung diễn giải hai cấp: SHAP (toàn cục) + LIME (cục bộ); nhất quán SHAP–LIME (Pearson, Spearman, Jaccard); taxonomy đặc trưng. |
| **7** | Bias audit (phishing thực vs. artifact; đơn nguồn vs. đa nguồn); thí nghiệm đối kháng (char-sub, keyword injection, HTML obfuscation), đo sụt F1. |
| **8** | Viết Chương 1 (Introduction) + Chương 2 (Background & Related Work); error analysis 30 mẫu sai. |
| **9** | Viết Chương 3 (Design & Implementation) + Chương 4 (Results) + Chương 5 (Conclusion); ánh xạ CIA Triad. |
| **10** (hoàn thiện) | Rà soát toàn bộ; chỉnh theo feedback GVHD; chuẩn hóa trích dẫn; chuẩn bị artifacts (GitHub, dataset release); nộp. |

*Mốc 10 tuần mang tính kế hoạch, điều chỉnh theo lịch khoa.*

---

## CHƯƠNG 1. GIỚI THIỆU / INTRODUCTION

**1.1 Lý do chọn đề tài / Rationale**
- Phishing là kênh tấn công mạng nguy hiểm nhất (đánh cắp credential, lừa đảo tài chính, ransomware); APWG: >4,7 triệu cuộc tấn công năm 2022.
- ML đạt F1 > 0,98 nhưng là hộp đen → xói mòn niềm tin của nhà phân tích.
- Paper hội thảo trước: F1 = 0,9936 (Linear SVM) nhưng **80% top-20 đặc trưng SHAP là artifact theo dataset (CEAS)**, không phải dấu hiệu phishing thực → nghi vấn tổng quát hóa.
- Hai vấn đề bỏ ngỏ: (1) thiên lệch một nguồn; (2) thiếu khung diễn giải hai cấp + chưa đánh giá đối kháng thực nghiệm.

**1.2 Mục tiêu nghiên cứu / Objectives**
1. Xây corpus phishing đa nguồn (CEAS + Nazario/SpamAssassin/Enron/Nigerian Fraud/Ling) để giảm bias một nguồn.
2. Đánh giá 5 ML cổ điển + 3 transformer theo giao thức thống nhất.
3. Khung diễn giải hai cấp SHAP (toàn cục) + LIME (cục bộ) + định lượng nhất quán.
4. Bias audit + đánh giá đối kháng thực nghiệm, ánh xạ CIA Triad.

**1.3 Câu hỏi nghiên cứu / Research questions**
- **RQ1** — Đơn nguồn → đa nguồn: hiệu năng và khả năng tổng quát hóa thay đổi ra sao?
- **RQ2** — SHAP (toàn cục) và LIME (cục bộ) nhất quán đến mức nào?
- **RQ3** — Quyết định do dấu hiệu phishing thực hay artifact? Đa nguồn có giảm bias không?
- **RQ4** — TF-IDF vs. transformer bền vững đến đâu trước tấn công đối kháng?

**1.4 Đối tượng & phạm vi / Scope**
- Dữ liệu: corpus ~50–80k email; cân bằng phishing/legitimate; chia tách kiểm soát rò rỉ theo sender-domain.
- Mô hình: 5 ML (TF-IDF) + 3 transformer (BERT-base, DistilBERT, RoBERTa).
- Phạm vi: phát hiện dựa trên nội dung văn bản (tiếng Anh); diễn giải/bias/đối kháng ở mức từ vựng-đặc trưng. Ngoài phạm vi: header forensics, đồ thị mạng người gửi.

**1.5 Phương pháp / Methodology**
Gộp nhiều dataset công khai → chuẩn hóa, khử trùng lặp, kiểm soát rò rỉ → TF-IDF + tokenizer transformer → huấn luyện & đánh giá đa chỉ số (StratifiedKFold k=3, bootstrap CI 95%, McNemar's Test) → SHAP + LIME + nhất quán → bias audit + thí nghiệm đối kháng.

**1.6 Cấu trúc khóa luận / Structure**
5 chương: Introduction; Background & Related Work; Design & Implementation; Results & Evaluation; Conclusion & Future Work.

---

## CHƯƠNG 2. CƠ SỞ LÝ THUYẾT & NGHIÊN CỨU LIÊN QUAN / BACKGROUND & RELATED WORK
- **2.1** Phát hiện phishing: từ heuristic/blocklist → đặc trưng cấu trúc + RF → đa mô hình ML → BERT.
- **2.2** Biểu diễn đặc trưng: TF-IDF vs. word embeddings vs. transformer ngữ cảnh.
- **2.3** XAI: SHAP, LIME, diễn giải hậu kiểm (Shapley values; xấp xỉ cục bộ).
- **2.4** Thiên lệch dữ liệu & tính bền vững đối kháng trong ML bảo mật (shortcut learning, artifact, leakage).
- **2.5** Các dataset/benchmark phishing hiện có (CEAS, Nazario, SpamAssassin, Enron, Nigerian Fraud, Ling, TREC; MeAJOR; Champa 11-datasets).
- **2.6** Khoảng trống: chưa có khung kết hợp đa nguồn + ML/transformer + diễn giải hai cấp có định lượng + bias audit + đối kháng thực nghiệm.

## CHƯƠNG 3. THIẾT KẾ HỆ THỐNG & TRIỂN KHAI / DESIGN & IMPLEMENTATION
- **3.1** Xây dựng corpus đa nguồn (thu thập → hợp nhất/làm sạch → chia tập kiểm soát rò rỉ).
- **3.2** Tiền xử lý & trích đặc trưng (clean HTML, URL/email→token, TF-IDF 1–2 gram; tokenizer transformer).
- **3.3** Kiến trúc & huấn luyện (5 ML trong Pipeline; fine-tune BERT/DistilBERT/RoBERTa, AdamW, early stopping).
- **3.4** Khung diễn giải hai cấp (SHAP toàn cục + LIME cục bộ + nhất quán Pearson/Spearman/Jaccard).
- **3.5** Bias-audit & đối kháng (phân loại đặc trưng thực/artifact; char-sub, keyword injection, HTML obfuscation).

## CHƯƠNG 4. KẾT QUẢ & ĐÁNH GIÁ / RESULTS & EVALUATION
- **4.1** So sánh hiệu năng 8 mô hình (Acc/Prec/Rec/F1/AUC + CI 95% + McNemar) — RQ1, RQ2.
- **4.2** Nhất quán SHAP–LIME (toàn cục vs. cục bộ; đặc trưng giao nhau) — RQ2.
- **4.3** Bias audit (tỷ lệ artifact: đơn nguồn vs. đa nguồn; error analysis 30 mẫu) — RQ3.
- **4.4** Tính bền vững đối kháng (sụt F1 TF-IDF vs. transformer dưới 3 lớp tấn công) — RQ4.
- **4.5** Ứng dụng bảo mật (CIA Triad), vai trò LIME trong SOC, GDPR Art. 22, vòng phản hồi.

## CHƯƠNG 5. KẾT LUẬN & HƯỚNG PHÁT TRIỂN / CONCLUSION & FUTURE WORK
- Đóng góp: corpus đa nguồn; so sánh ML vs. transformer có kiểm định; khung SHAP–LIME định lượng; bias audit đơn/đa nguồn; đánh giá đối kháng (CIA Triad).
- Hạn chế: chỉ nội dung văn bản; LIME giới hạn cỡ mẫu; đối kháng là mô phỏng có kiểm soát.
- Hướng tiếp: tín hiệu header/URL/đồ thị; adversarial training; triển khai thời gian thực (MTA); mở rộng đa ngôn ngữ (gồm tiếng Việt).
