# LIT-01 novelty screen — initial results v001

Protocol commit: d446d20067da11cdf43372ce79a971768bcecfa1
Search date: 2026-10-05
Status: bounded screen completed across Exa/web searches; Scite MCP unavailable on connected plan, so this is NOT a completed multi-database systematic review.

## Provisional decision
NO_EXACT_MATCH_IN_BOUNDED_SCREEN.

Meaning: no screened paper was found that combines all of:
- future continuous self-reported valence/arousal target;
- observed recent self-report / parameter-free persistence baseline;
- peripheral physiology tested for incremental value above that baseline;
- strict out-of-person evaluation;
- out-of-stimulus/segment evaluation or equivalent joint generalization;
- multi-horizon prospective test;
- external replication.

This is not proof of uniqueness. Manuscript language should be “to our knowledge” and disclose the bounded search.

## Closest papers

### Asutay et al. — Affective calculus: The construction of affect through information integration over time
Emotion 21(1):159–174. DOI 10.1037/emo0000681.
Classification: PARTIAL / IMPORTANT PREDECESSOR.
- Four experiments modeled momentary valence/arousal from recent evocative input and prior affect.
- Study 4 recorded facial EMG, EDA, respiration, and pulse.
- Prior affect reliably predicted current affect.
- Physiology added predictive information: e.g. facial EMG/EDA/respiration terms contributed, and physiology-informed/combined models improved fit by AIC.
- Target is currently experienced affect after/within the trial; prior affect is previous-trial state. This is affect integration, not the strict future-window forecast under person×stimulus holdout used here.
Implication: We must NOT claim novelty for conditioning affect prediction on prior affect plus physiology. Our distinction is the incremental prospective benchmark and generalization design.

### Coles et al. 2025 — Big team science reveals promises and limitations of machine learning efforts to model physiological markers of affective experience
Royal Society Open Science 12:241778. DOI 10.1098/rsos.241778.
Classification: DIRECT METHODOLOGICAL PREDECESSOR.
- Twelve teams, peripheral nervous system prediction of self-reported valence/arousal.
- Across-subject, emotion, induction, and time validation.
- 100% of tests beat random baseline; only 46% beat training-mean baseline.
- Replacing physiology with random noise worsened selected models in 93% of tests, proving real physiology signal.
- Explicitly calls for stronger baselines preserving continuity, temporal variability, autocorrelation and subject-specific first-order statistics.
Implication: Our work can be framed as directly answering this baseline gap with observed-state persistence and strict prospective evaluation.

### Ringeval et al. / RECOLA continuous emotion prediction
Pattern Recognition Letters / RECOLA work, 2014–2015.
Classification: PARTIAL.
- Speaker-disjoint train/dev/test.
- Concurrent/time-continuous valence/arousal recognition using audio/video/ECG/EDA.
- ECG/EDA-only CCC is relatively low; multimodal context improves results.
- No observed last-self-report persistence baseline and not our future target contract.

### Joudeh et al. 2022/2023 — RECOLA ECG+EDA prediction
Classification: NON-COMMENSURATE HIGH-PERFORMANCE COUNTEREXAMPLE.
- Reports very high concurrent valence/arousal accuracy/CCC from ECG+EDA.
- Pipeline describes sample shuffling and 80/20 splitting of records from 18 subjects.
- No speaker-disjoint future forecast or persistence/lagged-label baseline.
Implication: Do not call these results wrong; explain that random sample splitting on dense continuous labels answers a different and easier generalization question.

### Autoregressive multimodal Transformer on Ulm-TSST (arXiv:2311.10119)
Classification: PARTIAL.
- Explicit temporal/autoregressive decoder and multimodal continuous valence/arousal.
- Autoregression uses past internal/predicted states, not an observed self-report persistence baseline.
- Task is continuous recognition aligned to annotations rather than the same prospective-window test.
- Removing physiology has little effect on valence in reported analyses, directionally compatible with limited valence increment.
Implication: temporal modeling itself is prior art; our novelty cannot be “autoregression.”

### EMAP temporal arousal work
Psychophysiology 2024, DOI 10.1111/psyp.14446.
Classification: PARTIAL.
- Large continuous arousal dataset and temporal modeling of physiology.
- Concurrent momentary arousal prediction; not an incremental forecast beyond prior observed arousal.
Implication: important evidence that temporal physiological information can matter under a different target.

### Affective inertia / autoregressive affect literature
e.g. Bagnara et al., Emotion 2025, DOI 10.1037/emo0001541.
Classification: FOUNDATIONAL PRIOR ART.
- Establishes substantial persistence/autoregression in repeated affect reports.
Implication: “affect persists” is not novel.

### Dynamic physiology / NARX work
e.g. PLOS ONE 2025 dynamic emotion-intensity estimation from cardiovascular/EDA/respiration.
Classification: COUNTERWEIGHT.
- Demonstrates physiology can support dynamic emotion modeling under particular tasks and model forms.
Implication: rules out any universal “physiology cannot forecast emotion” language.

## Novelty-safe manuscript statement
A defensible provisional wording is:

“To our knowledge, prior physiology-based affect-prediction work has not directly tested whether peripheral physiological signals improve prospective continuous affect forecasts beyond an observed recent-state persistence benchmark under simultaneous person and stimulus generalization. We test that incremental question explicitly and replicate the valence result in an independent dataset.”

The sentence must remain provisional until the final citation-chain screen is complete.

## Reviewer-risk conclusions
1. Affective calculus prevents a broad novelty claim about prior affect + physiology.
2. EPiC is the intellectual bridge and should be foregrounded, not treated as a competitor to hide.
3. RECOLA high-performance papers show why split design and baseline choice are central.
4. If the change-target attacks find physiology increment, the title/abstract must narrow to absolute-level forecasts.
5. If the change-target attacks are nonpositive across CASE and POPANE, the benchmark/identifiability contribution becomes substantially stronger.
