# Affect Forecasting Paper — claim/evidence matrix v001

Status: pre-manuscript research artifact. POPANE-R6 and CASE-D2 metric sensitivities pending when frozen.

| Candidate claim | CASE support | POPANE support | Current status / required wording |
|---|---|---|---|
| Recent observed affect is a very strong short-horizon predictor of future recorded continuous affect. | Yes, valence + arousal, 1/11/21/31 s. | Yes, valence, 1/11/21/31 s. | Replicated for valence; CASE additionally supports arousal. Phrase as prediction of recorded self-report, not latent affect dynamics. |
| Peripheral physiology does not robustly improve future affect LEVEL prediction beyond recent-state/context baselines under stringent generalization. | Yes under simultaneous unseen-person × unseen-video evaluation and Ridge/HGB stress tests. | Yes for valence under simultaneous held-person × held-segment evaluation, Ridge/HGB. | Core replicated claim. External replication is valence only. |
| Persistence can outperform physiology, not merely tie it. | Yes. | Strongly yes; R1 all horizons and both learners, participant bootstrap and R4 crossed uncertainty. | Core result. Report effect sizes/CIs rather than categorical “physiology fails.” |
| Physiology contains aligned affect signal even when it does not add prospective utility. | Supported by CASE real-vs-shifted controls. | NOT replicated: R3 found no detectable real-vs-shifted advantage for recent valence. | CASE-specific demonstration only. Do not describe this as externally replicated. |
| Physiology may still predict future changes even if it loses on level prediction. | D1: HGB-only positive cells, but no Ridge/HGB robust rescue; zero-change beats physiology everywhere. | R2: no external change increment; zero-change dominates at all horizons both learners. | Strong transition-based rescue not supported. Mention CASE model-specific signals transparently as exploratory. |
| External result is robust to uncertainty over both generalization axes. | CASE uses crossed subject×video bootstrap in D1 and pending D2. | R4 crossed participant×segment bootstrap strongly supports R1 at all 8 horizon×learner contrasts. | Strong support for external result. |
| All-feature physiology loses only because irrelevant/noisy channels dilute a useful physiological subsystem. | Not the main CASE question here. | R5 pre-authorized ECG-only, EDA-only, ICG/hemodynamic-only all fail to rescue, every horizon both learners. | This specific rescue is weakened in POPANE. Do not generalize to all possible feature engineering. |
| The result is not merely a linear-model artifact. | HGB stress tests do not rescue level/change result robustly. | HGB independently reproduces persistence dominance. | Supported. |
| The result survives scoring rules beyond MAE. | D2 pending. | R6 pending. | Do not claim until metric sensitivities resolve. |
| There is no target leakage from POPANE zero-phase ECG filtering. | N/A. | Audited: filtering occurs only after predictor-window slice; no sample at/after target start enters filter. | Supported; disclose retrospective historical-window processing. |
| POPANE uses genuine continuous self-reported valence. | N/A. | Data descriptor: electronic 1–10 valence scale adjusted as often as needed, signal recorded at 1 kHz alongside physiology. | Supported. |
| The result demonstrates physiology is irrelevant to emotion/feeling. | No. | No. | FORBIDDEN. |
| The result demonstrates body-independence of feeling. | No. | No. | FORBIDDEN. |
| The result demonstrates persistence causes feeling. | No. | No. | FORBIDDEN. |
| The result establishes a consciousness/phenomenal theory. | No. | No. | FORBIDDEN. |
| No prior paper has ever done this. | Bounded novelty screen found no direct match. | Same. | Do NOT claim global priority. Use: “we found no direct match in our bounded search” / “underexamined distinction.” |
| Persistence reflects affective inertia rather than measurement inertia. | Not identifiable. | Not identifiable. | LIMITATION: continuous rating dynamics may contribute. Claim forecasting of measured trajectories, not latent-state causation. |

## Evidence hierarchy

### Primary/strongest
1. Frozen CASE/O002 prospective level result.
2. Frozen POPANE-R1 independent valence replication.

### Post-primary adversarial evidence
3. CASE-D1 future-change attack.
4. POPANE-R2 future-change valence replication.
5. POPANE-R4 crossed participant×segment uncertainty.
6. POPANE-R5 pre-authorized physiology-family ablations.
7. POPANE-R3 alignment control — importantly NONSUPPORTIVE of external aligned-signal narrative.
8. POPANE-R6 metric/trajectory sensitivity — pending at freeze.
9. CASE-D2 metric/trajectory sensitivity — pending at freeze.

## Proposed contribution sentence if pending metric gates do not force narrowing

“We provide a replicated benchmark demonstration that, for short-horizon forecasting of recorded continuous affect under stringent person/stimulus generalization, peripheral physiological features may offer little or negative incremental predictive utility once recent observed affect is available, despite the broader literature showing that physiology can carry affect-related information.”

## If CCC produces a robust tracking rescue

Replace broad “forecasting dominance” wording with:
“Recent-state persistence minimizes point-forecast error more reliably, while physiology can improve concordant trajectory tracking in specific settings.”

## Mandatory limitations
- POPANE external replication is valence only.
- CASE and POPANE use continuous self-report devices whose response dynamics may contribute to persistence.
- Tested peripheral features/models do not exhaust physiology representations.
- Short horizons do not establish long-horizon forecasting behavior.
- Predictive increment is not causal necessity or mechanistic importance.
- Post-primary sensitivities must be labeled as such.
