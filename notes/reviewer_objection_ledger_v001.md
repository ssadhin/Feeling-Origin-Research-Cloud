# Affect Forecasting Paper — reviewer objection ledger v001

Status: final-loop audit; CASE-D2 pending at creation.

## Addressed with empirical tests

### “Persistence only wins because you tested one tiny horizon.”
Addressed.
- CASE and POPANE: 1/11/21/31 s effective predictor-end-to-target-start gaps.
- Persistence advantage remains through 31 s.

### “The result is only linear-model failure.”
Addressed.
- Ridge and nonlinear HistGradientBoosting evaluated.
- POPANE R1/R2/R4/R5/R6 conclusions survive both model classes.
- CASE primary/D1 also includes nonlinear stress testing.

### “Physiology may predict changes rather than levels.”
Addressed, with nuance.
- CASE-D1: HGB-only positive context increments in a few cells, but no Ridge/HGB robust rescue; zero-change beats physiology everywhere.
- POPANE-R2: no external change increment; zero-change beats physiology at every valence horizon for both learners.
- Conclusion: a robust transition rescue is not supported; isolated CASE HGB effects remain exploratory and must be reported, not hidden.

### “Participant-cluster uncertainty ignores held-out stimulus/segment uncertainty.”
Addressed externally.
- POPANE-R4 crossed participant×segment bootstrap keeps all 8 naive-vs-physiology CIs strictly negative.

### “All-channel physiology loses because noisy modalities swamp one useful channel.”
Addressed for predeclared POPANE families.
- R5 ECG-only, EDA-only, and ICG/hemodynamic-only screens all fail to rescue physiology beyond context at all horizons and both learners.
- This does not rule out every possible representation or feature-selection method.

### “MAE hides better trajectory tracking by physiology.”
Addressed externally.
- POPANE-R6: physiology is worse than persistence on RMSE and CCC at all horizons, both learners; all relevant CIs unfavorable.
- CASE-D2 pending.
- R6 models were not optimized specifically for CCC, so do not claim universal CCC impossibility.

### “Zero-phase ECG filtering leaks future target samples.”
Addressed.
- In POPANE code, raw data are sliced to [-10,-1] s before sosfiltfilt is called.
- Filtering is non-causal within the completed historical window but cannot access target samples.

### “External replication might be based on synthetic/interpolated labels.”
Addressed.
- POPANE descriptor documents continuous self-reported valence using an electronic 1–10 rating scale adjusted as often as needed to reflect the participant’s current feeling and recorded alongside physiology.

### “The exact external data bytes cannot be reconstructed.”
Addressed.
- Study 6 archive provenance captured: SHA256 a5db8dd9b57fb1cd1ad799b635f4e59c9edaeb8481285a9e1fbef3522e998140; 2,872,865,432 bytes; 1,497 ZIP entries.

## Addressed by claim narrowing rather than empirical elimination

### “Persistence may reflect annotation mechanics, not latent affect inertia.”
Survives as a legitimate construct-validity limitation.
- Continuous joystick/electronic-scale dynamics can contribute to autocorrelation.
- The paper must claim forecasting of recorded continuous self-report, not identify the causal dynamics of latent feeling.
- Longer horizons/change targets reduce but do not eliminate this concern.

### “Physiology has been shown to predict affect in prior work.”
True and compatible with our result.
- Our question is incremental prospective value after strong observed-state history, not whether physiology ever contains useful affect information.

### “Other physiology representations/deep raw-signal models could do better.”
True.
- Current result applies to tested peripheral channels/features/model families.
- Do not universalize to all possible physiological encoders.

### “External replication is only valence.”
True.
- POPANE Study 6 external replication is valence only.
- Arousal claims remain CASE-specific.

### “CASE signal-without-increment pattern replicated externally.”
False.
- POPANE-R3 found no detectable real-vs-shifted aligned signal.
- Keep signal-without-increment distinction as CASE evidence only.

## Novelty attacks

### “Past affect is known to be predictive.”
True; not novel.
- DeepMood and related history-only forecasting establish this.

### “Wearable physiology can forecast future mood.”
True; not novel.
- Taylor et al., Saylam & İncel, Pounds et al., and related work.

### “CASE physiology has been modeled temporally before.”
True; not novel.
- EPiC/D’Amelio and other CASE work.

### Exact intersection
Bounded LIT-N1 search has not found a paper that simultaneously:
1. forecasts future subjective affect;
2. uses peripheral physiology;
3. explicitly conditions on observed recent affect/history; and
4. reports a history-only/persistence comparator or equivalent nested physiology increment.

This supports “under-tested distinction” / “no direct match found in our bounded search,” not a global first-study claim.

## Remaining active gate

CASE-O002-D2 RMSE/CCC sensitivity.

If D2 has no robust CCC rescue:
- no material scientific objection remains that requires another experiment before drafting;
- remaining issues are reporting/limitations and broader literature-search completeness.

If D2 has a robust CCC rescue:
- paper remains viable, but title/abstract/results must distinguish point-error persistence dominance from physiology trajectory concordance in CASE;
- external POPANE still shows no CCC rescue, making the effect dataset-specific.

## Stop rule

Do not invent new analyses simply because more analyses are possible. After D2:
- if the frozen PAPER-G1 gate returns READY, stop adding experiments unless a new concrete reviewer objection arises;
- shift to the required three-loop readiness-confirmation process and manuscript planning, without editing the manuscript until the project rule is satisfied.
