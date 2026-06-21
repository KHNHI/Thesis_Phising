"""Evaluation: standard metrics, 95% bootstrap CI, and McNemar's test."""
import numpy as np
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, confusion_matrix)


def basic_metrics(y_true, y_pred, y_score=None):
    out = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
    }
    if y_score is not None:
        out["auc_roc"] = roc_auc_score(y_true, y_score)
    return out


def bootstrap_ci(y_true, y_pred, metric=f1_score, n=1000, alpha=0.05, seed=42):
    rng = np.random.default_rng(seed)
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    stats = []
    for _ in range(n):
        idx = rng.integers(0, len(y_true), len(y_true))
        stats.append(metric(y_true[idx], y_pred[idx], zero_division=0))
    lo, hi = np.percentile(stats, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(np.mean(stats)), float(lo), float(hi)


def mcnemar(y_true, pred_a, pred_b):
    """McNemar's test comparing two classifiers (returns statistic, p-value)."""
    from statsmodels.stats.contingency_tables import mcnemar as _mcnemar
    a_correct = np.asarray(pred_a) == np.asarray(y_true)
    b_correct = np.asarray(pred_b) == np.asarray(y_true)
    table = [[np.sum(a_correct & b_correct), np.sum(a_correct & ~b_correct)],
             [np.sum(~a_correct & b_correct), np.sum(~a_correct & ~b_correct)]]
    res = _mcnemar(table, exact=False, correction=True)
    return float(res.statistic), float(res.pvalue)
