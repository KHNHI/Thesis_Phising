# Data card

Raw datasets are **not** committed to the repository (see `.gitignore`).

## Download (run outside the restricted sandbox)
Primary source — Kaggle "Phishing Email Dataset" (Naser Abdullah Alam), per-source CSVs:
`CEAS_08.csv`, `Nazario.csv`, `Nigerian_Fraud.csv`, `SpamAssasin.csv`, `Enron.csv`, `Ling.csv`.

```bash
# requires a Kaggle API token (~/.kaggle/kaggle.json)
kaggle datasets download -d naserabdullahalam/phishing-email-dataset -p data/raw --unzip
```

Place all CSVs under `data/raw/`. Then:
```bash
python -c "from src.data.merge_sources import merge; print('ready')"
```

## Common schema (after merge)
`sender, receiver, date, subject, body, urls, label, source`
- `label`: 1 = phishing, 0 = legitimate
- `source`: provenance tag (ceas / nazario / nigerian_fraud / spamassassin / enron / ling)
