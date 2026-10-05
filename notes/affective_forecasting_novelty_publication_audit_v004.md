# Affective forecasting novelty / publication audit v004 — 2026 update

Status: bounded current-literature audit after CASE O002-D1 and POPANE-R1; POPANE-R2/R3 outcomes pending. Search date: 2026-10-05. This is NOT a formal systematic-review proof of global uniqueness.

## Core candidate contribution after current evidence

The defensible contribution is methodological/predictive-identifiability oriented:

> In continuous self-reported affect forecasting, a parameter-free observed-state persistence baseline can dominate peripheral-physiology models. Real physiological affect signal and incremental prospective forecasting utility are distinct questions. In CASE, the non-increment pattern survives multiple horizons, unseen people and stimuli, nonlinear models, and a change-target attack against zero-change; in POPANE, valence level forecasting independently reproduces strong persistence dominance across unseen participants and segments.

No claim is made that physiology is causally irrelevant, that feelings are body-independent, or that physiology never forecasts affect.

## Important 2026 predecessor: Pounds et al.

Destiny Pounds, Vibhhuti Gupta, Himanshu Tripathi, Subash Neupane.
“Forecasting Minute-by-Minute Stress, Anxiety, and Affective States Using Time-Series Analysis of Wearable Sensor Data.”
medRxiv 2026.04.29.26352047; presented/published in IEEE/ACM CHASE 2026, DOI 10.1109/CHASE69719.2026.00088.

Why it is close:
- Explicitly forecasts the upcoming minute rather than only contemporaneous recognition.
- Uses EDA and HRV from WESAD.
- Time-series models use the prior ten minutes of BOTH physiological features and past labels.
- Uses GroupKFold so participant data remain grouped across folds.
- Reports substantially better temporal-model performance than static models for affect/stress/anxiety.

Why it does not answer our incremental-information question:
- The temporal model bundles past labels and physiology; the paper does not report a past-label-only or last-observed-state persistence comparator.
- Therefore improved temporal-model performance cannot identify how much incremental forecasting value comes from physiology after conditioning on prior self-report.
- The paper’s comparison is principally time-series vs static model, not physiology increment vs observed-state persistence.
- WESAD subjective measures are collected after experimental conditions; minute-level affect targets are derived/assigned from these condition-level surveys, unlike continuously sampled self-report trajectories in CASE/POPANE.
- The target is PANAS positive/negative affect rather than moment-to-moment valence/arousal trajectories.
- Sample size is 15 WESAD participants, materially smaller than POPANE and smaller than CASE.

Publication consequence:
Pounds et al. prevents us from claiming novelty for “forecasting affect from physiology while using past labels” or for subject-grouped physiological affect forecasting. Residual novelty must be the explicit decomposition and benchmarking: **past observed affect/persistence first, physiology increment second**, with continuous self-report, multi-horizon stress, double generalization, and independent replication.

## 2026 SemEval longitudinal affect forecasting

Noor & Fatima, “Emo-tica at SemEval-2026 Task 2: Trait–State Affect Forecaster for Longitudinal Valence and Arousal,” ACL Anthology, DOI 10.18653/v1/2026.semeval-1.31.
Related 2026 longitudinal-text work likewise reports strong short-term affective inertia, with prior numeric affect state dominating next-step forecasting.

Relevance:
- Strong independent evidence that prior affect can be an exceptionally powerful forecasting source.
- Establishes that affect persistence / inertia is not novel.
- Text-based longitudinal forecasting does not test peripheral physiology or our incremental physiology question.

## 2026 VADFormer

Sujatha T et al., “A multimodal transformer system for continuous Valence-Arousal trajectory modeling and emotion forecasting,” Expert Systems with Applications (2026), DOI 10.1016/j.eswa.2026.133306.
- Integrates facial video and speech for continuous VA regression/classification/one-step forecasting.
- Demonstrates that short-term affect forecasting is an active multimodal research topic.
- Does not use peripheral physiology and is not the same conditional-increment benchmark.

Consequence:
Do not claim novelty for short-term continuous VA forecasting itself.

## EPiC remains the strongest methodological predecessor

Coles et al. 2025, Royal Society Open Science, DOI 10.1098/rsos.241778.
- 12 teams predicted self-reported valence/arousal from peripheral physiology.
- 100% of tests beat random prediction, but only 46% beat a training-mean baseline.
- Replacing physiology with random noise reduced performance in most selected-model tests, establishing real physiological signal.
- Authors explicitly identify continuity-, variability-, autocorrelation-, and subject-statistic-preserving baselines as important future benchmark directions.

Our work should be framed as directly operationalizing a stronger version of that benchmarking concern using observed-state persistence and prospective targets, not as contradicting EPiC.

## Current physiology–subjective-affect theory context

Koppold et al. 2026, Psychophysiology, DOI 10.1111/psyp.70224:
- Across two independent samples, correspondence between subjective valence/arousal and physiology depends materially on intraindividual variability.
- Supports caution against universal one-to-one physiological “fingerprints” of subjective affect.
- Does not address prospective incremental forecasting beyond persistence.

Recent 2026 physiology-decoding studies continue to show that physiological or neural signals can classify/estimate affect under many settings. These are compatible with our central distinction: **having affect-related signal does not guarantee incremental future-value utility after a strong state-history comparator is available**.

## Residual novelty after v004 pressure test

Not novel:
1. affect persistence / autoregression;
2. physiology contains affect-related information;
3. physiology-based emotion recognition;
4. subject-independent physiology models;
5. multimodal affect forecasting;
6. forecasting using physiology plus historical labels;
7. temporal/nonlinear models for continuous emotion.

Potentially distinct combined contribution:
1. strict future windows separated from predictor windows;
2. parameter-free observed last-state persistence as first-class baseline;
3. direct physiology incremental-value test after persistence/context;
4. real-vs-shifted physiology alignment control (CASE; POPANE-R3 pending);
5. multi-horizon 1/11/21/31 s evaluation;
6. simultaneous unseen-person × unseen-stimulus/segment evaluation;
7. model-class robustness rather than a single favored learner;
8. independent external valence replication in POPANE;
9. explicit level-vs-change target attack (CASE D1; POPANE-R2 pending);
10. preservation of the distinction between physiological signal, incremental information, and causal/phenomenal interpretation.

## Publication status

Current classification: SERIOUS PAPER CANDIDATE, NOT YET MANUSCRIPT-READY.

What can still materially change the paper:
- POPANE-R2: whether physiology robustly predicts future valence changes beyond context/zero-change.
- POPANE-R3: whether the same external physiology features show genuine temporal alignment with recent valence.
- A final reproducibility/statistical audit, including exact participant/segment support, bootstrap unit justification, multiplicity language, sensitivity to MAE vs alternative proper point metrics, and transparent post-primary labeling.
- Formalized literature search protocol before any strong “first” or “novel” wording.

Recommended novelty wording if current pattern survives:
“we provide a replicated benchmark demonstration” / “we test an underexamined distinction” rather than “the first study” unless a formal systematic search later supports priority.

Forbidden wording:
“physiology is irrelevant to feelings,” “the body does not matter,” “physiology cannot predict emotion,” or any consciousness/phenomenality claim.
