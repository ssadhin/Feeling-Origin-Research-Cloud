# Affective forecasting novelty / replication audit v002

Status: bounded prior-art and external-data audit after O002-G1, before O002-G2 result.

## Current candidate paper claim

Real time-aligned peripheral physiological signal can coexist with little or negative incremental short-horizon forecasting utility once temporally persistent reported affect and context are known. In O002-G1 this pattern generalized under simultaneous unseen-person and unseen-stimulus holdout.

This is a predictive / benchmarking claim only. It does not imply physiological causal irrelevance, body-independence of feeling, phenomenal identity, or universal zero physiology utility.

## Closest prior art

### EPiC big-team benchmark — Coles et al., Royal Society Open Science 2025
DOI: 10.1098/rsos.241778
- Twelve teams predicted self-reported valence/arousal from peripheral nervous system measures.
- Generalization was tested across participants, targeted emotion, inductions, and time.
- All tests beat random prediction; only 46% beat a training-set mean baseline.
- Replacing physiology with random noise degraded most top-model tests, demonstrating real physiological signal.
- The authors explicitly identify stronger baselines preserving continuity, temporal variability, and autocorrelation as an unmet benchmarking need.
- Does not test physiology increment beyond a strong recent same-axis self-report + context baseline.

### CorrNet — Zhang et al., Sensors 2021
DOI: 10.3390/s21010052
- CASE + MERCA; fine-grained current valence/arousal recognition from physiology.
- Subject-independent CASE binary accuracy reported around 76.37% valence and 74.03% arousal.
- Establishes that physiology contains current-affect information.
- Not prospective future forecasting and not an incremental comparison against lagged self-report/context.

### EMAP — Eisenbarth et al., Psychophysiology 2024
DOI: 10.1111/psyp.14446
- 145 participants; 3,434 video trials; continuous moment-by-moment subjective arousal plus EEG and peripheral physiology.
- Temporal algorithms improve concurrent momentary arousal prediction compared with non-temporal algorithms.
- Paper discusses temporal-shift tests and continuous-rating temporal limitations.
- Does not establish the O002 prospective incremental question beyond lagged subjective affect.

### Emotional inertia / autoregression — Bagnara et al., Emotion 2025
DOI: 10.1037/emo0001541
- Eight experience-sampling datasets; N=948; 73,472 occasions.
- Significant autoregressive persistence of positive and negative affect.
- Establishes affect persistence as prior art.
- Does not test peripheral physiology increment beyond lagged affect.

### Wearable affect forecasting
Relevant longitudinal work includes next-day/week-ahead affect forecasting from wearables and diary/text information (e.g. arXiv:2201.11230; arXiv:2403.13841) and longitudinal passive-sensing valence/arousal prediction. These establish forecasting and multimodal sensing as prior art, but the bounded search did not identify the exact O002 comparison contract.

## Residual novelty after pressure test

Not novel independently:
- physiology predicts affect;
- CASE physiology supports subject-independent emotion recognition;
- temporal modeling of affect;
- affective inertia / autoregressive persistence;
- cross-subject physiology models;
- wearable affect forecasting.

Potentially distinct combination found so far:
1. future continuous affect forecasting rather than concurrent recognition;
2. explicit strong same-axis recent-report + context baseline;
3. physiology tested only for incremental value above that baseline;
4. autocorrelation-preserving time-shift control showing the physiology is real signal;
5. lag-depth attack showing report persistence is not only immediately adjacent joystick interpolation;
6. simultaneous unseen-person × unseen-stimulus evaluation;
7. external/model-class robustness rather than a single favorable model.

Bounded-search conclusion: POTENTIALLY PUBLISHABLE BUT NEEDS VALIDATION. No claim of global novelty is justified yet.

## External replication audit: EMAP

Official Zenodo record: https://zenodo.org/records/8327283
DOI: 10.5281/zenodo.8327283
- 145 participants, continuous arousal ratings, HR, respiration, skin conductance, blood volume, EEG.
- Both raw and clean data are documented; published feature extraction uses 500 ms bins.
- Scientifically well suited to an independent arousal-only prospective incremental replication.
- Files are RESTRICTED. The Zenodo record requires accepting the EMAP academic/research licence and submitting an access request; requests are stated to be processed within 48 hours.
- Licence forbids commercial use and redistribution. Therefore the project must not bypass or scrape restricted files.
- Until authorized access exists, EMAP is a genuine external-data dependency, not an executable replication.

## Active robustness gate

O002-G2 was frozen before outcome:
- protocol fc936cd6cd6cd77beb6622d0ab96a5ae86468452
- analysis 9401e8bfd6cb5cdf09b222e874ddb1ee3ad02c93
- workflow 30277b4796296d8e31b743dc6e6220e13bbb8430
- trigger 2bfc6ad371dd75d24c0d1d2c6cbc6c4d36ccdd90
- run 37255619996

It shifts the target 10/20/30 seconds farther forward under the same joint unseen-person × unseen-stimulus design. No G2 outcome is inferred here.

## Decision after G2

- If prior-report advantage remains and no physiology increment appears at all horizons: advance to independent-dataset replication / manuscript integrity stage; EMAP is preferred if authorized access can be obtained.
- If physiology becomes incrementally useful at one or more horizons: classify the result as horizon-dependent/mixed, narrow the paper claim, and independently replicate the positive horizon before any strong statement.
- If prior-report dominance collapses: retire any broad temporal-persistence framing and re-evaluate the paper around the narrower short-horizon result.
