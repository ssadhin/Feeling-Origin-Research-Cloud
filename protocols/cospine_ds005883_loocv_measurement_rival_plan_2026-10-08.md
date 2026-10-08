# CoSpine ds005883 exploratory out-of-sample measurement-rival audit — plan recorded 2026-10-08 07:31 +06

Scope: Feeling Origin only. Prior CoSpine results already inspected on 2026-10-08, so this is **not** an independent preregistration, blind confirmatory test, or new proof claim. This plan is committed before the *new LOOCV metric* is calculated. Existing frozen pre-outcome plan: Google Doc 1SZnO_4YFMUKcHE-PmAhcabDrZ1bxcFimpRHsA3AWPR0; source data pinned to OpenNeuroDatasets/ds005883 commit 037ed267e7f7f2024a5fe3d0e8fb4759f7f67bdd.

Question: does within-person intensity-to-unpleasantness structure generalize to held-out trials, or does a post-fit exact-bin residual mostly reflect noise/overfitting? This is a *measurement* audit, not a neural mechanism test.

Independent implementation: retrieve all 39 sub-XX_task-pain_events.tsv files from pinned commit; use only pain rows with numeric PR and UpR; no imputation/exclusion. Independently recompute centered sums, pooled correlation, common slope residual, person-specific slope residual, and exact-bin conditional residual; compare with earlier recorded aggregates.

Exploratory trialwise LOOCV, within each subject: train on other 14 pain trials, predict held-out unpleasantness UpR from PR.
- A = subject mean of UpR (excluding held-out).
- B = least-squares intercept + slope using PR, fallback to A if PR training variance is zero.
- C = exact PR-bin training mean UpR if matching bin has at least one training point; otherwise fallback to B.
No tuning, clipping, imputation, or trial deletion. Evaluate pooled squared-error mean/RMSE and subject-level wins B>A, C>B; also count fallback trials. Avoid inferential p-values unless separately specified.

Build: systematic intensity/unpleasantness divergence might be reflected in a reproducible nonlinear mapping. Attack: in-sample conditional residual is guaranteed nonnegative and can arise entirely from rating noise/discretization; LOOCV may fail or succeed without implying phenomenality. Further exact-bin residual is invariant to permutations of UpR within each subject's PR bins; it cannot by itself identify temporal dynamics or a causal mechanism.

Kill conditions: if C does not beat B in LOOCV, reject claims of a reliable bin-specific nonlinear mapping from this dataset; if B does not beat A, reject even a reliable within-subject linear mapping under this validation. Even if either succeeds, reject claims that this identifies M or P. Causal selectivity, sensory equivalence, reverse reasoning/access dissociation, neural held-out rival comparison, and independent replication remain absent.

P=phenomenal presence; S=affective significance; neither equals sensory intensity, valuation, autonomic response, bodily regulation, report, metacognition, access or reasoning. The ownership-dependent F=(G*C*S*O)^(1/4) equation remains rejected; ownership not assumed necessary. Report-to-experience bridge assumption is explicit and cannot provide strict third-person proof.

Next after audit: assess held-out neural/physiology predictors only after source QC and independent ROI freeze; seek causal double dissociation. Preserve all nulls. Publication-readiness: FAIL until formal M survives rivals, causal interventions, replication.