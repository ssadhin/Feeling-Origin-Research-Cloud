import json
from pathlib import Path
d=json.loads(Path("protocols/shared_minimum_cut_screen_v001.json").read_text(encoding="utf-8"))
rows=[]
survivors=[]
for c in d["candidates"]:
    direct=c.get("direct_causal_evidence") is True
    spared=c.get("spared_by_counterexamples") is True
    specific=c.get("feeling_specific_necessity") is True
    observable=c.get("observability_after_decisive_loss") is True
    survives=direct and spared and specific and observable
    row={
      "id":c["id"],
      "direct_causal_gate":direct,
      "spared_by_counterexamples_gate":spared,
      "feeling_specific_necessity_gate":specific,
      "post_intervention_observability_gate":observable,
      "minimum_cut_identified":survives,
      "failure_mode":c.get("failure_mode")
    }
    rows.append(row)
    if survives: survivors.append(c["id"])
out={
 "verdict":"IDENTIFIED_SHARED_MINIMUM_CUT" if survivors else "NO_SHARED_MINIMUM_CUT_IDENTIFIED",
 "n_candidates":len(rows),
 "n_identified_cuts":len(survivors),
 "identified_cuts":survivors,
 "rows":rows,
 "interpretation":"Failure does not prove there is no shared bottleneck. It means current direct human evidence does not identify one while preserving a feeling-specific observable. Route multiplicity and hidden convergence both remain live.",
 "next_action":"Prioritize perturb-and-recover, lesion-complement, and double-dissociation evidence that can separate feeling from arousal, report, recognition, and memory."
}
Path("results").mkdir(exist_ok=True)
Path("results/shared_minimum_cut_screen_v001.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps(out,indent=2))
