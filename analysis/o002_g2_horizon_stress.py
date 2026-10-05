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
SHIFTS=[1,2,3]

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

def tune_alpha(train,target_col,target_axis,spec,phys):
    cols=cols_for(target_axis,spec,phys)
    y=train[target_col].to_numpy(float)
    groups=train.subject.to_numpy()
    cv=GroupKFold(n_splits=min(4,len(np.unique(groups))))
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
    return {"mean":float(np.mean(delta_mat)),
            "ci95":[float(np.percentile(vals,2.5)),float(np.percentile(vals,97.5))]}

def horizon_frame(df,h):
    z=df.sort_values(["subject","video_id","time_norm"]).copy()
    g=z.groupby(["subject","video_id"],sort=False)
    z["target_valence"]=g["y_valence"].shift(-h)
    z["target_arousal"]=g["y_arousal"].shift(-h)
    z=z.dropna(subset=["target_valence","target_arousal"]).reset_index(drop=True)
    return z

def main():
    OUT.mkdir(exist_ok=True)
    base=pd.read_json(IN,lines=True)
    base["video_id"]=base["video_id"].astype(str)
    subjects=sorted(base.subject.unique())
    videos=sorted(base.video_id.unique(),key=lambda x:int(x))
    phys=sorted(c for c in base.columns if c.startswith("phys_"))
    if len(subjects)!=30 or videos!=[str(i) for i in range(1,9)] or len(phys)!=29:
        raise RuntimeError(f"Frozen shape mismatch subjects={len(subjects)} videos={videos} phys={len(phys)}")
    specs=["context_only","prior","physiology"]
    result={
      "status":"O002_G2_PROSPECTIVE_HORIZON_STRESS",
      "protocol":"protocols/o002_g2_horizon_stress.json",
      "source_rows":int(len(base)),
      "n_subjects":len(subjects),
      "n_videos":len(videos),
      "horizons":{},
      "firewall":"Post-primary predictive robustness only; no causal, physiological-irrelevance, or phenomenal inference."
    }
    any_phys_positive=False
    all_phys_negative=True
    prior_all=True
    for hi,h in enumerate(SHIFTS):
        df=horizon_frame(base,h)
        key=f"shift_{h}_gap_{10*h+1}s"
        hz={"shift_rows":h,"predictor_end_to_target_start_gap_sec":10*h+1,
            "rows":int(len(df)),"targets":{}}
        for ti,target in enumerate(("valence","arousal")):
            target_col="target_"+target
            cells={}
            matrices={spec:np.full((len(subjects),len(videos)),np.nan) for spec in specs}
            row_weighted={spec:{"y":[],"pred":[]} for spec in specs}
            for si,sub in enumerate(subjects):
                for vi,vid in enumerate(videos):
                    train=df[(df.subject!=sub)&(df.video_id!=vid)].reset_index(drop=True)
                    test=df[(df.subject==sub)&(df.video_id==vid)].reset_index(drop=True)
                    if len(test)==0:
                        raise RuntimeError(f"Missing test cell h={h} {sub} video {vid}")
                    yte=test[target_col].to_numpy(float)
                    ck=f"{sub}|video-{vid}"
                    cells[ck]={"n_test":int(len(test)),"models":{}}
                    print(f"h={h} {target} subject {si+1}/{len(subjects)} {sub} video {vid}",flush=True)
                    for spec in specs:
                        alpha=tune_alpha(train,target_col,target,spec,phys)
                        cols=cols_for(target,spec,phys)
                        mdl=make_pipe(alpha).fit(train[cols],train[target_col].to_numpy(float))
                        pred=mdl.predict(test[cols])
                        mae=float(mean_absolute_error(yte,pred))
                        matrices[spec][si,vi]=mae
                        cells[ck]["models"][spec]={"mae":mae,"alpha":alpha}
                        row_weighted[spec]["y"].extend(yte.tolist())
                        row_weighted[spec]["pred"].extend(pred.tolist())
            prior_delta=matrices["context_only"]-matrices["prior"]
            phys_delta=matrices["prior"]-matrices["physiology"]
            pstat=crossed_boot(prior_delta,201000+100*hi+ti)
            fstat=crossed_boot(phys_delta,202000+100*hi+ti)
            ppos=bool(pstat["ci95"][0]>0)
            fpos=bool(fstat["ci95"][0]>0)
            fneg=bool(fstat["ci95"][1]<0)
            prior_all=prior_all and ppos
            any_phys_positive=any_phys_positive or fpos
            all_phys_negative=all_phys_negative and fneg
            metrics={}
            for spec in specs:
                yy=np.asarray(row_weighted[spec]["y"],float)
                pp=np.asarray(row_weighted[spec]["pred"],float)
                metrics[spec]={
                  "row_weighted_mae":float(mean_absolute_error(yy,pp)),
                  "mean_cell_mae":float(np.mean(matrices[spec]))
                }
            hz["targets"][target]={
              "metrics":metrics,
              "prior_increment_crossed_bootstrap":pstat,
              "physiology_increment_crossed_bootstrap":fstat,
              "prior_increment_positive":ppos,
              "physiology_increment_positive":fpos,
              "physiology_significant_degradation":fneg,
              "cells":cells
            }
        result["horizons"][key]=hz
    if prior_all and all_phys_negative:
        verdict="REPORT_PERSISTENCE_HORIZON_GENERALIZES__STRONG_PHYSIOLOGY_DEGRADATION"
    elif prior_all and not any_phys_positive:
        verdict="REPORT_PERSISTENCE_HORIZON_GENERALIZES__NO_PHYSIOLOGY_INCREMENT_ACROSS_HORIZONS"
    elif any_phys_positive:
        verdict="PHYSIOLOGY_INCREMENT_AT_ONE_OR_MORE_HORIZONS__MIXED_REQUIRES_REPLICATION"
    else:
        verdict="MIXED_HORIZON_RESULT"
    result["verdict"]=verdict
    result["prior_positive_all_six"]=prior_all
    result["physiology_positive_any"]=any_phys_positive
    result["physiology_degradation_all_six"]=all_phys_negative
    (OUT/"o002_g2_horizon_stress.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    summary={"verdict":verdict,"horizons":{}}
    for k,hz in result["horizons"].items():
        summary["horizons"][k]={}
        for t,v in hz["targets"].items():
            summary["horizons"][k][t]={
              "metrics":v["metrics"],
              "prior_increment":v["prior_increment_crossed_bootstrap"],
              "physiology_increment":v["physiology_increment_crossed_bootstrap"]
            }
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
