# POPANE-R3 second technical failure audit — run 37268391855

Scientific status: NO VERDICT COMPUTED.

The frozen data extraction and model predictions completed. The run failed only during final metric aggregation.

Exact remaining implementation error:
`mean_absolute_error(prd.y, prd.shift)` again resolved `prd.shift` to the pandas DataFrame.shift method rather than the prediction column named `"shift"`.

This is the same namespace-collision class as the first failed run, but at a second line that the first one-line correction did not reach.

Permitted correction:
replace the remaining prediction-column attribute access with explicit bracket access:
`prd["shift"]`.
No scientific element may change: protocol, target, temporal-shift construction, feature set, folds, learners, uncertainty and decision rules remain frozen.

Run: 37268391855
Protocol: 8e2fb4e00a4dfeaed358b651d8e7570ceab6d1b4
First correction commit: 6b3819d22351ea885d748b2c5fc6f76d67f9650b

No R3 empirical conclusion may be drawn from this failed run.
