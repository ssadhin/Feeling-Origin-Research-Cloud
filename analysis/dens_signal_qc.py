from __future__ import annotations
import csv, json, tempfile, urllib.request
from pathlib import Path
import numpy as np

OUT=Path("results"); OUT.mkdir(exist_ok=True)
MANIFEST="https://data.nemar.org/on003751/v1.0.0/manifest.json"
SUB="sub-mit003"

def manifest():
    with urllib.request.urlopen(MANIFEST,timeout=120) as r: return json.load(r)
def path(e):
    for k in ("path","name","key","relative_path","file"):
        if isinstance(e.get(k),str): return e[k].lstrip("./")
    return ""
def url(e):
    for k in ("bytes_url","url","download_url"):
        if isinstance(e.get(k),str) and e[k].startswith("http"): return e[k]
    return None

m=manifest(); es=m if isinstance(m,list) else m.get("files",m.get("entries",[]))
tmp=Path(tempfile.mkdtemp(prefix="densqc_"))
downloads={}
for e in es:
    p=path(e)
    if SUB in p and p.endswith(("_task-Emotion_eeg.set","_task-Emotion_eeg.fdt")):
        dest=tmp/Path(p).name; urllib.request.urlretrieve(url(e),dest); downloads[p]=dest
for p in [f"{SUB}/beh/{SUB}_task-Emotion_beh.tsv",f"{SUB}/eeg/{SUB}_task-emotion_events.tsv"]:
    dest=tmp/Path(p).name
    urllib.request.urlretrieve("https://raw.githubusercontent.com/nemarDatasets/on003751/main/"+p,dest)
    downloads[p]=dest

import mne
from scipy.signal import welch
import neurokit2 as nk
raw=mne.io.read_raw_eeglab(next(str(v) for k,v in downloads.items() if k.endswith(".set")),preload=True,verbose="ERROR")
sf=float(raw.info["sfreq"])
eeg_names=[f"E{i}" for i in range(1,129) if f"E{i}" in raw.ch_names]
ecg_name="ECG"
ev=[]
with open(next(v for k,v in downloads.items() if k.endswith("_events.tsv")),encoding="utf-8-sig") as f:
    ev=list(csv.DictReader(f,delimiter="\t"))
stim=[float(r["onset"])/1000 for r in ev if r["trial_type"]=="stm"]

bands={"delta":(1,4),"theta":(4,8),"alpha":(8,13),"beta":(13,30),"gamma":(30,45)}
trial_qc=[]
for ti,on in enumerate(stim):
    # fixed label-blind analysis window: seconds 1 through 14 after stimulus onset
    a=int(round((on+1.0)*sf)); b=int(round((on+14.0)*sf))
    eeg=raw.get_data(picks=eeg_names,start=a,stop=b)
    ecg=raw.get_data(picks=[ecg_name],start=a,stop=b)[0]
    freqs,psd=welch(eeg,fs=sf,nperseg=min(int(2*sf),eeg.shape[1]),axis=1,detrend="constant")
    mask=(freqs>=1)&(freqs<=45)
    total=np.trapz(psd[:,mask],freqs[mask],axis=1)+1e-20
    bp={}
    for name,(lo,hi) in bands.items():
        mm=(freqs>=lo)&(freqs<hi)
        rel=np.trapz(psd[:,mm],freqs[mm],axis=1)/total
        bp[name]={"median":float(np.median(rel)),"iqr":float(np.percentile(rel,75)-np.percentile(rel,25))}
    # ECG detection on 13 sec segment; no outcome labels used
    try:
        clean=nk.ecg_clean(ecg,sampling_rate=sf,method="neurokit")
        _,info=nk.ecg_peaks(clean,sampling_rate=sf,method="neurokit")
        peaks=np.asarray(info["ECG_R_Peaks"],dtype=int)
        rr=np.diff(peaks)/sf
        rr=rr[(rr>=0.33)&(rr<=1.5)]
        hr=60/rr if len(rr) else np.asarray([])
        ecgq={
          "n_peaks":int(len(peaks)),
          "n_valid_rr":int(len(rr)),
          "median_hr":None if not len(hr) else float(np.median(hr)),
          "mean_hr":None if not len(hr) else float(np.mean(hr)),
          "rmssd_sec":None if len(rr)<3 else float(np.sqrt(np.mean(np.diff(rr)**2))),
        }
    except Exception as e:
        ecgq={"error":repr(e),"n_peaks":0,"n_valid_rr":0,"median_hr":None}
    trial_qc.append({"trial":ti+1,"eeg_relative_band_summary":bp,"ecg":ecgq})

valid=[x for x in trial_qc if x["ecg"].get("n_valid_rr",0)>=6 and x["ecg"].get("median_hr") is not None and 40<=x["ecg"]["median_hr"]<=180]
result={
 "status":"DENS_LABEL_BLIND_SIGNAL_QC",
 "subject":SUB,
 "window_sec":[1.0,14.0],
 "n_eeg_channels":len(eeg_names),
 "eeg_channels":eeg_names,
 "ecg_channel":ecg_name,
 "n_trials":len(trial_qc),
 "n_ecg_valid_trials":len(valid),
 "ecg_valid_fraction":len(valid)/len(trial_qc) if trial_qc else 0,
 "trial_qc":trial_qc,
 "gate":{
   "eeg_feature_extraction_ok":len(eeg_names)==128 and all(all(np.isfinite(list(v.values()))) for v in [t["eeg_relative_band_summary"]["alpha"] for t in trial_qc]),
   "ecg_peak_extraction_ok":len(valid)>=max(7,int(0.7*len(trial_qc)))
 },
 "firewall":"QC is label-blind. Self-reported valence/arousal are not loaded or inspected. No feature/model choice is based on target performance."
}
(OUT/"dens_signal_qc.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result,indent=2))
