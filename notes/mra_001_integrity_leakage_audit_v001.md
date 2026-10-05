# MRA-001 partial integrity / leakage audit

Date: 2026-10-05
Status: COMPLETED FOR CORE CASE O002 + POPANE-R1/R2 PIPELINES; R3/R5 outcome-dependent manuscript sections still pending.
Overall integrity verdict: INTEGRITY_PASS_WITH_SCOPE_CAVEATS.

## 1. Temporal separation — PASS

CASE O002 frozen contract:
- physiology predictor: [-10,-1) s relative to anchor in implementation;
- recent same-axis report: [-5,-1) s;
- future target: [0,5) s;
- therefore no annotation or physiology sample at/after target start enters predictors.
- later 11/21/31 s horizon tests shift the target forward within the same subject×video sequence.

POPANE:
- physiology predictor: [-10,-1] s;
- recent affect predictor: [-5,-1] s;
- target: [0,5] s and shifted future targets at 11/21/31 s effective predictor-end gaps.
- common anchors were restricted so all horizons remain inside the same subject×segment.
- no future affect sample is used in feature extraction.

## 2. Signal preprocessing — PASS

CASE:
- ECG/BVP filtering via sosfiltfilt is performed only on the already-sliced pre-target predictor window, so acausal filtering does not cross into the target interval.
- all physiology summary features are computed from the predictor slice only.

POPANE:
- ECG interpolation/filtering is restricted to the already-sliced physiology window.
- EDA/ICG/hemodynamic summaries likewise use only the predictor window.
- no target-window observations are used to construct physiological features.

## 3. Training/test isolation — PASS

CASE primary:
- leave-one-subject-out outer evaluation;
- Ridge tuning uses GroupKFold by training subject only;
- imputation/scaling/one-hot encoding are fitted inside training folds and then applied to held-out data.

CASE G1/G2:
- simultaneous unseen-person × unseen-video tests exclude every row from the test subject AND every row from the test video from training.
- video identity is omitted in the double-holdout models.

POPANE R1/R2/R4/R5:
- deterministic subject folds keep all rows from a person together.
- primary joint tests train on rows satisfying both: participant fold != test fold AND segment != held segment.
- test rows are the held participant-fold × held segment intersection.
- segment identity is omitted in the joint models.
- Ridge imputation/scaling/tuning are training-only; HGB imputation is training-fit.
- no participant or held-segment row enters training.

## 4. Outcome-dependent selection — PASS FOR FROZEN PRIMARY/REPLICATION CLAIMS

CASE O002 predictors/features/windows/model grid were frozen before CASE model outcome.
POPANE P0/P0b inspected access/schema only and explicitly stopped before observational data rows; R1 protocol was frozen before outcome values were analyzed.
R2 was frozen before the CASE D1 change-target outcome was known.
R4 uncertainty rule and R5 family definitions were frozen before their own outcomes.
Technical reruns changed implementation bugs only and did not alter scientific settings.

Post-primary analyses (B2/B3, D1, R2, R3, R4, R5) remain labeled exploratory/sensitivity as appropriate and cannot be presented as original confirmatory endpoints.

## 5. Technical-rerun audit — PASS WITH TRANSPARENT FAILURES

POPANE-R2 original run failed before scientific analysis because of a Python import path. Only the import path was changed; the successful rerun retained the frozen scientific protocol.

POPANE-R3 had two failed runs caused by pandas column-name/attribute collisions involving a column named "shift". Both failures were documented as NO SCIENTIFIC VERDICT. Corrections changed only explicit column access, not target, features, shift rule, folds, models, uncertainty or decisions.

These failures should be disclosed in the reproducibility supplement/change log, not hidden.

## 6. Time-normalization caveat — NOT TARGET LEAKAGE, BUT DEPLOYMENT ASSUMPTION

Both CASE and POPANE fitted context/physiology models use normalized position within the video/segment, computed with the full video/segment duration.

This does NOT use future affect values and is not label leakage. In structured elicitation experiments, stimulus/segment duration can be known metadata. However, in an open-ended real-time deployment, total future episode duration may be unknown.

Why it does not explain the central baseline result:
- the parameter-free persistence/no-change baselines do NOT receive this duration-derived normalized-time feature;
- the fitted context and physiology models DO receive it;
- despite this extra information, physiology-augmented models lose to persistence in the central comparisons.
Thus this assumption, if anything, makes the physiology models more advantaged rather than generating persistence dominance.

Manuscript requirement: describe normalized-time use and avoid implying direct deployability to indefinite streams without adaptation.

## 7. Construct/measurement caveat — IMPORTANT, NOT LEAKAGE

The target is future self-reported affect, not unobserved phenomenal affect itself.
Continuous report trajectories may contain:
- genuine affective inertia;
- response-device/motor inertia;
- cognitive/report smoothing;
- annotation dynamics.

The results establish forecasting behavior of the measured self-report trajectory. They do not identify which component causes persistence.
CASE H1/G2 longer gaps and POPANE's independent measurement context reduce, but do not eliminate, this interpretive ambiguity.

## 8. Missingness/QC — PREDECLARED, ACCEPTABLE WITH REPORTING

POPANE technical QC can exclude files for insufficient affect completeness or peripheral-signal completeness, but not for affect magnitude, physiology magnitude, model error or favorable outcome.
R1 observed 1,122 files, 1,115 usable, 7 excluded for peripheral missingness.
Manuscript should report this flow explicitly.

## 9. Current integrity conclusion

No unresolved target leakage or train/test contamination has been identified in the core CASE or POPANE evidence chain.

MRA integrity gate: PASS, with two scope caveats that must be explicit:
1. normalized-time relies on known episode duration metadata;
2. the construct is future reported affect and includes possible reporting dynamics.

These caveats constrain interpretation but do not explain away the replicated finding that simple recent-state persistence outperforms the tested physiology-augmented models.
