from __future__ import annotations
import csv, io, json, os, urllib.request, zipfile, hashlib
from pathlib import Path

ARTICLE=8869160
API=f"https://api.figshare.com/v2/articles/{ARTICLE}"
OUT=Path("results"); OUT.mkdir(exist_ok=True)

with urllib.request.urlopen(API,timeout=120) as r: meta=json.load(r)
files=meta.get("files",[])
if not files: raise RuntimeError("No files")
f=files[0]
url=f["download_url"]; name=f["name"]
zpath=OUT/name
print("DOWNLOAD",name,f.get("size"),url,flush=True)
urllib.request.urlretrieve(url,zpath)
sha=hashlib.sha256(zpath.read_bytes()).hexdigest()
with zipfile.ZipFile(zpath) as z:
    members=[i.filename for i in z.infolist()]
    cand=[m for m in members if ("/interpolated/" in m.lower() or "interpolated" in m.lower()) and m.lower().endswith(".csv")]
    preview={}
    for m in cand[:12]:
        b=z.read(m)
        txt=b.decode("utf-8-sig",errors="replace")
        rd=csv.reader(io.StringIO(txt))
        rows=[]
        for i,row in enumerate(rd):
            rows.append(row)
            if i>=3: break
        preview[m]={"bytes":len(b),"rows_preview":rows}
out={
  "status":"CASE_SNIPPET_SCHEMA_PROBE",
  "article_id":ARTICLE,
  "article_title":meta.get("title"),
  "file":{"name":name,"bytes":f.get("size"),"sha256":sha},
  "n_archive_members":len(members),
  "members":members,
  "interpolated_csv_candidates":cand,
  "preview":preview
}
(OUT/"case_snippet_probe.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps({"status":out["status"],"n_archive_members":len(members),"candidates":cand,"preview":preview},indent=2))
# avoid uploading big zip
zpath.unlink()
