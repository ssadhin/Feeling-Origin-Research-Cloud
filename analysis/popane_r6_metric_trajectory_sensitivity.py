from __future__ import annotations
import json
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

from popane_r1_independent_valence_replication import (
    ZIP, OUT, HORIZONS, GAPS, extract_rows, subject_folds,
    ridge_pipe, hgb_pipe, tune_ridge
)

NBOOT=5000

def ccc_from_arrays(y, x):
    y=np.asarray(y,dtype=float); x=np.asarray(x,dtype=float)
    my=float(np.mean(y)); mx=float(np.mean(x))
    vy=float(np.mean(y*y)-my*my)
    vx=float(np.mean(x*x)-mx*mx)
    cov=float(np.mean(y*x)-my*mx)
    den=vy+vx+(my-mx)**2
    return float(2*cov/den) if den>0 else float("nan")

def subject_sufficient(pr, pred_col):
    rows={}
    for s,q in pr.groupby("subject"):
        y=q["y"].to_numpy(float); x=q[pred_col].to_numpy(float)
        rows[int(s)]={
            "n":float(len(q)),
            "sum_y":float(np.sum(y)),
            "sum_y2":float(np.sum(y*y)),
            "sum_x":float(np.sum(x)),
            "sum_x2":float(np.sum(x*x)),
            "sum_xy":float(np.sum(x*y)),
            "sse":float(np.sum((y-x)**2))
        }
    return rows

def metrics_from_weighted(stats, counts):
    n=sy=sy2=sx=sx2=sxy=sse=0.0
    for s,w in counts.items():
        if w<=0: continue
        z=stats[s]
        n += w*z["n"]; sy += w*z["sum_y"]; sy2 += w*z["sum_y2"]
        sx += w*z["sum_x"]; sx2 += w*z["sum_x2"]; sxy += w*z["sum_xy"]
        sse += w*z["sse"]
    my=sy/n; mx=sx/n
    vy=sy2/n-my*my; vx=sx2/n-mx*mx; cov=sxy/n-my*mx
    den=vy+vx+(my-mx)**2
    ccc=(2*cov/den) if den>0 else np.nan
    rmse=np.sqrt(sse/n)
    return float(rmse),float(ccc)

def bootstrap_contrasts(pr, seed):
    subjects=sorted(int(s) for s in pr.subject.unique())
    stats={m:subject_sufficient(pr,m) for m in ("naive","context","phys")}
    rng=np.random.default_rng(seed)
    vals={k:np.empty(NBOOT,float) for k in (
        "rmse_naive_phys","rmse_context_phys","ccc_phys_naive","ccc_phys_context"
    )}
    for b in range(NBOOT):
        draw=rng.choice(subjects,size=len(subjects),replace=True)
        u,c=np.unique(draw,return_counts=True)
        counts={int(a):int(n) for a,n in zip(u,c)}
        rn,cn=metrics_from_weighted(stats["naive"],counts)
        rc,cc=metrics_from_weighted(stats["context"],counts)
        rp,cp=metrics_from_weighted(stats["phys"],counts)
        vals["rmse_naive_phys"][b]=rn-rp
        vals["rmse_context_phys"][b]=rc-rp
        vals["ccc_phys_naive"][b]=cp-cn
        vals["ccc_phys_context"][b]=cp-cc
    out={}
    for k,v in vals.items():
        v=v[np.isfinite(v)]
        out[k]={"ci95":[float(np.percentile(v,2.5)),float(np.percentile(v,97.5))],
                "n_boot_valid":int(len(v))}
    return out

def point_metrics(pr):
    out={}
    y=pr["y"].to_numpy(float)
    for m in ("naive","context","phys"):
        x=pr[m].to_numpy(float)
        out[m]={
            "mae":float(mean_absolute_error(y,x)),
            "rmse":float(np.sqrt(mean_squared_error(y,x))),
            "ccc":ccc_from_arrays(y,x)
        }
    out["delta_rmse_naive_phys"]=out["naive"]["rmse"]-out["phys"]["rmse"]
    out["delta_rmse_context_phys"]=out["context"]["rmse"]-out["phys"]["rmse"]
    out["delta_ccc_phys_naive"]=out["phys"]["ccc"]-out["naive"]["ccc"]
    out["delta_ccc_phys_context"]=out["phys"]["ccc"]-out["context"]["ccc"]
    return out

def main():
    if not ZIP.exists():
        raise FileNotFoundError(ZIP)
    feat,qc=extract_rows()
    if len(feat)<500 or feat.subject.nunique()<20 or feat.segment.nunique()<2:
        out={"status":"POPANE_R6_METRIC_TRAJECTORY_SENSITIVITY","verdict":"FAIL_TECHNICAL_QC","qc":qc}
        (OUT/"popane_r6_metric_trajectory_sensitivity.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
        print(json.dumps(out,indent=2)); return

    phys=[c for c in feat.columns if c not in {"subject","segment","time_norm","prior_affect","y_h0","y_h1","y_h2","y_h3"}]
    folds=subject_folds(feat.subject.unique())
    feat=feat.copy(); feat["fold"]=feat.subject.map(folds)

    results={}
    all_rmse_negative=True
    ccc_both_horizons=[]
    any_ccc_positive=False

    for hi,(h,gap) in enumerate(zip(HORIZONS,GAPS)):
        target=f"y_h{h}"
        hz={}
        positive_by_learner={}
        for li,learner in enumerate(("ridge","hgb")):
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
                    pc=mc.predict(te[ctx]); pp=mp.predict(te[pf]); pn=te["prior_affect"].to_numpy(float)
                    for idx,yy,nv,cv,pv in zip(te.index,yte,pn,pc,pp):
                        preds.append((int(te.loc[idx,"subject"]),float(yy),float(nv),float(cv),float(pv)))
            pr=pd.DataFrame(preds,columns=["subject","y","naive","context","phys"])
            if pr.empty: raise RuntimeError(f"No predictions gap={gap} learner={learner}")
            pt=point_metrics(pr)
            bs=bootstrap_contrasts(pr,101000+hi*100+li*10)
            pt["bootstrap"]=bs
            rmse_neg=bs["rmse_naive_phys"]["ci95"][1] < 0
            ccc_pos=bs["ccc_phys_naive"]["ci95"][0] > 0
            pt["rmse_naive_phys_strictly_negative"]=bool(rmse_neg)
            pt["ccc_phys_naive_strictly_positive"]=bool(ccc_pos)
            hz[learner]=pt
            all_rmse_negative=all_rmse_negative and rmse_neg
            positive_by_learner[learner]=ccc_pos
            any_ccc_positive=any_ccc_positive or ccc_pos
        if positive_by_learner["ridge"] and positive_by_learner["hgb"]:
            ccc_both_horizons.append(gap)
        results[f"gap_{gap}s"]=hz

    if ccc_both_horizons:
        verdict="PHYSIOLOGY_TRACKING_RESCUE"
    elif all_rmse_negative and not any_ccc_positive:
        verdict="METRIC_ROBUST_PERSISTENCE_DOMINANCE"
    elif any_ccc_positive:
        verdict="MODEL_SPECIFIC_TRACKING_SIGNAL"
    else:
        verdict="MIXED_METRIC_RESULT"

    out={
      "status":"POPANE_R6_METRIC_TRAJECTORY_SENSITIVITY",
      "protocol":"protocols/popane_r6_metric_trajectory_sensitivity.json",
      "classification":"POST_PRIMARY_SENSITIVITY",
      "qc":qc,
      "results":results,
      "ccc_both_learners_positive_horizons_sec":ccc_both_horizons,
      "verdict":verdict,
      "firewall":"Metric/trajectory sensitivity only; no causal, bodily-necessity, universal, or phenomenal inference."
    }
    (OUT/"popane_r6_metric_trajectory_sensitivity.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
    slim={"verdict":verdict,"ccc_both_learners_positive_horizons_sec":ccc_both_horizons,"results":{}}
    for h,v in results.items():
        slim["results"][h]={}
        for learner,z in v.items():
            slim["results"][h][learner]={
              "naive":z["naive"],"context":z["context"],"phys":z["phys"],
              "bootstrap":z["bootstrap"]
            }
    print(json.dumps(slim,indent=2))

if __name__=="__main__":
    main()
