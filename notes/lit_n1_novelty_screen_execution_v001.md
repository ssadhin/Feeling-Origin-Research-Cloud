# LIT-N1 novelty screen — execution checkpoint v001

Protocol: protocols/lit_n1_novelty_search_protocol.md
Protocol commit: 76358be72f9a4874b88e6afb29b91ae8e3774583
Search date: 2026-10-05
Status: BOUNDED SEARCH EXECUTED; NOT A SYSTEMATIC-REVIEW CLAIM OF GLOBAL PRIORITY.

## Search execution

The frozen LIT-N1 search families were run through the connected Exa academic/web index with category-targeted research-paper queries plus direct follow-up searches on close candidates.

Formal pass reviewed at least 68 ranked candidate slots across six search queries (4 × 12 broad-family results + 2 × 10 direct-prior-art follow-ups), before deduplication. Additional targeted searches were run earlier on named close predecessors.

Planned scite execution was unavailable because the connected scite MCP requires a paid plan/free trial. This limitation is recorded rather than silently replaced. Citation-neighborhood completeness is therefore not established.

## Frozen DIRECT prior-art criterion

A paper counts as DIRECT only if it:
1. predicts a future human subjective affect/emotion/mood outcome;
2. uses peripheral physiology/wearable physiological input;
3. uses observed prior subjective affect/labels or equivalent persistence information; AND
4. explicitly compares physiology against a prior-affect-only / last-value-persistence baseline or otherwise identifies the incremental predictive value of physiology after conditioning on prior affect.

No screened paper has yet satisfied all four conditions.

## Closest retained predecessors

### Saylam & İncel 2023 — Sensors
“Quantifying Digital Biomarkers for Well-Being: Stress, Anxiety, Positive and Negative Affect via Wearable Devices and Their Time-Based Predictions.”
DOI: 10.3390/s23218987.
Classification: CLOSE, NOT DIRECT.
- Tesserae office-worker data; next-day and longer-horizon prediction of stress/anxiety/positive affect/negative affect.
- Time-based models incorporate previous records of well-being factors and wearable-derived biomarkers.
- Temporal LSTM improves over conventional/non-time-based models.
- The reported comparison is time-based versus conventional model configurations, not an explicit prior-affect-only/persistence model versus prior-affect+physiology nested comparison.
- Therefore it shows the usefulness of historical affect and wearable context together, but does not identify physiology’s incremental value conditional on prior affect.

### Pounds et al. 2026 — CHASE / medRxiv
“Forecasting Minute-by-Minute Stress, Anxiety, and Affective States Using Time-Series Analysis of Wearable Sensor Data.”
Published at IEEE/ACM CHASE 2026; medRxiv DOI 10.64898/2026.04.29.26352047; conference DOI reported as 10.1109/CHASE69719.2026.00088.
Classification: CLOSE, NOT DIRECT.
- WESAD, 15 participants.
- Time-series models use 10 minutes of past physiology AND past labels to forecast the upcoming minute.
- GroupKFold keeps participants separated.
- Static-vs-time-series comparison shows temporal models outperform static models.
- No reported past-label-only or last-observation persistence comparator; therefore the contribution of physiology after conditioning on labels is not identified.
- Affect labels are PANAS scores collected after conditions and mapped to minute-level records, not continuously sampled subjective trajectories.

### D’Amelio et al. 2023 — ACIIW / EPiC CASE
“Affective Computing as a Tool for Understanding Emotion Dynamics from Physiology: A Predictive Modeling Study of Arousal and Valence.”
IEEE ACIIW 2023, document 10388155; DOI 10.1109/ACIIW59127.2023.10388155.
Classification: CLOSE, NOT DIRECT.
- Uses CASE continuous self-report and physiology.
- Explores past/present/future physiological windows and EPiC across-time/across-subject/across-elicitor/across-version scenarios.
- Reports that past physiology can be more informative than future physiology and beats a constant/dummy baseline in some scenarios.
- Does not use observed prior self-reported affect as a persistence comparator or test physiology increment beyond prior affect.
- This paper is especially important because it prevents novelty claims about using CASE, continuous labels, temporal physiology windows, or generalization scenarios themselves.

### Coles et al. 2025 — EPiC big-team science
Royal Society Open Science, DOI 10.1098/rsos.241778.
Classification: METHODOLOGICAL PREDECESSOR.
- Multiple teams predict self-reported affect from peripheral physiology.
- Random baselines are too weak; training-mean baselines eliminate many apparent wins.
- Explicitly motivates future baselines preserving continuity/autocorrelation/subject statistics.
- Does not itself implement the observed last-state persistence comparison central to our work.
- Our paper should be framed as operationalizing this stronger-baseline concern prospectively, not as contradicting EPiC.

### Barradas et al. 2025 — dynamic physiology / NARX
DOI: 10.1371/journal.pone.0315929.
Classification: COUNTEREXAMPLE / CLOSE CONTEXT.
- Demonstrates that dynamic physiological models can successfully track/predict emotion intensity in a setting that incorporates temporal subjective information.
- Prevents universal statements that physiology cannot contribute to affect dynamics.
- Does not establish the exact incremental prospective comparison under our persistence benchmark/generalization regime.

### Berkemeier et al. 2024 — IEEE Transactions on Affective Computing
“Measuring Affective State: Subject-Dependent and -Independent Prediction Based on Longitudinal Multimodal Sensing.”
DOI: 10.1109/TAFFC.2024.3474098.
Classification: CONTEXTUAL/CLOSE.
- Longitudinal daily-life self-reported valence/arousal with wearable physiology/behavior.
- Contrasts subject-dependent and LOSO subject-independent models.
- Uses same-day predictors for same-day affect rather than the exact strict future-window incremental question.
- Does not report a prior-affect persistence ablation.

### Objective next-day affect from wearables — 2023 longitudinal ZotCare study
Classification: CLOSE, NOT DIRECT.
- Predicts next-day positive/negative affect from wearable physiological/behavioral features.
- Explicitly emphasizes prediction without individual historical information/temporal context.
- Therefore it is forecasting prior art but not prior-affect-conditioned incremental-physiology prior art.

### 2026 longitudinal text forecasting / SemEval
Classification: CONCEPTUAL/METHODOLOGICAL PREDECESSOR.
- Strong prior-state / affective-inertia baselines dominate short-term forecasting.
- No peripheral physiology.
- Reinforces that affect persistence itself is not novel.

## Bounded novelty conclusion

No DIRECT prior-art match was found in the executed bounded search.

What remains plausibly distinctive is the combined evaluation question:
- strict future continuous/dense self-report targets;
- observed recent affect/persistence as a first-class parameter-free baseline;
- explicit physiology increment after persistence/context;
- simultaneous held-person × held-stimulus/segment evaluation;
- multi-horizon stress;
- linear + nonlinear model robustness;
- level and future-change targets;
- external replication of the non-increment/persistence-dominance result;
- crossed participant×segment uncertainty sensitivity.

## Important novelty limits

Do NOT claim novelty for:
- affect forecasting;
- physiology-based affect prediction;
- using lagged labels;
- autoregressive affect models;
- continuous valence/arousal prediction;
- subject-independent validation;
- CASE forecasting/generalization;
- temporal physiology features;
- the fact that affect is persistent.

Permitted language after this bounded screen:
- “we found no prior study in our bounded search that directly tested…”
- “we provide a replicated benchmark demonstration of…”
- “we examine an under-tested distinction between physiological signal and incremental prospective utility…”

Not permitted yet:
- “the first study to…”
- “unique in the literature”
- any global-priority statement.

## Remaining literature limitation

The frozen protocol requested a scite citation-neighborhood pass around EPiC, Pounds, and Barradas. The connected scite tool was unavailable because the account lacks an active paid/free-trial entitlement. Until that citation-neighborhood step or an equivalent formal database search is completed, global novelty remains unproven.
