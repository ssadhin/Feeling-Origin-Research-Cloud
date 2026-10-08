# Research #2 comparator audit addendum v002 (2026-10-08)

This is append-only to `2026-10-08_nondecisive_source_audit_v001.md`, not a rewriting of that frozen historical checkpoint.

## ResearchLoop verified additional evidence
Pinned repository HEAD: `7e0a4fbe0cf646f4c859b6d20e46870d73abb11a`.

- `tests/researchloop/test_reproduction_registry.py` (source collection ERROR at line 28; malformed/unterminated string). Original upstream blob SHA = `750284f776a4adf6a80fb8331c0cd47a21c34652`; local `git hash-object` **exactly matched**.
- `tests/researchloop/test_smoke_harness_contract.py` (source collection ERROR at line 29; invalid UTF-8). Original upstream blob SHA = `767a1c56b08380e5782e17c26b6b8d67d8fbcce8`; local Git hash exactly matched (v001).
- `tests/researchloop/test_audit_sources.py`: one FAILED assertion/test because `experiments/researchloop/scripts/audit_sources.py` invokes `yaml.safe_load(path.read_text(encoding="utf-8"))` on a dossier that cannot decode as UTF-8, error near byte 1590; exit 1.
- `tests/researchloop/test_baseline_cards.py`: **9 passed in 0.23 s, exit 0**, showing at least one reproducible unaffected test subset.

**Verdict:** ResearchLoop is a valid strong comparator still awaiting robust fidelity review; this Windows-source snapshot has **partial runnable tests and an upstream encoding reproducibility defect**. Never call this an AES win, delete the method, substitute a weakened wrapper, or silently patch original source. If a corrected development copy is made, record exact byte changes and keep original and corrected versions distinguishable. Full behavioral-policy parity remains OPEN.

## Experiment boundary
All tests above are **nondecisive upstream/unit/syntax tests only**, not Research #2 outcomes.
H011 provider telemetry, resource/model/task freeze, statistical preregistration and decisive authorization remain open.
