# Dataset Survey & Selection — Week 1

**Goal.** Select public, license-compatible email datasets to build a *multi-source* phishing
corpus that mitigates the single-source (CEAS-only) bias diagnosed in the accepted conference
paper, where 80% of the top-20 SHAP features were CEAS-specific artifacts rather than genuine
phishing indicators.

## 1. Candidate datasets surveyed

| # | Dataset | Type | Reported size | Notes / source |
|---|---------|------|---------------|----------------|
| 1 | **CEAS-08** | spam/phishing challenge corpus | ~39,154 (≈32,699 after cleaning, used in our paper: 47.7% phishing / 52.3% legit) | 2008 CEAS spam challenge; baseline source of current work |
| 2 | **Nazario** | phishing-only | 4,558 (some releases 4,555 / 11,527) | Hand-screened phishing from J. Nazario's inbox; spans multiple years |
| 3 | **Nigerian Fraud (CLAIR)** | phishing-only (financial fraud) | 3,975 | CLAIR "419" fraudulent-email corpus |
| 4 | **SpamAssassin** | ham + spam | 6,047 (≈31% spam) | Classic, source-diverse legitimate + spam |
| 5 | **Enron** | legitimate (ham) | ~517,401 full corpus | Only large real-world corporate email set; subset used as ham |
| 6 | **Ling-Spam** | academic mailing list (ham + spam) | 2,893 | Linguistics mailing-list corpus |
| 7 | **TREC-05 / 06 / 07** | spam benchmark | 92,189 / 37,822 / 75,419 | Large standardized spam-filtering corpora (optional) |

*Figures are as reported across published sources and the Kaggle aggregation; exact counts vary
by release and by cleaning. They will be re-verified against the downloaded files in Week 2 and
reported with the final corpus statistics.*

## 2. Selection decision

**Selected:** CEAS-08, Nazario, Nigerian Fraud, SpamAssassin, Enron, Ling.

Rationale:
- All six are available as a **single, schema-consistent Kaggle aggregation**
  ("Phishing Email Dataset", Naser Abdullah Alam; companion paper Al-Subaiey et al., 2024,
  arXiv:2405.11619). Because our prior paper already drew CEAS from this collection, the other
  five integrate with **no schema mismatch** (sender, receiver, date, subject, body, urls, label).
- Combined size ≈ **82,500 emails** (≈42,891 phishing / ≈39,595 legitimate) — large and roughly
  balanced, matching the ~50–80k target in the proposal.
- The mix spans **phishing-only** (Nazario, Nigerian Fraud), **spam/ham** (SpamAssassin, Ling),
  and **real-world legitimate** (Enron) — exactly the source diversity needed to test whether the
  classifier learns *genuine* phishing signals rather than corpus artifacts (RQ3).

**Deferred (optional):** TREC-05/06/07 — very large and spam-centric; may be added later for a
scale/robustness ablation if compute allows.

**Cross-checks for the related-work section:**
- Champa, Rabbi & Zibran — "Phishing Email: 11 Curated Datasets" (figshare; already cited as
  ref [9] in our paper).
- *MeAJOR Corpus: A Multi-Source Dataset for Phishing Email Detection* (arXiv:2507.17978) — recent
  multi-source effort to position against.

## 3. Risks & how they are handled
- **Label semantics differ** (some sources label *spam*, not strictly *phishing*) → keep a
  `source` provenance tag on every row; report results per-source; bias-audit compares
  single- vs. multi-source (RQ3).
- **Sender-domain leakage** → split with `GroupShuffleSplit` by sender domain (already in
  `src/data/split.py`).
- **Duplication across sources** → near-duplicate removal in `src/data/merge_sources.py`.
- **Recency** (Enron/SpamAssassin are early-2000s) → acknowledged as a limitation; Nazario adds
  more recent phishing.

## 4. Status
Survey complete; sources identified and access route confirmed. **Download + verification of exact
counts is the Week-2 task** (sandbox cannot fetch from Kaggle/HuggingFace; data will be pulled on
Colab/locally and placed in `data/raw/`).
