from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

IN=Path("results_snapshots/o002_feature_rows_run-37217735818.jsonl")
OUT=Path("results"); OUT.mkdir(exist_ok=True)
ALPHAS=[0.1,1.0,10.0,100.0,1000.0]
NBOOT=5000
SHIFTS=[0,1,2,3]
GAPS=[1,11,21,31]

def ridge_pipe(a):
    return Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler()),("m",Ridge(alpha=a))])

def hgb_pipe():
    return Pipeline([("imp",SimpleImputer(strategy="median")),
                     ("m",HistGradientBoostingRegressor(max_iter=150,learning_rate=0.05,max_leaf_nodes=15,
                                                        l2_regularization=1.0,random_state=1701))])

def tune(train,features,target):
    groups=train.subject.to_numpy()
    cv=GroupKFold(n_splits=min(4,len(np.unique(groups))))
    X=train[features]; y=train[target].to_numpy(float)
    scores={a:[] for a in ALPHAS}
    for tr,va in cv.split(X,y,groups):
        for a in ALPHAS:
            p=ridge_pipe(a).fit(X.iloc[tr],y[tr]).predict(X.iloc[va])
            scores[a].append(mean_absolute_error(y[va],p))
    return min(ALPHAS,key=lambda a:(float(np.mean(scores[a])),a))

def horizon_frame(base,h,axis):
    z=base.sort_values(["subject","video_id","time_norm"]).copy()
    g=z.groupby(["subject","video_id"],sort=False)
    z["future_y"]=g["y_"+axis].shift(-h)
    return z.dropna(subset=["future_y"]).reset_index(drop=True)

def ccc_from_moments(n,sy,sy2,sx,sx2,sxy):
    my=sy/n; mx=sx/n
    vy=sy2/n-my*my
    vx=sx2/n-mx*mx
    cov=sxy/n-my*mx
    den=vy+vx+(my-mx)**2
    return float(2*cov/den) if den>0 else float("nan")

def cell_stats(pr,pred_col):
    out={}
    for (s,v),q in pr.groupby(["subject","video_id"]):
        y=q["y"].to_numpy(float); x=q[pred_col].to_numpy(float)
        out[(int(s),str(v))]={
            "n":float(len(q)),
            "sy":float(np.sum(y)),
            "sy2":float(np.sum(y*y)),
            "sx":float(np.sum(x)),
            "sx2":float(np.sum(x*x)),
            "sxy":float(np.sum(x*y)),
            "sse":float(np.sum((y-x)**2))
        }
    return out

def weighted_metrics(stats,pc,vc):
    n=sy=sy2=sx=sx2=sxy=sse=0.0
    for (s,v),z in stats.items():
        w=pc.get(s,0)*vc.get(v,0)
        if not w: continue
        n += w*z["n"]; sy += w*z["sy"]; sy2 += w*z["sy2"]
        sx += w*z["sx"]; sx2 += w*z["sx2"]; sxy += w*z["sxy"]; sse += w*z["sse"]
    if n<=0:
        return float("nan"),float("nan")
    rmse=float(np.sqrt(sse/n))
    ccc=ccc_from_moments(n,sy,sy2,sx,sx2,sxy)
    return rmse,ccc

def crossed_metric_bootstrap(pr,subjects,videos,seed):
    stats={m:cell_stats(pr,m) for m in ("naive","context","phys")}
    rng=np.random.default_rng(seed)
    vals={k:np.empty(NBOOT,float) for k in (
        "rmse_naive_phys","rmse_context_phys","ccc_phys_naive","ccc_phys_context"
    )}
    for b in range(NBOOT):
        ps=rng.choice(subjects,size=len(subjects),replace=True)
        vs=rng.choice(videos,size=len(videos),replace=True)
        pc=Counter(int(x) for x in ps)
        vc=Counter(str(x) for x in vs)
        rn,cn=weighted_metrics(stats["naive"],pc,vc)
        rc,cc=weighted_metrics(stats["context"],pc,vc)
        rp,cp=weighted_metrics(stats["phys"],pc,vc)
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

def ccc_arrays(y,x):
    y=np.asarray(y,float); x=np.asarray(x,float)
    return ccc_from_moments(len(y),float(y.sum()),float((y*y).sum()),
                            float(x.sum()),float((x*x).sum()),float((x*y).sum()))

def point_metrics(pr):
    y=pr["y"].to_numpy(float)
    out={}
    for m in ("naive","context","phys"):
        x=pr[m].to_numpy(float)
        out[m]={
            "mae":float(mean_absolute_error(y,x)),
            "rmse":float(np.sqrt(mean_squared_error(y,x))),
            "ccc":ccc_arrays(y,x)
        }
    out["delta_rmse_naive_phys"]=out["naive"]["rmse"]-out["phys"]["rmse"]
    out["delta_rmse_context_phys"]=out["context"]["rmse"]-out["phys"]["rmse"]
    out["delta_ccc_phys_naive"]=out["phys"]["ccc"]-out["naive"]["ccc"]
    out["delta_ccc_phys_context"]=out["phys"]["ccc"]-out["context"]["ccc"]
    return out

def main():
    base=pd.read_json(IN,lines=True)
    base["video_id"]=base["video_id"].astype(str)
    subjects=sorted(int(x) for x in base.subject.unique())
    videos=sorted((str(x) for x in base.video_id.unique()),key=lambda x:int(x))
    phys=sorted(c for c in base.columns if c.startswith("phys_"))
    if len(subjects)!=30 or len(videos)!=8 or len(phys)!=29:
        raise RuntimeError("Frozen CASE shape mismatch")

    results={}
    all_rmse_negative=True
    any_ccc_positive=False
    robust_ccc_rescues=[]

    for hi,(h,gap) in enumerate(zip(SHIFTS,GAPS)):
        hk=f"gap_{gap}s"; results[hk]={}
        for ai,axis in enumerate(("valence","arousal")):
            df=horizon_frame(base,h,axis)
            ctx=["time_norm","prior_"+axis]
            pf=ctx+phys
            axisres={}
            ccc_pos={}
            for li,learner in enumerate(("ridge","hgb")):
                rows=[]
                for s in subjects:
                    for v in videos:
                        tr=df[(df.subject!=s)&(df.video_id!=v)].reset_index(drop=True)
                        te=df[(df.subject==s)&(df.video_id==v)].reset_index(drop=True)
                        if te.empty: continue
                        ytr=tr.future_y.to_numpy(float); yte=te.future_y.to_numpy(float)
                        if learner=="ridge":
                            ac=tune(tr,ctx,"future_y"); ap=tune(tr,pf,"future_y")
                            mc=ridge_pipe(ac).fit(tr[ctx],ytr)
                            mp=ridge_pipe(ap).fit(tr[pf],ytr)
                        else:
                            mc=hgb_pipe().fit(tr[ctx],ytr)
                            mp=hgb_pipe().fit(tr[pf],ytr)
                        pc=mc.predict(te[ctx]); pp=mp.predict(te[pf]); pn=te["prior_"+axis].to_numpy(float)
                        for yy,nv,cv,pv in zip(yte,pn,pc,pp):
                            rows.append((s,v,float(yy),float(nv),float(cv),float(pv)))
                pr=pd.DataFrame(rows,columns=["subject","video_id","y","naive","context","phys"])
                if pr.empty: raise RuntimeError(f"No predictions {gap=} {axis=} {learner=}")
                pt=point_metrics(pr)
                bs=crossed_metric_bootstrap(pr,subjects,videos,131000+hi*1000+ai*100+li*10)
                pt["bootstrap"]=bs
                rmse_neg=bs["rmse_naive_phys"]["ci95"][1] < 0
                ccc_positive=bs["ccc_phys_naive"]["ci95"][0] > 0
                pt["rmse_naive_phys_strictly_negative"]=bool(rmse_neg)
                pt["ccc_phys_naive_strictly_positive"]=bool(ccc_positive)
                axisres[learner]=pt
                all_rmse_negative=all_rmse_negative and rmse_neg
                any_ccc_positive=any_ccc_positive or ccc_positive
                ccc_pos[learner]=ccc_positive
            axisres["both_learners_ccc_positive_vs_naive"]=bool(ccc_pos["ridge"] and ccc_pos["hgb"])
            if axisres["both_learners_ccc_positive_vs_naive"]:
                robust_ccc_rescues.append({"gap_sec":gap,"axis":axis})
            results[hk][axis]=axisres

    if robust_ccc_rescues:
        verdict="PHYSIOLOGY_TRACKING_RESCUE"
    elif all_rmse_negative and not any_ccc_positive:
        verdict="METRIC_ROBUST_PERSISTENCE_DOMINANCE"
    elif any_ccc_positive:
        verdict="MODEL_SPECIFIC_TRACKING_SIGNAL"
    else:
        verdict="MIXED_METRIC_RESULT"

    out={
        "status":"O002_D2_CASE_METRIC_TRAJECTORY_SENSITIVITY",
        "protocol":"protocols/o002_d2_metric_trajectory_sensitivity.json",
        "classification":"POST_PRIMARY_SENSITIVITY",
        "results":results,
        "robust_ccc_rescues":robust_ccc_rescues,
        "verdict":verdict,
        "firewall":"Metric/trajectory sensitivity only; no causal, bodily-necessity, universal, or phenomenal inference."
    }
    (OUT/"o002_d2_metric_trajectory_sensitivity.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
    slim={"verdict":verdict,"robust_ccc_rescues":robust_ccc_rescues}
    print(json.dumps(slim,indent=2))

if __name__=="__main__":
    main()
