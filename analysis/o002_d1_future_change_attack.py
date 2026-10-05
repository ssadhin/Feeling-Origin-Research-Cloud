from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
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

def horizon_frame(base,h,axis):
    z=base.sort_values(["subject","video_id","time_norm"]).copy()
    g=z.groupby(["subject","video_id"],sort=False)
    z["future_y"]=g["y_"+axis].shift(-h)
    z["delta_y"]=z["future_y"]-z["prior_"+axis]
    return z.dropna(subset=["future_y","delta_y"]).reset_index(drop=True)

def main():
    base=pd.read_json(IN,lines=True)
    base["video_id"]=base["video_id"].astype(str)
    subjects=sorted(base.subject.unique())
    videos=sorted(base.video_id.unique(),key=lambda x:int(x))
    phys=sorted(c for c in base.columns if c.startswith("phys_"))
    if len(subjects)!=30 or len(videos)!=8 or len(phys)!=29:
        raise RuntimeError("Frozen CASE shape mismatch")
    out={"status":"O002_D1_FUTURE_CHANGE_ATTACK",
         "protocol":"protocols/o002_d1_future_change_attack.json",
         "classification":"EXPLORATORY_POST_PRIMARY",
         "results":{},
         "firewall":"Predictive change diagnostic only; no causal or phenomenal inference."}
    any_both_positive=False
    any_positive=False
    zero_strong=True
    for hi,(h,gap) in enumerate(zip(SHIFTS,GAPS)):
        hk=f"gap_{gap}s"
        out["results"][hk]={}
        for ai,axis in enumerate(("valence","arousal")):
            df=horizon_frame(base,h,axis)
            ctx=["time_norm","prior_"+axis]
            pf=ctx+phys
            axisres={}
            learner_stats={}
            for li,learner in enumerate(("ridge","hgb")):
                mats={k:np.full((len(subjects),len(videos)),np.nan) for k in ("zero","context","phys")}
                rows={k:{"y":[],"p":[]} for k in mats}
                for si,s in enumerate(subjects):
                    for vi,v in enumerate(videos):
                        tr=df[(df.subject!=s)&(df.video_id!=v)].reset_index(drop=True)
                        te=df[(df.subject==s)&(df.video_id==v)].reset_index(drop=True)
                        ytr=tr.delta_y.to_numpy(float); yte=te.delta_y.to_numpy(float)
                        if learner=="ridge":
                            ac=tune(tr,ctx,"delta_y"); ap=tune(tr,pf,"delta_y")
                            mc=ridge_pipe(ac).fit(tr[ctx],ytr)
                            mp=ridge_pipe(ap).fit(tr[pf],ytr)
                        else:
                            ac=ap=None
                            mc=hgb_pipe().fit(tr[ctx],ytr)
                            mp=hgb_pipe().fit(tr[pf],ytr)
                        pc=mc.predict(te[ctx]); pp=mp.predict(te[pf]); p0=np.zeros_like(yte)
                        for name,pred in (("zero",p0),("context",pc),("phys",pp)):
                            mats[name][si,vi]=mean_absolute_error(yte,pred)
                            rows[name]["y"].extend(yte.tolist()); rows[name]["p"].extend(pred.tolist())
                dzp=mats["zero"]-mats["phys"]
                dcp=mats["context"]-mats["phys"]
                bz=crossed_boot(dzp,410000+1000*hi+100*ai+li)
                bc=crossed_boot(dcp,420000+1000*hi+100*ai+li)
                pos=bc["ci95"][0]>0
                any_positive=any_positive or pos
                zero_strong=zero_strong and (bz["mean"]<=0 and bz["ci95"][0]<=0)
                metrics={}
                for name in mats:
                    yy=np.asarray(rows[name]["y"]); pp=np.asarray(rows[name]["p"])
                    metrics[name+"_row_mae"]=float(mean_absolute_error(yy,pp))
                    metrics[name+"_mean_cell_mae"]=float(np.mean(mats[name]))
                learner_stats[learner]={**metrics,
                    "delta_zero_phys":bz,"delta_context_phys":bc,
                    "physiology_increment_positive_vs_context":bool(pos)}
            both=learner_stats["ridge"]["physiology_increment_positive_vs_context"] and learner_stats["hgb"]["physiology_increment_positive_vs_context"]
            any_both_positive=any_both_positive or both
            axisres["learners"]=learner_stats
            axisres["both_learners_positive_vs_context"]=bool(both)
            out["results"][hk][axis]=axisres
    if any_both_positive:
        verdict="CHANGE_SIGNAL_SURVIVES"
    elif not any_positive:
        verdict="NO_INCREMENT_FOR_CHANGE"
    else:
        verdict="MIXED_CHANGE_RESULT"
    out["verdict"]=verdict
    out["zero_change_beats_physiology_strongly"]=bool(zero_strong)
    (OUT/"o002_d1_future_change_attack.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
    slim={"verdict":verdict,"zero_change_beats_physiology_strongly":zero_strong,"results":{}}
    for h,z in out["results"].items():
        slim["results"][h]={}
        for a,v in z.items():
            slim["results"][h][a]={"both_positive":v["both_learners_positive_vs_context"],
                                   "ridge":v["learners"]["ridge"],
                                   "hgb":v["learners"]["hgb"]}
    print(json.dumps(slim,indent=2))

if __name__=="__main__":
    main()
