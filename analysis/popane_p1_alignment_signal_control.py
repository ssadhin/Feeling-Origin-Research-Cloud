from __future__ import annotations
import json
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error

from popane_r1_independent_valence_replication import (
    ZIP, OUT, RNG_SEED, extract_rows, subject_folds,
    ridge_pipe, hgb_pipe, tune_ridge, bootstrap_subject
)

def make_shifted(feat, phys):
    z=feat.sort_values(["subject","segment","time_norm"]).copy()
    keep=[]
    for (s,g), q in z.groupby(["subject","segment"],sort=False):
        q=q.copy()
        n=len(q)
        if n<4:
            continue
        k=max(2,n//2)
        vals=q[phys].to_numpy(copy=True)
        q.loc[:,phys]=np.roll(vals,shift=k,axis=0)
        keep.append(q)
    if not keep:
        raise RuntimeError("No groups eligible for temporal shift")
    return pd.concat(keep,ignore_index=True)

def evaluate(real, shifted):
    key=["subject","segment","time_norm"]
    # Restrict aligned data to exactly the rows surviving shift eligibility.
    ids=shifted[key].copy()
    real2=real.merge(ids,on=key,how="inner")
    folds=subject_folds(real2.subject.unique())
    real2["fold"]=real2.subject.map(folds)
    shifted=shifted.copy(); shifted["fold"]=shifted.subject.map(folds)
    phys=[c for c in real2.columns if c not in {
        "subject","segment","time_norm","prior_affect","y_h0","y_h1","y_h2","y_h3","fold"
    }]
    out={}
    for learner in ("ridge","hgb"):
        rows=[]
        for f in range(10):
            for seg in sorted(real2.segment.unique()):
                te_r=real2[(real2.fold==f)&(real2.segment==seg)].copy()
                tr_r=real2[(real2.fold!=f)&(real2.segment!=seg)].copy()
                te_s=shifted[(shifted.fold==f)&(shifted.segment==seg)].copy()
                tr_s=shifted[(shifted.fold!=f)&(shifted.segment!=seg)].copy()
                if te_r.empty or te_s.empty: continue
                # deterministic key alignment
                te_r=te_r.sort_values(key); te_s=te_s.sort_values(key)
                tr_r=tr_r.sort_values(key); tr_s=tr_s.sort_values(key)
                if len(te_r)!=len(te_s) or len(tr_r)!=len(tr_s):
                    raise RuntimeError("Real/shift row mismatch")
                ytr=tr_r.prior_affect.to_numpy(float)
                yte=te_r.prior_affect.to_numpy(float)
                ctx=["time_norm"]; pf=ctx+phys
                if learner=="ridge":
                    ac=tune_ridge(tr_r,ctx,"prior_affect")
                    ar=tune_ridge(tr_r,pf,"prior_affect")
                    ash=tune_ridge(tr_s,pf,"prior_affect")
                    mc=ridge_pipe(ac).fit(tr_r[ctx],ytr)
                    mr=ridge_pipe(ar).fit(tr_r[pf],ytr)
                    ms=ridge_pipe(ash).fit(tr_s[pf],tr_s.prior_affect.to_numpy(float))
                else:
                    mc=hgb_pipe().fit(tr_r[ctx],ytr)
                    mr=hgb_pipe().fit(tr_r[pf],ytr)
                    ms=hgb_pipe().fit(tr_s[pf],tr_s.prior_affect.to_numpy(float))
                pc=mc.predict(te_r[ctx])
                pr=mr.predict(te_r[pf])
                ps=ms.predict(te_s[pf])
                for idx,yy,cv,rv,sv in zip(te_r.index,yte,pc,pr,ps):
                    rows.append((int(te_r.loc[idx,"subject"]),float(yy),float(cv),float(rv),float(sv)))
        p=pd.DataFrame(rows,columns=["subject","y","context","real","shifted"])
        subj={}
        for s,q in p.groupby("subject"):
            subj[int(s)]={
                "context":float(mean_absolute_error(q.y,q.context)),
                "real":float(mean_absolute_error(q.y,q.real)),
                "shifted":float(mean_absolute_error(q.y,q.shifted))
            }
        da={s:v["shifted"]-v["real"] for s,v in subj.items()}
        dc={s:v["context"]-v["real"] for s,v in subj.items()}
        ba=bootstrap_subject(da,71000+(0 if learner=="ridge" else 10))
        bc=bootstrap_subject(dc,72000+(0 if learner=="ridge" else 10))
        out[learner]={
            "n_rows":int(len(p)),
            "n_subjects":int(p.subject.nunique()),
            "context_mae":float(mean_absolute_error(p.y,p.context)),
            "aligned_phys_mae":float(mean_absolute_error(p.y,p.real)),
            "shifted_phys_mae":float(mean_absolute_error(p.y,p.shifted)),
            "delta_alignment":ba,
            "delta_context":bc,
            "alignment_positive":bool(ba["ci95"][0]>0),
            "context_increment_positive":bool(bc["ci95"][0]>0)
        }
    if out["ridge"]["alignment_positive"] and out["hgb"]["alignment_positive"] and (
        out["ridge"]["context_increment_positive"] or out["hgb"]["context_increment_positive"]
    ):
        verdict="ALIGNED_PHYSIOLOGY_SIGNAL_VALID"
    elif not out["ridge"]["alignment_positive"] and not out["hgb"]["alignment_positive"]:
        verdict="NO_ALIGNMENT_SIGNAL"
    else:
        verdict="WEAK_OR_MODEL_SPECIFIC_SIGNAL"
    return out,verdict

def main():
    if not ZIP.exists(): raise FileNotFoundError(ZIP)
    feat,qc=extract_rows()
    phys=[c for c in feat.columns if c not in {
        "subject","segment","time_norm","prior_affect","y_h0","y_h1","y_h2","y_h3"
    }]
    shifted=make_shifted(feat,phys)
    results,verdict=evaluate(feat,shifted)
    out={
      "status":"POPANE_P1_TEMPORAL_ALIGNMENT_SIGNAL_CONTROL",
      "protocol":"protocols/popane_p1_alignment_signal_control.json",
      "classification":"POST_PRIMARY_POSITIVE_CONTROL",
      "qc":qc,
      "shift_control_rows":int(len(shifted)),
      "results":results,
      "verdict":verdict,
      "firewall":"Concurrent/aligned signal-validity control only; no prospective, causal, bodily-necessity, or phenomenal inference."
    }
    (OUT/"popane_p1_alignment_signal_control.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
