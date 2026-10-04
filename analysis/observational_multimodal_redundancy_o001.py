from __future__ import annotations

import argparse, csv, io, json, math, os, tempfile, urllib.request
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.signal import butter, sosfiltfilt, find_peaks, welch
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

DATASET="on002722"
VERSION="v1.0.0"
MANIFEST=f"https://data.nemar.org/{DATASET}/{VERSION}/manifest.json"
EEG_CH=["FP1","FPz","FP2","F7","F3","Fz","F4","F8","FT9","FC5","FC1","FC2","FC6","FT10",
        "T7","C3","Cz","C4","T8","TP9","CP5","CP1","CP2","CP6","TP10","P7","P3","Pz","P4","P8","O1","O2"]
BANDS=[("delta",1,4),("theta",4,8),("alpha",8,13),("beta",13,30),("gamma",30,45)]
ALPHAS=[0.1,1.0,10.0,100.0,1000.0]

def get_json(url):
    with urllib.request.urlopen(url,timeout=180) as r: return json.load(r)

def epath(e):
    for k in ("path","name","key","relative_path","file"):
        if isinstance(e.get(k),str): return e[k].lstrip("./")
    return ""

def eurl(e):
    for k in ("bytes_url","url","download_url"):
        if isinstance(e.get(k),str) and e[k].startswith("http"): return e[k]
    return None

def download(url,path):
    urllib.request.urlretrieve(url,path)

class EDF:
    def __init__(self,path):
        self.path=Path(path)
        with open(path,"rb") as fh:
            h=fh.read(256)
            self.header_bytes=int(h[184:192].decode().strip())
            self.n_records=int(h[236:244].decode().strip())
            self.record_duration=float(h[244:252].decode().strip())
            self.n_signals=int(h[252:256].decode().strip())
            sh=fh.read(self.header_bytes-256)
        pos=0
        def fields(width,cast=str):
            nonlocal pos
            xs=[sh[pos+i*width:pos+(i+1)*width].decode("latin1").strip() for i in range(self.n_signals)]
            pos += width*self.n_signals
            return xs if cast is str else [cast(x) for x in xs]
        self.labels=fields(16); fields(80); self.units=fields(8)
        self.pmin=fields(8,float); self.pmax=fields(8,float)
        self.dmin=fields(8,int); self.dmax=fields(8,int)
        fields(80); self.spr=fields(8,int); fields(32)
        if len(set(self.spr)) != 1:
            raise RuntimeError("Unequal EDF samples-per-record unsupported in frozen O001")
        self.spr0=self.spr[0]
        self.fs=self.spr0/self.record_duration
        if abs(self.record_duration-1.0)>1e-6:
            raise RuntimeError(f"Unexpected EDF record duration {self.record_duration}")
        total=sum(self.spr)
        self.mm=np.memmap(path,dtype="<i2",mode="r",offset=self.header_bytes,
                          shape=(self.n_records,total)).reshape(self.n_records,self.n_signals,self.spr0)
        self.duration=self.n_records*self.record_duration
    def segment(self,label,start_sec,end_sec):
        i=self.labels.index(label)
        total_samples=self.n_records*self.spr0
        a=max(0,int(round(start_sec*self.fs))); b=min(total_samples,int(round(end_sec*self.fs)))
        if b<=a:
            return np.asarray([],dtype=float)
        # Read only the EDF records intersecting the requested short window.
        r0=a//self.spr0
        r1=(b-1)//self.spr0+1
        block=np.asarray(self.mm[r0:r1,i,:],dtype=np.float64).reshape(-1)
        off=a-r0*self.spr0
        x=block[off:off+(b-a)]
        den=self.dmax[i]-self.dmin[i]
        if den==0: return np.full_like(x,np.nan,dtype=float)
        return (x-self.dmin[i])*(self.pmax[i]-self.pmin[i])/den+self.pmin[i]

def robust_clip(x):
    x=np.asarray(x,dtype=float)
    med=np.nanmedian(x); mad=np.nanmedian(np.abs(x-med))
    if np.isfinite(mad) and mad>0:
        x=np.clip(x,med-8*mad,med+8*mad)
    return x-med

def eeg_features(edf,start,end):
    xs=[]
    for ch in EEG_CH:
        x=robust_clip(edf.segment(ch,start,end))
        xs.append(x)
    n=min(map(len,xs))
    X=np.vstack([x[:n] for x in xs])
    nper=min(int(round(2*edf.fs)),X.shape[1])
    nover=min(nper//2,nper-1)
    f,p=welch(X,fs=edf.fs,nperseg=nper,noverlap=nover,axis=1,detrend="constant")
    total_mask=(f>=1)&(f<=45)
    total=np.trapezoid(p[:,total_mask],f[total_mask],axis=1)+1e-30
    feats=[]
    for _,lo,hi in BANDS:
        m=(f>=lo)&(f<hi)
        feats.extend((np.trapezoid(p[:,m],f[m],axis=1)/total).tolist())
    return np.asarray(feats,dtype=float)

def ecg_features(x,fs):
    x=robust_clip(x)
    if len(x)<int(3*fs) or not np.all(np.isfinite(x)):
        return [np.nan]*4,False
    try:
        sos=butter(2,[5,25],btype="bandpass",fs=fs,output="sos")
        y=sosfiltfilt(sos,x)
        sd=np.std(y)
        if not np.isfinite(sd) or sd<=1e-12: return [np.nan]*4,False
        y=y/sd
        candidates=[]
        for sign in (1,-1):
            peaks,_=find_peaks(sign*y,distance=max(1,int(.33*fs)),prominence=.6)
            rr=np.diff(peaks)/fs
            rr=rr[(rr>=.333)&(rr<=1.5)]
            if len(rr)>=5:
                hr=60/rr
                med=float(np.median(hr))
                if 40<=med<=180:
                    cv=float(np.std(rr)/(np.mean(rr)+1e-12))
                    candidates.append((len(rr),-cv,rr,hr))
        if not candidates: return [np.nan]*4,False
        _,_,rr,hr=max(candidates,key=lambda z:(z[0],z[1]))
        return [float(np.mean(hr)),float(np.median(hr)),float(np.std(rr,ddof=1)),float(np.sqrt(np.mean(np.diff(rr)**2)))],True
    except Exception:
        return [np.nan]*4,False

def gsr_features(x,fs):
    x=robust_clip(x)
    if len(x)<2 or not np.all(np.isfinite(x)): return [np.nan]*5
    n=len(x); t=np.arange(n)/fs
    slope=float(np.polyfit(t,x,1)[0]) if n>2 else np.nan
    q=max(1,int(fs))
    return [float(np.std(x)),float(np.max(x)-np.min(x)),slope,
            float(np.mean(x[-q:])-np.mean(x[:q])),
            float(np.mean(x[n//2:])-np.mean(x[:n//2]))]

def mean_segment(edf,label,a,b):
    x=edf.segment(label,a,b)
    return float(np.nanmean(x)) if len(x) else np.nan

def parse_trials(tsv_text):
    rows=list(csv.DictReader(io.StringIO(tsv_text),delimiter="\t"))
    groups=defaultdict(list)
    durations={}
    for r in rows:
        try:
            onset=float(r["onset"]); dur=float(r["duration"]); code=int(float(r["trial_type"]))
        except Exception:
            continue
        groups[round(onset,6)].append(code); durations[round(onset,6)]=dur
    out=[]
    for onset,codes in sorted(groups.items()):
        targets=[c for c in codes if 1<=c<=9]
        mus=[c for c in codes if c>9]
        if targets and mus:
            out.append({"onset":float(onset),"duration":durations[onset],
                        "target_code":targets[0],"music_id":mus[0]})
    return out

def collect(max_subjects=0):
    m=get_json(MANIFEST); entries=m if isinstance(m,list) else m.get("files",m.get("entries",[]))
    bypath={epath(e):e for e in entries}
    edfs=sorted([p for p in bypath if p.endswith("_eeg.edf")])
    subjects=sorted({p.split("/")[0] for p in edfs if p.startswith("sub-")})
    if max_subjects: subjects=subjects[:max_subjects]
    rows=[]; qc={"edf_files":0,"trials_seen":0,"trials_usable":0,"ecg_valid":0,"file_errors":[]}
    td=Path(tempfile.mkdtemp(prefix="o001_"))
    for si,sub in enumerate(subjects,1):
        sub_edfs=[p for p in edfs if p.startswith(sub+"/")]
        print(f"SUBJECT {si}/{len(subjects)} {sub}: {len(sub_edfs)} EDFs",flush=True)
        for p in sub_edfs:
            evt=p.replace("_eeg.edf","_events.tsv")
            if evt not in bypath: qc["file_errors"].append({"file":p,"error":"missing events"}); continue
            u=eurl(bypath[p]); eu=eurl(bypath[evt])
            if not u or not eu: qc["file_errors"].append({"file":p,"error":"missing bytes_url"}); continue
            local=td/(sub+"_"+Path(p).name)
            try:
                download(u,local)
                with urllib.request.urlopen(eu,timeout=120) as rr: evt_text=rr.read().decode("utf-8-sig",errors="replace")
                edf=EDF(local); qc["edf_files"]+=1
                missing=[c for c in EEG_CH+["ECG","GSR","VA1","VA2"] if c not in edf.labels]
                if missing: raise RuntimeError(f"missing channels {missing}")
                trials=parse_trials(evt_text)
                run_name=Path(p).stem
                for ti,tr in enumerate(trials):
                    qc["trials_seen"]+=1
                    on=tr["onset"]
                    if on+20>edf.duration: continue
                    ef=eeg_features(edf,on+5,on+14)
                    ecgv,valid=ecg_features(edf.segment("ECG",on+5,on+14),edf.fs)
                    gsrv=gsr_features(edf.segment("GSR",on+5,on+14),edf.fs)
                    prior_v=mean_segment(edf,"VA1",on+10,on+14)
                    prior_a=mean_segment(edf,"VA2",on+10,on+14)
                    yv=mean_segment(edf,"VA1",on+15,on+20)
                    ya=mean_segment(edf,"VA2",on+15,on+20)
                    if not (np.isfinite(ef).all() and np.isfinite(prior_v) and np.isfinite(prior_a) and np.isfinite(yv) and np.isfinite(ya)):
                        continue
                    row={"subject":sub,"run":run_name,"trial":ti+1,"onset":on,
                         "target_code":str(tr["target_code"]),"music_id":str(tr["music_id"]),
                         "prior_valence":prior_v,"prior_arousal":prior_a,
                         "y_valence":yv,"y_arousal":ya,"ecg_valid":bool(valid)}
                    for j,v in enumerate(ef): row[f"eeg_{j:03d}"]=float(v)
                    for name,v in zip(["hr_mean","hr_median","sdnn","rmssd"],ecgv): row["auto_"+name]=float(v)
                    for name,v in zip(["gsr_std","gsr_range","gsr_slope","gsr_endstart","gsr_halfdiff"],gsrv): row["auto_"+name]=float(v)
                    rows.append(row); qc["trials_usable"]+=1; qc["ecg_valid"]+=int(valid)
            except Exception as e:
                qc["file_errors"].append({"file":p,"error":repr(e)})
            finally:
                try: local.unlink()
                except Exception: pass
    qc["subjects"]=subjects
    qc["n_subjects"]=len(subjects)
    qc["ecg_valid_fraction"]=qc["ecg_valid"]/qc["trials_usable"] if qc["trials_usable"] else 0
    return rows,qc

def make_preprocessor(spec,target,eeg_cols,auto_cols):
    cat=["target_code","music_id"]
    prior=["prior_valence" if target=="valence" else "prior_arousal"]
    trs=[("cat",OneHotEncoder(handle_unknown="ignore",sparse_output=False),cat)]
    if spec!="stimulus_only":
        trs.append(("prior",Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler())]),prior))
    if spec in ("eeg","combined"):
        trs.append(("eeg",Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler()),
                                   ("pca",PCA(n_components=20,svd_solver="auto"))]),eeg_cols))
    if spec in ("autonomic","combined"):
        trs.append(("auto",Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler())]),auto_cols))
    return ColumnTransformer(trs,remainder="drop",sparse_threshold=0.0)

def fit_tuned(train,test,target,spec,eeg_cols,auto_cols):
    import pandas as pd
    ycol="y_"+target
    groups=train["subject"].to_numpy()
    uniq=np.unique(groups)
    nsplit=min(4,len(uniq))
    cv=GroupKFold(n_splits=nsplit)
    scores={a:[] for a in ALPHAS}
    for itr,iva in cv.split(train,train[ycol],groups):
        tr=train.iloc[itr]; va=train.iloc[iva]
        pp=make_preprocessor(spec,target,eeg_cols,auto_cols)
        Xtr=pp.fit_transform(tr); Xva=pp.transform(va)
        ytr=tr[ycol].to_numpy(float); yva=va[ycol].to_numpy(float)
        for a in ALPHAS:
            mdl=Ridge(alpha=a).fit(Xtr,ytr)
            scores[a].append(mean_absolute_error(yva,mdl.predict(Xva)))
    best=min(ALPHAS,key=lambda a:(float(np.mean(scores[a])),a))
    pp=make_preprocessor(spec,target,eeg_cols,auto_cols)
    Xtr=pp.fit_transform(train); Xte=pp.transform(test)
    mdl=Ridge(alpha=best).fit(Xtr,train[ycol].to_numpy(float))
    return mdl.predict(Xte),best

def bootstrap_deltas(subject_metrics,n=5000,seed=5001):
    rng=np.random.default_rng(seed)
    subs=sorted(subject_metrics)
    pairs={
      "combined_vs_stimulus_prior":("stimulus_prior","combined"),
      "autonomic_increment_beyond_eeg":("eeg","combined"),
      "eeg_increment_beyond_autonomic":("autonomic","combined"),
    }
    out={}
    for name,(a,b) in pairs.items():
        vals=np.array([subject_metrics[s][a]-subject_metrics[s][b] for s in subs],float)
        boots=np.empty(n)
        for i in range(n): boots[i]=np.mean(rng.choice(vals,size=len(vals),replace=True))
        out[name]={"mean":float(np.mean(vals)),"ci95":[float(np.percentile(boots,2.5)),float(np.percentile(boots,97.5))],
                   "subject_differences":{s:float(subject_metrics[s][a]-subject_metrics[s][b]) for s in subs}}
    return out

def analyze(rows,qc,bootstrap=5000):
    import pandas as pd
    df=pd.DataFrame(rows)
    eeg_cols=sorted([c for c in df.columns if c.startswith("eeg_")])
    auto_cols=sorted([c for c in df.columns if c.startswith("auto_")])
    subjects=sorted(df.subject.unique())
    counts=df.groupby("subject").size()
    gate={
      "minimum_subjects":len(subjects)>=12,
      "minimum_usable_trials":len(df)>=600,
      "minimum_ecg_valid_fraction":qc["ecg_valid_fraction"]>=0.70,
      "minimum_outer_subjects_with_30_trials":int((counts>=30).sum())>=12,
      "observed":{"subjects":len(subjects),"usable_trials":len(df),"ecg_valid_fraction":qc["ecg_valid_fraction"],
                  "subjects_with_30_trials":int((counts>=30).sum())}
    }
    specs=["stimulus_only","stimulus_prior","eeg","autonomic","combined"]
    targets={}
    all_predictions=[]
    for target in ("valence","arousal"):
        subj_metrics={}; pooled_y=[]; pooled={s:[] for s in specs}
        chosen={s:[] for s in specs}
        for oi,sub in enumerate(subjects,1):
            print(f"MODEL {target} OUTER {oi}/{len(subjects)} {sub}",flush=True)
            train=df[df.subject!=sub].reset_index(drop=True)
            test=df[df.subject==sub].reset_index(drop=True)
            y=test["y_"+target].to_numpy(float); pooled_y.extend(y.tolist())
            subj_metrics[sub]={}
            predmap={}
            for spec in specs:
                pred,alpha=fit_tuned(train,test,target,spec,eeg_cols,auto_cols)
                predmap[spec]=pred; pooled[spec].extend(pred.tolist()); chosen[spec].append({"heldout":sub,"alpha":alpha})
                subj_metrics[sub][spec]=float(mean_absolute_error(y,pred))
            for i in range(len(test)):
                all_predictions.append({"target":target,"subject":sub,"run":test.loc[i,"run"],"trial":int(test.loc[i,"trial"]),
                                        "y":float(y[i]),**{f"pred_{s}":float(predmap[s][i]) for s in specs}})
        metrics={}
        yy=np.asarray(pooled_y)
        for spec in specs:
            pp=np.asarray(pooled[spec])
            metrics[spec]={"mae":float(mean_absolute_error(yy,pp)),
                           "r2":float(r2_score(yy,pp)),
                           "pearson_r":float(np.corrcoef(yy,pp)[0,1]) if np.std(pp)>0 and np.std(yy)>0 else None,
                           "mean_subject_mae":float(np.mean([subj_metrics[s][spec] for s in subjects]))}
        deltas=bootstrap_deltas(subj_metrics,n=bootstrap,seed=5001+(0 if target=="valence" else 100))
        if not all(v for k,v in gate.items() if k!="observed"):
            taxonomy="INSUFFICIENT_DATA_OR_QC"
        else:
            c0=deltas["combined_vs_stimulus_prior"]["ci95"][0]>0
            ca=deltas["autonomic_increment_beyond_eeg"]["ci95"][0]>0
            ce=deltas["eeg_increment_beyond_autonomic"]["ci95"][0]>0
            if c0 and ca and ce: taxonomy="BIDIRECTIONAL_COMPLEMENTARITY"
            elif c0 and ca and not ce: taxonomy="AUTONOMIC_ADDS_ONLY"
            elif c0 and ce and not ca: taxonomy="EEG_ADDS_ONLY"
            elif c0: taxonomy="MULTIMODAL_INCREMENT_NO_CLEAR_COMPLEMENTARITY"
            else: taxonomy="NO_INCREMENT_BEYOND_PRIOR_REPORT_AND_STIMULUS"
        targets[target]={"metrics":metrics,"bootstrap_deltas":deltas,"taxonomy":taxonomy,
                         "chosen_alphas":chosen,"subject_mae":subj_metrics}
    return {"admission_gate":gate,"targets":targets,"predictions":all_predictions,
            "feature_counts":{"eeg":len(eeg_cols),"autonomic":len(auto_cols)}}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--max-subjects",type=int,default=0)
    ap.add_argument("--bootstrap",type=int,default=5000)
    ap.add_argument("--extract-only",action="store_true")
    args=ap.parse_args()
    out=Path("results"); out.mkdir(exist_ok=True)
    rows,qc=collect(args.max_subjects)
    # compact feature cache as JSONL for auditability; no raw signals.
    with open(out/"o001_feature_rows.jsonl","w",encoding="utf-8") as f:
        for r in rows: f.write(json.dumps(r,separators=(",",":"))+"\n")
    base={"status":"O001_EXTRACT_ONLY" if args.extract_only else "O001_OBSERVATIONAL_BRIDGE",
          "protocol":"protocols/observational_multimodal_redundancy_o001.json",
          "dataset":DATASET,"version":VERSION,"qc":qc,
          "firewall":"Observational first-person-report bridge only. No causal, necessary/sufficient, phenomenal-identity, or consciousness-detector inference."}
    if not args.extract_only:
        base["analysis"]=analyze(rows,qc,args.bootstrap)
    (out/"observational_multimodal_redundancy_o001.json").write_text(json.dumps(base,indent=2),encoding="utf-8")
    print(json.dumps({k:v for k,v in base.items() if k!="analysis"},indent=2))
    if "analysis" in base:
        print(json.dumps({"gate":base["analysis"]["admission_gate"],
                          "valence":base["analysis"]["targets"]["valence"]["taxonomy"],
                          "arousal":base["analysis"]["targets"]["arousal"]["taxonomy"],
                          "deltas":{t:base["analysis"]["targets"][t]["bootstrap_deltas"] for t in ("valence","arousal")}},indent=2))

if __name__=="__main__":
    main()
