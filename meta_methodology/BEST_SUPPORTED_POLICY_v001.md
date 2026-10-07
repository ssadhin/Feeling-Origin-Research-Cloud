12_BEST_SUPPORTED_POLICY_v001 — ADAPTIVE EPISTEMIC SEARCH v2
Subtitle: Gated Recursive Tournament Policy


STATUS
BEST-SUPPORTED OPERATING METHODOLOGY FOR THIS PROJECT'S CURRENT RESEARCH CLASS.
Not a universal-best-science claim.


WHY THIS POLICY
Synthetic benchmark v001.1:
P14/P15 were the strongest robust survivors on locked TEST and OOD composite worlds.
P16 looked strongest on development validation but failed OOD generalization, demonstrating that adaptive thresholds themselves can overfit.
Real-case replay:
literal P14/P15 miss prior-art collisions, software-contract bugs, identifiability/pseudoreplication, and measurement/stimulus leakage unless those gates are explicitly added.
Therefore the final policy is not “P14” or “P15” unchanged. It is the minimal synthesis justified by both evidence streams.


CORE PRINCIPLE
Use recursion to search an incomplete hypothesis space.
Use cheap universal gates before expensive verification.
Use specialized operators only when the current claim/task exposes their failure class.
Never force a winner when remaining candidates are empirically underdetermined.


FORMAL STATE
S_t = (H_t, E_t, U_t, B_t, L_t, C_t)


H_t = current hypothesis population
E_t = accumulated evidence
U_t = unresolved residuals / contradictions
B_t = remaining budget
L_t = lineage of prior and rejected candidates
C_t = declared claim/task type and active failure risks


The policy chooses:
pi(a_t | S_t)


FIXED SPINE — ALWAYS REQUIRED


STAGE 0 — FREEZE QUESTION, CLAIM CEILING, AND CURRENT STATE
Freeze:
decision question;
current candidates;
known evidence;
definitions;
primary claim type;
budget;
success/kill conditions where applicable;
lineage/ancestor state;
data/code version.
No silent redefinition.


STAGE 1 — FRONT-DOOR VALIDITY GATES
Trigger by declared task/claim type, before expensive inference.


A. CODE / COMPUTATIONAL CLAIM
Require software validity:
unit/invariant tests;
metamorphic/symmetry tests where applicable;
cross-process/environment reproducibility;
known-positive and known-negative cases;
provenance/hash freeze.


B. NOVELTY / MECHANISM-INDEPENDENCE CLAIM
Require prior-art audit:
exact terminology;
mathematical/mechanistic synonyms;
older terminology;
strong rival theories;
negative/null literature;
citation-chain search.
“No prior art found” means only within the documented search.


C. MODEL-SELECTION / IDENTIFIABILITY / HUMAN-DESIGN CLAIM
Require model recovery / identifiability:
simulate known generating models;
null calibration;
coverage;
unit-of-analysis check;
item/family generalization;
leave-group-out stability;
recovery of meaningful target effects;
hidden-confound stress test.


D. PROXY / ITEM / VIGNETTE / QUESTIONNAIRE CLAIM
Require measurement validity:
construct separation;
surface/nuisance matching;
independent validation;
reliability;
pilot kill gate.


E. FORMAL CRITERION / MINIMALITY / SPECIFICITY CLAIM
Require MIST:
prevalence;
minimal realization;
symmetry/equivalence;
matched controls;
redundancy/overlap;
perturbation robustness.


These gates are conditional on C_t. They are not all executed mechanically on every project.


STAGE 2 — RECURSIVE OPTION TOURNAMENT
1. Generate a broad candidate set, including established theories, simplest rivals, negations, causal reversals, latent/common-cause alternatives, hybrids, and failure-derived options.
2. Formalize each serious candidate enough to expose inputs, mechanism, predictions, strongest rival, and kill condition.
3. Steelman each survivor.
4. Attack each survivor with counterexamples and alternative explanations.
5. Compare survivors pairwise where their predictions differ.
6. Group equivalent/redundant candidates rather than pretending they are independent.
7. Inspect residuals and failures.
8. Generate new candidates from those residuals.
9. Repeat only while materially new non-equivalent survivors are appearing.


STAGE 3 — CHEAP UNIVERSAL GATES
Before expensive escalation, run:


1. Negative-control / generic-effect check.
2. Ancestor challenge:
current leader vs first serious version;
strongest rejected predecessor;
simplest viable ancestor;
any earlier version that retained an explanatory advantage.
3. Equivalence / underdetermination check:
use prespecified practical-equivalence bounds where a null/equivalence claim is possible.
If observationally indistinguishable under the allowed evidence, report UNDERDETERMINED.


These gates receive priority because the synthetic benchmark showed strong value at modest cost and because project history repeatedly exposed failures they target.


STAGE 4 — CLAIM-DIRECTED ESCALATION
Only invoke the expensive operator justified by the unresolved claim:


Causal claim -> targeted intervention + negative/positive controls.
Parameter/structural robustness claim -> global sensitivity.
Analysis-choice robustness -> multiverse/specification curve.
Generalization claim -> OOD/adversarial holdout + replication ladder.
Null/absence claim -> equivalence test with frozen SESOI.
Mechanism discrimination -> optimal experiment design / expected information gain.
Stochastic analysis -> independent analysis trajectories.
Biological/general theory extension -> external-data/domain transfer.
Confirmatory claim -> preregistration/Registered-Report-style firewall before decisive outcomes.


Do not run the full verification stack simply because it exists.


STAGE 5 — DECISION
For each candidate:
PASS / PARTIAL / FAIL / BLOCKED / EQUIVALENT / UNDERDETERMINED.


A candidate can lead only if:
it beats serious rivals on the relevant evidence;
its support is not an artifact of software, measurement, confounding, analysis flexibility, or prior-art misclassification;
its claim ceiling matches the evidence;
a simpler candidate is not practically equivalent.


STAGE 6 — STOPPING
Stop the current loop when:
finite spaces are exhausted where applicable;
two successive regeneration rounds yield no materially new survivor;
survivors and strongest failed rivals have been compared;
ancestor challenge does not recover a superior earlier model;
identifiability boundaries are explicit;
robustness checks stop changing the conclusion;
new literature search stops changing the taxonomy;
remaining differences are underdetermined or further expected epistemic value is low relative to cost.


Do not stop because one model merely looks good.
Do not continue because recursion itself feels productive.


WHAT THE BENCHMARK CHANGED


REJECTED AS DEFAULT:
One-pass research.
Preregistration alone.
Maximal fixed verification stack.
Development-tuned cheap adaptive threshold policy P16.
Surprise-guided search as truth criterion.


RETAINED AS CORE:
Recursive option search.
Strong rival comparison.
Residual-driven regeneration.
Negative controls.
Ancestor challenge.
Equivalence / underdetermination.
Claim ceiling.


RETAINED CONDITIONALLY:
MIST.
Software test.
Model recovery.
Prior-art audit.
Measurement/stimulus audit.
Causal intervention.
Sensitivity.
Multiverse.
Replication/OOD.
Optimal experiment design.
Preregistration.


SYNTHETIC EVIDENCE SNAPSHOT
Locked TEST, 22,000 episodes/policy:
P14 accuracy .96109; FP .00491; Brier .02701; cost 80.
P15 accuracy .96155; FP .00577; Brier .02545; cost 90.
P16 accuracy .95677; FP .00764; Brier .02477; cost 82.66.


OOD composite test, 6,000 episodes/policy:
P14 accuracy .82617; FP .05183; Brier .11210; cost 80.
P15 accuracy .82367; FP .05000; Brier .11068; cost 90.
P16 accuracy .69783; FP .19933; Brier .22122; cost 83.93.


Interpretation:
P14/P15 survive the OOD shift.
P16 does not.
The P14-vs-P15 difference does not justify mandatory MIST everywhere; MIST is therefore retained as a claim-triggered specialized gate rather than a universal fixed step.


KILL CONDITIONS FOR THIS METHODOLOGY
Downgrade or replace AES v2 if:
1. a simpler fixed policy is practically equivalent or superior across fresh external tasks at lower cost;
2. claim-triggered routing systematically misses failures that a fixed stack catches;
3. real-case replay shows frequent failures caused by skipped conditional gates;
4. independent benchmark designers produce materially different world families where AES v2 is dominated;
5. task-type routing proves too unreliable to decide when MIST/model-recovery/software/measurement gates are needed;
6. repeated domain transfers show no advantage over a simpler recursive tournament.


OPERATIONAL RULE FOR OUR RESEARCH
Use AES v2 immediately as the default methodology for consciousness, feeling-origin, artificial-emotion, and related formal/computational research.
Every active loop must begin by declaring its claim/task type so the relevant front-door gates are selected before outcome inspection.


FINAL VERDICT
For our current research class, the best-supported methodology is:
Adaptive Epistemic Search v2 — Gated Recursive Tournament.


The evidence supports its architecture, not universal optimality.