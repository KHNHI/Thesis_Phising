"""Week 4 — statistical tests (McNemar, bootstrap CI) and error analysis."""
import json, numpy as np, pandas as pd
from statsmodels.stats.contingency_tables import mcnemar
from sklearn.metrics import f1_score

ORDER = ["Linear SVM","Logistic Regression","Random Forest","Naive Bayes","Decision Tree"]
preds = json.load(open("results/tables/test_predictions.json"))
meta = pd.read_csv("results/tables/test_meta.csv")
y = meta["label"].values
src = meta["source"].values
te = pd.read_pickle("data/processed/test_clean.pkl").reset_index(drop=True)
te["n_words"] = te["text"].str.split().str.len()

out = {}

# ---- Bootstrap CI for F1 ----
def boot_ci(y, p, n=1000, seed=42):
    rng = np.random.default_rng(seed); y=np.asarray(y); p=np.asarray(p); s=[]
    for _ in range(n):
        idx = rng.integers(0, len(y), len(y)); s.append(f1_score(y[idx], p[idx], zero_division=0))
    lo, hi = np.percentile(s, [2.5, 97.5]); return round(float(np.mean(s)),4), round(float(lo),4), round(float(hi),4)
out["bootstrap_f1_ci"] = {m: dict(zip(["mean","lo","hi"], boot_ci(y, preds[m]))) for m in ORDER}

# ---- McNemar vs best (Linear SVM) ----
best = np.array(preds["Linear SVM"])
out["mcnemar_vs_svm"] = {}
for m in ORDER:
    if m == "Linear SVM": continue
    pm = np.array(preds[m])
    a = (best == y); b = (pm == y)
    tb = [[int(np.sum(a&b)), int(np.sum(a&~b))],[int(np.sum(~a&b)), int(np.sum(~a&~b))]]
    r = mcnemar(tb, exact=False, correction=True)
    out["mcnemar_vs_svm"][m] = {"statistic": round(float(r.statistic),3), "p_value": float(f"{r.pvalue:.3e}"),
                                "svm_only_correct": tb[0][1], "other_only_correct": tb[1][0]}

# ---- Error analysis for best model (Linear SVM) ----
p = np.array(preds["Linear SVM"])
fp = (p==1)&(y==0); fn = (p==0)&(y==1); tp=(p==1)&(y==1); tn=(p==0)&(y==0)
out["svm_errors"] = {"FP": int(fp.sum()), "FN": int(fn.sum()), "TP": int(tp.sum()), "TN": int(tn.sum()),
    "FP_rate_pct": round(100*fp.sum()/(y==0).sum(),3), "FN_rate_pct": round(100*fn.sum()/(y==1).sum(),3),
    "mean_words": {"FP": round(te.loc[fp,"n_words"].mean(),1), "FN": round(te.loc[fn,"n_words"].mean(),1),
                   "correct": round(te.loc[tp|tn,"n_words"].mean(),1)}}

# ---- per-source error rate (Linear SVM) ----
ps={}
for s in pd.unique(src):
    mask = src==s; err = (p[mask]!=y[mask]).mean()
    ps[s] = {"n": int(mask.sum()), "error_pct": round(100*err,3), "phishing_share": round(100*y[mask].mean(),1)}
out["svm_error_by_source"] = ps

# ---- per-source error for ALL models (struggling types) ----
allm={}
for m in ORDER:
    pm=np.array(preds[m]); allm[m]={s: round(100*(pm[src==s]!=y[src==s]).mean(),2) for s in pd.unique(src)}
out["error_by_source_all_models"]=allm

json.dump(out, open("results/tables/error_analysis.json","w"), indent=2)
print(json.dumps(out, indent=2))
