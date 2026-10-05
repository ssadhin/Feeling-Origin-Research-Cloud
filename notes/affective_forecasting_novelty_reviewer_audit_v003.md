# Affective forecasting novelty / reviewer-risk audit v003

Status: post-POPANE-R1, pre-O002-D1 outcome. Bounded literature audit current through 2026-10-05. This is not a systematic-review claim of uniqueness.

## Result now requiring literature placement

Two independent continuous self-report datasets show that simple recent-state persistence is an exceptionally strong prospective benchmark. In CASE, peripheral physiology contains real aligned affect signal but does not improve future valence/arousal level prediction beyond recent self-report/context under simultaneous unseen-person × unseen-stimulus evaluation and 1/11/21/31 s gaps. In POPANE Study 6, the valence level result externally replicates across 186 usable participants and 18 held-out segment labels, with both Ridge and nonlinear HGB physiology models significantly worse than naive persistence at all four horizons.

## Closest prior art and pressure tests

### Coles et al. 2025 — EPiC big-team science, Royal Society Open Science
DOI: 10.1098/rsos.241778.
- Twelve teams predicted self-reported valence/arousal from peripheral nervous system measures.
- Models were evaluated across participants, targeted emotions, inductions, and time.
- Every team beat a random baseline, but only 46% of tests beat a training-mean baseline.
- Replacing physiology with simulated randomness reduced accuracy in 93% of selected-model tests, showing that real physiology genuinely carried usable affect information.
- Crucially, the paper explicitly says future baselines should preserve continuity, temporal variability, autocorrelation, or subject-specific first-order statistics.
- This is the strongest conceptual predecessor and supports our benchmark motivation.
- It does NOT report the specific prospective comparison against observed recent self-report / last-state persistence that our analyses target.

### Autoregressive multimodal continuous-emotion models (e.g. Ulm-TSST Transformer work, arXiv:2311.10119 and subsequent versions)
- These models explicitly use temporal/autoregressive structure and multimodal inputs.
- Autoregression is based on past model states/predictions, not an explicit parameter-free observed last-self-report benchmark.
- Their task is principally time-continuous recognition/estimation aligned with contemporaneous annotations, rather than our strictly future target windows.
- Removing physiology produces very small/no significant valence degradation in reported experiments, while audio/video matter more, which is directionally compatible with limited incremental physiology utility for valence.
- This work means we must not claim novelty for using temporal/autoregressive information itself.

### RECOLA physiology prediction literature
- Ringeval et al. used speaker-disjoint train/dev/test partitions and found ECG/EDA-only continuous valence/arousal performance relatively low; multimodal context improved prediction.
- Joudeh et al. 2022/2023 reported extremely high ECG+EDA performance (~0.995 CCC), but their pipeline describes shuffling data records and an 80/20 split across samples from 18 subjects rather than a speaker-disjoint prospective forecast, and does not compare against persistence/lagged-label baselines.
- Therefore high concurrent physiology accuracy in that line of work is not commensurate with our generalization/forecasting question. Do not call it invalid; call the evaluation target and split non-equivalent.

### Affective inertia / dynamic affect literature
- Prior affect strongly predicts subsequent affect; autoregressive persistence is well established and therefore not novel.
- Our contribution cannot be “affect persists.” The contribution, if it survives the change-target attack, is that this trivial persistence benchmark can dominate considerably more elaborate peripheral-physiology predictors in prospective continuous-affect forecasting, even while real physiology contains affect-related signal.

### Physiological dynamics / NARX / longitudinal wearable work
- Papers exist showing physiology can predict dynamic emotion intensity or future mood under specific settings and can exhibit temporal instability across months.
- These prevent any universal claim that physiology has no forecasting value.
- Our claim must be conditional on continuous affect level forecasting, the tested short horizons, datasets, peripheral channels/features, and generalization regimes.

## Residual novelty that appears defensible after bounded search

Potential paper contribution is the combined methodological demonstration:
1. Real peripheral physiology can carry demonstrable affect-related information yet still have zero/negative incremental prospective utility once a strong observed-state persistence baseline is used.
2. The finding is evaluated against a parameter-free last-state baseline rather than random or training-mean baselines.
3. It survives longer 1/11/21/31 s horizons.
4. It survives simultaneous unseen-person × unseen-stimulus/segment evaluation.
5. It survives model-class change (linear Ridge and nonlinear HGB in independent POPANE).
6. It externally replicates for valence in a different public dataset, with different tasks, signals and feature extraction.
7. The work explicitly distinguishes “physiology contains signal” from “physiology adds predictive information conditional on a strong baseline.”

No global uniqueness claim is justified until a formal systematic search is completed.

## Strongest remaining reviewer objection

The paper currently predicts absolute affect LEVEL. Because continuous ratings are temporally smooth, persistence can dominate by construction. Physiology might still predict TRANSITIONS or deviations from the persistence forecast. That is why O002-D1 was frozen post-primary before inspecting future-change outcomes. A fair change target is:
delta = future affect - recent pre-anchor affect,
with zero-change as the trivial baseline and prior level/time as context. Adding physiology must improve this change prediction under the same double holdout to rescue a meaningful dynamic physiology contribution.

If D1 shows a positive change increment, the manuscript must narrow from “physiology adds no prospective utility” to “physiology adds no level-forecast utility but may help predict changes.” The positive change result must then be independently replicated in POPANE.
If D1 is nonpositive, run the same POPANE change-target test before manuscript-ready classification.

## Current manuscript framing

Best working title direction:
“Persistence before physiology: strong autoregressive baselines reshape prospective affect prediction from peripheral signals”

Best contribution type:
benchmarking / predictive identifiability / evaluation methodology, not a theory of consciousness or bodily irrelevance.

Forbidden claims:
- physiology is irrelevant to emotion;
- emotions are independent of the body;
- peripheral physiology never forecasts affect;
- self-report persistence is the causal generator of feeling;
- the results establish phenomenal or consciousness conclusions.
