"""Week 6 — Adversarial robustness evaluation (RQ4).

Apply each attack to phishing test emails at 5/10/15%, run the full defender
pipeline (clean -> TF-IDF -> model), and measure the drop in phishing detection
(recall) and overall F1. Legitimate emails are left unchanged (realistic threat model).
"""
import json, numpy as np, pandas as pd, joblib
from src.features.preprocess import clean_text
from src.robustness.adversarial import apply_attack
from sklearn.metrics import f1_score, recall_score

MODELS = {"Linear SVM":"linear_svm","Logistic Regression":"logistic_regression",
          "Random Forest":"random_forest","Naive Bayes":"naive_bayes","Decision Tree":"decision_tree"}
ATTACKS = ["char_substitution","keyword_injection","html_obfuscation"]
LEVELS = [0.05, 0.10, 0.15]

te = pd.read_csv("data/processed/test.csv", low_memory=False)
te["raw"] = te["subject"].fillna("").astype(str) + " " + te["body"].fillna("").astype(str).str.slice(0,40000)
y = te["label"].values
is_ph = y == 1
vec = joblib.load("models/tfidf_vectorizer.joblib")
clf = {m: joblib.load(f"models/{f}.joblib") for m,f in MODELS.items()}

# baseline: clean everything once
clean_all = te["raw"].map(clean_text).values
Xb = vec.transform(clean_all)
base = {m: {"recall_phish": round(recall_score(y, clf[m].predict(Xb)), 4),
            "f1": round(f1_score(y, clf[m].predict(Xb)), 4)} for m in MODELS}
base_pred = {m: clf[m].predict(Xb) for m in MODELS}

results = {"baseline": base, "attacks": {}}
ph_idx = np.where(is_ph)[0]

for atk in ATTACKS:
    results["attacks"][atk] = {}
    for lv in LEVELS:
        # perturb only phishing raw text, then clean
        perturbed = clean_all.copy()
        for i in ph_idx:
            perturbed[i] = clean_text(apply_attack(te["raw"].iloc[i], atk, lv))
        Xp = vec.transform(perturbed)
        row = {}
        for m in MODELS:
            pred = clf[m].predict(Xp)
            row[m] = {"recall_phish": round(recall_score(y, pred), 4),
                      "f1": round(f1_score(y, pred), 4),
                      "recall_drop": round(base[m]["recall_phish"] - recall_score(y, pred), 4)}
        results["attacks"][atk][f"{int(lv*100)}%"] = row
        print(f"{atk:18s} {int(lv*100):>2}%  " +
              "  ".join(f"{m.split()[0]}:{row[m]['recall_phish']:.3f}" for m in MODELS), flush=True)

json.dump(results, open("results/tables/adversarial.json","w"), indent=2)
print("\nBASELINE phishing recall:", {m: base[m]["recall_phish"] for m in MODELS})
print("saved results/tables/adversarial.json")
