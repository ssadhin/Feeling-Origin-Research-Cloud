# STATIC-01 Protocol↔code conformance audit

Audit scope: O002-G1, O002-G2, POPANE-R1, O002-D1, POPANE-R2 corrected analysis.
Audit date: 2026-10-05. This is a static code/protocol review, not an independent code reproduction.

## Overall decision
NO MATERIAL PROTOCOL VIOLATION FOUND in the audited contracts.

## O002-G1
- Training excludes all rows from both held subject and held video exactly as frozen.
- video_id is absent from all model feature lists.
- Ridge alpha is tuned only inside training data with GroupKFold by subject.
- imputation/scaling are fit inside training pipelines.
- exact frozen phys_ feature columns are used.
- crossed subject×video bootstrap matches the frozen Cartesian resampling rule.
- Material wording issue only: protocol says 'immediately prior same-axis report'; extractor actually uses the mean report over [-5,-1) s. Terminology correction commit 56e0085cc44823c0165eff7d7a4546c4fa934b64 governs manuscript wording.

## O002-G2
- Targets are shifted only within subject×video groups; no boundary crossing.
- Predictors stay on row i; targets move to i+1/i+2/i+3, corresponding to 11/21/31 s predictor-end→target-start gaps under 10 s anchor spacing.
- Same double holdout, training-only tuning, features, MAE deltas and crossed bootstrap are preserved.
- No post-result horizon selection is encoded.

## POPANE-R1
- Filename-based eligible-segment threshold is applied before reading observational values.
- Technical QC implements the frozen duration, affect-finite, physiology-finite and timestamp rules; no value-magnitude/error-based exclusions.
- Common anchors are restricted so all four horizons are available, avoiding horizon-specific row-selection artifacts.
- Predictor windows end before target windows; no target samples enter physiology/prior features.
- 10 subject folds are deterministic from sorted participant IDs.
- Primary joint evaluation excludes every participant in held fold AND all rows of held segment from training; segment identity is not a predictor.
- Ridge tuning is training-only by participant; HGB hyperparameters are fixed.
- Primary uncertainty is participant-cluster bootstrap on participant-level paired MAE differences.
- R1 frozen decision logic is implemented as specified.

## O002-D1
- Change target is future target minus the same recent-state predictor value, exactly as frozen.
- zero-change baseline predicts zero without fitting.
- context and physiology feature sets match protocol.
- double holdout remains subject AND video.
- Ridge/HGB specifications, MAE deltas and crossed bootstrap match protocol.
- Frozen change-signal rule requires both learners positive for the same horizon×axis; code implements this.

## POPANE-R2 corrected analysis
- Reuses R1 extraction, QC, folds, feature construction and models rather than redefining them.
- Change target, zero baseline, context features and joint person×segment split match the frozen R2 protocol.
- Participant-cluster bootstrap and both-learner clear-signal rule match protocol.
- R2 and R2b failures occurred before outcome computation; R2c changes only download robustness and uses the same corrected analysis.

## Residual limitations that are NOT protocol violations
1. These are observational predictive analyses; no causal interpretation is licensed.
2. MAE is the primary utility metric. A model could conceivably improve a different shape/correlation metric while worsening MAE; that would be a different endpoint and should not be retrofitted as a rescue analysis before manuscript unless explicitly justified.
3. CASE and POPANE recent-state baselines are short-window means, not literal last samples.
4. POPANE external replication covers valence, not arousal.
5. Feature engineering cannot exhaust all possible physiological representations; claims must remain conditional on tested peripheral channels/features/model classes.

## Audit consequence
Absent a later discovered implementation bug, the mandatory change-target and signal-validity gates should determine manuscript claim class under MANUSCRIPT-GATE-01 rather than adding more same-dataset endpoints.
