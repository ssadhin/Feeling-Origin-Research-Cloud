from __future__ import annotations
import csv, io, json, urllib.request
from pathlib import Path
import numpy as np

BASE="https://data.nemar.org/on002724/v1.0.0/"
OUT=Path("results"); OUT.mkdir(exist_ok=True)

with urllib.request.urlopen(BASE+"manifest.json",timeout=60) as r:
    manifest=json.loads(r.read())
entries=manifest if isinstance(manifest,list) else manifest.get("files",manifest.get("entries",[]))

def path_of(e):
    for k in ("path","name","key","relative_path","file"):
        if e.get(k): return str(e[k])
    return ""
def url_of(e):
    return e.get("bytes_url") or BASE+path_of(e)

edf_entries=sorted([e for e in entries if path_of(e).endswith("_eeg.edf")],key=lambda e:path_of(e))
if not edf_entries: raise RuntimeError("No EDFs")
e=edf_entries[0]
edf_path=OUT/"schema_probe.edf"
urllib.request.urlretrieve(url_of(e),edf_path)

stem=path_of(e).replace("_eeg.edf","")
ev_path=stem+"_events.tsv"
ev_e=next(x for x in entries if path_of(x)==ev_path)
with urllib.request.urlopen(url_of(ev_e),timeout=60) as r:
    event_text=r.read().decode("utf-8-sig")
events=list(csv.DictReader(io.StringIO(event_text),delimiter="\t"))

# Minimal EDF fixed-header parser. The public files use an anonymized invalid
# start date (e.g. 00.00.14), which strict EDF libraries reject. Date/time are
# irrelevant to signal values and are not used here.
with open(edf_path,"rb") as fh:
    h=fh.read(256)
    startdate=h[168:176].decode("latin1").strip()
    starttime=h[176:184].decode("latin1").strip()
    header_bytes=int(h[184:192].decode().strip())
    n_records=int(h[236:244].decode().strip())
    record_duration=float(h[244:252].decode().strip())
    n_signals=int(h[252:256].decode().strip())
    sh=fh.read(header_bytes-256)

pos=0
def fields(width, cast=str):
    global pos
    raw=[sh[pos+i*width:pos+(i+1)*width].decode("latin1").strip() for i in range(n_signals)]
    pos += width*n_signals
    if cast is str: return raw
    return [cast(x) for x in raw]

labels=fields(16)
transducer=fields(80)
units=fields(8)
pmin=fields(8,float); pmax=fields(8,float)
dmin=fields(8,int); dmax=fields(8,int)
prefilter=fields(80)
samples_per_record=fields(8,int)
reserved=fields(32)

if len(set(samples_per_record)) != 1:
    raise RuntimeError("Probe parser currently expects equal per-channel sample counts")
spr=samples_per_record[0]
if abs(record_duration-1.0)>1e-9:
    raise RuntimeError("Probe parser expects 1-second EDF records")
fs=spr/record_duration
total_per_record=sum(samples_per_record)
raw=np.memmap(edf_path,dtype="<i2",mode="r",offset=header_bytes,
              shape=(n_records,total_per_record)).reshape(n_records,n_signals,spr)

targets=["VA1","VA2","VAtarg","ECG","GSR"]
summary={}; signals={}
for lab in targets:
    if lab not in labels: continue
    i=labels.index(lab)
    dig=raw[:,i,:].astype(np.float64).reshape(-1)
    phys=(dig-dmin[i])*(pmax[i]-pmin[i])/(dmax[i]-dmin[i])+pmin[i]
    signals[lab]=phys
    q=np.nanpercentile(phys,[0,1,5,25,50,75,95,99,100])
    summary[lab]={
      "index":i,"sampling_hz":float(fs),"n":int(len(phys)),
      "physical_unit":units[i],"physical_min":pmin[i],"physical_max":pmax[i],
      "quantiles":{str(k):float(v) for k,v in zip([0,1,5,25,50,75,95,99,100],q)},
      "mean":float(np.nanmean(phys)),"std":float(np.nanstd(phys)),
      "n_unique_rounded_4dp":int(len(np.unique(np.round(phys,4))))
    }

window_rows=[]
for ev in events[:12]:
    onset=float(ev["onset"]); dur=float(ev["duration"])
    row={"onset":onset,"duration":dur,"trial_type":ev["trial_type"]}
    for lab,x in signals.items():
        a=max(0,int(round(onset*fs))); b=min(len(x),int(round((onset+dur)*fs)))
        w=x[a:b]
        one=max(1,int(fs))
        row[lab+"_mean"]=float(np.nanmean(w))
        row[lab+"_std"]=float(np.nanstd(w))
        row[lab+"_start_1s"]=float(np.nanmean(w[:one]))
        row[lab+"_end_1s"]=float(np.nanmean(w[-one:]))
    window_rows.append(row)

corr={}
for i,a in enumerate(("VA1","VA2","VAtarg")):
    for b in ("VA1","VA2","VAtarg")[i+1:]:
        if a in signals and b in signals:
            corr[a+"__"+b]=float(np.corrcoef(signals[a],signals[b])[0,1])

out={
 "status":"SCHEMA_ONLY_SINGLE_EDF_PROBE",
 "source_path":path_of(e),
 "source_url":url_of(e),
 "edf_bytes":edf_path.stat().st_size,
 "edf_header":{"startdate_raw":startdate,"starttime_raw":starttime,
               "header_bytes":header_bytes,"n_records":n_records,
               "record_duration":record_duration,"n_signals":n_signals,
               "anonymized_invalid_date_ignored":True},
 "labels":labels,
 "sampling_hz":float(fs),
 "target_channel_summary":summary,
 "first_event_windows":window_rows,
 "report_target_correlations":corr,
 "schema_gate":{
    "va1_varies":summary.get("VA1",{}).get("std",0)>0,
    "va2_varies":summary.get("VA2",{}).get("std",0)>0,
    "target_is_discrete":summary.get("VAtarg",{}).get("n_unique_rounded_4dp",999)<=20,
    "ecg_present":"ECG" in signals,
    "gsr_present":"GSR" in signals
 },
 "interpretation_firewall":"Schema only. VA1/VA2 are synchronized continuous FEELTRACE report axes; no EEG-vs-autonomic predictive comparison is computed. The invalid anonymized EDF date is ignored without modifying signal samples."
}
out["verdict"]="PASS_SIGNAL_LEVEL_ALIGNMENT_GATE" if all(out["schema_gate"].values()) else "FAIL_SIGNAL_LEVEL_ALIGNMENT_GATE"
(OUT/"affect_multimodal_single_edf_schema_probe.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
# Remove large raw file so artifact remains small.
edf_path.unlink()
print(json.dumps(out,indent=2))
