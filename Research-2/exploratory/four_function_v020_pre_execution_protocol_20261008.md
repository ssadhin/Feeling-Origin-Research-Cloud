# Research #2 — Exploratory four-function organism v0.2 adversarial protocol

Date: 2026-10-08. Status: **development micro-study protocol before v0.2 execution**; NOT the frozen Research #2 AES-v2 methodology benchmark or formal preregistration. This is a test of simulation hypotheses with independent-looking seeded data; user explicitly requested continuation of four-function case study.

## Scientific claim ceiling and risk
Goal: challenge v0.1's apparent context-dependent "emotion" advantage. Null: a temporally persistent threat-response state is reducible to a generic memory/risk filter and cannot be identified as emotion from behavior alone. Alternative: survival differs between predeclared architectures across threat dynamics. No claims about human affect, phenomenal experience, or AES-v2 research-method superiority.

## Shared world and observation contract
120 time steps; initial energy 52 and health 100; survival if both remain >0 at t=120. Actions FORAGE or SHELTER. Forage: energy +8 when a pre-generated food uniform <0.78, minus 1.3; shelter energy -1.75. Under hidden hazard, strike with pre-generated random <0.31 while foraging or <0.015 while shelter; health -21. Energy/health clipped [0,100]. All policies see only energy, health, noisy binary cue and step. All get exactly same per-world pre-generated hazard, cue, food and attack draws, with no direct hidden-hazard observation.
Non-privileged Bayesian controller uses one **fixed** generic guessed hazard transition (onset .15, persistence .75) and globally fixed assumed cue rates (.75/.18); it may be wrong. It never queries the true scenario parameters. This is a model-based competitor but its inductive assumptions are not matched to the reactive controllers; report separately and forbid universal fairness claims.

## Source environment families
DEV and seen-condition EVAL: calm (onset .015, persist .30), persistent (.05,.94), volatile (.36,.45), cue sens .75 and FP .18, food .78.
Novel OOD EVAL families only: hazard_shift (first 60 steps persistent then volatile), hazard_shift_reverse (first volatile then persistent), unreliable_signal (persistent hazards cue sens .55 FP .45), scarce_food (persistent hazards food .55). World generators are public in source; random draws isolated from controller state. These are **developmental OOD stress cases**, not sealed independent external benchmarks.

## Seed separation and stopping
DEV 64 seeds per seen regime, seeds 10000..10063; EVAL 256 per seen+OOD regime, seeds 500000..500255. EVAL values must not be viewed before all source code, tuning grid and policy selection are finalized and recorded in immutable provenance. No optimization on EVAL. All outcomes including failures retained. v0.2 is a new version, never overwrite v0.1.

## Policy arms
1 maintenance-only original, 2 fixed instinct original, 3 tuned instinct using same present cue, 4 original EMA "emotion" alpha .22/theta .36, 5 literal EMA relabelled control with identical dynamics, 6 report-only on original emotion (no action feedback), 7 tuned EMA risk filter, 8 tuned sliding-window mean cue, 9 fixed generic Bayes, 10 tuned generic Bayes, 11 memory ablation (cue-only threshold .36).
Common energy urgency and max energy parameters of emotion, EMA/window: 16/78. Instinct original urgency/max=18/80; tuned instinct urgency in [10,16,18,24], max in [60,78,80,90]. Tuned EMA alpha in [.10,.22,.35,.55,.80], theta in [.25,.36,.45,.55]; tuned window width in [2,4,8,16], theta same; Bayes tuned threshold in [.20,.29,.40,.50] with energy urgency/max=14/80. All reported costs must include at least action count and fixed per-step algorithmic operation proxy; true wall/compute benchmarking not established.

## Development selection rule, fixed before evaluation
For each tunable family, grid-search independently on 3 seen DEV regimes. Optimize **unweighted macro average survival fraction** across the 3 regimes. Deterministic tie-break: larger macro mean living steps, then fewer mean strikes, then lexicographically lowest parameter tuple. No benchmark condition may be changed after seeing EVAL. Keep all grid candidates and selected configuration in record before running EVAL.

## Evaluation outcome reporting
Primary: per-regime survived-to-120 fraction. Secondary: mean living time, mean attacks, mean forages, paired seedwise survival difference between original emotion and (a) fixed instinct, (b) tuned instinct, (c) tuned EMA, (d) tuned window, (e) fixed generic Bayes, (f) tuned generic Bayes, and between emotion and literal EMA clone. Bootstrap seed-paired confidence interval by fixed auxiliary RNG for descriptive uncertainty, explicitly no multiplicity-controlled confirmatory inference. Report **every** seen and OOD regime and cross-regime reversal; don't average away failure.
Report whether original emotion actions and survival are identically reproduced by relabelled EMA and by the report-only proxy (software equivalence should be exact). Check that removing memory changes action on at least one seed (mutation sensitivity). Independence audit: no policy reads scenario name/hidden hazard; no controller changes RNG; no unpaired environment draws.

## Interpretation
Equivalent algorithms imply non-identifiability of "emotion" from these tasks, not that emotions biologically do not exist. A report label is not a phenomenal feeling. Persistence may be useful in persistent regimes and harmful under volatility. The protocol supports comparing **toy controllers**, NOT deciding which scientific research methodology (AES v2 vs six competitors) is strongest. Research #2 official freeze/19C fidelity remains untouched.
