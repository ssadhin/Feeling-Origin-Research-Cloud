# Benchmarking Research Policies Under Incomplete Hypothesis Spaces
## Locked and Out-of-Distribution Evaluation of Budgeted Epistemic Workflows, with Failure-Driven Derivation of Adaptive Epistemic Search v2

**Hossain Ahmed Sadhin**  
Independent Researcher, Dhaka, Bangladesh  
Corresponding author: sadhinhossainahmed@gmail.com

**Manuscript type:** Methods / metascience research article  
**Version:** 1.0 — 7 October 2026

## Abstract

Scientific methodology is commonly discussed as a collection of principles or workflows, but difficult research often requires a sequential decision: whether the next unit of effort should generate alternatives, test a mechanism, audit software, challenge a prior conclusion, characterize equivalence, search literature, or stop. The problem is harder when the true explanation is absent from the initial hypothesis set. We therefore asked: under a fixed research budget and an initially incomplete hypothesis space, which research policies most reliably recover the best-supported explanation while controlling false conclusions, missed alternatives, overfitting, and conceptual drift? We implemented a hidden-ground-truth benchmark with 22 failure-world classes, a budget of 100 action-cost units, and 17 policy analogues spanning one-pass, preregistered, Bayesian-workflow-like, strong-inference-like, recursive, maximal-stack, diversity-oriented, and adaptive strategies. Policy development was restricted to TRAIN/VALIDATION; Generation-2 policies were frozen before a 22,000-episode-per-policy locked test and a 6,000-episode-per-policy composite out-of-distribution (OOD) test. On the locked test, P14 and P15 achieved 96.11% and 96.15% correct terminal decisions, respectively. The development-leading adaptive P16 achieved 95.68% on the locked test but fell to 69.78% on OOD composites, with a 19.93% false-positive rate. P14 retained 82.62% OOD accuracy and a 5.18% false-positive rate; versus P16, the paired OOD accuracy difference was +12.83 percentage points (95% CI 11.55–14.12) and the false-positive difference was -14.75 points (95% CI -15.83 to -13.67). P14 and P15 were statistically similar in OOD effectiveness, while P15 spent 10 additional budget units. Retrospective replay of six failures from the originating research program then showed that the synthetic survivors still omitted claim-specific gates for prior art, software validity, identifiability, and measurement validity. We therefore derive Adaptive Epistemic Search v2 (AES v2), a gated recursive tournament framework that retains recursive rival search, negative controls, ancestor challenge, and equivalence/underdetermination as its core while routing specialized validity checks according to claim type. AES v2 itself was derived after the decisive benchmark and is not claimed to have been prospectively validated end-to-end. The results support a narrower conclusion: in this benchmark family, recursive research policies with explicit equivalence and lineage checks were substantially more robust than one-pass and development-tuned adaptive alternatives, and the combined failure evidence motivates AES v2 as a prospective research-policy hypothesis.

**Keywords:** scientific methodology; metascience; hypothesis search; research agents; adaptive research; out-of-distribution evaluation; underdetermination; falsification; research policy; AI for science

## 1. Introduction

Scientific inquiry is iterative, but iteration alone does not specify a research methodology. At any stage of a difficult investigation, a researcher may have to choose among qualitatively different actions: generate a rival explanation, inspect residuals, perform a causal intervention, test software, search prior art, conduct sensitivity analysis, challenge an earlier rejected model, test practical equivalence, replicate, or stop. These choices consume limited time, compute, experimental capacity, and attention. The quality of a research program therefore depends not only on the statistical procedure used after data are collected, but also on the sequence in which epistemic actions are selected.

Several established traditions address parts of this problem. Strong Inference emphasizes multiple hypotheses and decisive tests [1]. Bayesian workflow treats modeling as an iterative process of construction, inference, checking, comparison, and revision [2]. Registered Reports and preregistration constrain outcome-contingent flexibility [3,4]. Multiverse and specification-curve analyses expose analytic flexibility [5,6], equivalence testing distinguishes evidence of absence from absence of evidence [7], adversarial collaboration structures disagreement [8], and optimal experimental design (OED) formalizes efficient data acquisition [9]. These are powerful components, but they answer different questions. None alone determines whether the next valuable operation should be new-hypothesis generation, software validation, an ancestor comparison, a negative control, an intervention, literature search, or abstention.

The problem becomes especially acute when the initial hypothesis space is incomplete. If the true mechanism is not among the starting candidates, increasingly rigorous comparison of only those candidates can produce a well-controlled answer to the wrong question. Open-ended model discovery and recent AI-for-science systems address hypothesis generation and iterative refinement [10–15], while contemporary work has begun to formalize adaptive inquiry, moving-incumbent statistical control, and adversarial falsification [16–18]. Yet a complementary metascientific question remains: can complete research workflows themselves be represented and experimentally compared as policies over heterogeneous epistemic actions under a common resource budget?

This paper operationalizes that question. We represent a research methodology as a policy over a state containing candidate hypotheses, evidence, unresolved residuals, remaining budget, and lineage. We then compare policy analogues in hidden-ground-truth synthetic worlds designed to instantiate recurrent research failures such as missing true hypotheses, confounding, behavioral mimicry, non-identifiability, software errors, analysis flexibility, weak-null reasoning, OOD failure, ancestor loss, and shared analyst bias. Importantly, the benchmark is not intended to simulate all of science. Its purpose is to test whether different research-policy structures exhibit predictable strengths and failures under declared conditions.

The study also treats methodology development as vulnerable to the same overfitting it is intended to prevent. Policies were developed only on TRAIN/VALIDATION. Generation-2 candidates were frozen before a locked test and then challenged by composite OOD worlds formed by combining failure classes. This produced a scientifically useful negative result: P16, the strongest balanced development candidate, failed sharply under OOD composition. The result prevented us from simply promoting the most sophisticated adaptive controller.

Finally, we replayed six previously encountered failures from the originating computational/formal research program. This retrospective replay was not blinded and is not an independent external benchmark. Its role was diagnostic: to ask whether the strongest synthetic policies would have required the operations that actually exposed those failures. The replay revealed several omissions, leading to a post-benchmark synthesis, Adaptive Epistemic Search v2 (AES v2).

The contributions are therefore fourfold. First, we formulate research methodology as a budgeted policy over heterogeneous epistemic actions rather than as a fixed checklist. Second, we introduce a benchmark architecture in which the true explanation may be missing from the initial hypothesis set and where lineage, equivalence, software, measurement, and OOD failures can be scored. Third, we show with locked and composite OOD evaluation that development-optimal adaptivity can itself overfit, while simpler recursive policies generalize better in the tested world family. Fourth, we use synthetic and retrospective failure evidence to derive AES v2 while explicitly separating the evidence for its backbone from the still-unvalidated post hoc synthesis.

## 2. Related Work and Novelty Boundary

### 2.1 Classical and modern methodological components

Platt's Strong Inference formalized a cycle of alternative hypotheses, crucial experiments, and recycling of remaining alternatives [1]. AES inherits this adversarial comparative spirit but adds explicit mechanisms for regenerating a hypothesis space when the truth may be absent, testing equivalence, preserving rejected ancestors, and routing non-experimental validity checks.

Bayesian workflow is explicitly iterative and emphasizes model building, checking, comparison, computational troubleshooting, and model expansion [2]. Our benchmark includes a stylized Bayesian-workflow analogue, but it would be incorrect to interpret the results as a test of Bayesian statistics itself. The comparison concerns policy structure in the synthetic environment, not the mathematical validity of Bayesian inference.

Registered Reports and preregistration reduce outcome-contingent flexibility and publication bias by committing key elements before decisive data are known [3,4]. In AES, such freezing is a confirmatory firewall rather than a universal first step, because premature freezing can preserve an incomplete hypothesis space. Multiverse analysis and specification curves address analytic choice sensitivity [5,6]; equivalence testing provides a formal route to claims of practical similarity or absence [7]. These appear as claim-triggered operators rather than mandatory operations in every loop.

OED and Bayesian experimental design treat data acquisition as a decision problem and increasingly support sequential, non-myopic policies [9]. The present work differs in the action space: an epistemic policy may choose not only which experiment to run, but whether the next action should instead be hypothesis generation, prior-art search, code validation, equivalence testing, lineage recovery, or stopping.

### 2.2 Automated scientific discovery and open-ended hypothesis search

Automated statistical model discovery has cast model building as an iterative propose-and-critique process [10]. The AI Scientist demonstrated a broad automated loop from idea generation through code, experiments, manuscript production, and simulated review [11]. Auto-Bench evaluates active scientific discovery through hidden causal structures and interventions [12]. Robin connects literature search, hypothesis generation, experiments, data analysis, and updated hypotheses in a lab-in-the-loop system [13]. Diverse Scientific Hypothesis Search explicitly optimizes a portfolio of high-quality alternatives under a fixed validation budget [14]. HypoArena evaluates prospective construction of hypothesis spaces from inconclusive evidence [15].

These systems make it untenable to claim that recursion, hypothesis generation, tournaments, or adaptive scientific loops are novel in isolation. The question addressed here is at a different level: how to compare *research policies composed of heterogeneous epistemic operators*, especially when the initial hypothesis population can exclude the truth and when the research process must decide between exploration, verification, equivalence, lineage recovery, and specialized validity checks.

### 2.3 Closest 2026 overlaps

Three recent lines of work substantially narrow the novelty claim.

Iris organizes long-horizon ML engineering around an evolving information state and distinguishes epistemic from interventional actions, using adaptive inquiry and knowledge revision under a budget [16]. This is conceptually close to our state-and-action formulation. The present study differs by making the research-policy architecture itself the benchmark object and by explicitly scoring missing-hypothesis recovery, ancestor recovery, underdetermination, failure detection, calibration, and action cost across hidden-world classes.

Evidence-Gated Research (EGR) treats adaptive moving-incumbent model adoption as a statistical control point and supplies anytime-valid evidence and online error control under explicit assumptions [17]. EGR is stronger than AES in formal sequential error guarantees. AES instead addresses a broader action-selection problem and currently lacks comparable FDR/FWER guarantees. The two are complementary: an EGR-like adoption gate is a natural candidate operator for future AES versions.

DASES argues that a static evaluator can itself become an overfitting target and replaces passive validation with adaptive, validity-constrained falsification [18]. This directly challenges any fixed synthetic benchmark, including ours. Our composite OOD test reduces but does not eliminate evaluator-design bias. DASES therefore motivates an important next validation step: test the frozen AES policy against independently generated and adaptively adversarial research environments.

AutoResearchEval independently finds that end-to-end research agents often lack a metacognitive loop capable of checking intermediate products, revising when they fail, and questioning the path taken [19]. EXHYTE similarly identifies weak connections between exploration, hypothesis generation, executable testing, and feedback as a bottleneck in current AI-assisted science [20]. AES can be read as one candidate orchestration-level response, but this paper does not test AES directly on those external benchmarks.

### 2.4 Documented novelty audit

A targeted novelty audit was conducted through 7 October 2026 using semantic and keyword searches across whole-research workflows, AI scientist systems, hypothesis-space search, adaptive inquiry, sequential research decisions, and the exact phrase “Adaptive Epistemic Search.” The audit screened recent academic results and followed the closest matches above. No established scientific-methodology framework using the exact name “Adaptive Epistemic Search” was identified in the documented search, although exact-name uniqueness cannot be guaranteed outside the searched corpus.

The audit does **not** support novelty claims for recursive science, adaptive inquiry, hypothesis search, falsification, frozen validation, or state-based action selection individually. The defensible contribution is the particular evaluation-and-synthesis architecture: (i) complete research methodologies represented as equal-budget policies over heterogeneous epistemic operators; (ii) hidden worlds in which truth can be absent from the initial candidate set; (iii) explicit lineage/ancestor and equivalence/underdetermination scoring; (iv) locked plus composite-OOD policy testing that is allowed to falsify the development winner; and (v) failure-driven derivation of claim-type validity gates from real research mistakes.

## 3. Research Question and Formalization

The primary research question was:

> Given limited time, limited compute, incomplete evidence, and an initially incomplete hypothesis space, what sequence of research actions most reliably discovers the best-supported explanation while minimizing false conclusions, missed alternatives, wasted effort, and conceptual drift?

The research state at step *t* was represented as

**S_t = (H_t, E_t, U_t, B_t, L_t)**,

where H_t is the current hypothesis population, E_t accumulated evidence, U_t unresolved residuals/contradictions, B_t remaining budget, and L_t the lineage of current and rejected candidates. The post-benchmark AES v2 formulation adds **C_t**, the declared claim/task type and active failure risks, because retrospective replay showed that some validity checks should be triggered by claim class rather than executed universally.

A methodology is treated as a policy

**pi(a_t | S_t)**,

where an action may generate hypotheses, observe, compare, inspect residuals, intervene, run controls, perform MIST, test software, conduct sensitivity or multiverse analysis, test equivalence, challenge an ancestor, perform OOD evaluation, replicate, or stop.

This formalization separates two questions that are often conflated: (1) whether a particular epistemic operator is useful under some conditions, and (2) whether a policy invokes that operator at the right time and cost.

## 4. Methods

### 4.1 Benchmark design philosophy

The benchmark was designed as a *stylized diagnostic environment*, not a simulation of scientific reality. Hidden ground truth allows objective scoring of terminal decisions, while deliberately simplified operators permit controlled comparisons of research-policy sequencing. The benchmark can demonstrate that one policy structure performs better than another within the declared generator; it cannot establish universal methodological superiority.

Three safeguards were imposed. First, all policies operated under the same total budget of 100 cost units. Second, policy logic received only a public state; hidden world objects containing the answer key were inaccessible to policy functions. Third, the decisive locked and OOD splits were unavailable during policy development.

### 4.2 Failure-world universe

The frozen benchmark contained 22 world classes:

SIMPLE_TRUE; MISSING_TRUE_HYPOTHESIS; DIVERSITY_COLLAPSE; CONFOUND_TRAP; BEHAVIORAL_MIMIC; NONIDENTIFIABLE; INTERVENTION_ONLY; PARAMETER_FRAGILITY; ANALYSIS_FLEXIBILITY; NEGATIVE_CONTROL_TRAP; WEAK_NULL_EQUIVALENCE; OOD_FAILURE; MEASUREMENT_CIRCULARITY; SOFTWARE_BUG; HYBRID_TRUTH; OVERCOMPLEXITY; REEVALUATION_DRIFT; REJECTED_ANCESTOR_RECOVERY; SURPRISE_DISTRACTOR; EXPENSIVE_PERFECT_TEST; MYOPIC_INFORMATION_GAIN; and SHARED_ANALYST_BIAS.

Several classes deliberately remove the true hypothesis from the initial set. Others create observational mimicry, confounding, analytic flexibility, or implementation artifacts that can make a wrong candidate appear strong. NONIDENTIFIABLE defines multiple hypotheses as equivalent under accessible evidence. REJECTED_ANCESTOR_RECOVERY removes the true earlier candidate from the active population so that only explicit lineage recovery can restore it.

The OOD meta-test used six *compositions* not used as individual development worlds: MISSING_TRUE_HYPOTHESIS+CONFOUND_TRAP; HYBRID_TRUTH+OOD_FAILURE; REJECTED_ANCESTOR_RECOVERY+ANALYSIS_FLEXIBILITY; SURPRISE_DISTRACTOR+SOFTWARE_BUG; MYOPIC_INFORMATION_GAIN+SHARED_ANALYST_BIAS; and DIVERSITY_COLLAPSE+PARAMETER_FRAGILITY. These combinations were intended to test whether policies that solved individual failure modes would retain competence when failures interacted.

### 4.3 Epistemic action costs

The common budget was 100. Action costs were fixed in the benchmark: generate 8; parallel generation 14; observation 8; comparison 10; residual inspection 6; preregistration 3; intervention 20; negative control 8; positive control 6; MIST 10; software test 8; sensitivity analysis 10; multiverse analysis 12; equivalence test 10; OOD test 14; replication 12; ancestor challenge 8; independent analysis 12; simplification 8; hybridization 10.

The numerical costs are abstractions. Their role is to prevent policies from winning simply by executing every available operation.

### 4.4 Policy universe

Seventeen policies were evaluated on the decisive splits. Baseline families included P0 one-pass; P1 preregistered confirmatory; P2 Bayesian-workflow analogue; P3 strong-inference analogue; P5 recursive tournament; P6 tournament+MIST; P7 full fixed stack; P8 first-generation adaptive epistemic search; P9 minimal adaptive; P10 diversity/hierarchical search; P11 surprise/MCTS analogue; and P12 parallel-independent generation/analysis.

Generation 2 added P14–P18 after documented development failures. P14 executes a fixed recursive sequence: generate -> observe -> compare -> residual -> regenerate -> negative control -> ancestor challenge -> equivalence -> OOD. P15 inserts MIST into the same backbone. P16 is a strengthened adaptive controller that conditionally regenerates, compares, intervenes, and performs software/OOD checks based on observed score gaps. P17 repairs the earlier adaptive policy with earlier ancestor/equivalence checks. P18 is a cheaper state-dependent router.

These labels denote *benchmark analogues*, not complete implementations of the named scientific traditions. For example, P2 is not “Bayesian science,” and P3 is not the full historical practice of Strong Inference.

### 4.5 Development firewall and software validity

The first executable prototype was not accepted as evidence. During software-validity testing, two major problems were removed before results were counted: nondeterministic policy seeding and an unacceptable route by which adaptive policy logic could inspect hidden truth. Later, cross-process testing found that Python set iteration made outcomes depend on `PYTHONHASHSEED`. Benchmark v001.1 replaced unordered candidate iteration with deterministic sorted iteration and added a cross-hash-seed invariance check. Results generated before this correction were excluded from the evidential record.

Generation-2 development validation used 22 classes x 250 worlds = 5,500 episodes per policy. P16 was the strongest balanced development candidate (accuracy 0.96273, false-positive rate 0.00527, Brier score 0.02158, mean cost 82.59), slightly ahead of P14/P15 on raw development accuracy. P14–P18 were then frozen. A “locked-test opening” notice explicitly prohibited post-test tuning before the decisive workflow was run.

The locked-test and OOD workflows executed benchmark self-tests and hash-seed invariance checks before evaluation. Both decisive runs used GitHub Actions at commit `633fc711e34e9bf1be37f5760147a5918276d31a`.

### 4.6 Outcome metrics

The primary terminal metric was correct truth/equivalence recovery. Additional metrics included false-positive promotion, false-negative killing of true candidates, missing-hypothesis recovery, recognition of underdetermination, confidence calibration (Brier score), failure-detection coverage, lineage/ancestor recovery, OOD robustness, reproducibility, and mean action cost.

No single weighted score was declared primary. Policies were interpreted using accuracy, false-positive risk, calibration, cost, and Pareto trade-offs.

### 4.7 Statistical analysis

For binomial proportions we report Wilson 95% confidence intervals. Because policies were evaluated on the same world identifiers within a split, primary pairwise accuracy and false-positive comparisons use paired discordant outcomes and exact two-sided McNemar/binomial tests. We also report paired mean differences with normal-approximation 95% confidence intervals; with 22,000 locked and 6,000 OOD paired episodes, these intervals are stable for the large effects emphasized here. P-values are descriptive rather than a substitute for effect size.

The most important pre-specified interpretation constraint was the claim ceiling: success on synthetic hidden-ground-truth worlds could support conclusions about this benchmark family, not “the best scientific method.”

## 5. Results

### 5.1 Locked test

The locked test contained 22,000 episodes per policy. P15 had the highest raw accuracy, 96.15% (95% CI 95.89–96.40), closely followed by P14 at 96.11% (95% CI 95.85–96.36) and P16 at 95.68% (95% CI 95.40–95.94). P14 had the lowest false-positive rate among these three at 0.49% (95% CI 0.41–0.59), versus 0.58% for P15 and 0.76% for P16.

P14 materially exceeded the original adaptive P8: +5.08 percentage points in accuracy (95% CI 4.62–5.54) while reducing false positives by 3.89 points and spending approximately 16.68 fewer budget units. Compared with the simpler Tournament+MIST P6, P14 improved accuracy by 5.80 points (95% CI 5.37–6.24), reduced false positives by 3.54 points, and used the same mean cost of 80.

P14 and P15 were effectively tied in terminal accuracy. The paired P14-P15 accuracy difference was -0.05 points (95% CI -0.36 to +0.27; exact paired p=0.80), and the false-positive difference was -0.09 points (95% CI -0.22 to +0.05; p=0.23). P15 had a small mean Brier advantage of 0.00156 but cost 10 additional units per episode. Thus the locked test did not justify requiring MIST universally.

### 5.2 Composite OOD test

OOD composition produced a much stronger separation. P14 achieved 82.62% correct terminal decisions (95% CI 81.64–83.55) with a 5.18% false-positive rate (95% CI 4.65–5.77). P15 achieved 82.37% (95% CI 81.38–83.31) with a 5.00% false-positive rate. In contrast, P16 dropped to 69.78% accuracy (95% CI 68.61–70.93) with a 19.93% false-positive rate (95% CI 18.94–20.96).

The paired P14-P16 OOD accuracy difference was +12.83 percentage points (95% CI 11.55–14.12; exact paired p=1.47 x 10^-83). The false-positive difference was -14.75 points (95% CI -15.83 to -13.67; p=1.18 x 10^-156), and the Brier-score difference favored P14 by 0.109. P14 also spent 3.93 fewer budget units on average. The central methodological result is therefore not simply that P14 scored highly: the policy that looked best during development was *falsified as the robust winner* by the OOD test.

P14 also outperformed P6 OOD by +4.70 accuracy points (95% CI 3.44–5.96) at equal mean cost, and outperformed the original P8 by +9.92 points (95% CI 8.50–11.34) while spending 16.72 fewer units. P14 and P15 remained statistically indistinguishable in OOD accuracy (+0.25 points for P14; 95% CI -0.96 to +1.46; p=0.71) and false positives (+0.18 points; 95% CI -0.59 to +0.95; p=0.67), while P15 retained its fixed +10 cost.

### 5.3 Failure-class anatomy

The class-level pattern explains why recursive/equivalence policies improved. On the locked test, P3 strong-inference analogue performed well in many worlds but recovered only about 18.6% of MISSING_TRUE_HYPOTHESIS and 18.8% of HYBRID_TRUTH worlds, and approximately 5.3% of REJECTED_ANCESTOR_RECOVERY worlds. It also failed NONIDENTIFIABLE completely because it lacked an explicit equivalence/underdetermination mechanism. P14 was approximately 69.0%, 72.2%, 99.8%, and 100% accurate on those four classes, respectively.

P8, by contrast, performed strongly on individual missing-truth worlds but was weak on ancestor recovery and non-identifiability. Its success did not compose robustly: OOD accuracy was 72.7%, compared with 82.6% for P14. This supports the interpretation that robust research policy requires not only adaptive exploration but also explicit cheap gates that constrain how results are promoted.

The hardest composite for P14 was MYOPIC_INFORMATION_GAIN+SHARED_ANALYST_BIAS (53.8% accuracy), followed by MISSING_TRUE_HYPOTHESIS+CONFOUND_TRAP (71.7%) and HYBRID_TRUTH+OOD_FAILURE (73.3%). These failures matter: P14 is not a solved policy, and the OOD benchmark identifies exactly where further policy development should focus.

### 5.4 Cost and Pareto interpretation

Low-cost baselines remain Pareto-nondominated if cost is treated as an independent objective, even when their scientific accuracy is poor. For this reason, Pareto membership was not interpreted as “scientifically preferred.” The practical comparison is conditional on required reliability. P14 occupied a favorable high-accuracy region at cost 80; P15 offered essentially the same effectiveness at cost 90; P16 spent about 83.9 units OOD but generalized substantially worse.

The result argues against two extremes: minimal one-pass workflows are cheap but fragile, while a maximal fixed verification stack consumes budget on operators that may not target the active failure. The strongest synthetic policies instead use a recurring backbone plus a small number of high-value gates.

## 6. Retrospective Real-Case Replay

Synthetic worlds can reward assumptions embedded by their designer. We therefore replayed the surviving policies against six failures already documented in the originating research program. The replay was qualitative, retrospective, and non-independent. It did not contribute new numeric superiority evidence; its function was to search for missing operator classes.

**R1 — Behavioral non-uniqueness.** A topology-distinct gated-learning rival reproduced a frozen behavioral signature without the initially favored direct reciprocal mechanism. Strong-rival generation, equivalence criteria, held-out evaluation, and a causal discriminator were required. The P14/P15 backbone handled the comparative/equivalence part well.

**R2 — Prior-art/novelty collision.** Targeted literature review later revealed substantial overlap between a proposed mechanism and established consciousness/affective theories, invalidating earlier novelty/winner language. P14/P15 did not encode prior-art search, so a novelty gate was required.

**R3 — Identifiability and pseudoreplication.** A human-study design appeared powerful under participant-level regression but had few truly independent vignette families, yielding severely inflated false positives in simulation. Model recovery, null calibration, unit-of-analysis checks, and leave-family-out validation were necessary. General comparison/equivalence was insufficient.

**R4 — Software contract and redundancy.** A process-ensemble implementation issue had to be corrected before freezing results, and complete-class tests revealed substantial redundancy among formal primitives. This motivated mandatory software validity for code-dependent claims and conditional MIST for criterion-specificity claims.

**R5 — Benchmark hash-order nondeterminism.** The methodology benchmark itself depended on Python hash/set ordering across processes. Same-process repetition failed to reveal the problem; nuisance-environment perturbation (`PYTHONHASHSEED`) did. The incident motivated cross-process reproducibility as a first-class software gate.

**R6 — Stimulus/measurement leakage.** Candidate prose stimuli leaked structural cue words, explicitness, length/event-count differences, and causal ambiguities. The main human experiment was blocked pending measurement validation. This motivated independent construct/stimulus validation and cheap pilot kill gates.

The replay therefore falsified a literal interpretation of P14/P15 as complete research methodologies. Their synthetic backbone was useful, but several real failures belonged to claim-specific validity domains absent from the synthetic action sequence.

## 7. Derivation of Adaptive Epistemic Search v2

AES v2 is a *post-benchmark synthesis*. It should therefore be treated as a prospectively testable methodology, not as if it had generated P14's benchmark scores.

The AES v2 state is expanded to

**S_t = (H_t, E_t, U_t, B_t, L_t, C_t)**,

where C_t records the declared claim/task type and active failure risks.

### Stage 0 — Freeze the problem

Freeze the research question, claim ceiling, current candidates, known evidence, success/kill conditions, remaining budget, lineage/ancestor state, and code/data version. Silent redefinition is prohibited.

### Stage 1 — Claim-triggered front-door validity gates

Before expensive inference, trigger only the gates required by C_t. Code-dependent claims require software validity (unit/invariant/metamorphic tests, cross-process reproducibility, positive/negative cases, provenance). Novelty/mechanism-independence claims require a prior-art audit. Model-selection or human-design claims require model recovery and identifiability checks. Proxy/item/vignette/questionnaire claims require measurement validity. Formal-criterion/minimality claims trigger MIST.

### Stage 2 — Recursive option tournament

Generate broad serious alternatives, including established theories, simple rivals, negations, causal reversals, common-cause explanations, hybrids, and failure-derived candidates. Formalize serious candidates, steelman them, attack them with counterexamples, compare them pairwise where predictions diverge, group equivalent candidates, inspect residuals, regenerate from residuals, and repeat only while materially new non-equivalent survivors appear.

### Stage 3 — Cheap universal gates

Before expensive escalation, perform a negative-control/generic-effect check, an ancestor challenge, and an equivalence/underdetermination check. The ancestor challenge compares the current leader with the first serious candidate, strongest rejected predecessor, simplest viable ancestor, and any earlier version retaining a specific explanatory advantage. If serious survivors are practically indistinguishable under the available evidence, the correct status is UNDERDETERMINED rather than a forced winner.

### Stage 4 — Claim-directed escalation

Escalate only to the operator justified by the live uncertainty: causal intervention for causal claims; sensitivity for parameter fragility; multiverse/specification curves for analytic flexibility; OOD/replication for generalization; equivalence tests with frozen SESOI for null claims; OED/expected information gain for mechanism discrimination; independent analysis trajectories for stochastic analysis; external/domain transfer for general theory extension; and preregistration or Registered-Report-style freezing before decisive confirmatory outcomes.

### Stage 5 — Explicit decision state

Candidates receive PASS, PARTIAL, FAIL, BLOCKED, EQUIVALENT, or UNDERDETERMINED. A leader is promotable only if serious rivals have been addressed, its support is not an artifact of known validity failures, the claim ceiling matches the evidence, and a simpler candidate is not practically equivalent.

### Stage 6 — Stopping

Stop when the relevant finite space is exhausted, repeated regeneration no longer produces material non-equivalent survivors, robust comparisons cease to change the conclusion, identifiability boundaries are explicit, or the expected epistemic value of another operation is lower than its cost. Both convergence and formal underdetermination are legitimate terminal outcomes.

## 8. Discussion

### 8.1 What the benchmark supports

The strongest conclusion is structural rather than branded. In the tested hidden-world family, recursive research policies that could regenerate hypotheses from residuals and explicitly test negative controls, ancestors, and equivalence were markedly more robust than one-pass and several adaptive alternatives. A development-optimized adaptive controller was not protected by sophistication: composite OOD worlds exposed a large degradation. This is a concrete demonstration of *methodological overfitting* at the research-policy level.

The P14-P15 comparison also illustrates why “more rigor” is not synonymous with “run every test.” Adding universal MIST produced no detectable OOD accuracy or false-positive gain in this benchmark but consumed 10% of the total budget. The appropriate conclusion is not that MIST is useless; real-case replay showed it was valuable for formal redundancy/specificity. Instead, the evidence supports conditional routing.

### 8.2 What the benchmark does not support

The study does not show that P14, P15, or AES v2 is universally superior to Bayesian workflow, Strong Inference, preregistration, OED, or any complete real-world scientific tradition. The benchmark policies are stylized analogues. Nor does synthetic recovery establish that the benchmark's world distribution resembles all difficult scientific domains.

Most importantly, AES v2 was synthesized after the locked/OOD evidence and retrospective replay. It has **not** yet been prospectively evaluated end-to-end on an independent benchmark. The paper therefore treats AES v2 as the main *derived methodological hypothesis*, not the empirical winner of the decisive splits. The empirical winner in those splits is the P14/P15 backbone family.

### 8.3 Relationship to the 2026 frontier

The literature audit substantially changed how this work should be framed. Iris already treats long-horizon work as adaptive inquiry over an evolving information state [16]. EGR provides formal statistical control for adaptive moving-incumbent adoption [17]. DASES makes the evaluator itself adaptive and adversarial [18]. AutoResearchEval empirically catalogs process-level failures in frontier autonomous research systems [19], while EXHYTE maps AI-assisted science across exploration, hypothesis generation, and testing with feedback [20]. These results mean that “adaptive recursive research” is not a sufficient novelty claim.

The residual contribution is the *metascientific benchmark object*: a complete research policy over heterogeneous epistemic operators, explicitly tested when truth may be absent from the initial hypothesis set and where lineage, equivalence, failure detection, and cost are outcomes. In this sense the work is closer to policy evaluation for scientific reasoning than to another autonomous-scientist implementation.

### 8.4 Threats to validity

**World-generator inductive bias.** Every synthetic benchmark encodes assumptions about which operations reveal which failure modes. P14's advantage may partly reflect those design choices. Composite OOD tests challenge combinations of frozen classes but remain generated by the same conceptual universe.

**Static-evaluator vulnerability.** The locked benchmark prevents post-test tuning, but DASES highlights a deeper concern: a capable search process can overfit the evaluator family itself [18]. Independent and adaptively generated test environments are required.

**Stylized baselines.** Policy analogues abstract complex traditions. A poor P2 result cannot be interpreted as evidence against Bayesian data analysis, and P3 is not a full historical implementation of Strong Inference.

**Post hoc synthesis.** AES v2 contains gates derived after observing synthetic and real-case failures. Those additions are scientifically motivated but require prospective testing.

**Retrospective replay.** The six real cases come from the same research program, were selected retrospectively, and were judged by the framework's developers. They are useful for failure discovery, not unbiased effect estimation.

**No formal sequential error guarantee.** Unlike EGR, AES v2 presently lacks a theorem controlling long-run false adoption across an adaptively changing hypothesis stream. Integrating anytime-valid statistical adoption is a priority.

**Unmodeled scientific dimensions.** The benchmark does not adequately represent team science, ethical constraints, institutional incentives, wet-lab logistics, domain expertise, theory value beyond truth recovery, or the social processes by which scientific consensus develops.

### 8.5 Falsification criteria for AES v2

AES v2 should be downgraded or replaced if a simpler fixed policy proves practically equivalent or superior on fresh external tasks at lower cost; claim-triggered routing repeatedly misses failures caught by a fixed stack; independent benchmark designers create materially different world families in which AES is dominated; routing cannot reliably identify when specialized gates are needed; or repeated domain transfer shows no advantage over a simpler recursive tournament.

These kill conditions are part of the methodology, not rhetorical caveats. A research method that cannot specify how it would lose is difficult to improve scientifically.

### 8.6 Prospective validation program

The next decisive study should freeze an executable AES v2 router before outcome inspection and evaluate it on research tasks not designed by the present author. Suitable targets include hidden-mechanism discovery benchmarks, prospective hypothesis-space benchmarks, end-to-end research trajectories, and an independently designed adversarial environment suite. The strongest design would compare AES v2, P14, EGR-enhanced P14, an adaptive-falsification policy, and simpler recursive baselines under a matched budget. The primary outcome should remain multi-objective: correct/underdetermined terminal decision, false promotion, calibration, failure detection, missing-hypothesis recovery, and cost.

## 9. Conclusion

This study treats scientific methodology as an experimentally testable sequential policy rather than only a philosophical prescription or fixed checklist. In a frozen hidden-ground-truth benchmark, recursive policies with explicit negative-control, lineage, and equivalence gates achieved high locked-test performance and retained substantially more accuracy under composite OOD failure than a development-leading adaptive controller. The key negative result—P16's OOD collapse—shows why research-policy development itself requires holdouts and why adaptive sophistication does not guarantee generalization.

Retrospective replay then demonstrated that the strongest synthetic backbones were still incomplete for real code-heavy and theory-building work. Those failures motivated AES v2, which combines a recursive tournament spine with claim-triggered validity gates and selective escalation. The current evidence supports AES v2 as a serious *prospective methodological hypothesis* for research with incomplete hypothesis spaces; it does not establish universal optimality, and it does not yet constitute independent end-to-end validation of AES v2 itself.

The broader proposal is falsifiable: research methodologies can be represented as policies, challenged in hidden-world and real-task environments, rejected when they overfit, and revised from documented failure. If this approach survives independent testing, methodological debates can increasingly be supplemented by empirical policy comparison rather than settled only by tradition or intuition.

## Data, Code, and Reproducibility

The benchmark code, frozen workflows, and result snapshots are maintained in the project's GitHub repository (`ssadhin/Feeling-Origin-Research-Cloud`). The decisive locked and OOD runs were executed at commit `633fc711e34e9bf1be37f5760147a5918276d31a` (GitHub Actions runs 37585920892 and 37585926112). Locked and OOD result snapshots are stored under `results_snapshots/meta_methodology/`. A durable public archival release with a DOI should be created before or at submission if the target venue requires anonymous or public artifact access.

## Ethics Statement

This methodology study used synthetic benchmark worlds and retrospective analysis of the author's own research-process artifacts. It did not recruit human participants or use identifiable participant data. Any future application of AES v2 to human-subject research must undergo the ethical review required by the relevant institution and jurisdiction.

## Funding

This research received no external funding.

## Competing Interests

The author declares no competing interests.

## Author Contributions

Hossain Ahmed Sadhin: Conceptualization; Methodology; Investigation; Formal Analysis; Software; Validation; Data Curation; Resources; Visualization; Writing - Original Draft; Writing - Review & Editing; Project Administration. Roles should be revised at submission if any listed contribution is not supported by the final provenance record.

## Acknowledgments and AI-Assistance Disclosure

The author acknowledges the use of OpenAI's ChatGPT as an AI-assisted research tool during parts of the project, including methodological brainstorming, literature-search support, research-organization support, code and benchmark-development assistance, adversarial critique, statistical-analysis assistance, visualization support, and language/editing assistance. The author reviewed the research decisions, evidence, analyses, interpretations, and manuscript content and retains responsibility for the work. Computational workflows were supported by GitHub and GitHub Actions as recorded in the project provenance. ChatGPT is not listed as an author because accountability for the manuscript and scientific claims remains with the human author.

## References

1. Platt JR. Strong inference: certain systematic methods of scientific thinking may produce much more rapid progress than others. *Science*. 1964;146(3642):347-353. doi:10.1126/science.146.3642.347.
2. Gelman A, Vehtari A, Simpson D, et al. Bayesian workflow. arXiv:2011.01808. 2020. doi:10.48550/arXiv.2011.01808.
3. Chambers CD, Dienes Z, McIntosh RD, Rotshtein P, Willmes K. Registered reports: realigning incentives in scientific publishing. *Cortex*. 2015;66:A1-A2. doi:10.1016/j.cortex.2015.03.022.
4. Scheel AM, Schijen MRMJ, Lakens D. An excess of positive results: comparing the standard psychology literature with Registered Reports. *Advances in Methods and Practices in Psychological Science*. 2021;4(2). doi:10.1177/25152459211007467.
5. Steegen S, Tuerlinckx F, Gelman A, Vanpaemel W. Increasing transparency through a multiverse analysis. *Perspectives on Psychological Science*. 2016;11(5):702-712. doi:10.1177/1745691616658637.
6. Simonsohn U, Simmons JP, Nelson LD. Specification curve analysis. *Nature Human Behaviour*. 2020;4:1208-1214. doi:10.1038/s41562-020-0912-z.
7. Lakens D. Equivalence tests: a practical primer for t tests, correlations, and meta-analyses. *Social Psychological and Personality Science*. 2017;8(4):355-362. doi:10.1177/1948550617697177.
8. Mellers B, Hertwig R, Kahneman D. Do frequency representations eliminate conjunction effects? An exercise in adversarial collaboration. *Psychological Science*. 2001;12(4):269-275. doi:10.1111/1467-9280.00350.
9. Huan X, Jagalur J, Marzouk Y. Optimal experimental design: formulations and computations. *Acta Numerica*. 2024;33:715-840. doi:10.1017/S0962492924000023.
10. Li MY, Fox EB, Goodman ND. Automated statistical model discovery with language models. In: *Proceedings of the 41st International Conference on Machine Learning*. PMLR 235; 2024. arXiv:2402.17879.
11. Lu C, Lu C, Lange RT, Foerster J, Clune J, Ha D. The AI Scientist: towards fully automated open-ended scientific discovery. arXiv:2408.06292. 2024. doi:10.48550/arXiv.2408.06292.
12. Chen T, Anumasa S, Lin B, Shah V, Goyal A, Liu D. Auto-Bench: an automated benchmark for scientific discovery in LLMs. arXiv:2502.15224. 2025. doi:10.48550/arXiv.2502.15224.
13. Ghareeb AE, Chang B, Mitchener L, et al. A multi-agent system for automating scientific discovery. *Nature*. 2026;655:497-505. doi:10.1038/s41586-026-10652-y.
14. Wang H, Shojaee P, Meidani K, et al. Towards diverse scientific hypothesis search with large language models. arXiv:2606.10587. 2026. doi:10.48550/arXiv.2606.10587.
15. Zhong T, Jiang W, Wang W, et al. Before the action: benchmarking LLMs on prospective hypothesis discovery. arXiv:2607.15766. 2026. doi:10.48550/arXiv.2607.15766.
16. Fu S, Tao Y, Jin L, et al. Beyond solution-centric search: adaptive inquiry and knowledge revision for autonomous ML engineering. arXiv:2608.02143. 2026. doi:10.48550/arXiv.2608.02143.
17. Guo Y. Evidence-Gated Research: statistically controlled model adoption in adaptive search. arXiv:2610.01751. 2026. doi:10.48550/arXiv.2610.01751.
18. Li P, Lin F, Xing S, et al. Let the abyss stare back: adaptive falsification for autonomous scientific discovery. arXiv:2603.29045. 2026. doi:10.48550/arXiv.2603.29045.
19. Fei Y, Liu N, Yu X, et al. How do agents fail on AutoResearch: end-to-end diagnostic evaluation on 100 real-world frontier research tasks. arXiv:2608.14905. 2026. doi:10.48550/arXiv.2608.14905.
20. Hasib MM, Jo S, Sinha H, Song J, Das A, et al. Unifying AI-assisted scientific discovery around exploration, hypothesis generation, and testing. *Patterns*. Published online September 28, 2026. doi:10.1016/j.patter.2026.101660.
21. Dwork C, Feldman V, Hardt M, Pitassi T, Reingold O, Roth A. The reusable holdout: preserving validity in adaptive data analysis. *Science*. 2015;349(6248):636-638. doi:10.1126/science.aaa9375.

---

### Figure captions

**Figure 1. Research-policy evaluation and derivation of AES v2.** Development occurs before frozen locked and composite OOD tests. The benchmark survivors and retrospective real-case replay jointly motivate AES v2. The figure explicitly separates the evidence for P14/P15 from the post-benchmark AES v2 synthesis.

**Figure 2. Locked-test performance does not guarantee OOD robustness.** Correct terminal decision rates for selected policy analogues; error bars show Wilson 95% confidence intervals. P16 was highly competitive on the locked test but lost substantial accuracy on composite OOD worlds.

**Figure 3. OOD performance-cost trade-off.** Mean action cost versus correct terminal decision rate on the composite OOD test. P14 provides the strongest observed accuracy among the plotted policies at cost 80; P15 has similar accuracy at cost 90.
