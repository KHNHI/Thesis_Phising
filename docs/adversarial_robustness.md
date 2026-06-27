# Adversarial Robustness Evaluation (RQ4)

Real results from `src/robustness/run_adversarial.py` on the 5 classical models, multi-source test
set. **Threat model:** an attacker modifies *phishing* emails to evade detection (flip phishing →
legitimate). Attacks are applied to the raw email, then the defender's normal pipeline runs
(clean → TF-IDF → model), so only attacks that **survive preprocessing** count. Legitimate emails
are unchanged. Primary metric: **phishing detection rate (recall)** — lower means more evasion.

## 1. Attacks
- **Character substitution** — leetspeak (`verify` → `v3rify`); digits are stripped by the cleaner,
  leaving a broken token (`vrify`) that evades the exact TF-IDF feature.
- **Keyword injection / dilution** — append benign / legitimate-associated tokens
  (`enron, wrote, thanks, meeting, …`, drawn from the SHAP artifact list) to drown the phishing signal.
- **HTML obfuscation** — insert empty inline tags inside words (`ver<b></b>ify`); after HTML
  stripping the word fragments.

## 2. Phishing recall under attack (baseline → 5% → 10% → 15%)

| Model | Baseline | Char-sub 15% | **Injection 5%** | **Injection 10%** | **Injection 15%** | HTML 15% |
|-------|---------:|-------------:|-----------------:|------------------:|------------------:|---------:|
| Linear SVM | 0.9924 | 0.997 | 0.741 | 0.392 | **0.201** | 0.993 |
| Logistic Regression | 0.9901 | 0.997 | 0.794 | 0.553 | 0.398 | 0.993 |
| Random Forest | 0.9801 | 0.934 | 0.542 | 0.373 | 0.291 | 0.978 |
| Naive Bayes | 0.9381 | 0.981 | 0.850 | 0.784 | **0.724** | 0.965 |
| Decision Tree | 0.9543 | 0.904 | 0.376 | 0.228 | 0.175 | 0.887 |

## 3. Key findings
1. **Keyword injection is a severe vulnerability.** At only 15% added tokens, Linear SVM's phishing
   recall collapses from **0.992 to 0.201** — i.e., ~80% of phishing slips through. All TF-IDF
   models degrade sharply. This is the direct, empirical confirmation of the conference paper's
   warning and is the flip side of the bias finding (RQ3): because the models key on aggregate
   lexical frequency (including corpus artifacts), flooding an email with opposite-class vocabulary
   overrides the decision.
2. **Character substitution and HTML obfuscation barely dent the linear models** (SVM/LR stay
   ≈0.99). Surviving tokens plus bigrams retain enough signal, and HTML stripping neutralizes tag
   obfuscation. Tree models (RF/DT) are somewhat more affected.
3. **Naive Bayes is the most injection-robust** (0.724 at 15%) thanks to its feature-independence
   assumption — added benign tokens cannot easily cancel strong phishing tokens — although its
   baseline recall is the lowest.
4. **Decision Tree is the most fragile overall.**

## 4. Security interpretation (CIA Triad)
The injection attack threatens **Availability/Integrity** of the filter: a trivial, content-only
manipulation (no infrastructure needed) defeats a 98%+ F1 detector. For a production Mail Transfer
Agent filter this is critical — it means a TF-IDF + SVM stage must not be used alone.

## 5. Toward RQ4 conclusion & transformers
Classical TF-IDF detectors are **robust to surface obfuscation but critically vulnerable to
semantic dilution**. The hypothesis is that **contextual transformers resist injection far better**,
because they model meaning in context rather than bag-of-words frequency. `train_transformer_robustness.py`
(Colab/GPU) fine-tunes a transformer and runs the **same three attacks**, producing
`transformer_robustness.json` to complete the TF-IDF-vs-transformer robustness comparison.

## 6. Limitations
Attacks are controlled simulations at fixed strengths, not adaptive/optimization-based attacks; a
single defender pipeline is tested; transformer robustness is pending the GPU run. Adversarial
training as a defense is left for future work.

*Figures:* `adversarial_robustness.png` (recall vs. attack strength), `adversarial_drop_15.png`.
