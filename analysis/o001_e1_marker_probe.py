from __future__ import annotations
import csv, io, json, tempfile, urllib.request
from pathlib import Path
import numpy as np

DATASET="on002725"; VERSION="v1.0.0"; SUB="sub-01"; TASK="genMusic01"
MANIFEST=f"https://data.nemar.org/{DATASET}/{VERSION}/manifest.json"
OUT=Path("results"); OUT.mkdir(exist_ok=True)

def gj(u):
    with urllib.request.urlopen(u,timeout=180) as r:return json.load(r)
def ep(e):
    for k in ("path","name","key","relative_path","file"):
        if isinstance(e.get(k),str):return e[k].lstrip("./")
    return ""
def eu(e):
    for k in ("bytes_url","url","download_url"):
        if isinstance(e.get(k),str) and e[k].startswith("http"):return e[k]
    return None
class EDF:
    def __init__(self,p):
        with open(p,"rb") as f:
            h=f.read(256); self.hb=int(h[184:192].decode().strip()); self.nr=int(h[236:244].decode().strip()); self.rd=float(h[244:252].decode().strip()); self.ns=int(h[252:256].decode().strip()); sh=f.read(self.hb-256)
        pos=0
        def fs(w,cast=str):
            nonlocal pos
            x=[sh[pos+i*w:pos+(i+1)*w].decode("latin1").strip() for i in range(self.ns)]; pos+=w*self.ns
            return x if cast is str else [cast(v) for v in x]
        self.labels=fs(16);fs(80);self.units=fs(8);self.pmin=fs(8,float);self.pmax=fs(8,float);self.dmin=fs(8,int);self.dmax=fs(8,int);fs(80);self.spr=fs(8,int);fs(32)
        assert len(set(self.spr))==1
        self.spr0=self.spr[0]; self.rate=self.spr0/self.rd
        total=sum(self.spr); self.mm=np.memmap(p,dtype="<i2",mode="r",offset=self.hb,shape=(self.nr,total)).reshape(self.nr,self.ns,self.spr0)
    def seg(self,label,a,b):
        i=self.labels.index(label); total=self.nr*self.spr0; ia=max(0,int(round(a*self.rate))); ib=min(total,int(round(b*self.rate)))
        r0=ia//self.spr0; r1=(ib-1)//self.spr0+1; z=np.asarray(self.mm[r0:r1,i,:],float).reshape(-1); z=z[ia-r0*self.spr0:ia-r0*self.spr0+(ib-ia)]
        return (z-self.dmin[i])*(self.pmax[i]-self.pmin[i])/(self.dmax[i]-self.dmin[i])+self.pmin[i]

m=gj(MANIFEST); es=m if isinstance(m,list) else m.get("files",m.get("entries",[])); by={ep(e):e for e in es}
base=f"{SUB}/eeg/{SUB}_task-{TASK}"; edp=base+"_eeg.edf"; evp=base+"_events.tsv"
td=Path(tempfile.mkdtemp()); lp=td/"x.edf"; urllib.request.urlretrieve(eu(by[edp]),lp)
with urllib.request.urlopen(eu(by[evp]),timeout=120) as r:txt=r.read().decode("utf-8-sig",errors="replace")
starts=[]
for row in csv.DictReader(io.StringIO(txt),delimiter="\t"):
    try:
        if int(float(row["trial_type"]))==768: starts.append(float(row["onset"]))
    except:pass
starts=sorted(starts)
ded=[]
for x in starts:
    if not ded or x-ded[-1]>.1: ded.append(x)
E=EDF(lp)
chs=["music","trialtype","ft_valance","ft_arousal","ft_ghostvalence","ft_ghostarousal","Status"]
rows=[]
for ti,on in enumerate(ded,1):
    z={"trial":ti,"onset":on}
    for ch in chs:
        x=E.seg(ch,max(0,on-.25),on+1.25)
        nz=x[np.abs(x)>1e-8]
        z[ch]={
          "min":float(np.min(x)),"max":float(np.max(x)),"median":float(np.median(x)),
          "n_nonzero":int(len(nz)),
          "first_nonzero":None if not len(nz) else float(nz[0]),
          "unique_nonzero_rounded":sorted(set(np.round(nz,6).tolist()))[:30]
        }
    # condition clues over middle of trial
    for ch in ["ft_valance","ft_arousal","ft_ghostvalence","ft_ghostarousal"]:
        x=E.seg(ch,on+2,on+38)
        z[ch+"_mid_std"]=float(np.std(x)); z[ch+"_mid_nonzero_fraction"]=float(np.mean(np.abs(x)>1e-8))
    rows.append(z)
res={"status":"O001_E1_MARKER_PROBE","raw_start_events":len(starts),"dedup_trial_starts":len(ded),"rows":rows,
     "firewall":"Schema/condition identification only. No physiology-to-affect model fit."}
(OUT/"o001_e1_marker_probe.json").write_text(json.dumps(res,indent=2),encoding="utf-8")
print(json.dumps(res,indent=2))
