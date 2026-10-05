# LIT-N1 addendum — backward citation trace

Search date: 2026-10-05
Parent audit: notes/lit_n1_novelty_screen_execution_v001.md

## Taylor et al. 2017/2020 — important forecasting predecessor, not DIRECT prior art

Sara Taylor, Natasha Jaques, Ehimwenma Nosakhare, Akane Sano, Rosalind Picard.
“Personalized Multitask Learning for Predicting Tomorrow’s Mood, Stress, and Health.”
IEEE Transactions on Affective Computing. DOI: 10.1109/TAFFC.2017.2784832.

Full-text HTML was inspected.

Key design facts:
- Forecasts tomorrow evening’s binary mood/stress/health labels using only day-t data.
- The paper formalizes its task as p(y_{t+1} | x_t), where x_t is smartphone, wearable sensor, behavioral survey, location and weather information from the current day.
- It explicitly contrasts this with prior self-report-history forecasting and states that its approach does not require users to input daily mood labels.
- 343 candidate features include 172 physiology features plus phone, location, behavioral survey, weather and other variables; selected 21-feature set includes physiology and behavior, but not today’s self-reported mood label as a predictor.
- Therefore there is no observed prior-affect persistence baseline to condition on, and no nested “history-only vs history+physiology” increment test.

Classification: CLOSE FORECASTING PREDECESSOR, NOT DIRECT.

## DeepMood / Suhara et al. 2017 — strong history-only predecessor, no physiology increment question

Suhara, Xu & Pentland, “DeepMood: Forecasting Depressed Mood Based on Self-Reported Histories via Recurrent Neural Networks.”
- Forecasts future depressed mood from self-reported mood histories.
- Prior literature reports that previous-day mood is the most important short-horizon predictor.
- This establishes the power of lagged affect history and prevents any novelty claim that “past affect predicts future affect.”
- It does not supply the peripheral-physiology incremental comparison central to our work.

Classification: HISTORY-BASELINE CONCEPTUAL PREDECESSOR, NOT DIRECT.

## Combined implication

The literature contains both sides separately:
1. physiology/behavior can forecast future mood without prior affect labels (e.g., Taylor et al.); and
2. prior self-reported affect history can be an exceptionally strong forecaster (e.g., DeepMood).

The under-tested intersection remains whether peripheral physiology adds prospective value once the strong observed-state/history baseline is explicitly available, especially for continuous self-report under held-person × held-stimulus generalization.
