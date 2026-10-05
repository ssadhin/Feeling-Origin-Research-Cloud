# Forecast-horizon terminology correction

Audit date: 2026-10-05.

All O002/POPANE horizon labels 1 s, 11 s, 21 s and 31 s denote the gap from the END of the latest predictor window to the START of the 5-second target window.

CASE/POPANE common timing:
- physiology window: [-10,-1] s relative to predictor anchor
- recent self-report window: [-5,-1] s
- horizon 0 target: [0,5] s => predictor-end-to-target-start gap = 1 s
- shifted horizon 1 target: [10,15] s => gap = 11 s
- shifted horizon 2 target: [20,25] s => gap = 21 s
- shifted horizon 3 target: [30,35] s => gap = 31 s

The outcome is the MEAN self-report over each 5-second target window, not a point value exactly 1/11/21/31 seconds later.

Manuscript language should say 'target-start gap' on first definition. Thereafter 'forecast gap' or 'horizon' is acceptable only after this definition.

This is terminology only; it changes no result.
