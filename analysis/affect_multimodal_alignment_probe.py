from __future__ import annotations
import csv, io, json, urllib.request
from pathlib import Path

BASE="https://data.nemar.org/on002724/v1.0.0/"
MAN=BASE+"manifest.json"
OUT=Path("results"); OUT.mkdir(exist_ok=True)

def get(url):
    with urllib.request.urlopen(url,timeout=60) as r:
        return r.read()

manifest=json.loads(get(MAN))
entries=manifest if isinstance(manifest,list) else manifest.get("files",manifest.get("entries",[]))

def path_of(e):
    for k in ("path","name","key","relative_path","file"):
        if e.get(k): return str(e[k])
    return ""

def url_of(e):
    return e.get("bytes_url") or (BASE+path_of(e))

events=[e for e in entries if path_of(e).endswith("_events.tsv")]
channels=[e for e in entries if path_of(e).endswith("_channels.tsv")]
eegjson=[e for e in entries if path_of(e).endswith("_eeg.json")]
signals=[e for e in entries if any(path_of(e).lower().endswith(x) for x in (".set",".fdt",".edf",".bdf",".vhdr",".eeg",".vmrk"))]

def parse_tsv(b):
    txt=b.decode("utf-8-sig",errors="replace")
    rows=list(csv.DictReader(io.StringIO(txt),delimiter="\t"))
    return txt,rows

event_schemas={}
event_examples=[]
rating_cols=set()
trial_types=set()
for e in events:
    txt,rows=parse_tsv(get(url_of(e)))
    hdr=tuple(rows[0].keys()) if rows else tuple(txt.splitlines()[0].split("\t")) if txt.strip() else tuple()
    event_schemas[str(hdr)]=event_schemas.get(str(hdr),0)+1
    for h in hdr:
        hl=h.lower()
        if any(t in hl for t in ("valence","arousal","rating","pleasant","emotion","affect")):
            rating_cols.add(h)
    for r in rows:
        for key in ("trial_type","event_type","condition","value"):
            if key in r and r[key]:
                trial_types.add(r[key])
    if len(event_examples)<3:
        event_examples.append({"path":path_of(e),"url":url_of(e),"text":txt})

channel_schemas={}
channel_examples=[]
types=set(); names=set()
for e in channels[:12]:
    txt,rows=parse_tsv(get(url_of(e)))
    hdr=tuple(rows[0].keys()) if rows else tuple()
    channel_schemas[str(hdr)]=channel_schemas.get(str(hdr),0)+1
    for r in rows:
        if r.get("type"): types.add(r["type"])
        if r.get("name"): names.add(r["name"])
    if len(channel_examples)<2:
        channel_examples.append({"path":path_of(e),"url":url_of(e),"text":txt})

json_examples=[]
for e in eegjson[:2]:
    raw=get(url_of(e)).decode("utf-8-sig",errors="replace")
    json_examples.append({"path":path_of(e),"url":url_of(e),"text":raw})

out={
 "status":"AFFECT_MULTIMODAL_ALIGNMENT_PROBE",
 "dataset":"on002724/ds002724",
 "n_event_files":len(events),
 "n_channel_files":len(channels),
 "n_eeg_json_files":len(eegjson),
 "n_signal_files":len(signals),
 "signal_examples":[{"path":path_of(e),"size":e.get("size",e.get("bytes")),"url":url_of(e)} for e in signals[:10]],
 "event_schemas":event_schemas,
 "rating_like_event_columns":sorted(rating_cols),
 "trial_type_examples":sorted(trial_types)[:100],
 "event_examples":event_examples,
 "channel_schemas":channel_schemas,
 "channel_types":sorted(types),
 "channel_names":sorted(names),
 "channel_examples":channel_examples,
 "eeg_json_examples":json_examples,
 "alignment_gate":{
   "ratings_in_events":bool(rating_cols),
   "ecg_channel_present":any("ECG" in x.upper() or "EKG" in x.upper() for x in types|names),
   "gsr_channel_present":any("GSR" in x.upper() or "EDA" in x.upper() or "GALV" in x.upper() for x in types|names),
   "synchronized_signal_file_present":bool(signals)
 }
}
g=out["alignment_gate"]
out["verdict"]="PASS_MULTIMODAL_ALIGNMENT_GATE" if all(g.values()) else "FAIL_MULTIMODAL_ALIGNMENT_GATE"
out["firewall"]="This is a schema/alignment gate only. It does not test predictive independence, causality, necessity, or phenomenality."
(OUT/"affect_multimodal_alignment_probe.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps(out,indent=2))
