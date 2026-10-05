# MANUSCRIPT-DATA-01 — canonical result table source

Purpose: single source for manuscript tables/figures. Reporting consolidation only; no new statistical analysis.
Date: 2026-10-05.

## Timing definitions
- physiology predictor: [-10,-1] s
- recent-state self-report predictor: mean over [-5,-1) s
- target: mean self-report over a 5-second future window
- forecast labels 1/11/21/31 s = predictor-end → target-window-start gaps

## CASE G1 — simultaneous unseen person × unseen video, Ridge
| Axis | Context MAE | Recent-state fitted MAE | Physiology MAE | Recent-state increment (95% CI) | Physiology increment (95% CI) |
|---|---:|---:|---:|---:|---:|
| Valence | 1.384980 | 0.167136 | 0.176362 | +1.151377 [0.780366, 1.593827] | -0.008972 [-0.012454, -0.006198] |
| Arousal | 1.326413 | 0.186114 | 0.191432 | +1.146679 [0.737142, 1.568847] | -0.005743 [-0.009636, -0.002033] |

## CASE parameter-free recent-state persistence MAE
| Gap | Valence | Arousal |
|---|---:|---:|
| 1 s | 0.162226 | 0.176388 |
| 11 s | 0.374212 | 0.395940 |
| 21 s | 0.529180 | 0.558414 |
| 31 s | 0.643342 | 0.662333 |

## CASE G2 — fitted physiology increment beyond fitted recent-state/context
| Gap | Valence Δ prior−phys (95% CI) | Arousal Δ prior−phys (95% CI) |
|---|---:|---:|
| 11 s | -0.012758 [-0.021261, -0.006258] | -0.011008 [-0.020646, -0.001434] |
| 21 s | -0.014116 [-0.026016, -0.003468] | -0.012423 [-0.028656, 0.002183] |
| 31 s | -0.020010 [-0.038163, -0.003401] | -0.017563 [-0.036921, 0.001128] |

## CASE P1 signal-validity control
| Axis | Shifted−aligned MAE delta (95% CI) | Baseline−aligned delta (95% CI) |
|---|---:|---:|
| Valence | +0.002000 [0.000642, 0.003413] | -0.003705 [-0.005618, -0.001881] |
| Arousal | +0.001404 [0.000099, 0.002744] | -0.004727 [-0.006904, -0.002456] |
Interpretation: aligned physiology contains detectable signal relative to shift, yet worsens forecast vs frozen baseline.

## POPANE Study 6 R1 — independent valence level forecast, simultaneous held person × held segment
| Gap | Learner | Recent-state naive MAE | Fitted context MAE | Physiology MAE | Naive−phys (95% CI) | Context−phys (95% CI) |
|---|---|---:|---:|---:|---:|---:|
| 1 s | Ridge | 0.124848 | 0.145123 | 0.162567 | -0.037695 [-0.048655,-0.030765] | -0.017434 [-0.028556,-0.010889] |
| 1 s | HGB | 0.124848 | 0.166532 | 0.180226 | -0.055350 [-0.061542,-0.049496] | -0.013678 [-0.017904,-0.009970] |
| 11 s | Ridge | 0.300502 | 0.347702 | 0.378031 | -0.077490 [-0.097748,-0.064019] | -0.030320 [-0.049800,-0.017951] |
| 11 s | HGB | 0.300502 | 0.374016 | 0.404272 | -0.103747 [-0.115201,-0.092679] | -0.030249 [-0.037343,-0.023298] |
| 21 s | Ridge | 0.438355 | 0.502406 | 0.542064 | -0.103689 [-0.135110,-0.083301] | -0.039670 [-0.069786,-0.021596] |
| 21 s | HGB | 0.438355 | 0.532610 | 0.578560 | -0.140129 [-0.156205,-0.124240] | -0.045883 [-0.057951,-0.034564] |
| 31 s | Ridge | 0.553494 | 0.633120 | 0.679646 | -0.126185 [-0.159580,-0.101986] | -0.046596 [-0.080633,-0.025074] |
| 31 s | HGB | 0.553494 | 0.661914 | 0.725996 | -0.172411 [-0.196011,-0.149450] | -0.064000 [-0.083265,-0.046899] |

## CASE D1 — future-change adversarial attack
Frozen verdict: MIXED_CHANGE_RESULT.
- No horizon×axis has BOTH Ridge and HGB positive context-adjusted physiology increment.
- Ridge positive contexts: none.
- HGB-only positive context-adjusted effects:
  - arousal 1 s: +0.008866 [0.000228,0.016588]
  - arousal 11 s: +0.019267 [0.001509,0.036613]
  - valence 31 s: +0.039263 [0.005536,0.079153]
  - arousal 31 s: +0.070627 [0.016075,0.127017]
- zero-change beats physiology for both axes, all gaps, both learners; all paired CIs favor zero-change.

## POPANE Study 6 R2 — future-change valence
Frozen verdict: NO_EXTERNAL_CHANGE_INCREMENT; strong zero-change dominance.
| Gap | Learner | Zero MAE | Context MAE | Physiology MAE | Zero−phys (95% CI) | Context−phys (95% CI) |
|---|---|---:|---:|---:|---:|---:|
| 1 s | Ridge | 0.124848 | 0.143216 | 0.151409 | -0.026545 [-0.028946,-0.024256] | -0.008190 [-0.010184,-0.006438] |
| 1 s | HGB | 0.124848 | 0.158100 | 0.168362 | -0.043489 [-0.047763,-0.039561] | -0.010249 [-0.014043,-0.006536] |
| 11 s | Ridge | 0.300502 | 0.343322 | 0.357387 | -0.056857 [-0.063450,-0.050848] | -0.014065 [-0.019243,-0.009817] |
| 11 s | HGB | 0.300502 | 0.366011 | 0.386715 | -0.086185 [-0.095267,-0.077424] | -0.020692 [-0.028196,-0.013522] |
| 21 s | Ridge | 0.438355 | 0.496664 | 0.516156 | -0.077797 [-0.087900,-0.068531] | -0.019517 [-0.027343,-0.012634] |
| 21 s | HGB | 0.438355 | 0.523841 | 0.561098 | -0.122674 [-0.136379,-0.109324] | -0.037195 [-0.050362,-0.025311] |
| 31 s | Ridge | 0.553494 | 0.626041 | 0.649165 | -0.095712 [-0.107966,-0.084045] | -0.023200 [-0.032598,-0.014871] |
| 31 s | HGB | 0.553494 | 0.653725 | 0.701004 | -0.147432 [-0.167973,-0.127924] | -0.047195 [-0.065865,-0.029311] |

## POPANE Study 6 P1 positive control
Verdict: NO_ALIGNMENT_SIGNAL.
- Ridge shifted−aligned +0.001617 [-0.004439,0.009316]; time-only−aligned -0.049499 [-0.071687,-0.027018].
- HGB shifted−aligned +0.011994 [-0.002502,0.026228]; time-only−aligned -0.087336 [-0.132526,-0.047271].
Consequence: Study 6 supports external baseline dominance/nonincrement, but NOT independent replication of the stronger CASE 'aligned signal exists yet no increment' synthesis.

## Pending
- POPANE Study 5 P2 signal-validity + level-forecast validation (run 37265436088).

All broad causal/body/consciousness claims remain forbidden.
