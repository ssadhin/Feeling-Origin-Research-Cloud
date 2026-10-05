from __future__ import annotations
import json,re
from pathlib import Path
import requests
from remotezip import RemoteZip

URL="https://data.psychosensing.psnc.pl/popane/files/study5.zip"
OUT=Path("results"); OUT.mkdir(exist_ok=True)
MAX_SCAN=64

def parse_name(path):
    stem=Path(path).stem
    m=re.match(r"^(\d+)_(.+)$",stem)
    return (m.group(1),m.group(2)) if m else (None,None)

def find_header(rz,name):
    meta=[]
    with rz.open(name) as f:
        for i in range(MAX_SCAN):
            raw=f.readline(262144)
            if not raw: break
            line=(raw.decode("utf-8-sig",errors="replace") if isinstance(raw,bytes) else str(raw)).strip()
            if not line: continue
            if line.startswith("#"):
                meta.append(line); continue
            return {"header":line,"metadata_keys":[m.split(",",1)[0].lstrip("#").strip() for m in meta],"lines_scanned":i+1}
    return {"error":"No true header within scan limit","metadata_keys":[m.split(",",1)[0].lstrip("#").strip() for m in meta]}

def main():
    probe=requests.get(URL,headers={"Range":"bytes=0-127"},stream=True,timeout=60)
    range_ok=probe.status_code==206 or "bytes" in probe.headers.get("Accept-Ranges","").lower()
    cr=probe.headers.get("Content-Range"); probe.close()
    out={"status":"POPANE_P2A_STUDY5_SCHEMA_PREFLIGHT","archive_url":URL,
         "range_supported":range_ok,"content_range_probe":cr,"samples":[],
         "firewall":"Outcome-blind schema preflight; no observational data rows read."}
    if not range_ok:
        out["verdict"]="FAIL_STUDY5_SCHEMA_OR_ACCESS"
        (OUT/"popane_p2a_study5_schema_preflight.json").write_text(json.dumps(out,indent=2))
        print(json.dumps(out,indent=2)); return
    with RemoteZip(URL) as rz:
        infos=rz.infolist()
        csvs=sorted(i.filename for i in infos if i.filename.lower().endswith(".csv"))
        parsed=[(n,)+parse_name(n) for n in csvs]
        participants=sorted({p for _,p,_ in parsed if p},key=int)
        segments=sorted({s for _,_,s in parsed if s and s.lower() not in ("all","baseline")})
        nonbase=[n for n,p,s in parsed if s and s.lower() not in ("all","baseline")]
        base=[n for n,p,s in parsed if s and s.lower()=="baseline"]
        chosen=nonbase[:18]+base[:3]
        for n in chosen:
            pid,seg=parse_name(n); h=find_header(rz,n)
            item={"path":n,"participant_id":pid,"segment_label":seg,**h}
            if "header" in item:
                item["columns"]=[x.strip().strip('"') for x in item["header"].split(",")]
            out["samples"].append(item)
        out["archive"]={"entries_total":len(infos),"csv_entries":len(csvs),
                        "n_participants":len(participants),"n_named_nonbaseline_segments":len(segments),
                        "segment_label_sample":segments[:80]}
    good=[x for x in out["samples"] if "columns" in x]
    union=set()
    for x in good: union.update(c.lower() for c in x["columns"])
    def has(keys): return any(any(k in c for k in keys) for c in union)
    qc={"n_headers_found":len(good),"column_union":sorted(union),
        "has_time_or_sample":has(["time","timestamp","sample","index"]),
        "has_affect_or_valence":has(["affect","valence"]),
        "has_ecg":has(["ecg","ekg"]),
        "has_eda":has(["eda","gsr","skin_conduct"])}
    out["qc"]=qc
    if range_ok and out["archive"]["n_participants"]>=20 and out["archive"]["n_named_nonbaseline_segments"]>=2 and qc["has_time_or_sample"] and qc["has_affect_or_valence"] and qc["has_ecg"] and qc["has_eda"]:
        out["verdict"]="PASS_STUDY5_VALIDATION_FEASIBLE"
    else:
        out["verdict"]="FAIL_STUDY5_SCHEMA_OR_ACCESS"
    (OUT/"popane_p2a_study5_schema_preflight.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
