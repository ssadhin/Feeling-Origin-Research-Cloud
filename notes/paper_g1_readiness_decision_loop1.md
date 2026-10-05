# PAPER-G1 research-loop decision 1 of 3

Date: 2026-10-05
Frozen gate: protocols/paper_g1_manuscript_readiness_gate.md
Gate commit: 590e43570c8d5ab4605bb2c8acc290e2ecde22ad

## Decision

PAPER_READY_FOR_DRAFTING — LOOP DECISION 1 OF 3.

This is a research-readiness decision only. The project rule remains active: do NOT create or modify the manuscript until three consecutive research-loop readiness decisions agree, unless the user explicitly overrides that rule.

## Gate evaluation

G1 — Primary CASE/O002 prospective result: PASS.
The primary CASE result is preserved, predictor/target windows are prospectively separated, and the stronger O002-G1 double holdout excludes both test person and test video from training. Prior-state persistence gives a very large improvement; peripheral physiology adds no positive increment for valence or arousal.

G2 — Independent external replication: PASS.
POPANE-R1 independently reproduces persistence dominance for continuous self-reported valence across 1/11/21/31 s and Ridge/HGB under held-person × held-segment evaluation.

G3 — Transition/change rescue: PASS.
CASE-D1 has some HGB-only exploratory positive context increments but no Ridge/HGB robust rescue and zero-change beats physiology everywhere. POPANE-R2 independently shows NO_EXTERNAL_CHANGE_INCREMENT and strong zero-change dominance.

G4 — Generalization-axis uncertainty: PASS.
POPANE-R4 crossed participant×segment bootstrap leaves all 8 physiology-vs-persistence CIs strictly unfavorable to physiology.

G5 — Feature-burden objection: PASS.
POPANE-R5 finds no rescue from ECG-only, EDA-only, or ICG/hemodynamic-only families at any horizon for either learner.

G6 — Metric dependence / trajectory tracking: PASS-ROBUST under the frozen PAPER-G1 rule.
POPANE-R6 shows physiology significantly worse than persistence on RMSE and CCC at every horizon for both learners.
CASE-D2 has no CCC rescue: all 16 physiology-vs-persistence CCC differences are negative and all 16 95% CIs are strictly below zero. RMSE point estimates favor persistence in all 16 cells; 15/16 CIs are strictly negative. The sole inconclusive RMSE cell is 21 s arousal HGB (delta naive-phys = -0.05897, 95% CI [-0.14714, +0.00201]); this is not a reversal. Therefore the core point-error result is not reversed and there is no concordant-trajectory physiology rescue. D2's internal MIXED_METRIC_RESULT label reflects its stricter requirement that all 16 RMSE CIs be significantly negative.

G7 — Timing/leakage integrity: PASS.
POPANE preprocessing is confined to already-sliced historical predictor windows. Zero-phase ECG filtering cannot access target-window samples. CASE timing is likewise prospective with historical windows ending before target start.

G8 — Reproducibility/provenance: PASS.
Protocols, analysis code, workflow triggers, run IDs, aggregate artifacts, CASE versioned Figshare provenance, POPANE exact archive checksum, and a reproducibility manifest are preserved. Technical failures are explicitly documented as no-outcome and only implementation-only corrections were rerun.

G9 — Novelty boundary: PASS-BOUNDED.
The frozen bounded search reached its minimum coverage and found no DIRECT prior-art match to the exact incremental question. Backward citation tracing covered important predecessors including Taylor et al., DeepMood, Saylam & İncel, Pounds et al., EPiC/D'Amelio, and longitudinal wearable forecasting. Global “first” or “unique” claims remain forbidden because the planned scite citation-neighborhood pass was unavailable and this was not a full systematic review.

G10 — Interpretive firewall: PASS.
The defensible result is predictive/benchmarking only. It does not establish physiological irrelevance, body-independence, universal forecasting impossibility, causal persistence, or any phenomenal/consciousness conclusion.

## Defensible paper claim after this loop

Across the tested short-horizon continuous-affect forecasting settings, recent observed affect/persistence is an exceptionally strong benchmark under stringent person/stimulus generalization, and the tested peripheral-physiology representations do not provide robust prospective improvement beyond that state-history information. This pattern replicates externally for valence in POPANE and survives nonlinear models, change targets, crossed uncertainty, physiology-family ablations, RMSE, and CCC.

Important boundaries:
- POPANE external replication is valence only; arousal remains CASE-specific.
- CASE shows aligned physiology signal under its own control; POPANE-R3 does not independently replicate that signal-without-increment distinction.
- Continuous-rating/annotation dynamics may contribute to observed persistence.
- Other physiological representations, tasks, populations, and longer horizons remain open.
- Phrase the contribution as a stronger-baseline/incremental-utility benchmark, not a universal null result.

## Stop rule

No additional experiment is currently required before drafting on the basis of the objections already tested. Future analyses should require a new concrete reviewer-level objection rather than open-ended robustness accumulation.

## Manuscript-control status

Consecutive readiness decisions: 1 / 3 required.
Manuscript action: HOLD. No manuscript creation or editing authorized by this decision alone.
