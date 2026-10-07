02_METHOD BENCHMARK PROTOCOL v001
Date: 2026-10-07
Program: Artificial Emotion Simulation
Purpose: Do not merely call Tournament–MIST "best." Empirically benchmark the methodology itself against serious rival research workflows.
CORE PRINCIPLE
"Best" must be an outcome of a frozen meta-experiment, not a compliment to our own method.
SCOPE
The target is:
best defensible methodology for formal/computational artificial-emotion mechanism discovery under limited research resources.
This is NOT a claim about the best scientific method for every discipline.
==================================================
A. RIVAL PROTOCOLS
==================================================
P0 — SIMPLE HYPOTHESIS TESTING
Choose one plausible model, simulate, test predicted outcomes.
P1 — PREREGISTERED HYPOTHESIS TESTING
P0 plus frozen hypotheses/metrics/analysis.
P2 — BAYESIAN WORKFLOW
Iterative probabilistic model construction, predictive checking, validation, comparison.
P3 — ADVERSARIAL COLLABORATION WORKFLOW
Competing models + jointly acceptable discriminating tests.
P4 — OPTIMAL-DESIGN MODEL TOURNAMENT
Multiple models + model recovery + expected-information-gain experiment selection.
P5 — RECURSIVE TOURNAMENT ONLY
Generate -> attack -> compare -> regenerate.
P6 — MIST ONLY
Formal candidate + complete/minimal implementation stress profile.
P7 — TOURNAMENT + MIST
Our original combined core without the additional safeguards.
P8 — FULL TOURNAMENT–MIST STACK
Systematic evidence audit
+ recursive option generation
+ formalization
+ software/metamorphic validation
+ MIST
+ strongest-rival gate
+ model recovery
+ optimal/adaptive design
+ preregistration
+ causal intervention
+ negative/positive controls
+ sensitivity
+ multiverse
+ equivalence testing
+ locked/nested holdouts
+ blinding where possible
+ OOD/cross-architecture replication
+ reproducible provenance
+ recursive regeneration.
==================================================
B. SYNTHETIC "RESEARCH WORLDS"
==================================================
Construct benchmark worlds where ground truth is known but hidden from each protocol.
W1 — SIMPLE TRUE MECHANISM
One candidate is actually correct and strongly identifiable.
W2 — TRIVIAL-IMPLEMENTATION TRAP
A criterion appears sophisticated but is satisfied by many minimal generic systems.
W3 — BEHAVIORAL MIMIC
Two agents behave similarly; only one contains the proposed coordinating mechanism.
W4 — REWARD-CONFOUND TRAP
Emotion-like behavior is fully explained by scalar reward.
W5 — PARAMETER-FRAGILITY TRAP
Candidate works only in a narrow tuned hyperparameter region.
W6 — ANALYSIS-FLEXIBILITY TRAP
One analysis specification supports the claim while most defensible alternatives do not.
W7 — NON-IDENTIFIABILITY TRAP
Two models generate near-equivalent observable data under standard environments.
W8 — OPTIMAL-INTERVENTION WORLD
Models are indistinguishable passively but separable under one specific intervention.
W9 — SOFTWARE-BUG TRAP
A simulator implementation error generates the apparent signature while preserving ordinary unit outputs.
W10 — NEGATIVE-CONTROL TRAP
A hidden nuisance process affects both candidate state and outcome.
W11 — NULL/NECESSITY TRAP
Ablation yields a nonsignificant difference but the data are too imprecise to establish equivalence.
W12 — OOD FAILURE
A candidate succeeds in training worlds but fails under held-out environmental structure.
W13 — UNKNOWN-MODEL WORLD
Ground truth is NOT present in the initial candidate set. Success requires residual-driven generation of a new model.
W14 — HYBRID-TRUTH WORLD
Two partially correct models must be combined to recover the actual mechanism.
W15 — OVERCOMPLEXITY TRAP
A complex model fits best in-sample but a simpler mechanism is true.
W16 — MEASUREMENT-ALIAS TRAP
The operational metric directly encodes the proposed mechanism and creates circular confirmation.
==================================================
C. FAIRNESS RULE
==================================================
Every protocol receives:
the same initial evidence;
the same candidate descriptions where applicable;
the same total simulation budget;
the same compute ceiling;
the same literature packet;
the same ground-truth-blind evaluator.
Protocol-specific tools are allowed only if they are part of the frozen protocol.
No protocol may inspect the benchmark generator or answer key.
==================================================
D. BLINDING
==================================================
Benchmark worlds receive random opaque IDs.
Condition/model names are replaced by neutral labels during analysis where possible.
The evaluator scoring conclusions is blind to which workflow generated them until scoring is frozen.
Rationale:
blinding is an established protection against expectation/observer bias; evidence from life-science research associates non-blinded methods with inflated effects.
==================================================
E. LOCKED TEST SET / NESTED VALIDATION
==================================================
Any thresholds, hyperparameters, latent-state extractors, or model-selection rules must be tuned using training/validation worlds only.
A locked meta-test set of research worlds is never used during method development.
Where hyperparameter/model tuning occurs, use nested validation or an equivalent clean separation so evaluation data cannot leak into selection.
Rationale:
using the same data for tuning and assessment produces optimistic performance; nested validation substantially reduces this bias.
==================================================
F. PRIMARY METRICS
==================================================
M1 — TRUE-MECHANISM RECOVERY
Fraction of worlds in which the protocol identifies the correct mechanism/equivalence class.
M2 — FALSE-POSITIVE RATE
Fraction of trap/null worlds where the protocol promotes a false mechanism.
M3 — FALSE-NEGATIVE RATE
Fraction of identifiable true worlds where the protocol kills the true mechanism.
M4 — UNKNOWN-MODEL DISCOVERY
Success rate in W13/W14 where the initial candidate set is incomplete.
M5 — CALIBRATION
Do confidence/status labels match actual correctness frequencies?
M6 — CLAIM-CEILING ACCURACY
Does the workflow stop at the strongest claim supported rather than overclaim?
M7 — IDENTIFIABILITY RECOGNITION
Does it correctly label underdetermination when the world does not permit discrimination?
M8 — ROBUSTNESS
How often does a promoted result survive parameter, analysis, seed and OOD variation?
M9 — REPRODUCIBILITY
Can a second independent execution regenerate the same verdict from the frozen artifacts?
M10 — EFFICIENCY
Compute/time/number of experiments required to reach a correct terminal verdict.
M11 — SCIENTIFIC INFORMATION GAIN
Reduction in uncertainty over model space per unit research budget.
M12 — FAILURE-DETECTION COVERAGE
Which planted error classes are detected before a false claim is promoted?
==================================================
G. NO ARBITRARY SINGLE SCORE INITIALLY
==================================================
Do NOT invent one weighted "method quality score" first.
Primary comparison:
Pareto analysis over:
accuracy;
false-positive control;
unknown-model recovery;
calibration;
robustness;
reproducibility;
cost.
A protocol dominates another only if it is no worse on all predeclared primary dimensions and better on at least one, within uncertainty.
If a single decision score is later required, weights must be frozen BEFORE the locked test set and sensitivity-tested across plausible weight sets.
==================================================
H. METHOD ABLATION
==================================================
If P8 wins, ask WHY.
Remove one gate at a time:
- MIST
- preregistration
- adversarial rival
- optimal design
- model recovery
- negative controls
- sensitivity
- multiverse
- equivalence
- metamorphic tests
- OOD
- blinding
- locked holdout
Measure which failure modes reappear.
A component stays canonical only if it:
(a) prevents a material failure,
(b) improves efficiency/information gain,
or
(c) is required for reproducibility/claim integrity.
This prevents "more steps" from being confused with "better method."
==================================================
I. EXTERNAL-METHOD UPDATE FROM 2026 SEARCH
==================================================
Additional protections added after the first Tournament–MIST v1.0:
1. BLIND ANALYSIS WHERE FEASIBLE
Observer/experimenter expectations can bias outcomes. Condition identities and expected directions should be masked for subjective/manual adjudication steps where practical.
2. NESTED / LOCKED VALIDATION
All selection/tuning must be separated from final performance assessment. This is particularly important for choosing latent-state algorithms, thresholds, hyperparameters, or the "best" emotion detector.
3. INDEPENDENT HYPOTHESIS GENERATION
Recent automated-science systems demonstrate end-to-end cycles of literature search, hypothesis generation, experiment proposal, analysis and hypothesis update.
Use at least two independent hypothesis-generation lanes when option coverage matters:
Lane A = canonical project/Tournament derivation.
Lane B = independent generator given the same problem but not Lane A's candidate list.
Deduplicate only AFTER generation.
This is intended to reduce anchoring; it is not treated as independent scientific validation when both lanes use related AI models.
4. METHOD-OF-METHODS ABLATION
The methodology itself must undergo ablation, so complexity is retained only when it produces epistemic value.
==================================================
J. PASS STANDARD FOR "ONE OF THE BEST"
==================================================
We may responsibly describe P8 as "among the strongest / most comprehensive methods we could identify for this problem" only if:
1. no searched integrated methodology covers a strict superset of its nonredundant safeguards;
2. P8 is Pareto-nondominated on the locked benchmark;
3. it materially outperforms simpler baselines on false-positive control and true-model recovery;
4. its advantage survives method-ablation and budget matching;
5. results reproduce independently;
6. external methodological review finds no major omitted failure class.
==================================================
K. PASS STANDARD FOR "BEST" WITHIN DECLARED BENCHMARK
==================================================
We may say:
"best-performing protocol in our preregistered benchmark"
ONLY if P8 satisfies the frozen decision rule on the locked meta-test set.
We may NOT generalize that statement to:
"best scientific method in the world."
==================================================
L. CURRENT STATUS
==================================================
The full method is a LEADING CANDIDATE, not yet benchmark-proven best.
The methodology research has already established that no single compared established method covers all identified failure classes:
Registered Reports protect precommitment/publication bias;
Bayesian workflow protects iterative model checking;
adversarial collaboration protects rival fairness;
optimal design protects experimental information;
MIST protects implementation specificity;
multiverse/sensitivity protect analytic/parameter robustness;
negative controls/causal intervention protect causal validity;
metamorphic testing protects simulator validity;
nested validation protects tuning leakage;
replication/provenance protect generalization/reproducibility.
The Tournament–MIST stack is designed as their nonredundant integration.
NEXT ACTION
Implement the methodology benchmark before using "best" as a scientific claim
METHOD BENCHMARK UPDATE — RE-EVALUATION / DRIFT TESTS
Add benchmark worlds:
W17 — RE-EVALUATION DRIFT TRAP
The initial model is closer to ground truth than later increasingly elaborate revisions. A good method must detect when repeated critique is causing overcorrection rather than improvement.
W18 — REJECTED-ANCESTOR RECOVERY
A rejected early model contains one correct component that the current leader dropped. Success requires comparing the lineage, recovering the lost component, and generating a hybrid.
Add benchmark metrics:
M13 — LINEAGE RECOVERY
How often does the method recover useful structure from earlier/rejected models when later models have drifted?
M14 — RE-EVALUATION STABILITY
How often does repeated reevaluation improve correctness versus merely change framing or increase unnecessary complexity?
M15 — RECENCY-BIAS RESISTANCE
When anonymized candidate versions are scored without chronological order, does the method still select the same current leader?
New ablation:
Remove ancestral comparison while keeping forward recursion. Measure whether W17/W18 failures increase.
Interpretation:
Repeated reevaluation is itself a candidate operator, not automatically beneficial. It remains in the canonical method only if it improves benchmark performance under equal budget.
.