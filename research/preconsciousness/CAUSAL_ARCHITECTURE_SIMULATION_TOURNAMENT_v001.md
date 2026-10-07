CAUSAL ARCHITECTURE SIMULATION TOURNAMENT v001
Date: 2026-10-07
Status: Synthetic falsification/identifiability demonstration; not empirical evidence.

DESIGN
Four linear-Gaussian generative models were frozen for a simple demonstration:
S — strict serial: M -> I -> E -> F.
B — homeostatic bypass: strict serial + M -> F.
P — parallel/direct emotion route: M -> I, M -> E, I -> E, E -> F.
R-proxy — an acyclic reduced-form proxy containing multiple/direct paths expected from recurrent mature systems.

For each model:
N = 2,000 observations per replicate.
500 independent replicates.
Fixed seed block 100000–100499.
All structural coefficients were fixed before simulation.
Primary statistics:
partial correlation r(M,E | I),
partial correlation r(M,F | E),
partial correlation r(I,F | E).

These are chosen because the strict-chain DAG predicts all three to be zero under causal sufficiency/faithfulness in the ideal linear-Gaussian setting.

RESULTS

STRICT SERIAL S
M-E | I: mean r = 0.000282; 5–95% = [-0.038107, 0.039832]; Pr(|r|>.10)=0.000.
M-F | E: mean r = -0.000921; 5–95% = [-0.040736, 0.037290]; Pr(|r|>.10)=0.000.
I-F | E: mean r = -0.001922; 5–95% = [-0.038100, 0.034180]; Pr(|r|>.10)=0.000.

HOMEOSTATIC BYPASS B
M-E | I: mean r = 0.000282; 5–95% = [-0.038107, 0.039832]; Pr(|r|>.10)=0.000.
M-F | E: mean r = 0.441276; 5–95% = [0.410356, 0.471236]; Pr(|r|>.10)=1.000.
I-F | E: mean r = 0.213891; 5–95% = [0.177735, 0.248437]; Pr(|r|>.10)=1.000.

PARALLEL/DIRECT-E ROUTE P
M-E | I: mean r = 0.395359; 5–95% = [0.362562, 0.425687]; Pr(|r|>.10)=1.000.
M-F | E: mean r = -0.001025; 5–95% = [-0.039586, 0.035976]; Pr(|r|>.10)=0.000.
I-F | E: mean r = -0.001869; 5–95% = [-0.036929, 0.030016]; Pr(|r|>.10)=0.000.

RECURRENT-SYSTEM REDUCED-FORM PROXY
M-E | I: mean r = 0.332213; 5–95% = [0.298345, 0.363440]; Pr(|r|>.10)=1.000.
M-F | E: mean r = 0.137538; 5–95% = [0.100016, 0.173321]; Pr(|r|>.10)=0.950.
I-F | E: mean r = 0.387216; 5–95% = [0.357031, 0.415387]; Pr(|r|>.10)=1.000.

INTERPRETATION
The simulation verifies the exact d-separation analysis:
- the strict-chain constraints behave as expected;
- a homeostatic-feeling bypass specifically breaks the M-F | E and I-F | E constraints;
- a direct/parallel route into emotion specifically breaks M-E | I;
- a multiroute architecture breaks several serial constraints.

This provides a concrete preregistration template for later empirical data: the four-stage ladder is not merely a verbal proposal; it has conditional-independence consequences that can be attacked.

LIMITATIONS
This is synthetic and does not establish which human architecture is true.
The models are linear Gaussian and omit measurement error, latent confounding, time lags, and cyclic dynamics.
The R model is only an acyclic reduced-form proxy and is not evidence about true biological recurrence.

VERDICT
COMPUTATIONAL CHECK PASSES.
The formal attack is internally coherent and can distinguish important rival architectures in ideal data. Empirical testing would require validated measurements for M, I, E and F and explicit latent-confounder/measurement models.
