# O001 — Observational Multimodal Redundancy Bridge

Status: FROZEN BEFORE OUTCOME COMPARISON

## Purpose

Test whether central EEG and peripheral autonomic channels carry complementary held-out information about continuously reported felt affect in the public BCMI training dataset (NEMAR on002724 / OpenNeuro ds002724).

This is an **observational redundancy test**, not a test of causal origin, necessity, sufficiency, consciousness, or phenomenal identity.

## Dataset pin

- Dataset: BCMI training sessions, ds002724 / NEMAR on002724
- Public NEMAR release path used by scripts: https://data.nemar.org/on002724/v1.0.0/
- Manifest-based deterministic file enumeration.
- Required synchronized channels: 32 EEG channels, ECG, GSR, VA1, VA2, VAtarg.
- Event files define 21-s target-state segments. Because adjacent half-trial events overlap by ~1 s, no analysis window may use the final 2 s of an event.

The public source describes VA1/VA2 jointly as the two continuously recorded FEELTRACE user-report dimensions. Unless a source explicitly maps the channel names to valence versus arousal, O001 will report them as **FEELTRACE axis 1** and **FEELTRACE axis 2** rather than guessing the ordering.

## Parsing rule

The archived EDF files use an anonymized invalid start date (observed as 00.00.14), which strict EDF readers may reject. The analysis may ignore the date field and parse the fixed EDF header/data records directly. Signal samples, channel scaling, timestamps relative to run start, and event files must not be modified.

## Eligible runs

A run is included only if:
1. the EDF and matching events.tsv are public and downloadable;
2. required channels EEG(32), ECG, GSR, VA1, VA2, VAtarg are present;
3. sample frequency is 1000 Hz and all required channels share that rate;
4. EDF record structure is internally consistent;
5. at least one prespecified analysis sample can be constructed.

No run is excluded because of its predictive outcome.

## Analysis samples

For every 21-s event, construct four samples at relative target times:
- 6 s
- 10 s
- 14 s
- 18 s

For a target time tau:

- outcome Y1/Y2: mean VA1/VA2 during [tau, tau+1 s)
- prior-report baseline: mean VA1 and VA2 during [tau-2, tau-1 s)
- explicit 1-s gap: [tau-1, tau) is unused
- modality predictor window: [tau-6, tau-2 s)

This makes modality features temporally precede the report target and prevents direct sample overlap.

Additional baseline variables:
- one-hot VAtarg target code, sampled at tau-3 s and rounded to nearest integer 0..9;
- event-relative target-time indicator (6/10/14/18 s).

## EEG features

Use only the modality predictor window.

For each EEG channel:
1. subtract linear trend;
2. compute Hann-windowed rFFT periodogram;
3. integrate power in fixed bands:
   - theta: 4–8 Hz
   - alpha: 8–13 Hz
   - beta: 13–30 Hz
   - low gamma: 30–45 Hz
4. log(power + 1e-12).

Average log band power within five prespecified channel groups:

- frontal: FP1, FPz, FP2, F7, F3, Fz, F4, F8
- frontocentral: FT9, FC5, FC1, FC2, FC6, FT10
- central-temporal: T7, C3, Cz, C4, T8
- centroparietal: TP9, CP5, CP1, CP2, CP6, TP10
- parietal-occipital: P7, P3, Pz, P4, P8, O1, O2

Primary EEG vector = 5 regions × 4 bands = 20 features.

## Autonomic features

From ECG and GSR in the same predictor window, use simple waveform features that do not require a fragile peak detector.

For each channel:
- mean
- standard deviation
- linear slope
- RMS first derivative

ECG additionally:
- log spectral power 0.8–2.5 Hz
- frequency of maximum power within 0.8–2.5 Hz

GSR additionally:
- difference between last and first 0.5-s mean
- log low-frequency power 0.01–0.5 Hz

Primary autonomic vector = 12 features total.

These are called **autonomic-channel features**, not heart rate or sympathetic/parasympathetic states.

## Models

Fit separate models for VA1 and VA2.

Four nested ridge-regression models:

- B: prior VA1/VA2 + VAtarg one-hot + within-event time
- B+A: B + autonomic features
- B+E: B + EEG features
- B+A+E: B + both modalities

All feature standardization is fitted on training data only.

Ridge alpha is selected independently for each fold/model/outcome from:
0.1, 1, 10, 100

Alpha selection uses inner leave-one-run-out validation restricted to the outer-training sessions. No test-session samples may participate in feature scaling or hyperparameter selection.

## Outer validation

Subject-specific models, matching the dataset's personalized BCMI design.

Primary outer split: leave-one-session-out within each participant.

A participant is eligible for primary inference only if they have at least two distinct sessions and at least two runs in each testable session. Runs are never split across train and test.

If the public mirror contains fewer sessions than expected for a participant, that participant contributes only folds that satisfy these rules.

## Primary metrics

For each subject-session fold and each FEELTRACE axis:
- RMSE
- R²

Primary unique-information contrasts are RMSE improvements:

- EEG unique beyond autonomic:
  delta_E_given_A = RMSE(B+A) - RMSE(B+A+E)

- autonomic unique beyond EEG:
  delta_A_given_E = RMSE(B+E) - RMSE(B+A+E)

Positive values favor complementary information.

The primary pooled statistic is the mean of each delta across the two FEELTRACE axes within fold, then averaged across folds/subjects.

## Uncertainty

Cluster bootstrap at the participant level, fixed seed 50001, 5000 replicates.

A channel class earns a **held-out unique-information PASS** only if the 95% participant-bootstrap CI for its pooled mean RMSE improvement is entirely above 0.

Classification:
- both PASS: OBSERVATIONAL_COMPLEMENTARITY
- EEG only: EEG_PREDICTIVE_DOMINANCE
- autonomic only: AUTONOMIC_PREDICTIVE_DOMINANCE
- neither: NO_DETECTED_UNIQUE_COMPLEMENTARITY

This classification is descriptive/predictive only.

## Mandatory sensitivity analyses

### S1 — motor-adjacent EEG exclusion

Repeat B+E and B+A+E after removing:
FC5, FC1, FC2, FC6, C3, Cz, C4, CP5, CP1, CP2, CP6.

If EEG unique-information PASS disappears only after this exclusion, flag:
MOTOR_REPORT_CONTAMINATION_PLAUSIBLE.

### S2 — stronger temporal separation

Repeat the primary analysis using:
- modality window [tau-8, tau-4 s)
- prior-report baseline [tau-3, tau-2 s)
- outcome [tau, tau+1 s)

Only target times 10, 14, 18 s are valid here.

If a unique-information result exists only in the primary 2-s separation but not S2, flag:
SHORT_LAG_DEPENDENCE.

### S3 — target-free baseline

Repeat without VAtarg one-hot.

This is secondary and checks whether target-state metadata suppresses or creates modality complementarity.

## Failure / interpretation rules

1. If fewer than 5 participants satisfy outer-validation eligibility, report INSUFFICIENT_PARTICIPANTS; do not classify complementarity.
2. If VA1/VA2 are constant or missing within analysis windows, abort.
3. If one modality materially fails QC in >20% of otherwise eligible runs, report MODALITY_QC_LIMITED.
4. Predictive complementarity does not imply multiple causal generators.
5. Predictive dominance does not imply causal primacy.
6. Failure of one channel class to add held-out prediction does not show it is irrelevant to feeling.
7. No claim about valence-versus-arousal axis identity is allowed unless VA1/VA2 ordering is source-verified independently.
8. V015 remains withheld regardless of O001 outcome.

## Precommitted scientific consequences

- OBSERVATIONAL_COMPLEMENTARITY: a simple one-channel descriptive source model is inadequate for this dataset at the measured scale; motivates causal perturbation of multiple routes.
- EEG_PREDICTIVE_DOMINANCE or AUTONOMIC_PREDICTIVE_DOMINANCE: prioritizes that channel family for causal follow-up but does not establish origin.
- NO_DETECTED_UNIQUE_COMPLEMENTARITY: measured modalities are redundant/noisy at this feature scale; do not conclude a single origin.
- Sensitivity failures downgrade any primary PASS accordingly.
