# LIT-01 Systematic novelty screen protocol

Frozen: 2026-10-05, after POPANE-R1 level replication and before O002-D1 / POPANE-R2 change-target outcomes.

## Question
Has prior human research already demonstrated the same combined result as this project: prospective prediction of continuous self-reported valence/arousal from peripheral physiology, evaluated incrementally against an observed recent-affect/persistence baseline, under out-of-person and preferably out-of-stimulus generalization?

## Sources
1. Scite literature index.
2. Exa/web search for recent/preprint work and papers not indexed in Scite.
3. Citation chaining from the closest papers, especially Coles et al. 2025 (EPiC), continuous-emotion autoregressive models, RECOLA, CASE, and affective-inertia work.

## Date range
2010 through 2026-10-05, with emphasis on 2018 onward.

## Search concepts
A. ("continuous affect" OR "continuous emotion" OR valence OR arousal) AND (physiology OR ECG OR EDA OR "peripheral nervous system") AND (forecast* OR predict* OR prospective)
B. ("prior affect" OR "lagged affect" OR autoregressive OR persistence OR "last value") AND (physiology OR wearable) AND (valence OR arousal OR mood)
C. ("temporal autocorrelation" OR persistence OR continuity) AND ("emotion recognition" OR "affect prediction") AND baseline
D. ("subject independent" OR "leave one subject out") AND ("stimulus independent" OR "leave one stimulus out") AND physiology AND emotion
E. citation neighbors of DOI 10.1098/rsos.241778 and major continuous-affect benchmark papers.

## Inclusion
- Human empirical study or benchmark.
- Subjective affect/emotion is an outcome, preferably continuous/dense valence/arousal.
- Peripheral physiology is modeled or explicitly ablated.
- Predictive evaluation is reported.
- Strong relevance if prior observed affect/lagged label/persistence is a comparator or covariate.

## Exclusion / separate-context bucket
- Discrete emotion classification only, unless methodologically relevant to generalization/baselines.
- Brain-only / fMRI/EEG-only unless peripheral physiology is also tested.
- Retrospective clip-level ratings only with no temporal forecasting.
- Studies using only previous model predictions rather than observed prior self-report are related but not exact matches.
- Concurrent recognition is related but not an exact prospective match.

## Extraction
For every close paper record:
- DOI/title/year/dataset/sample.
- Concurrent vs future target and forecast horizon.
- Outcome source: self-report vs observer annotation.
- Physiology channels.
- Prior-affect/persistence baseline present? exact definition.
- Split unit: random samples / time / person / stimulus / double holdout.
- Does physiology add incremental accuracy beyond prior affect?
- Exact-match classification: exact / partial / methodological predecessor / not comparable.
- Any leakage or commensurability concern stated neutrally.

## Novelty decision
Do NOT claim uniqueness merely because no exact match is found.
- PRIOR_EXACT_MATCH_FOUND: at least one paper implements essentially the full contract and reaches the same core conclusion.
- NO_EXACT_MATCH_IN_BOUNDED_SCREEN: no exact match found after protocol search; phrase manuscript novelty as “to our knowledge” and describe search scope.
- AMBIGUOUS: candidate paper cannot be classified without unavailable full text/data.

## Firewall
Novelty search does not alter empirical decision rules. Literature unfavorable to the project must be retained, not filtered out.
