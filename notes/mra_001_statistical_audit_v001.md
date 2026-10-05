# MRA-001 statistical audit v001

Date: 2026-10-05
Status: CORE STATISTICAL AUDIT COMPLETE; R3 result still pending.
Verdict: STATISTICAL_REPORTING_PASS_WITH_NO-EQUIVALENCE_FIREWALL.

## Primary estimands

CASE O002:
Primary question is paired out-of-sample MAE improvement from adding peripheral physiology beyond the frozen context + recent-report model.
Delta = MAE(baseline) - MAE(physiology); positive favors physiology.

POPANE R1:
Primary benchmark is even stricter:
delta_naive_phys = MAE(recent-state persistence) - MAE(physiology-augmented model).
Positive favors physiology.
The fitted context-vs-physiology delta is a secondary nested comparison.

These signs must be stated explicitly in every table/figure to avoid inversion errors.

## Repeated-observation uncertainty

CASE primary:
participant bootstrap over held-out-subject MAE is aligned with the LOSO generalization target.

CASE G1/G2:
crossed subject×video bootstrap explicitly acknowledges both generalization dimensions.

POPANE R1:
predeclared participant-cluster bootstrap preserves dependence among windows/segments within participants.

POPANE R4 sensitivity:
independently resamples participants and segments and operates on observed participant×segment cell contrasts.
R4 outcome CROSSED_UNCERTAINTY_STRONGLY_SUPPORTS_R1: all eight horizon×learner naive-vs-physiology CIs remain strictly negative.
Therefore the R1 conclusion is not dependent on participant-only uncertainty.

## Effect-size direction, not only significance

POPANE effects grow in absolute MAE disadvantage with horizon.
R1 participant-cluster delta naive−physiology:
- Ridge: approximately -0.038, -0.077, -0.104, -0.126 at 1/11/21/31 s.
- HGB: approximately -0.055, -0.104, -0.140, -0.172.
R4 crossed-cell means are nearly identical in direction/magnitude.

Thus the result is not merely a collection of CIs touching one side of zero; the observed physiology models are materially worse than the simple benchmark in these data.

## No equivalence claim

The project did NOT preregister a smallest effect size of interest or equivalence margin.
Therefore:
- CI containing zero must be described as inconclusive/non-significant, not “equivalent.”
- Negative CIs support degradation relative to the comparator, not proof that true incremental information is exactly zero.
- “no incremental benefit detected” is permitted when the relevant CI is non-positive under the frozen rule.
- “equivalent,” “same,” “no effect whatsoever,” and universal-zero language are not permitted.

## Multiplicity

Confirmatory/frozen decisions:
- preserve their predeclared rules as primary.

Post-primary screens:
- B2/B3, D1, R2, R3, R4, R5 are sensitivity/exploratory layers.
- D1 contains multiple horizon×axis×learner cells; isolated HGB positives are not promoted because the frozen D1 rescue required cross-model agreement.
- R5 contains 3 families × 4 horizons × 2 learners. Its protocol explicitly forbids promoting isolated cells and requires the same family×horizon to be positive for both learners.
- R5 verdict NO_FAMILY_RESCUE; in fact all observed family-vs-context means were negative.

No post-primary family/horizon/model cell should be described as “statistically significant discovery” without multiplicity-aware follow-up.

## Model selection / hyperparameter tuning

Ridge alpha selection is performed only on training data using participant-grouped folds.
Held-out subject/video/segment data do not enter tuning.

HGB hyperparameters are fixed in the frozen external protocol rather than optimized on held-out outcomes.

This supports honest out-of-sample evaluation but does not establish that every possible physiology representation/model would fail.

## Metric scope

Primary loss is MAE, chosen before the relevant outcomes.
MAE is interpretable on the report scale and robust to occasional large errors.

Current claim must be metric-specific:
“under MAE-based prospective level/change forecasting...”

The project has not yet established that the ordering is identical under every alternative scoring rule (e.g., RMSE, correlation/CCC, probabilistic scores). This is a reporting limitation, not a hidden failure.

Recommended manuscript reporting:
- keep MAE as primary;
- provide RMSE/correlation only as explicitly post-primary descriptive/sensitivity metrics if computed;
- do not let a secondary metric override the frozen MAE decision.

## Persistence baseline interpretation

The parameter-free comparator is not a trained autoregressive model. It carries forward the recent pre-target mean affect state.
This is scientifically important because it is:
- leakage-resistant;
- deployable without training;
- not helped by segment duration metadata;
- difficult to dismiss as overfitting.

The fitted context and physiology models receive normalized time metadata in addition to recent state, so the persistence benchmark is not winning because it had more covariates.

## Change-target analysis

CASE D1:
mixed model-specific physiology-vs-context effects, but no cross-model rescue; zero-change beats physiology everywhere.

POPANE R2:
NO_EXTERNAL_CHANGE_INCREMENT and strong zero-change dominance.
Both Ridge and HGB are significantly worse than context and zero-change at all four valence horizons.

This means the level result cannot be dismissed simply by saying “physiology predicts transitions rather than levels” under the tested POPANE representation.

## Generalizability boundary

Statistical evidence supports:
- CASE valence/arousal within this controlled-video continuous-report dataset;
- POPANE valence in Study 6;
- 1/11/21/31 s horizon regime;
- tested peripheral features/models/generalization contracts.

It does NOT statistically support:
- all possible physiological features;
- all horizons;
- all affect tasks;
- all populations;
- all modalities;
- external arousal replication;
- causal irrelevance.

## Current statistical readiness

PASS for manuscript drafting once R3 is resolved or appropriately scoped.

R4 removes the main uncertainty-unit concern.
R5 removes the simple “one noisy modality ruined the full model” objection.
R2 removes the cleanest independent transition-target rescue.

Remaining wording discipline:
- predictive increment, not causal mechanism;
- replicated for valence externally, not arousal;
- degradation/no benefit under tested MAE contract, not universal equivalence.
