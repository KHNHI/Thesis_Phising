"""Week 2 — Build the multi-source phishing corpus and report statistics.

Pipeline: load 6 sources -> normalize to a common schema (+source tag) ->
concatenate -> deduplicate -> leakage-controlled split (GroupShuffleSplit by
sender domain) -> write processed CSVs + a statistics report.

Run:
    python src/data/build_corpus.py --raw_dir data/raw --out_dir data/processed
"""
import argparse
import json
import os
import pandas as pd

from src.data.merge_sources import load_source
from src.data.split import group_split

SOURCES = {
    "ceas": "CEAS_08.csv",
    "nazario": "Nazario.csv",
    "nigerian_fraud": "Nigerian_Fraud.csv",
    "spamassassin": "SpamAssasin.csv",
    "enron": "Enron.csv",
    "ling": "Ling.csv",
}


def label_counts(df):
    vc = df["label"].value_counts(dropna=False).to_dict()
    return {int(k) if pd.notna(k) else "NaN": int(v) for k, v in vc.items()}


def build(raw_dir, out_dir):
    report = {"per_source": {}, "pipeline": {}}

    frames = []
    for name, fname in SOURCES.items():
        path = os.path.join(raw_dir, fname)
        df = load_source(path, name)
        frames.append(df)
        report["per_source"][name] = {"rows": len(df), "labels": label_counts(df)}

    merged = pd.concat(frames, ignore_index=True)
    report["pipeline"]["merged_rows"] = len(merged)

    # drop rows with empty body, then deduplicate on (subject, body)
    merged = merged.dropna(subset=["body"])
    merged = merged[merged["body"].astype(str).str.strip() != ""]
    report["pipeline"]["after_empty_body_drop"] = len(merged)

    before = len(merged)
    merged = merged.drop_duplicates(subset=["subject", "body"]).reset_index(drop=True)
    report["pipeline"]["duplicates_removed"] = before - len(merged)
    report["pipeline"]["final_corpus_rows"] = len(merged)
    report["pipeline"]["final_labels"] = label_counts(merged)

    # leakage-controlled split
    train, test = group_split(merged, test_size=0.20, seed=42)
    report["pipeline"]["train_rows"] = len(train)
    report["pipeline"]["test_rows"] = len(test)
    report["pipeline"]["train_labels"] = label_counts(train)
    report["pipeline"]["test_labels"] = label_counts(test)

    os.makedirs(out_dir, exist_ok=True)
    merged.to_csv(os.path.join(out_dir, "corpus.csv"), index=False)
    train.to_csv(os.path.join(out_dir, "train.csv"), index=False)
    test.to_csv(os.path.join(out_dir, "test.csv"), index=False)
    with open(os.path.join(out_dir, "corpus_stats.json"), "w") as f:
        json.dump(report, f, indent=2)
    return report


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw_dir", default="data/raw")
    ap.add_argument("--out_dir", default="data/processed")
    args = ap.parse_args()
    rep = build(args.raw_dir, args.out_dir)
    print(json.dumps(rep, indent=2))
