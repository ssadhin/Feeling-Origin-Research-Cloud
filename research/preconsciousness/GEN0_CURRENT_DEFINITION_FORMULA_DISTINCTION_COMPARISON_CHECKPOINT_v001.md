GENERATION-0 CURRENT DEFINITION / FORMULA / DISTINCTION / COMPARISON CHECKPOINT v001
Date: 2026-10-07
Purpose: Freeze the exact current construct result BEFORE starting the recursive option-tournament method. This file is a baseline for later comparison and must not be silently rewritten.
STATUS
Generation-0 checkpoint only. Not the final answer.
==================================================
M — SELF-MAINTENANCE
==================================================
CURRENT DEFINITION
Self-maintenance is the active endogenous regulation by which a living system preserves or restores physiological/organizational variables inside a viability-compatible region under perturbation.
CURRENT TYPE
Regulatory process / viability-control relation.
CURRENT FORMULA
x_(t+1) = f_M(x_t,u_t,w_t)
V = {x : g_j(x) <= 0 for all viability constraints j}
M_H(x_t,pi_M) =
P_piM[x_(t+k) in V for every k=0,...,H | x_t]
Alternative measures:
expected first-exit time from V;
viability kernel;
control cost needed to return to V;
regulated-variable error/recovery dynamics.
CURRENT DISTINCTION
M concerns regulation of viability-relevant state trajectories.
It is not itself an action disposition, emotion episode, or phenomenal feeling.
==================================================
I — "INSTINCT", NARROWED TO ICAD
==================================================
CURRENT DEFINITION
Broad "instinct" is rejected as a single natural kind.
Operational replacement:
Developmentally Canalized Action Disposition (ICAD) = a reliable disposition that biases the selection or generation of action policies across a species-typical developmental range without requiring the same task-specific individual learning history that produces an acquired habit.
CURRENT TYPE
Disposition / policy prior.
CURRENT FORMULAS
P_0(pi | s,d)
= pre-task-learning policy distribution under state/context s and developmental history d.
C_I(s) =
1 - E_{d,d' in D_N}[JSD(P_0(pi|s,d),P_0(pi|s,d'))] / log(2)
L_I =
I(Pi ; H_task | S,D)
B_I(s,d) =
D_KL[P_0(pi|s,d) || P_ref(pi|s)]
I is vector-valued:
I = (B_I,C_I,L_I,trigger specificity,population regularity,developmental requirements)
CURRENT DISTINCTION
I describes a disposition over possible action policies.
It differs from M because it is action-policy structure rather than viability regulation.
It differs from E because it is a disposition rather than an occurrent coordinating state.
It differs from F because it is not defined phenomenally.
==================================================
E — FUNCTIONAL EMOTION-STATE
==================================================
CURRENT DEFINITION
A functional emotion-state is an occurrent, temporally extended internal state elicited by organism-relevant conditions that coordinates changes across multiple systems such as physiology, action readiness, attention/valuation, expression, learning, and decision processes.
Feeling is explicitly excluded from the definition of E so E-versus-F remains testable.
CURRENT TYPE
Occurrent latent dynamical coordination state.
CURRENT FORMULAS
e_(t+1) =
f_E(e_t,z_t,x_t,c_t,theta_E) + eta_t
For output channel k:
y_t^(k) = g_k(e_t) + xi_t^(k)
Candidate incremental information:
Delta_E =
I(e_t ; Y_future | M_t,I_t,context_t)
CURRENT FUNCTIONAL SIGNATURE
persistence;
scalability/intensity;
generalization;
valence/relevance;
coordination across multiple outputs;
causal influence on multiple behavioral/cognitive systems.
CURRENT FALSIFIER
E loses independent status if M + action policy + arousal + context fully account for the reproducible multisystem structure and targeted perturbation reveals no independent coordinating state.
CURRENT DISTINCTION
E differs from I because I is a relatively stable/developmentally grounded action disposition whereas E is an activated, temporally extended coordinating state that can modulate many policies and systems.
E differs from M because E is not defined by viability preservation.
E differs from F because E is third-person functionally specifiable while F is defined by first-person qualitative presence.
==================================================
F — FEELING
==================================================
CURRENT DEFINITION
Feeling is a first-person qualitative/phenomenal state: there is something it is like for the subject to be in that state.
CURRENT TYPE
Phenomenal / experiential state.
CURRENT SUBTYPES
F_h = homeostatic/interoceptive feeling.
F_e = emotional feeling.
F_s = sensory-affective feeling if required.
F_report = explicit report/judgment.
F_phen = phenomenal feeling itself.
CURRENT FORMULA / MEASUREMENT MODEL
Let phi_t denote phenomenal state.
r_t ~ P(r | phi_t,a_t,l_t,demand_t,memory_t)
Report is an observation channel and is not identical to F_phen.
CURRENT DISTINCTION
F is defined by first-person qualitative presence.
M, I and E can be specified in third-person functional/causal terms.
F_report/access is measurable but F_phen is not uniquely identified by report alone without an explicit bridge/identity theory.
==================================================
GENERATION-0 CROSS-CONSTRUCT COMPARISON
==================================================
M:
trajectory/control -> viability preservation.
I:
state + development -> distribution/disposition over policies.
E:
time + body + relevance/context -> latent coordination state -> multi-system outputs.
F:
underlying mechanism/state -> phenomenal state -> imperfect report/access observations.
CURRENT ARCHITECTURE RESULT
The universal strict chain M -> I -> E -> F is rejected.
Generation-0 leading family is branching/recurrent, with additional neighboring variables such as drive/motivation, arousal, perception/interoception, learning/memory and cognition.
CURRENT CLAIM STATUS
M distinct: PASS.
Broad instinct as one natural kind: FAIL.
Narrow ICAD construct distinct: PASS.
Functional E distinct from one action disposition: PASS under explicit convention.
F distinct from functional E: PASS as an operational/ontological distinction.
Feeling unitary: FAIL / family label.
Strict M->I->E->F: FAIL.
Four exhaustive categories of human experience: FAIL.
BASELINE PURPOSE
All later recursive-tournament results must be compared against this exact checkpoint:
- retained unchanged;
- refined;
- split;
- merged;
- killed;
- or shown empirically/formally equivalent.