FOUR-CONSTRUCT FINAL ADJUDICATION v001
Date: 2026-10-07
Program: Pre-Consciousness Construct Separation
Status: Current canonical answer after literature-family tournament, construct destruction, exact architecture enumeration, formalization, novelty attack, and synthetic falsification simulation.
IMPORTANT EPISTEMIC SCOPE
"Final" here means the strongest conclusion supported by the current scientific evidence and the project's bounded-exhaustive attack. It does not mean metaphysical certainty or that no future experiment can overturn it.
The search was exhaustive in two different senses:
1. THEORY SPACE: bounded-exhaustive across the major serious theory families and large integrative taxonomies relevant to homeostasis, innate action, emotion and feeling.
2. FOUR-NODE CAUSAL SPACE: mathematically exhaustive across all directed M/I/E/F graphs without self-loops.
It is impossible in empirical science to prove that every conceivable future theory has been enumerated.
==================================================
EXECUTIVE ANSWER
==================================================
The original statement
SELF-MAINTENANCE -> INSTINCT -> EMOTION -> FEELING
is NOT a scientifically established universal four-step hierarchy.
The investigation finds something more precise:
Self-maintenance, instinctive/canalized action disposition, functional emotion-state, and feeling CAN be separated scientifically, but they are different KINDS OF CONSTRUCT rather than four values on one common depth scale.
The correct typed distinction is:
M — SELF-MAINTENANCE
Type: regulatory process / viability-control relation.
I — INSTINCT, SCIENTIFICALLY NARROWED
Type: developmentally canalized action disposition / prior over policies.
The broad ordinary word "instinct" is not one natural kind and must not be used as an unqualified scalar.
E — FUNCTIONAL EMOTION-STATE
Type: occurrent, temporally extended latent dynamical state that coordinates multiple systems in relation to organism-relevant significance.
F — FEELING
Type: first-person phenomenal/experiential state.
At minimum this family must distinguish homeostatic/interoceptive feeling from emotional feeling, and both must be distinguished from report/access.
Thus:
YES — the four targets can be made scientifically non-equivalent.
NO — they are not four exhaustive categories of human experience.
NO — they do not form a universal strict serial ladder.
NO — "instinct" and broad "feeling" are not single clean natural kinds as ordinarily used.
YES — each can be given a formal scientific role, although F_phen has a stronger identifiability limit than the other constructs.
==================================================
1. SELF-MAINTENANCE — M
==================================================
SCIENTIFIC DEFINITION
Self-maintenance is the active endogenous regulation by which a living system preserves or restores physiological/organizational variables inside a viability-compatible region under perturbation.
WHAT MAKES IT DISTINCT
The target of regulation is continued viable organization or viability-relevant variables, not the selection of a species-typical behavior, an emotional episode, or a first-person experience.
It exists at biological scales that do not require a nervous system. Cellular and microbial homeostasis therefore provide a clean counterexample to any definition that makes self-maintenance depend on instinct, emotion or feeling.
ONTOLOGICAL TYPE
Process / control relation.
FORMALIZATION
x_(t+1) = f_M(x_t,u_t,w_t).
Let V be the viability-compatible region:
V = {x : g_j(x) <= 0 for all viability constraints j}.
Candidate horizon measure:
M_H(x_t,pi_M) =
P_piM[x_(t+k) in V for every k=0,...,H | x_t].
Other valid measures:
expected first-exit time from V;
viability kernel;
control cost required to return to V;
regulated-variable error/recovery dynamics.
These equations are project operationalizations, not claimed biological laws.
MEASUREMENTS
Temperature, osmolarity, glucose/energy state, oxygenation, pH, endocrine/autonomic regulation, repair/turnover, recovery after perturbation, and organism-specific viability variables.
FALSIFIER
If a proposed M measure does not distinguish manipulations that alter viability regulation from arbitrary state change, the measure fails.
PRIMARY PRIOR ART
Ramsay & Woods 2014, DOI 10.1037/a0035942.
Sterling 2012, DOI 10.1016/j.physbeh.2011.06.004.
Petzschner et al. 2021, DOI 10.1016/j.tins.2020.09.012.
Keramati & Gutkin 2014, DOI 10.7554/eLife.04811.
Weinberger 2026, DOI 10.1007/s10539-026-10018-8.
==================================================
2. INSTINCT — I
==================================================
SCIENTIFIC VERDICT ON THE WORD
"Instinct" in its broad ordinary sense is NOT a clean single scientific natural kind.
Properties commonly bundled under "instinct" can dissociate:
present at birth;
genetically influenced;
species-typical;
developmentally canalized;
unlearned in a task-specific sense;
stereotyped;
cue-triggered;
motivationally gated;
implemented by specialized circuits.
Normal developmental experience can be required for reliable species-typical behavior. Therefore "hardwired," "genetically programmed," and "independent of experience" are not safe general definitions.
PROJECT'S SCIENTIFIC REPLACEMENT
I = DEVELOPMENTALLY CANALIZED ACTION DISPOSITION (ICAD).
SCIENTIFIC DEFINITION
An ICAD is a reliable disposition that biases the selection or generation of action policies across a species-typical developmental range without requiring the same task-specific individual learning history that produces an acquired habit.
This definition explicitly permits developmental input.
WHAT MAKES IT DISTINCT
I describes a propensity/disposition over possible actions.
M describes regulation of viability variables.
E describes an occurrent coordinating state.
F describes experience.
ONTOLOGICAL TYPE
Disposition / policy prior.
FORMALIZATION
P_0(pi | s,d) =
the distribution over policies pi under state/context s and developmental history d before the task-specific learning history whose contribution is being tested.
Canalization candidate:
C_I(s) =
1 - E_{d,d' in D_N}[JSD(P_0(pi|s,d),P_0(pi|s,d'))] / log(2).
Task-learning dependence:
L_I = I(Pi ; H_task | S,D).
Policy-bias strength relative to reference:
B_I(s,d) =
D_KL[P_0(pi|s,d) || P_ref(pi|s)].
Do NOT collapse I to one number.
Use a vector:
I = (B_I,C_I,L_I,trigger specificity,population regularity,developmental requirements).
MEASUREMENTS
Expression before task-specific training;
reaction norms across normal developmental environments;
population regularity;
effect of altered developmental input;
effect of task-specific training;
sensorimotor/neural circuitry;
policy-selection probabilities.
FALSIFIER
A candidate I construct fails if the behavior is fully explained by ordinary task-specific learning or by an immediate regulatory/reflex loop with no separable policy disposition.
PRIMARY PRIOR ART
Mameli & Bateson 2011, DOI 10.1098/rstb.2010.0174.
Blumberg 2017, DOI 10.1002/wcs.1371.
NIMH RDoC Innate Motor Patterns.
Developmental/neuroethological action-selection literature.
==================================================
3. EMOTION — E
==================================================
SCIENTIFIC TERMINOLOGY
There is no universally accepted definition of "emotion."
Therefore this project must use the explicit term FUNCTIONAL EMOTION-STATE and state its convention.
SCIENTIFIC DEFINITION
A functional emotion-state is an occurrent, temporally extended internal state elicited by organism-relevant conditions that coordinates changes across multiple systems such as physiology, action readiness, attention/valuation, expression, learning and decision processes.
Feeling is NOT included in the definition of E, deliberately, so E-versus-F can be tested rather than assumed.
WHAT MAKES IT DISTINCT
An action disposition biases what the organism can/tends to do.
An emotion-state is an activated coordinating state that can persist, scale, generalize across outputs and reorganize several systems simultaneously.
ONTOLOGICAL TYPE
Occurrent latent dynamical state.
FORMALIZATION
e_(t+1) =
f_E(e_t,z_t,x_t,c_t,theta_E) + eta_t.
For output channel k:
y_t^(k) = g_k(e_t) + xi_t^(k).
Candidate incremental information:
Delta_E =
I(e_t ; Y_future | M_t,I_t,context_t).
Prediction is insufficient by itself; independent causal intervention is required for a strong mechanism claim.
FUNCTIONAL SIGNATURES
Persistence;
scalability;
generalization;
valence/relevance;
coordination across multiple outputs;
causal influence on multiple behavioral/cognitive systems.
FALSIFIER
The distinct E layer is weakened if M + action policy + arousal + context fully account for reproducible multisystem structure and targeted perturbations reveal no independent state.
PRIMARY PRIOR ART
Anderson & Adolphs 2014, DOI 10.1016/j.cell.2014.03.003.
Adolphs 2017, DOI 10.1093/scan/nsw153.
Adolphs & Andler 2018.
Scherer & Moors 2019, DOI 10.1146/annurev-psych-122216-011854.
Dukes & Sander 2024, DOI 10.1007/s42761-024-00272-y.
==================================================
4. FEELING — F
==================================================
SCIENTIFIC DEFINITION
Feeling, for this project, is a first-person qualitative/phenomenal state: there is something it is like for the subject to be in that state.
This definition must not be equated with verbal report.
REQUIRED SUBTYPES
F_h — homeostatic/interoceptive feeling:
hunger, thirst, pain, dyspnea, temperature discomfort, wellbeing/malaise and related experienced body states.
F_e — emotional feeling:
the experienced fear, anger, joy, sadness, etc. associated with an emotion episode.
F_s — sensory-affective feeling may need a separate subtype where the literature demands it.
F_report — explicit report/judgment about a feeling.
F_phen — phenomenal feeling itself.
WHAT MAKES IT DISTINCT
M, I and E can be operationalized in third-person functional terms.
F_phen is defined by first-person qualitative presence.
ONTOLOGICAL TYPE
Phenomenal / experiential state.
MEASUREMENT MODEL
Let phi_t denote phenomenal state.
r_t ~ P(r | phi_t,a_t,l_t,demand_t,memory_t),
where:
a_t = access/metacognition,
l_t = language/report channel.
Thus report is an observation channel, not the definition of feeling.
IDENTIFIABILITY LIMIT
A model that predicts reports does not thereby prove that its latent variable is identical to phenomenal experience. Multiple latent ontologies can generate the same accessible report/behavior distribution. A phenomenal identity claim therefore requires an explicit bridge/identity hypothesis in addition to causal evidence.
FALSIFIER OF A UNITARY F CONSTRUCT
If homeostatic, emotional and sensory feelings have materially different generators and causal organization, "Feeling" must remain a family label rather than one mechanism.
PRIMARY PRIOR ART
Damasio & Carvalho 2013, DOI 10.1038/nrn3403.
Adolphs 2017.
LeDoux & Brown 2017, DOI 10.1073/pnas.1619316114.
Human Affectome, DOI 10.1016/j.neubiorev.2023.105450.
==================================================
5. EXACT DIFFERENCE BETWEEN THE FOUR
==================================================
The deepest result is a TYPE difference:
M:
maps organism trajectories/control into viability preservation.
I:
maps state + development into a disposition/distribution over policies.
E:
maps ongoing body/context/relevance into a temporally extended latent coordination state that produces multiple outputs.
F:
is a phenomenal state whose third-person measurement is indirect.
They therefore cannot be validly collapsed into one scalar "depth" variable without throwing away their mathematical type.
In concise notation:
M : trajectory -> viability/control functional.
I : state × development -> distribution over policies.
E : time × body × context -> latent coordinating state -> multi-system outputs.
F : underlying state/process -> phenomenal state -> imperfect report/access observations.
==================================================
6. DISSOCIATION / COUNTEREXAMPLE ATTACK
==================================================
M WITHOUT I/E/F
Cellular and microbial homeostasis demonstrates viability regulation without nervous-system action-policy architecture, emotion-state, or human-like report.
I-LIKE ACTION WITHOUT FULL E/F
RDoC recognizes innate motor patterns such as startle and stereotyped action plans separately from affective/cognitive domains. This supports a separable action-control construct even though particular innate behaviors may interact with emotion.
E WITHOUT DEFINING F
Under the Adolphs functional-state convention, E is scientifically defined independently of conscious emotional experience. This is an operational separation; empirical proof that a particular nonverbal organism has no phenomenality is not claimed.
F WITHOUT REQUIRING A FULL E
Damasio/Carvalho and homeostatic-feeling literature include hunger, pain and wellbeing as feelings of body state. Therefore a universal rule that every feeling must be produced by a preceding full emotion episode is not theory-neutral and fails under this scientifically influential usage.
ATTACK FROM DENTON ET AL.
Denton and colleagues call homeostatic subjective states "primordial emotions" and describe them as subjective elements of instincts.
This does not destroy the underlying process distinctions; it demonstrates that ordinary labels are theory-dependent.
The project's solution is explicit typed operational terminology rather than asserting ownership of the words.
==================================================
7. EXHAUSTIVE FOUR-NODE CAUSAL CALCULATION
==================================================
With four labeled nodes M,I,E,F and no self-loops, 12 directed edges are possible.
All directed graphs:
2^12 = 4,096.
Exact enumeration:
4,096 directed graphs.
543 directed acyclic graphs.
185 Markov-equivalence classes among those DAGs.
24 possible strict total orders.
6 strict total orders with M first.
3 strict total orders with M first and E before F.
Therefore the words themselves cannot identify a unique causal order.
The original chain
M -> I -> E -> F
under ordinary DAG causal sufficiency/faithfulness assumptions predicts:
M independent of E given I.
M independent of F given E.
I independent of F given E.
Adding an empirically motivated homeostatic/interoceptive M->F bypass destroys the latter mediator independences.
This is an exact structural result, not an opinion.
==================================================
8. SYNTHETIC CAUSAL ATTACK
==================================================
A frozen 500-replicate synthetic tournament with N=2,000 per replicate verified the expected constraints.
STRICT S:
mean partial r(M,E|I) = 0.0003.
mean partial r(M,F|E) = -0.0009.
mean partial r(I,F|E) = -0.0019.
HOMEOSTATIC BYPASS:
mean partial r(M,F|E) = 0.4413.
mean partial r(I,F|E) = 0.2139.
PARALLEL/DIRECT-E MODEL:
mean partial r(M,E|I) = 0.3954.
MULTIROUTE/RECURRENT PROXY:
all three serial constraints were materially broken.
This does NOT establish the human causal graph. It demonstrates that the proposed theories make discriminating quantitative predictions and can be tested.
==================================================
9. THEORY-FAMILY WAR / TOURNAMENT
==================================================
The project attacked the original claim against:
homeostasis/allostasis/body-regulation theory;
developmental systems and ethology of innateness;
basic-emotion/Pankseppian affective neuroscience;
appraisal/component-process theory;
psychological construction/predictive-allostatic theory;
functional-state/cross-species emotion theory;
survival-circuit/higher-order emotional consciousness;
Damasio/body-state feeling theory;
Human Affectome;
NIMH RDoC;
formal Emotion Ontology;
recent componential/Affectivism synthesis;
homeostatic RL/active inference;
recent 2026 mathematical motivated-emotion architectures;
causal-control and causal-emotion-network work.
No serious theory family found in this bounded search rescues the proposition that the four ordinary words are simultaneously:
unitary natural kinds,
exhaustive of human experience,
and universally ordered M->I->E->F.
The strongest recurring lesson across competing theories is separation of regulatory state, action/motivation, affective coordination, and subjective experience — but theories disagree on terminology, boundaries, and causal ordering.
==================================================
10. "ARE THESE THE FOUR CATEGORIES HUMANS EXPERIENCE?"
==================================================
NO, if "categories humans experience" means an exhaustive taxonomy of subjective human life.
Reasons:
Self-maintenance is mostly a regulatory mechanism and often entirely nonconscious.
I is primarily a behavioral disposition/control architecture.
Major frameworks separately require constructs for sensation/perception, arousal, motivation, mood, cognition, memory, social processing, agency/volition, etc.
NIMH RDoC currently uses six major domains of human functioning rather than these four.
Human Affectome maps a far richer affective conceptual space.
Therefore the original four should never be called "the four exhaustive categories of human experience."
==================================================
11. WHAT SURVIVES OF THE USER'S ORIGINAL INTUITION?
==================================================
A strong core survives:
1. Self-maintenance really is a biologically deep regulatory foundation.
2. Innate/canalized action tendencies are not the same thing as self-maintenance.
3. Functional emotion states are not the same thing as a single action policy.
4. Subjective feeling is not the same thing as the functional emotion state under an explicit functionalist convention.
5. These distinctions matter before attempting a theory of consciousness.
What does NOT survive:
the assumption that they are exhaustive;
the assumption that each label is a unitary natural kind;
the assumption of one universal serial order.
==================================================
12. LEADING ARCHITECTURE
==================================================
There is no justified single total order.
A more defensible family of models is branching/recurrent:
M -> viability/interoceptive regulation.
M and internal need -> motivation/drive.
Development + state + context -> canalized action-policy biases.
Body state + relevance/appraisal/context/history -> E.
Interoceptive representation + conscious-capable mechanism -> F_h.
E + conscious-capable mechanism -> F_e.
E, action, feeling, cognition and learning feed back recurrently.
Motivation/drive, arousal, perception/interoception, learning/memory and cognition should be modeled as neighboring variables rather than forced inside one of the four.
==================================================
13. CAN WE WRITE A PAPER?
==================================================
YES, but the publishable paper is NOT:
"We proved four fundamental layers of mind."
The defensible paper is:
"Four Words, Four Types, No Four-Step Ladder: A Typed Causal Framework for Self-Maintenance, Canalized Action Dispositions, Emotion States, and Feeling."
Potential contribution:
- cross-disciplinary construct disambiguation;
- explicit ontological/mathematical type signatures;
- complete four-node graph enumeration;
- conditional-independence falsifiers for the strict ladder;
- simulation demonstration;
- homeostatic-feeling counterexample;
- phenomenal-report identifiability firewall;
- preregisterable empirical tests.
CURRENT NOVELTY
Provisional synthesis/methods novelty survives targeted attack.
However, all individual ideas have substantial prior art:
Human Affectome;
Emotion Ontology;
Adolphs functional emotion states;
Damasio body-state feelings;
component-process theories;
homeostatic RL/active inference;
2026 mathematical motivated-emotion models;
causal-control work.
Therefore novelty must be claimed only for the specific formal synthesis and its derived causal tests unless a systematic database review confirms more.
CURRENT PAPER READINESS
Strong enough to develop a theoretical/formal manuscript.
Not yet justified as a submission-ready empirical paper.
A database-logged systematic novelty review and stronger simulation/empirical validation remain required before submission.
==================================================
14. FINAL CLAIM MATRIX
==================================================
Claim: Self-maintenance is scientifically distinguishable.
Verdict: PASS.
Claim: Broad "instinct" is one scientific natural kind.
Verdict: FAIL.
Claim: A narrow canalized action-disposition construct is scientifically distinguishable.
Verdict: PASS.
Claim: A functional emotion-state can be distinguished from a single action disposition.
Verdict: PASS, under explicit operational convention.
Claim: Feeling can be distinguished from functional emotion-state.
Verdict: PASS AS AN OPERATIONAL/ONTOLOGICAL DISTINCTION; phenomenal absence/presence is not directly third-person observable.
Claim: Feeling is unitary.
Verdict: FAIL / at minimum requires subtype separation.
Claim: M->I->E->F is a universal strict causal chain.
Verdict: FAIL.
Claim: The four are exhaustive categories of human experience.
Verdict: FAIL.
Claim: The four can all be formalized.
Verdict:
M PASS.
I PASS after narrowing/decomposition.
E PASS as a functional latent-state model.
F PARTIAL: report/access can be modeled; phenomenal identity remains scientifically underdetermined without an explicit bridge theory.
Claim: A paper is possible.
Verdict: YES, as a formal construct-separation/causal-identifiability paper; not as proof of four fundamental layers.
==================================================
15. CANONICAL ANSWER IN ONE PARAGRAPH
==================================================
Self-maintenance, instinctive action, emotion and feeling should not be treated as four successive degrees of one thing. The strongest scientifically defensible separation is typed: self-maintenance is a viability-regulation process; "instinct," when made operational, is a developmentally canalized disposition over action policies; emotion, under an explicit functional convention, is an occurrent multi-system coordination state; and feeling is first-person qualitative experience, with homeostatic and emotional subtypes and with report treated only as an imperfect observation channel. These constructs are different, but the four words are neither exhaustive natural kinds nor a universal serial hierarchy. The original M->I->E->F ladder therefore fails as a general law; a branching/recurrent architecture with additional motivation, arousal, perception/interoception, learning and cognition variables is required. This result is formalizable and can support a theoretical methods paper, but phenomenal feeling remains subject to an explicit consciousness/identity bridge rather than being "solved" by the four-construct model.