"""
OPTIONAL (Colab/GPU) — Transformer adversarial robustness, to complete RQ4.

Fine-tunes ONE transformer (default DistilBERT for speed; change MODEL to 'roberta-base'
or 'bert-base-uncased' if you want), then applies the SAME three attacks used on the
classical models (char substitution, keyword injection, HTML obfuscation) at 5/10/15%
to phishing test emails, and measures phishing recall.

Run on Colab with GPU:
    !pip install -q transformers datasets accelerate scikit-learn
    !python train_transformer_robustness.py
Output: transformer_robustness.json  -> send it back to finish the RQ4 comparison.
"""
import json, os, re, random, urllib.request
import numpy as np, pandas as pd, torch
from datasets import Dataset
from transformers import (AutoTokenizer, AutoModelForSequenceClassification,
                          TrainingArguments, Trainer, DataCollatorWithPadding)
from sklearn.metrics import recall_score
from sklearn.model_selection import GroupShuffleSplit

MODEL = "distilbert-base-uncased"      # change to roberta-base / bert-base-uncased if desired
RAW = "https://raw.githubusercontent.com/rokibulroni/Phishing-Email-Dataset/main"
SRC = {"ceas":"CEAS_08.csv","nazario":"Nazario.csv","nigerian_fraud":"Nigerian_Fraud.csv",
       "spamassassin":"SpamAssasin.csv","enron":"Enron.csv","ling":"Ling.csv"}
SCHEMA=["sender","receiver","date","subject","body","urls","label","source"]; SEED=42

# ---- same attacks as the classical pipeline ----
LEET={"a":"4","e":"3","i":"1","o":"0","s":"5","t":"7"}
INJECT=["enron","wrote","thanks","regards","meeting","team","python","university","report","attached","schedule","project"]
def char_sub(t,r,s=42):
    rng=random.Random(s); c=list(t); idx=[i for i,ch in enumerate(c) if ch.lower() in LEET]; rng.shuffle(idx)
    for i in idx[:int(len(idx)*r)]: c[i]=LEET[c[i].lower()]
    return "".join(c)
def inject(t,r,s=42):
    rng=random.Random(s); n=max(1,int(len(t.split())*r)); return t+" "+" ".join(rng.choice(INJECT) for _ in range(n))
def html_ob(t,r,s=42):
    rng=random.Random(s); w=t.split()
    for i,x in enumerate(w):
        if len(x)>3 and rng.random()<r:
            p=rng.randint(1,len(x)-1); w[i]=x[:p]+"<b></b>"+x[p:]
    return " ".join(w)
ATT={"char_substitution":char_sub,"keyword_injection":inject,"html_obfuscation":html_ob}

def build():
    os.makedirs("raw",exist_ok=True); fr=[]
    for n,f in SRC.items():
        p=f"raw/{f}"
        if not os.path.exists(p): urllib.request.urlretrieve(f"{RAW}/{f}",p)
        d=pd.read_csv(p,low_memory=False); d.columns=[c.strip().lower() for c in d.columns]
        for c in SCHEMA:
            if c not in d.columns: d[c]=None
        d["source"]=n; fr.append(d[SCHEMA])
    df=pd.concat(fr,ignore_index=True); df=df.dropna(subset=["body"]); df=df[df["body"].astype(str).str.strip()!=""]
    df=df.drop_duplicates(subset=["subject","body"]).reset_index(drop=True)
    dom=df["sender"].fillna("").astype(str).str.extract(r"@([\w.-]+)")[0]
    miss=dom.isna()|(dom==""); dom[miss]=[f"__r{i}" for i in range(miss.sum())]
    tr_i,te_i=next(GroupShuffleSplit(n_splits=1,test_size=0.2,random_state=SEED).split(df,groups=dom.values))
    return df.iloc[tr_i].copy(), df.iloc[te_i].copy()

def mktext(d): return (d["subject"].fillna("").astype(str)+" "+d["body"].fillna("").astype(str).str.slice(0,4000))

def main():
    assert torch.cuda.is_available(),"Use a GPU runtime."
    tr,te=build()
    tr=tr.assign(text=mktext(tr))[["text","label"]]
    te_raw=mktext(te).values; y=te["label"].values
    tok=AutoTokenizer.from_pretrained(MODEL)
    enc=lambda b: tok(b["text"],truncation=True,max_length=256)
    dtr=Dataset.from_pandas(tr).map(enc,batched=True)
    model=AutoModelForSequenceClassification.from_pretrained(MODEL,num_labels=2)
    args=TrainingArguments(output_dir="out",num_train_epochs=3,per_device_train_batch_size=16,
        per_device_eval_batch_size=64,learning_rate=2e-5,seed=SEED,report_to="none",save_strategy="no",fp16=True,logging_steps=200)
    tr_obj=Trainer(model=model,args=args,train_dataset=dtr,data_collator=DataCollatorWithPadding(tok))
    tr_obj.train()
    def recall_on(texts):
        d=Dataset.from_dict({"text":list(texts)}).map(enc,batched=True)
        logits=tr_obj.predict(d).predictions; pred=logits.argmax(-1)
        return round(recall_score(y,pred),4)
    out={"model":MODEL,"baseline":recall_on(te_raw),"attacks":{}}
    ph=np.where(y==1)[0]
    for a in ATT:
        out["attacks"][a]={}
        for lv in [0.05,0.10,0.15]:
            pert=te_raw.copy()
            for i in ph: pert[i]=ATT[a](te_raw[i],lv)
            out["attacks"][a][f"{int(lv*100)}%"]=recall_on(pert)
            print(a,int(lv*100),out["attacks"][a][f"{int(lv*100)}%"],flush=True)
            json.dump(out,open("transformer_robustness.json","w"),indent=2)
    print("DONE -> transformer_robustness.json")

if __name__=="__main__": main()
