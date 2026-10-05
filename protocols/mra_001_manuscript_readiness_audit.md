# MRA-001 Frozen manuscript-readiness audit

Status: FROZEN BEFORE POPANE-R3/R4/R5 OUTCOMES
Date: 2026-10-05

## Objective
Decide whether the current Feeling Origin affect-forecasting branch is ready to become a manuscript, and exactly what claim is scientifically defensible.

## Required evidence blocks

### A. Core empirical chain
1. CASE primary/replication result and exact frozen endpoint.
2. Evidence that physiology contains real aligned affect information (not only noise).
3. Strong recent-state/persistence baseline.
4. Longer-horizon stress.
5. Joint unseen-person × unseen-stimulus evaluation.
6. Model-class sensitivity.
7. Independent POPANE valence replication.
8. Level-vs-change target attack.
9. POPANE R3 alignment-signal control.
10. POPANE R4 crossed participant×segment uncertainty.
11. POPANE R5 physiology-family ablation if completed.

### B. Preregistration / timing classification
Every reported analysis must be labeled one of:
- frozen confirmatory before outcome;
- frozen external replication before external outcome;
- post-primary sensitivity explicitly pre-authorized;
- exploratory/post-primary;
- technical correction with no scientific-design change.

No exploratory result may be rhetorically upgraded to confirmatory evidence.

### C. Leakage audit
Verify and report:
- predictor physiology ends before target starts;
- prior self-report ends before target starts;
- preprocessing/imputation/scaling/tuning fitted on training data only;
- participant leakage absent;
- held-out stimulus/segment absent from training in joint tests;
- horizon shifts stay within subject×stimulus/segment;
- no target-derived feature selection;
- technical reruns did not change scientific settings.

Any unresolved leakage = NOT MANUSCRIPT READY.

### D. Statistical audit
Required:
- primary metric and estimand stated explicitly;
- uncertainty unit justified for repeated observations;
- R4 crossed uncertainty reported as sensitivity for POPANE joint generalization;
- no dichotomous "no effect" interpretation from a CI merely crossing zero;
- post-primary multiplicity acknowledged;
- model/family/horizon screens not cherry-picked;
- effect direction and magnitude reported, not only p/CI sign;
- no equivalence claim unless an effect-size margin was frozen independently.

### E. Construct audit
Distinguish:
- latent/experienced affect;
- participant's reported affect trajectory;
- continuous response-device dynamics;
- peripheral physiological activity.

The paper's empirical target is future SELF-REPORTED affect, not phenomenality itself.
Observed report-state persistence may contain true affect inertia, rating-device/motor inertia, smoothing, or all three.
No causal generator claim is allowed.

### F. External-validity audit
State explicitly:
- CASE: valence + arousal internal evidence.
- POPANE: independent valence evidence.
- no independent dense-self-report arousal replication currently available to the project.
- both major datasets are structured/elicited contexts; do not universalize to all real-world affect.
- tested horizons are short (1/11/21/31 s).

### G. Novelty audit
Use frozen LIT-N1 protocol and disclose its execution limitations.
At minimum discuss:
- Coles et al. 2025 EPiC big-team benchmark;
- D'Amelio et al. 2023 CASE temporal physiology benchmark;
- Beatton et al. 2024 positive affect + HRV with prior feeling control;
- Barradas et al. 2025 dynamic physiology/NARX emotion intensity;
- Pounds et al. 2026 next-minute physiology + past-label forecasting;
- current longitudinal affect-inertia/forecasting work.

Forbidden novelty language unless a fully executed systematic search supports it:
- "first study"
- "unique"
- "no prior work"

Permitted bounded language:
- "replicated benchmark demonstration"
- "underexamined conditional-information question"
- "in our bounded search, we found no prior study matching the full evaluation contract"

### H. Causal / phenomenality firewall
Forbidden conclusions:
- physiology is irrelevant to emotion or feeling;
- the body does not matter;
- physiology never predicts affect;
- recent self-report causes future feeling;
- feelings are body-independent;
- any consciousness/phenomenality identity claim.

Allowed:
- statements about out-of-sample prospective predictive increment under the tested measurements, models, datasets and horizons.

### I. Reproducibility audit
Must list:
- dataset citations/licenses;
- protocol commits;
- analysis commits;
- workflow commits;
- run IDs;
- artifact IDs/digests;
- permanent aggregate result snapshots;
- technical failure audits and correction commits;
- exact environment/dependency bounds;
- code sufficient to rerun from public/authorized data;
- raw restricted/licensed data not redistributed.

### J. Paper-readiness classification
MANUSCRIPT_READY_CANDIDATE only if:
1. no leakage/integrity failure;
2. independent POPANE R1 result remains supported after R4;
3. R2 does not reveal a robust independent transition rescue that contradicts the proposed claim;
4. R3 is either positive aligned-signal evidence OR, if null, manuscript wording explicitly avoids asserting external physiology signal;
5. R5, if completed, has no model-robust family rescue; if it does, claim is narrowed before manuscript drafting;
6. novelty is phrased as bounded benchmark contribution;
7. all post-primary analyses are labeled;
8. arousal external-replication limitation is explicit.

If R5 is still running when all other gates pass, status may be MANUSCRIPT_DRAFTABLE_PENDING_FAMILY_SENSITIVITY, not final ready.

## Candidate claim to evaluate, not assume
"Across two continuous self-report datasets, recent observed affect provides a strong short-horizon prospective benchmark. Under the tested peripheral features and generalization regimes, adding physiology does not improve—and often worsens—future affect-level prediction; in independent POPANE valence, the pattern also extends to future-change targets. This separates physiological affect-related signal from incremental forecasting utility."

This wording must be narrowed if R3/R4/R5 contradict any component.
