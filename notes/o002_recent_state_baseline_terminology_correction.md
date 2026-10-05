# Terminology correction — recent-state persistence baseline

Audit date: 2026-10-05.

The CASE O002 feature extractor defines prior_valence and prior_arousal as the MEAN annotation value in the frozen [-5,-1) second window before the anchor:
pv = PR.valence.mean(); pa = PR.arousal.mean().

The POPANE-R1 extractor likewise defines prior_affect as the MEAN affect value in [-5,-1] seconds.

Therefore manuscript text must use terms such as:
- recent-state persistence baseline
- recent 4-second mean self-report
- carry-forward of the recent pre-anchor mean

Do NOT describe the tested baseline as the literal last sample / last joystick value unless a separate analysis is run.

This correction changes terminology only, not any prediction, protocol, result, or inference. The parameter-free level forecast is y_hat = recent pre-anchor mean self-report.
