# Research Questions & Scope (finalized — Week 1)

**Expansion direction.** The accepted conference paper showed that a high-accuracy
TF-IDF + Linear SVM phishing detector (F1 = 0.9936) relied largely on CEAS-specific
artifacts (80% of top-20 SHAP features). The thesis extends this from a *diagnosis on one
dataset* to a *trustworthy, generalizable framework* by adding (a) a multi-source corpus,
(b) transformer models, and (c) empirical adversarial-robustness evaluation.

- **RQ1 — Generalization.** Moving from single-source (CEAS) to a multi-source corpus, how
  does detection performance of classical ML and transformer models change, and does
  generalization improve?
- **RQ2 — Explanation consistency.** How consistent are global (SHAP) and local (LIME)
  explanations (Pearson, Spearman, Jaccard), and do they agree on what drives detection?
- **RQ3 — Genuine signal vs. bias.** To what extent are decisions driven by genuine phishing
  indicators vs. dataset artifacts, and does multi-source construction reduce this bias?
- **RQ4 — Adversarial robustness.** How robust are TF-IDF vs. transformer detectors against
  character substitution, keyword injection/dilution, and HTML obfuscation?

**Scope.** Content-based detection on English email text; explanation, bias audit, and
adversarial analysis at the lexical/feature level. Out of scope: header forensics, sender-graph
analysis, non-English email.
