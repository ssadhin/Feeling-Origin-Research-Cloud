#!/usr/bin/env python3
"""CoSpine sidecar QC, metadata only. No affect/phenomenality inference."""
import json, statistics, urllib.request
from urllib.error import HTTPError
PIN="037ed267e7f7f2024a5fe3d0e8fb4759f7f67bdd"
ROOT=f"https://raw.githubusercontent.com/OpenNeuroDatasets/ds005883/{PIN}"
def load(s, suffix):
    path=f"sub-{s}/func/sub-{s}_task-pain_{suffix}.json"
    try:
        with urllib.request.urlopen(f"{ROOT}/{path}",timeout=25) as f:
            return json.load(f), None
    except HTTPError as e:
        return None, f"HTTP {e.code}"
def seconds(clock):
    a=[float(x) for x in clock.split(":")]
    return 3600*a[0]+60*a[1]+a[2]
rows=[]
for i in range(1,40):
    s=f"{i:02d}"
    b,be=load(s,"bold")
    p,pe=load(s,"recording-pulse_physio")
    r,re=load(s,"recording-respiratory_physio")
    bt=seconds(b["AcquisitionTime"]) if b and b.get("AcquisitionTime") else None
    row={"subject":s,"errors":{"bold":be,"pulse":pe,"resp":re},
         "TR":b.get("RepetitionTime") if b else None,
         "TE":b.get("EchoTime") if b else None,
         "n_slice":len(b.get("SliceTiming",[])) if b else None,
         "AcquisitionTime":b.get("AcquisitionTime") if b else None}
    for label,x in [("pulse",p),("resp",r)]:
        row[label]=None if x is None else {
          "start_raw":x.get("StartTime"),"duration_raw":x.get("Duration"),
          "sampling_hz":x.get("SamplingFrequency"),"columns":x.get("Columns"),
          "candidate_offset_s":x["StartTime"]/1000-bt if bt is not None and isinstance(x.get("StartTime"),(int,float)) else None}
    rows.append(row)
bad_offset=[z["subject"] for z in rows if z["pulse"] and not (-300<z["pulse"]["candidate_offset_s"]<0)]
bad_duration=[z["subject"] for z in rows if z["pulse"] and not (600<=z["pulse"]["duration_raw"]/1000<=900)]
summary={"source_commit":PIN,"n_bold":sum(z["TR"] is not None for z in rows),
 "n_pulse":sum(z["pulse"] is not None for z in rows),
 "n_resp":sum(z["resp"] is not None for z in rows),
 "bad_pulse_offset_subjects":bad_offset,"bad_pulse_duration_subjects":bad_duration,
 "warning":"Offsets assume PMU clock milliseconds and BOLD AcquisitionTime as time zero; neither is validated by triggers. No neural/physiology fitting."}
print(json.dumps({"summary":summary,"rows":rows},indent=2))
