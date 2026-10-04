# Novelty / publication audit after O002-P1 and O002-H1

## Current empirical synthesis

O002 now supports three simultaneously true statements:

1. Recent reported affect is a very strong short-horizon predictor of future reported affect.
2. That report-persistence signal extends well beyond the immediately adjacent annotation window: approximately 11 s and 21 s-gap predictors still materially improve over video/time context.
3. Real peripheral physiology contains statistically detectable time-aligned predictive information relative to an autocorrelation-preserving shifted control, but does not add reliable held-out forecasting value beyond the report-persistence/context baseline.

Therefore the correct result is not a generic null. It is a redundancy/incremental-information result: REAL SIGNAL BUT LITTLE/NO INCREMENT BEYOND TEMPORALLY PERSISTENT REPORTED STATE.

## Literature pressure

Closest direct comparator remains Coles et al. 2025, Royal Society Open Science, DOI 10.1098/rsos.241778. Their CASE big-team study shows physiology can beat random baselines, but weak/mean baselines are much harder and the authors explicitly call for baselines preserving continuity, temporal variability and autocorrelation. O002-P1 is consistent with their real-vs-random finding while O002 primary/H1 impose a stronger recent-report benchmark.

Continuous annotation literature creates an important measurement caveat. CASE uses simultaneous joystick self-report and its released interpolated annotation stream was linearly interpolated to 50 ms spacing (Sharma et al. 2019, Scientific Data, DOI 10.1038/s41597-019-0209-0). Other continuous-emotion work explicitly models annotator reaction lag and slow label dynamics (e.g. Khorram et al., IEEE TAFFC, DOI 10.1109/TAFFC.2019.2917047). H1 weakens a purely immediate joystick-persistence explanation because report information remains strong at ~11 and ~21 s gaps, but does not prove a pure psychological latent-state mechanism.

Additional nearby prior art found in the targeted search includes a 2026 paper on dynamic affective surprise that computes previous affect from exponentially weighted recent continuous ratings and studies memory consequences. This confirms that recent affect history as a scientifically meaningful construct is prior art. It does not, from the methods inspected, test the incremental prospective value of physiology beyond prior affect under held-out-person forecasting.

Targeted searches for combinations of prior/lagged self-report + physiology + prospective continuous valence/arousal + held-out-person evaluation did not reveal an obvious already-published equivalent. This is evidence for possible novelty, not proof of uniqueness; broader systematic literature screening is still required before manuscript submission.

## Novelty classification

POTENTIALLY PUBLISHABLE; NOVELTY CANDIDATE STRENGTHENED, BUT EXTERNAL PATTERN REPLICATION AND SYSTEMATIC PRIOR-ART SCREEN STILL REQUIRED.

Candidate contribution:

Use temporally persistent self-reported affect as a strong prospective baseline for continuous emotion forecasting, then quantify what physiology adds beyond that baseline. Across O002, aligned physiology contains real signal yet does not improve prediction beyond recent reported state/context, and this non-increment persists when the report predictor is moved ~11 and ~21 s farther from the target.

## Claim boundaries

Allowed: physiology contains affect-related signal but may provide little independent short-horizon cross-person forecasting information after conditioning on recent reported affect and context.

Not allowed: physiology is irrelevant to emotion; bodily feedback is unnecessary; feelings are disembodied; reported-state persistence is identical to phenomenal persistence; this is a consciousness detector.

## Remaining publication gates

- External pattern replication in O001, with explicit limitation that its trial-wise permutation cannot preserve exact music identity.
- Stronger generalization beyond the same stimulus set, ideally joint unseen-person × unseen-stimulus evaluation.
- Systematic prior-art screen focused on incremental predictive validity / autoregressive affect baselines, not generic emotion recognition.
- Manuscript-level leakage audit, target-window overlap audit, feature timing audit, and sensitivity to forecast horizon.

Current likely venue category: affective computing / computational emotion / methodological negative-result paper, not consciousness theory.