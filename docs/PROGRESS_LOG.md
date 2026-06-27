# PROGRESS & CONTEXT LOG

> File theo dõi context + công việc đã làm qua từng tuần. Đọc file này đầu mỗi phiên để nắm nhanh.
> Cập nhật lần cuối: Tuần 6 (adversarial robustness thật; transformer-robustness chờ GPU).

## 0. BẢN ĐỒ FILE (đọc để tiếp tục ở phiên/chế độ mới)
- **Đề cương đầy đủ:** `docs/DeCuong_KhoaLuan.md` (5 chương + kế hoạch tuần).
- **Mẫu báo cáo tuần GVHD:** `docs/REPORT_TEMPLATE.md` (cấu trúc chính xác để tái tạo).
- **Báo cáo .docx đã nộp:** `reports/` (đề cương + Tuần 1/2/3) — dùng làm mẫu định dạng.
- **Code generate báo cáo:** `build_baocao_tuan3.js` (copy để làm báo cáo tuần sau).
- **Kết quả thật:** `results/tables/*.json` (metrics 5 ML), `results/figures/*.png` (12 hình).
- **Tài liệu chương:** `docs/{source_descriptions,data_quality,corpus_statistics,week3_results,research_questions,dataset_survey}.md`.
- **Tái tạo data/model:** `python src/data/build_corpus.py` → `python src/models/run_classical.py`.
- → Tóm lại: **chỉ cần đưa nguyên repo này** là phiên mới có đủ đề cương, mẫu báo cáo, code và kết quả.

---

## 1. Tổng quan dự án
- **Loại:** Khóa luận tốt nghiệp UEH, mở rộng từ **paper hội thảo đã được accept** ("An Explainable AI Framework for Phishing Email Detection Using SHAP and LIME").
- **Đề tài (mở rộng):** Trustworthy Phishing Email Detection — Multi-Source Dataset + SHAP–LIME + Adversarial Robustness.
- **GVHD:** TS. Nguyễn Quốc Hưng (hungngq@ueh.edu.vn).
- **Sinh viên:** *chưa chốt tên* — đề cương ghi "Lê Quốc Bảo" (theo file mẫu), nhưng paper đứng tên **Khai Nhi Thieu**. ❓ Cần xác nhận.

## 2. Paper gốc (số liệu THẬT, dùng được ngay cho chương kết quả phần đã làm)
- 5 ML cổ điển trên TF-IDF; **Linear SVM tốt nhất: F1 = 0.9936, AUC-ROC = 0.9981, Acc = 0.9932**.
- Confusion matrix SVM: TP=3113, TN=2702, FP=21 (~0.77%), FN=19 (~0.61%).
- Dataset gốc: CEAS (~32,699 email; 47.7% phishing / 52.3% legit) từ Kaggle (Naser Abdullah Alam).
- Nhất quán SHAP–LIME: **Pearson r = 0.556; Spearman ρ = 0.300 (p=0.624); Jaccard = 16.7%**; 5 đặc trưng giao nhau (urltoken, men, health, watches, love) — đều là artifact.
- **Phát hiện chính:** 80% (16/20) top-20 SHAP features là artifact theo dataset, 0 là dấu hiệu phishing kinh điển → động lực mở rộng đa nguồn.

## 3. Hướng mở rộng đã chốt (so với paper)
1. **Đa nguồn** thay vì chỉ CEAS → giảm bias.
2. Thêm **transformer** (BERT/DistilBERT/RoBERTa) cạnh 5 ML cổ điển.
3. **Diễn giải hai cấp SHAP–LIME** + định lượng nhất quán.
4. **Đánh giá đối kháng thực nghiệm** + bias audit + CIA Triad.

→ 4 RQ: RQ1 tổng quát hóa (đơn→đa nguồn); RQ2 nhất quán SHAP–LIME; RQ3 phishing thực vs. artifact; RQ4 robustness TF-IDF vs. transformer.

## 4. Thỏa thuận làm việc (QUAN TRỌNG — giữ nhất quán)
- ✅ Khóa luận viết **100% tiếng Anh**, học thuật tự nhiên (mục tiêu AI-detect thấp; **không cam kết con số cụ thể**).
- ✅ **KHÔNG hallucination số liệu.** Chương cần code → chỉ ghi **kết quả chạy thật** (từ paper hoặc thí nghiệm ta chạy).
- ✅ Viết **lần lượt từng chương để duyệt** (không viết ồ ạt một mạch).
- ✅ **Chỉ viết khi sinh viên ra hiệu lệnh** ("viết Chương X"). Không tự động viết.
- 🎯 Mục tiêu độ dài: **≥ 70 trang**.

## 5. Giới hạn môi trường (đã test thật)
- ✅ Cài thư viện Python (pypi OK).
- ❌ **Không tải được Kaggle & HuggingFace** (403) → pretrained model phải lấy ngoài sandbox.
- ✅ **CẬP NHẬT (Tuần 2): lấy được DATA THẬT qua GitHub mirror** `rokibulroni/Phishing-Email-Dataset` (raw.githubusercontent.com truy cập được). 6 CSV đã tải, đã chạy pipeline thật → KHÔNG cần upload data thủ công nữa.
- ❌ **Không có GPU** → fine-tune transformer phải chạy **Colab/Kaggle**, rồi paste output về cho tôi viết.
- ➡️ Chạy ĐƯỢC tại đây: gộp corpus + ML cổ điển + SHAP/LIME + bias audit + đối kháng (tất cả trên data thật).

## 6. Dataset đã chọn (Tuần 1)
6 nguồn schema-tương thích (cùng bộ tổng hợp Kaggle với CEAS): **CEAS, Nazario, Nigerian Fraud, SpamAssassin, Enron, Ling** → ~82,500 email. TREC để dành (ablation tùy chọn). Chi tiết: `docs/dataset_survey.md`.

## 7. Repo & artifacts
- Repo: `phishing-xai-thesis/` (git đã init; sinh viên ĐÃ đẩy lên GitHub).
- Code chạy thật đã có: `features/preprocess.py`, `robustness/adversarial.py`, `explain/consistency.py`, `evaluation/metrics.py`.
- Scaffold (chưa chạy): `models/train_classical.py`, `models/train_transformer.py` (GPU), `explain/shap_global.py`, `explain/lime_local.py`.

---

## 8. NHẬT KÝ THEO TUẦN

### Tuần 1 — ✅ HOÀN THÀNH
**Việc theo đề cương:** chốt hướng + 4 RQ · khảo sát & chọn dataset · dựng môi trường + repo.
**Đã làm:**
- Chốt hướng mở rộng + 4 RQ → `docs/research_questions.md`.
- Khảo sát 7 dataset (số liệu có nguồn), chọn 6 nguồn → `docs/dataset_survey.md`.
- Dựng repo đầy đủ + git init/commit; code thật cho preprocess/adversarial/consistency/metrics (đã test chạy OK).
- Viết email cập nhật GVHD (2 bản: concise/detailed); sinh viên đã gửi link GitHub.
**Deliverables:** `phishing-xai-thesis.zip`, `Week1_Dataset_Survey.md`, `DeCuong_KhoaLuan_Phishing_XAI.docx` (+ bản `.md`).
**Còn treo:** ❓ tên sinh viên; ngôn ngữ email (đang để EN).

### Tuần 2 — ✅ HOÀN THÀNH (data THẬT)
**Việc theo đề cương:** gộp nguồn → corpus đa nguồn → chuẩn hóa schema → khử trùng lặp → cân bằng nhãn → split kiểm soát rò rỉ → thống kê.
**Đã làm (số THẬT):**
- Tải 6 CSV thật từ GitHub mirror; gộp = **82,486** email → sau làm sạch = **82,481** (loại 5 email rỗng body; exact-dedup = 0).
- Cân bằng nhãn cuối: **42,886 phishing (52.0%) / 39,595 legit (48.0%)** → giữ phân bố tự nhiên, không resample.
- Split kiểm soát rò rỉ theo sender-domain (seed 42): **train 67,657 / test 14,824** (~82/18 theo dòng vì group theo domain).
- Per-source label (cho bias audit RQ3): CEAS 21,842/17,312 · Enron 13,976/15,791 · SpamAssassin 1,718/4,091 · Nigerian 3,332/0 · Ling 458/2,401 · Nazario 1,565/0.
- Code mới: `src/data/build_corpus.py`; nâng cấp `split.py` (xử lý nguồn không có sender).
**Deliverables:** `docs/corpus_statistics.md`, `results/figures/corpus_composition.png`, `data/processed/{corpus,train,test}.csv` + `corpus_stats.json`.
**Lưu ý trung thực:** Enron trong bộ này CÓ nhãn spam (không phải legit-only) — cần nhớ khi phân tích bias.

### Tuần 3 — ✅ HOÀN THÀNH (data THẬT) + đã xử lý feedback GVHD
**Feedback Tuần 2 đã bổ sung:** mô tả 6 nguồn (`docs/source_descriptions.md`), sơ đồ pipeline (`data_integration_pipeline.png`), thêm 5 biểu đồ (contribution/label-per-source/length/url/domain), tiêu chí khử trùng lặp + đánh giá chất lượng (`docs/data_quality.md`).
**Việc Tuần 3 (số THẬT):**
- Tiền xử lý nâng cấp: NFKC + HTML + token url/email/phone + chuẩn hóa (`preprocess.py`).
- TF-IDF sweep (LR test F1): 5k=.9763 · 10k=.9765 · 20k=.9792 · 50k=.9795 → chọn **20k**.
- Train 5 ML trên corpus đa nguồn (train 67,657 / test 14,824). Kết quả test:
  **Linear SVM F1=.9826** (Acc .9805, ROC .9983, PR .9985) · LR .9792 · RF .9763 · NB .9632 · DT .9557.
- So sánh với paper (CEAS-only SVM F1=.9936): giảm nhẹ — hợp lý vì eval đa nguồn + kiểm soát rò rỉ khó hơn.
**Deliverables:** `docs/{source_descriptions,data_quality,week3_results}.md`, 12 figure trong `results/figures/`, `models/*.joblib`, `results/tables/*.json`, `BaoCao_KhoaLuan_Tuan3.docx`.
**Data-quality thật:** removal 0.006% · missing sender/date/urls ~40% (do Enron+Ling) · imbalance 1.083 · email legit dài hơn phishing (357 vs 195 từ) · 19,386 domain.

### Tuần 4 — ✅ HOÀN THÀNH phần chạy được tại đây (90%; transformer chờ GPU) + xử lý feedback Tuần 3
**Feedback Tuần 3 đã xử lý (số THẬT):**
- Phân tích NGUYÊN NHÂN: SVM>LR (McNemar p=3.9e-06, biên lớn hơn) · RF/DT thấp (cây kém trên TF-IDF thưa 20k) · NB precision cao/recall thấp (lỗi dồn ở Nazario 21.6%).
- McNemar vs SVM: tất cả p<0.001 (LR 3.9e-6 · RF 4.6e-9 · NB 1.9e-30 · DT 1.1e-51) → SVM vượt trội có ý nghĩa.
- Bootstrap CI 95% F1: SVM [.9806–.9845] · LR [.9769–.9814] · RF [.9740–.9787] · NB [.9603–.9660] · DT [.9524–.9589].
- Error analysis SVM: FP=227 (3.43%) · FN=62 (0.76%); nguồn khó nhất SpamAssassin 4.52%, Nazario 3.79%.
- Pipeline timing+retention: 4 bước, retention 99.99% (`pipeline_timing.json`).
- Calibration curves (5 model) + calibrated SVM đã train.
**XAI (phần thầy nói "quyết định"):**
- SHAP toàn cục SVM: bias DỊCH từ CEAS→Enron (enron/vince/wrote/pm) + vài dấu hiệu thật (click/http).
- LIME cục bộ (35 phishing): nêu dấu hiệu thật (click/account/alert/lose).
- Nhất quán SHAP–LIME: Jaccard 8.1% · Pearson 0.787 · Spearman 0.5 → bổ sung nhau.
**Deliverables:** `docs/week4_analysis.md`, figures (shap_summary, shap_vs_lime, calibration_curves, roc/pr_curves), `results/tables/{error_analysis,shap_top20,lime_analysis,shap_lime_consistency,pipeline_timing}.json`, `BaoCao_KhoaLuan_Tuan4.docx`.
**CHỜ SV:** chạy `src/models/train_transformer.py` trên **Colab/Kaggle (GPU)** → gửi `transformer_metrics.json` về để viết so sánh ML vs transformer.

### Tuần 5 — ✅ Transformer ĐÃ CHẠY (GPU, kết quả thật) + so sánh toàn diện
**Kết quả transformer (test 14,824):** RoBERTa F1=0.9948 (FP=28) · BERT 0.9914 (FP=110) · DistilBERT 0.9895 (FP=135).
**So sánh RQ1:** cả 3 transformer > SVM tốt nhất (0.9826). RoBERTa +0.0122 F1, giảm FP 227→28 (precision .9729→.9966) — thắng lợi lớn nhất là giảm false alarm ~8x.
**Lý do:** TF-IDF bỏ qua ngữ cảnh/thứ tự (dựa artifact); transformer mô hình ngữ nghĩa theo ngữ cảnh.
**Deliverables:** `results/tables/{transformer_metrics,all_models_comparison}.json`, figures (all_models_comparison, f1_ranking, transformer_confusion_matrices), `docs/classical_vs_transformer.md`.
**CHỜ SV (tùy chọn):** chạy `train_transformer_preds.py` (lưu dự đoán từng email) → gửi `transformer_predictions.json` để làm McNemar + bootstrap CI cho transformer.

### Tuần 6 — ✅ Adversarial Robustness (số THẬT, chạy tại đây)
**Threat model:** sửa email phishing để né phát hiện; đo recall phishing sau tấn công.
**3 tấn công × 5 model × mức 5/10/15%:**
- **Keyword injection = lỗ hổng nghiêm trọng:** SVM recall 0.992→0.201 (15%); mọi model TF-IDF sụp mạnh. NB bền nhất (0.724). → đúng cảnh báo của paper + mặt trái của bias (RQ3).
- Char substitution & HTML obfuscation: model tuyến tính BỀN (~0.99); chỉ cây giảm nhẹ.
**Kết luận RQ4 (phía cổ điển):** TF-IDF bền với che giấu bề mặt nhưng RẤT yếu trước "pha loãng ngữ nghĩa".
**Deliverables:** `docs/adversarial_robustness.md`, `results/tables/adversarial.json`, figures (adversarial_robustness, adversarial_drop_15), `src/robustness/run_adversarial.py`.
**CHỜ SV (tùy chọn, hoàn tất RQ4):** chạy `train_transformer_robustness.py` (Colab/GPU) → gửi `transformer_robustness.json` để so sánh độ bền transformer vs TF-IDF (giả thuyết: transformer bền hơn với injection).

### Tuần 6–7 — ⏳ KẾ HOẠCH

---

## 9. NEXT ACTION
- **SV chạy GPU:** `python src/models/train_transformer.py` trên Colab/Kaggle → gửi `transformer_metrics.json`.
- Sau đó: viết so sánh ML vs transformer + McNemar; rồi sang **đối kháng (adversarial robustness)** — chạy được tại đây bằng `robustness/adversarial.py` trên model đã lưu.
- Mở rộng SHAP/LIME (full summary + nhiều case study) cho Chương 4.
- Khi viết: chỉ dùng số THẬT trong `results/tables/*.json`.
