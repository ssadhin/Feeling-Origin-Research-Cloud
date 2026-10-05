# PAPER-G1 Frozen manuscript-readiness gate

Freeze date: 2026-10-05
Status: FROZEN BEFORE POPANE-R6 AND CASE-O002-D2 OUTCOMES

This gate decides whether the current affect-forecasting evidence is scientifically mature enough to begin manuscript drafting. It does NOT authorize manuscript edits by itself. Project rule remains: manuscript changes require three consecutive research-loop paper decisions to agree.

## Candidate claim under evaluation

Across the tested public continuous-self-report datasets and short prospective horizons, recent observed affect/persistence is a stronger general-purpose forecaster than the tested peripheral-physiology representations under stringent person/stimulus generalization. Peripheral physiology should be evaluated for incremental prospective utility after strong state-history baselines, not merely against weak random/mean baselines.

The external replication claim is VALENCE ONLY. CASE includes valence and arousal; POPANE Study 6 supplies valence.

The stronger statement “real physiology contains aligned affect signal but still adds no future utility” is CASE-specific unless independently replicated elsewhere; POPANE-R3 did not detect aligned valence signal.

## Required gates

### G1 — Primary empirical result
PASS if the frozen CASE/O002 primary prospective result is complete and preserved with strict predictor/target separation and double held-person × held-video evaluation.

### G2 — Independent external replication
PASS if POPANE-R1 independently shows non-increment/persistence dominance for valence with different participants, elicitation segments, signals/features and model classes.

### G3 — Strongest alternative explanation: transition prediction
PASS if future-change analyses do not produce a model-class-robust physiology rescue.
- CASE-D1 may be mixed/model-specific, but no robust rescue.
- POPANE-R2 must show no external robust change increment.

### G4 — Generalization-axis uncertainty
PASS if persistence dominance survives a sensitivity that resamples both held-person and held-segment axes in POPANE.

### G5 — Feature-burden objection
PASS if pre-authorized ECG-only, EDA-only and ICG/hemodynamic family screens do not yield a model-class-robust physiology rescue.

### G6 — Metric dependence / trajectory tracking
PASS-ROBUST if neither POPANE-R6 nor CASE-D2 yields a model-class-robust physiology-vs-persistence CCC rescue and RMSE does not reverse the core point-error result.
PASS-NARROWED if CCC shows a robust physiology tracking advantage while MAE/RMSE remain worse; manuscript must explicitly distinguish absolute-error forecasting from concordant trajectory tracking.
FAIL/PENDING if results conflict so strongly that a coherent bounded claim cannot yet be stated without another confirmatory analysis.

### G7 — Target leakage / timing integrity
PASS if predictor windows are strictly historical and preprocessing is confined to the historical slice. Zero-phase filtering inside a completed historical window is allowed but must be disclosed as retrospective-window processing rather than streaming-causal filtering.

### G8 — Reproducibility/provenance
PASS if frozen protocols/code/trigger commits, immutable aggregate artifacts/results, public dataset source, and the exact POPANE Study 6 archive checksum are preserved.

### G9 — Novelty boundary
PASS-BOUNDED if a frozen literature screen reaches its prespecified minimum coverage and finds no DIRECT prior-art match to the exact incremental question.
Global “first”/“unique” language remains forbidden unless a fuller database/citation-neighborhood search later supports it.

### G10 — Interpretive firewall
PASS only if the manuscript claim explicitly does NOT infer:
- physiology is irrelevant to emotion;
- feelings are body-independent;
- peripheral physiology never forecasts affect;
- persistence is the causal generator of feeling;
- phenomenal/consciousness conclusions.

## Loop decision rules

PAPER_READY_FOR_DRAFTING:
- G1–G5, G7–G10 pass; and
- G6 is PASS-ROBUST or PASS-NARROWED with a coherent revised claim; and
- all technical failures are documented as no-outcome and only implementation-only fixes were rerun.

PAPER_CANDIDATE_NEEDS_MORE_TESTING:
- any required gate is unresolved or G6 is materially mixed.

NOT_A_DEFENSIBLE_PAPER:
- external replication fails in the direction required for the core claim, a direct prior-art match collapses the contribution, leakage invalidates the primary test, or the only defensible wording becomes trivial.

## Manuscript-control rule

Even if this loop returns PAPER_READY_FOR_DRAFTING, record it as one loop decision only. Do not modify/create the manuscript until three consecutive research-loop paper-readiness decisions agree, unless the user explicitly overrides that rule.
