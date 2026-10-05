from __future__ import annotations
import json
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error

from popane_r1_independent_valence_replication import (
    ZIP, OUT, HORIZONS, GAPS, extract_rows, subject_folds,
    ridge_pipe, hgb_pipe, tune_ridge, bootstrap_subject
)

META={"subject","segment","time_norm","prior_affect","y_h0","y_h1","y_h2","y_h3"}

def available_phys(feat):
    cols=[]
    for c in feat.columns:
        if c in META: continue
        v=pd.to_numeric(feat[c],errors="coerce").to_numpy(float)
        if np.isfinite(v).any():
            cols.append(c)
    return cols

def make_shifted(feat,phys):
    z=feat.sort_values(["subject","segment","time_norm"]).copy()
    pieces=[]
    for _,q in z.groupby(["subject","segment"],sort=False):
        q=q.copy()
        n=len(q)
        if n<4: continue
        k=max(2,n//2)
        q.loc[:,phys]=np.roll(q[phys].to_numpy(copy=True),shift=k,axis=0)
        pieces.append(q)
    if not pieces:
        raise RuntimeError("No groups eligible for shift")
    return pd.concat(pieces,ignore_index=True)

def eval_signal(feat,phys):
    shifted=make_shifted(feat,phys)
    key=["subject","segment","time_norm"]
    ids=shifted[key].copy()
    real=feat.merge(ids,on=key,how="inner")
    folds=subject_folds(real.subject.unique())
    real=real.copy(); shifted=shifted.copy()
    real["fold"]=real.subject.map(folds); shifted["fold"]=shifted.subject.map(folds)
    res={}
    for learner in ("ridge","hgb"):
        rows=[]
        for f in range(10):
            for seg in sorted(real.segment.unique()):
                te=real[(real.fold==f)&(real.segment==seg)].sort_values(key)
                tr=real[(real.fold!=f)&(real.segment!=seg)].sort_values(key)
                tes=shifted[(shifted.fold==f)&(shifted.segment==seg)].sort_values(key)
                trs=shifted[(shifted.fold!=f)&(shifted.segment!=seg)].sort_values(key)
                if te.empty: continue
                if len(te)!=len(tes) or len(tr)!=len(trs): raise RuntimeError("shift alignment mismatch")
                ctx=["time_norm"]; pf=ctx+phys
                ytr=tr.prior_affect.to_numpy(float); yte=te.prior_affect.to_numpy(float)
                if learner=="ridge":
                    ac=tune_ridge(tr,ctx,"prior_affect")
                    ar=tune_ridge(tr,pf,"prior_affect")
                    ash=tune_ridge(trs,pf,"prior_affect")
                    mc=ridge_pipe(ac).fit(tr[ctx],ytr)
                    mr=ridge_pipe(ar).fit(tr[pf],ytr)
                    ms=ridge_pipe(ash).fit(trs[pf],trs.prior_affect.to_numpy(float))
                else:
                    mc=hgb_pipe().fit(tr[ctx],ytr)
                    mr=hgb_pipe().fit(tr[pf],ytr)
                    ms=hgb_pipe().fit(trs[pf],trs.prior_affect.to_numpy(float))
                pc=mc.predict(te[ctx]); pr=mr.predict(te[pf]); ps=ms.predict(tes[pf])
                for idx,yy,cv,rv,sv in zip(te.index,yte,pc,pr,ps):
                    rows.append((int(te.loc[idx,"subject"]),float(yy),float(cv),float(rv),float(sv)))
        p=pd.DataFrame(rows,columns=["subject","y","context","aligned","shifted"])
        subj={}
        for s,q in p.groupby("subject"):
            subj[int(s)]={
                "context":float(mean_absolute_error(q.y,q.context)),
                "aligned":float(mean_absolute_error(q.y,q.aligned)),
                "shifted":float(mean_absolute_error(q.y,q.shifted))
            }
        da={s:v["shifted"]-v["aligned"] for s,v in subj.items()}
        dc={s:v["context"]-v["aligned"] for s,v in subj.items()}
        ba=bootstrap_subject(da,81000+(0 if learner=="ridge" else 10))
        bc=bootstrap_subject(dc,82000+(0 if learner=="ridge" else 10))
        res[learner]={
            "n_rows":int(len(p)),"n_subjects":int(p.subject.nunique()),
            "context_mae":float(mean_absolute_error(p.y,p.context)),
            "aligned_mae":float(mean_absolute_error(p.y,p.aligned)),
            "shifted_mae":float(mean_absolute_error(p.y,p.shifted)),
            "delta_alignment":ba,"delta_context":bc,
            "alignment_positive":bool(ba["ci95"][0]>0),
            "context_increment_positive":bool(bc["ci95"][0]>0)
        }
    valid=(res["ridge"]["alignment_positive"] and res["hgb"]["alignment_positive"] and
           (res["ridge"]["context_increment_positive"] or res["hgb"]["context_increment_positive"]))
    if valid:
        signal="SIGNAL_VALID"
    elif not res["ridge"]["alignment_positive"] and not res["hgb"]["alignment_positive"]:
        signal="NO_SIGNAL_VALIDATION"
    else:
        signal="WEAK_OR_MODEL_SPECIFIC_SIGNAL"
    return res,signal,int(len(shifted))

def eval_level(feat,phys):
    folds=subject_folds(feat.subject.unique())
    z=feat.copy(); z["fold"]=z.subject.map(folds)
    out={}; any_both_positive=False; no_positive_either=True; naive_better_all=True
    pos={"ridge":[],"hgb":[]}
    for h,gap in zip(HORIZONS,GAPS):
        target=f"y_h{h}"; hz={}
        for learner in ("ridge","hgb"):
            rows=[]
            for f in range(10):
                for seg in sorted(z.segment.unique()):
                    te=z[(z.fold==f)&(z.segment==seg)]
                    tr=z[(z.fold!=f)&(z.segment!=seg)]
                    if te.empty: continue
                    ctx=["prior_affect","time_norm"]; pf=ctx+phys
                    ytr=tr[target].to_numpy(float); yte=te[target].to_numpy(float)
                    if learner=="ridge":
                        ac=tune_ridge(tr,ctx,target); ap=tune_ridge(tr,pf,target)
                        mc=ridge_pipe(ac).fit(tr[ctx],ytr); mp=ridge_pipe(ap).fit(tr[pf],ytr)
                    else:
                        mc=hgb_pipe().fit(tr[ctx],ytr); mp=hgb_pipe().fit(tr[pf],ytr)
                    pc=mc.predict(te[ctx]); pp=mp.predict(te[pf])
                    for idx,yy,cv,pv in zip(te.index,yte,pc,pp):
                        rows.append((int(te.loc[idx,"subject"]),float(yy),float(te.loc[idx,"prior_affect"]),float(cv),float(pv)))
            p=pd.DataFrame(rows,columns=["subject","y","naive","context","phys"])
            subj={}
            for s,q in p.groupby("subject"):
                subj[int(s)]={
                    "naive":float(mean_absolute_error(q.y,q.naive)),
                    "context":float(mean_absolute_error(q.y,q.context)),
                    "phys":float(mean_absolute_error(q.y,q.phys))
                }
            dn={s:v["naive"]-v["phys"] for s,v in subj.items()}
            dc={s:v["context"]-v["phys"] for s,v in subj.items()}
            bn=bootstrap_subject(dn,83000+h*100+(0 if learner=="ridge" else 10))
            bc=bootstrap_subject(dc,84000+h*100+(0 if learner=="ridge" else 10))
            pnaive=bool(bn["ci95"][0]>0)
            pos[learner].append(pnaive)
            no_positive_either=no_positive_either and (not pnaive)
            naive_better_all=naive_better_all and (mean_absolute_error(p.y,p.naive)<mean_absolute_error(p.y,p.phys))
            hz[learner]={
                "n_rows":int(len(p)),"n_subjects":int(p.subject.nunique()),
                "naive_mae":float(mean_absolute_error(p.y,p.naive)),
                "context_mae":float(mean_absolute_error(p.y,p.context)),
                "physiology_mae":float(mean_absolute_error(p.y,p.phys)),
                "delta_naive_phys":bn,"delta_context_phys":bc,
                "physiology_positive_vs_naive":pnaive
            }
        both=hz["ridge"]["physiology_positive_vs_naive"] and hz["hgb"]["physiology_positive_vs_naive"]
        any_both_positive=any_both_positive or both
        out[f"gap_{gap}s"]=hz
    return out,{"any_both_positive":any_both_positive,"no_positive_either":no_positive_either,
                "naive_better_all":naive_better_all,"positive_by_learner":pos}

def main():
    if not ZIP.exists(): raise FileNotFoundError(ZIP)
    feat,qc=extract_rows()
    phys=available_phys(feat)
    signal,sig_state,shift_n=eval_signal(feat,phys)
    level,lev_state=eval_level(feat,phys)
    signal_valid=(sig_state=="SIGNAL_VALID")
    if signal_valid and lev_state["no_positive_either"] and lev_state["naive_better_all"]:
        verdict="VALID_SIGNAL_WITH_STRONG_BASELINE_DOMINANCE"
    elif signal_valid and lev_state["any_both_positive"]:
        verdict="VALID_SIGNAL_WITH_PHYSIOLOGY_INCREMENT"
    elif signal_valid:
        verdict="VALID_SIGNAL_MIXED_FORECAST"
    elif sig_state=="NO_SIGNAL_VALIDATION":
        verdict="NO_SIGNAL_VALIDATION"
    else:
        verdict="WEAK_OR_MODEL_SPECIFIC_SIGNAL"
    result={
      "status":"POPANE_P2_STUDY5_VALIDATION",
      "protocol":"protocols/popane_p2_study5_validation.json",
      "qc":qc,
      "available_physiology_features":phys,
      "n_available_physiology_features":len(phys),
      "shift_control_rows":shift_n,
      "signal_validity":signal,
      "signal_state":sig_state,
      "prospective_level":level,
      "level_decision_state":lev_state,
      "verdict":verdict,
      "firewall":"Dependency-resolution predictive validation only; no causal, body-independence, universal, or phenomenal inference."
    }
    (OUT/"popane_p2_study5_validation.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
