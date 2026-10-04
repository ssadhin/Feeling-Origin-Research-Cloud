# Virtual Organism v014 — Frozen Confirmatory Protocol

Date: 2026-10-04
Program: Feeling Origin / Artificial Consciousness Research
Status: PRECOMMITTED BEFORE CONFIRMATORY HELD-OUT RUN

## Purpose

Test whether the current CRFI functional architecture produces post-event organism consequences that simpler topology-distinct recurrent/homeostatic rivals cannot reproduce, while explicitly preventing an immediate-reaction mismatch from being counted as evidence.

This simulation tests functional and causal architecture only. It must not be interpreted as proof of subjective feeling or phenomenal consciousness.

## Frozen implementation

- Simulator commit: 5fc180888777eaab28467945752da04ac013980b
- Cloud runner commit: 923364e8ad1100e5cbbe509131cb9027a99dabc7
- Workflow commit: ed027385982ac1a22d3367ca78a3b250b65c7b62
- Simulator: simulations/virtual_organism_v014.py
- Runner: cloud/run_organism.py
- Workflow: .github/workflows/research-compute.yml

No code or threshold changes are permitted after inspecting the confirmatory seed block if the result is to be called confirmatory.

## Development and confirmatory split

Development worlds:
- seeds 0..39
- allowed for rival tuning
- 30 random rival parameter candidates

Confirmatory worlds:
- exactly 120 worlds
- seed block 50000..50119
- these seeds have not been inspected in development pilots

## Organism

Regulated body variables:
- energy
- hydration
- temperature
- physical integrity

Environment:
- 19x19 stochastic ecology
- food
- water
- hot/cold locations
- hazard patch
- irrelevant distractor field
- standardized forced hazard exposure
- later hazard removal/resource reversal

No emotion category labels such as fear, happiness, sadness, or relief are programmed into the organism.

The appraisal vector is defined only from viability-relevant geometry:
- deterioration risk
- restoration opportunity
- controllability
- uncertainty

## Architectures

Primary clean rivals:
1. reactive
2. homeostatic learning
3. appraisal
4. recurrent downstream only
5. gated recurrent downstream only
6. gated recurrent + learning modulation, with no direct domain-to-content feedback
7. CRFI no-C
8. CRFI no-L
9. tuned gated-learning rival

Near-neighbor:
- tuned generic bidirectional recurrent system

The generic bidirectional recurrent system is NOT automatically a clean non-CRFI rival because direct E<->S reciprocity may place it inside the physical core of CRFI. If it matches CRFI, interpret that as pressure on CRFI-specific admission/selectivity, not automatically as a refutation of recurrence/embedding itself.

## Primary signature metrics

1. escape — immediate escape latency after standardized hazard exposure
2. post_hazard_visits — later visits to the old hazard zone after the event
3. reversal_latency — latency to re-approach after the hazard is removed and the site becomes useful
4. recovery_auc — post-event physiological dysregulation area
5. q_change — post-event learning/plasticity change

final_drive and survival are descriptive secondary metrics.

## Frozen validity rule

Immediate reaction is a confound-control, not a success metric.

For a rival comparison to be valid:
- |Cohen d| for escape must be < 0.20.

If escape is not matched:
- classify the comparison as CONFOUNDED_IMMEDIATE_MISMATCH.
- do not count it as evidence that CRFI wins.

## Frozen behavioral uniqueness kill condition

A topology-distinct rival defeats CRFI behavioral uniqueness if:
- immediate escape is matched: |d_escape| < 0.20
AND
- all four post-event metrics are equivalent:
  - |d_post_hazard_visits| < 0.20
  - |d_reversal_latency| < 0.20
  - |d_recovery_auc| < 0.20
  - |d_q_change| < 0.20

If any clean rival meets this condition on the confirmatory block:
- behavioral_uniqueness_verdict = FAIL
- CRFI must not claim a unique behavioral signature from this experiment.

If no clean rival defeats uniqueness, but at least one clean rival has matched immediate escape and a non-equivalent post-event signature:
- behavioral_uniqueness_verdict = SURVIVES_MATCHED_RIVALS_V014

If no serious rival achieves matched immediate escape:
- result is INCONCLUSIVE_NO_MATCHED_RIVAL, not a CRFI victory.

## Causal-topology diagnostic

The simulator additionally reports local intervention signatures:
- E_to_S
- S_to_E
- reciprocal = E_to_S * S_to_E

These are topology diagnostics, not independent proof of consciousness.

The key structural question is whether post-event effects require direct local reciprocal content<->domain causation or can be reproduced by a recurrent/gated system that only modulates downstream policy and learning.

## Development warning already observed

Small development pilots suggested that a gated recurrent learning-modulation rival can sometimes closely match CRFI behavior without direct local S->E feedback. This is why that rival was promoted into the primary adversarial set before the confirmatory run.

That observation is development-only and must not be treated as the confirmatory result.

## Interpretation firewall

Possible outcomes:
- FAIL: a clean rival matches the full signature under the validity gate.
- SURVIVES_MATCHED_RIVALS_V014: valid matched rivals fail at least one post-event signature.
- INCONCLUSIVE: immediate matching fails or the environment does not produce discriminating variation.

None of these outcomes establish actual subjective feeling.

The larger CRFI identity claim remains a separate question from whether this virtual organism has a unique functional signature.
