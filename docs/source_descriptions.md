# Source Descriptions & Selection Rationale

Detailed characterization of each of the six public sources merged into the corpus
(addresses supervisor feedback: collection period, data characteristics, selection rationale).
Collection periods reflect the commonly documented windows for each corpus and will be cited
in the thesis; exact windows vary slightly across releases.

## CEAS-08 — 39,154 emails (21,842 phishing / 17,312 legitimate)
- **Origin / period:** Corpus from the 2008 Conference on Email and Anti-Spam (CEAS) live spam
  challenge.
- **Characteristics:** Full metadata (sender, receiver, date, subject, body, urls, label); rich
  HTML bodies; mixes legitimate technical-mailing-list traffic with spam/phishing.
- **Why selected:** It is the source used in the accepted conference paper; keeping it lets us
  measure the single-source → multi-source effect directly, and it is the corpus whose artifacts
  (e.g., "python", "opensuse") the prior SHAP audit flagged.

## Enron — 29,767 emails (13,976 "phishing/spam" / 15,791 legitimate)
- **Origin / period:** Real corporate email from Enron Corporation (messages ~1998–2002), publicly
  released during the FERC investigation (~2004); the full corpus is ~517k messages.
- **Characteristics:** Minimal schema here (subject, body, label); genuine business correspondence.
- **Why selected:** Provides large-scale, real-world *legitimate* email, balancing the
  phishing-heavy sources. **Honest note:** in this aggregation Enron also carries spam-labelled
  rows, so it is not purely legitimate — relevant for the bias audit (RQ3).

## SpamAssassin — 5,809 emails (1,718 spam / 4,091 legitimate)
- **Origin / period:** Apache SpamAssassin public corpus (assembled ~2002–2006).
- **Characteristics:** Full schema; ~30% spam; widely used ham/spam benchmark with diverse
  legitimate mail.
- **Why selected:** A well-established, source-diverse legitimate + spam reference that broadens
  the legitimate distribution beyond corporate email.

## Nigerian Fraud — 3,332 emails (3,332 phishing / 0 legitimate)
- **Origin / period:** CLAIR "419" advance-fee fraud collection (~1998–2007).
- **Characteristics:** Full schema; long narrative social-engineering bodies; phishing-only.
- **Why selected:** Represents financial-fraud phishing with a distinct linguistic style, testing
  whether models learn genuine social-engineering cues vs. corpus artifacts.

## Ling — 2,859 emails (458 spam / 2,401 legitimate)
- **Origin / period:** Ling-Spam corpus (~2000), from a linguistics profession mailing list.
- **Characteristics:** Minimal schema (subject, body, label); clean academic discussion + spam.
- **Why selected:** Adds a topically narrow legitimate domain, useful for probing over-fitting to
  topic vocabulary.

## Nazario — 1,565 emails (1,565 phishing / 0 legitimate)
- **Origin / period:** Jose Nazario's phishing corpus (collected ~2004–2007 and after), a
  long-running real-world phishing collection.
- **Characteristics:** Full schema; genuine credential-harvesting phishing.
- **Why selected:** Provides authentic, in-the-wild phishing (the closest to real attacks),
  important for testing genuine-signal detection.

## Selection summary
The six sources deliberately span three regimes — **phishing-only** (Nazario, Nigerian Fraud),
**spam/ham** (SpamAssassin, Ling), and **large mixed** (CEAS, Enron) — which is exactly the
heterogeneity needed to separate genuine phishing detection from dataset-specific artifacts and to
stress-test generalization (RQ1, RQ3). TREC-05/06/07 were deferred as an optional scale ablation.
