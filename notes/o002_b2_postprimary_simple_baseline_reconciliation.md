# O002-B2 post-primary simple-baseline reconciliation

Status: EXPLORATORY / POST-PRIMARY RECONCILIATION. This comparison was specified only after O002-G1 and O002-B1 outcomes were known. It is not confirmatory and cannot replace the frozen O002 primary or G1 decisions.

Purpose: pair the O002-B1 parameter-free persistence MAE with the already frozen O002-G1 fitted-prior and physiology model MAEs in the same 30 subjects × 8 videos (240 cells), then use the same crossed subject×video bootstrap structure to quantify the descriptive gap.

Data sources:
- O002-G1 run 37226922346, artifact 11311754909.
- O002-B1 run 37256052367, artifact 11323095942.
- 5,000 crossed bootstrap resamples per contrast.

Positive delta below means the named fitted model has larger MAE (worse error) than the simpler comparator.

## Valence
- fitted prior model minus naive persistence: mean +0.0047038; 95% crossed-bootstrap CI [0.0033105, 0.0061754]. Fitted model worse in 90.0% of cells.
- physiology model minus naive persistence: mean +0.0136753; 95% CI [0.0104950, 0.0177932]. Physiology model worse in 91.67% of cells.
- physiology model minus fitted prior model: mean +0.0089715; 95% CI [0.0062422, 0.0124174]. Physiology model worse in 77.92% of cells.

## Arousal
- fitted prior model minus naive persistence: mean +0.0103861; 95% CI [0.0054084, 0.0159425]. Fitted model worse in 86.67% of cells.
- physiology model minus naive persistence: mean +0.0161288; 95% CI [0.0102893, 0.0230369]. Physiology model worse in 87.08% of cells.
- physiology model minus fitted prior model: mean +0.0057427; 95% CI [0.0020606, 0.0095977]. Physiology model worse in 62.08% of cells.

Interpretation:
At the original ~1 s gap, the scientifically relevant benchmark is not a sophisticated learned autoregressive model. A no-training persistence forecast is already stronger. This strengthens the critique of weak affect-prediction baselines and weakens any claim that the project discovered a novel predictive model. It also makes the short-horizon negative physiology increment harder to dismiss as Ridge regularization alone, because the physiology model is worse than a parameter-free reference. However, because B2 is post-primary and uses the same CASE data, independent replication remains necessary.

Firewall:
No causal, bodily-necessity, or phenomenal inference. Do not generalize this 1 s comparison to longer horizons until O002-G2 is complete.
