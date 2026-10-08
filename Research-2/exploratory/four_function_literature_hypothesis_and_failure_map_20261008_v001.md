RESEARCH #2 — EXPLORATORY SCIENCE LOOP 1
Four-function virtual organism: maintenance, instinct, emotion-like state, and feeling report
Date 2026-10-08 | Status: Development result, not preregistered confirmation | Claim ceiling: software-functional distinctions only

I. RESEARCH QUESTION AND ROLE
Can self-maintenance regulation, innate/rapid cue-policy selection, temporally persistent emotion-like control state, and an accessible/reportable body-affect representation be separated by minimal executable interventions?
This is an explicitly chosen development case relevant to scientific methodology benchmarking. It does not replace Research #2's central AES v2-versus-competitors prospective experiment or reactivate a legacy consciousness program. No Research #2 AES decisive trial occurred.

II. TERMS AND SOURCE-GROUNDED COMPETING ACCOUNTS
(1) Self-maintenance: regulated bodily variables remaining inside viability bounds. Feedback/homeostasis and predictive allostasis are different control accounts; their distinction is debated. [Sterling 2012 DOI:10.1016/j.physbeh.2011.06.004.]
(2) Instinct: developmentally/evolutionarily biased sensor-to-behavior control (not necessarily immutable or learning-free). Ethology requires mechanistic, developmental, functional and evolutionary questions to be separated. [Tinbergen 1963 DOI:10.1111/j.1439-0310.1963.tb01161.x]
(3) Emotion: Adolphs treats emotions as biological functional states organizing behavior and separable from subjective experience; Scherer's appraisal component process theory places coordinated, dynamic appraisal at the center; Barrett's constructed emotion theory emphasizes interoception/prediction/categorization. These are rivals, not a consensus single definition. [Adolphs 2017 DOI:10.1093/scan/nsw153; Scherer 2009 DOI:10.1080/02699930902928969; Barrett 2017 DOI:10.1093/scan/nsw154]
(4) Feeling: Damasio and Carvalho interpret feelings as mental experiences of body states; LeDoux and Brown advance a higher-order theory of emotional consciousness; Seth and Friston relate affect to active interoceptive inference. Whether a computational reporter feels anything is not established. [Damasio & Carvalho 2013 DOI:10.1038/nrn3403; LeDoux & Brown 2017 DOI:10.1073/pnas.1619316114; Seth & Friston 2016 DOI:10.1098/rstb.2016.0007; Butlin et al 2026 DOI:10.1016/j.tics.2025.10.011]
These four are NOT proven sequential stages of evolution. Mechanisms overlap, and conscious feeling is not identified by an output label alone.

III. SEPARABLE HYPOTHESES AND FALSIFIERS
H0 Minimalist: viability feedback and cue/instinct rules are sufficient for the observed choice patterns. Falsifier: an equal-observation/equal-compute temporal integration mechanism generates reliable OOD advantages not available to the restricted fixed policy.
H1 Persistent functional emotion: a latent affect-like state integrates hazard evidence across time and causally changes action in a way the memoryless version cannot. Falsifier: delete its persistence or replace it with a simple risk estimator and recover equal behavior and performance.
H2 Predictive allostasis: anticipatory inference explains any benefit without a separate emotion-specific mechanism. Falsifier: after model privilege and resource costs are matched, emotion-specific control produces a replicable residual behavior prediction.
H3 Feelings-as-access: bodily and affective signals become accessible to reporting/metacognitive tasks. Falsifier for strong behavioral necessity: reporting added to isolated agent gives no survival advantage; however this is NOT a test of phenomenal feeling.
H4 Constructed/appraisal accounts: learned concepts and context evaluations predict transferable variation beyond undifferentiated arousal. Their mechanisms are NOT implemented in this v0.1 toy; they remain strong alternatives, not eliminated.

IV. MINIMAL COMPUTATIONAL MODEL (ASSUMPTIONS, NOT BIOLOGICAL LAWS)
Body x_t=(energy_t, health_t), viability I(x_t) = I[energy>0 AND health>0].
Exogenous hidden hazard h_t follows a two-state Markov chain. Public cue c_t has sensitivity 0.75 and false-positive probability 0.18.
All policies receive the same body variables and cue and choose the same two actions {forage, shelter}. They face pre-generated matched hazard, cue, attack and food draws.
Maintenance-only policy acts on energy deficit. Instinct policy combines energy urgency with current threat cue.
Emotion-like latent arousal m_t = 0.78 m_(t-1) + 0.22 c_t, used in a thresholded foraging decision.
Memory ablation changes m_t to c_t instantaneously.
Feeling/report proxy f_t=categorize(1 - 2*abs(energy_t-55)/55 - m_t); it has no feedback into behavior. This variable is report ACCESS, not subjective feeling.
Predictive policy updates P(h_t=1|c_1:t) by a two-state Bayes filter, but is PRIVILEGED with true regime transition rates; it is included as a strong conceptual rival, not a fair ranking comparator.

V. V0.1 EXECUTED DEVELOPMENT RUN
Code: Research-2/exploratory/virtual_organism_four_functions_v010.py
Results: Research-2/exploratory/virtual_organism_four_functions_v010_results.json
Office Eon run proc_937fb52b9be145ed9897 exit 0; rerun/self-test proc_09a16eb751eb4e7d96d3 exit 0.
Python 3.12 from existing Office isolated audit312 venv; standard library only, no API calls.
160 fixed development seeds per regime; 3 regimes; 120 time steps maximum; 6 policies; fully paired exogenous worlds.
Observed survival proportions:
- CALM: all policies 1.0000.
- PERSISTENT: maintenance .5875; instinct .7250; persistent emotion .9313; emotion+report .9313; predictive .9000; memory-ablation .7438.
- VOLATILE: maintenance .6062; instinct .9313; persistent emotion .8500; emotion+report .8500; predictive .9313; memory-ablation .9250.
These are DESCRIPTIVE, chosen-rule outcomes, not estimates of human or biological emotion. No methodology winner or formal hypothesis-test p-value.
Basic software checks all PASS: deterministic world, same action semantics, physiological bounds, memory ablation detected, feeling-report noncausal. They are insufficient for scientific validity.
Initial apparent context-specific advantage of persistence reverses in volatile hazard conditions. This undermines any universal 'emotion always improves survival' claim.
A report variable does not make the creature conscious and does not change its isolated survival.

VI. VALIDITY ATTACK / FAILURE LEDGER
F1: Hand-designed thresholds and regimes may tailor results. Interpretation restricted to this code and scenarios.
F2: Predictive comparator has privileged true Markov transition rates. Cannot rank it fairly against other policies; model privilege must be removed or disclosed.
F3: 'Emotion' may simply be low-pass risk memory; latent state NOT uniquely identified as emotion.
F4: 'Feeling report' is a symbolic label, not a measurement of experience; phenomenal claim BLOCKED.
F5: One task family, no independent model, no source-derived competitor policies, no held-out OOD/replication, no matched computation.
F6: Original four-function labels need construct validity and disambiguation from learning, appraisal, drives, motivational state, and interoceptive inference.

VII. EXACT NEXT TEST, PREDECISIVE
Build an independently reviewed, neutral body/world interface and compare a strong memoryless instinct, tuned finite-memory risk estimator, non-privileged Bayesian belief controller, learned appraisal/constructed-state agent, and report-access ablation on multiple publicly developed task families. Predeclare matched sensors/actions/resources and then reserve untouched test families. Separately continue full 19C/19G/19H source fidelity gates for six official research-method competitors.
No AES v2 decisive comparisons until finalist method contracts, independent knowledgeable-defender reviews, resource parity and frozen preregistration pass.

VERDICT: PARTIAL (functional simulation executed), UNDERDETERMINED (biological origin/phenomenal feeling), BLOCKED (methodology superiority).
