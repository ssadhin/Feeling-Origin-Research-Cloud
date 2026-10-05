from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse
import requests
from remotezip import RemoteZip

URL="https://data.psychosensing.psnc.pl/popane/files/study6.zip"
OUT=Path("results"); OUT.mkdir(exist_ok=True)
MAX_HEADERS=12
MAX_BASELINES=3

def safe_header(rz,name):
    with rz.open(name) as f:
        raw=f.readline(65536)
    if isinstance(raw,bytes):
        return raw.decode("utf-8-sig",errors="replace").strip()
    return str(raw).strip()

def classify(n):
    x=n.lower()
    if "baseline" in x:
        return "baseline"
    if any(k in x for k in ("manipulation","film","video","emotion","clip","round","trial")):
        return "manipulation_like"
    return "other"

def main():
    head=requests.head(URL,allow_redirects=True,timeout=60)
    # Some servers omit Accept-Ranges on HEAD; probe a tiny range explicitly.
    probe=requests.get(URL,headers={"Range":"bytes=0-127"},stream=True,timeout=60)
    range_supported=(probe.status_code==206) or ("bytes" in (probe.headers.get("Accept-Ranges","").lower()))
    content_range=probe.headers.get("Content-Range")
    probe.close()

    out={
      "status":"POPANE_P0_STUDY6_SCHEMA_PREFLIGHT",
      "archive_url":URL,
      "http":{
        "head_status":head.status_code,
        "content_length":head.headers.get("Content-Length"),
        "accept_ranges_head":head.headers.get("Accept-Ranges"),
        "range_probe_status":probe.status_code,
        "content_range":content_range,
        "range_supported":range_supported
      },
      "zip":{},
      "header_samples":[],
      "qc":{},
      "firewall":"Outcome-blind schema/access preflight only; no valence/physiology values inspected."
    }

    if not range_supported:
        out["verdict"]="FAIL_SCHEMA_OR_ACCESS"
        out["qc"]["range_access"]=False
        (OUT/"popane_p0_study6_schema_preflight.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
        print(json.dumps(out,indent=2)); return

    with RemoteZip(URL) as rz:
        infos=rz.infolist()
        names=sorted(i.filename for i in infos)
        csvs=[n for n in names if n.lower().endswith(".csv")]
        out["zip"]={
          "entries_total":len(names),
          "csv_entries":len(csvs),
          "top_level_prefixes":sorted({n.split("/")[0] for n in names if n})[:50],
          "sample_names_first_40":names[:40]
        }
        baseline=[n for n in csvs if classify(n)=="baseline"]
        manipulation=[n for n in csvs if classify(n)=="manipulation_like"]
        other=[n for n in csvs if classify(n)=="other"]
        chosen=(manipulation[:MAX_HEADERS] if manipulation else other[:MAX_HEADERS])
        chosen+=baseline[:MAX_BASELINES]
        for n in chosen:
            try:
                h=safe_header(rz,n)
                cols=[c.strip().strip('"') for c in h.replace(";",",").split(",")]
                out["header_samples"].append({
                  "path":n,
                  "class":classify(n),
                  "header":h,
                  "columns":cols
                })
            except Exception as e:
                out["header_samples"].append({"path":n,"class":classify(n),"error":repr(e)})

    headers=[x for x in out["header_samples"] if "columns" in x]
    canon=set()
    for x in headers:
        canon.update(c.lower() for c in x["columns"])
    has_time=any(any(k in c for k in ("time","sample","index")) for c in canon)
    has_valence=any("valence" in c for c in canon)
    has_ecg=any("ecg" in c or "ekg" in c for c in canon)
    has_eda=any("eda" in c or "gsr" in c or "skin conduct" in c for c in canon)
    has_marker=any(any(k in c for k in ("marker","event","stim","condition","phase")) for c in canon)

    # Participant/stimulus naming evidence derived from filenames only.
    participant_tokens=set()
    for n in [x["path"] for x in headers]:
        stem=Path(n).stem
        participant_tokens.add(stem.split("_")[0])
    out["qc"]={
      "range_access":True,
      "headers_read":len(headers),
      "has_time_or_sample_column":has_time,
      "has_valence_column":has_valence,
      "has_ecg_column":has_ecg,
      "has_eda_column":has_eda,
      "has_marker_or_event_column":has_marker,
      "participant_filename_tokens_sample":sorted(participant_tokens)[:30],
      "n_distinct_participant_tokens_in_header_sample":len(participant_tokens),
      "manipulation_like_csv_count":len(manipulation),
      "baseline_csv_count":len(baseline),
      "other_csv_count":len(other)
    }
    synced=has_valence and (has_ecg or has_eda)
    if synced and has_time and (has_marker or len(manipulation)>0):
        verdict="PASS_REMOTE_REPLICATION_FEASIBLE"
    elif synced and has_time:
        verdict="PASS_PERSON_ONLY_GENERALIZATION"
    else:
        verdict="FAIL_SCHEMA_OR_ACCESS"
    out["verdict"]=verdict
    (OUT/"popane_p0_study6_schema_preflight.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
