# LIT-N1 Frozen novelty-search protocol — persistence vs physiology in prospective affect forecasting

Status: FROZEN BEFORE FORMAL SEARCH EXECUTION
Freeze date: 2026-10-05

## Research question
Has prior empirical work already tested whether peripheral physiological signals add prospective predictive value for future continuously/densely self-reported affect (valence/arousal or closely related subjective affect) after conditioning on an observed recent-affect / lagged-label / persistence baseline, under participant-independent evaluation?

Secondary novelty dimensions:
1. strict future target separated from predictor window;
2. explicit last-value / lagged observed-affect comparator;
3. incremental physiology-ablation or nested comparison;
4. held-out-person generalization;
5. held-out-stimulus/condition generalization;
6. multi-horizon forecasting;
7. continuous/dense own subjective affect rather than external annotator labels;
8. real-vs-shifted physiology signal control;
9. external replication.

## Sources
Primary academic search: scite literature index.
Supplementary discovery/verification: Exa/web academic search and publisher/DOI pages when needed.
Cutoff: 2026-10-05.
Years: 2000–2026, with no language exclusion at title/abstract stage if English metadata are available.

## Frozen search families
A. ("affect" OR emotion OR valence OR arousal OR mood) AND (forecast* OR predict* OR "future") AND (physiolog* OR ECG OR EDA OR HRV OR wearable) AND ("self-report" OR subjective) AND (lagged OR autoregressive OR persistence OR "past label" OR "previous rating")

B. ("continuous emotion" OR "continuous affect" OR valence OR arousal) AND (physiolog* OR ECG OR EDA) AND (autoregressive OR temporal OR persistence OR lagged) AND (forecast* OR prediction)

C. ("momentary affect" OR mood OR valence OR arousal) AND (wearable OR physiolog*) AND ("prior affect" OR "previous affect" OR "lagged affect" OR "past labels") AND (incremental OR ablation OR baseline)

D. ("emotion recognition" OR "affective computing") AND physiolog* AND (baseline OR benchmark) AND (autocorrelation OR continuity OR persistence OR temporal)

E. Citation-neighborhood search around:
- Coles et al. 2025, DOI 10.1098/rsos.241778
- Pounds et al. 2026, DOI 10.1109/CHASE69719.2026.00088 / medRxiv 10.64898/2026.04.29.26352047
- Barradas et al. 2025, DOI 10.1371/journal.pone.0315929

## Inclusion criteria
Include for full-text/close abstract review if a paper:
- predicts a human subjective affect/emotion/mood outcome, AND
- uses peripheral physiology/wearables as predictive input, AND
- is temporal/prospective OR has enough temporal design detail to plausibly address incremental forecasting, AND
- reports an empirical evaluation.

Flag as DIRECT PRIOR ART only if it explicitly compares physiology against a model/baseline containing observed prior subjective affect (or an equivalent last-value persistence predictor) for a future affect target.

Flag as CLOSE PREDECESSOR if it has at least 3 of the following but misses the direct comparison: future target; past affect labels; physiology; participant-independent split; continuous/dense self-report; stimulus-generalization; explicit baseline/ablation.

## Exclusion criteria
Exclude from direct-prior-art classification if:
- only concurrent emotion recognition/classification;
- target labels are only stimulus categories with no subjective affect;
- physiology is absent;
- past affect is not observed / only past model hidden states are used;
- no empirical evaluation;
- review/editorial only (may retain as contextual source);
- external observer annotations only, unless clearly relevant as methodological predecessor.

## Extraction fields
For every retained direct/close paper:
- citation/DOI/year;
- sample size and dataset;
- target construct and label source;
- target timing/horizon;
- predictor timing;
- physiology channels;
- whether observed prior affect/labels are inputs;
- whether a last-value/past-label-only baseline is reported;
- physiology incremental comparison result;
- participant split;
- stimulus/condition split;
- model families;
- primary metric;
- relevance classification: DIRECT / CLOSE / CONTEXTUAL / EXCLUDED;
- exact reason.

## Decision rule
Novelty survives in bounded form if no DIRECT prior-art paper is found after:
1. all five search families;
2. at least the first 50 relevance-ranked scite hits across A–D combined (deduplicated);
3. citation-neighborhood review around the three seed papers, where scite coverage is adequate;
4. supplementary web/Exa search for 2025–2026 forecasting papers.

If a DIRECT paper is found, do not claim novelty for the overlapping component. Reframe around whatever dimensions remain distinct.

No "first study" wording is allowed solely from this search. Permitted wording after a clean search: "we found no prior study in our bounded search that..." and "an underexamined distinction."
