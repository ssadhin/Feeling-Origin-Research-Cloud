# Supplementary Information
## Benchmarking Research Policies Under Incomplete Hypothesis Spaces

**Author:** Hossain Ahmed Sadhin  
**Version:** 1.0 — 7 October 2026

## S1. Benchmark world classes

| World class | Intended failure pressure | Key discriminating operation(s) |
|---|---|---|
| SIMPLE_TRUE | Straightforward identification | Observation/comparison |
| MISSING_TRUE_HYPOTHESIS | Truth absent initially | Generation after residuals |
| DIVERSITY_COLLAPSE | Early candidate dominance suppresses alternatives | Diverse/regenerative search |
| CONFOUND_TRAP | Wrong candidate benefits from confounding | Negative control/intervention |
| BEHAVIORAL_MIMIC | Rival matches observable behavior | Equivalence + intervention |
| NONIDENTIFIABLE | Multiple candidates observationally equivalent | Equivalence/underdetermination |
| INTERVENTION_ONLY | Observation cannot discriminate | Intervention |
| PARAMETER_FRAGILITY | Candidate succeeds only in narrow regime | Sensitivity analysis |
| ANALYSIS_FLEXIBILITY | Flexible analysis favors wrong candidate | Preregistration/multiverse |
| NEGATIVE_CONTROL_TRAP | Generic effect masquerades as mechanism | Negative control |
| WEAK_NULL_EQUIVALENCE | Non-significance misread as equivalence | Equivalence test |
| OOD_FAILURE | Candidate fails beyond development environment | OOD test/replication |
| MEASUREMENT_CIRCULARITY | Measure embeds target conclusion | Software/measurement/MIST-style audit |
| SOFTWARE_BUG | Implementation artifact supports wrong conclusion | Software test |
| HYBRID_TRUTH | Truth requires combined/generated mechanism | Regeneration/hybridization |
| OVERCOMPLEXITY | Complex candidate appears superior without necessity | Simplification/OOD |
| REEVALUATION_DRIFT | Revision moves away from stronger earlier model | Ancestor challenge |
| REJECTED_ANCESTOR_RECOVERY | True earlier candidate is absent from active set | Ancestor recovery |
| SURPRISE_DISTRACTOR | Novel/surprising candidate is attractive but wrong | OOD/replication |
| EXPENSIVE_PERFECT_TEST | Decisive test exists but is costly | Budget-sensitive allocation |
| MYOPIC_INFORMATION_GAIN | Locally informative action blocks later discovery | Residual-driven regeneration |
| SHARED_ANALYST_BIAS | Repeated analysis shares the same bias | Independent analysis/replication |

## S2. Decisive policy definitions

The benchmark compared 17 policies. Generation-2 policies were frozen before the decisive tests.

- **P14 — Recursive Tournament + Equivalence:** generate -> observe -> compare -> residual -> generate -> negative control -> ancestor -> equivalence -> OOD. Fixed cost 80.
- **P15 — Tournament-MIST + Equivalence:** P14 with MIST inserted after observation. Fixed cost 90.
- **P16 — Strengthened adaptive controller:** generate and observe; regenerate or compare based on score/gap thresholds; universal negative-control/ancestor/equivalence gates; terminate on detected non-identifiability; conditionally intervene; then software/OOD/observation as budget permits.
- **P17 — Repaired adaptive P8:** earlier ancestor/equivalence routing followed by selective intervention and verification.
- **P18 — Cheap-first router:** early generate/observe, conditionally inspect residuals or compare, then cheap gates and selective escalation.

The policies were benchmark programs, not literal implementations of complete philosophical or statistical traditions.

## S3. Decisive quantitative results

### S3.1 Locked test (22,000 episodes per policy)

| Policy | Accuracy | 95% CI | False-positive rate | 95% CI | Brier | Mean cost |
|---|---:|---:|---:|---:|---:|---:|
| P3 | 0.79891 | 0.79356–0.80415 | 0.04800 | 0.04525–0.05090 | 0.10367 | 70.00 |
| P5 | 0.89445 | 0.89030–0.89846 | 0.03686 | 0.03446–0.03942 | 0.07431 | 78.00 |
| P6 | 0.90305 | 0.89906–0.90689 | 0.04027 | 0.03775–0.04295 | 0.06998 | 80.00 |
| P8 | 0.91027 | 0.90642–0.91398 | 0.04377 | 0.04115–0.04656 | 0.05904 | 96.68 |
| P14 | 0.96109 | 0.95845–0.96357 | 0.00491 | 0.00407–0.00592 | 0.02701 | 80.00 |
| P15 | 0.96155 | 0.95892–0.96401 | 0.00577 | 0.00485–0.00686 | 0.02545 | 90.00 |
| P16 | 0.95677 | 0.95400–0.95938 | 0.00764 | 0.00657–0.00888 | 0.02477 | 82.66 |
| P17 | 0.94900 | — | 0.02150 | — | 0.03281 | 96.53 |
| P18 | 0.93036 | — | 0.03377 | — | 0.04884 | 75.16 |

### S3.2 Composite OOD test (6,000 episodes per policy)

| Policy | Accuracy | 95% CI | False-positive rate | 95% CI | Brier | Mean cost |
|---|---:|---:|---:|---:|---:|---:|
| P3 | 0.42983 | — | 0.24733 | — | — | 70.00 |
| P5 | 0.72700 | — | 0.12950 | — | 0.19541 | 78.00 |
| P6 | 0.77917 | 0.76849–0.78948 | 0.06333 | 0.05745–0.06978 | 0.14179 | 80.00 |
| P8 | 0.72700 | — | 0.12517 | — | 0.17982 | 96.72 |
| P14 | 0.82617 | 0.81637–0.83555 | 0.05183 | 0.04651–0.05774 | 0.11210 | 80.00 |
| P15 | 0.82367 | 0.81382–0.83310 | 0.05000 | 0.04477–0.05581 | 0.11068 | 90.00 |
| P16 | 0.69783 | 0.68609–0.70932 | 0.19933 | 0.18942–0.20963 | 0.22122 | 83.93 |
| P17 | 0.75167 | — | 0.16000 | — | 0.18213 | 96.84 |
| P18 | 0.68033 | — | 0.23183 | — | — | 75.15 |

### S3.3 Paired comparisons centered on P14

| Split | Comparator | Accuracy difference P14 - comparator | 95% CI | Exact paired p | False-positive difference | 95% CI | Exact paired p |
|---|---|---:|---:|---:|---:|---:|---:|
| Locked | P15 | -0.00045 | -0.00363 to 0.00272 | 0.801 | -0.00086 | -0.00220 to 0.00047 | 0.230 |
| Locked | P16 | 0.00432 | 0.00112 to 0.00752 | 0.0089 | -0.00273 | -0.00420 to -0.00126 | 0.00033 |
| Locked | P6 | 0.05805 | 0.05366 to 0.06243 | <1e-100 | -0.03536 | approximately -0.038 to -0.033 | <1e-100 |
| Locked | P8 | 0.05082 | 0.04624 to 0.05540 | <1e-100 | -0.03886 | approximately -0.041 to -0.036 | <1e-100 |
| OOD | P15 | 0.00250 | -0.00962 to 0.01462 | 0.706 | 0.00183 | -0.00586 to 0.00953 | 0.671 |
| OOD | P16 | 0.12833 | 0.11551 to 0.14116 | 1.47e-83 | -0.14750 | -0.15830 to -0.13670 | 1.18e-156 |
| OOD | P6 | 0.04700 | 0.03437 to 0.05963 | 3.96e-13 | -0.01150 | -0.01946 to -0.00354 | 0.0053 |
| OOD | P8 | 0.09917 | 0.08499 to 0.11335 | 5.0e-42 | -0.07333 | approximately -0.083 to -0.064 | 4.57e-50 |

The quantitative interpretation does not depend on marginal P14/P15 differences. The robust signal is the large OOD separation between P14/P15 and P16, and between P14 and simpler/adaptive comparators.

## S4. OOD composition results

Accuracy by OOD composition for selected policies:

| Composition | P5 | P6 | P8 | P14 | P15 | P16 |
|---|---:|---:|---:|---:|---:|---:|
| DIVERSITY_COLLAPSE + PARAMETER_FRAGILITY | 0.927 | 0.997 | 0.997 | 0.994 | 0.999 | 0.976 |
| HYBRID_TRUTH + OOD_FAILURE | 0.642 | 0.697 | 0.596 | 0.733 | 0.716 | 0.374 |
| MISSING_TRUE_HYPOTHESIS + CONFOUND_TRAP | 0.680 | 0.707 | 0.705 | 0.717 | 0.720 | 0.406 |
| MYOPIC_INFORMATION_GAIN + SHARED_ANALYST_BIAS | 0.268 | 0.379 | 0.635 | 0.538 | 0.542 | 0.435 |
| REJECTED_ANCESTOR_RECOVERY + ANALYSIS_FLEXIBILITY | 0.851 | 0.896 | 0.433 | 0.976 | 0.965 | 0.996 |
| SURPRISE_DISTRACTOR + SOFTWARE_BUG | 0.994 | 0.999 | 0.996 | 0.999 | 1.000 | 1.000 |

P14 is not uniformly dominant. The MYOPIC_INFORMATION_GAIN + SHARED_ANALYST_BIAS composition remains a major weakness and should be emphasized in future benchmark expansion.

## S5. Retrospective real-case replay

| Case | Failure eventually demonstrated | Operation that exposed/managed it | P14/P15 status | AES v2 repair |
|---|---|---|---|---|
| R1 behavioral non-uniqueness | Topology-distinct rival matched behavioral signature | Strong rival + frozen equivalence + held-out + causal discriminator | Good backbone | Retain; require causal discriminator for uniqueness |
| R2 prior-art collision | Proposed mechanism substantially overlapped existing theories | Prior-art/citation-chain search | Miss | Novelty gate |
| R3 identifiability/pseudoreplication | Few independent vignette families inflated apparent power/FPR | Model recovery + unit-of-analysis + null calibration | Miss | Identifiability gate |
| R4 software contract/redundancy | Code contract bug; formal primitives redundant | Software tests + complete-class/MIST-style audit | Partial/miss | Software gate; MIST conditional |
| R5 hash nondeterminism | Results changed across PYTHONHASHSEED | Cross-process reproducibility | Miss | Cross-environment software validation |
| R6 stimulus validity | Structural cue leakage and nuisance differences | Measurement audit + independent validation + pilot kill gate | Miss | Measurement gate |

## S6. Novelty audit protocol and result

### Search scope

The novelty audit was conducted on 7 October 2026. It was a targeted literature audit, not a registered systematic review. Searches covered:

1. whole-research workflow/policy benchmarking under incomplete/open hypothesis spaces;
2. autonomous scientific-discovery systems and end-to-end benchmarks;
3. diverse/open-ended scientific hypothesis search;
4. Strong Inference, adversarial collaboration, Bayesian workflow, Registered Reports, equivalence, multiverse/specification curves, and optimal experimental design;
5. sequential/value-of-information formulations of research decisions;
6. exact-phrase search for “Adaptive Epistemic Search”; and
7. targeted follow-up for the closest 2026 overlaps (EGR, DASES, AutoResearchEval, EXHYTE, HypoArena, Diverse Scientific Hypothesis Search, Iris).

### Closest prior work and residual contribution

| Prior work | Closest overlap | Why it does not subsume the present contribution |
|---|---|---|
| Strong Inference (1964) | Multiple alternatives; decisive tests; recycling | Does not operationalize heterogeneous research actions, software/measurement gates, incomplete hypothesis-space recovery, or benchmark policy selection |
| Bayesian workflow (2020) | Iterative model building/checking/comparison | Focused on statistical modeling workflow rather than a budgeted policy over literature, software, lineage, controls, experiment design, and stopping |
| OED review (2024) | Sequential, non-myopic acquisition policies | Optimizes data/experiment acquisition over a declared design space, not the entire epistemic action set |
| Automated statistical model discovery (2024) | Open-ended propose/critique model search | Searches model space rather than experimentally comparing complete research methodologies |
| AI Scientist (2024) / Robin (2026) | End-to-end iterative research loops | System implementations; do not benchmark competing epistemic policies under hidden missing-hypothesis worlds |
| Diverse Scientific Hypothesis Search (2026) | Diverse alternatives under fixed validation budget | Optimizes hypothesis portfolio generation, not downstream heterogeneous operator sequencing |
| HypoArena (2026) | Prospective hypothesis-space construction | Evaluates pre-action hypothesis discovery; AES benchmark continues through controls, equivalence, lineage, OOD, and stopping |
| Iris (2026) | Information-state representation; epistemic vs interventional actions; adaptive topology | Very close state/action framing, but evaluated as an ML-engineering agent; present study benchmarks multiple complete policy structures with lineage/equivalence/missing-truth outcomes |
| Evidence-Gated Research (2026) | Adaptive path dependence; frozen challengers; statistical adoption control | Stronger formal error control, narrower adoption problem; AES covers broader research-action routing and currently lacks EGR's guarantees |
| DASES (2026) | Adaptive falsification; benchmark-overfitting critique | Adaptive evaluator is complementary and exposes a limitation of the fixed synthetic benchmark; not a policy comparison over the full action taxonomy |
| AutoResearchEval (2026) | Process-level failure taxonomy; missing metacognitive loop | External diagnostic benchmark rather than a proposed/evaluated policy architecture |
| EXHYTE (2026) | Explore-hypothesize-test-feedback workflow abstraction | High-level review abstraction rather than a budgeted policy benchmark with hidden truth, lineage, and explicit validity gates |

### Novelty verdict

The paper should **not** claim invention of recursive science, adaptive inquiry, falsification, hypothesis search, frozen validation, OOD testing, or epistemic action selection. The defensible novelty is the combined benchmark-and-derivation contribution:

1. complete research methodologies are evaluated as policies over heterogeneous epistemic operators under an equal budget;
2. the hidden benchmark explicitly contains missing true hypotheses, non-identifiability, ancestor recovery, software/measurement failures, and interacting OOD failures;
3. methodology selection itself is subjected to development/locked/OOD separation, and the development-leading adaptive policy is allowed to fail;
4. lineage/ancestor challenge and equivalence/underdetermination are first-class policy actions/outcomes;
5. a retrospective failure replay is used to identify claim-specific validity operators omitted by synthetic winners; and
6. the resulting AES v2 is explicitly labeled a post-benchmark synthesis requiring prospective validation.

No exact established research methodology named “Adaptive Epistemic Search” was identified in the documented search. This is a bounded search result, not a guarantee of global naming uniqueness.

## S7. Reproducibility provenance

- Repository: `ssadhin/Feeling-Origin-Research-Cloud` (private at manuscript preparation time).
- Deterministic benchmark v001.1 commit: `8fced8cf429263e7969bfc463666518f6899885d`.
- Generation-2 benchmark commit: `963d9642b688d66d0b12be02cf6e48e6284c856f`.
- Frozen decisive workflow commit: `633fc711e34e9bf1be37f5760147a5918276d31a`.
- Locked run: GitHub Actions `37585920892`; artifact ID `11465579673`; artifact SHA-256 digest `9b38e530d39ba345d7fec40af02577f44edc7c4465925ec1eb47eb4bd7b14b07`.
- OOD run: GitHub Actions `37585926112`; artifact ID `11466571256`; artifact SHA-256 digest `de00fa7d1538febd23f95a89abc4a89aef2171cf0ec460a8892ed3d8bde5f572`.
- Frozen result snapshot commits: locked `2b78b049a4d7c857399dc3e7c9436462fe8bccea`; OOD `052802e474aca76d5218fb3289d20597fe03363b`.
- Real-case replay commit: `621b703992b38eca4bc99981b4b8def4f30b74f9`.
- AES v2 operating-policy commit: `e8a2d5fc699336d658ea8196ab9d9f4ccdd5c331`.

Before public submission, the recommended archival action is to create a permanent public release or DOI-bearing archive of the benchmark code, frozen configs, decisive result summaries, and enough raw data to reproduce the reported tables and paired comparisons.
