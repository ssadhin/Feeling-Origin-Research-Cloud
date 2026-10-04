from __future__ import annotations
import csv, io, json, tempfile, urllib.request
from pathlib import Path
import numpy as np
from scipy.signal import welch, butter, sosfiltfilt, find_peaks

DATASET="on002725"; VERSION="v1.0.0"; SUB="sub-01"; TASK="genMusic01"
MANIFEST=f"https://data.nemar.org/{DATASET}/{VERSION}/manifest.json"
OUT=Path("results"); OUT.mkdir(exist_ok=True)

def gj(url):
    with urllib.request.urlopen(url,timeout=180) as r: return json.load(r)
def ep(e):
    for k in ("path","name","key","relative_path","file"):
        if isinstance(e.get(k),str): return e[k].lstrip("./")
    return ""
def eu(e):
    for k in ("bytes_url","url","download_url"):
        if isinstance(e.get(k),str) and e[k].startswith("http"): return e[k]
    return None

class EDF:
    def __init__(self,p):
        with open(p,"rb") as f:
            h=f.read(256)
            self.header_bytes=int(h[184:192].decode().strip()); self.n_records=int(h[236:244].decode().strip())
            self.record_duration=float(h[244:252].decode().strip()); self.n_signals=int(h[252:256].decode().strip())
            sh=f.read(self.header_bytes-256)
        pos=0
        def fields(w,cast=str):
            nonlocal pos
            xs=[sh[pos+i*w:pos+(i+1)*w].decode("latin1").strip() for i in range(self.n_signals)]
            pos+=w*self.n_signals
            return xs if cast is str else [cast(x) for x in xs]
        self.labels=fields(16); fields(80); self.units=fields(8); self.pmin=fields(8,float); self.pmax=fields(8,float)
        self.dmin=fields(8,int); self.dmax=fields(8,int); fields(80); self.spr=fields(8,int); fields(32)
        if len(set(self.spr))!=1: raise RuntimeError("unequal samples per record")
        self.spr0=self.spr[0]; self.fs=self.spr0/self.record_duration
        total=sum(self.spr)
        self.mm=np.memmap(p,dtype="<i2",mode="r",offset=self.header_bytes,
                          shape=(self.n_records,total)).reshape(self.n_records,self.n_signals,self.spr0)
        self.duration=self.n_records*self.record_duration
    def seg(self,label,a,b):
        i=self.labels.index(label); total=self.n_records*self.spr0
        ia=max(0,int(round(a*self.fs))); ib=min(total,int(round(b*self.fs)))
        if ib<=ia:return np.asarray([],float)
        r0=ia//self.spr0; r1=(ib-1)//self.spr0+1
        z=np.asarray(self.mm[r0:r1,i,:],dtype=np.float64).reshape(-1)
        z=z[ia-r0*self.spr0:ia-r0*self.spr0+(ib-ia)]
        den=self.dmax[i]-self.dmin[i]
        return (z-self.dmin[i])*(self.pmax[i]-self.pmin[i])/den+self.pmin[i]
def robust(x):
    x=np.asarray(x,float); m=np.median(x); mad=np.median(np.abs(x-m))
    if mad>0:x=np.clip(x,m-8*mad,m+8*mad)
    return x-m

m=gj(MANIFEST); entries=m if isinstance(m,list) else m.get("files",m.get("entries",[])); by={ep(e):e for e in entries}
base=f"{SUB}/eeg/{SUB}_task-{TASK}"
edf_p=base+"_eeg.edf"; evt_p=base+"_events.tsv"
if edf_p not in by or evt_p not in by: raise RuntimeError("probe files missing")
td=Path(tempfile.mkdtemp(prefix="o001e1_")); lp=td/"probe.edf"
urllib.request.urlretrieve(eu(by[edf_p]),lp)
with urllib.request.urlopen(eu(by[evt_p]),timeout=120) as r: evt=r.read().decode("utf-8-sig",errors="replace")
E=EDF(lp)
starts=[]
for row in csv.DictReader(io.StringIO(evt),delimiter="\t"):
    try:
        if int(float(row["trial_type"]))==768: starts.append(float(row["onset"]))
    except: pass

eeg=[x for x in E.labels if x in ["FP1","FP2","F3","F4","C3","C4","P3","P4","O1","O2","F7","F8","T7","T8","P7","P8","Fz","Cz","Pz","Oz","FC1","FC2","CP1","CP2","FC5","FC6","CP5","CP6","TP9","TP10","POz"]]
trial=[]
for k,on in enumerate(starts):
    end=min(on+40,E.duration)
    # label-blind metadata/QC only
    tt=E.seg("trialtype",on+1,end-1); mus=E.seg("music",on+1,end-1)
    v=E.seg("ft_valance",on+1,end-1); a=E.seg("ft_arousal",on+1,end-1)
    ecg=robust(E.seg("ECG",on+5,min(on+35,end)))
    # trial type/music summarized by robust central value
    def q(x):
        return {"median":float(np.median(x)),"min":float(np.min(x)),"max":float(np.max(x)),"std":float(np.std(x))}
    # ECG peak plausibility
    ecgq={"valid":False}
    try:
        y=sosfiltfilt(butter(2,[5,25],btype="bandpass",fs=E.fs,output="sos"),ecg); sd=np.std(y); y=y/(sd if sd>0 else 1)
        cand=[]
        for sign in (1,-1):
            pk,_=find_peaks(sign*y,distance=int(.33*E.fs),prominence=.6)
            rr=np.diff(pk)/E.fs; rr=rr[(rr>=.333)&(rr<=1.5)]
            if len(rr)>=8:
                hr=60/rr; med=float(np.median(hr))
                if 40<=med<=180:cand.append((len(rr),med,float(np.mean(hr))))
        if cand:
            best=max(cand); ecgq={"valid":True,"n_rr":best[0],"median_hr":best[1],"mean_hr":best[2]}
    except Exception as ex: ecgq={"valid":False,"error":repr(ex)}
    # spectral plausibility summary, deliberately no targets used
    x=robust(E.seg(eeg[0],on+5,min(on+35,end)))
    f,p=welch(x,fs=E.fs,nperseg=min(int(2*E.fs),len(x)),noverlap=int(E.fs))
    powers={}
    for name,lo,hi in [("delta",1,4),("theta",4,8),("alpha",8,13),("beta",13,30),("gamma",30,45),("mr_45_55",45,55),("mr_55_70",55,70)]:
        mm=(f>=lo)&(f<hi); powers[name]=float(np.trapezoid(p[mm],f[mm])) if mm.any() else 0
    trial.append({"trial":k+1,"onset":on,"duration":end-on,"trialtype":q(tt),"music":q(mus),
                  "ft_valance":q(v),"ft_arousal":q(a),"ecg":ecgq,"probe_eeg_band_power":powers})

res={"status":"O001_E1_LABEL_BLIND_SCHEMA_QC","dataset":DATASET,"subject":SUB,"task":TASK,
     "fs":E.fs,"duration_sec":E.duration,"labels":E.labels,"n_trial_starts":len(starts),
     "trials":trial,
     "gates":{
       "has_required_channels":all(x in E.labels for x in eeg+["ECG","ft_valance","ft_arousal","music","trialtype"]),
       "trial_starts_found":len(starts)>=6,
       "ecg_valid_fraction":sum(t["ecg"].get("valid",False) for t in trial)/len(trial) if trial else 0,
       "feeltrace_varies":any(t["ft_valance"]["std"]>0.05 or t["ft_arousal"]["std"]>0.05 for t in trial)
     },
     "firewall":"Label-blind schema/QC only. No relationship between EEG/ECG and felt reports is modeled; FEELTRACE is inspected only to identify reporting-trial structure and dynamic range."}
(OUT/"o001_e1_schema_qc.json").write_text(json.dumps(res,indent=2),encoding="utf-8")
print(json.dumps(res,indent=2))
