"""Week 4-5 - Transformer fine-tuning (BERT, DistilBERT, RoBERTa).

RUN ON GPU (Google Colab / Kaggle), NOT in the restricted sandbox:
the sandbox blocks HuggingFace and has no GPU.

Steps on Colab:
  1. Runtime -> Change runtime type -> GPU (T4 is enough).
  2. Upload data/processed/train.csv and test.csv (from build_corpus.py), or re-run it there.
  3. pip install -q transformers datasets accelerate scikit-learn
  4. python train_transformer.py
  5. Send results/tables/transformer_metrics.json back; it will be written into Chapter 4.

Uses the SAME test split and metrics as the classical pipeline for a fair comparison.
"""
import json, os, numpy as np, pandas as pd
import torch
from datasets import Dataset
from transformers import (AutoTokenizer, AutoModelForSequenceClassification,
                          TrainingArguments, Trainer, DataCollatorWithPadding)
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             roc_auc_score, average_precision_score, confusion_matrix)

MODELS = {"BERT": "bert-base-uncased", "DistilBERT": "distilbert-base-uncased", "RoBERTa": "roberta-base"}
MAX_LEN, EPOCHS, BATCH, LR, SEED = 256, 3, 16, 2e-5, 42
os.makedirs("results/tables", exist_ok=True)

def load_split():
    tr = pd.read_csv("data/processed/train.csv", low_memory=False)
    te = pd.read_csv("data/processed/test.csv", low_memory=False)
    for d in (tr, te):
        d["text"] = (d["subject"].fillna("").astype(str) + " " +
                     d["body"].fillna("").astype(str).str.slice(0, 4000))
    return tr[["text", "label"]], te[["text", "label"]]

def metrics_from(y, pred, score):
    return {"accuracy": round(accuracy_score(y, pred), 4), "precision": round(precision_score(y, pred), 4),
            "recall": round(recall_score(y, pred), 4), "f1": round(f1_score(y, pred), 4),
            "roc_auc": round(roc_auc_score(y, score), 4), "pr_auc": round(average_precision_score(y, score), 4),
            "confusion_matrix": confusion_matrix(y, pred).tolist()}

def run(name, ckpt, tr, te):
    tok = AutoTokenizer.from_pretrained(ckpt)
    def enc(b): return tok(b["text"], truncation=True, max_length=MAX_LEN)
    dtr = Dataset.from_pandas(tr).map(enc, batched=True)
    dte = Dataset.from_pandas(te).map(enc, batched=True)
    model = AutoModelForSequenceClassification.from_pretrained(ckpt, num_labels=2)
    args = TrainingArguments(output_dir=f"out_{name}", num_train_epochs=EPOCHS,
        per_device_train_batch_size=BATCH, per_device_eval_batch_size=64, learning_rate=LR,
        seed=SEED, logging_steps=200, report_to="none", eval_strategy="epoch", save_strategy="no",
        fp16=torch.cuda.is_available())
    trainer = Trainer(model=model, args=args, train_dataset=dtr, eval_dataset=dte,
        tokenizer=tok, data_collator=DataCollatorWithPadding(tok))
    trainer.train()
    logits = trainer.predict(dte).predictions
    prob = torch.softmax(torch.tensor(logits), dim=1)[:, 1].numpy()
    pred = (prob >= 0.5).astype(int)
    return metrics_from(te["label"].values, pred, prob)

if __name__ == "__main__":
    assert torch.cuda.is_available(), "No GPU - run on Colab/Kaggle with a GPU."
    tr, te = load_split()
    results = {}
    for name, ckpt in MODELS.items():
        print(f"\n=== Fine-tuning {name} ({ckpt}) ===")
        results[name] = run(name, ckpt, tr, te); print(name, results[name])
        json.dump(results, open("results/tables/transformer_metrics.json", "w"), indent=2)
    print("\nDONE -> results/tables/transformer_metrics.json")
