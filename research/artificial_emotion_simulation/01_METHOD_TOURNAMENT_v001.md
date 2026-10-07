01_METHOD_TOURNAMENT — Research Methodology Components v001
Date: 2026-10-07
Paper: Artificial Emotion Simulation
Purpose: Use our own option-tournament method on research methodologies, compare what each contributes, reject redundancy, and build the strongest justified hybrid protocol.
IMPORTANT CLAIM LIMIT
There is no scientifically meaningful way to prove one methodology is "the best in the world" for every research problem. The goal here is narrower and stronger: construct the most defensible methodology we can justify for artificial-emotion simulation and formal computational theory, using nonredundant strengths from established research methods.
==================================================
EVALUATION CRITERIA
==================================================
Each methodology is judged on:
1. candidate-space coverage;
2. falsifiability / kill power;
3. protection against researcher degrees of freedom;
4. ability to distinguish rival models;
5. causal identification;
6. robustness to parameter/analysis choices;
7. detection of trivial/minimal implementations;
8. simulator/software correctness;
9. reproducibility;
10. efficiency/information gain;
11. ability to learn from failures;
12. clear stopping/convergence rules.
==================================================
CANDIDATE A — RECURSIVE OPTION TOURNAMENT
==================================================
Core:
Generate materially distinct options -> formalize each -> hard-check individually -> compare survivors and failures -> categorize/equivalence-group -> generate new options from residuals/comparisons -> repeat to saturation.
Strength:
Best candidate-generation/discovery engine in the current stack.
Unlike ordinary model selection, comparison itself generates new hypotheses.
Preserves failures as information.
Weakness:
Open-ended spaces can never be literally exhaustive.
Without precommitment, the recursive process can drift or rescue attractive candidates.
Does not by itself test implementation specificity.
Decision:
KEEP AS OUTER DISCOVERY ENGINE.
==================================================
CANDIDATE B — MIST
==================================================
MIST = Minimal-Implementation Stress Test.
Core:
For a formal criterion in a declared minimal model class, measure:
complete-class prevalence where feasible;
minimal realizations;
symmetry/equivalence classes;
matched-mechanism controls;
perturbational/stochastic robustness;
cross-criterion overlap;
operationalization fidelity.
Strength:
Tests whether a supposedly demanding mechanism is structurally cheap/trivial.
Excellent for artificial emotion because an "emotion criterion" that appears in tiny generic controllers is weak evidence of emotion specificity.
Weakness:
Requires a formalizable criterion and declared minimal model class.
Cannot establish biological or phenomenal truth.
A criterion may pass MIST yet still be wrong.
Decision:
KEEP AS INNER SPECIFICITY STRESS TEST.
==================================================
CANDIDATE C — SYSTEMATIC EVIDENCE SYNTHESIS / PRISMA-STYLE AUDIT
==================================================
Core:
Predefine searches, databases, screening rules, inclusion/exclusion, source table, and transparent flow of retained/excluded literature.
Evidence:
PRISMA 2020 provides a 27-item reporting framework and flow diagrams for systematic reviews and encourages explicit reporting of search and selection methods.
Strength:
Prevents our candidate universe from being built only from theories we happen to know.
Creates an auditable prior-art and contradiction record.
Weakness:
PRISMA is primarily a reporting guideline, not a complete discovery algorithm.
Systematic search can still miss terminology or unpublished work.
Decision:
KEEP AS LITERATURE-COVERAGE GATE.
Use a PRISMA-inspired protocol even if the paper itself is not a formal systematic review.
==================================================
CANDIDATE D — PREREGISTRATION / REGISTERED REPORT LOGIC
==================================================
Core:
Freeze hypotheses, primary metrics, controls, exclusions, success/partial/kill gates, and confirmatory analysis before inspecting decisive results.
Evidence:
Registered Reports use peer review/in-principle acceptance before outcomes are known and have been associated with improved methodological and analytic quality while reducing publication/result-selection bias.
Strength:
Prevents post-hoc rescue, HARKing, moving thresholds, and selective reporting.
Weakness:
Cannot eliminate bad theory or bad measurement.
Exploratory discovery still needs flexibility.
Decision:
KEEP AS CONFIRMATORY FIREWALL.
Separate exploratory Tournament generations from frozen confirmatory tests.
==================================================
CANDIDATE E — ADVERSARIAL COLLABORATION
==================================================
Core:
Opposing positions agree in advance on tests capable of resolving disagreement, ideally with neutral arbitration.
Evidence:
Mellers, Hertwig & Kahneman (2001) formalized adversarial collaboration around mutually agreed empirical tests.
Strength:
Forces the winning test to be acceptable to the strongest rival, not only to the theory's proponent.
Excellent protection against straw-man baselines.
Weakness:
True external adversaries may not be available.
Internal red-team simulation is weaker than real independent opponents.
Decision:
KEEP AS ADVERSARY GATE.
For major claims, require a "strongest-rival protocol": what test would a competent defender of each rival accept?
==================================================
CANDIDATE F — OPTIMAL / ADAPTIVE EXPERIMENTAL DESIGN
==================================================
Core:
Choose interventions/environments that maximize expected ability to discriminate candidate models, often via information-gain or model-recovery utility.
Evidence:
Myung & Pitt (2009) show optimal experimental design can choose design variables that maximally distinguish competing cognitive models. Adaptive design work extends this sequentially.
Strength:
Replaces arbitrary experiment selection with explicit information gain.
Particularly useful once multiple artificial-emotion models survive.
Weakness:
Can optimize only against models currently represented.
A design optimal for known rivals may be fragile to unknown models or misspecification.
Decision:
KEEP AS EXPERIMENT-SELECTION ENGINE.
Combine with reserved adversarial/OOD tests not used by the optimizer.
==================================================
CANDIDATE G — MULTIVERSE / SPECIFICATION CURVE
==================================================
Core:
Run all theoretically justified, statistically valid, nonredundant analysis specifications rather than one convenient pipeline.
Evidence:
Steegen et al. (2016) proposed multiverse analysis; Simonsohn, Simmons & Nelson (2020) formalized specification-curve analysis around valid nonredundant specifications and joint inference.
Strength:
Reveals whether conclusions depend on arbitrary preprocessing, metric, exclusion, normalization, seed aggregation, or model-fitting choices.
Weakness:
A badly chosen universe can still be biased.
Combinatorics can explode.
Decision:
KEEP AS ANALYTIC-ROBUSTNESS GATE.
Use bounded justified specifications, not every mathematically imaginable analysis.
==================================================
CANDIDATE H — EQUIVALENCE TESTING / SESOI
==================================================
Core:
Predefine the smallest effect size of interest and test whether effects are small enough to count as practically/theoretically absent, rather than treating "p > .05" as evidence of no effect.
Evidence:
Lakens, Scheel & Isager (2018) describe TOST equivalence tests and emphasize prespecifying and justifying the SESOI.
Strength:
Essential for ablation and negative results:
"removing mechanism X makes no meaningful difference" requires evidence of equivalence, not nonsignificance.
Weakness:
Requires defensible equivalence bounds.
Bad SESOI choices can manufacture an easy null.
Decision:
KEEP FOR NULL / NECESSITY CLAIMS.
==================================================
CANDIDATE I — GLOBAL SENSITIVITY / UNCERTAINTY ANALYSIS
==================================================
Core:
Vary parameters globally rather than only around one tuned point; identify main and interaction effects and structural/scenario sensitivity.
Evidence:
Global sensitivity methods such as Morris screening and Sobol-type variance decomposition are designed to assess parameter importance across parameter space.
Strength:
Prevents one lucky hyperparameter region from masquerading as a mechanism.
Can identify interactions and fragile assumptions.
Weakness:
Can be expensive.
Parameter sensitivity does not by itself address model-structure uncertainty.
Decision:
KEEP AS PARAMETER-ROBUSTNESS GATE.
Pair with Tournament model-structure variation.
==================================================
CANDIDATE J — NEGATIVE CONTROLS + POSITIVE CONTROLS
==================================================
Core:
Negative control: should share relevant bias structure but lack the hypothesized causal mechanism.
Positive control: known condition where the pipeline should detect the effect.
Evidence:
Negative-control methodology is used to detect confounding and bias; recent guidance emphasizes explicit assumptions and prespecified null interpretation.
Strength:
Powerful for detecting generic reward effects, seed artifacts, environment difficulty, logging errors, and spurious causal claims.
For artificial emotion, "flattened mimic" or "same reward without coordination mechanism" can act as mechanism-oriented controls.
Weakness:
A bad negative control may not share the same bias structure.
Null negative controls do not prove absence of all confounding.
Decision:
KEEP AS MANDATORY CONTROL LAYER.
==================================================
CANDIDATE K — CAUSAL INTERVENTION / STRUCTURAL MODEL TESTING
==================================================
Core:
State causal graph assumptions, intervene on candidate internal variables/mechanisms, test predicted downstream consequences, and compare to matched interventions on rivals.
Strength:
Needed because behavioral resemblance and correlational latent states are insufficient for an emotion-mechanism claim.
Ablation, clamping, scrambling, rewiring, and counterfactual interventions become theory tests rather than debugging.
Weakness:
Interventions can have off-target effects.
The chosen causal graph may omit hidden common causes.
Decision:
KEEP AS CORE CLAIM GATE.
No E2+ "emotion-like regulator" claim from correlation alone.
==================================================
CANDIDATE L — MODEL RECOVERY / POSTERIOR-PREDICTIVE WORKFLOW
==================================================
Core:
Before trusting model selection, generate synthetic data from each candidate and verify the inference procedure can recover the true generating model under realistic noise. Then perform predictive checks and out-of-sample comparison.
Evidence:
Modern Bayesian workflow emphasizes iterative model construction, model checking, validation, and comparison; model-discrimination design literature likewise treats recovery as central.
Strength:
Detects non-identifiability and fitting pipelines that always prefer one model.
Separates "model wins" from "our fitting procedure is biased."
Weakness:
Recovery depends on simulated assumptions.
Does not prove reality matches the candidate set.
Decision:
KEEP AS IDENTIFIABILITY GATE.
Inference method can be Bayesian or frequentist; model recovery is mandatory regardless.
==================================================
CANDIDATE M — METAMORPHIC / PROPERTY-BASED TESTING FOR SCIENTIFIC SOFTWARE
==================================================
Core:
Specify relations that outputs must obey when inputs are transformed, even when the exact correct answer is unknown.
Evidence:
Metamorphic testing is specifically used in scientific software where a traditional test oracle is unavailable; exploratory metamorphic testing can expose bugs and model constraints.
Examples for artificial emotion:
renaming irrelevant state labels must not change results;
permuting agent IDs must preserve symmetric outcomes;
adding unused variables must not create emotion-state detection;
time-unit rescaling should preserve dimensionless predictions where applicable;
duplicating an equivalent representation should not create an "emergent" state.
Strength:
Protects scientific conclusions from simulator/code artifacts.
Weakness:
Only tests specified invariances/relations.
A bug that preserves tested relations can remain.
Decision:
KEEP AS SOFTWARE-VALIDITY GATE.
==================================================
CANDIDATE N — COMPUTATIONAL REPRODUCIBILITY / PROVENANCE
==================================================
Core:
version code/data/configs; frozen random seeds; environment lock/container; machine-readable run manifests; raw outputs immutable; regeneration command; checksums where appropriate.
Evidence:
Container-based workflows are recommended to reduce dependency/environment incompatibilities that undermine computational reproducibility.
Strength:
Allows independent regeneration and prevents accidental result drift.
Weakness:
Reproducibility of a wrong model is still wrong science.
Decision:
KEEP AS INFRASTRUCTURE REQUIREMENT.
==================================================
CANDIDATE O — CROSS-SEED / CROSS-ENVIRONMENT / CROSS-ARCHITECTURE REPLICATION
==================================================
Core:
A mechanism survives:
multiple random seeds;
held-out environments;
novel perturbation regimes;
multiple agent architectures where the claim is supposed to be substrate-general;
independent implementation when feasible.
Strength:
Distinguishes a generative principle from a single simulator's quirks.
Weakness:
Transfer scope must match the claim. Requiring universal transfer can wrongly kill implementation-specific mechanisms.
Decision:
KEEP AS GENERALIZATION LADDER.
==================================================
TOURNAMENT RESULT
==================================================
No single methodology dominates all criteria.
The strongest design is a STACK, because the methods solve different failure modes:
Tournament:
failure = incomplete candidate search / premature winner.
PRISMA-style audit:
failure = incomplete prior-art/evidence map.
Preregistration/RR:
failure = moving goals after results.
Adversarial collaboration:
failure = weak/straw-man rivals.
Optimal design:
failure = low-information experiments.
Causal intervention + controls:
failure = correlation/generic behavior mistaken for mechanism.
MIST:
failure = trivial/minimal implementation mistaken for specificity.
Model recovery:
failure = non-identifiable model-selection machinery.
Sensitivity + multiverse:
failure = parameter/analysis fragility.
Equivalence:
failure = nonsignificant result mistaken for absence.
Metamorphic testing:
failure = software/simulator artifact.
Replication/OOD:
failure = one-seed/one-world artifact.
Reproducibility:
failure = result cannot be independently regenerated.
==================================================
META-CONCLUSION
==================================================
The best justified method for this paper is not Tournament OR MIST.
It is:
RECURSIVE TOURNAMENT
+ SYSTEMATIC EVIDENCE AUDIT
+ PRECOMMITMENT
+ ADVERSARIAL RIVAL CONSTRUCTION
+ OPTIMAL DISCRIMINATING DESIGN
+ CAUSAL CONTROLS/INTERVENTIONS
+ MIST
+ MODEL RECOVERY
+ GLOBAL SENSITIVITY
+ MULTIVERSE/SPECIFICATION CURVE
+ EQUIVALENCE TESTING
+ METAMORPHIC SOFTWARE TESTING
+ CROSS-DOMAIN REPLICATION
+ REPRODUCIBLE PROVENANCE.
The canonical method document should arrange these in a sequence so that they do not create redundant bureaucracy.