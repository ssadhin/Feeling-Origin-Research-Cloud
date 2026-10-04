# Baseline dominance checkpoint — O001 and O002

Purpose: quantify how much short-horizon prospective prediction is gained by adding immediately prior same-axis self-report to context before any physiology is added.

## O001 (ds002722, 19 participants)

- Valence: stimulus-only MAE 1.1746370 -> stimulus+prior MAE 0.5317092. Relative MAE reduction 54.73%; error ratio 2.21x.
- Arousal: stimulus-only MAE 1.2089359 -> stimulus+prior MAE 0.6061400. Relative MAE reduction 49.86%; error ratio 1.99x.

## O002 (CASE, 30 participants)

- Valence: stimulus/time-only MAE 1.0347886 -> stimulus/time+prior MAE 0.1778034. Relative MAE reduction 82.82%; error ratio 5.82x.
- Arousal: stimulus/time-only MAE 0.8335935 -> stimulus/time+prior MAE 0.1965672. Relative MAE reduction 76.42%; error ratio 4.24x.

Interpretation: the immediately prior self-report is an extremely strong forecasting variable in both datasets, especially CASE. This supports using a recent-report baseline when assessing incremental physiological utility.

Adversarial caveat: do not automatically interpret this as psychological affective inertia. Continuous annotations are physically generated with a joystick, can have reaction lag, are slowly varying, and CASE's released interpolated annotation stream was linearly interpolated to a fixed 50 ms grid. The dominant prior-report signal could therefore mix true affect persistence with measurement/annotation persistence.

Next attack: O002-H1 lag-depth robustness will compare near, mid and far prior-report windows and test physiology increment at each lag. If only the immediate prior window dominates, the theoretical 'affective inertia' framing should be weakened toward 'recent-report persistence'.