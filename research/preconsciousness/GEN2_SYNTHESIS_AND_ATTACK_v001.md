GENERATION-2 SYNTHESIS AND ATTACK v001
Date: 2026-10-07
Method: Generated only from Generation-1 comparisons, failures, equivalences and residuals.
Rule: These are new candidates, not silent rewrites of Generation 0.
==================================================
M10 — CONSTITUTIVE-VIABILITY SELF-MAINTENANCE
==================================================
DEFINITION
Self-maintenance is the coupled set of endogenous processes by which a living system:
(1) keeps viability-relevant state variables inside recoverable bounds, and
(2) regenerates/repairs the organization or constraints that make those regulatory processes possible.
WHY GENERATED
M4 captured viability geometry but not constitutive self-production.
M5 captured organizational regeneration but was abstract about state regulation.
M9 captured multiscale regulation but did not explicitly type the constitutive part.
M10 is their conjunction.
FORMALIZATION
Let x_t = physiological/functional state.
Let c_t = constitutive/organizational state or constraint configuration.
Let u_t = regulatory/repair control.
Let w_t = perturbation.
x_(t+1) = f_x(x_t,c_t,u_t,w_t)
c_(t+1) = f_c(c_t,x_t,u_t,w_t)
Let A be the admissible living-region in joint state space:
A = {(x,c): viability constraints hold AND constitutive organization remains/regenerates within admissible bounds}.
M10_H(x_t,c_t,pi) =
P_pi[(x_(t+k),c_(t+k)) in A for all k=0,...,H | x_t,c_t].
OPTIONAL DECOMPOSITION
M_reg = short/medium-timescale regulated-variable control.
M_const = repair/turnover/constraint regeneration.
M_pred = anticipatory/allostatic control.
M10 does not claim that these three are always separable biological modules.
ATTACKS
Attack M10-A: Is organizational closure necessary for every operational use of "self-maintenance"?
Result: NO. Physiology can study self-maintenance without committing to autonomy theory.
Consequence: M10 cannot be imposed as the only disciplinary definition.
Attack M10-B: Can viability be maintained externally?
Yes. External life support/protection can improve survival without endogenous self-maintenance.
Consequence: survival probability is not identical to M10.
Attack M10-C: Can constitutive regeneration occur while selected regulated variables leave nominal setpoints?
Yes. This supports joint state/organization modeling rather than fixed setpoint identity.
STATUS
PASS as a broad project-level synthesis.
Not a field-wide canonical definition.
Generation-2 refinement required: distinguish constitutive criterion from operational physiological measures rather than requiring every experiment to observe c_t directly.
==================================================
I16 — DEVELOPMENTALLY CANALIZED PREPARED POLICY LANDSCAPE
==================================================
DEFINITION
An instinct-like action architecture is a developmentally produced landscape of policy biases that:
(a) recurs with measurable robustness across a defined normal ecological/developmental range;
(b) is present before the specific task-learning history used to create an ordinary acquired habit;
(c) can still require developmental experience;
(d) is expressed conditionally on current sensory/internal state.
WHY GENERATED
I1-I3 failed.
I8 survived developmental critique.
I9 supplied computational policy language.
I10 supplied robust developmental convergence.
I7/I5/I14 are useful motor subtypes/implementations.
FORMALIZATION
Let d denote developmental history.
Let h denote task-specific learning history.
Let s denote current state/context.
Let pi denote policy.
P(pi | s,d,h) proportional to exp(beta [B_0(pi,s,d) + Q_h(pi,s)]).
B_0 is the prepared/developmentally produced policy-bias field.
Q_h is task-specific acquired value/bias.
CANALIZATION
C_I(s) =
1 - E_{d,d' in D_N}[JSD(P_0(pi|s,d),P_0(pi|s,d'))]/log(2).
TASK-LEARNING DEPENDENCE
L_task =
I(Pi ; H_task | S,D).
PREPAREDNESS INDEX
A candidate vector, not a scalar:
I16 = (pre-task bias strength, developmental robustness, task-learning dependence, trigger specificity, population regularity, developmental requirements).
ATTACKS
Attack I16-A: What if a behavior is species-typical but learned socially?
Then species-typicality alone does not qualify. I16 requires evidence about task-specific learning dependence and developmental robustness.
Attack I16-B: What if a reflex qualifies?
Some reflexes may occupy a low-complexity region of I16, but reflex must remain a subtype because direct sensorimotor transformation does not exhaust prepared policy landscapes.
Attack I16-C: What if a learned habit becomes highly robust?
Robustness after learning is not enough; the relevant comparison is pre-task or independently developed bias versus the task-specific history that creates the habit.
Attack I16-D: Is "instinct" still one natural kind?
No. I16 is an operational replacement for one scientifically useful portion of the broad word.
STATUS
PASS as a stronger replacement than Generation-0 ICAD.
It is not equivalent to broad ordinary "instinct."
==================================================
E16 — DUAL-LEVEL EMOTION ORGANIZATION
==================================================
DEFINITION
Because major emotion theories disagree over whether feeling is constitutive of emotion, use two explicitly typed targets:
E_func:
a third-person functional emotion organization — a temporally structured coordination trajectory among appraisal/relevance, physiology, action readiness, attention/valuation, expression, and learning/decision systems. Phenomenality is not part of this definition.
E_episode:
a full theory-dependent emotion episode. Under component-process and some ordinary usages, E_episode may include conscious feeling as one component.
WHY GENERATED
E3 survived but "central latent state" was too restrictive.
E4/E11 support component coordination/distributed dynamics.
E7 shows categories can be constructed.
E15 shows "emotion" is a family-level field term.
Emotion Ontology distinguishes emotion process, subjective feeling, action tendency/disposition and behavior.
FORMALIZATION
Let the functional component vector be:
z_t =
[a_t, p_t, q_t, v_t, x_t, l_t]
where:
a_t = appraisal/relevance variables;
p_t = physiological/autonomic variables;
q_t = action-tendency/readiness variables;
v_t = attention/valuation variables;
x_t = expression/action-output variables;
l_t = learning/decision modulation variables.
Dynamics:
z_(t+1) = F_E(z_t, body_t, context_t, history_t) + epsilon_t.
COORDINATION MEASURE
E_coord may be represented by time-varying multivariate dependence/coupling among component trajectories:
K_E(t) = functional of cross-component coupling, persistence, scalability and generalization.
LATENT COMPRESSION IS OPTIONAL
A latent e_t may summarize z_t if it improves prediction/intervention, but E16 does not require a single central hidden variable.
FULL EPISODE
E_episode(t) = [z_t, phi_emotion(t)] only under theories that include conscious feeling as a constitutive emotion component.
Under functionalist work, E_func can be studied without assuming phi_emotion.
ATTACKS
Attack E16-A: Does broad coordination make everything an emotion?
Risk confirmed.
Required gate: organism-relevant elicitation + temporal episode structure + affective/valenced or motivational significance + coordinated multi-component change. Generic cognitive coordination is insufficient.
Attack E16-B: Is feeling necessary?
Theory-dependent. Therefore E_func and E_episode must stay separate.
Attack E16-C: Are discrete categories required?
No. E16 permits categorical, dimensional, constructed or mixed organization at a higher descriptive level.
Attack E16-D: Could core affect alone be E?
No under E16; core affect can be an ingredient/background state without full episode organization.
STATUS
PASS as Generation-2 leader for a theory-neutral research framework.
It is a refinement of Generation 0, not confirmation of a single latent central emotion state.
==================================================
F15 — PHENOMENAL FAMILY / MODE MODEL
==================================================
DEFINITION
Feeling is not assumed to be one content generator.
It is the family of first-person phenomenal states in which some bodily, affective, sensory, metacognitive or other content is experientially present.
SUBTYPES CURRENTLY REQUIRED
F_h = homeostatic/interoceptive feeling.
F_e = emotional feeling.
F_s = sensory/somatic feeling.
F_m = metacognitive/epistemic feeling.
F_a = core-affective/hedonic feeling where relevant.
F_report and F_access remain measurement/access variables, not identical definitions.
WHY GENERATED
F3/F4/F5/F6/F7/F8 all survived in restricted domains.
F12 failed as a definition.
F13/F14 jointly explained why the word applies across heterogeneous content families.
FORMALIZATION
Let c_t be content-generating state (which may be interoceptive, emotional, sensory, metacognitive, etc.).
Let phi_t be phenomenal presentation.
phi_t = Phi(c_t, X_t)
where X_t denotes whatever consciousness-enabling conditions eventually prove necessary.
This is a placeholder structural relation, not a solved consciousness equation.
REPORT MODEL
r_t ~ P(r | phi_t, access_t, language_t, memory_t, confidence_t, demand_t).
CONTENT-FAMILY MODEL
phi_t belongs to union of phenomenal families:
F = F_h union F_e union F_s union F_m union F_a ...
This set notation does not assert that the families share one neural generator.
ATTACKS
Attack F15-A: Is every phenomenal state a "feeling"?
Ordinary/scientific usage is inconsistent. Visual color phenomenology may be called experience rather than feeling.
Consequence: F15 must remain scoped to felt/affective/bodily/metacognitive phenomenology unless the project explicitly chooses the maximal philosophical usage.
Attack F15-B: Does "phenomenal mode" explain why anything feels?
No. It types the target and prevents category errors; it does not solve consciousness.
Attack F15-C: Can report validate phi?
Only indirectly. Report/access confounds remain.
Attack F15-D: Could homeostatic feeling simply be called emotion, as Denton does?
Yes under another terminology. This is why the project must type processes rather than infer structure from ordinary labels.
STATUS
PASS as a stronger family-level target than a unitary Feeling mechanism.
Mechanism of phenomenality remains unresolved.
==================================================
N25 — MOTIVATIONAL CONTROL STATE
==================================================
DEFINITION
A state that changes action direction, vigor, persistence or effort as a function of need, incentive, expected outcome and opportunity.
FORMAL ROLE
m_(t+1)=f_m(m_t,need_t,incentive_t,expectation_t,context_t)
P(action|s) is modulated by m_t.
ATTACK
Motivation overlaps emotion, reward and homeostasis but is independently represented in major frameworks and cannot be automatically absorbed into I or E.
STATUS
PASS as neighbor variable that the four-target model must condition on.
==================================================
N26 — AFFECTIVE BACKGROUND STATE
==================================================
DEFINITION
A slower or object-unspecific affective condition characterized by dimensions such as valence and activation/arousal, capable of modulating emotion episodes, cognition and action.
ATTACK
Core affect can be consciously accessible and mood-like; it may become part of an emotion episode but is not identical to every emotion episode.
STATUS
PASS as neighbor/background variable.
==================================================
GENERATION-2 INTEGRATED MODEL
==================================================
The four original words now map to different scientific roles:
M10 = constitutive + viability regulation.
I16 = prepared/canalized policy landscape.
E16 = functional component-coordination trajectory, with optional full episode including feeling depending on theory.
F15 = phenomenal family/mode with heterogeneous content generators.
Mandatory neighbors:
N25 motivation/drive.
N26 affective background/core affect/mood.
Plus arousal, perception/interoception, memory/learning, cognition/appraisal, and access/report as separate variables where needed.
No universal total order is implied.
==================================================
GENERATION-3 OPTIONS PRODUCED BY ATTACK
==================================================
M11 — TWO-TIER SELF-MAINTENANCE
Tier 1 constitutive self-maintenance: regeneration of enabling organization/constraints.
Tier 2 regulatory self-maintenance: feedback/predictive control of viability variables.
Reason: M10-A showed that physiology can study Tier 2 without measuring or endorsing a full autonomy-theory Tier 1.
I17 — PREPAREDNESS FAMILY
Instead of one I16 mechanism, represent instinct-like organization as a family of prepared biases:
reflex preparedness;
motor-pattern preparedness;
policy-selection preparedness;
perceptual/attentional preparedness.
Reason: I16 may still over-unify distinct prepared architectures.
E17 — EMOTION ORGANIZATION FAMILY
Replace one universal E_func state with a family of dynamical organizations sharing functional criteria but allowing multiple mechanisms and component topologies.
Reason: E16-A/E16-C leave open whether one coordination architecture covers all emotions.
F16 — FELT-PRESENCE TAXONOMY
Separate the generic property of phenomenal presence from content-specific feeling families:
P* = felt/phenomenal presence condition;
C_h,C_e,C_s,C_m = content generators;
F_x = P* applied to content family x.
Reason: F15-B shows feeling-family taxonomy and consciousness-enabling condition are distinct problems.
These Generation-3 candidates must undergo a new destruction/comparison round before convergence can be claimed.