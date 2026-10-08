# Research #2 — Four-function virtual organism, adversarial Loop 2 report

Status: **open exploratory development / heldout within a developer-authored synthetic family**. Not the frozen AES v2 prospective Research #2 methodology evaluation. No biological or phenomenal-consciousness claim.

## Reproducibility chain and chronology

1. Protocol pre-execution: commit `80cf20ed2735268a86a92c9e87bade530b871f1b`, `Research-2/exploratory/four_function_v020_pre_execution_protocol_20261008.md`.
2. Implementation after pre-run unit check/repair: commit `72d1369b65947d6b3fd134f6c93cf55cb8fa03a6`, `Research-2/exploratory/virtual_organism_four_functions_v020.py`. Source SHA256 on Office: `8ed7d15a756e35a8d74b1228cddc311c882c11bef00633a81223a42bff43131e`.
3. Development-only grid selection before evaluation: commit `7fef61755813bb66211211103bbe6e3c4f51143d`, `Research-2/exploratory/virtual_organism_four_functions_v020_dev_config.json`; selected: instinct (urgent=10,target=60); EMA (alpha=.55,threshold=.25); sliding window (n=2,threshold=.25); generic Bayesian (threshold=.20).
4. First heldout Office Eon eval process `proc_8f512b02b8b1430499a0`, exit 0. Complete raw normalized results commit `e170e0985f457fb2cd6db049c17fea4e37c5a845`, `Research-2/exploratory/virtual_organism_four_functions_v020_evaluation.json`.
5. Independent second Eon process `proc_6152e77faf7a45f98d54`: the computation itself ran; a subsequent inline Python command failed owing to shell quoting (exit 1). Direct Eon PowerShell comparison subsequently confirmed **exact equality** between parsed JSON outputs, all 77 metric rows. Preserve both the initial command failure and successful comparison.
6. Eon Windows PowerShell output redirection initially generated UTF-16LE; it was converted to UTF-8 after the run solely for interoperable archival. Numerical result unchanged.
7. All six Research #2 official research-method comparators are still not fully certified; AES v2 itself has **zero prospective decisive trials**.

## Primary data: survival through 120 time steps, 256 paired heldout worlds per condition

| Condition | Instinct fixed | Instinct tuned | Original emotion label | Tuned generic EMA | Tuned window | Generic Bayes tuned |
|---|---:|---:|---:|---:|---:|---:|
| Calm (seen) | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| Persistent (seen) | .6953 | .7031 | .9102 | .9102 | .9102 | .9336 |
| Volatile (seen) | .8828 | .9102 | .8672 | .9102 | .9180 | .9023 |
| Persistent->volatile shift (OOD) | .7891 | .8203 | .8984 | .9219 | .9258 | .9297 |
| Volatile->persistent shift (OOD) | .7695 | .7695 | .8672 | .9102 | .9219 | .9297 |
| Unreliable threat cue (OOD) | .5430 | .5898 | .6758 | .6055 | .5898 | .5938 |
| Scarce food (OOD) | .5898 | .6289 | .8438 | .8164 | .8125 | .8164 |

Additional untuned generic Bayesian and maintenance controls and the complete 77-row results are in the machine-readable JSON. No row is omitted from the raw record.

Paired unadjusted bootstrap uncertainty examples for the original emotion-label agent minus comparator:
- Persistent vs tuned instinct: +.20703 [+.16016, +.26172].
- Persistent vs tuned EMA: .00000 [-.03125,+.03516].
- Volatile vs tuned window: -.05078 [-.10156,-.00391].
- Reversed hazard-shift vs tuned Bayesian: -.06250 [-.10547,-.02344].
- Unreliable warning vs tuned EMA: +.07031 [+.01562,+.12109].
- Scarce food vs tuned EMA: +.02734 [-.01172,+.07031].

These intervals describe uncertainty over the prescribed seeds inside an artificial probabilistic world; they do not estimate biological effect size or support uncontrolled multi-comparison significance claims. Best controller changes by scenario. The Bayesian controller no longer reads true environment transition rates, but uses a fixed guessed HMM and therefore retains different inductive assumptions and computational cost. Full compute parity NOT established.

## Direct mechanical identity and identifiability

The "emotion" v0.1 state uses
`m_t=(1-0.22)m_(t-1)+0.22*c_t`, initial `m_0=0`, then chooses forage iff energy<16 or (m_t<.36 and energy<78).

The explicitly ordinary EMA risk-memory controller uses exactly this same recurrence, initialization, and policy under a different label. For equal initial body, external cue, and matched draws, elementary induction yields equal latent state and action at every time step; hence equal bodily trajectories. Tests confirm equality in every examined condition. The symbol 'emotion' is not distinguishable from generic temporal integration under this task and implementation. It follows **neither** that biological emotion is impossible nor that risk estimation is its only mechanism. Rather, this software task cannot identify the construct.

A report-only readout labels a computed bodily/arousal proxy as pleasant, neutral or unpleasant; it does not feed into action. Its actions and survival are therefore exactly identical by design. **No inference whatsoever about phenomenal feeling** is warranted. Reporting absence of survival gain is not a negative biological test.

The memory-ablation controller replaces history by instantaneous cue; observed action changes verify persistence's causal effect under these rules. This is a narrow within-code intervention, not independent causal evidence of emotion.

## Literature-directed validity audit

- Anderson & Adolphs, Cell 157 (2014), DOI `10.1016/j.cell.2014.03.003`: cross-species functional emotion primitives include **persistence, scalability, valence, generalization**, and their causal relationship to behaviors. v0.2 tests persistence and limited continuous intensity, not positive/negative valence or transfer across stimuli/actions.
- Adolphs, SCAN 12 (2017), DOI `10.1093/scan/nsw153`: functional emotion states, conscious feeling, emotion concepts, and expression must not be conflated.
- Scherer, Cognition and Emotion 23 (2009), DOI `10.1080/02699930902928969`: appraisal/response synchronization rival not represented in this simple filter.
- Barrett, SCAN 12 (2017), DOI `10.1093/scan/nsw154`: constructed emotion via prediction and categorization; not faithfully modeled by report labels.
- Seth & Friston, Philosophical Transactions B 371 (2016), DOI `10.1098/rstb.2016.0007`: interoceptive inference and allostasis rival; crude Bayesian hazard tracking not its full model.
- Emanuel & Eldar, Neuroscience & Biobehavioral Reviews 144 (2023), DOI `10.1016/j.neubiorev.2022.104977`: computational emotion frameworks evaluate states, actions, uncertainty and prospects. Strong prior art prohibits labeling generic state evaluation as novel emotion definition.

**Four-layer functional map:** viability regulation: physiological bounds and need signals; instinct: cue-triggered default action tendencies; emotion-like state: temporally persistent graded internal modulation of several responses (the latter mostly untested); feeling: subjective experience, not measured by labels. Evolutionary chronology **not** inferred; these are analytically distinguishable functions, not a demonstrated biological four-stage tree.

## Adversarial conclusion and failure ledger

1. **Failure of uniqueness:** original 'emotion' equals an ordinary low-pass risk filter. Behavioral construct identification **FAIL/UNDERDETERMINED**, not a novel discovered emotional essence.
2. **Context reversal:** original gains on persistent threats, is worse than tuned window and tuned instinct under volatile threats, and trails generic Bayesian on both shift directions. There is no universal better controller.
3. **OOL/OOD stress:** original exceeds tuned filters when cues unreliable or food scarce, but this can follow from its hand-selected inertia and energy thresholds. It is not biological evidence.
4. **Report proxy:** readout only, no subjective feeling assay; feeling origin remains **BLOCKED**.
5. **Inference limitations:** 256 heldout seeds per synthetic condition, code and world from the same developer; no external lab, source-native theory competitors, sealed transfer, or matched compute/time budget. Methodology victory **NOT TESTED**.
6. **Software issues preserved:** first pre-run v0.2 source failed import of dataclass-containing prior module because it was not added to sys.modules; fixed before committing code or tuning. Second-run verification's command-line quoting failed; comparison later succeeded. Neither failure concealed.

## Next executable study

Design v0.3 **emotion-primitives construct-validity assay**, separate from the six research-method arm preparation:
- independent threat and reward cues; at least two outcome channels/actions; graded intensity, opposed valence, persistence after cue cessation, context generalization.
- strongest fair opponents: calibrated memoryless reflex, generic vector-valued EMA, finite-memory model, learned value state, explicit multi-component appraisal and non-privileged predictive/interoceptive regulation, all seeing same inputs and using matched resource budgets.
- causal ablations for persistence, valence, cross-context sharing, representation and report access; identify counterexample cases.
- preregister all task-family splits and decision criteria before execution; independent knowledgeable defender review; allow EQUIVALENT/UNDERDETERMINED.
- only then treat this as a rigorous **research-case benchmark candidate**, not as evidence AES v2 wins any Research 2 methodology tournament. The six-method fidelity gate and prospective tournament remain pending.

End-of-loop: Mechanism identified as an EMA filter, not uniquely emotion. Biological feeling UNDERDETERMINED. Research-method tournament BLOCKED. No decisive AES v2 studies.
