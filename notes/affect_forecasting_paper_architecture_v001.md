# Affect forecasting paper architecture v001

Status: pre-manuscript architecture authorized after PAPER-G1 readiness 3/3.

## Working contribution
Strong recent-state/history baselines should be mandatory in short-horizon continuous-affect forecasting. Across CASE and POPANE Study 6, the tested peripheral-physiology representations do not provide robust incremental prospective utility beyond recent affect/context under stringent generalization; external replication is valence-only.

## Paper structure
1. Introduction
   - Separate affect detection from prospective forecasting.
   - Establish two known literatures without claiming novelty: physiology can predict affect; affect history is strongly autocorrelated/predictive.
   - Gap: incremental physiology utility after a strong observed-state/history baseline is under-tested.
   - State bounded contribution, no priority language.

2. Methods
   - CASE primary public-dataset analysis: valence + arousal; strict historical predictor windows; held-person and held-video generalization.
   - POPANE Study 6 independent replication: valence only; held-person × held-segment.
   - Baselines: persistence/recent affect and fitted context.
   - Physiology representations and Ridge/HGB.
   - Frozen post-primary attacks: change targets, crossed uncertainty, family ablation, RMSE/CCC, alignment controls.
   - Provenance and technical-failure policy.

3. Results
   - CASE primary persistence dominance/non-increment.
   - Stronger double-holdout and multi-horizon stress.
   - POPANE-R1 external valence replication.
   - Transition/change attacks: CASE-D1 mixed but no cross-model rescue; POPANE-R2 no external increment.
   - POPANE-R4 crossed uncertainty.
   - POPANE-R5 family ablation.
   - Metric/trajectory sensitivity: POPANE-R6 robust; CASE-D2 no CCC rescue and no RMSE reversal, with one inconclusive RMSE CI retained.
   - Alignment diagnostic: CASE aligned signal is CASE-specific; POPANE-R3 no detectable aligned signal.

4. Discussion
   - Main inference: tested physiology does not robustly improve short-horizon prospective prediction after strong state-history baselines in these datasets.
   - Benchmarking implication for affective computing.
   - Distinguish predictive redundancy/non-increment from physiological irrelevance.
   - Explain why persistence can dominate: true affective inertia plus possible continuous-rating/annotation dynamics.
   - External replication boundary: valence only.
   - Representation/model/horizon limits.
   - No causal or phenomenal inference.

5. Limitations
   - Continuous self-report is a measurement process, not direct phenomenality.
   - Rating inertia may inflate persistence.
   - Tested peripheral features/model families are not exhaustive.
   - POPANE arousal unavailable for replication.
   - Novelty audit bounded; no global first/unique claim.
   - Post-primary robustness analyses are labeled as such.

## Claim firewall
Forbidden:
- physiology is irrelevant to emotion;
- body-independent feelings;
- physiology can never forecast affect;
- persistence causes feeling;
- any consciousness/phenomenality conclusion;
- global first/unique novelty.

Required null preservation:
- CASE-D1 mixed result;
- POPANE-R3 non-replication of aligned-signal distinction;
- CASE-D2 MIXED_METRIC_RESULT label and one inconclusive RMSE CI.

## Next executable manuscript action
Draft Methods and Results first from immutable protocols/result snapshots, then Introduction/Discussion around the bounded claim. Do not draft from memory or chat.
