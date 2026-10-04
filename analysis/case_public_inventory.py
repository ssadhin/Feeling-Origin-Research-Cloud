from __future__ import annotations
import json, urllib.request
from pathlib import Path

ARTICLE_ID=8869157
URL=f"https://api.figshare.com/v2/articles/{ARTICLE_ID}"
with urllib.request.urlopen(URL,timeout=120) as r:
    d=json.load(r)
files=[]
for f in d.get("files",[]):
    files.append({
      "id":f.get("id"),
      "name":f.get("name"),
      "size":f.get("size"),
      "download_url":f.get("download_url"),
      "supplied_md5":f.get("supplied_md5") or f.get("computed_md5")
    })
out={
  "status":"CASE_PUBLIC_INVENTORY",
  "article_id":ARTICLE_ID,
  "title":d.get("title"),
  "doi":d.get("doi"),
  "description":d.get("description"),
  "files":files,
  "total_bytes":sum((f["size"] or 0) for f in files),
  "candidate_snippet":[f for f in files if "snippet" in (f["name"] or "").lower()],
  "candidate_full":[f for f in files if "full" in (f["name"] or "").lower()],
}
Path("results").mkdir(exist_ok=True)
Path("results/case_public_inventory.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps(out,indent=2))
