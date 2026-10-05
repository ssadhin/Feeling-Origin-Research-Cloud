# LIT-N1 partial execution + novelty audit v005

Status: PARTIAL FORMAL EXECUTION. Frozen protocol commit: 76358be72f9a4874b88e6afb29b91ae8e3774583.
Search date: 2026-10-05.

## Search-source limitation
The frozen protocol named scite as the primary academic index. scite MCP could not be executed because the connected account lacks the required paid/trial access. This limitation was discovered only after the protocol was frozen. The frozen search families were then executed through available Exa/web academic search without changing the research question or inclusion criteria.

Consequence: LIT-N1 is NOT a completed systematic novelty review under its original source rule. No "first study" or global uniqueness wording is authorized. The strongest defensible wording remains: "in our bounded search, we found no prior study matching the full evaluation contract."

## Most important newly screened predecessors

### D'Amelio et al. 2023 — CLOSE PRIOR ART
Tomás A. D'Amelio, Nicolás M. Bruno, Leandro A. Bugnon, Federico Zamberlan, Enzo Tagliazucchi.
“Affective Computing as a Tool for Understanding Emotion Dynamics from Physiology: A Predictive Modeling Study of Arousal and Valence.”
ACIIW 2023. DOI: 10.1109/ACIIW59127.2023.10388155.

Overlap:
- Uses the CASE dataset with continuous participant joystick valence/arousal.
- Physiological prediction of continuous affect.
- EPiC test scenarios include across-time, across-subject, across-elicitor and across-version generalization.
- Explicitly studies temporal windows and reports that past physiological features can be more informative than future physiological features.

Why not DIRECT under LIT-N1:
- The predictor is physiology-derived features; observed prior self-reported valence/arousal is not used as a persistence comparator.
- It does not isolate physiology's incremental forecasting value conditional on the participant's recent observed affect.
- Its temporal-analysis question is therefore different from the present baseline-decomposition question.

Novelty consequence:
Do not claim novelty for continuous CASE prediction, temporal physiology, subject generalization, elicitor generalization, or the idea that past physiology relates to later annotation. The distinct piece is conditioning prospective forecasting on observed recent affect and testing whether physiology adds incremental information.

### Beatton et al. 2024 — CLOSE / CONCEPTUAL PRIOR ART
Tony Beatton et al.
“Positive affect and heart rate variability: a dynamic analysis.”
Scientific Reports 14, 7004 (2024). DOI: 10.1038/s41598-024-57279-5.

Overlap:
- >300 individuals over 24 hours, ~5,000 activities, HRV plus self-reported positive feelings.
- Dynamic activity-level analyses.
- The paper reports that the last activity's reported feeling strongly correlates with current positive feeling.
- When past positive feeling is controlled, the current LF/HF association with current feeling becomes statistically weak / insignificant at conventional 5% level.

Why not DIRECT under LIT-N1:
- This is explanatory/activity-level regression rather than strict out-of-sample short-horizon forecasting.
- HRV and the outcome are largely contemporaneous at the current activity rather than separated predictor/target windows.
- No held-out-person forecasting benchmark against a parameter-free recent-state persistence predictor.
- No joint held-person × held-stimulus generalization.
- No multi-horizon prospective error comparison.

Novelty consequence:
The conceptual idea "prior feeling can absorb physiology–feeling association" is NOT novel. The paper must frame its contribution as a predictive benchmark/generalization demonstration.

### Pounds et al. 2026 — CLOSE FORECASTING PRIOR ART
“Forecasting Minute-by-Minute Stress, Anxiety, and Affective States Using Time-Series Analysis of Wearable Sensor Data.”
medRxiv DOI: 10.64898/2026.04.29.26352047; CHASE 2026 DOI: 10.1109/CHASE69719.2026.00088.

Overlap:
- Explicit next-minute forecasting.
- ECG/EDA-derived features.
- Time-series models use ten minutes of past physiology plus past labels.
- Participant-grouped cross-validation.

Why not DIRECT:
- Does not report a past-label-only / persistence-only model against the combined physiology+past-label model.
- Hence physiology's incremental value conditional on past labels is not identified.
- WESAD affect labels are condition-level survey-derived rather than continuously sampled participant trajectories.

### Longitudinal affect / wearable studies — CONTEXTUAL
Search also identified:
- next-day/week-ahead wearable affect forecasting;
- sleep/circadian predictors of later mood;
- HRV/mental-health cross-lag studies;
- longitudinal text forecasting with strong prior-state baselines.

These establish that objective data beyond affect history can predict later mood in some domains/timescales, and that affect-history baselines are increasingly recognized. They prevent broad claims that physiology or wearable information lacks forecasting value in general.

## Direct-prior-art screen status

No retrieved study so far matches ALL of:
1. continuous/dense OWN subjective valence/arousal trajectory;
2. physiology measured strictly before future target;
3. observed recent subjective affect / persistence baseline;
4. direct physiology increment above that baseline;
5. participant-independent evaluation;
6. stimulus/segment-independent evaluation;
7. multiple short forecast horizons;
8. replicated in an independent dataset.

However, because scite could not be executed, this is a bounded-search statement only.

## Revised novelty claim

The paper must NOT claim novelty for:
- affect persistence;
- physiology–affect association;
- physiology-based continuous affect prediction;
- temporal physiology on CASE;
- subject/stimulus generalization separately;
- short-horizon affect forecasting;
- combining physiology with past affect labels;
- conditioning an explanatory physiology association on prior feeling.

Potentially distinctive contribution:
A replicated, adversarial benchmark demonstration that asks a more specific conditional-information question:
**When recent observed affect is already available, does peripheral physiology add prospective forecasting skill?**
The project tests this with parameter-free recent-state/no-change baselines, strict future windows, multiple horizons, double held-person×stimulus/segment generalization, linear/nonlinear learners, level and change targets, physiology-alignment controls, and independent POPANE replication.

Recommended wording:
- “replicated benchmark demonstration”
- “an underexamined conditional-information distinction”
- “we found no matching evaluation contract in our bounded search”

Forbidden wording without a completed systematic review:
- “first ever”
- “first study”
- “unique”
- “no prior work”
