# LRA v0.1 synthetic consistency result

Status: internal-coherence simulation only; not empirical evidence for phenomenality.

Model class: recurrent hierarchy with homeostatic state (H), automatic valuation (V), emotion state (E), organism-state representation (P), reasoning (R), and affective output (F). Memory enters at implicit and explicit channels.

Frozen settings: seed=123; N=100,000.

Observed summary from the frozen model:
- Baseline: sd(F)≈0.545; sd(R)≈0.661.
- Suppress V: sd(F)≈0.502; sd(R)≈0.659.
- Suppress P: sd(F)≈0.427; sd(R)≈0.643.
- Suppress R: sd(F)≈0.499; sd(R)=0 by intervention.
- Suppress H: sd(F)≈0.506; sd(R)≈0.663.

Interpretation:
1. The recurrent model can support substantial reasoning variance when organism-state/affective channels are attenuated.
2. It can support substantial affective variance when explicit reasoning is removed.
3. It therefore implements the desired double-dissociation architecture.
4. This is not confirmation because the architecture generated its own synthetic data.
5. The empirical target is a preregistered causal double dissociation in independent human data.

Falsified conceptual target: the strict feed-forward ladder H→V→E→F→R is too strong given known bypasses and dissociation evidence.

Next executable scientific action: preregister an empirical model comparison and causal intervention design separating sensory representation, affective significance, report/access, and reasoning.
