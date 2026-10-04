import json
from pathlib import Path
d=json.loads(Path("protocols/felt_vs_physiology_network_data_audit_v001.json").read_text(encoding="utf-8"))
fields=list(d["required_fields"].keys())
rows=[]
passing=[]
for x in d["datasets"]:
    gates={k:(x.get(k) is True) for k in fields}
    ok=all(gates.values())
    rows.append({"id":x["id"],"gates":gates,"all_required":ok,"note":x["note"]})
    if ok: passing.append(x["id"])
out={
 "verdict":"PASS_COMMON_PUBLIC_DATASET" if passing else "FAIL_NO_COMMON_PUBLIC_DATASET_FOR_FELT_VS_PHYSIOLOGY_NETWORK_CONTRAST",
 "n_datasets_screened":len(rows),
 "n_passing_datasets":len(passing),
 "passing_datasets":passing,
 "rows":rows,
 "near_misses":sorted(
   [{"id":r["id"],"n_passed":sum(r["gates"].values()),"missing":[k for k,v in r["gates"].items() if not v]} for r in rows],
   key=lambda z:(-z["n_passed"],z["id"])
 ),
 "consequence":d["scientific_consequence"]
}
Path("results").mkdir(exist_ok=True)
Path("results/felt_vs_physiology_network_data_audit_v001.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps(out,indent=2))
