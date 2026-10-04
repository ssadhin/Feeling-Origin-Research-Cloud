# Loop 005 — Causal Route Mapping and Degeneracy of Felt Affect

## Status

**Opened after formal closure of CRFI as a distinct theory.**

CRFI is retained only as synthesis/engineering vocabulary and historical benchmark. Loop 005 does not attempt to rescue CRFI or replace it immediately with a new identity theory.

## Core question

> Which causal routes are necessary, sufficient, substitutable, redundant, or merely modulatory for felt affect in humans?

The first target is not metaphysical identity. It is an intervention-constrained causal atlas.

## Why this loop exists

Loop 004 ended with:
- V014 behavioral uniqueness FAIL;
- prior-art collisions across GNWT, RPT, IIT, N*, HOTEC, Damasio/Carvalho, Seth/Friston, Solms, self-representational/reflexive affect theories and MEM;
- theory discrimination audits with strong conceptual divergences but no V015-admissible experiment;
- theory-to-data identifiability FAIL_NO_COMMON_IDENTIFIABLE_DATASET;
- CRFI reduction audit REDUCE_TO_SYNTHESIS_FRAMEWORK with zero distinct surviving commitments.

Loop 005 therefore changes the objective from “discover one new mechanism” to “map the causal routes and bottlenecks that survive direct human intervention evidence.”

## Evidence classes

Every evidence item must be labeled as one or more of:

1. **Necessity challenge** — lesion/blockade/deafferentation with the target feeling preserved.
2. **Causal participation** — direct perturbation changes a feeling or a feeling-relevant state.
3. **Partial sufficiency** — direct perturbation can evoke a reported affective state, with network-spread caveats.
4. **Modulation** — perturbation changes intensity/probability/quality without proving necessity.
5. **Route substitution** — target feeling survives loss of a canonical route via another elicitation pathway.
6. **Physiology–feeling dissociation** — emotion-related physiology changes while subjective emotion is absent.
7. **Network propagation** — stimulation of one site rapidly recruits a broader network, blocking isolated-node sufficiency inference.

Behavioral proxies alone do not count as direct evidence of feeling.

## Causal Route Atlas v001 — frozen evidence set

Protocol: `protocols/causal_route_atlas_v001.json`
Protocol commit: `6c0a7dcea25cbf272793843d206eff8efb6009a3`
Executable: `analysis/causal_route_atlas_v001.py`
Executable commit: `af9d41843037bb6ac046b6df891dc158506a7f87`
Workflow support commit: `f9bfc6d989f1632a903ec1fa886a10a8b3bee073`

### Amygdala

**Bilateral lesion / CO2**
- Feinstein et al. 2013, Nature Neuroscience, DOI 10.1038/nn.3323.
- Three people with focal bilateral amygdala damage experienced CO2-evoked fear and panic.
- This refutes the universal claim that the amygdala is necessary for all human fear/panic.
- It does not remove the amygdala's strong role in exteroceptive and anticipatory fear.

**Bilateral lesion / isoproterenol**
- Khalsa et al. 2016, Frontiers in Human Neuroscience, PMCID PMC4804013.
- Peripheral beta-adrenergic stimulation produced anxiety in both tested bilateral-amygdala lesion patients and full panic in one.
- This strengthens the case for an amygdala-independent interoceptive aversive route.

**Direct stimulation**
- Inman et al., PMID 29551365 / PMCID PMC6139084.
- Nine epilepsy patients: amygdala stimulation reliably produced dose-dependent electrodermal increases and HR deceleration.
- Subjective emotional responses occurred only in a minority (2/9).
- This is a direct physiology–feeling dissociation: amygdala-driven defensive autonomic output is not equivalent to felt emotional presence.

### Insula

**Complete bilateral destruction**
- Damasio et al. 2013, Cerebral Cortex, DOI 10.1093/cercor/bhs077.
- Patient B had complete bilateral insular destruction and extensive additional limbic damage yet retained broad body and emotional feelings.
- This is a strong counterexample to the insula as an exclusive universally necessary feeling platform.
- It is a single case and does not establish normal-population equivalence.

**Direct stimulation**
- Intracranial stimulation work (PMCID PMC10893903) shows insular sites can evoke visceral/autonomic sensations and, less frequently, anxiety/foreboding.
- This supports causal participation, not global necessity or isolated sufficiency.

### Distributed limbic/operculo-insular routes

**Large direct-stimulation dataset**
- 12,088 bipolar stimulations in 203 patients (PMCID PMC9852394).
- 115 emotional sensations were elicited.
- Fear/anxiety was associated with stimulation of several distinct sites including amygdala, anterior cingulate, hippocampus, anterior insula and frontal operculum.
- Roughly half of evoked emotional sensations were reported without a paired visceral sensation.
- This is strong evidence for anatomical route multiplicity.

**Case series/literature review**
- PMCID PMC10235553.
- Mirth, excitement, fear, sadness and calmness were evoked from multiple sites including superior frontal gyrus, frontal/parietal operculum, insula, middle cingulate, amygdala and hippocampus.

### Hypothalamus

- Parvizi et al. 2022, Brain Stimulation, DOI 10.1016/j.brs.2022.04.008.
- In one deeply monitored patient, stimulation near ventromedial hypothalamus reproducibly evoked profound shame, sadness and fear.
- Single-pulse stimulation also produced measurable responses in amygdala, hippocampus, vmPFC/OFC, ACC and insula.
- This supports hypothalamic causal importance while directly demonstrating a network-propagation confound. It is not evidence of isolated hypothalamic sufficiency.

### Periaqueductal gray

- Human neurosurgical dPAG stimulation literature reports autonomic arousal plus subjective anxiety/panic-like feelings (e.g. Graeff et al. 1995, PMID 7480384).
- This supports a brainstem causal route with substantial historical/selection limitations.
- Global necessity remains open.

### Peripheral autonomic feedback

**Pure autonomic failure**
- Heims et al. 2004, PMID 15381028.
- Patients with peripheral autonomic denervation were broadly preserved on motivational decision-making, emotional recognition, theory of mind and social cognition; one emotional-attribution measure was mildly impaired.
- This strongly weakens a simple claim that ongoing peripheral autonomic feedback is globally necessary for emotional/social functioning, but the measures are not a complete assay of moment-to-moment feeling.

**Randomized beta-1 blockade**
- de Vos et al. 2024, DOI 10.1007/s00213-024-06548-2.
- Atenolol/metoprolol reduced tonic cardiovascular state but did not reduce subjective CO2 panic/fear/discomfort.
- The relative panic HR response and non-beta-1 bodily channels remained, so this is a selective route constraint rather than body-independence evidence.

**H001 project reanalysis**
- Parrotta et al. 2026 public false-cardiac-feedback pain data.
- Project sensitivity analysis found subjective feedback effects not detectably statistically mediated by HR, HRd or HRd_Z.
- This constrains strict measured-cardiac mediation only.

## Precommitted v001 candidate assessments

Before executing the atlas code:

- **Amygdala**: global necessity REFUTED; causal participation SUPPORTED; isolated sufficiency NOT ESTABLISHED; route-specific roles SUPPORTED.
- **Insula**: global necessity REFUTED; causal participation SUPPORTED; isolated sufficiency NOT ESTABLISHED.
- **Peripheral autonomic feedback**: global necessity STRONGLY WEAKENED but not cleanly refuted for every feeling; modulatory contribution supported.
- **Ventromedial hypothalamic region**: causal participation SUPPORTED; global necessity UNKNOWN; isolated sufficiency NOT ESTABLISHED because of network propagation.
- **dPAG**: causal participation supported with older-evidence caveats; global necessity UNKNOWN.
- **Distributed operculo-insulo-limbic routes**: route multiplicity SUPPORTED; existence/location of a shared downstream minimum cut UNKNOWN.

## v001 gate

The atlas reports EVIDENCE_FAVORS_ROUTE_MULTIPLICITY only if:
1. direct human stimulation gives reported emotion from multiple anatomically distinct regions;
2. at least one canonical candidate can be lost while the same broad affect class remains available through another route;
3. no exclusive single anatomical source survives the frozen necessity constraints.

This verdict does **not** mean multiple independent phenomenal generators are proven.

## Critical alternative

All apparently distinct routes could still converge on a shared downstream causal bottleneck that current human stimulation/lesion methods have not isolated.

Therefore the strongest next question is:

> Is there a shared minimum causal cut across preserved and evoked feelings, or is affect truly supported by multiple substitutable downstream organizations?

Finding that cut—or failing to find one under sufficiently rich causal data—is more informative than naming another single brain region.

## Current execution status

Atlas protocol and executable are frozen. Cloud dispatch was attempted after the freeze, but the Home Laptop relay disconnected before the GitHub Actions dispatch command completed. **No atlas run is claimed yet.** Resume the frozen run unchanged when a dispatch path is available.


## Atlas v001 executed result

The frozen atlas executed successfully in GitHub Actions.

Canonical run: `37206982306`  
Head: `ca6f8778788e19f964df70f5bedf4e9ad09712cb`  
Artifact ID: `11305386184`  
Artifact SHA256: `af657c41b825a89d577d71cce6700889d7037594a7347a51217c4ce805f0bf8c`  
Permanent raw snapshot: `results_snapshots/causal-route-atlas-v001-run-37206982306.json`  
Snapshot commit: `e3ea7eb31b758b1cb5600bf75dc22e5025a680ec`

A first dispatch also completed before a relay error became visible (run `37206790877`); it used the same frozen protocol and returned the same qualitative verdict. The later run above is canonical.

### Verdict

`EVIDENCE_FAVORS_ROUTE_MULTIPLICITY`

- evidence rows: 12
- global necessity refuted in v001: amygdala, insula
- global necessity unresolved: ventromedial hypothalamic region, dPAG
- route multiplicity gate: PASS
- route substitution gate: PASS
- physiology–feeling dissociation gate: PASS
- single exclusive anatomical source survives v001: NO

### Interpretation firewall

This is **not** proof of multiple independent phenomenal generators.

The strongest surviving alternative is that anatomically different upstream perturbations converge on a common downstream causal bottleneck. The next Loop 005 task is therefore a shared-minimum-cut screen, not a search for another named single region.


## Shared Minimum-Cut Screen v001

After atlas v001 favored route multiplicity, the next adversarial alternative was frozen:

> multiple effective routes may all converge on one shared downstream causal bottleneck.

Protocol: `protocols/shared_minimum_cut_screen_v001.json`  
Protocol commit: `2ad028a7ec4d80184c21b78128015e3e7cacba36`  
Executable: `analysis/shared_minimum_cut_screen_v001.py`  
Executable commit: `175144a5be092021e0f4940431a455299fafc4a3`  
Workflow support commit: `28c5099d79d36329b8deb81c53fa4fe44e6669ef`

Canonical run: `37207403625`  
Head: `28c5099d79d36329b8deb81c53fa4fe44e6669ef`  
Artifact ID: `11305536518`  
Artifact SHA256: `f7671362778302c9ef2c91a722cbd2478416d21498035999702e573d38d8f449`  
Permanent snapshot: `results_snapshots/shared-minimum-cut-screen-v001-run-37207403625.json`  
Snapshot commit: `fef2d005a7c1aee8d842c29f3a9e39713b9626b4`

### Frozen admission criteria

A shared anatomical minimum cut counted only if:
1. it survives known lesion counterexamples;
2. direct causal loss specifically abolishes felt affect rather than merely recognition, autonomic output, memory, arousal or access;
3. wakefulness and a viable first-person report/communication channel remain sufficiently intact to assess feeling;
4. the evidence is directly causal.

### Verdict

`NO_SHARED_MINIMUM_CUT_IDENTIFIED`

Seven candidate bottlenecks were screened; **zero** passed all criteria.

- rostral dorsolateral pontine tegmentum: causal role in coma/wakefulness is strong, but fails feeling-specificity and observability because decisive injury causes coma;
- ventral anterior insula/pregenual ACC network: fails lesion-complement evidence;
- somatosensory cortices: plausible and often implicated, but no direct global-feeling necessity test;
- ventromedial hypothalamic region: stimulation can evoke emotion but no necessity test and network propagation is substantial;
- dPAG: causal participation supported, selective human feeling-necessity test absent;
- higher-order/global cortical machinery: decisive loss is confounded with access/report loss;
- distributed dynamic bottleneck: remains an open hypothesis class but is not yet operationalized.

### Interpretation

This result does **not** show that there is no common bottleneck.

It shows that current direct human evidence does not identify one while preserving a feeling-specific observable. Two live possibilities remain:

1. **true causal-route degeneracy/substitution** — more than one downstream organization can support overlapping felt affect;
2. **hidden network convergence** — distinct entry routes converge on a distributed state that current lesions/stimulation methods have not selectively isolated.

The next Loop 005 attack should therefore target **network convergence conditional on subjective affect**, not simply anatomical overlap.

## New lead: subjective-affect network convergence versus physiology-only propagation

Existing evidence creates a useful contrast:

- multiple stimulation sites can evoke reported fear/anxiety or other emotion;
- amygdala stimulation can robustly evoke defensive autonomic physiology without subjective emotion in most tested cases.

Candidate question:

> Do stimulation events that produce a reported affective experience converge on a downstream causal/network pattern that is absent or weaker in stimulation events producing autonomic defensive physiology without reported emotion?

This is deliberately framed as a **subjective-report-associated network signature**, not a phenomenal ground-truth detector.

The strongest rival possibilities are:

- **COMMON-FELT-NETWORK**: diverse emotion-evoking stimulation routes converge on a reproducible downstream state/network feature not explained by autonomic arousal alone.
- **ROUTE-HETEROGENEITY**: after controlling for stimulation site, intensity, arousal and report/access variables, no common downstream feature remains across subjective-emotion events.

Before freezing this as a new experiment, conduct a novelty/data-availability attack. Direct electrical stimulation network mapping is already substantial prior art (including es-fMRI causal mapping and recent broad DES-network analyses), so the project must establish whether the **felt-report vs physiology-only** contrast itself is both novel and identifiable from available data.
