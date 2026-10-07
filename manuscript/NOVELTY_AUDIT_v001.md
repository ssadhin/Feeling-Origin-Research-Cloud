# Novelty Audit v001 — AES v2 Research-Policy Paper

Date: 2026-10-07
Author: Hossain Ahmed Sadhin
Scope: documented search through 2026-10-07.

## Claim ceiling
This audit does not claim that no prior work exists. It records the closest work found and narrows the contribution to what remains defensible.

## Closest overlaps
1. Guo, Y. (2026). Evidence-Gated Research: Statistically Controlled Model Adoption in Adaptive Search. arXiv:2610.01751. Strong overlap in adaptive, path-dependent research/model search and frozen evidence gates. EGR contributes formal sequential error control that AES v2 does not provide.
2. Li, P. et al. (2026). Let the Abyss Stare Back: Adaptive Falsification for Autonomous Scientific Discovery. arXiv:2603.29045. Strong overlap in adaptive falsification and protection against static-evaluator overfitting.
3. Fei, Y. et al. (2026). How Do Agents Fail on AutoResearch: End-to-End Diagnostic Evaluation on 100 Real-World Frontier Research Tasks. arXiv:2608.14905. Strong overlap in process-level research failure analysis and metacognitive-loop failures.
4. Fu, S. et al. (2026). Beyond Solution-Centric Search: Adaptive Inquiry and Knowledge Revision for Autonomous ML Engineering. arXiv:2608.02143. Strong overlap in state-based adaptive epistemic/interventional actions under a finite budget.
5. Wang, B. et al. (2026). Towards Diverse Scientific Hypothesis Search with LLMs. arXiv:2606.10587. Overlap in diversity-preserving search over scientific hypotheses.
6. Zhong, T. et al. (2026). Before the Action: Benchmarking LLMs on Prospective Hypothesis Discovery. arXiv:2607.15766. Overlap in constructing hypothesis spaces when conclusions are withheld.
7. Hasib, M. M. et al. (2026). Unifying AI-assisted scientific discovery around exploration, hypothesis generation, and testing. Patterns, DOI 10.1016/j.patter.2026.101660. Overlap in workflow-level abstraction of exploration, hypothesis generation, testing, and feedback.
8. Gelman, A. et al. (2020). Bayesian workflow. arXiv:2011.01808. Prior art for iterative model building, checking, comparison, and refinement.
9. Platt, J. R. (1964). Strong Inference. Science 146:347-353. Prior art for multiple hypotheses and decisive tests.
10. Huan, X., Jagalur, J., & Marzouk, Y. (2024). Optimal experimental design: Formulations and computations. Acta Numerica 33:715-840. Prior art for sequential, information-efficient experiment selection.

## What is NOT novel enough to claim
- recursive science or iterative research;
- generating multiple hypotheses;
- adversarial/falsification loops;
- state-dependent research actions;
- preregistration or locked evaluation;
- OOD/replication testing;
- value-of-information or optimal experimental design;
- adaptive research agents;
- hypothesis-space expansion by itself.

## Defensible contribution
The paper's defensible novelty is the combined experimental framing:
1. treating complete research workflows as equal-budget policies over heterogeneous epistemic operators rather than benchmarking one isolated statistical tool;
2. explicitly evaluating recovery when the true hypothesis is absent from the initial candidate set;
3. including non-identifiability, lineage/ancestor recovery, software/measurement failures, analysis flexibility, and interacting OOD failure classes within the same policy benchmark;
4. making ancestor challenge and equivalence/underdetermination explicit research actions/outcomes;
5. freezing Generation-2 policies before a locked test and then exposing them to composite OOD worlds, where the development-leading P16 was allowed to fail;
6. using retrospective real-project failure replay to identify failure classes omitted by the synthetic winners and derive claim-triggered validity gates;
7. separating the empirically supported P14/P15 backbone from AES v2, which is explicitly presented as a post-benchmark synthesis requiring prospective external evaluation.

## Name search
The exact phrase "Adaptive Epistemic Search" did not reveal an established scientific-methodology framework in the documented searches. This is a bounded search result, not proof that the phrase has never been used.

## Publication recommendation
Do not market AES v2 as "the best scientific method." Submit the paper as a benchmark-and-methodology study of research policies under incomplete hypothesis spaces. The strongest claim is that the recursive/equivalence/ancestor backbone generalized better than the compared adaptive shortcut under the frozen synthetic/OOD benchmark, and that retrospective failure replay motivated a gated prospective synthesis.
