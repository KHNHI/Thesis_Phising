# Classical ML vs. Transformers — Comprehensive Comparison (RQ1)

Real results on the **same** multi-source, leakage-controlled test set (N = 14,824). Classical
metrics from `classical_metrics.json`; transformer metrics from the Colab GPU run
(`transformer_metrics.json`). Same split (seed 42) → directly comparable.

## 1. Full comparison (8 models, ranked by F1)

| Rank | Model | Type | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC | FP | FN |
|---:|-------|------|---------:|----------:|-------:|---:|--------:|-------:|---:|---:|
| 1 | **RoBERTa** | Transformer | 0.9943 | 0.9966 | 0.9931 | **0.9948** | 0.9996 | 0.9997 | 28 | 57 |
| 2 | BERT | Transformer | 0.9904 | 0.9867 | 0.9961 | 0.9914 | 0.9996 | 0.9995 | 110 | 32 |
| 3 | DistilBERT | Transformer | 0.9883 | 0.9837 | 0.9954 | 0.9895 | 0.9995 | 0.9996 | 135 | 38 |
| 4 | Linear SVM | Classical | 0.9805 | 0.9729 | 0.9924 | 0.9826 | 0.9983 | 0.9985 | 227 | 62 |
| 5 | Logistic Regression | Classical | 0.9767 | 0.9684 | 0.9901 | 0.9792 | 0.9973 | 0.9978 | — | — |
| 6 | Random Forest | Classical | 0.9737 | 0.9726 | 0.9801 | 0.9763 | 0.9968 | 0.9971 | — | — |
| 7 | Naive Bayes | Classical | 0.9603 | 0.9897 | 0.9381 | 0.9632 | 0.9965 | 0.9972 | — | — |
| 8 | Decision Tree | Classical | 0.9510 | 0.9571 | 0.9543 | 0.9557 | 0.9516 | 0.9402 | — | — |

## 2. Key findings (RQ1)
- **All three transformers beat the best classical model.** RoBERTa improves F1 from 0.9826
  (Linear SVM) to **0.9948 (+0.0122)**.
- **The biggest practical gain is in false positives.** Linear SVM flags **227** legitimate
  emails as phishing; RoBERTa flags only **28** (precision 0.9729 → **0.9966**). For a real email
  filter, an ~8× reduction in false alarms is the most operationally meaningful improvement.
- **Why:** TF-IDF treats words independently and ignores order/context, so it leans on lexical
  artifacts (Chapter 4 SHAP analysis showed Enron/CEAS corpus tokens). Contextual transformers
  model word meaning in context, which is exactly what separates a genuine "verify your account"
  phishing line from the same words in a legitimate message.
- **Efficiency note:** DistilBERT (F1 = 0.9895) trails BERT by only 0.0019 while being ~40%
  smaller/faster — a strong accuracy/efficiency trade-off for deployment.
- **Honest caveat:** transformers require a GPU and are far heavier than the TF-IDF + SVM pipeline.
  The classical models remain a strong, cheap, CPU-only baseline; the thesis argues the transformer
  gain (especially the false-positive reduction) justifies the cost for a trustworthy filter.

## 3. Statistical tests — status
- **Classical models:** McNemar vs. SVM and bootstrap 95% CIs already computed (see
  `error_analysis.json` / Week-4 report). SVM significantly best among classical (all p < 0.001).
- **Transformers (pending):** McNemar (transformer vs. SVM) and bootstrap CIs require the
  transformers' **per-email predictions**, which the first Colab run did not save (only confusion
  matrices). The updated script `train_transformer_preds.py` saves
  `transformer_predictions.json`; one more run lets us complete the paired tests and finish the
  full statistical comparison.

*Figures:* `all_models_comparison.png`, `f1_ranking.png`, `transformer_confusion_matrices.png`.
