# Affect Forecasting Manuscript — Methods and Results Draft v001

Status: authorized manuscript draft after PAPER-G1 readiness 3/3. This draft is constrained to immutable protocols/result snapshots and the frozen claim-evidence matrix. It does not make causal or phenomenal claims.

## Methods

### Study question and design
We tested a prospective benchmarking question: when recent observed continuous affect is available, do peripheral physiological features provide robust incremental information for forecasting future recorded affect? This differs from contemporaneous affect recognition. The primary analysis used CASE and evaluated valence and arousal. POPANE Study 6 served as an independent external replication for valence.

Predictors were restricted to information preceding the future target window. Forecast gaps are defined from the end of the predictor window to the start of the 5-s target window; the tested gaps were 1, 11, 21, and 31 s. Generalization was evaluated across held-out people and stimuli/segments rather than by random sample splitting.

### Datasets
CASE was the primary public-dataset analysis and supplied continuous valence and arousal ratings together with peripheral physiology. The paper treats these continuous ratings as recorded affect reports, not direct measurements of phenomenal experience.

POPANE Study 6 was the independent replication dataset (DOI 10.1038/s41597-021-01117-0; OSF DOI 10.17605/OSF.IO/94BPX). Its archive provenance was independently frozen in the project manifest (SHA-256 a5db8dd9b57fb1cd1ad799b635f4e59c9edaeb8481285a9e1fbef3522e998140). POPANE provided continuous self-reported valence and peripheral physiological channels. External replication is therefore valence-only.

### Forecasting baselines and models
The critical comparator was recent observed affect: a naive recent-state/persistence forecast and, where specified, a fitted context model based on prior affect/time information. Peripheral-physiology models used the frozen historical-window representations defined before outcome inspection. Ridge regression provided a linear learner and histogram gradient boosting (HGB) supplied a nonlinear stress test.

The inferential quantity was prospective performance relative to the strong state-history comparator, not whether physiology carried any affect-related signal in isolation. Primary scoring used MAE; post-primary frozen sensitivities used RMSE and concordance correlation coefficient (CCC).

### Generalization and uncertainty
CASE included stringent unseen-person/unseen-video evaluation. POPANE used simultaneous held-person × held-segment evaluation. The external result was subsequently attacked with a crossed participant × segment bootstrap that independently resampled both generalization axes and recomputed equal observed participant×segment-cell contrasts.

### Frozen post-primary attacks
After the primary level-forecasting results, we froze separate adversarial analyses before inspecting their outcomes: (i) future-change targets, testing whether physiology predicted transitions missed by persistence; (ii) real-versus-time-shifted alignment controls; (iii) crossed uncertainty over participant and segment; (iv) pre-authorized ECG-only, EDA-only, and ICG/hemodynamic-only ablations; and (v) RMSE/CCC metric and trajectory sensitivities. Technical failures that occurred before a verdict statistic was completed were logged as technical-only; scientific protocols were not changed after outcome inspection.

### Reproducibility and claim boundaries
Frozen protocols, analysis code, workflow identifiers, artifacts, checksums, result snapshots, failure audits, and the claim-evidence matrix are preserved in the project repository. The analyses test predictive increment only. They do not test whether physiology is causally necessary for affect, whether feelings are body-independent, whether persistence causes feeling, or any claim about phenomenal consciousness.

## Results

### Recent affect dominated short-horizon level forecasting in CASE
Across the tested 1-, 11-, 21-, and 31-s forecast gaps, recent observed affect was a strong predictor of future recorded valence and arousal. Under the project's stringent person/stimulus generalization tests, the tested peripheral-physiology representations did not provide a robust prospective improvement over recent-state/history baselines. The result survived linear and nonlinear learner checks and stronger simultaneous held-person × held-video evaluation.

This result is deliberately phrased as a forecasting benchmark result. It does not identify whether the persistence arises from latent affective inertia, continuous-rating dynamics, or both.

### Independent POPANE valence replication
POPANE Study 6 independently reproduced the central valence result under simultaneous held-person × held-segment generalization: recent-state persistence outperformed the tested physiological models across all four forecast gaps and for both Ridge and HGB. The external replication therefore supports the bounded claim that, in these continuous-affect forecasting settings, peripheral physiology did not add robust prospective value once recent affect/context was available. POPANE does not provide an arousal replication.

### Future-change attacks did not provide a robust physiology rescue
CASE-D1 yielded a frozen verdict of MIXED_CHANGE_RESULT. HGB showed positive physiology increments over the fitted context model in a small number of horizon/axis cells, but Ridge did not confirm those gains. No horizon × affect-axis cell satisfied the preregistered cross-model rescue criterion. More strongly, the parameter-free zero-change baseline beat physiology for both affect axes, all four horizons, and both learners; every bootstrap 95% interval for the zero-change-versus-physiology contrast excluded zero in favor of zero-change.

The independent POPANE-R2 change analysis was cleaner. Its frozen verdict was NO_EXTERNAL_CHANGE_INCREMENT with strong zero-change dominance. At every horizon and for both learners, physiology was significantly worse than both zero-change and fitted prior-affect/time context. For example, context-minus-physiology MAE contrasts were -0.00819 (95% CI -0.01018 to -0.00644) for Ridge and -0.01025 (-0.01404 to -0.00654) for HGB at 1 s; by 31 s they were -0.02320 (-0.03260 to -0.01487) and -0.04719 (-0.06586 to -0.02931), respectively. Thus an independent transition-based rescue was not supported.

### External result survived crossed uncertainty
POPANE-R4 independently resampled participants and held-out segment labels over 1,115 observed participant×segment cells. Persistence remained significantly better than physiology for both learners at every horizon. The naive-minus-physiology MAE contrasts were -0.03772 (95% CI -0.06296 to -0.02886) and -0.05538 (-0.06537 to -0.04601) at 1 s for Ridge and HGB, respectively, and -0.12616 (-0.19122 to -0.09254) and -0.17250 (-0.21161 to -0.13813) at 31 s. All eight intervals were strictly negative.

### No peripheral physiology family rescued the POPANE result
The pre-authorized POPANE-R5 ablation tested ECG-only, EDA-only, and ICG/hemodynamic-only representations. No family × horizon combination satisfied the rescue criterion for both learners; family-versus-context intervals were negative across the tested horizons and learners. This weakens the specific explanation that the all-channel result was caused merely by dilution from unrelated physiological channels, while leaving open other feature representations and modalities.

### Metric and trajectory sensitivities preserved the main result
POPANE-R6 found physiology worse than persistence on both RMSE and CCC at all four horizons for both Ridge and HGB (METRIC_ROBUST_PERSISTENCE_DOMINANCE).

CASE-D2 was conservatively labelled MIXED_METRIC_RESULT because one RMSE interval was inconclusive. Nevertheless, physiology-minus-persistence CCC was unfavorable to physiology in all 16 horizon × axis × learner cells, with every 95% interval excluding zero. RMSE point estimates favored persistence in all 16 cells and 15/16 intervals excluded zero. The sole inconclusive cell was 21-s arousal with HGB: naive-minus-physiology RMSE = -0.05897, 95% CI -0.14714 to +0.00201. There was therefore no CCC trajectory-tracking rescue and no RMSE reversal of the central result.

### Alignment controls delimit, rather than broaden, the conclusion
CASE real-versus-shifted controls supported the presence of aligned physiological affect signal despite absent incremental forecasting value. That distinction did not externally replicate in POPANE-R3: Ridge real-versus-shifted delta was +0.00162 (95% CI -0.00444 to +0.00932) and HGB was +0.01199 (-0.00250 to +0.02623), yielding NO_DETECTABLE_ALIGNED_SIGNAL. Accordingly, the paper treats “aligned physiology signal without incremental prospective utility” as CASE-specific rather than a replicated finding.

## Results synthesis
Across two public continuous-affect datasets, recent observed affect/history was an exceptionally strong short-horizon benchmark. The central non-increment/persistence-dominance pattern externally replicated for valence and survived nonlinear learners, future-change targets, crossed uncertainty, physiology-family ablations, RMSE, and CCC. The evidence does not establish physiological irrelevance: it establishes that the tested peripheral-physiology representations did not robustly improve prospective prediction after strong recent-state/context baselines under the tested generalization regimes.

## Mandatory limitations carried forward
1. POPANE replication is valence-only; CASE arousal is not externally replicated.
2. Continuous-rating response dynamics may contribute to persistence and are not separable from latent affective inertia in these data.
3. Tested physiology features and learners do not exhaust possible representations or models.
4. The tested horizons are short and do not establish long-horizon behavior.
5. Post-primary attacks are labelled as such.
6. Predictive redundancy is not causal or mechanistic irrelevance.
7. Recorded self-report trajectories are not equivalent to phenomenal experience.
