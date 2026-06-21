"""Fine-tune transformer baselines (BERT / DistilBERT / RoBERTa).

NOTE: requires a GPU and HuggingFace access -> run on Google Colab or Kaggle,
not in the restricted sandbox. Outputs (metrics JSON) are copied back to
results/ and reported in Chapter 4. This is a runnable template, not yet executed.
"""
# from transformers import (AutoTokenizer, AutoModelForSequenceClassification,
#                           TrainingArguments, Trainer)
# from datasets import Dataset

def fine_tune(model_name, train_df, eval_df, text_col="text", label_col="label",
              epochs=3, lr=2e-5, batch_size=16, max_length=256, seed=42):
    """Skeleton: tokenize -> Trainer.train() -> evaluate. Fill in on GPU runtime."""
    raise NotImplementedError(
        "Run on GPU (Colab/Kaggle). See README 'Environment' section."
    )
