import json
from pathlib import Path

p=Path("protocols/theory_data_identifiability_v001.json")
d=json.loads(p.read_text(encoding="utf-8"))

rows=[]
for ds,mods in d["precommitted_dataset_assessments"].items():
    for model,a in mods.items():
        rows.append({"dataset":ds,"model":model,"status":a["expected"],"reason":a["reason"]})

datasets=sorted(d["precommitted_dataset_assessments"])
cross=[]
for ds in datasets:
    statuses={m:a["expected"] for m,a in d["precommitted_dataset_assessments"][ds].items()}
    both_pass=all(v=="PASS" for v in statuses.values())
    cross.append({"dataset":ds,"model_statuses":statuses,"fair_cross_theory_comparison":both_pass})

mem_unspecified=[x for x in d["models"]["MEM_2026_primary_formalism"]["required_core"] if not x["source_specified_mapping"]]
bayes_unspecified=[x for x in d["models"]["Hierarchical_Bayesian_HDT_2026"]["required_core"] if not x["source_specified_mapping"]]

out={
  "status":"PASS_IDENTIFIABLE_COMMON_DATASET" if any(x["fair_cross_theory_comparison"] for x in cross) else "FAIL_NO_COMMON_IDENTIFIABLE_DATASET",
  "rows":rows,
  "cross_theory":cross,
  "mem_core_items_without_source_specified_mapping":len(mem_unspecified),
  "mem_unspecified_names":[x["name"] for x in mem_unspecified],
  "bayesian_hdt_core_items_without_source_specified_mapping":len(bayes_unspecified),
  "interpretation":(
    "No current dataset in this audit supports a fair direct MEM-vs-hierarchical-Bayesian model comparison. "
    "H001 remains useful for mechanism constraints but would require custom observation models for both theories. "
    "The heartbeat-discrimination dataset supports the published Bayesian model and its parameter-recovery tests, "
    "but MEM lacks a source-specified task likelihood and recoverable parameterization for that task. "
    "Do not interpret this asymmetry as evidence that the Bayesian theory of feeling is true; it is a maturity/identifiability result."
  )
}
Path("results").mkdir(exist_ok=True)
Path("results/theory_data_identifiability_v001.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps(out,indent=2))
