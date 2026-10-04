from __future__ import annotations

import argparse, csv, io, json, tempfile, urllib.request
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

DATASET="on002724"
VERSION="v1.0.0"
MANIFEST=f"https://data.nemar.org/{DATASET}/{VERSION}/manifest.json"
EEG_CH=["FP1","FPz","FP2","F7","F3","Fz","F4","F8","FT9","FC5","FC1","FC2","FC6","FT10",
        "T7","C3","Cz","C4","T8","TP9","CP5","CP1","CP2","CP6","TP10","P7","P3","Pz","P4","P8","O1","O2"]
BANDS=[("delta",1,4),("theta",4,8),("alpha",8,13),("beta",13,30),("gamma",30,45)]
ALPHAS=[0.1,1.0,10.0,100.0,1000.0]
PUBLIC_SUBS=["sub-08","sub-09","sub-10","sub-11","sub-12","sub-13","sub-14","sub-15","sub-16","sub-17"]

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

class EDF:
    def __init__(self,path):
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
        if len(set(self.spr))!=1: raise RuntimeError("Unequal samples-per-record")
        self.spr0=self.spr[0]; self.fs=self.spr0/self.record_duration
        if abs(self.record_duration-1.0)>1e-6: raise RuntimeError("Unexpected EDF record duration")
        total=sum(self.spr)
        self.mm=np.memmap(path,dtype="<i2",mode="r",offset=self.header_bytes,
                          shape=(self.n_records,total)).reshape(self.n_records,self.n_signals,self.spr0)
        self.duration=self.n_records*self.record_duration
    def segment(self,label,a,b):
        i=self.labels.index(label); total=self.n_records*self.spr0
        ia=max(0,int(round(a*self.fs))); ib=min(total,int(round(b*self.fs)))
        if ib<=ia: return np.asarray([],float)
        r0=ia//self.spr0; r1=(ib-1)//self.spr0+1
        block=np.asarray(self.mm[r0:r1,i,:],dtype=np.float64).reshape(-1)
        off=ia-r0*self.spr0; x=block[off:off+(ib-ia)]
        den=self.dmax[i]-self.dmin[i]
        if den==0: return np.full_like(x,np.nan,dtype=float)
        return (x-self.dmin[i])*(self.pmax[i]-self.pmin[i])/den+self.pmin[i]

def robust_clip(x):
    x=np.asarray(x,float); med=np.nanmedian(x); mad=np.nanmedian(np.abs(x-med))
    if np.isfinite(mad) and mad>0: x=np.clip(x,med-8*mad,med+8*mad)
    return x-med

def eeg_features(edf,a,b):
    xs=[robust_clip(edf.segment(ch,a,b)) for ch in EEG_CH]
    n=min(map(len,xs)); X=np.vstack([x[:n] for x in xs])
    nper=min(int(2*edf.fs),X.shape[1]); nover=min(nper//2,nper-1)
    f,p=welch(X,fs=edf.fs,nperseg=nper,noverlap=nover,axis=1,detrend="constant")
    m=(f>=1)&(f<=45); total=np.trapezoid(p[:,m],f[m],axis=1)+1e-30
    feats=[]
    for _,lo,hi in BANDS:
        q=(f>=lo)&(f<hi)
        feats.extend((np.trapezoid(p[:,q],f[q],axis=1)/total).tolist())
    return np.asarray(feats,float)

def ecg_features(x,fs):
    x=robust_clip(x)
    if len(x)<int(3*fs) or not np.all(np.isfinite(x)): return [np.nan]*4,False
    try:
        sos=butter(2,[5,25],btype="bandpass",fs=fs,output="sos"); y=sosfiltfilt(sos,x)
        sd=np.std(y)
        if not np.isfinite(sd) or sd<=1e-12: return [np.nan]*4,False
        y=y/sd; cand=[]
        for sign in (1,-1):
            peaks,_=find_peaks(sign*y,distance=max(1,int(.33*fs)),prominence=.6)
            rr=np.diff(peaks)/fs; rr=rr[(rr>=.333)&(rr<=1.5)]
            if len(rr)>=5:
                hr=60/rr; med=float(np.median(hr))
                if 40<=med<=180:
                    cand.append((len(rr),-float(np.std(rr)/(np.mean(rr)+1e-12)),rr,hr))
        if not cand: return [np.nan]*4,False
        _,_,rr,hr=max(cand,key=lambda z:(z[0],z[1]))
        return [float(np.mean(hr)),float(np.median(hr)),float(np.std(rr,ddof=1)),
                float(np.sqrt(np.mean(np.diff(rr)**2)))],True
    except Exception:
        return [np.nan]*4,False

def gsr_features(x,fs):
    x=robust_clip(x)
    if len(x)<2 or not np.all(np.isfinite(x)): return [np.nan]*5
    n=len(x); t=np.arange(n)/fs; q=max(1,int(fs))
    return [float(np.std(x)),float(np.max(x)-np.min(x)),float(np.polyfit(t,x,1)[0]),
            float(np.mean(x[-q:])-np.mean(x[:q])),
            float(np.mean(x[n//2:])-np.mean(x[:n//2]))]

def meanseg(edf,label,a,b):
    x=edf.segment(label,a,b)
    return float(np.nanmean(x)) if len(x) else np.nan

def parse_events(txt):
    out=[]
    for r in csv.DictReader(io.StringIO(txt),delimiter="\t"):
        try:
            code=int(float(r["trial_type"])); onset=float(r["onset"])
        except Exception: continue
        if 1<=code<=9:
            out.append({"onset":onset,"target_code":str(code)})
    return out

def collect(max_subjects=0):
    m=get_json(MANIFEST); entries=m if isinstance(m,list) else m.get("files",m.get("entries",[]))
    by={epath(e):e for e in entries}
    edfs=sorted([p for p in by if p.endswith("_eeg.edf") and "/ses-3/" in p])
    subs=[s for s in PUBLIC_SUBS if any(p.startswith(s+"/") for p in edfs)]
    if max_subjects: subs=subs[:max_subjects]
    td=Path(tempfile.mkdtemp(prefix="o001r1_"))
    rows=[]; qc={"edf_files":0,"segments_seen":0,"segments_usable":0,"ecg_valid":0,"file_errors":[],"subjects":subs,"n_subjects":len(subs)}
    for si,sub in enumerate(subs,1):
        files=[p for p in edfs if p.startswith(sub+"/")]
        print(f"SUBJECT {si}/{len(subs)} {sub}: {len(files)} EDFs",flush=True)
        for p in files:
            evt=p.replace("_eeg.edf","_events.tsv")
            if evt not in by: qc["file_errors"].append({"file":p,"error":"missing events"}); continue
            local=td/(sub+"_"+Path(p).name)
            try:
                urllib.request.urlretrieve(eurl(by[p]),local)
                with urllib.request.urlopen(eurl(by[evt]),timeout=120) as rr: txt=rr.read().decode("utf-8-sig",errors="replace")
                edf=EDF(local); qc["edf_files"]+=1
                missing=[c for c in EEG_CH+["ECG","GSR","VA1","VA2"] if c not in edf.labels]
                if missing: raise RuntimeError(f"missing channels {missing}")
                events=parse_events(txt)
                for ti,tr in enumerate(events):
                    qc["segments_seen"]+=1; on=tr["onset"]
                    if on+19>edf.duration: continue
                    ef=eeg_features(edf,on+4,on+13)
                    ecg,ok=ecg_features(edf.segment("ECG",on+4,on+13),edf.fs)
                    gsr=gsr_features(edf.segment("GSR",on+4,on+13),edf.fs)
                    pv=meanseg(edf,"VA1",on+9,on+13); pa=meanseg(edf,"VA2",on+9,on+13)
                    yv=meanseg(edf,"VA1",on+14,on+19); ya=meanseg(edf,"VA2",on+14,on+19)
                    if not (np.isfinite(ef).all() and all(np.isfinite([pv,pa,yv,ya]))): continue
                    row={"subject":sub,"run":Path(p).stem,"segment":ti+1,"target_code":tr["target_code"],
                         "prior_valence":pv,"prior_arousal":pa,"y_valence":yv,"y_arousal":ya,"ecg_valid":bool(ok)}
                    for j,v in enumerate(ef): row[f"eeg_{j:03d}"]=float(v)
                    for n,v in zip(["hr_mean","hr_median","sdnn","rmssd"],ecg): row["auto_"+n]=float(v)
                    for n,v in zip(["gsr_std","gsr_range","gsr_slope","gsr_endstart","gsr_halfdiff"],gsr): row["auto_"+n]=float(v)
                    rows.append(row); qc["segments_usable"]+=1; qc["ecg_valid"]+=int(ok)
            except Exception as e:
                qc["file_errors"].append({"file":p,"error":repr(e)})
            finally:
                try: local.unlink()
                except Exception: pass
    qc["ecg_valid_fraction"]=qc["ecg_valid"]/qc["segments_usable"] if qc["segments_usable"] else 0
    return rows,qc

def pre(spec,target,eeg,auto):
    cat=["target_code"]; prior=["prior_"+target]
    trs=[("cat",OneHotEncoder(handle_unknown="ignore",sparse_output=False),cat)]
    if spec!="target_only":
        trs.append(("prior",Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler())]),prior))
    if spec in ("eeg","combined"):
        trs.append(("eeg",Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler()),("pca",PCA(n_components=20))]),eeg))
    if spec in ("autonomic","combined"):
        trs.append(("auto",Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler())]),auto))
    return ColumnTransformer(trs,sparse_threshold=0.0)

def tuned(train,test,target,spec,eeg,auto):
    ycol="y_"+target; groups=train.subject.to_numpy(); cv=GroupKFold(n_splits=min(4,len(np.unique(groups))))
    scores={a:[] for a in ALPHAS}
    for tr,va in cv.split(train,train[ycol],groups):
        A=train.iloc[tr]; B=train.iloc[va]; pp=pre(spec,target,eeg,auto)
        xa=pp.fit_transform(A); xb=pp.transform(B); ya=A[ycol].to_numpy(float); yb=B[ycol].to_numpy(float)
        for a in ALPHAS: scores[a].append(mean_absolute_error(yb,Ridge(alpha=a).fit(xa,ya).predict(xb)))
    best=min(ALPHAS,key=lambda a:(np.mean(scores[a]),a)); pp=pre(spec,target,eeg,auto)
    xa=pp.fit_transform(train); xb=pp.transform(test)
    pred=Ridge(alpha=best).fit(xa,train[ycol].to_numpy(float)).predict(xb)
    return pred,best

def boot(subj,n=5000,seed=7001):
    rng=np.random.default_rng(seed); subs=sorted(subj)
    pairs={"combined_vs_target_prior":("target_prior","combined"),
           "autonomic_increment_beyond_eeg":("eeg","combined"),
           "eeg_increment_beyond_autonomic":("autonomic","combined")}
    out={}
    for k,(a,b) in pairs.items():
        vals=np.asarray([subj[s][a]-subj[s][b] for s in subs])
        z=np.asarray([np.mean(rng.choice(vals,len(vals),replace=True)) for _ in range(n)])
        out[k]={"mean":float(np.mean(vals)),"ci95":[float(np.percentile(z,2.5)),float(np.percentile(z,97.5))]}
    return out

def analyze(rows,qc,nboot):
    import pandas as pd
    df=pd.DataFrame(rows); eeg=sorted(c for c in df if c.startswith("eeg_")); auto=sorted(c for c in df if c.startswith("auto_"))
    subs=sorted(df.subject.unique())
    gate={"minimum_subjects":len(subs)>=8,"minimum_usable_segments":len(df)>=1000,
          "minimum_ecg_valid_fraction":qc["ecg_valid_fraction"]>=.70,
          "observed":{"subjects":len(subs),"segments":len(df),"ecg_valid_fraction":qc["ecg_valid_fraction"]}}
    specs=["target_only","target_prior","eeg","autonomic","combined"]; out={}
    for target in ("valence","arousal"):
        sm={}; yy=[]; pp={s:[] for s in specs}
        for i,sub in enumerate(subs,1):
            print(f"MODEL {target} {i}/{len(subs)} {sub}",flush=True)
            tr=df[df.subject!=sub].reset_index(drop=True); te=df[df.subject==sub].reset_index(drop=True)
            y=te["y_"+target].to_numpy(float); yy.extend(y.tolist()); sm[sub]={}
            for spec in specs:
                pred,_=tuned(tr,te,target,spec,eeg,auto); pp[spec].extend(pred.tolist()); sm[sub][spec]=float(mean_absolute_error(y,pred))
        metrics={}
        Y=np.asarray(yy)
        for spec in specs:
            P=np.asarray(pp[spec]); metrics[spec]={"mae":float(mean_absolute_error(Y,P)),"r2":float(r2_score(Y,P)),
               "pearson_r":float(np.corrcoef(Y,P)[0,1]) if np.std(P)>0 and np.std(Y)>0 else None,
               "mean_subject_mae":float(np.mean([sm[s][spec] for s in subs]))}
        d=boot(sm,nboot,7001+(100 if target=="arousal" else 0))
        if not all(v for k,v in gate.items() if k!="observed"): tax="INSUFFICIENT_DATA_OR_QC"
        else:
            c0=d["combined_vs_target_prior"]["ci95"][0]>0; ca=d["autonomic_increment_beyond_eeg"]["ci95"][0]>0; ce=d["eeg_increment_beyond_autonomic"]["ci95"][0]>0
            if c0 and ca and ce: tax="BIDIRECTIONAL_COMPLEMENTARITY"
            elif c0 and ca and not ce: tax="AUTONOMIC_ADDS_ONLY"
            elif c0 and ce and not ca: tax="EEG_ADDS_ONLY"
            elif c0: tax="MULTIMODAL_INCREMENT_NO_CLEAR_COMPLEMENTARITY"
            else: tax="NO_INCREMENT_BEYOND_PRIOR_REPORT_AND_TARGET"
        out[target]={"metrics":metrics,"deltas":d,"taxonomy":tax,"subject_mae":sm}
    return {"gate":gate,"targets":out}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--max-subjects",type=int,default=0); ap.add_argument("--bootstrap",type=int,default=5000); ap.add_argument("--extract-only",action="store_true"); args=ap.parse_args()
    Path("results").mkdir(exist_ok=True)
    rows,qc=collect(args.max_subjects)
    res={"status":"O001_R1_EXTRACT_ONLY" if args.extract_only else "O001_R1_TEMPORAL_REPLICATION",
         "protocol":"protocols/observational_multimodal_redundancy_o001_r1.json","qc":qc,
         "firewall":"Same-cohort session generalization only; observational association, not causal evidence."}
    if not args.extract_only: res["analysis"]=analyze(rows,qc,args.bootstrap)
    Path("results/observational_multimodal_redundancy_o001_r1.json").write_text(json.dumps(res,indent=2),encoding="utf-8")
    print(json.dumps(res if args.extract_only else {"status":res["status"],"qc":qc,"gate":res["analysis"]["gate"],"taxonomies":{k:v["taxonomy"] for k,v in res["analysis"]["targets"].items()}},indent=2))

if __name__=="__main__": main()
