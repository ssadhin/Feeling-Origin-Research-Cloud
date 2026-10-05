# POPANE-R1 temporal leakage audit

Status: REVIEWED AGAINST analysis/popane_r1_independent_valence_replication.py

## Window separation

For anchor a:
- physiology predictor window: [a-10, a-1] s
- recent-affect baseline/context window: [a-5, a-1] s
- future target windows:
  - nominal 1 s gap: [a, a+5] s
  - nominal 11 s gap: [a+10, a+15] s
  - nominal 21 s gap: [a+20, a+25] s
  - nominal 31 s gap: [a+30, a+35] s

Thus the latest predictor/baseline sample is at a-1 and the earliest primary target begins at a. The minimum nominal separation is 1 s under the protocol's second-resolution interpretation.

## ECG filtering

ECG feature extraction uses a zero-phase Butterworth bandpass via scipy.signal.sosfiltfilt. However, filtering is invoked only after the raw dataframe has already been sliced to the predictor window:
sub = df.loc[pm]
e = ecg_features(sub.ECG, 1000.0)

Therefore forward/backward filtering can use samples from both directions only INSIDE the already-frozen predictor window. It cannot access samples at a or later and cannot leak target-window information.

Missing ECG interpolation is likewise performed only inside that already-sliced predictor window.

EDA and hemodynamic summary/slope features are computed from the same predictor-window slice.

## Conclusion

No future-target sample is used in the R1 physiological feature extraction as implemented. The use of zero-phase filtering is non-causal within the historical predictor window, but it does not create target leakage because the full future signal is never supplied to the filter.

This audit addresses target leakage only; it does not imply deployment-time streaming equivalence, because an online implementation would need to wait until the predictor window has fully elapsed before computing these retrospective window features.
