import json
from pathlib import Path
d=json.loads(Path("protocols/crfi_reduction_audit_v001.json").read_text())
rows=[]
survivors=[]
for k in d["commitments"]:
    prior_escape = len(k.get("prior_coverage",[]))==0
    divergent = bool(k.get("current_unique_observable_prediction",False))
    eligible = not k.get("post_hoc_refinement",False) and not k.get("methodological_not_mechanistic",False)
    survives = prior_escape and divergent and eligible and not k.get("directly_falsified",False)
    row={
      "id":k["id"],
      "prior_art_escape":prior_escape,
      "divergent_observable_prediction":divergent,
      "eligible_original_mechanistic_commitment":eligible,
      "directly_falsified":bool(k.get("directly_falsified",False)),
      "distinctness_survives":survives,
      "coverage":k.get("prior_coverage",[])
    }
    rows.append(row)
    if survives: survivors.append(k["id"])
out={
 "verdict":"DISTINCT_THEORY_SURVIVES" if survivors else "REDUCE_TO_SYNTHESIS_FRAMEWORK",
 "n_commitments":len(rows),
 "n_distinct_survivors":len(survivors),
 "survivors":survivors,
 "rows":rows,
 "consequence":(
   "CRFI must no longer be presented as a distinct discovered mechanism of feeling. "
   "Retain it, if useful, as a synthesis/engineering framework, vocabulary, or benchmark architecture. "
   "The V009 methodological no-go and other project results remain valid on their own terms. "
   "A future revival of distinct-theory status would require genuinely new evidence, not reinterpretation of these failed gates."
 )
}
Path("results").mkdir(exist_ok=True)
Path("results/crfi_reduction_audit_v001.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps(out,indent=2))
