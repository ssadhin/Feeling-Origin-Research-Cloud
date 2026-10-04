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

# matching events
stem=path_of(e).replace("_eeg.edf","")
ev_path=stem+"_events.tsv"
ev_e=next(x for x in entries if path_of(x)==ev_path)
with urllib.request.urlopen(url_of(ev_e),timeout=60) as r:
    event_text=r.read().decode("utf-8-sig")
events=list(csv.DictReader(io.StringIO(event_text),delimiter="\t"))

import pyedflib
f=pyedflib.EdfReader(str(edf_path))
labels=f.getSignalLabels()
fs=[f.getSampleFrequency(i) for i in range(f.signals_in_file)]
targets=["VA1","VA2","VAtarg","ECG","GSR"]
summary={}
signals={}
for lab in targets:
    if lab not in labels: continue
    i=labels.index(lab)
    x=f.readSignal(i)
    signals[lab]=x
    q=np.nanpercentile(x,[0,1,5,25,50,75,95,99,100])
    summary[lab]={
      "index":i,"sampling_hz":float(fs[i]),"n":int(len(x)),
      "physical_min":float(f.getPhysicalMinimum(i)),
      "physical_max":float(f.getPhysicalMaximum(i)),
      "quantiles":{str(k):float(v) for k,v in zip([0,1,5,25,50,75,95,99,100],q)},
      "mean":float(np.nanmean(x)),"std":float(np.nanstd(x)),
      "n_unique_rounded_4dp":int(len(np.unique(np.round(x,4))))
    }

# window summaries for first 12 events; use native 1 kHz signal timing
window_rows=[]
for ev in events[:12]:
    onset=float(ev["onset"]); dur=float(ev["duration"])
    row={"onset":onset,"duration":dur,"trial_type":ev["trial_type"]}
    for lab,x in signals.items():
        sf=summary[lab]["sampling_hz"]
        a=max(0,int(round(onset*sf))); b=min(len(x),int(round((onset+dur)*sf)))
        w=x[a:b]
        row[lab+"_mean"]=float(np.nanmean(w))
        row[lab+"_std"]=float(np.nanstd(w))
        row[lab+"_start"]=float(np.nanmean(w[:max(1,int(sf))]))
        row[lab+"_end"]=float(np.nanmean(w[-max(1,int(sf)):]))
    window_rows.append(row)

corr={}
for a in ("VA1","VA2","VAtarg"):
    for b in ("VA1","VA2","VAtarg"):
        if a<b and a in signals and b in signals:
            n=min(len(signals[a]),len(signals[b]))
            corr[a+"__"+b]=float(np.corrcoef(signals[a][:n],signals[b][:n])[0,1])

out={
 "status":"SCHEMA_ONLY_SINGLE_EDF_PROBE",
 "source_path":path_of(e),
 "source_url":url_of(e),
 "edf_bytes":edf_path.stat().st_size,
 "labels":labels,
 "sample_frequencies":{lab:float(fs[i]) for i,lab in enumerate(labels)},
 "target_channel_summary":summary,
 "first_event_windows":window_rows,
 "report_target_correlations":corr,
 "interpretation_firewall":"Schema only. These summaries are not used to judge EEG vs autonomic prediction or causal origin. VA1/VA2 are treated as the two continuous FEELTRACE user-report axes until exact channel-to-axis ordering is source-verified."
}
(OUT/"affect_multimodal_single_edf_schema_probe.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps(out,indent=2))
