from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error

IN=Path("results_snapshots/o002_feature_rows_run-37217735818.jsonl")
OUT=Path("results")
NBOOT=5000
SHIFTS=[0,1,2,3]

def crossed_boot(mat,seed):
    rng=np.random.default_rng(seed)
    ns,nv=mat.shape
    vals=np.empty(NBOOT,float)
    for b in range(NBOOT):
        si=rng.integers(0,ns,size=ns)
        vi=rng.integers(0,nv,size=nv)
        vals[b]=float(np.mean(mat[np.ix_(si,vi)]))
    return {"mean":float(np.mean(mat)),
            "ci95":[float(np.percentile(vals,2.5)),float(np.percentile(vals,97.5))]}

def horizon_frame(df,h):
    z=df.sort_values(["subject","video_id","time_norm"]).copy()
    g=z.groupby(["subject","video_id"],sort=False)
    z["target_valence"]=g["y_valence"].shift(-h)
    z["target_arousal"]=g["y_arousal"].shift(-h)
    return z.dropna(subset=["target_valence","target_arousal"]).reset_index(drop=True)

def main():
    OUT.mkdir(exist_ok=True)
    base=pd.read_json(IN,lines=True)
    base["video_id"]=base["video_id"].astype(str)
    subjects=sorted(base.subject.unique())
    videos=sorted(base.video_id.unique(),key=lambda x:int(x))
    if len(subjects)!=30 or videos!=[str(i) for i in range(1,9)]:
        raise RuntimeError("Frozen CASE shape mismatch")
    res={"status":"O002_B1_NAIVE_PERSISTENCE_BASELINE",
         "protocol":"protocols/o002_b1_naive_persistence.json",
         "horizons":{},
         "firewall":"Diagnostic benchmark only; no physiology, causal, or phenomenal inference."}
    for hi,h in enumerate(SHIFTS):
        df=horizon_frame(base,h)
        hk=f"shift_{h}_gap_{1+10*h}s"
        hz={"rows":int(len(df)),"targets":{}}
        for ti,target in enumerate(("valence","arousal")):
            target_col="target_"+target
            pred_col="prior_"+target
            y=df[target_col].to_numpy(float)
            p=df[pred_col].to_numpy(float)
            mat=np.full((len(subjects),len(videos)),np.nan)
            cells={}
            for si,s in enumerate(subjects):
                for vi,v in enumerate(videos):
                    q=df[(df.subject==s)&(df.video_id==v)]
                    if len(q)==0: raise RuntimeError(f"Missing cell {s} {v} h={h}")
                    mae=float(mean_absolute_error(q[target_col],q[pred_col]))
                    mat[si,vi]=mae
                    cells[f"{s}|video-{v}"]={"n":int(len(q)),"mae":mae}
            hz["targets"][target]={
              "row_weighted_mae":float(mean_absolute_error(y,p)),
              "mean_cell_mae":float(np.mean(mat)),
              "crossed_bootstrap_mean_cell_mae":crossed_boot(mat,301000+hi*100+ti),
              "cells":cells
            }
        res["horizons"][hk]=hz
    (OUT/"o002_b1_naive_persistence.json").write_text(json.dumps(res,indent=2),encoding="utf-8")
    slim={"status":res["status"],"horizons":{}}
    for h,hz in res["horizons"].items():
        slim["horizons"][h]={t:{k:v for k,v in tv.items() if k!="cells"} for t,tv in hz["targets"].items()}
    print(json.dumps(slim,indent=2))

if __name__=="__main__":
    main()
