from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesRegressor, HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

IN=Path("results/o002_feature_rows.jsonl")
OUT=Path("results"); OUT.mkdir(exist_ok=True)
BOOT=5000

df=pd.read_json(IN,lines=True)
subjects=sorted(df.subject.unique())
phys=sorted(c for c in df.columns if c.startswith("phys_"))

def prep(target,combined):
    trs=[
      ("cat",OneHotEncoder(handle_unknown="ignore",sparse_output=False),["video_id"]),
      ("time",Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler())]),["time_norm"]),
      ("prior",Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler())]),["prior_"+target]),
    ]
    if combined:
        trs.append(("phys",Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler())]),phys))
    return ColumnTransformer(trs,sparse_threshold=0.0)

def learner(name):
    if name=="hgb":
        return HistGradientBoostingRegressor(max_iter=200,learning_rate=0.05,max_leaf_nodes=15,l2_regularization=1.0,random_state=601)
    return ExtraTreesRegressor(n_estimators=300,min_samples_leaf=5,max_features=0.5,n_jobs=-1,random_state=602)

def boot(vals,seed):
    rng=np.random.default_rng(seed); vals=np.asarray(vals,float)
    z=np.asarray([np.mean(rng.choice(vals,size=len(vals),replace=True)) for _ in range(BOOT)])
    return {"mean":float(np.mean(vals)),"ci95":[float(np.percentile(z,2.5)),float(np.percentile(z,97.5))]}

res={"status":"O002_S1_NONLINEAR_SENSITIVITY","protocol":"protocols/o002_s1_nonlinear_sensitivity.json","learners":{}}
any_positive=False; all_negative=True
for lname in ("hgb","extra_trees"):
    res["learners"][lname]={}
    for ti,target in enumerate(("valence","arousal")):
        diffs=[]; subj={}
        for i,s in enumerate(subjects,1):
            print(f"{lname} {target} {i}/{len(subjects)} {s}",flush=True)
            tr=df[df.subject!=s].reset_index(drop=True); te=df[df.subject==s].reset_index(drop=True)
            ytr=tr["y_"+target].to_numpy(float); yte=te["y_"+target].to_numpy(float)
            pb=prep(target,False); xb=pb.fit_transform(tr); xbt=pb.transform(te)
            pc=prep(target,True); xc=pc.fit_transform(tr); xct=pc.transform(te)
            mb=learner(lname).fit(xb,ytr); mc=learner(lname).fit(xc,ytr)
            eb=float(mean_absolute_error(yte,mb.predict(xbt))); ec=float(mean_absolute_error(yte,mc.predict(xct)))
            d=eb-ec; diffs.append(d); subj[s]={"baseline_mae":eb,"peripheral_mae":ec,"delta":d}
        b=boot(diffs,11000+ti+(0 if lname=="hgb" else 100))
        pos=b["ci95"][0]>0; neg=b["ci95"][1]<0
        any_positive=any_positive or pos; all_negative=all_negative and neg
        res["learners"][lname][target]={"bootstrap_delta":b,"subject_results":subj,"positive_increment":pos,"significant_degradation":neg}
if any_positive:
    verdict="NONLINEAR_PERIPHERAL_INCREMENT"
elif all_negative:
    verdict="STRONG_DEGRADATION"
else:
    verdict="ROBUST_NO_PERIPHERAL_INCREMENT"
res["verdict"]=verdict
res["firewall"]="Post-primary sensitivity only; cannot replace the frozen O002 primary endpoint."
(OUT/"o002_s1_nonlinear_sensitivity.json").write_text(json.dumps(res,indent=2),encoding="utf-8")
print(json.dumps({"verdict":verdict,"summary":{l:{t:res["learners"][l][t]["bootstrap_delta"] for t in ("valence","arousal")} for l in res["learners"]}},indent=2))
