# POPANE-R3 technical failure audit — run 37267700807

Scientific status: NO VERDICT COMPUTED.

The public Study 6 archive downloaded successfully and the frozen feature extraction completed (including 1,100+ files) before the script failed during metric aggregation. No R3 decision statistic or verdict was produced.

Exact error:
sklearn InvalidParameterError because `q.shift` resolved to pandas DataFrame.shift (a method) rather than the prediction column named `"shift"`.

Cause:
A pure implementation namespace collision in the metric line:
`mean_absolute_error(q.y, q.shift)`.
The intended column was `q["shift"]`.

Correction rule:
The scientific protocol, target, shift construction, features, participant/segment folds, learners, uncertainty, and decision rules must remain unchanged. The only permitted fix is replacing attribute access with explicit column access for the already-computed shifted-model predictions.

Original failed run: 37267700807
Protocol: 8e2fb4e00a4dfeaed358b651d8e7570ceab6d1b4
Analysis: b9c63dd648c9bf72401db5f513d8ffd91ec195a4
Workflow: f365c0f7533db0df6773ee59b8ec87c590932374
Trigger: 0ba388d50a1aeb91c5088176e9c8af9631d0166d

This failure is technical and must not be counted as empirical evidence.
