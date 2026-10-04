from __future__ import annotations
import argparse, csv, io, json, math, os, tempfile, urllib.request
from collections import defaultdict
from pathlib import Path

import numpy as np

BASE="https://data.nemar.org/on002724/v1.0.0/"
OUT=Path("results"); OUT.mkdir(exist_ok=True)
ALPHAS=[0.1,1.0,10.0,100.0]
SEED=50001
BOOT=5000
TARGET_TIMES=[6.0,10.0,14.0,18.0]
EEG_GROUPS={
 "frontal":["FP1","FPz","FP2","F7","F3","Fz","F4","F8"],
 "frontocentral":["FT9","FC5","FC1","FC2","FC6","FT10"],
 "central_temporal":["T7","C3","Cz","C4","T8"],
 "centroparietal":["TP9","CP5","CP1","CP2","CP6","TP10"],
 "parietal_occipital":["P7","P3","Pz","P4","P8","O1","O2"],
}
MOTOR_EXCLUDE={"FC5","FC1","FC2","FC6","C3","Cz","C4","CP5","CP1","CP2","CP6"}
BANDS={"theta":(4,8),"alpha":(8,13),"beta":(13,30),"lowgamma":(30,45)}

def get(url):
    with urllib.request.urlopen(url,timeout=120) as r: return r.read()

def pof(e):
    for k in ("path","name","key","relative_path","file"):
        if e.get(k): return str(e[k])
    return ""
def uof(e): return e.get("bytes_url") or BASE+pof(e)

def parse_header(path):
    with open(path,"rb") as f:
        h=f.read(256)
        hb=int(h[184:192].decode().strip()); nr=int(h[236:244].decode().strip())
        dur=float(h[244:252].decode().strip()); ns=int(h[252:256].decode().strip())
        sh=f.read(hb-256)
    pos=0
    def fields(w,cast=str):
        nonlocal pos
        z=[sh[pos+i*w:pos+(i+1)*w].decode("latin1").strip() for i in range(ns)]
        pos += w*ns
        return z if cast is str else [cast(x) for x in z]
    labels=fields(16); trans=fields(80); units=fields(8)
    pmin=fields(8,float); pmax=fields(8,float); dmin=fields(8,int); dmax=fields(8,int)
    pre=fields(80); spr=fields(8,int); res=fields(32)
    return dict(header_bytes=hb,n_records=nr,duration=dur,n_signals=ns,labels=labels,
                units=units,pmin=pmin,pmax=pmax,dmin=dmin,dmax=dmax,spr=spr)

def load_phys(path,h):
    if len(set(h["spr"]))!=1 or abs(h["duration"]-1.0)>1e-9:
        raise ValueError("nonuniform sampling/record duration")
    spr=h["spr"][0]; fs=spr/h["duration"]
    total=sum(h["spr"])
    mm=np.memmap(path,dtype="<i2",mode="r",offset=h["header_bytes"],
                 shape=(h["n_records"],total)).reshape(h["n_records"],h["n_signals"],spr)
    return mm,fs

def channel_slice(mm,h,idx,a,b,fs):
    ia=max(0,int(round(a*fs))); ib=min(h["n_records"]*h["spr"][0],int(round(b*fs)))
    spr=h["spr"][0]
    # data are record-major, channel-major; flatten one channel without copying whole file
    r0=ia//spr; r1=(ib-1)//spr
    pieces=[]
    for r in range(r0,r1+1):
        lo=ia-r*spr if r==r0 else 0
        hi=ib-r*spr if r==r1 else spr
        pieces.append(np.asarray(mm[r,idx,lo:hi],dtype=float))
    dig=np.concatenate(pieces) if pieces else np.empty(0)
    return (dig-h["dmin"][idx])*(h["pmax"][idx]-h["pmin"][idx])/(h["dmax"][idx]-h["dmin"][idx])+h["pmin"][idx]

def lin_detrend(x):
    n=len(x)
    if n<3:return x-x.mean()
    t=np.arange(n,dtype=float)
    tc=t-t.mean(); xc=x-x.mean()
    den=float(tc@tc)
    slope=float(tc@xc)/den if den else 0
    return xc-slope*tc

def band_logpowers(x,fs):
    x=lin_detrend(x)
    win=np.hanning(len(x)); y=np.fft.rfft(x*win)
    p=(np.abs(y)**2)/(max(1,(win**2).sum())*fs)
    f=np.fft.rfftfreq(len(x),1/fs)
    out={}
    for name,(lo,hi) in BANDS.items():
        m=(f>=lo)&(f<hi)
        out[name]=math.log(float(p[m].sum())+1e-12)
    return out

def eeg_features(mm,h,fs,a,b,exclude_motor=False):
    per={}
    for lab in [x for g in EEG_GROUPS.values() for x in g]:
        if exclude_motor and lab in MOTOR_EXCLUDE: continue
        idx=h["labels"].index(lab)
        per[lab]=band_logpowers(channel_slice(mm,h,idx,a,b,fs),fs)
    feats=[]
    for g,labs in EEG_GROUPS.items():
        use=[x for x in labs if x in per]
        for band in BANDS:
            feats.append(float(np.mean([per[x][band] for x in use])) if use else 0.0)
    return feats

def slope(x):
    if len(x)<2:return 0.0
    t=np.arange(len(x),dtype=float); tc=t-t.mean(); xc=x-x.mean()
    return float(tc@xc)/float(tc@tc)

def spec_power(x,fs,lo,hi):
    y=lin_detrend(x); win=np.hanning(len(y)); z=np.fft.rfft(y*win)
    p=np.abs(z)**2; f=np.fft.rfftfreq(len(y),1/fs); m=(f>=lo)&(f<hi)
    return float(p[m].sum()), f[m], p[m]

def autonomic_features(mm,h,fs,a,b):
    vals=[]
    for lab in ("ECG","GSR"):
        idx=h["labels"].index(lab); x=channel_slice(mm,h,idx,a,b,fs)
        d=np.diff(x)
        vals += [float(x.mean()),float(x.std()),slope(x),float(np.sqrt(np.mean(d*d)))]
        if lab=="ECG":
            power,f,p=spec_power(x,fs,0.8,2.5)
            vals += [math.log(power+1e-12), float(f[int(np.argmax(p))]) if len(p) else 0.0]
        else:
            q=max(1,int(0.5*fs))
            vals += [float(x[-q:].mean()-x[:q].mean()), math.log(spec_power(x,fs,0.01,0.5)[0]+1e-12)]
    return vals

def mean_channel(mm,h,fs,lab,a,b):
    return float(channel_slice(mm,h,h["labels"].index(lab),a,b,fs).mean())

def parse_subject_session_run(path):
    parts=path.split("/")
    sub=parts[0]; ses=parts[1]
    fn=parts[-1]
    run=fn.split("_task-run")[1].split("_")[0]
    return sub,ses,run

def extract_dataset(max_runs=None):
    manifest=json.loads(get(BASE+"manifest.json"))
    entries=manifest if isinstance(manifest,list) else manifest.get("files",manifest.get("entries",[]))
    edfs={pof(e):e for e in entries if pof(e).endswith("_eeg.edf")}
    events={pof(e):e for e in entries if pof(e).endswith("_events.tsv")}
    rows=[]; qc=[]; td=Path(tempfile.mkdtemp(prefix="o001_"))
    for k,path in enumerate(sorted(edfs)):
        if max_runs is not None and k>=max_runs: break
        stem=path[:-8] # remove _eeg.edf
        ep=stem+"_events.tsv"
        if ep not in events: qc.append({"path":path,"status":"NO_EVENTS"}); continue
        sub,ses,run=parse_subject_session_run(path)
        local=td/f"r{k}.edf"
        try:
            urllib.request.urlretrieve(uof(edfs[path]),local)
            h=parse_header(local)
            required=set(sum(EEG_GROUPS.values(),[])+["ECG","GSR","VA1","VA2","VAtarg"])
            missing=sorted(required-set(h["labels"]))
            if missing or h["n_signals"]<37:
                qc.append({"path":path,"status":"MISSING_CHANNELS","missing":missing}); continue
            mm,fs=load_phys(local,h)
            if abs(fs-1000)>1e-9:
                qc.append({"path":path,"status":"BAD_FS","fs":fs}); continue
            erows=list(csv.DictReader(io.StringIO(get(uof(events[ep])).decode("utf-8-sig")),delimiter="\t"))
            made=0
            for ei,ev in enumerate(erows):
                onset=float(ev["onset"]); dur=float(ev["duration"])
                for tau_rel in TARGET_TIMES:
                    if tau_rel+1>min(dur,20.0): continue
                    tau=onset+tau_rel
                    y1=mean_channel(mm,h,fs,"VA1",tau,tau+1)
                    y2=mean_channel(mm,h,fs,"VA2",tau,tau+1)
                    p1=mean_channel(mm,h,fs,"VA1",tau-2,tau-1)
                    p2=mean_channel(mm,h,fs,"VA2",tau-2,tau-1)
                    vt=int(round(mean_channel(mm,h,fs,"VAtarg",tau-3,tau-2)))
                    a=tau-6; b=tau-2
                    af=autonomic_features(mm,h,fs,a,b)
                    ef=eeg_features(mm,h,fs,a,b,False)
                    ef_nomotor=eeg_features(mm,h,fs,a,b,True)
                    row=dict(subject=sub,session=ses,run=f"{sub}/{ses}/run{run}",
                        event=ei,tau_rel=tau_rel,y1=y1,y2=y2,prior1=p1,prior2=p2,
                        vtarget=vt,auto=af,eeg=ef,eeg_nomotor=ef_nomotor)
                    if tau_rel in (10.0,14.0,18.0):
                        row["prior1_s2"]=mean_channel(mm,h,fs,"VA1",tau-3,tau-2)
                        row["prior2_s2"]=mean_channel(mm,h,fs,"VA2",tau-3,tau-2)
                        row["vtarget_s2"]=int(round(mean_channel(mm,h,fs,"VAtarg",tau-5,tau-4)))
                        row["auto_s2"]=autonomic_features(mm,h,fs,tau-8,tau-4)
                        row["eeg_s2"]=eeg_features(mm,h,fs,tau-8,tau-4,False)
                        row["eeg_nomotor_s2"]=eeg_features(mm,h,fs,tau-8,tau-4,True)
                    rows.append(row)
                    made+=1
            qc.append({"path":path,"status":"OK","samples":made,"subject":sub,"session":ses,"run":run})
            del mm
        except Exception as ex:
            qc.append({"path":path,"status":"ERROR","error":repr(ex)})
        finally:
            try: local.unlink()
            except: pass
    return rows,qc

def baseline_vec(r,target_free=False,variant="primary"):
    if variant=="s2":
        z=[r["prior1_s2"],r["prior2_s2"]]
        vt=r["vtarget_s2"]
        times=(10.0,14.0,18.0)
    else:
        z=[r["prior1"],r["prior2"]]
        vt=r["vtarget"]
        times=TARGET_TIMES
    if not target_free:
        z += [1.0 if vt==j else 0.0 for j in range(10)]
    z += [1.0 if r["tau_rel"]==t else 0.0 for t in times]
    return z

def feature_vec(r,kind,target_free=False,no_motor=False,variant="primary"):
    z=baseline_vec(r,target_free,variant)
    if variant=="s2":
        if "A" in kind:z+=r["auto_s2"]
        if "E" in kind:z+=(r["eeg_nomotor_s2"] if no_motor else r["eeg_s2"])
    else:
        if "A" in kind:z+=r["auto"]
        if "E" in kind:z+=(r["eeg_nomotor"] if no_motor else r["eeg"])
    return z

def ridge_fit(X,y,alpha):
    X=np.asarray(X,float); y=np.asarray(y,float)
    mu=X.mean(0); sd=X.std(0); sd[sd<1e-10]=1
    Z=(X-mu)/sd
    ym=y.mean(); yc=y-ym
    A=Z.T@Z + alpha*np.eye(Z.shape[1])
    beta=np.linalg.solve(A,Z.T@yc)
    return mu,sd,ym,beta

def predict(model,X):
    mu,sd,ym,beta=model
    return ((np.asarray(X,float)-mu)/sd)@beta+ym

def rmse(y,p): return float(np.sqrt(np.mean((np.asarray(y)-np.asarray(p))**2)))
def r2(y,p):
    y=np.asarray(y); p=np.asarray(p); den=float(((y-y.mean())**2).sum())
    return None if den<1e-12 else float(1-((y-p)**2).sum()/den)

def choose_alpha(train,kind,outcome,target_free=False,no_motor=False,variant="primary"):
    runs=sorted({r["run"] for r in train})
    if len(runs)<2:return 10.0
    scores={a:[] for a in ALPHAS}
    for vr in runs:
        tr=[r for r in train if r["run"]!=vr]; va=[r for r in train if r["run"]==vr]
        if not tr or not va: continue
        Xt=[feature_vec(r,kind,target_free,no_motor,variant) for r in tr]
        yt=[r[outcome] for r in tr]; Xv=[feature_vec(r,kind,target_free,no_motor,variant) for r in va]
        yv=[r[outcome] for r in va]
        for a in ALPHAS:
            try:scores[a].append(rmse(yv,predict(ridge_fit(Xt,yt,a),Xv)))
            except np.linalg.LinAlgError:scores[a].append(1e99)
    return min(ALPHAS,key=lambda a:np.mean(scores[a]) if scores[a] else 1e99)

def evaluate(rows,target_free=False,no_motor=False,variant="primary"):
    use=[r for r in rows if variant!="s2" or r["tau_rel"] in (10.0,14.0,18.0)]
    result=[]
    bysub=defaultdict(list)
    for r in use:bysub[r["subject"]].append(r)
    for sub,sr in sorted(bysub.items()):
        sessions=sorted({r["session"] for r in sr})
        if len(sessions)<2: continue
        for test_ses in sessions:
            te=[r for r in sr if r["session"]==test_ses]
            tr=[r for r in sr if r["session"]!=test_ses]
            if len({r["run"] for r in te})<2 or len({r["run"] for r in tr})<2: continue
            fold={"subject":sub,"test_session":test_ses,"n_train":len(tr),"n_test":len(te),"axes":{}}
            for outcome in ("y1","y2"):
                ax={}
                for kind in ("B","BA","BE","BAE"):
                    alpha=choose_alpha(tr,kind,outcome,target_free,no_motor,variant)
                    Xtr=[feature_vec(r,kind,target_free,no_motor,variant) for r in tr]
                    ytr=[r[outcome] for r in tr]
                    Xte=[feature_vec(r,kind,target_free,no_motor,variant) for r in te]
                    yte=[r[outcome] for r in te]
                    pr=predict(ridge_fit(Xtr,ytr,alpha),Xte)
                    ax[kind]={"alpha":alpha,"rmse":rmse(yte,pr),"r2":r2(yte,pr)}
                ax["delta_E_given_A"]=ax["BA"]["rmse"]-ax["BAE"]["rmse"]
                ax["delta_A_given_E"]=ax["BE"]["rmse"]-ax["BAE"]["rmse"]
                fold["axes"][outcome]=ax
            result.append(fold)
    return result

def bootstrap(folds,key):
    # participant-level cluster bootstrap: resample subjects, retain all folds
    by=defaultdict(list)
    for f in folds:
        vals=[f["axes"][a][key] for a in ("y1","y2")]
        by[f["subject"]].append(float(np.mean(vals)))
    subs=sorted(by)
    rng=np.random.default_rng(SEED+(0 if key=="delta_E_given_A" else 1))
    vals=[]
    for _ in range(BOOT):
        ss=rng.choice(subs,size=len(subs),replace=True)
        x=[]
        for s in ss:x.extend(by[s])
        vals.append(float(np.mean(x)))
    point=float(np.mean([v for s in subs for v in by[s]]))
    return {"mean":point,"ci95":[float(np.percentile(vals,2.5)),float(np.percentile(vals,97.5))],
            "n_subjects":len(subs),"n_folds":len(folds)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--max-runs",type=int,default=None)
    ap.add_argument("--extract-only",action="store_true")
    args=ap.parse_args()
    rows,qc=extract_dataset(args.max_runs)
    okruns=[x for x in qc if x["status"]=="OK"]
    if args.extract_only:
        out={"status":"O001_EXTRACTION_PREFLIGHT_ONLY","n_rows":len(rows),"n_ok_runs":len(okruns),
             "subjects":sorted({r["subject"] for r in rows}),"qc":qc,
             "feature_lengths":{
               "baseline":len(baseline_vec(rows[0])) if rows else 0,
               "autonomic":len(rows[0]["auto"]) if rows else 0,
               "eeg":len(rows[0]["eeg"]) if rows else 0,
               "eeg_nomotor":len(rows[0]["eeg_nomotor"]) if rows else 0,
               "s2_present":bool(rows and any("auto_s2" in r for r in rows))
             }}
        (OUT/"o001_extraction_preflight.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
        print(json.dumps(out,indent=2))
        return
    subs=sorted({r["subject"] for r in rows})
    folds=evaluate(rows)
    nm=evaluate(rows,no_motor=True)
    s2=evaluate(rows,variant="s2")
    tf=evaluate(rows,target_free=True)
    primary={k:bootstrap(folds,k) for k in ("delta_E_given_A","delta_A_given_E")}
    sens_nm={k:bootstrap(nm,k) for k in ("delta_E_given_A","delta_A_given_E")}
    sens_s2={k:bootstrap(s2,k) for k in ("delta_E_given_A","delta_A_given_E")}
    sens_tf={k:bootstrap(tf,k) for k in ("delta_E_given_A","delta_A_given_E")}
    nsub=len({f["subject"] for f in folds})
    def passed(x):return x["ci95"][0]>0
    if nsub<5: cls="INSUFFICIENT_PARTICIPANTS"
    else:
        ep=passed(primary["delta_E_given_A"]); ap=passed(primary["delta_A_given_E"])
        cls="OBSERVATIONAL_COMPLEMENTARITY" if ep and ap else "EEG_PREDICTIVE_DOMINANCE" if ep else "AUTONOMIC_PREDICTIVE_DOMINANCE" if ap else "NO_DETECTED_UNIQUE_COMPLEMENTARITY"
    out={"status":"O001_OBSERVATIONAL_ONLY","classification":cls,
         "dataset":{"base":BASE,"n_rows":len(rows),"n_ok_runs":len(okruns),"subjects":subs},
         "primary":primary,"motor_exclusion":sens_nm,"stronger_temporal_separation":sens_s2,
         "target_free_baseline":sens_tf,"folds":folds,"qc":qc,
         "flags":{
            "motor_report_contamination_plausible":passed(primary["delta_E_given_A"]) and not passed(sens_nm["delta_E_given_A"]),
            "eeg_short_lag_dependence":passed(primary["delta_E_given_A"]) and not passed(sens_s2["delta_E_given_A"]),
            "autonomic_short_lag_dependence":passed(primary["delta_A_given_E"]) and not passed(sens_s2["delta_A_given_E"])
         },
         "firewall":"Predictive complementarity/dominance is not causal origin, necessity, sufficiency, or phenomenal identity. VA1/VA2 axis ordering is not assumed."}
    (OUT/"o001_observational_multimodal_redundancy.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
    print(json.dumps({k:out[k] for k in ("status","classification","dataset","primary","motor_exclusion","stronger_temporal_separation","target_free_baseline","flags")},indent=2))

if __name__=="__main__":main()
