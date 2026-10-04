from __future__ import annotations
import csv, hashlib, io, json, urllib.request, zipfile
from pathlib import Path

BASE="https://zenodo.org/records/21536139/files/"
FILES={
  "EBS_elecloc_QCcleaned.csv":"EBS_elecloc_QCcleaned.csv?download=1",
  "Part3-CCEP.zip":"Part3-CCEP.zip?download=1",
}
OUT=Path("results")
OUT.mkdir(exist_ok=True)

def dl(name, suffix):
    path=OUT/name
    url=BASE+suffix
    print("DOWNLOAD",url)
    urllib.request.urlretrieve(url,path)
    h=hashlib.sha256(path.read_bytes()).hexdigest()
    return path,h

def csv_info_bytes(name,b):
    text=b.decode("utf-8-sig",errors="replace")
    rdr=csv.reader(io.StringIO(text))
    rows=[]
    for i,row in enumerate(rdr):
        rows.append(row)
        if i>=4: break
    header=rows[0] if rows else []
    nlines=text.count("\n")
    return {"name":name,"bytes":len(b),"approx_lines":nlines,"header":header,"preview":rows[1:4]}

meta_path,meta_sha=dl("EBS_elecloc_QCcleaned.csv",FILES["EBS_elecloc_QCcleaned.csv"])
zip_path,zip_sha=dl("Part3-CCEP.zip",FILES["Part3-CCEP.zip"])

meta_bytes=meta_path.read_bytes()
inventory={
  "status":"PUBLIC_BRIDGE_INVENTORY",
  "source":{
    "zenodo_record":"10.5281/zenodo.21536139",
    "record_url":"https://zenodo.org/records/21536139",
    "paper_related_doi":"10.1038/s41593-025-02009-x"
  },
  "downloads":{
    "EBS_elecloc_QCcleaned.csv":{"sha256":meta_sha,"bytes":len(meta_bytes)},
    "Part3-CCEP.zip":{"sha256":zip_sha,"bytes":zip_path.stat().st_size},
  },
  "meta_csv":csv_info_bytes("EBS_elecloc_QCcleaned.csv",meta_bytes),
  "archive_members":[],
  "csv_tables":[],
}

with zipfile.ZipFile(zip_path) as z:
    for info in z.infolist():
        inventory["archive_members"].append({"name":info.filename,"bytes":info.file_size})
        if info.filename.lower().endswith((".csv",".tsv",".txt")) and info.file_size<25_000_000:
            try:
                inventory["csv_tables"].append(csv_info_bytes(info.filename,z.read(info.filename)))
            except Exception as e:
                inventory["csv_tables"].append({"name":info.filename,"error":repr(e)})

# conservative eligibility: public table must expose some stimulation-site identity/label and
# some connectivity-like numerical features or edge summaries.
connectivity_tokens=("ccep","connect","incoming","outgoing","latency","amplitude","zscore","z_score","response")
site_tokens=("subject","bipolar","seed","stim","electrode","channel","hot_cold","category")
eligible=[]
for t in inventory["csv_tables"]:
    h=[str(x).lower() for x in t.get("header",[])]
    has_site=any(any(tok in col for tok in site_tokens) for col in h)
    has_conn=any(any(tok in col for tok in connectivity_tokens) for col in h)
    if has_site and has_conn:
        eligible.append(t["name"])
inventory["candidate_connectivity_tables"]=eligible
inventory["bridge_gate"]="PUBLIC_SITE_LEVEL_CONNECTIVITY_TABLE_FOUND" if eligible else "NO_OBVIOUS_SITE_LEVEL_CONNECTIVITY_TABLE_FROM_SCHEMA_SCAN"
inventory["firewall"]="Inventory only. No inferential model is fit here; absence from schema scan may reflect data encoded in MAT/NPY/Pickle or scripts rather than tabular files."

(OUT/"lyu_public_bridge_inventory.json").write_text(json.dumps(inventory,indent=2),encoding="utf-8")
print(json.dumps(inventory,indent=2))
