# O002-B3 post-primary longer-horizon simple-baseline reconciliation

Status: EXPLORATORY / POST-PRIMARY. G2 and B1 were already observed before this paired reconciliation. It is not confirmatory.

Question: At 11/21/31 s gaps under the same subject×video cells, does the fitted time+prior Ridge model or physiology-augmented model outperform the parameter-free last-reported-state forecast?

Method: pair cell-level MAE from frozen O002-G2 run 37255619996 with frozen O002-B1 run 37256052367. Crossed subject×video bootstrap, 5,000 resamples. Positive delta means the fitted model is worse than naive persistence.

## 11 s gap
Valence:
- fitted prior − naive: +0.01551, 95% CI [0.00926, 0.02331]; fitted prior worse in 82.92% of cells.
- physiology − naive: +0.02826, 95% CI [0.01808, 0.04224]; physiology worse in 85.83%.
Arousal:
- fitted prior − naive: +0.03166, 95% CI [0.01310, 0.05317]; fitted prior worse in 76.67%.
- physiology − naive: +0.04266, 95% CI [0.02271, 0.06742]; physiology worse in 77.50%.

## 21 s gap
Valence:
- fitted prior − naive: +0.02866, 95% CI [0.01574, 0.04360]; fitted prior worse in 78.75%.
- physiology − naive: +0.04277, 95% CI [0.02594, 0.06390]; physiology worse in 81.25%.
Arousal:
- fitted prior − naive: +0.06402, 95% CI [0.02529, 0.10537]; fitted prior worse in 77.50%.
- physiology − naive: +0.07644, 95% CI [0.03930, 0.11824]; physiology worse in 78.33%.

## 31 s gap
Valence:
- fitted prior − naive: +0.04101, 95% CI [0.01843, 0.06645]; fitted prior worse in 77.92%.
- physiology − naive: +0.06102, 95% CI [0.03398, 0.09191]; physiology worse in 77.50%.
Arousal:
- fitted prior − naive: +0.09114, 95% CI [0.03532, 0.14914]; fitted prior worse in 75.83%.
- physiology − naive: +0.10870, 95% CI [0.05121, 0.16980]; physiology worse in 77.92%.

Interpretation:
Across all tested horizons, a parameter-free last-state carry-forward forecast outperforms both the fitted time+prior Ridge model and its physiology-augmented version. This further weakens any model-novelty framing and strengthens the paper's benchmarking/identifiability angle: continuous-affect forecasting must be evaluated against simple persistence before attributing value to multimodal physiology.

This does NOT establish that physiology is causally irrelevant. It is a post-primary same-dataset reconciliation and requires external replication.
