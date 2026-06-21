# Data Quality Assessment (post-integration)

Addresses supervisor feedback: deduplication criteria, removal rate, missingness, label imbalance,
and sender-domain distribution. All numbers are produced by `src/data/eda.py` on the merged corpus.

## 1. Deduplication criteria
Duplicates are identified by an **exact match on the combined (subject, body) text** after
normalization. This content-based key is used because four of the six sources carry no
`Message-ID` field (Enron and Ling expose only subject/body/label), so a header-based key is not
uniformly available. Result: **0 exact duplicates** were found across the curated sources.
*Limitation / next step:* exact matching does not catch near-duplicates (minor formatting or
quoting differences); fuzzy near-duplicate detection (e.g., MinHash/SimHash) is noted as an
optional Week-3+ refinement.

## 2. Removal rate
| Stage | Rows | Removed |
|-------|-----:|--------:|
| Raw merged | 82,486 | — |
| Empty-body removal | 82,481 | 5 (0.006%) |
| Exact dedup | 82,481 | 0 |
| **Final** | **82,481** | **5 total (0.006%)** |

The removal rate is negligible, indicating the curated sources were already clean.

## 3. Missing-data profile
| Field | Missing % | Reason |
|-------|----------:|--------|
| sender | 40.0% | Enron + Ling carry no sender field |
| receiver | 42.1% | same (and some sources omit receiver) |
| date | 40.1% | Enron + Ling carry no date |
| urls | 39.6% | Enron + Ling carry no urls field |
| subject | 0.4% | a few empty subjects |
| body | 0.0% | none (empty bodies were dropped) |

Missingness is **structural** (driven by the two minimal-schema sources), not random. Text fields
needed for modelling (subject, body) are essentially complete.

## 4. Label balance
Final corpus: **42,886 phishing (52.0%) / 39,595 legitimate (48.0%)** →
**majority:minority ratio = 1.083**. This is only mildly imbalanced, so no resampling is applied;
the natural distribution is kept (consistent with the conference paper).

## 5. Email-length distribution (words)
- Overall: mean 273, median 130, p95 846, max 127,119.
- **By class:** legitimate mean = 357.0 words vs. phishing mean = 195.4 words — legitimate emails
  are, on average, longer. This is a genuine signal worth noting for the explainability analysis.

## 6. URL-count distribution
- 49,705 emails (60.3%) contain **no** URL; 32,776 (39.7%) contain at least one.
- Mean URLs per email = 1.93; maximum = 3,133 (a marketing/spam outlier).
- URL presence is informative but not exclusive to phishing (consistent with the prior finding
  that the `urltoken` feature was the single most influential — and partly artifactual — signal).

## 7. Sender-domain distribution
- 49,524 rows carry a sender; **19,386 unique domains**.
- Top domains: gmail.com (2,661), hotmail.com (726), spamassassin.taint.org (648), yahoo.com (627),
  python.org (560). The presence of `python.org` / `spamassassin.taint.org` reflects the
  tech-mailing-list provenance that the prior SHAP audit flagged as a bias source.
- The large number of unique domains is what makes the **sender-domain GroupShuffleSplit**
  meaningful: train and test share no sender domain, preventing optimistic leakage.

*Figures:* `dataset_contribution.png`, `phishing_rate_per_source.png`, `email_length_distribution.png`,
`url_count_distribution.png`, `sender_domain_top15.png`, `data_integration_pipeline.png`.
