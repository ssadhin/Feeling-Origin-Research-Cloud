from __future__ import annotations
import json,re
from pathlib import Path
import requests
from remotezip import RemoteZip

URL="https://data.psychosensing.psnc.pl/popane/files/study6.zip"
OUT=Path("results"); OUT.mkdir(exist_ok=True)
MAX_SCAN=64

def find_header(rz,name):
    meta=[]
    with rz.open(name) as f:
        for i in range(MAX_SCAN):
            raw=f.readline(262144)
            if not raw:
                break
            if isinstance(raw,bytes):
                line=raw.decode("utf-8-sig",errors="replace").strip()
            else:
                line=str(raw).strip()
            if not line:
                continue
            if line.startswith("#"):
                meta.append(line)
                continue
            return {"header":line,"metadata_lines":meta,"lines_scanned":i+1}
    return {"error":"No non-comment header found within scan limit","metadata_lines":meta}

def split_cols(line):
    # POPANE is documented CSV. Preserve exact header and use comma split for schema detection.
    return [x.strip().strip('"') for x in line.split(",")]

def stem_info(name):
    stem=Path(name).stem
    m=re.match(r"^(\d+)_([^/]+)$",stem)
    if not m:
        return None,None
    return m.group(1),m.group(2)

def main():
    r=requests.get(URL,headers={"Range":"bytes=0-127"},stream=True,timeout=60)
    range_ok=r.status_code==206 or "bytes" in r.headers.get("Accept-Ranges","").lower()
    r.close()
    out={"status":"POPANE_P0B_STUDY6_TRUE_HEADER_PREFLIGHT",
         "protocol":"protocols/popane_p0b_study6_true_header_preflight.json",
         "range_supported":range_ok,"samples":[],"qc":{},
         "firewall":"Outcome-blind true-header discovery; no data rows read."}
    if not range_ok:
        out["verdict"]="FAIL_SCHEMA"
        (OUT/"popane_p0b_study6_true_header_preflight.json").write_text(json.dumps(out,indent=2))
        print(json.dumps(out,indent=2)); return

    with RemoteZip(URL) as rz:
        names=sorted(i.filename for i in rz.infolist() if i.filename.lower().endswith(".csv"))
        parsed=[(n,)+stem_info(n) for n in names]
        participant_ids=sorted({pid for _,pid,_ in parsed if pid},key=int)
        segment_labels=sorted({seg for _,_,seg in parsed if seg and seg.lower() not in ("all","baseline")})
        nonbase=[n for n,pid,seg in parsed if seg and seg.lower() not in ("all","baseline")]
        base=[n for n,pid,seg in parsed if seg and seg.lower()=="baseline"]
        chosen=nonbase[:18]+base[:3]
        for n in chosen:
            h=find_header(rz,n)
            item={"path":n}
            pid,seg=stem_info(n); item["participant_id"]=pid; item["segment_label"]=seg
            item.update(h)
            if "header" in item:
                item["columns"]=split_cols(item["header"])
                # Preserve metadata key names but not any observational values.
                item["metadata_keys"]=[m.split(",",1)[0].lstrip("#").strip() for m in item["metadata_lines"]]
            out["samples"].append(item)

    good=[x for x in out["samples"] if "columns" in x]
    colsets=[{c.lower() for c in x["columns"]} for x in good]
    union=set().union(*colsets) if colsets else set()
    def has_any(keys):
        return any(any(k in c for k in keys) for c in union)
    has_time=has_any(["time","timestamp","sample","index"])
    has_valence=has_any(["valence","affect"])
    has_ecg=has_any(["ecg","ekg"])
    has_eda=has_any(["eda","gsr","skin_conduct"])
    # ICG / hemodynamic is also a peripheral modality, but require >=2 total peripheral families.
    has_icg=has_any(["icg","dz","z0","impedance"])
    has_bp=has_any(["sbp","dbp","blood"])
    peripheral_count=sum([has_ecg,has_eda,has_icg,has_bp])
    out["qc"]={
      "n_archive_participants":len(participant_ids),
      "participant_id_min":participant_ids[0] if participant_ids else None,
      "participant_id_max":participant_ids[-1] if participant_ids else None,
      "n_named_nonbaseline_segments":len(segment_labels),
      "segment_label_sample":segment_labels[:60],
      "n_headers_found":len(good),
      "column_union":sorted(union),
      "has_time_or_sample":has_time,
      "has_valence":has_valence,
      "has_ecg":has_ecg,
      "has_eda":has_eda,
      "has_icg":has_icg,
      "has_bp":has_bp,
      "peripheral_family_count":peripheral_count
    }
    if good and has_time and has_valence and peripheral_count>=2 and len(participant_ids)>=20 and len(segment_labels)>=2:
        out["verdict"]="PASS_REMOTE_REPLICATION_FEASIBLE"
    elif good and has_time and has_valence and peripheral_count>=1 and len(participant_ids)>=20:
        out["verdict"]="PASS_PERSON_ONLY_GENERALIZATION"
    else:
        out["verdict"]="FAIL_SCHEMA"
    (OUT/"popane_p0b_study6_true_header_preflight.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
