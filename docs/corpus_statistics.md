# Multi-Source Corpus — Statistics (Week 2)

**Pipeline:** load 6 sources → normalize to common schema (+`source` tag) → drop empty bodies →
deduplicate on (subject, body) → leakage-controlled split (GroupShuffleSplit by sender domain, seed 42).
Produced by `src/data/build_corpus.py`. All numbers below are **actual outputs** of the run.

## 1. Per-source composition

| Source | Rows | Phishing/Spam (1) | Legitimate (0) | Note |
|--------|-----:|------------------:|---------------:|------|
| CEAS-08 | 39,154 | 21,842 | 17,312 | spam-challenge corpus (full metadata) |
| Enron | 29,767 | 13,976 | 15,791 | this aggregation includes spam-labelled rows (not legitimate-only) |
| SpamAssassin | 5,809 | 1,718 | 4,091 | ~30% spam |
| Nigerian Fraud | 3,332 | 3,332 | 0 | phishing-only (419 fraud) |
| Ling | 2,859 | 458 | 2,401 | academic mailing-list corpus |
| Nazario | 1,565 | 1,565 | 0 | phishing-only |
| **Total** | **82,486** | **42,891** | **39,595** | before cleaning |

*Schema note:* CEAS, Nazario, Nigerian Fraud, SpamAssassin carry the full schema
(`sender, receiver, date, subject, body, urls, label`); Enron and Ling carry only
(`subject, body, label`). Missing fields are normalized to null and tagged with `source`.

## 2. Cleaning & final corpus

| Step | Rows |
|------|-----:|
| Merged | 82,486 |
| After dropping empty bodies | 82,481 (−5) |
| After exact (subject, body) dedup | 82,481 (−0) |
| **Final corpus** | **82,481** |

Final label balance: **42,886 phishing (52.0%) / 39,595 legitimate (48.0%)** — already near-balanced,
so no resampling is applied; natural distribution is kept (consistent with the conference paper).

*Honest notes:* (a) exact (subject, body) duplicate matching removed none across these curated
sources; fuzzy/near-duplicate detection is a possible Week-3 refinement. (b) The final phishing
count (42,886) is 5 fewer than the commonly cited 42,891 because of the empty-body rows dropped here.

## 3. Leakage-controlled split (by sender domain)

| Split | Rows | Phishing (1) | Legitimate (0) |
|-------|-----:|-------------:|---------------:|
| Train | 67,657 | 34,680 | 32,977 |
| Test | 14,824 | 8,206 | 6,618 |

The split is ~82% / 18% by **rows** (not exactly 80/20) because `GroupShuffleSplit` partitions by
**sender domain**, so no domain appears in both train and test. Rows without a sender (Enron, Ling)
receive a unique per-row group so they distribute normally rather than collapsing into one split.

## 4. Relevance to the research questions
- **RQ1/RQ3:** the source mix is deliberately heterogeneous — phishing-only (Nazario, Nigerian
  Fraud), spam/ham (SpamAssassin, Ling), and a large mixed corpus (Enron, CEAS). The `source` tag
  enables a single- vs. multi-source bias comparison and per-source error breakdown.
- The leakage-controlled split prevents the optimistic bias of sender-domain leakage that inflates
  single-corpus results.

*Figure:* `results/figures/corpus_composition.png` (stacked bar by source and label).
