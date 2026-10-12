# Research #2 Relay5 — EvoMaster class-level trajectory isolation PRE-EXECUTION v001
Date: 2026-10-12 Asia/Dhaka. Nondecisive development only. Frozen before executing new test.
Official upstream: sjtu-sai-agents/EvoMaster @ 36a52bc6c42a6b9fd710a41c52f3c3bb948b9ac9
Primary original file: evomaster/agent/agent.py; expected Git blob 696984729eda88eaac900db26ae7d1152f6f430b.
Secondary original: evomaster/core/playground.py blob 32b4ec763ecd74e72d84483b226e95beb40461bb.
Prior v022: normal single-process writer emits one entry per step; full native integration untested.
Question: In the original BaseAgent class-level path/experiment metadata, can two distinct agent instances in a single Python process overwrite one another's destination and experiment label when interleaved?
Synthetic fixture: agent A task_id=A path=A/trajectory.json exp=(alpha,1); agent B task_id=B path=B/trajectory.json exp=(beta,2). Set A class path/exp, set B class path/exp, then append A step and B step using original AST-extracted unmodified class methods. All files are isolated temporary synthetic files.
Primary observation (not comparative success metric): A's record appears under B path or B exp label. If yes classify bounded class-state isolation failure, not full native multi-process workflow failure.
Controls: (1) single A writer correct path/label; (2) two agents same shared path intentional multiplex both records; (3) missing path produces no output; (4) reversed interleave routes B to A; (5) separate class per-agent-state mutation prevents cross routing; (6) source exact Git SHA and original AST method text verification; (7) two independent deterministic processes with matching normalized receipts; (8) no provider calls, no external tools, no sealed benchmark.
Failure: if upstream blob differs, test blocked. If original method extraction or dependency stubs cannot execute, BLOCKED. If cross-routing absent, NULL not FAIL. If present, FAIL_BOUNDED_CLASS_STATE, native concurrency admissibility remains OPEN.
No changes to 19C/19G/19H or prereg21. No AES comparison, no model costs. Do not modify original repository. Defender must inspect actual launcher topology and whether two playground instances share process before attributing real-world native impact.
Provenance: pre-execution commit in isolated Research2 branch; result to follow as separate commit and Drive checkpoint; no concurrent experiment reuse.
