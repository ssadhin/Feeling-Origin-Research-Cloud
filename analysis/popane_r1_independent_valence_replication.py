from __future__ import annotations
import json, math, os, re, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.signal import butter, sosfiltfilt, find_peaks
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ZIP=Path(os.environ.get("POPANE_ZIP","/tmp/study6.zip"))
OUT=Path("results"); OUT.mkdir(exist_ok=True)
HORIZONS=[0,1,2,3]
GAPS=[1,11,21,31]
ALPHAS=[0.1,1.0,10.0,100.0,1000.0]
NBOOT=5000
MIN_SEGMENT_PARTICIPANTS=20
RNG_SEED=1601

def parse_name(path):
    stem=Path(path).stem
    m=re.match(r"^(\d+)_(.+)$",stem)
    return (int(m.group(1)),m.group(2)) if m else (None,None)

def finite(x):
    a=pd.to_numeric(x,errors="coerce").to_numpy(float)
    return a[np.isfinite(a)]

def stats_basic(x):
    v=finite(x)
    if len(v)<3: return [np.nan]*5
    return [float(np.mean(v)),float(np.std(v)),float(np.sqrt(np.mean(v*v))),float(np.ptp(v)),
            float(np.std(np.diff(v))) if len(v)>3 else np.nan]

def slope_feature(t,x):
    tt=pd.to_numeric(t,errors="coerce").to_numpy(float)
    xx=pd.to_numeric(x,errors="coerce").to_numpy(float)
    m=np.isfinite(tt)&np.isfinite(xx)
    if m.sum()<3: return np.nan
    zt=tt[m]-np.mean(tt[m])
    den=float(np.dot(zt,zt))
    return float(np.dot(zt,xx[m]-np.mean(xx[m]))/den) if den>0 else 0.0

def mean_std_slope(t,x):
    v=pd.to_numeric(x,errors="coerce").to_numpy(float)
    m=np.isfinite(v)
    if m.sum()<3: return [np.nan,np.nan,np.nan]
    return [float(np.mean(v[m])),float(np.std(v[m])),slope_feature(t,x)]

def ecg_features(x,fs=1000.0):
    a=pd.to_numeric(x,errors="coerce").to_numpy(float)
    good=np.isfinite(a)
    raw=a[good]
    basic=stats_basic(pd.Series(raw)) if len(raw) else [np.nan]*5
    if good.mean()<0.6 or len(raw)<int(fs*3):
        return basic+[np.nan]*4
    # interpolate only within the already-frozen predictor window
    idx=np.arange(len(a))
    a=np.interp(idx,idx[good],a[good])
    a=a-np.median(a)
    try:
        sos=butter(2,[5,25],btype="bandpass",fs=fs,output="sos")
        y=sosfiltfilt(sos,a)
    except Exception:
        y=a
    sd=float(np.std(y))
    prom=max(1e-9,0.75*sd)
    dist=max(1,int(0.30*fs))
    p1,pr1=find_peaks(y,distance=dist,prominence=prom)
    p2,pr2=find_peaks(-y,distance=dist,prominence=prom)
    def score(peaks,props):
        if len(peaks)<2: return (-1,-1)
        rr=np.diff(peaks)/fs
        plausible=np.mean((rr>=0.30)&(rr<=2.0))
        return (plausible,float(np.sum(props.get("prominences",[]))))
    peaks=p1 if score(p1,pr1)>=score(p2,pr2) else p2
    rr=np.diff(peaks)/fs if len(peaks)>=2 else np.array([])
    rr=rr[(rr>=0.30)&(rr<=2.0)]
    if len(rr)<2:
        return basic+[float(len(peaks)),np.nan,np.nan,np.nan]
    hr=float(60.0/np.mean(rr))
    sdnn=float(np.std(rr))
    rmssd=float(np.sqrt(np.mean(np.diff(rr)**2))) if len(rr)>=3 else np.nan
    return basic+[float(len(peaks)),hr,sdnn,rmssd]

def eda_features(t,x):
    v=pd.to_numeric(x,errors="coerce").to_numpy(float)
    tt=pd.to_numeric(t,errors="coerce").to_numpy(float)
    m=np.isfinite(v)&np.isfinite(tt)
    if m.sum()<3: return [np.nan]*6
    vv=v[m]; ttv=tt[m]
    dv=np.diff(vv)
    return [float(np.mean(vv)),float(np.std(vv)),float(np.ptp(vv)),slope_feature(pd.Series(ttv),pd.Series(vv)),
            float(np.std(dv)) if len(dv)>1 else np.nan,float(np.sum(np.clip(dv,0,None)))]

def read_csv_member(zf,name):
    cols=["timestamp","affect","ECG","dzdt","dz","z0","EDA","SBP","DBP","CO","TPR"]
    with zf.open(name) as f:
        return pd.read_csv(f,comment="#",usecols=lambda c: c in cols,low_memory=False)

def eligible_names(zf):
    names=[n for n in zf.namelist() if n.lower().endswith(".csv")]
    counts={}
    parsed=[]
    for n in names:
        pid,seg=parse_name(n)
        if pid is None or seg.lower() in ("all","baseline"): continue
        parsed.append((n,pid,seg))
        counts.setdefault(seg,set()).add(pid)
    eligible={s for s,pids in counts.items() if len(pids)>=MIN_SEGMENT_PARTICIPANTS}
    return [(n,p,s) for n,p,s in parsed if s in eligible],{s:len(p) for s,p in counts.items()},sorted(eligible)

def extract_rows():
    rows=[]; qc={"files_seen":0,"files_usable":0,"reject":{}}
    with zipfile.ZipFile(ZIP) as zf:
        selected,segment_counts,eligible=eligible_names(zf)
        for fi,(name,pid,seg) in enumerate(selected,1):
            qc["files_seen"]+=1
            try:
                df=read_csv_member(zf,name)
                for c in ["timestamp","affect","ECG","dzdt","dz","z0","EDA","SBP","DBP","CO","TPR"]:
                    if c not in df: df[c]=np.nan
                    df[c]=pd.to_numeric(df[c],errors="coerce")
                df=df[np.isfinite(df.timestamp)].sort_values("timestamp").reset_index(drop=True)
                if len(df)<10: raise ValueError("too_few_rows")
                t=df.timestamp.to_numpy(float)
                duration=float(t[-1]-t[0])
                if duration<55: raise ValueError("duration")
                if np.mean(np.isfinite(df.affect.to_numpy(float)))<0.90: raise ValueError("affect_missing")
                ecgfrac=float(np.mean(np.isfinite(df.ECG.to_numpy(float))))
                edafrac=float(np.mean(np.isfinite(df.EDA.to_numpy(float))))
                if max(ecgfrac,edafrac)<0.80: raise ValueError("peripheral_missing")
                if np.any(np.diff(t)<0): raise ValueError("timestamp")
                start=float(t[0]); end=float(t[-1])
                # Common anchors support all four horizons, preventing horizon-specific row-selection artifacts.
                max_anchor=end-35.0
                anchors=np.arange(start+10.0,max_anchor+1e-9,10.0)
                if len(anchors)==0: raise ValueError("no_anchor")
                qc["files_usable"]+=1
                for a in anchors:
                    pm=(t>=a-10)&(t<=a-1)
                    am=(t>=a-5)&(t<=a-1)
                    if pm.sum()<100 or am.sum()<100: continue
                    prior_vals=df.loc[am,"affect"].to_numpy(float)
                    prior_vals=prior_vals[np.isfinite(prior_vals)]
                    if len(prior_vals)<100: continue
                    rec={"subject":pid,"segment":seg,"time_norm":float((a-start)/max(1e-9,duration)),
                         "prior_affect":float(np.mean(prior_vals))}
                    # future targets
                    ok=True
                    for h in HORIZONS:
                        tm=(t>=a+10*h)&(t<=a+10*h+5)
                        y=df.loc[tm,"affect"].to_numpy(float)
                        y=y[np.isfinite(y)]
                        if len(y)<100:
                            ok=False; break
                        rec[f"y_h{h}"]=float(np.mean(y))
                    if not ok: continue
                    sub=df.loc[pm]
                    tt=sub.timestamp
                    e=ecg_features(sub.ECG,1000.0)
                    names_e=["ecg_mean","ecg_std","ecg_rms","ecg_range","ecg_diff_std","rpeak_count","hr_mean","sdnn","rmssd"]
                    rec.update(dict(zip(names_e,e)))
                    ed=eda_features(tt,sub.EDA)
                    rec.update(dict(zip(["eda_mean","eda_std","eda_range","eda_slope","eda_diff_std","eda_posdiff_area"],ed)))
                    for c,prefix in [("dzdt","dzdt"),("dz","dz"),("z0","z0")]:
                        b=stats_basic(sub[c])
                        rec.update({f"{prefix}_{k}":v for k,v in zip(["mean","std","rms","range","diff_std"],b)})
                    for c in ["SBP","DBP","CO","TPR"]:
                        vals=mean_std_slope(tt,sub[c])
                        rec.update({f"{c.lower()}_{k}":v for k,v in zip(["mean","std","slope"],vals)})
                    rows.append(rec)
                if fi%50==0:
                    print(f"extract {fi}/{len(selected)} files; rows={len(rows)}",flush=True)
            except Exception as e:
                k=str(e)
                qc["reject"][k]=qc["reject"].get(k,0)+1
        qc["segment_filename_counts"]=segment_counts
        qc["eligible_segments"]=eligible
    feat=pd.DataFrame(rows)
    qc["feature_rows"]=int(len(feat))
    qc["subjects_usable"]=int(feat.subject.nunique()) if len(feat) else 0
    qc["segments_usable"]=int(feat.segment.nunique()) if len(feat) else 0
    return feat,qc

def subject_folds(subjects):
    ss=sorted(int(x) for x in subjects)
    return {s:i%10 for i,s in enumerate(ss)}

def ridge_pipe(alpha):
    return Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler()),("m",Ridge(alpha=alpha))])

def hgb_pipe():
    return Pipeline([("imp",SimpleImputer(strategy="median")),
                     ("m",HistGradientBoostingRegressor(max_iter=150,learning_rate=0.05,max_leaf_nodes=15,
                                                        l2_regularization=1.0,random_state=RNG_SEED))])

def tune_ridge(train,features,target):
    groups=train.subject.to_numpy()
    uniq=np.unique(groups)
    if len(uniq)<2: return 10.0
    cv=GroupKFold(n_splits=min(4,len(uniq)))
    scores={a:[] for a in ALPHAS}
    y=train[target].to_numpy(float)
    X=train[features]
    for tr,va in cv.split(X,y,groups):
        for a in ALPHAS:
            p=ridge_pipe(a).fit(X.iloc[tr],y[tr]).predict(X.iloc[va])
            scores[a].append(mean_absolute_error(y[va],p))
    return min(ALPHAS,key=lambda a:(float(np.mean(scores[a])),a))

def bootstrap_subject(diffs,seed):
    # diffs is participant-level paired MAE difference
    v=np.asarray(list(diffs.values()),float)
    rng=np.random.default_rng(seed)
    bs=np.array([np.mean(rng.choice(v,size=len(v),replace=True)) for _ in range(NBOOT)])
    return {"mean":float(np.mean(v)),"ci95":[float(np.percentile(bs,2.5)),float(np.percentile(bs,97.5))],
            "n_subjects":int(len(v))}

def primary_joint(feat):
    phys=[c for c in feat.columns if c not in {"subject","segment","time_norm","prior_affect","y_h0","y_h1","y_h2","y_h3"}]
    folds=subject_folds(feat.subject.unique())
    feat=feat.copy(); feat["fold"]=feat.subject.map(folds)
    res={}
    decision_positive={"ridge":[],"hgb":[]}
    decision_means={"ridge":[],"hgb":[]}
    naive_better_all=True
    for h,gap in zip(HORIZONS,GAPS):
        target=f"y_h{h}"
        hz={}
        for learner in ["ridge","hgb"]:
            preds=[]
            for f in range(10):
                held_subjects=set(k for k,v in folds.items() if v==f)
                for seg in sorted(feat.segment.unique()):
                    te=feat[(feat["fold"]==f)&(feat.segment==seg)]
                    if te.empty: continue
                    tr=feat[(feat["fold"]!=f)&(feat.segment!=seg)]
                    if tr.subject.nunique()<10 or len(tr)<100: continue
                    ytr=tr[target].to_numpy(float); yte=te[target].to_numpy(float)
                    basef=["prior_affect","time_norm"]; physf=basef+phys
                    if learner=="ridge":
                        ab=tune_ridge(tr,basef,target); ap=tune_ridge(tr,physf,target)
                        mb=ridge_pipe(ab).fit(tr[basef],ytr); mp=ridge_pipe(ap).fit(tr[physf],ytr)
                    else:
                        ab=None; ap=None
                        mb=hgb_pipe().fit(tr[basef],ytr); mp=hgb_pipe().fit(tr[physf],ytr)
                    pb=mb.predict(te[basef]); pp=mp.predict(te[physf])
                    for idx,yy,bv,pv in zip(te.index,yte,pb,pp):
                        preds.append((int(te.loc[idx,"subject"]),float(yy),float(te.loc[idx,"prior_affect"]),float(bv),float(pv)))
            pr=pd.DataFrame(preds,columns=["subject","y","naive","fitted","phys"])
            if pr.empty: raise RuntimeError(f"No predictions h={h} learner={learner}")
            subj={}
            for s,q in pr.groupby("subject"):
                subj[int(s)]={
                  "naive":float(mean_absolute_error(q.y,q.naive)),
                  "fitted":float(mean_absolute_error(q.y,q.fitted)),
                  "phys":float(mean_absolute_error(q.y,q.phys))
                }
            dnp={s:v["naive"]-v["phys"] for s,v in subj.items()}
            dfp={s:v["fitted"]-v["phys"] for s,v in subj.items()}
            bnp=bootstrap_subject(dnp,50000+h*100+(0 if learner=="ridge" else 10))
            bfp=bootstrap_subject(dfp,51000+h*100+(0 if learner=="ridge" else 10))
            metrics={
              "n_rows":int(len(pr)),"n_subjects":int(pr.subject.nunique()),
              "naive_mae":float(mean_absolute_error(pr.y,pr.naive)),
              "fitted_mae":float(mean_absolute_error(pr.y,pr.fitted)),
              "physiology_mae":float(mean_absolute_error(pr.y,pr.phys)),
              "delta_naive_phys":bnp,"delta_fitted_phys":bfp,
              "physiology_positive_vs_naive":bool(bnp["ci95"][0]>0)
            }
            hz[learner]=metrics
            decision_positive[learner].append(metrics["physiology_positive_vs_naive"])
            decision_means[learner].append(bnp["mean"])
            naive_better_all=naive_better_all and (metrics["naive_mae"]<metrics["physiology_mae"])
        res[f"gap_{gap}s"]=hz
    clear=any(decision_positive["ridge"][i] and decision_positive["hgb"][i] for i in range(4))
    nonpos=(not any(decision_positive["ridge"]) and not any(decision_positive["hgb"]) and
            sum(x<=0 for x in decision_means["ridge"])>=3 and sum(x<=0 for x in decision_means["hgb"])>=3)
    if clear:
        verdict="CLEAR_EXTERNAL_PHYSIOLOGY_INCREMENT"
    elif nonpos and naive_better_all:
        verdict="STRONG_REPLICATION_OF_BASELINE_DOMINANCE"
    elif nonpos:
        verdict="REPLICATED_NONPOSITIVE_INCREMENT_PATTERN"
    else:
        verdict="MIXED_EXTERNAL_RESULT"
    return res,verdict,{"positive":decision_positive,"means":decision_means,"naive_better_all":naive_better_all}

def main():
    if not ZIP.exists(): raise FileNotFoundError(ZIP)
    feat,qc=extract_rows()
    if len(feat)<500 or feat.subject.nunique()<20 or feat.segment.nunique()<2:
        out={"status":"POPANE_R1","verdict":"FAIL_TECHNICAL_QC","qc":qc}
    else:
        primary,verdict,dec=primary_joint(feat)
        out={"status":"POPANE_R1_INDEPENDENT_VALENCE_REPLICATION",
             "protocol":"protocols/popane_r1_independent_valence_replication.json",
             "qc":qc,"primary_joint":primary,"decision_state":dec,"verdict":verdict,
             "firewall":"External predictive valence replication only; no causal, bodily-necessity, or phenomenal inference."}
    (OUT/"popane_r1_independent_valence_replication.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
    # aggregate-only console summary
    slim={"verdict":out.get("verdict"),"qc":{k:v for k,v in qc.items() if k!="segment_filename_counts"}}
    if "primary_joint" in out:
        slim["primary_joint"]={h:{l:{k:v for k,v in m.items() if k not in ()} for l,m in z.items()} for h,z in out["primary_joint"].items()}
    print(json.dumps(slim,indent=2))

if __name__=="__main__":
    main()
