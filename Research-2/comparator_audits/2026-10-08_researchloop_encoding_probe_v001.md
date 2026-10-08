# ResearchLoop encoding probe — 2026-10-08

Pinned original Git commit: `7e0a4fbe0cf646f4c859b6d20e46870d73abb11a`. No decisive runs.

| File | UTF-8 decode | GB18030 decode | Parse after GB18030 |
|---|---|---|---|
| `tests/researchloop/test_smoke_harness_contract.py` | FAIL | PASS | Python AST PASS |
| `tests/researchloop/test_reproduction_registry.py` | FAIL | PASS | Python AST FAIL (line 28 unterminated literal) |
| `docs/research/V0/reproduction/REPRODUCTION_LEDGER.yaml` | FAIL | PASS | YAML parser FAIL (mapping near line 28) |

Conclusion: blind transcoding does not repair the source reliably and could change semantics. Keep untouched upstream. A separately versioned byte-local repair/diff is needed before calling the selected tests executable. ResearchLoop's unaffected `test_baseline_cards.py` still passed 9/9. These are source-integrity outcomes, **not** AES-versus-ResearchLoop evidence.
