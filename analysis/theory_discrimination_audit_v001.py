import json
from pathlib import Path

P=Path("protocols/feeling_theory_discrimination_audit_v001.json")
data=json.loads(P.read_text(encoding="utf-8"))

strong={"EXPLICIT","DERIVED"}
opposites={
    frozenset(("ABOLISH","PRESERVE_BASIC")),
    frozenset(("ABOLISH","PRESERVE_ELEMENTAL")),
    frozenset(("ABOLISH_ELEMENTAL_AFFECT","PRESERVE_IF_HOR_GNC_REMAINS")),
    frozenset(("ABSENT","POSSIBLE")),
    frozenset(("ABSENT_OR_INACCESSIBLE","PRESERVE_PHENOMENAL")),
    frozenset(("DEGRADE_PHENOMENAL_QUALITY","PRESERVE_ACCESS_IF_BROADCAST_PRESERVED")),
}

rows=[]
for inv in data["interventions"]:
    ps=inv.get("predictions",{})
    names=list(ps)
    for i,a in enumerate(names):
        for b in names[i+1:]:
            pa,pb=ps[a],ps[b]
            divergent=frozenset((pa["value"],pb["value"])) in opposites
            strong_pair=pa["strength"] in strong and pb["strength"] in strong
            observable=(inv.get("independent_phenomenal_ground_truth") is True and inv.get("report_available") is True)
            feasible=(inv.get("human_feasible") is True)
            feeling_scope=(inv.get("scope_feeling") is True)
            admissible=all((divergent,strong_pair,observable,feasible,feeling_scope))
            rows.append({
                "intervention":inv["id"],"theory_a":a,"theory_b":b,
                "prediction_a":pa["value"],"prediction_b":pb["value"],
                "divergent":divergent,"strong_pair":strong_pair,
                "observable":observable,"feasible":feasible,
                "feeling_scope":feeling_scope,"v015_admissible":admissible,
                "failure_mode":inv.get("failure_mode")
            })

admissible=[r for r in rows if r["v015_admissible"]]
near=[r for r in rows if r["divergent"] and r["strong_pair"]]
out={
    "status":"PASS" if admissible else "FAIL_NO_V015_ADMISSIBLE_PAIR",
    "n_pairwise_rows":len(rows),
    "n_strong_divergent_pairs":len(near),
    "n_v015_admissible_pairs":len(admissible),
    "strong_divergent_pairs":near,
    "v015_admissible_pairs":admissible,
    "interpretation":"A strong theoretical disagreement is insufficient unless the same experiment preserves independent observability, selectivity/feasibility, and feeling-specific scope."
}
Path("results").mkdir(exist_ok=True)
Path("results/feeling_theory_discrimination_audit_v001.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps(out,indent=2))
