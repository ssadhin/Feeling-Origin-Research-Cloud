FOUR-CONSTRUCT ARCHITECTURE ENUMERATION v001
Date: 2026-10-07

Interpretation of nodes:
M = self-maintenance
I = narrowly operationalized canalized action disposition
E = functional emotion-state
F = feeling

SEARCH SPACE
A four-node directed graph with no self-loops has 12 possible directed edges, hence 2^12 = 4096 possible directed graphs when recurrent cycles are allowed.

Exact enumeration result:
- Directed graphs without self-loops: 4096
- Directed acyclic graphs (DAGs): 543
- Markov-equivalence classes among the 543 DAGs: 185
- Total strict linear orders of four labeled constructs: 24
- Strict linear orders with M forced first: 6
- If M is first and E is additionally required before F: 3

CONSEQUENCE
The labels themselves cannot identify a unique causal architecture. Even restricting to DAGs leaves 543 candidates, and observational conditional-independence information collapses them into 185 Markov-equivalence classes. Interventions, temporal constraints, mechanistic knowledge, or stronger assumptions are required.

STRICT SERIAL MODEL
M -> I -> E -> F

Under causal sufficiency and faithfulness, this chain implies:
M independent of E conditional on I.
M independent of F conditional on E.
I independent of F conditional on E.

The enumeration script verifies all three d-separations.

HOMEOSTATIC-FEELING ATTACK
Add a direct M -> F route as the four-node projection of a body-regulation/interoceptive path to homeostatic feeling.

Then:
M is no longer independent of F conditional on E.
I is no longer independent of F conditional on E because I <- M -> F opens an association not blocked by conditioning on E.

This is the formal reason that a genuine homeostatic/interoceptive feeling route is incompatible with the universal strict chain.

LIMIT
The graph calculation does not prove that M -> F exists. That premise comes from the scientific literature on homeostatic/interoceptive feelings. The computation shows the structural consequence once that empirically motivated bypass is admitted.

VERDICT
The original strict four-node chain is not just one untested story; it has explicit conditional-independence consequences that differ from branching alternatives. The project should therefore treat causal architecture as an intervention/model-selection problem, not infer order from verbal depth.
