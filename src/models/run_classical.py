"""Week 3 — TF-IDF + 5 classical ML models on the multi-source corpus.

Real experiment (CPU). Reports Accuracy, Precision, Recall, F1, ROC-AUC, PR-AUC,
and confusion matrices; sweeps TF-IDF max_features; saves models + metrics for
reproducibility.
"""
import json, os, time, warnings
import numpy as np, pandas as pd, joblib
warnings.filterwarnings("ignore")
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             roc_auc_score, average_precision_score, confusion_matrix,
                             roc_curve, precision_recall_curve)

SEED = 42
os.makedirs("results/tables", exist_ok=True)
os.makedirs("models", exist_ok=True)
STOP = list(ENGLISH_STOP_WORDS | {"from","to","cc","subject","sent","re","fwd"})

tr = pd.read_pickle("data/processed/train_clean.pkl")
te = pd.read_pickle("data/processed/test_clean.pkl")
ytr, yte = tr["label"].values, te["label"].values
print(f"train={len(tr):,} test={len(te):,}")

# ---------- 1. TF-IDF feature-count sweep (justify max_features) ----------
sweep = {}
for mf in [5000, 10000, 20000, 50000]:
    vec = TfidfVectorizer(ngram_range=(1,2), max_features=mf, sublinear_tf=True, min_df=2, stop_words=STOP)
    Xtr = vec.fit_transform(tr["text"]); Xte = vec.transform(te["text"])
    clf = LogisticRegression(max_iter=1000, random_state=SEED).fit(Xtr, ytr)
    f1 = f1_score(yte, clf.predict(Xte))
    sweep[mf] = round(f1, 4); print(f"  max_features={mf:>6}: LR test F1={f1:.4f}, vocab={len(vec.vocabulary_):,}")
json.dump(sweep, open("results/tables/feature_sweep.json","w"), indent=2)

# ---------- 2. Final TF-IDF (max_features=20000) ----------
vec = TfidfVectorizer(ngram_range=(1,2), max_features=20000, sublinear_tf=True, min_df=2, stop_words=STOP)
Xtr = vec.fit_transform(tr["text"]); Xte = vec.transform(te["text"])
joblib.dump(vec, "models/tfidf_vectorizer.joblib")
print(f"TF-IDF matrix: train {Xtr.shape}, test {Xte.shape}")

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=SEED),
    "Naive Bayes": MultinomialNB(),
    "Decision Tree": DecisionTreeClassifier(random_state=SEED),
    "Random Forest": RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=SEED),
    "Linear SVM": LinearSVC(random_state=SEED),
}

results, curves = {}, {}
for name, clf in models.items():
    t0 = time.time(); clf.fit(Xtr, ytr); pred = clf.predict(Xte)
    if hasattr(clf, "predict_proba"): score = clf.predict_proba(Xte)[:,1]
    else: score = clf.decision_function(Xte)
    cm = confusion_matrix(yte, pred)
    results[name] = {
        "accuracy": round(accuracy_score(yte, pred),4),
        "precision": round(precision_score(yte, pred),4),
        "recall": round(recall_score(yte, pred),4),
        "f1": round(f1_score(yte, pred),4),
        "roc_auc": round(roc_auc_score(yte, score),4),
        "pr_auc": round(average_precision_score(yte, score),4),
        "confusion_matrix": cm.tolist(),
        "train_seconds": round(time.time()-t0,1),
    }
    fpr,tpr,_ = roc_curve(yte, score); prec,rec,_ = precision_recall_curve(yte, score)
    curves[name] = {"fpr":fpr.tolist(),"tpr":tpr.tolist(),"prec":prec.tolist(),"rec":rec.tolist()}
    joblib.dump(clf, f"models/{name.replace(' ','_').lower()}.joblib")
    r=results[name]; print(f"  {name:20s} F1={r['f1']:.4f} ROC-AUC={r['roc_auc']:.4f} PR-AUC={r['pr_auc']:.4f} ({r['train_seconds']}s)")

json.dump(results, open("results/tables/classical_metrics.json","w"), indent=2)
json.dump(curves, open("results/tables/curves.json","w"), indent=2)
print("saved metrics + models")
