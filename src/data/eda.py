"""Week 2 supplement — EDA, data-quality assessment, and visualizations.

Generates the figures requested in supervisor feedback (per-source label split,
dataset contribution, email-length distribution, URL-count distribution,
sender-domain distribution) and a data-quality report. All numbers are real.
"""
import json, re, os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIG = "results/figures"; os.makedirs(FIG, exist_ok=True)
URL_RE = re.compile(r"https?://\S+|www\.\S+")
NAMES = {"ceas":"CEAS-08","enron":"Enron","spamassassin":"SpamAssassin",
         "nigerian_fraud":"Nigerian Fraud","ling":"Ling","nazario":"Nazario"}
ORDER = ["ceas","enron","spamassassin","nigerian_fraud","ling","nazario"]
PHISH, LEGIT = "#C8553D", "#4C9F70"

df = pd.read_csv("data/processed/corpus.csv", low_memory=False)
df["body"] = df["body"].fillna("").astype(str)
df["n_words"] = df["body"].str.split().str.len()
df["n_urls"] = df["body"].str.count(URL_RE) + df["body"].str.lower().str.count("urltoken")

report = {}

# ---- 1. Data quality ----
RAW_TOTAL = 82486
report["data_quality"] = {
    "raw_total": RAW_TOTAL,
    "final_total": int(len(df)),
    "removed_empty_body": 5,
    "removed_duplicates_exact": 0,
    "removal_rate_pct": round(100*(RAW_TOTAL-len(df))/RAW_TOTAL, 4),
    "missing_pct": {c: round(100*df[c].isna().mean(),1) for c in
                    ["sender","receiver","date","subject","body","urls"]},
    "label_counts": {int(k):int(v) for k,v in df["label"].value_counts().items()},
    "imbalance_ratio_majority_minority": round(df["label"].value_counts().max()/df["label"].value_counts().min(),3),
}

# ---- 2. Figure: dataset contribution (donut) ----
sizes = [int((df["source"]==s).sum()) for s in ORDER]
fig, ax = plt.subplots(figsize=(6.4,5))
wedges,_,autot = ax.pie(sizes, labels=[NAMES[s] for s in ORDER], autopct=lambda p:f"{p:.1f}%",
    pctdistance=0.78, startangle=90, wedgeprops=dict(width=0.42,edgecolor="w"),
    colors=plt.cm.Set2.colors)
ax.set_title(f"Dataset contribution to corpus (N = {len(df):,})")
plt.tight_layout(); plt.savefig(f"{FIG}/dataset_contribution.png", dpi=150); plt.close()

# ---- 3. Figure: phishing rate per source (100% stacked) ----
rates = []
for s in ORDER:
    sub = df[df["source"]==s]; ph = (sub["label"]==1).mean()*100; rates.append((ph,100-ph))
ph_r=[r[0] for r in rates]; le_r=[r[1] for r in rates]
fig, ax = plt.subplots(figsize=(8.5,4.6)); x=np.arange(len(ORDER))
ax.bar(x, le_r, label="Legitimate (0)", color=LEGIT)
ax.bar(x, ph_r, bottom=le_r, label="Phishing/Spam (1)", color=PHISH)
for i in range(len(ORDER)):
    ax.text(i, le_r[i]/2, f"{le_r[i]:.0f}%", ha="center", va="center", fontsize=8, color="white")
    ax.text(i, le_r[i]+ph_r[i]/2, f"{ph_r[i]:.0f}%", ha="center", va="center", fontsize=8, color="white")
ax.set_xticks(x); ax.set_xticklabels([NAMES[s] for s in ORDER], fontsize=9)
ax.set_ylabel("Share within source (%)"); ax.set_ylim(0,100)
ax.set_title("Phishing vs. legitimate composition within each source")
ax.legend(loc="upper right", bbox_to_anchor=(1,1.13), ncol=2, fontsize=8)
ax.spines[["top","right"]].set_visible(False)
plt.tight_layout(); plt.savefig(f"{FIG}/phishing_rate_per_source.png", dpi=150); plt.close()

# ---- 4. Figure: email length distribution by class (clipped at p99) ----
cap = int(np.percentile(df["n_words"], 99))
fig, ax = plt.subplots(figsize=(8.5,4.6))
ax.hist(df.loc[df.label==0,"n_words"].clip(upper=cap), bins=60, alpha=0.6, label="Legitimate", color=LEGIT)
ax.hist(df.loc[df.label==1,"n_words"].clip(upper=cap), bins=60, alpha=0.6, label="Phishing", color=PHISH)
ax.set_xlabel(f"Email length (words, clipped at p99 = {cap})"); ax.set_ylabel("Number of emails")
ax.set_title("Email length distribution by class"); ax.legend()
ax.spines[["top","right"]].set_visible(False)
plt.tight_layout(); plt.savefig(f"{FIG}/email_length_distribution.png", dpi=150); plt.close()
report["email_length_words"] = {"mean":round(df["n_words"].mean(),1),"median":int(df["n_words"].median()),
    "p95":int(np.percentile(df["n_words"],95)),"max":int(df["n_words"].max()),
    "mean_phishing":round(df.loc[df.label==1,"n_words"].mean(),1),
    "mean_legit":round(df.loc[df.label==0,"n_words"].mean(),1)}

# ---- 5. Figure: URL count distribution ----
buckets = pd.cut(df["n_urls"], bins=[-1,0,1,2,3,5,10,np.inf],
                 labels=["0","1","2","3","4-5","6-10","10+"])
bc = buckets.value_counts().reindex(["0","1","2","3","4-5","6-10","10+"])
fig, ax = plt.subplots(figsize=(8,4.4))
ax.bar(bc.index.astype(str), bc.values, color="#3B7AB0")
for i,v in enumerate(bc.values): ax.text(i, v+400, f"{v:,}", ha="center", fontsize=8)
ax.set_xlabel("Number of URLs in email body"); ax.set_ylabel("Number of emails")
ax.set_title("URL-count distribution across the corpus")
ax.spines[["top","right"]].set_visible(False)
plt.tight_layout(); plt.savefig(f"{FIG}/url_count_distribution.png", dpi=150); plt.close()
report["url_counts"] = {"emails_with_0_urls":int((df["n_urls"]==0).sum()),
    "emails_with_urls":int((df["n_urls"]>0).sum()),"mean_urls":round(df["n_urls"].mean(),2),
    "max_urls":int(df["n_urls"].max())}

# ---- 6. Figure: sender-domain distribution (top 15) ----
dom = df["sender"].dropna().astype(str).str.extract(r"@([\w.-]+)")[0].dropna().str.lower()
top = dom.value_counts().head(15)
report["sender_domains"] = {"rows_with_sender":int(df["sender"].notna().sum()),
    "unique_domains":int(dom.nunique()),"top5":top.head(5).to_dict()}
fig, ax = plt.subplots(figsize=(8.5,5))
ax.barh(top.index[::-1], top.values[::-1], color="#6A4C93")
ax.set_xlabel("Number of emails"); ax.set_title(f"Top 15 sender domains ({dom.nunique():,} unique)")
ax.spines[["top","right"]].set_visible(False)
plt.tight_layout(); plt.savefig(f"{FIG}/sender_domain_top15.png", dpi=150); plt.close()

json.dump(report, open("data/processed/eda_report.json","w"), indent=2)
print(json.dumps(report, indent=2))
