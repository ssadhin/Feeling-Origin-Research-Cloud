from __future__ import annotations
import csv, io, json, os, re, tempfile, urllib.request
from pathlib import Path

OUT=Path("results"); OUT.mkdir(exist_ok=True)
MANIFEST_URL="https://data.nemar.org/on003751/v1.0.0/manifest.json"
SUB="sub-mit003"

def fetch_json(url):
    with urllib.request.urlopen(url, timeout=120) as r:
        return json.load(r)

def entry_path(e):
    for k in ("path","name","key","relative_path","file"):
        if k in e and isinstance(e[k],str):
            return e[k].lstrip("./")
    return ""

def bytes_url(e):
    for k in ("bytes_url","url","download_url"):
        if k in e and isinstance(e[k],str) and e[k].startswith("http"):
            return e[k]
    return None

m=fetch_json(MANIFEST_URL)
entries=m if isinstance(m,list) else m.get("files",m.get("entries",[]))
if not isinstance(entries,list):
    raise RuntimeError(f"Unknown manifest schema: {type(m)} keys={list(m)[:20] if isinstance(m,dict) else ''}")

sub_entries=[e for e in entries if SUB in entry_path(e)]
summary=[{
    "path":entry_path(e),
    "size":e.get("size",e.get("bytes",e.get("size_bytes"))),
    "has_bytes_url":bool(bytes_url(e))
} for e in sub_entries]

need=[]
for e in sub_entries:
    p=entry_path(e)
    if p.endswith(("_task-Emotion_eeg.set","_task-Emotion_eeg.fdt","_task-emotion_events.tsv","_task-Emotion_beh.tsv")):
        need.append(e)

tmp=Path(tempfile.mkdtemp(prefix="denspilot_"))
downloaded={}
for e in need:
    p=entry_path(e)
    u=bytes_url(e)
    if not u:
        continue
    dest=tmp/Path(p).name
    urllib.request.urlretrieve(u,dest)
    downloaded[p]={"local":str(dest),"bytes":dest.stat().st_size}

# Behavior/events can also be fetched from GitHub if absent from manifest direct bytes
base="https://raw.githubusercontent.com/nemarDatasets/on003751/main/"
fallbacks=[
    f"{SUB}/beh/{SUB}_task-Emotion_beh.tsv",
    f"{SUB}/eeg/{SUB}_task-emotion_events.tsv",
]
for p in fallbacks:
    if p not in downloaded:
        dest=tmp/Path(p).name
        urllib.request.urlretrieve(base+p,dest)
        downloaded[p]={"local":str(dest),"bytes":dest.stat().st_size,"fallback":"github"}

set_path=next((v["local"] for k,v in downloaded.items() if k.endswith(".set")),None)
if not set_path:
    raise RuntimeError("No .set downloaded from manifest")

try:
    import mne
    raw=mne.io.read_raw_eeglab(set_path, preload=False, verbose="ERROR")
    ch_names=raw.ch_names
    ch_types=raw.get_channel_types()
    channel_summary={
        "n_channels":len(ch_names),
        "sfreq":float(raw.info["sfreq"]),
        "duration_sec":float(raw.n_times/raw.info["sfreq"]),
        "channels":[{"name":n,"type":t} for n,t in zip(ch_names,ch_types)],
    }
except Exception as e:
    channel_summary={"load_error":repr(e)}

beh_path=next(v["local"] for k,v in downloaded.items() if k.endswith("_beh.tsv"))
evt_path=next(v["local"] for k,v in downloaded.items() if k.endswith("_events.tsv"))
with open(beh_path,encoding="utf-8-sig") as f:
    beh=list(csv.DictReader(f,delimiter="\t"))
with open(evt_path,encoding="utf-8-sig") as f:
    ev=list(csv.DictReader(f,delimiter="\t"))
stm=[x for x in ev if x.get("trial_type")=="stm"]
val=[x for x in ev if x.get("trial_type")=="vlnc"]
# Onsets are represented in milliseconds in these converted files; verify against recording duration.
onsets=[float(x["onset"]) for x in stm]
raw_dur=channel_summary.get("duration_sec")
scale_guess=1000.0 if raw_dur and max(onsets)/1000.0 < raw_dur*1.2 else 1.0
stim_intervals=[]
for s in stm:
    so=float(s["onset"])/scale_guess
    later=[float(v["onset"])/scale_guess for v in val if float(v["onset"])>float(s["onset"])]
    vo=min(later) if later else None
    stim_intervals.append({"label":s.get("label"),"onset_sec":so,"to_valence_sec":None if vo is None else vo-so})

result={
    "status":"DENS_PILOT_SCHEMA_INVENTORY",
    "manifest_url":MANIFEST_URL,
    "manifest_entry_count":len(entries),
    "subject_manifest_entries":summary,
    "downloaded":{k:{"bytes":v["bytes"],**({"fallback":v["fallback"]} if "fallback" in v else {})} for k,v in downloaded.items()},
    "channel_summary":channel_summary,
    "behavior":{
        "n_rows":len(beh),
        "columns":list(beh[0].keys()) if beh else [],
        "rows_preview":beh[:3],
    },
    "events":{
        "n_events":len(ev),
        "n_stimulus_events":len(stm),
        "onset_scale_divisor":scale_guess,
        "stimulus_intervals":stim_intervals,
    },
    "gate":{
        "raw_loadable": "load_error" not in channel_summary,
        "has_128_eeg_expected": sum(1 for x in channel_summary.get("channels",[]) if x["type"]=="eeg") >= 128,
        "has_ecg_named_or_typed": any(x["type"]=="ecg" or "ecg" in x["name"].lower() for x in channel_summary.get("channels",[])),
        "behavior_trials_match_stimuli": len(beh)==len(stm),
    },
    "firewall":"Schema/pilot only. No affect prediction is fit and no analytic feature choices are selected from outcome performance."
}
(OUT/"dens_pilot_inventory.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result,indent=2))
