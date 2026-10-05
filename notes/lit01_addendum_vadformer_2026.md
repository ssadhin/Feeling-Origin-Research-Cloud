# LIT-01 addendum — 2026 forecasting paper audit

New close paper found during the final methodological search:

## Sujatha et al. 2026 — VADFormer
Title: A multimodal transformer system for continuous Valence-Arousal trajectory modeling and emotion forecasting
Journal: Expert Systems with Applications 331, 133306
DOI: 10.1016/j.eswa.2026.133306

Classification: IMPORTANT FORECASTING PREDECESSOR, NOT AN EXACT CONTRACT MATCH based on accessible abstract/indexed methods.

Accessible details:
- Explicitly unifies continuous V-A regression, classification and one-step affect forecasting.
- Uses facial video + speech/audio multimodal inputs, not peripheral physiology.
- Evaluates Aff-Wild2, AFEW-VA and OMG-Emotion.
- Reports 6–10% forecasting-error reductions and cross-domain robustness.
- The accessible description does not establish an observed recent-self-report / parameter-free persistence comparator, nor simultaneous person×stimulus holdout matching our design.
- Full text is closed in the currently accessible sources; details about exact forecasting baselines and whether ground-truth prior VA enters the model remain unresolved. Do not infer those details.

Novelty consequence:
Forecasting continuous V-A itself is clearly NOT novel in 2026 and must not be presented as such. The candidate distinction must be narrower: peripheral physiological incremental utility conditioned on observed recent self-report/persistence under strict person/stimulus generalization and external replication.

Updated novelty-safe wording:
“Recent work has introduced explicit short-term continuous valence–arousal forecasting in multimodal audio-visual systems. Our question is different: whether peripheral physiological signals add prospective predictive value once an observed recent self-reported affect state is already available, evaluated against a parameter-free persistence benchmark under strict person and stimulus generalization.”

Because VADFormer full-text methodological details were not accessible in the bounded search, LIT-01 remains NO_EXACT_MATCH_IN_BOUNDED_SCREEN rather than a uniqueness claim.
