# Week 4 — Analysis, Statistical Tests, Error Analysis, and Explainability

All numbers are real outputs of `src/models/stats_error.py` and the SHAP/LIME runs on the
multi-source corpus (test = 14,824). Addresses the supervisor's Week-3 feedback.

## 1. Why the models rank as they do (not just metrics)

**Bootstrap 95% CI for F1** (1,000 resamples):

| Model | F1 | 95% CI |
|-------|---:|--------|
| Linear SVM | 0.9826 | [0.9806, 0.9845] |
| Logistic Regression | 0.9792 | [0.9769, 0.9814] |
| Random Forest | 0.9764 | [0.9740, 0.9787] |
| Naive Bayes | 0.9633 | [0.9603, 0.9660] |
| Decision Tree | 0.9557 | [0.9524, 0.9589] |

**McNemar's test vs. Linear SVM** (all differences significant):

| vs. SVM | statistic | p-value | SVM-only correct | other-only correct |
|---------|----------:|--------:|-----------------:|-------------------:|
| Logistic Regression | 21.3 | 3.9e-06 | 102 | 45 |
| Random Forest | 34.4 | 4.6e-09 | 196 | 95 |
| Naive Bayes | 131.6 | 1.9e-30 | 487 | 188 |
| Decision Tree | 228.8 | 1.1e-51 | 634 | 197 |

- **SVM > Logistic Regression:** both are linear models on the same TF-IDF space, but SVM maximizes
  the margin, which generalizes better on sparse, high-dimensional (20k) text. The advantage is
  small but **statistically significant** (p = 3.9e-06); SVM is uniquely correct on 102 test emails
  vs. LR's 45.
- **Random Forest & Decision Tree lower:** tree models split on one feature at a time, which is
  inefficient when the phishing signal is spread across thousands of sparse TF-IDF terms. A single
  Decision Tree overfits and is weakest; Random Forest recovers some ground through averaging but
  still trails the linear models. Their weakness is clearest on the minority sources (DT error:
  Ling 9.1%, Nigerian Fraud 6.3%).
- **Naive Bayes — high precision, low recall:** its errors concentrate on **Nazario (21.6% error)**,
  which is real, in-the-wild phishing. The feature-independence assumption makes NB conservative:
  it labels an email phishing only on strong lexical evidence, so when it does, it is almost always
  right (precision 0.990) but it misses subtler phishing (recall 0.938).

## 2. Error analysis (Linear SVM)
- **False Positives = 227 (3.43% of legitimate)**, **False Negatives = 62 (0.76% of phishing).**
  The model errs toward over-flagging legitimate mail rather than missing phishing — the safer
  failure mode for a security filter.
- **Length of errors:** FP mean 245.8 words, FN mean 191.9 words, correct 232.4 — false negatives
  (missed phishing) tend to be shorter, giving the model less lexical evidence.
- **Hardest sources (SVM error rate):** SpamAssassin 4.52%, Nazario 3.79%, CEAS 2.41%, then
  Ling 1.25%, Enron 1.16%, Nigerian Fraud 0.00%. The model struggles most where legitimate and
  spam vocabulary overlap (SpamAssassin) and on authentic phishing (Nazario); it is perfect on the
  stylistically distinctive Nigerian-fraud emails.

## 3. Data Integration Pipeline — timing & retention (per supervisor request)

| Step | Rows after | Removed | Time |
|------|-----------:|--------:|-----:|
| 1. Load + merge | 82,486 | 0 | 2.38 s |
| 2. Drop empty bodies | 82,481 | 5 | 0.39 s |
| 3. Exact dedup | 82,481 | 0 | 0.36 s |
| 4. Leakage-controlled split | 82,481 | 0 | 0.17 s |

**Overall retention = 99.99%** (train 67,657 / test 14,824). The pipeline is fast and near-lossless.

## 4. Explainability — first pass (the decisive contribution)

**SHAP (global, Linear SVM) — top features:** `enron, wrote, vince, thanks, click, urltoken, life,
university, http, pm …`. **Honest finding:** the bias the conference paper found on CEAS
(*python, opensuse*) has **shifted, not disappeared** — global importance is now dominated by
**Enron-corpus artifacts** (`enron`, `vince`, `wrote`, `pm`). A few genuine phishing cues
(`click`, `http`, `urltoken`) do appear. This is strong evidence that multi-source construction
**reduces single-corpus dependence but does not by itself remove artifact reliance** (RQ3).

**LIME (local, aggregated over 35 phishing emails) — top features:** `custom, click, account,
alert, lose, love, cnn, girl, man …`. LIME's instance-level view surfaces **more genuine
social-engineering triggers** (`click`, `account`, `alert`, `lose`) than the global SHAP view.

**SHAP–LIME consistency:** overlap = 3 features (`click, life, love`), **Jaccard = 8.1%**,
**Pearson = 0.787**, Spearman = 0.50 (p = 0.67). Low overlap confirms the two methods are
**complementary** — SHAP captures corpus-level patterns, LIME captures email-specific phishing
cues — echoing and extending the conference paper's consistency result on the new corpus.

*Figures:* `calibration_curves.png`, `shap_summary.png`, `shap_vs_lime.png`,
`roc_curves.png`, `pr_curves.png`, `confusion_matrices.png`.

## 5. Transformer step (prepared, pending GPU)
`src/models/train_transformer.py` is a complete, runnable script to fine-tune BERT, DistilBERT, and
RoBERTa on the **same split and metrics**. It must run on Colab/Kaggle (GPU + HuggingFace), then the
resulting `transformer_metrics.json` is written into Chapter 4 for the classical-vs-transformer
comparison (RQ1) and McNemar tests against the SVM.
