# Research #2 — EvoScientist cross-task memory context sentinel (v001)

Date: 2026-10-09, Asia/Dhaka. Nondecisive PRE-FREEZE developmental source-native test; not a frozen AES-v2 prospective comparison.

## Frozen original source
- Official EvoScientist/EvoScientist pinned commit: `3b382b92b8fdad6e1f13467c382dcdd91d9b19d2`.
- Git worktree checked clean before/after both runs.
- Python 3.12.10; isolated `C:\Users\hasad\Research2\venvs\evosci312\Scripts\python.exe`.
- Test source stored adjacent in this audit, SHA256 of original on Google Drive Windows filesystem: `B1547994AC487B6019F048ED893C4E7B7762C45B7DDDDBA3ACA270AE442F23EB`. GitHub has normalized LF text; do not assume same raw-file SHA256 after normalization.
- Test harness remains outside official checkout. No changes to upstream, no model/provider calls and no sealed Research 2 tasks.

## Source-native development checks
1. `test_prior_failed_direction_reaches_later_task_only_with_memory`: store a project-scoped prior *failed* direction through the official observation-store entrypoint; start a separate later request through the original `create_memory_middleware`; assert the unique failure summary appears in the later model-request system context; assert it did not appear before memory was written, and disappears when original `enable_observation_memory=False` ablation is used.
2. `test_project_scoped_failed_direction_not_in_other_workspace`: same source memory store, two distinct project IDs; assert later request for unrelated project does not include project-A failure.

## Reproduced runs
- Run 001: exit 0; 2 passed in 15.40 seconds; log `G:\My Drive\Consciousness Formula Research\09_Checkpoints\EvoScientist_ES3_ES5_cross_task_20261009_v001\run001_stdout.txt`; SHA256 `5311C8A96C55DBA438608761F31AA1525F25A19EBEE9A8BEBB2F72534FAE044D`.
- Run 002: independent second test process; exit 0; 2 passed in 8.88 seconds; log same checkpoint directory `run002_stdout.txt`; SHA256 `304EAF5E60D036C1D61D9E1D72221A6A03E8F360BFCAB16557271D3D761B21AF`.

## Critical interpretation
The tests support ES-3 negative-outcome observation accessibility, ES-4 later-task *context availability*, and ES-5 memory-enabled/disabled isolation at the original middleware boundary. They do NOT establish that an end-to-end later-task agent retrieves a relevant memory, acts differently, improves decisions, nor ES-1 distinct researcher/engineer and ES-2 evolution-worker behavior. This result adds source-native evidence, not full policy fidelity certification. Full six-rival 19C/19G/19H gate remains 0/6; AES-v2 decisive trials remain zero; winner/loser/equivalence outcome UNDERDETERMINED.

## Independent supervisor infrastructure (not science)
Home Eon original MCP module `tests/test_eon_telegram_alerts.py`: 15 unittest tests passed, exit 0; local Windows temp log `C:\Users\hasad\AppData\Local\Temp\eon_telegram_tests_20261009_loop1.txt`, SHA256 `C7349D3573F0470AC2956A7601B58AFB6E0BA810979F86F26E6A251FD85C49B6`. Live Telegram delivery and safe same-tab continuation NOT established. Never automatically repeat ambiguous prior send. Bot credentials not configured and no network Telegram call was made by tests.

## Next exact executable science action
Construct and run a no-provider source-native closed-loop EvoScientist later-task consumer that *actually invokes* relevant memory-retrieval tools and changes a predeclared task action under memory ON vs OFF, then independently defend ES-1..ES-5. Keep this as nondecisive and persist failures. Do not mark 19G pass or open sealed AES trials.
