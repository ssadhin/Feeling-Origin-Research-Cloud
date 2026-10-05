from __future__ import annotations
import json, os
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error

from popane_r1_independent_valence_replication import (
    ZIP, OUT, RNG_SEED, extract_rows, subject_folds,
    ridge_pipe, hgb_pipe, tune_ridge, bootstrap_subject
)

def add_shifted_features(feat, phys):
    z=feat.sort_values(["subject","segment","time_norm"]).copy()
    shifted=z[phys].copy()
    for (_, _), idx in z.groupby(["subject","segment"],sort=False).groups.items():
        ids=list(idx)
        n=len(ids)
        k=max(1,n//2)
        vals=z.loc[ids,phys].to_numpy()
        shifted.loc[ids,phys]=np.roll(vals,shift=k,axis=0)
    for c in phys:
        z["shift_"+c]=shifted[c].to_numpy()
    return z.reset_index(drop=True)

def main():
    if not ZIP.exists():
        raise FileNotFoundError(ZIP)
    feat,qc=extract_rows()
    if len(feat)<500 or feat.subject.nunique()<20 or feat.segment.nunique()<2:
        out={"status":"POPANE_R3_ALIGNMENT_SIGNAL_CONTROL","verdict":"FAIL_TECHNICAL_QC","qc":qc}
        (OUT/"popane_r3_alignment_signal_control.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
        print(json.dumps(out,indent=2)); return

    phys=[c for c in feat.columns if c not in {"subject","segment","time_norm","prior_affect","y_h0","y_h1","y_h2","y_h3"}]
    feat=add_shifted_features(feat,phys)
    folds=subject_folds(feat.subject.unique())
    feat["fold"]=feat.subject.map(folds)

    result={}
    positives={}
    for learner in ("ridge","hgb"):
        preds=[]
        for f in range(10):
            for seg in sorted(feat.segment.unique()):
                te=feat[(feat["fold"]==f)&(feat.segment==seg)]
                if te.empty:
                    continue
                tr=feat[(feat["fold"]!=f)&(feat.segment!=seg)]
                if tr.subject.nunique()<10 or len(tr)<100:
                    continue

                timef=["time_norm"]
                realf=["time_norm"]+phys
                shiftf=["time_norm"]+["shift_"+c for c in phys]
                ytr=tr["prior_affect"].to_numpy(float)
                yte=te["prior_affect"].to_numpy(float)

                if learner=="ridge":
                    at=tune_ridge(tr,timef,"prior_affect")
                    ar=tune_ridge(tr,realf,"prior_affect")
                    ash=tune_ridge(tr,shiftf,"prior_affect")
                    mt=ridge_pipe(at).fit(tr[timef],ytr)
                    mr=ridge_pipe(ar).fit(tr[realf],ytr)
                    ms=ridge_pipe(ash).fit(tr[shiftf],ytr)
                else:
                    mt=hgb_pipe().fit(tr[timef],ytr)
                    mr=hgb_pipe().fit(tr[realf],ytr)
                    ms=hgb_pipe().fit(tr[shiftf],ytr)

                pt=mt.predict(te[timef])
                pr=mr.predict(te[realf])
                ps=ms.predict(te[shiftf])

                for idx,yy,tv,rv,sv in zip(te.index,yte,pt,pr,ps):
                    preds.append((int(te.loc[idx,"subject"]),float(yy),float(tv),float(rv),float(sv)))

        prd=pd.DataFrame(preds,columns=["subject","y","time","real","shift"])
        if prd.empty:
            raise RuntimeError("No R3 predictions")

        subj={}
        for s,q in prd.groupby("subject"):
            subj[int(s)]={
                "time":float(mean_absolute_error(q.y,q.time)),
                "real":float(mean_absolute_error(q.y,q.real)),
                "shift":float(mean_absolute_error(q["y"],q["shift"]))
            }

        d_sr={s:v["shift"]-v["real"] for s,v in subj.items()}
        d_tr={s:v["time"]-v["real"] for s,v in subj.items()}
        bsr=bootstrap_subject(d_sr,71000+(0 if learner=="ridge" else 10))
        btr=bootstrap_subject(d_tr,72000+(0 if learner=="ridge" else 10))
        metrics={
            "n_rows":int(len(prd)),
            "n_subjects":int(prd.subject.nunique()),
            "time_only_mae":float(mean_absolute_error(prd.y,prd.time)),
            "real_physiology_mae":float(mean_absolute_error(prd.y,prd.real)),
            "shifted_physiology_mae":float(mean_absolute_error(prd.y,prd.shift)),
            "delta_shift_real":bsr,
            "delta_time_real":btr,
            "aligned_signal_positive":bool(bsr["ci95"][0]>0)
        }
        result[learner]=metrics
        positives[learner]=metrics["aligned_signal_positive"]

    if positives["ridge"] and positives["hgb"]:
        verdict="ALIGNED_SIGNAL_REPLICATED"
    elif positives["ridge"] or positives["hgb"]:
        verdict="MODEL_SPECIFIC_ALIGNED_SIGNAL"
    else:
        verdict="NO_DETECTABLE_ALIGNED_SIGNAL"

    out={
        "status":"POPANE_R3_ALIGNMENT_SIGNAL_CONTROL",
        "protocol":"protocols/popane_r3_alignment_signal_control.json",
        "classification":"EXPLORATORY_POST_PRIMARY",
        "qc":qc,
        "models":result,
        "verdict":verdict,
        "firewall":"Concurrent/recent valence alignment diagnostic only; no causal, bodily-necessity, or phenomenal inference."
    }
    (OUT/"popane_r3_alignment_signal_control.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
