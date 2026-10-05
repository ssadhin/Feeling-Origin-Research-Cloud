from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error

from popane_r1_independent_valence_replication import (
    ZIP, OUT, HORIZONS, GAPS, extract_rows, subject_folds,
    ridge_pipe, hgb_pipe, tune_ridge
)

NBOOT=5000

def crossed_incomplete_boot(cell_delta, participants, segments, seed):
    rng=np.random.default_rng(seed)
    pids=list(participants); segs=list(segments)
    vals=np.empty(NBOOT,float)
    keys=list(cell_delta.keys())
    for b in range(NBOOT):
        pc=Counter(rng.choice(pids,size=len(pids),replace=True).tolist())
        sc=Counter(rng.choice(segs,size=len(segs),replace=True).tolist())
        num=0.0; den=0.0
        for (p,s) in keys:
            w=pc.get(p,0)*sc.get(s,0)
            if w:
                num += w*cell_delta[(p,s)]
                den += w
        vals[b]=num/den if den>0 else np.nan
    vals=vals[np.isfinite(vals)]
    point=float(np.mean(list(cell_delta.values())))
    return {"mean_equal_observed_cell":point,
            "ci95":[float(np.percentile(vals,2.5)),float(np.percentile(vals,97.5))],
            "n_observed_cells":int(len(cell_delta)),
            "n_boot_valid":int(len(vals))}

def main():
    if not ZIP.exists():
        raise FileNotFoundError(ZIP)
    feat,qc=extract_rows()
    if len(feat)<500 or feat.subject.nunique()<20 or feat.segment.nunique()<2:
        out={"status":"POPANE_R4_CROSSED_UNCERTAINTY","verdict":"FAIL_TECHNICAL_QC","qc":qc}
        (OUT/"popane_r4_crossed_uncertainty.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
        print(json.dumps(out,indent=2)); return

    phys=[c for c in feat.columns if c not in {"subject","segment","time_norm","prior_affect","y_h0","y_h1","y_h2","y_h3"}]
    folds=subject_folds(feat.subject.unique())
    feat=feat.copy(); feat["fold"]=feat.subject.map(folds)
    participants=sorted(int(x) for x in feat.subject.unique())
    segments=sorted(str(x) for x in feat.segment.unique())

    results={}
    all_negative=True
    any_positive=False
    for hi,(h,gap) in enumerate(zip(HORIZONS,GAPS)):
        target=f"y_h{h}"
        hz={}
        for li,learner in enumerate(("ridge","hgb")):
            preds=[]
            for f in range(10):
                for seg in segments:
                    te=feat[(feat["fold"]==f)&(feat.segment==seg)]
                    if te.empty:
                        continue
                    tr=feat[(feat["fold"]!=f)&(feat.segment!=seg)]
                    if tr.subject.nunique()<10 or len(tr)<100:
                        continue
                    pf=["time_norm","prior_affect"]+phys
                    ytr=tr[target].to_numpy(float); yte=te[target].to_numpy(float)
                    if learner=="ridge":
                        a=tune_ridge(tr,pf,target)
                        mp=ridge_pipe(a).fit(tr[pf],ytr)
                    else:
                        mp=hgb_pipe().fit(tr[pf],ytr)
                    pp=mp.predict(te[pf])
                    for idx,yy,pv in zip(te.index,yte,pp):
                        preds.append((int(te.loc[idx,"subject"]),str(te.loc[idx,"segment"]),
                                      float(yy),float(te.loc[idx,"prior_affect"]),float(pv)))
            pr=pd.DataFrame(preds,columns=["subject","segment","y","naive","phys"])
            if pr.empty:
                raise RuntimeError(f"No predictions gap={gap} learner={learner}")
            cell={}
            for (p,s),q in pr.groupby(["subject","segment"]):
                mn=float(mean_absolute_error(q.y,q.naive))
                mp=float(mean_absolute_error(q.y,q.phys))
                cell[(int(p),str(s))]=mn-mp
            bs=crossed_incomplete_boot(cell,participants,segments,81000+hi*100+li)
            neg=bs["ci95"][1]<0
            pos=bs["ci95"][0]>0
            all_negative=all_negative and neg
            any_positive=any_positive or pos
            hz[learner]={
                "row_weighted_naive_mae":float(mean_absolute_error(pr.y,pr.naive)),
                "row_weighted_physiology_mae":float(mean_absolute_error(pr.y,pr.phys)),
                "delta_naive_phys_crossed":bs,
                "strictly_negative":bool(neg),
                "strictly_positive":bool(pos)
            }
        results[f"gap_{gap}s"]=hz

    if all_negative:
        verdict="CROSSED_UNCERTAINTY_STRONGLY_SUPPORTS_R1"
    elif not any_positive:
        verdict="CROSSED_UNCERTAINTY_SUPPORTS_NONPOSITIVE_PATTERN"
    else:
        verdict="CROSSED_UNCERTAINTY_MIXED"

    out={
      "status":"POPANE_R4_CROSSED_PARTICIPANT_SEGMENT_UNCERTAINTY",
      "protocol":"protocols/popane_r4_crossed_uncertainty.json",
      "classification":"POST_PRIMARY_SENSITIVITY",
      "qc":qc,
      "results":results,
      "verdict":verdict,
      "firewall":"Statistical robustness sensitivity only; no causal or phenomenal inference."
    }
    (OUT/"popane_r4_crossed_uncertainty.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
