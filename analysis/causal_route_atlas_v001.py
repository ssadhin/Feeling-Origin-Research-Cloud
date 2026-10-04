import json
from pathlib import Path

p=Path("protocols/causal_route_atlas_v001.json")
d=json.loads(p.read_text(encoding="utf-8"))
ev=d["evidence"]

def has(cls):
    return [e for e in ev if cls in e["causal_class"]]

direct_mult=[e for e in has("route_multiplicity") if e["direct_subjective_report"]]
sub=[e for e in ev if "route_substitution" in e["causal_class"] or "alternative_interoceptive_route" in e["causal_class"]]
diss=[e for e in has("physiology_feeling_dissociation") if e["direct_subjective_report"]]

assess=d["precommitted_candidate_assessments"]
global_refuted=[k for k,v in assess.items() if v.get("global_necessity")=="REFUTED"]
global_unknown=[k for k,v in assess.items() if v.get("global_necessity")=="UNKNOWN"]

route_mult=bool(direct_mult)
substitution=bool(sub)
phys_diss=bool(diss)
single_source_survives=(len(global_refuted)==0 and not route_mult and not substitution)

out={
  "status":"EVIDENCE_FAVORS_ROUTE_MULTIPLICITY" if (route_mult and substitution and not single_source_survives) else "INCONCLUSIVE",
  "n_evidence_rows":len(ev),
  "global_necessity_refuted_candidates":global_refuted,
  "global_necessity_unknown_candidates":global_unknown,
  "route_multiplicity_gate":route_mult,
  "route_substitution_gate":substitution,
  "physiology_feeling_dissociation_gate":phys_diss,
  "single_anatomical_source_survives_v001":single_source_survives,
  "candidate_assessments":assess,
  "critical_caveat":"This atlas does not prove independent redundant generators. Multiple perturbation sites may converge on a shared downstream network not isolated by current human data. The result is about route multiplicity and failure of simple exclusive-node models at current resolution.",
  "next_test":"Search for human double-dissociations or selective perturbations that can identify a shared minimum cut across preserved/evoked feelings without using report loss as evidence of absent phenomenality."
}
Path("results").mkdir(exist_ok=True)
Path("results/causal_route_atlas_v001.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps(out,indent=2))
