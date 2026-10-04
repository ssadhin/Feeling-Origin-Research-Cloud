from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

IN=Path("results_snapshots/o002_feature_rows_run-37217735818.jsonl")
OUT=Path("results")
ALPHAS=[0.1,1.0,10.0,100.0,1000.0]
NBOOT=5000

def cols_for(target,spec,phys):
    if spec=="context_only":
        return ["time_norm"]
    if spec=="prior":
        return ["time_norm","prior_"+target]
    return ["time_norm","prior_"+target]+phys

def make_pipe(alpha):
    return Pipeline([
      ("imp",SimpleImputer(strategy="median")),
      ("sc",StandardScaler()),
      ("ridge",Ridge(alpha=alpha))
    ])

def tune_alpha(train,target,spec,phys):
    cols=cols_for(target,spec,phys)
    y=train["y_"+target].to_numpy(float)
    groups=train.subject.to_numpy()
    nsplit=min(4,len(np.unique(groups)))
    cv=GroupKFold(n_splits=nsplit)
    scores={a:[] for a in ALPHAS}
    for it,iv in cv.split(train[cols],y,groups):
        Xtr=train.iloc[it][cols]; Xva=train.iloc[iv][cols]
        ytr=y[it]; yva=y[iv]
        for a in ALPHAS:
            pred=make_pipe(a).fit(Xtr,ytr).predict(Xva)
            scores[a].append(mean_absolute_error(yva,pred))
    return min(ALPHAS,key=lambda a:(float(np.mean(scores[a])),a))

def crossed_boot(delta_mat,seed):
    rng=np.random.default_rng(seed)
    ns,nv=delta_mat.shape
    vals=np.empty(NBOOT,float)
    for b in range(NBOOT):
        si=rng.integers(0,ns,size=ns)
        vi=rng.integers(0,nv,size=nv)
        vals[b]=float(np.mean(delta_mat[np.ix_(si,vi)]))
    return {
      "mean":float(np.mean(delta_mat)),
      "ci95":[float(np.percentile(vals,2.5)),float(np.percentile(vals,97.5))]
    }

def main():
    OUT.mkdir(exist_ok=True)
    df=pd.read_json(IN,lines=True)
    df["video_id"]=df["video_id"].astype(str)
    subjects=sorted(df.subject.unique())
    videos=sorted(df.video_id.unique(),key=lambda x:int(x))
    phys=sorted(c for c in df.columns if c.startswith("phys_"))
    if len(subjects)!=30 or videos!=[str(i) for i in range(1,9)] or len(phys)!=29:
        raise RuntimeError(f"Frozen shape mismatch subjects={len(subjects)} videos={videos} phys={len(phys)}")
    specs=["context_only","prior","physiology"]
    result={
      "status":"O002_G1_JOINT_PERSON_STIMULUS_GENERALIZATION",
      "protocol":"protocols/o002_g1_joint_person_stimulus_generalization.json",
      "n_subjects":len(subjects),"n_videos":len(videos),"n_test_cells":len(subjects)*len(videos),
      "targets":{},
      "firewall":"Predictive robustness only; no causal or phenomenal inference."
    }
    for ti,target in enumerate(("valence","arousal")):
        cells={}
        matrices={spec:np.full((len(subjects),len(videos)),np.nan) for spec in specs}
        row_weighted={spec:{"y":[],"pred":[]} for spec in specs}
        for si,sub in enumerate(subjects):
            for vi,vid in enumerate(videos):
                print(f"{target} cell subject {si+1}/{len(subjects)} {sub} video {vid}",flush=True)
                train=df[(df.subject!=sub)&(df.video_id!=vid)].reset_index(drop=True)
                test=df[(df.subject==sub)&(df.video_id==vid)].reset_index(drop=True)
                if len(test)==0:
                    raise RuntimeError(f"Missing test cell {sub} video {vid}")
                yte=test["y_"+target].to_numpy(float)
                ck=f"{sub}|video-{vid}"
                cells[ck]={"n_test":int(len(test)),"models":{}}
                for spec in specs:
                    alpha=tune_alpha(train,target,spec,phys)
                    cols=cols_for(target,spec,phys)
                    mdl=make_pipe(alpha).fit(train[cols],train["y_"+target].to_numpy(float))
                    pred=mdl.predict(test[cols])
                    mae=float(mean_absolute_error(yte,pred))
                    matrices[spec][si,vi]=mae
                    cells[ck]["models"][spec]={"mae":mae,"alpha":alpha}
                    row_weighted[spec]["y"].extend(yte.tolist())
                    row_weighted[spec]["pred"].extend(pred.tolist())
        prior_delta=matrices["context_only"]-matrices["prior"]
        phys_delta=matrices["prior"]-matrices["physiology"]
        pstat=crossed_boot(prior_delta,101000+ti)
        fstat=crossed_boot(phys_delta,102000+ti)
        metrics={}
        for spec in specs:
            yy=np.asarray(row_weighted[spec]["y"],float)
            pp=np.asarray(row_weighted[spec]["pred"],float)
            metrics[spec]={
              "row_weighted_mae":float(mean_absolute_error(yy,pp)),
              "mean_cell_mae":float(np.mean(matrices[spec]))
            }
        result["targets"][target]={
          "metrics":metrics,
          "prior_increment_crossed_bootstrap":pstat,
          "physiology_increment_crossed_bootstrap":fstat,
          "prior_increment_positive":bool(pstat["ci95"][0]>0),
          "physiology_increment_positive":bool(fstat["ci95"][0]>0),
          "cells":cells
        }
    prior_both=all(result["targets"][t]["prior_increment_positive"] for t in ("valence","arousal"))
    phys_axes=[t for t in ("valence","arousal") if result["targets"][t]["physiology_increment_positive"]]
    if prior_both and len(phys_axes)==0:
        verdict="REPORT_PERSISTENCE_GENERALIZES__NO_PHYSIOLOGY_INCREMENT_UNDER_DOUBLE_HOLDOUT"
    elif prior_both and len(phys_axes)==2:
        verdict="REPORT_AND_PHYSIOLOGY_INCREMENT_GENERALIZE"
    else:
        verdict="MIXED_GENERALIZATION"
    result["verdict"]=verdict
    result["physiology_positive_axes"]=phys_axes
    (OUT/"o002_g1_joint_person_stimulus_generalization.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps({
      "verdict":verdict,
      "targets":{t:{
        "metrics":v["metrics"],
        "prior_increment":v["prior_increment_crossed_bootstrap"],
        "physiology_increment":v["physiology_increment_crossed_bootstrap"]
      } for t,v in result["targets"].items()}
    },indent=2))

if __name__=="__main__":
    main()
