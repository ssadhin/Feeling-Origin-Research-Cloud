# Research #2 — Nondecisive comparator audit checkpoint (2026-10-08)

**Status:** DEVELOPMENT/FIDELITY AUDIT ONLY. Not final contestant freeze; no AES-vs-rival benchmark, sealed task, or hidden evaluator was run.

## Home-computer environment
- Connected authorized Windows 64-bit workstation via Desktop Commander.
- Isolated comparator checkouts in the Research2 workspace; Python 3.12 used for checks.
- No supported provider API credential was found in the inspected environment-variable list. H011 authoritative provider usage/retry telemetry remains BLOCKED_REAL_PROVIDER.
- These source checks are *not* evidence of scientific efficacy.

## Public upstream commit candidates, independently cloned and HEAD-verified

| Candidate | Exact inspected source commit |
|---|---|
| The AI Scientist-v2 (SakanaAI/AI-Scientist-v2) | `96bd51617cfdbb494a9fc283af00fe090edfae48` |
| InternAgent-1.5 (InternScience/InternAgent) | `fa8c3eedfa9751d3752ea6eb49220b303ac2397d` |
| OmniScientist V2 (tsinghua-fib-lab/OmniScientist-V2) | `1cbb9f6f6d793290326ca29df4d389fb64832f91` |
| EvoScientist (EvoScientist/EvoScientist) | `3b382b92b8fdad6e1f13467c382dcdd91d9b19d2` |
| ResearchLoop (plan-lab-szu/ResearchLoop) | `7e0a4fbe0cf646f4c859b6d20e46870d73abb11a` |
| EvoMaster (sjtu-sai-agents/EvoMaster) | `36a52bc6c42a6b9fd710a41c52f3c3bb948b9ac9` |

All six commit IDs were verified by GitHub repository-head references and independent local Git checkouts on this date. **They are inspection anchors only**; neither a version freeze nor a passed executable-policy fidelity audit.

## Measured nondecisive results

**OmniScientist V2:** installed an isolated local Python 3.12 environment from the pinned source as `-e .[dev]`; ran:

`python -m pytest -q tests/research/test_research_verify.py tests/research/test_provenance.py tests/agent/test_plan_pipeline_invariants.py --disable-warnings --maxfail=1`

Result: **23 passed in 125.06 s; exit 0**. Supports the audited source's claim/evidence-verification, provenance, and planning-invariant paths *on this Windows development setup only*. Does **not** prove OS-1..OS-6 functional/behavioral fidelity under the future neutral harness.

**ResearchLoop:** initial local shallow clone had an incomplete worktree; repair `git -c core.longpaths=true restore --worktree --source=HEAD -- .` completed with exit 0, revealing `src/`, `tests/`, and `experiments/` that were always present in the pinned Git tree. Do not misclassify it as a docs-only repository. Executed two selected upstream pytest modules individually with the isolated Python 3.12 environment:
- `tests/researchloop/test_smoke_harness_contract.py`: collection **ERROR**, upstream file contains invalid UTF-8 (line 29); exit 1. Local `git hash-object` and `git rev-parse HEAD:<path>` both `767a1c56b08380e5782e17c26b6b8d67d8fbcce8`, therefore this is not a local byte mutation.
- `tests/researchloop/test_reproduction_registry.py`: collection **ERROR**, malformed/unterminated quoted source at line 28; exit 2. This second test's byte hash should be verified independently before attributing it definitively to upstream.
- No assertion-level test for these modules ran. Classification: **SOURCE_TEST_BLOCKED**, not ResearchLoop-method FAIL and not an AES win. Corrected private testing copies, if needed, must be versioned separately and cannot be misrepresented as original upstream code.

**EvoScientist:** `py -3.12 -m compileall -q .../EvoScientist/EvoScientist`: exit 0. **Syntax smoke only**, not runtime fidelity.

**EvoMaster:** `py -3.12 -m compileall -q .../EvoMaster/evomaster`: exit 0. **Syntax smoke only**. Official source shows X-Master Solver→Critic→Rewriter→Selector phases and optional post-run `--evolve` wrapper. Do not compare an abstract EvoMaster framework by allowing it arbitrary unfrozen agents or switches. Provisional strongest fixed representative: X-Master with the optional evolutionary wrapper **only if** exact resource accounting and topology compatibility are independently verified; this is not yet a frozen or certified configuration.

## Version-choice observation
OmniScientist V2's `v2.0.0rc8` annotated release tag targets `f2d6b359a9fa521033cd174adde0bad34cf6ac12`. The current head is 2 commits newer and includes material runtime/design-document and other changes. Both are immutable via SHA, but this audit uses the newer `1cbb9...` head; final selection must preserve defining behavior and fidelity parity, not simply prefer a version because it performs better.

## Unresolved gates
- H011 authoritative real-provider token/cached/reasoning usage and retries: BLOCKED_REAL_PROVIDER.
- ResearchLoop test-source error: BLOCKED upstream selected test modules; repair lineage/sensitivity or unaffected modules needed.
- All six comparator method-fidelity behavioral sentinels: NOT YET PASSED.
- Strongest fixed EvoMaster representative and optional evolution overhead: NOT FROZEN.
- Exact common model, tasks, resource caps, metrics/SESOI, N, multiplicity, OOD, preregistration, and final container: NOT FROZEN.
- AES v2 and P14/P15 implementations: NOT FROZEN.

## Scientific conclusion
**AES v2 decisive comparisons: 0 completed.** Scientific claim ceiling remains unchanged: AES v2 is prospective/unvalidated, and neither the six external rivals nor P14/P15 have a Research #2 decisive outcome in this audit.

## Exact next safe action
Reproduce and classify ResearchLoop source-test errors on a byte-clean Linux snapshot or isolated corrected development copy; run an unaffected audit-sentinel set; finish source-derived behavioral fidelity tests for OmniScientist V2, EvoMaster and the remaining candidates; continue provider-telemetry work only when a legitimate provider credential/runtime is available. Preserve all failures and do **not** open decisive benchmarks before preregistration.
