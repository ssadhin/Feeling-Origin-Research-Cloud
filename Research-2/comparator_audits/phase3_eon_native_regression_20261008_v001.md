# Research #2 — Phase 3 fidelity continuation, 2026-10-08

Pre-freeze development record, NOT certification or decisive benchmark.

Office Eon CHOLOSPEED selected; research commands used Eon only. All six pinned upstream HEADs independently rechecked and Git worktrees clean. Original SHA anchors remain as recorded in 19H.

ResearchLoop: tracked sparse file docs/research/CURRENT restored through `git sparse-checkout add`, then tracked docs/research/V6 directory restored after CURRENT resolved to V6; git status remained clean, no upstream edits.
- Full tests/researchloop collection: two upstream parsing/UTF-8 syntax errors; process proc_95b2601500f24dd5890d.
- Excluding two uncollectable modules, initial six-test-file run: 25 PASS/10 FAIL (missing CURRENT and malformed UTF-8); process proc_5aea3ec4b536457c98f2.
- After restoring CURRENT, 25 PASS/10 FAIL, with missing V6 now exposed; process proc_f9ec361b42ea497d998f.
- After restoring V6, same six-file run: **26 PASS/9 FAIL**, exit 1, process proc_5a6aada567ca4ec79085. Nine remaining failures are source/fixture decoding issues; source files unchanged. Two uncollectable test files remain outside this 35-test subset.
- V1 focused test after V6: 5 PASS/1 FAIL; failure invalid UTF-8 in V1 PAPER_SCOPE.md; process proc_8b401679eb38443e9929.
- ResearchLoop license still unresolved; author/defender validation of any repair required.

Four-rival source AST/source-method exercises were independently rerun through Eon in clean pinned trees; managed process proc_f1d84ef859d246429cd7 exit 0:
- AI Scientist-v2 Node stage/parent routing: 9/9 PASS; mutation detected (2 failures).
- InternAgent original generation/evolution failed-memory source methods: 7/7 PASS; both source-method mutants detected (2 failures each).
- EvoScientist original MemoryScheduler: 8/8 PASS; mutation detected (1 failure).
- EvoMaster X-Master source selector: 12/12 PASS; mutation detected (2 failures).
- These are *narrow original code mechanism tests* with selective AST extraction/test doubles; no policy-wide execution, no provider invocation, no decisive test. Synthetic intentionally triggered logging messages are expected in their negative-control tests.
- OmniScientist historical upstream unit evidence remains as documented in 19G: selected runs passed, one independent timing failure retained. No new full-fidelity claim.

Canonical gate 19C/19G requires complete source-native defining sentinels with mutation controls, tested dependency environment, provider/broker/permission parity, independent knowledgeable defender, and frozen final executable. None of six rivals yet meets all gates. Full six-rival fidelity: 0/6; source acquisitions: 6/6; AES v2 prospective decisive trials: 0.

AES v2 inherited evidence from Research 1 P14/P15 but AES v2 itself was post-benchmark synthesis; no comparative superior/equivalent/inferior verdict from Research 2. No changes to frozen contestants or benchmark conditions were made.

Next: author-approved/defender-approved ResearchLoop fixture resolution and license clearance, isolated reproducible dependencies for all methods, full 19C execution and independent defender assessment, matched common broker. Do not interpret test failures as policy inferiority.

## Further native dependency-closure blockers (Office audit312 env)
- OmniScientist-V2 two selected native test modules (paper-review script / research provenance): base pytest collection failed because `omni` was not installed / on PYTHONPATH (Eon managed process proc_ebc41af7c9074076bfd6, exit 1). After setting only source PYTHONPATH=cli/src, collection reached package import and failed on missing `httpx` (proc_7b073a26b594402e9e5a, exit 1). No native test result can be inferred from collection errors; CLI uv.lock exists but was not provisioned into dedicated reproducible env.
- EvoScientist original upstream tests/test_scheduler.py collection in audit312 failed on missing `httpx`; warnings indicated missing pytest-asyncio options (proc_6fa07c494a7d4bafb2ab, exit 1). Do not count as an upstream test assertion failing or infer method inferiority.
- Resource-safe decision: no dependency installation in shared audit environment; dedicated isolated pinned/hashed reproducible envs still required.
