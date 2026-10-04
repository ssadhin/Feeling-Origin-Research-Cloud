from __future__ import annotations
import json, urllib.request
from pathlib import Path

URL="https://data.nemar.org/on002724/v1.0.0/manifest.json"
OUT=Path("results"); OUT.mkdir(exist_ok=True)

with urllib.request.urlopen(URL, timeout=60) as r:
    raw=r.read()
data=json.loads(raw)

# normalize likely manifest shapes
if isinstance(data,list):
    entries=data
elif isinstance(data,dict):
    for key in ("files","entries","manifest","items"):
        if isinstance(data.get(key),list):
            entries=data[key]; break
    else:
        entries=[]
else:
    entries=[]

def pick_path(x):
    for k in ("path","name","key","relative_path","file"):
        if isinstance(x,dict) and x.get(k):
            return str(x[k])
    return ""

def pick_size(x):
    for k in ("size","bytes","size_bytes","length"):
        if isinstance(x,dict) and x.get(k) is not None:
            return x[k]
    return None

rows=[]
for e in entries:
    p=pick_path(e)
    rows.append({
      "path":p,
      "size":pick_size(e),
      "bytes_url":e.get("bytes_url") if isinstance(e,dict) else None,
      "raw":e if len(rows)<5 else None
    })

patterns=("events.tsv","events.json","channels.tsv","eeg.json","participants.tsv","beh","physio","ratings","rating","electrodes.tsv")
matches=[r for r in rows if any(q in r["path"].lower() for q in patterns)]
small=sorted([r for r in rows if isinstance(r.get("size"),(int,float))], key=lambda z:z["size"])[:80]

out={
 "status":"AFFECT_MULTIMODAL_MANIFEST_INVENTORY",
 "dataset":"NEMAR on002724 / OpenNeuro ds002724",
 "manifest_url":URL,
 "manifest_bytes":len(raw),
 "manifest_type":type(data).__name__,
 "n_entries":len(rows),
 "first_entries":rows[:10],
 "metadata_behavior_matches":matches[:300],
 "smallest_files":small,
}
(OUT/"affect_multimodal_manifest_inventory.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps(out,indent=2))
