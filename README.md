# An Explainable AI Framework for Trustworthy Phishing Email Detection

Multi-Source Dataset Construction, SHAP–LIME Interpretability, and Adversarial Robustness.

Graduation thesis (UEH). Extends the accepted conference paper
*"An Explainable AI Framework for Phishing Email Detection Using SHAP and LIME"*.

## Research questions
- **RQ1** Moving from a single source (CEAS) to a multi-source corpus, how does detection
  performance of classical ML and transformer models change, and does generalization improve?
- **RQ2** How consistent are global (SHAP) and local (LIME) explanations?
- **RQ3** Are decisions driven by genuine phishing indicators or dataset artifacts, and does
  multi-source construction reduce this bias?
- **RQ4** How robust are TF-IDF vs. transformer detectors against adversarial manipulations?

## Pipeline
1. `src/data`        – load each public dataset, merge into a multi-source corpus (provenance kept)
2. `src/features`    – text cleaning, URL/email tokenization, TF-IDF
3. `src/models`      – classical ML (sklearn) + transformer fine-tuning (run on GPU)
4. `src/explain`     – SHAP (global) + LIME (local) + SHAP–LIME consistency metrics
5. `src/robustness`  – adversarial perturbations (char-substitution, keyword injection, HTML obfuscation)
6. `src/evaluation`  – Accuracy/Precision/Recall/F1/AUC, 95% bootstrap CI, McNemar's test

## Environment
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
Classical-ML + XAI + robustness run on CPU. Transformer fine-tuning requires a GPU
(Google Colab / Kaggle) and downloads pretrained weights from HuggingFace.

## Data
Datasets are NOT committed (see `.gitignore`). Download instructions: `data/README.md`.

## Reproducibility
Global seed `42`; configuration in `config/config.yaml`.
