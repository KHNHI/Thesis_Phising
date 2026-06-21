"""Leakage-controlled train/test split (GroupShuffleSplit by sender domain).

Rows without a sender address (e.g. Enron, Ling) get a unique per-row group so
they are distributed across the split rather than collapsing into one bucket.
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit


def sender_domain(series):
    dom = series.fillna("").astype(str).str.extract(r"@([\w.-]+)")[0]
    return dom


def make_groups(df):
    """Domain group where available; unique group id otherwise (no false leakage)."""
    dom = sender_domain(df["sender"]) if "sender" in df.columns else pd.Series([np.nan] * len(df))
    groups = dom.copy()
    missing = groups.isna() | (groups == "")
    groups[missing] = ["__row_%d" % i for i in range(missing.sum())]
    return groups.values


def group_split(df, test_size=0.20, seed=42):
    groups = make_groups(df)
    gss = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=seed)
    train_idx, test_idx = next(gss.split(df, groups=groups))
    return df.iloc[train_idx].copy(), df.iloc[test_idx].copy()
