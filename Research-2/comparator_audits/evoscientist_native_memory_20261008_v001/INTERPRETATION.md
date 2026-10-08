# EvoScientist — Original native memory checks (2026-10-08)

**Scientific classification:** exploratory Phase 3 source-native reproducibility only; **not** a full ES-1..ES-5 methodology-fidelity certification and **not** a prospective AES v2 comparison.

- **Source:** `EvoScientist/EvoScientist`, pinned commit `3b382b92b8fdad6e1f13467c382dcdd91d9b19d2`; Git working tree clean before/after each run.
- **Tests:** unmodified original upstream `tests/test_observation_memory.py` SHA256 `7130002f8c47be1ff33843e3ea4de4df0613770d86689b513be905febc3662ff` and `tests/test_profile_memory_middleware.py` SHA256 `33137b34e45e46895a2927c341c5175dbecced912c5e19afd0f06ed928f53c0f`.
- **Isolated native Python:** `C:\Users\hasad\Research2\venvs\evosci312\Scripts\python.exe` 3.12.10 with pytest 9.1.1; `pytest-asyncio` present.
- **Provider access:** prevented via disabled proxies, no authorized external LLM/model calls.
- **Run 001**: `157 passed, 9 failed` in ~28.49 s of pytest; exit 1, total ~29.96 s. The runner mistakenly set `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, suppressing installed `pytest-asyncio`; all nine errors explicitly reported unsupported `async def` and the project's `asyncio_` pytest options were unrecognized. **Infrastructure/run-harness error**, not established EvoScientist scientific failure.
- **Run 002**: corrected **only the external runner** to permit automatic plugin loading (upstream checkout and test bytes unchanged). `166 passed`, 0 failed in 22.78 s of pytest; total ~25.982 s; exit 0.
- **Reproducibility:** original upstream Git checkout unchanged before/after both tests; both raw outcomes archived, no selective green-result deletion.
- **Claim ceiling:** this verifies that selected native memory-observation/middleware tests can run under a correctly configured offline environment. It **does not** demonstrate task-level evolution, persistent cross-task memory transfer, source-faithful complete policy execution, matched provider/tools, independent defender review, or equal-cost harness action fidelity. Thus full ES-1..ES-5 gate remains **OPEN**.
- **Next adversarial action:** create a bounded source-derived *negative/positive observation-memory-to-later-task* behavioral sentinel within a neutral budgeted broker; show that removing prior-task memory changes a future task's choice under matched initial conditions, and an independent knowledgeable defender audits the proposed sentinel before freezing. No sealed benchmark or prospective decisive trial may run before gates close.

Raw runner/result files: `run001.json`, `run002.json`, `runner_v001.py`, `runner_v002.py`. They are immutable append-only snapshots from the user's `G:\My Drive\Consciousness Formula Research\09_Checkpoints` output location.

**AES v2 decisive Research #2 trials remain 0. No methodology winner is established.**
