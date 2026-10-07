FOUR-CONSTRUCT FORMAL MODEL v001
Date: 2026-10-07
Status: Project formalization; equations are candidate operational definitions unless explicitly identified as standard literature models.
PURPOSE
Give self-maintenance, instinct, emotion, and feeling mathematically different roles so they can be tested without circularly defining one by another.
NOTATION
x_t = physiological/organismic state.
w_t = perturbations/disturbances.
u_t = regulatory action.
s_t = exteroceptive/interoceptive context available to action selection.
d = developmental environment/history within a species-typical range.
h_t = task-specific individual learning history.
pi = action policy/action sequence.
e_t = latent emotion-state.
y_t^(k) = output channel k (physiology, action tendency, attention, expression, learning/decision bias, etc.).
phi_t = phenomenal/felt state, when present.
r_t = report/judgment about experience.
a_t = access/metacognitive state.
l_t = linguistic/report channel.
==================================================
M — SELF-MAINTENANCE / VIABILITY REGULATION
==================================================
ONTOLOGICAL TYPE
Occurrent regulatory process plus viability constraint/objective over physiological trajectories.
DYNAMICS
x_(t+1) = f_M(x_t, u_t, w_t).
VIABILITY REGION
V = {x : g_j(x) <= 0 for all viability constraints j}.
HORIZON VIABILITY FUNCTION
M_H(x_t, pi_M) =
P_piM[x_(t+k) in V for every k = 0,...,H | x_t].
Alternative measurable formulations:
- expected first exit time from V;
- distance/cost to restore a viable region;
- viability kernel under admissible controls;
- homeostatic/allostatic prediction error or control cost.
SCIENTIFIC TEST
M is present to the degree that interventions and control actions systematically preserve/recover viability variables under perturbation.
TYPE SIGNATURE
M is not a feeling or behavioral disposition. It is a regulation/control relation over state trajectories.
==================================================
I — INSTINCT, OPERATIONALLY NARROWED TO CANALIZED ACTION DISPOSITION
==================================================
TERMINOLOGY FIREWALL
The broad folk/scientific word "instinct" is rejected as a single natural kind.
For formal work, I means:
DEVELOPMENTALLY CANALIZED ACTION DISPOSITION (ICAD).
ONTOLOGICAL TYPE
A disposition / prior bias over action policies, not an occurrent emotional or phenomenal state.
POLICY FORM
P_0(pi | s, d)
= pre-task-learning distribution over policies under current state/context s and developmental history d.
The superscript/subscript 0 means before the specific individual task-learning history whose contribution we want to distinguish.
CANALIZATION
For a set D_N of normal species-typical developmental environments, define a robustness index:
C_I(s) =
1 - E_{d,d' in D_N}[ JSD(P_0(pi|s,d), P_0(pi|s,d')) ] / log(2).
C_I near 1 means policy bias is similar across the normal developmental range.
C_I does NOT mean the behavior developed without experience.
TASK-LEARNING DEPENDENCE
A candidate history-dependence measure is:
L_I = I(Pi ; H_task | S,D),
conditional mutual information between selected policy and task-specific learning history.
An instinct-like/canalized disposition should show:
- nontrivial pre-task policy bias;
- high enough robustness across normal developmental conditions;
- less dependence on task-specific individual reinforcement history than a learned habit;
while still allowing developmentally necessary experience.
BIAS STRENGTH
Relative to a chosen neutral/reference policy distribution P_ref:
B_I(s,d) = D_KL[P_0(pi|s,d) || P_ref(pi|s)].
IMPORTANT
No one scalar is asserted to be "amount of instinct."
The scientifically defensible object is a vector:
I = (B_I, C_I, L_I, trigger specificity, population regularity, developmental requirements).
SCIENTIFIC TEST
I is supported when an action-policy bias:
- exists before task-specific training;
- recurs across individuals under a normal developmental range;
- can be perturbed independently of core physiological regulation;
- is not fully explained by the individual's task-specific reinforcement history.
TYPE SIGNATURE
I is a disposition over actions/policies. It is not the executed action, drive state, emotion episode, or feeling.
==================================================
E — FUNCTIONAL EMOTION-STATE
==================================================
TERMINOLOGY FIREWALL
Because theories disagree over whether "emotion" necessarily includes feeling, this project uses the explicit term FUNCTIONAL EMOTION-STATE.
ONTOLOGICAL TYPE
Occurrent, temporally extended latent dynamical state coordinating multiple organismic systems.
STATE DYNAMICS
e_(t+1) =
f_E(e_t, z_t, x_t, c_t, theta_E) + eta_t,
where:
z_t = organism-relevant appraisal/relevance inputs;
x_t = body/internal state;
c_t = context/history variables;
eta_t = process noise.
MULTI-SYSTEM OBSERVATION MODEL
y_t^(k) = g_k(e_t) + xi_t^(k),
for output systems k including:
- autonomic/endocrine physiology;
- action readiness;
- attention/valuation;
- expression;
- learning/decision bias.
FUNCTIONAL-STATE CRITERIA
Candidate emotion-state signatures include:
- persistence after the eliciting event;
- scalability/intensity;
- generalization across behaviors/context;
- valence/relevance;
- coordinated causal effects across multiple output systems.
INCREMENTAL-IDENTIFIABILITY TEST
Let Y be held-out multisystem observations.
Compare:
Model base: P(Y | M, I, context)
against
Model E: P(Y | M, I, context, e_t).
E earns independent scientific status only if:
1. a reproducible latent state improves held-out prediction beyond simpler controls;
2. interventions on the candidate state alter multiple predicted outputs;
3. the effect is not reducible to one motor policy, generalized arousal, or one physiological variable.
A candidate information criterion is:
Delta_E = I(e_t ; Y_future | M_t, I_t, context_t),
with causal perturbation required because predictive mutual information alone does not establish mechanism.
TYPE SIGNATURE
E is an occurrent coordinating state. It is neither a stable action disposition nor subjective experience by definition.
==================================================
F — FEELING
==================================================
ONTOLOGICAL TYPE
First-person phenomenal/experiential state.
REQUIRED SUBTYPES
F_h = homeostatic/interoceptive feeling (e.g. hunger, thirst, pain, dyspnea, wellbeing).
F_e = emotional feeling (felt fear, anger, joy, etc.).
F_s = sensory affect/feeling where required by the evidence.
These subtypes may share phenomenality without sharing the same upstream generator.
PHENOMENAL VARIABLE
phi_t denotes the felt/phenomenal state.
MEASUREMENT MODEL
Phenomenality is not equated with self-report.
Instead:
r_t ~ P(r | phi_t, a_t, l_t, demand_t, memory_t),
where report depends on the felt state plus access/metacognition, language, demand characteristics and memory.
Likewise physiological/behavioral observables may be modeled as:
b_t ~ P(b | phi_t, e_t, x_t, action policy, context).
IDENTIFIABILITY LIMIT
If phi_t is latent, report/behavior alone generally do not uniquely identify its ontology. Multiple latent-state parameterizations can generate the same observable distribution. Therefore a claim that a particular neural/functional variable IS phenomenal feeling requires an explicit bridge/identity assumption plus causal evidence; it does not follow from predictive fit alone.
SCIENTIFICALLY ACCESSIBLE TARGET
F_report/access can be operationalized and predicted.
F_phen remains a latent phenomenal target whose mapping to third-person mechanisms is underdetermined by ordinary report correlations.
TYPE SIGNATURE
F is the only one of the four whose defining target is first-person qualitative experience.
==================================================
WHY THE FOUR ARE MATHEMATICALLY DIFFERENT
==================================================
M belongs to the class of control/regulatory functionals over physiological trajectories.
I belongs to the class of dispositions/priors over policies.
E belongs to the class of latent dynamical states producing coordinated multi-output effects.
F belongs to the class of phenomenal latent states with indirect measurement through report/behavior.
They therefore occupy different mathematical roles:
M : trajectory -> viability/control value
I : state/development -> distribution over policies
E : time/context/body -> latent state -> multisystem outputs
F : mechanism/state -> phenomenal state -> imperfect report/access observations
This typed distinction is stronger than ranking all four on one scalar "depth" axis.
==================================================
STRICT SERIAL MODEL AND ITS TESTABLE IMPLICATIONS
==================================================
The original chain:
M -> I -> E -> F
is a structural causal model only under strong assumptions (causal sufficiency, no hidden bypass paths, stable construct definitions).
It implies conditional independences such as:
E independent of M given I
F independent of M given E
F independent of I given E
A direct homeostatic/interoceptive route from body regulation to feeling violates F independent of M given E.
Likewise, learned/contextual/cognitive routes into emotion make a narrow instinctive disposition non-sufficient as the sole mediator from M to E.
Therefore the strict chain is empirically falsifiable and is already inconsistent with the broad scientific use of "feeling" that includes homeostatic/interoceptive feelings.
==================================================
LEADING ARCHITECTURE
==================================================
The current model should not be a four-node chain.
At minimum include nuisance/neighbor constructs:
D_t = drive/motivation;
A_t = arousal;
C_t = appraisal/cognition;
H_t = learned history/memory;
P_t = perception/interoceptive representation.
Qualitative graph:
M <-> D
M -> P_interoceptive
I + D + perception/context/history -> action policy
D + appraisal/context/history/body -> E
P_interoceptive + conscious-capable architecture -> F_h
E + body/appraisal + conscious-capable architecture -> F_e
E -> action selection
F/cognition -> recurrent regulation of E, action, and indirectly M
This is a branching/recurrent system, not a universal staircase.
==================================================
FALSIFIERS
==================================================
M fails as a separate construct if viability regulation cannot be operationalized independently of action/affect in controlled systems.
I/ICAD fails if candidate behavior is completely accounted for by task-specific learning or immediate reflex regulation and shows no robust pre-task policy bias.
E fails as a separate construct if coordinated multisystem observations are fully predicted by M + action policy + arousal + context with no reproducible latent-state increment and no distinct causal perturbation signature.
F_report fails as a useful proxy if report variation is dominated by access/language/demand variables and does not track independently validated experience-related manipulations.
Any strong identity claim for F_phen fails if a causally/observationally equivalent rival without the proposed identity mapping explains all accessible data.
==================================================
CURRENT FORMAL VERDICT
==================================================
We can formulate all four targets, but not symmetrically.
M: strongest mathematically and empirically grounded.
I: formalizable only after replacing broad "instinct" with a vector-valued canalized action disposition.
E: formalizable as a latent functional dynamical state, but exact emotion ontology remains theory-dependent.
F: report/access is operationalizable; phenomenal feeling is not uniquely identifiable from ordinary third-person observations without an explicit consciousness bridge.
This asymmetry is itself a scientific result.