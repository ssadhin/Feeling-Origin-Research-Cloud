from __future__ import annotations

import argparse, io, json, math, urllib.request, zipfile, hashlib
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.signal import butter, sosfiltfilt, find_peaks, welch
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

FIGSHARE_URL="https://ndownloader.figshare.com/files/16260497"
EXPECTED_MD5="5e679ce69d6602c5f8225f03c489df76"
EMOTIONAL_VIDEOS={1,2,3,4,5,6,7,8}
ALPHAS=[0.1,1.0,10.0,100.0,1000.0]

def robust(x):
    x=np.asarray(x,float)
    med=np.nanmedian(x); mad=np.nanmedian(np.abs(x-med))
    if np.isfinite(mad) and mad>0: x=np.clip(x,med-8*mad,med+8*mad)
    return x-med

def rr_features(x,fs,kind):
    x=robust(x)
    if len(x)<int(3*fs) or not np.all(np.isfinite(x)): return [np.nan]*4,False
    try:
        if kind=="ecg":
            sos=butter(2,[5,25],btype="bandpass",fs=fs,output="sos")
            min_dist=.333; prom=.6
        else:
            sos=butter(2,[0.5,5],btype="bandpass",fs=fs,output="sos")
            min_dist=.35; prom=.25
        y=sosfiltfilt(sos,x); sd=np.std(y)
        if not np.isfinite(sd) or sd<=1e-12: return [np.nan]*4,False
        y=y/sd; candidates=[]
        for sign in (1,-1):
            peaks,_=find_peaks(sign*y,distance=max(1,int(min_dist*fs)),prominence=prom)
            rr=np.diff(peaks)/fs; rr=rr[(rr>=.333)&(rr<=1.5)]
            if len(rr)>=5:
                hr=60/rr; med=float(np.median(hr))
                if 40<=med<=180:
                    candidates.append((len(rr),-float(np.std(rr)/(np.mean(rr)+1e-12)),rr,hr))
        if not candidates: return [np.nan]*4,False
        _,_,rr,hr=max(candidates,key=lambda z:(z[0],z[1]))
        return [float(np.mean(hr)),float(np.median(hr)),float(np.std(rr,ddof=1)),float(np.sqrt(np.mean(np.diff(rr)**2)))],True
    except Exception:
        return [np.nan]*4,False

def lin_slope(x,fs):
    x=np.asarray(x,float)
    if len(x)<2:return np.nan
    t=np.arange(len(x))/fs
    return float(np.polyfit(t,x,1)[0])

def gsr_feats(x,fs):
    x=robust(x); n=len(x); q=max(1,int(fs))
    if n<2:return [np.nan]*5
    return [float(np.std(x)),float(np.ptp(x)),lin_slope(x,fs),
            float(np.mean(x[-q:])-np.mean(x[:q])),
            float(np.mean(x[n//2:])-np.mean(x[:n//2]))]

def resp_feats(x,fs):
    x=robust(x)
    if len(x)<int(5*fs):return [np.nan]*3
    f,p=welch(x,fs=fs,nperseg=min(len(x),int(8*fs)),detrend="constant")
    m=(f>=0.08)&(f<=0.7)
    rate=float(f[m][np.argmax(p[m])]*60) if np.any(m) else np.nan
    return [rate,float(np.std(x)),lin_slope(x,fs)]

def temp_feats(x,fs):
    x=np.asarray(x,float); n=len(x); q=max(1,int(fs))
    if n<2:return [np.nan]*4
    return [float(np.mean(x)),float(np.std(x)),lin_slope(x,fs),float(np.mean(x[-q:])-np.mean(x[:q]))]

def emg_feats(x):
    x=robust(x)
    if len(x)<2:return [np.nan]*3
    return [float(np.sqrt(np.mean(x*x))),float(np.mean(np.abs(x))),float(np.std(x))]

def subset_by_rel(df,timecol,start_ms,a,b):
    rel=(df[timecol].to_numpy(float)-start_ms)/1000.0
    m=(rel>=a)&(rel<b)
    return df.loc[m]

def extract_subject(z,sub):
    ap=f"CASE_full/data/interpolated/annotations/sub_{sub}.csv"
    pp=f"CASE_full/data/interpolated/physiological/sub_{sub}.csv"
    with z.open(ap) as f: ann=pd.read_csv(f)
    with z.open(pp) as f: phy=pd.read_csv(f)
    rows=[]; qc={"windows_seen":0,"windows_usable":0,"ecg_valid":0,"bvp_valid":0}
    for vid in sorted(EMOTIONAL_VIDEOS):
        A=ann[ann.video==vid]
        P=phy[phy.video==vid]
        if A.empty or P.empty: continue
        a0=float(A.jstime.iloc[0]); p0=float(P.daqtime.iloc[0])
        adur=(float(A.jstime.iloc[-1])-a0)/1000.0
        pdur=(float(P.daqtime.iloc[-1])-p0)/1000.0
        dur=min(adur,pdur)
        anchors=np.arange(20.0,max(20.0,dur-6.0)+1e-9,10.0)
        for anchor in anchors:
            qc["windows_seen"]+=1
            PS=subset_by_rel(P,"daqtime",p0,anchor-10,anchor-1)
            PR=subset_by_rel(A,"jstime",a0,anchor-5,anchor-1)
            TY=subset_by_rel(A,"jstime",a0,anchor,anchor+5)
            if len(PS)<5000 or PR.empty or TY.empty: continue
            fs=1000.0
            ecg,eok=rr_features(PS.ecg.to_numpy(float),fs,"ecg")
            bvp,bok=rr_features(PS.bvp.to_numpy(float),fs,"bvp")
            gsr=gsr_feats(PS.gsr.to_numpy(float),fs)
            rsp=resp_feats(PS.rsp.to_numpy(float),fs)
            skt=temp_feats(PS.skt.to_numpy(float),fs)
            ez=emg_feats(PS.emg_zygo.to_numpy(float)); ec=emg_feats(PS.emg_coru.to_numpy(float)); et=emg_feats(PS.emg_trap.to_numpy(float))
            pv=float(PR.valence.mean()); pa=float(PR.arousal.mean())
            yv=float(TY.valence.mean()); ya=float(TY.arousal.mean())
            if not all(np.isfinite([pv,pa,yv,ya])): continue
            row={"subject":f"sub-{sub:02d}","video_id":str(vid),"time_norm":float(anchor/dur),
                 "prior_valence":pv,"prior_arousal":pa,"y_valence":yv,"y_arousal":ya,
                 "ecg_valid":bool(eok),"bvp_valid":bool(bok)}
            vals=ecg+bvp+gsr+rsp+skt+ez+ec+et
            names=["ecg_hr_mean","ecg_hr_median","ecg_sdnn","ecg_rmssd",
                   "bvp_hr_mean","bvp_hr_median","bvp_sdnn","bvp_rmssd",
                   "gsr_std","gsr_range","gsr_slope","gsr_endstart","gsr_halfdiff",
                   "rsp_rate","rsp_std","rsp_slope",
                   "skt_mean","skt_std","skt_slope","skt_endstart",
                   "emg_zygo_rms","emg_zygo_abs","emg_zygo_std",
                   "emg_coru_rms","emg_coru_abs","emg_coru_std",
                   "emg_trap_rms","emg_trap_abs","emg_trap_std"]
            for n,v in zip(names,vals): row["phys_"+n]=float(v)
            rows.append(row); qc["windows_usable"]+=1; qc["ecg_valid"]+=int(eok); qc["bvp_valid"]+=int(bok)
    return rows,qc

def preprocess(spec,target,phys):
    cat=["video_id"]; time=["time_norm"]; prior=["prior_"+target]
    trs=[
      ("cat",OneHotEncoder(handle_unknown="ignore",sparse_output=False),cat),
      ("time",Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler())]),time)
    ]
    if spec!="stimulus_time_only":
        trs.append(("prior",Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler())]),prior))
    if spec=="peripheral":
        trs.append(("phys",Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler())]),phys))
    return ColumnTransformer(trs,sparse_threshold=0.0)

def fit_tuned(train,test,target,spec,phys):
    ycol="y_"+target; groups=train.subject.to_numpy()
    cv=GroupKFold(n_splits=min(5,len(np.unique(groups))))
    scores={a:[] for a in ALPHAS}
    for it,iv in cv.split(train,train[ycol],groups):
        A=train.iloc[it]; B=train.iloc[iv]; pp=preprocess(spec,target,phys)
        xa=pp.fit_transform(A); xb=pp.transform(B)
        ya=A[ycol].to_numpy(float); yb=B[ycol].to_numpy(float)
        for a in ALPHAS:
            scores[a].append(mean_absolute_error(yb,Ridge(alpha=a).fit(xa,ya).predict(xb)))
    best=min(ALPHAS,key=lambda a:(float(np.mean(scores[a])),a))
    pp=preprocess(spec,target,phys); xa=pp.fit_transform(train); xb=pp.transform(test)
    pred=Ridge(alpha=best).fit(xa,train[ycol].to_numpy(float)).predict(xb)
    return pred,best

def boot(vals,n,seed):
    rng=np.random.default_rng(seed); vals=np.asarray(vals,float)
    z=np.asarray([np.mean(rng.choice(vals,size=len(vals),replace=True)) for _ in range(n)])
    return {"mean":float(np.mean(vals)),"ci95":[float(np.percentile(z,2.5)),float(np.percentile(z,97.5))]}

def analyze(rows,qc,nboot):
    df=pd.DataFrame(rows); phys=sorted(c for c in df if c.startswith("phys_")); subs=sorted(df.subject.unique())
    counts=df.groupby("subject").size()
    gate={"minimum_subjects":len(subs)>=24,
          "minimum_total_windows":len(df)>=1000,
          "minimum_subjects_with_20_windows":int((counts>=20).sum())>=24,
          "minimum_ECG_valid_fraction":qc["ecg_valid_fraction"]>=.70,
          "observed":{"subjects":len(subs),"windows":len(df),"subjects_with_20_windows":int((counts>=20).sum()),"ecg_valid_fraction":qc["ecg_valid_fraction"]}}
    specs=["stimulus_time_only","stimulus_time_prior","peripheral"]; out={}
    for target in ("valence","arousal"):
        sm={}; pooled_y=[]; pooled={s:[] for s in specs}; alphas={s:[] for s in specs}
        for i,sub in enumerate(subs,1):
            print(f"MODEL {target} {i}/{len(subs)} {sub}",flush=True)
            tr=df[df.subject!=sub].reset_index(drop=True); te=df[df.subject==sub].reset_index(drop=True)
            y=te["y_"+target].to_numpy(float); pooled_y.extend(y.tolist()); sm[sub]={}
            for spec in specs:
                pred,a=fit_tuned(tr,te,target,spec,phys); pooled[spec].extend(pred.tolist()); alphas[spec].append({"subject":sub,"alpha":a})
                sm[sub][spec]=float(mean_absolute_error(y,pred))
        Y=np.asarray(pooled_y); metrics={}
        for spec in specs:
            P=np.asarray(pooled[spec]); metrics[spec]={"mae":float(mean_absolute_error(Y,P)),"r2":float(r2_score(Y,P)),
                "pearson_r":float(np.corrcoef(Y,P)[0,1]) if np.std(P)>0 and np.std(Y)>0 else None,
                "mean_subject_mae":float(np.mean([sm[s][spec] for s in subs]))}
        dif=[sm[s]["stimulus_time_prior"]-sm[s]["peripheral"] for s in subs]
        delta=boot(dif,nboot,8200+(0 if target=="valence" else 1))
        if not all(v for k,v in gate.items() if k!="observed"): verdict="INSUFFICIENT_DATA_OR_QC"
        elif delta["ci95"][0]>0: verdict="PERIPHERAL_INCREMENT"
        else: verdict="NO_PERIPHERAL_INCREMENT"
        out[target]={"verdict":verdict,"metrics":metrics,"primary_delta":delta,"subject_mae":sm,"chosen_alphas":alphas}
    return {"gate":gate,"targets":out,"n_phys_features":len(phys)}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--bootstrap",type=int,default=5000); ap.add_argument("--max-subjects",type=int,default=0); ap.add_argument("--extract-only",action="store_true"); args=ap.parse_args()
    OUT=Path("results"); OUT.mkdir(exist_ok=True); zpath=OUT/"CASE_full.zip"
    if not zpath.exists():
        print("DOWNLOAD full CASE 4.55GB",flush=True); urllib.request.urlretrieve(FIGSHARE_URL,zpath)
    md5=hashlib.md5()
    with open(zpath,"rb") as f:
        for chunk in iter(lambda:f.read(8<<20),b""): md5.update(chunk)
    md5hex=md5.hexdigest()
    if md5hex!=EXPECTED_MD5: raise RuntimeError(f"MD5 mismatch {md5hex}")
    rows=[]; total={"windows_seen":0,"windows_usable":0,"ecg_valid":0,"bvp_valid":0,"subjects":[],"file_errors":[]}
    subs=list(range(1,31));
    if args.max_subjects: subs=subs[:args.max_subjects]
    with zipfile.ZipFile(zpath) as z:
        names=set(z.namelist())
        for i,sub in enumerate(subs,1):
            print(f"SUBJECT {i}/{len(subs)} {sub}",flush=True)
            apath=f"CASE_full/data/interpolated/annotations/sub_{sub}.csv"; ppath=f"CASE_full/data/interpolated/physiological/sub_{sub}.csv"
            if apath not in names or ppath not in names:
                total["file_errors"].append({"subject":sub,"error":"missing processed CSV"}); continue
            try:
                rr,q=extract_subject(z,sub); rows.extend(rr); total["subjects"].append(sub)
                for k in ("windows_seen","windows_usable","ecg_valid","bvp_valid"): total[k]+=q[k]
            except Exception as e:
                total["file_errors"].append({"subject":sub,"error":repr(e)})
    total["n_subjects"]=len(total["subjects"]); total["ecg_valid_fraction"]=total["ecg_valid"]/total["windows_usable"] if total["windows_usable"] else 0
    total["bvp_valid_fraction"]=total["bvp_valid"]/total["windows_usable"] if total["windows_usable"] else 0
    base={"status":"O002_EXTRACT_ONLY" if args.extract_only else "O002_CASE_EXTERNAL_REPLICATION",
          "protocol":"protocols/case_external_replication_o002.json","dataset_md5":md5hex,"qc":total,
          "firewall":"Independent observational peripheral-physiology replication only; no causal or phenomenal-identity inference."}
    with open(OUT/"o002_feature_rows.jsonl","w",encoding="utf-8") as f:
        for r in rows:f.write(json.dumps(r,separators=(",",":"))+"\n")
    if not args.extract_only: base["analysis"]=analyze(rows,total,args.bootstrap)
    (OUT/"case_external_replication_o002.json").write_text(json.dumps(base,indent=2),encoding="utf-8")
    print(json.dumps(base if args.extract_only else {"status":base["status"],"qc":total,"gate":base["analysis"]["gate"],"targets":{t:{"verdict":v["verdict"],"delta":v["primary_delta"]} for t,v in base["analysis"]["targets"].items()}},indent=2))
    zpath.unlink()

if __name__=="__main__": main()
