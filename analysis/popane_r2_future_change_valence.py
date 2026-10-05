from __future__ import annotations
import json, os
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error

from analysis.popane_r1_independent_valence_replication import (
    ZIP, OUT, HORIZONS, GAPS, RNG_SEED,
    extract_rows, subject_folds, ridge_pipe, hgb_pipe, tune_ridge, bootstrap_subject
)

def primary_joint_change(feat):
    phys=[c for c in feat.columns if c not in {"subject","segment","time_norm","prior_affect","y_h0","y_h1","y_h2","y_h3"}]
    folds=subject_folds(feat.subject.unique())
    feat=feat.copy(); feat["fold"]=feat.subject.map(folds)
    res={}
    pos={"ridge":[],"hgb":[]}
    zero_means={"ridge":[],"hgb":[]}
    zero_positive={"ridge":[],"hgb":[]}
    for h,gap in zip(HORIZONS,GAPS):
        target=f"delta_h{h}"
        feat[target]=feat[f"y_h{h}"]-feat["prior_affect"]
        hz={}
        for learner in ("ridge","hgb"):
            preds=[]
            for f in range(10):
                for seg in sorted(feat.segment.unique()):
                    te=feat[(feat["fold"]==f)&(feat.segment==seg)]
                    if te.empty: continue
                    tr=feat[(feat["fold"]!=f)&(feat.segment!=seg)]
                    if tr.subject.nunique()<10 or len(tr)<100: continue
                    ytr=tr[target].to_numpy(float); yte=te[target].to_numpy(float)
                    ctx=["prior_affect","time_norm"]; pf=ctx+phys
                    if learner=="ridge":
                        ac=tune_ridge(tr,ctx,target); ap=tune_ridge(tr,pf,target)
                        mc=ridge_pipe(ac).fit(tr[ctx],ytr)
                        mp=ridge_pipe(ap).fit(tr[pf],ytr)
                    else:
                        mc=hgb_pipe().fit(tr[ctx],ytr)
                        mp=hgb_pipe().fit(tr[pf],ytr)
                    pc=mc.predict(te[ctx]); pp=mp.predict(te[pf]); p0=np.zeros_like(yte)
                    for idx,yy,cv,pv,zv in zip(te.index,yte,pc,pp,p0):
                        preds.append((int(te.loc[idx,"subject"]),float(yy),float(zv),float(cv),float(pv)))
            pr=pd.DataFrame(preds,columns=["subject","y","zero","context","phys"])
            if pr.empty: raise RuntimeError(f"No predictions gap={gap} learner={learner}")
            subj={}
            for s,q in pr.groupby("subject"):
                subj[int(s)]={
                    "zero":float(mean_absolute_error(q.y,q.zero)),
                    "context":float(mean_absolute_error(q.y,q.context)),
                    "phys":float(mean_absolute_error(q.y,q.phys))
                }
            dz={s:v["zero"]-v["phys"] for s,v in subj.items()}
            dc={s:v["context"]-v["phys"] for s,v in subj.items()}
            bz=bootstrap_subject(dz,61000+h*100+(0 if learner=="ridge" else 10))
            bc=bootstrap_subject(dc,62000+h*100+(0 if learner=="ridge" else 10))
            metrics={
                "n_rows":int(len(pr)),"n_subjects":int(pr.subject.nunique()),
                "zero_change_mae":float(mean_absolute_error(pr.y,pr.zero)),
                "context_mae":float(mean_absolute_error(pr.y,pr.context)),
                "physiology_mae":float(mean_absolute_error(pr.y,pr.phys)),
                "delta_zero_phys":bz,
                "delta_context_phys":bc,
                "physiology_positive_vs_context":bool(bc["ci95"][0]>0),
                "physiology_positive_vs_zero":bool(bz["ci95"][0]>0)
            }
            hz[learner]=metrics
            pos[learner].append(metrics["physiology_positive_vs_context"])
            zero_means[learner].append(bz["mean"])
            zero_positive[learner].append(metrics["physiology_positive_vs_zero"])
        res[f"gap_{gap}s"]=hz

    clear=any(pos["ridge"][i] and pos["hgb"][i] for i in range(4))
    any_ctx=any(pos["ridge"]) or any(pos["hgb"])
    if clear:
        verdict="CLEAR_EXTERNAL_CHANGE_SIGNAL"
    elif not any_ctx:
        verdict="NO_EXTERNAL_CHANGE_INCREMENT"
    else:
        verdict="MIXED_EXTERNAL_CHANGE_RESULT"
    strong_zero=all(m<=0 for l in zero_means.values() for m in l) and not any(zero_positive["ridge"]) and not any(zero_positive["hgb"])
    return res,verdict,{"positive_vs_context":pos,"zero_means":zero_means,"positive_vs_zero":zero_positive,
                        "strong_zero_change_dominance":bool(strong_zero)}

def main():
    if not ZIP.exists(): raise FileNotFoundError(ZIP)
    feat,qc=extract_rows()
    if len(feat)<500 or feat.subject.nunique()<20 or feat.segment.nunique()<2:
        out={"status":"POPANE_R2","verdict":"FAIL_TECHNICAL_QC","qc":qc}
    else:
        primary,verdict,dec=primary_joint_change(feat)
        out={"status":"POPANE_R2_INDEPENDENT_FUTURE_CHANGE_VALENCE",
             "protocol":"protocols/popane_r2_future_change_valence.json",
             "classification":"EXPLORATORY_POST_PRIMARY",
             "qc":qc,"primary_joint_change":primary,"decision_state":dec,"verdict":verdict,
             "firewall":"Change-prediction diagnostic only; no causal, bodily-necessity, or phenomenal inference."}
    (OUT/"popane_r2_future_change_valence.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
