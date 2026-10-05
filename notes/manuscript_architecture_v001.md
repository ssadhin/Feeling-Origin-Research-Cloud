# Manuscript architecture v001 — conditional on MANUSCRIPT-GATE-01

Working title:
**Persistence before physiology: strong recent-state baselines reshape prospective affect prediction from peripheral signals**

Alternative:
**Real physiological signal, limited incremental forecast: benchmarking continuous affect prediction against recent-state persistence**

## One-sentence paper question
When forecasting continuous self-reported affect, do peripheral physiological signals add prospective predictive information beyond a strong parameter-free recent-state persistence benchmark under strict person and stimulus generalization?

## Contribution boundaries
This is a benchmarking / predictive-identifiability paper.
It is NOT a claim that physiology is irrelevant to emotion, that affect is body-independent, or that self-report persistence causes feeling.

## Abstract structure
1. Motivation: physiology-based affect models are often evaluated against random or mean baselines, while continuous affect is strongly temporally dependent.
2. Gap: incremental utility beyond observed recent affect under strict person/stimulus generalization is rarely tested.
3. CASE methods: continuous valence/arousal; physiology [-10,-1] s; recent self-report mean [-5,-1) s; future target [0,5] s and 11/21/31 s extensions; double holdout.
4. CASE result: recent-state persistence dominates context; physiology provides no positive level-forecast increment.
5. External POPANE: independent valence dataset, 186 usable participants, 18 segments, Ridge + HGB; strong baseline dominance at all four horizons.
6. Dynamic attack placeholder: [insert O002-D1 + POPANE-R2 classification exactly].
7. Signal-validity placeholder: [insert POPANE-P1].
8. Conclusion: benchmark choice changes inference; real affect-related physiology need not imply incremental prospective utility conditional on recent state.

## Introduction

### 1. Why physiology prediction matters
- Peripheral physiology is widely used to infer affective experience.
- Practical and theoretical appeal: objective sensing, continuous measurement, multimodal emotion AI.

### 2. The benchmark problem
- EPiC / Coles et al. 2025: all teams beat random; only 46% beat a training-mean baseline.
- EPiC explicitly calls for continuity/autocorrelation-preserving baselines.
- Dense affect reports have temporal dependence / affective inertia.

### 3. Prior affect integration is prior art
- Asutay et al. “Affective calculus”: current affect integrates prior affect, stimuli and physiology.
- Affective-inertia and computational affect-dynamics literature.
- Therefore our novelty is not “prior affect matters” and not “physiology + prior affect can be modeled.”

### 4. Specific gap
- Prospective future-window prediction.
- Observed recent-state persistence as parameter-free benchmark.
- Incremental physiology above that benchmark.
- Simultaneous unseen person + unseen stimulus.
- Horizon stress.
- Independent external replication.

### 5. Hypothesis framing
Avoid directional theoretical claims about embodiment.
Primary predictive question: whether physiology reduces out-of-sample MAE conditional on recent state/context.

## Methods

### Dataset 1: CASE
- 30 subjects × 8 emotional videos.
- Continuous valence/arousal and synchronized peripheral physiology.
- Cite canonical dataset.
- Frozen feature extraction:
  - physiology [-10,-1] s;
  - recent report mean [-5,-1) s;
  - target mean [0,5] s;
  - anchors 10 s apart.
- Exact 29 physiology features.
- No predictor/target overlap.

### CASE models
- Context/time.
- Context + recent-state report.
- Context + recent-state + physiology.
- Parameter-free persistence: target_hat = recent-state mean.
- Ridge; HGB only in post-primary change attack.
- Training-only imputation/scaling/tuning.

### CASE evaluation
- G1 simultaneous held subject × held video.
- Crossed subject×video bootstrap.
- G2 11/21/31 s future targets.
- B1/B2/B3 simple-baseline reconciliations labeled post-primary.
- D1 future-change target explicitly labeled exploratory/post-primary.

### Dataset 2: POPANE Study 6
- Public CC BY-NC 4.0.
- Published N=187; 186 technically usable in R1.
- Continuous valence + ECG/EDA/ICG/hemodynamic signals.
- 18 eligible named affect segments.
- Same predictor/target timing and horizons where possible.
- 10 deterministic held-person folds crossed with held-segment label.
- Ridge + HistGradientBoosting.
- Participant-cluster bootstrap.
- Raw data transient; aggregate outputs only.

### POPANE positive control
- P1 alignment test: aligned physiology vs within-person×segment circular temporal shift for concurrent/recent affect.
- Explicitly not prospective evidence.

### Outcomes
Primary utility metric: MAE and paired MAE difference.
Sign convention clearly stated.
Do not use correlation/CCC to override MAE decisions.

## Results

### R1. Real physiology is affect-related in CASE
- Summarize frozen shifted-physiology positive control.
- Establish distinction between signal presence and incremental forecast value.

### R2. Recent-state persistence is an unusually strong prospective benchmark in CASE
- G1 context vs recent-state effect for valence/arousal.
- B1 parameter-free persistence.
- State accurately that baseline is the mean report over [-5,-1), not literal last sample.

### R3. Physiology does not improve CASE level forecasts under double holdout
- G1 deltas + crossed bootstrap.
- Avoid “no information”; say no incremental MAE utility conditional on tested baseline/model.

### R4. Result survives longer horizons
- G2 11/21/31 s.
- Plot baseline and physiology MAE by horizon.
- Emphasize valence consistent degradation; arousal nonpositive/inconclusive at longer horizons.

### R5. Independent POPANE valence replication
- 8,919 rows, 186 participants, 18 segments.
- Ridge + HGB.
- All four horizons: naive recent-state persistence lower MAE than physiology, CIs strictly negative for naive−phys.
- Physiology also worse than fitted prior/context models.

### R6. Future-change adversarial test
- Placeholder pending O002-D1 and POPANE-R2.
- If positive: explicitly narrow level conclusion.
- If nonpositive: state strongest transition rescue was not supported, while retaining exploratory label.

### R7. POPANE signal-validity control
- Placeholder pending P1.
- If valid: supports “real/aligned signal can coexist with negative incremental forecast.”
- If weak: soften external mechanistic interpretation; baseline-dominance result remains.

## Figures

Figure 1 — Design and information firewall
- Timeline: physiology [-10,-1], recent report [-5,-1), target [0,5].
- Horizon targets +10/+20/+30 s.
- Double holdout schematic.
- Distinguish signal detection vs incremental forecasting.

Figure 2 — CASE
- Panel A: context, recent-state, physiology MAE at 1 s.
- Panel B: naive persistence vs fitted prior vs physiology over 1/11/21/31 s.
- Panel C: physiology increment CIs by horizon/axis.

Figure 3 — POPANE external replication
- Ridge/HGB MAE curves across horizons.
- Participant-cluster delta naive−phys CIs.
- Clear dataset distinction from CASE.

Figure 4 — Change-target + signal-validity
- Change-target deltas across datasets.
- P1 real-vs-shifted physiology alignment control.
- Conceptual quadrant: signal present? incremental utility present?

## Discussion

### Main conclusion
Benchmark choice fundamentally changes the interpretation of physiology-based continuous-affect prediction.

### Signal ≠ incremental utility
Use CASE shifted control + [POPANE-P1 pending].
A physiological measure can contain affect-related information while adding no useful forecast once recent affect is observed.

### Generalization
Person novelty and stimulus novelty are multiplicative constraints.
Tie directly to EPiC.

### Why persistence is strong
Possible sources:
- genuine affective inertia;
- continuous rating dynamics / motor smoothing;
- stimulus continuity;
- slow latent affect dynamics.
Do NOT identify one as causal from these data.

### What physiology may still do
- predict affect without access to self-report;
- predict different timescales;
- predict specific transitions or contexts;
- improve other metrics/tasks;
- encode causal bodily processes despite no conditional MAE gain.

### Limitations
- short horizons only (1–31 s).
- recent self-report is unavailable in many deployment settings.
- POPANE external replication valence only.
- tested feature/model families do not exhaust physiology.
- continuous self-report measurement dynamics.
- observational data.
- post-primary nature of B-series, D1/R2/P1.
- bounded novelty screen; unavailable Scite/Elicit API prevents claiming exhaustive systematic search.

## Conclusion wording target
“Peripheral physiology can carry affect-related signal without necessarily providing incremental short-horizon forecasting utility once recent reported affect is known. In two continuous-affect datasets, a simple recent-state persistence benchmark proved harder to beat than substantially richer physiological models under strict generalization. These findings argue for stronger temporal baselines and explicit conditional-information tests in affective computing.”

## Claims forbidden in title/abstract/discussion
- “physiology does not matter for emotion”
- “feelings are independent of the body”
- “physiology cannot predict affect”
- “self-report causes future affect”
- any consciousness/phenomenal conclusion
