from __future__ import annotations
import time

# Empirically motivated structural constraints.
# PASS means the model has independent degrees of freedom needed to represent the case
# without redefining one variable after seeing the result.
constraints = {
 "unconscious_local_processing":
   "Local appraisal/sensory computation can persist when global conscious capacity is absent.",
 "awake_unseen_emotion":
   "A globally conscious subject can process an emotional stimulus and react autonomically without awareness of that content.",
 "dream_internal_content":
   "Conscious content can exist without matching current external input.",
 "context_changes_quality":
   "The same/similar local input or stimulation can have different qualitative interpretation under different causal context.",
 "hypersynchrony_loss":
   "High activity/connectivity alone can coexist with loss of consciousness when differentiation collapses.",
 "cross_species":
   "A universal account cannot require mammalian-specific laminar/thalamocortical anatomy."
}

models = {
 "survival_scalar":{
   "unconscious_local_processing":False,
   "awake_unseen_emotion":False,
   "dream_internal_content":False,
   "context_changes_quality":False,
   "hypersynchrony_loss":False,
   "cross_species":True,
 },
 "global_gate_only":{
   "unconscious_local_processing":True,
   "awake_unseen_emotion":False,
   "dream_internal_content":True,
   "context_changes_quality":False,
   "hypersynchrony_loss":False,
   "cross_species":True,
 },
 "recurrence_only":{
   "unconscious_local_processing":True,
   "awake_unseen_emotion":False,
   "dream_internal_content":True,
   "context_changes_quality":False,
   "hypersynchrony_loss":False,
   "cross_species":True,
 },
 "mammalian_L5_switch":{
   "unconscious_local_processing":True,
   "awake_unseen_emotion":True,
   "dream_internal_content":True,
   "context_changes_quality":True,
   "hypersynchrony_loss":True,
   "cross_species":False,
 },
 "local_pattern_plus_gate":{
   "unconscious_local_processing":True,
   "awake_unseen_emotion":True,
   "dream_internal_content":True,
   "context_changes_quality":False,
   "hypersynchrony_loss":True,
   "cross_species":True,
 },
 "domain_plus_admission_plus_causal_geometry":{
   "unconscious_local_processing":True,
   "awake_unseen_emotion":True,
   "dream_internal_content":True,
   "context_changes_quality":True,
   "hypersynchrony_loss":True,
   "cross_species":True,
 },
}

def main():
    t=time.perf_counter()
    print("=== V008 RIVAL CONSTRAINT TEST ===")
    headers=list(constraints)
    for name,m in models.items():
        score=sum(bool(m[k]) for k in headers)
        failed=[k for k in headers if not m[k]]
        print(f"{name:42s} {score}/{len(headers)}  failures={','.join(failed) if failed else 'NONE'}")
    full=[name for name,m in models.items() if all(m[k] for k in headers)]
    print("\nModels with representational degrees of freedom for every constraint:",full)
    print("\nIMPORTANT:")
    print("This is a structural falsification matrix, not a likelihood fit.")
    print("Passing means the architecture can represent every constraint without changing definitions.")
    print("It does not prove that the architecture is the unique biological implementation.")
    print(f"runtime_seconds={time.perf_counter()-t:.6f}")

if __name__=="__main__":
    main()
