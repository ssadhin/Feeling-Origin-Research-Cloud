# Research #2 — OmniScientist original-source timing reproducibility, second run

Date: 2026-10-08
Classification: NONDECISIVE original-source methodology-fidelity/reproducibility development evidence.
No AES v2 vs competitor outcome observed.

Upstream: tsinghua-fib-lab/OmniScientist-V2
Frozen input commit: 1cbb9f6f6d793290326ca29df4d389fb64832f91
Original native source: cli/tests/agent/test_paper_review_engine.py
Execution: C:\Users\hasad\Research2\venvs\omni312\Scripts\python.exe -B -m pytest -q -p no:cacheprovider tests/agent/test_paper_review_engine.py
Source working tree before and after: CLEAN for both.
Provider: no real external model requests; upstream mocked test.

Run 1: 30 PASS, 1 FAIL (test_engine_starts_mineru_first_and_overlaps_semantic_scholar[False-partial-7]), runner exit_code=1, elapsed=17.35 s. Expected three_way_overlap_seconds > 0; observed 0.0. Native pytest reported 14.68 s.
Run 1 evidence JSON SHA256: 79f16b715fd90a1bd2b13a8f631e0928dce5e876942fb2c84d95cf045a6ebace.
Location: G:\My Drive\Consciousness Formula Research\09_Checkpoints\OmniV2_native_timing_20261008_v001\run001.json.

Run 2: 31 PASS, 0 FAIL, runner exit_code=0, elapsed=11.944 s. Native pytest reported 10.30 s.
Run 2 evidence JSON SHA256: 72112f7c50fdd16ca295efd7d94fddf249770d5b76214a6f8d54901219c5e24e.
Location: G:\My Drive\Consciousness Formula Research\09_Checkpoints\OmniV2_native_timing_20261008_v002\run002.json.

Reproducibility observation: outcome differs across two full native pytest invocations with pinned original source and no edits; likely timing/order/load sensitivity and not demonstrated deterministic functional failure. Preserve both outcomes (never replace first failure with later pass). This does not certify OS-1..OS-6 or prove superiority/inferiority of any research methodology. Scientific gate: full six-rival fidelity 0/6, decisive AES v2 comparisons 0, independent defender parity OPEN.
Next nondecisive action: controlled repeated original-source paper-review test with recorded host load/event timing, upstream concurrency-source inspection and a defensible flaky-test label. Preserve the mocked native source and exact commit; avoid test rewriting in the frozen source. Once reproducibility characterized, finish source-native method/construct sentinels and independent review before tournament freeze.

Infrastructure note: Original Eon MCP browser source was updated with a per-device authenticated persistent Playwright bridge (eon_browser_bridge.py; no extra ChatGPT plugin); release generation 276ba1ecfd1e7dc5d68c8eb7bc431090b0963b5cee3238ae1b184aa15e01566c. Independent 13+7+7=27 tests PASS; Home Chrome project URL persisted across independent Eon requests. Browser text/Enter submission and fully unattended scientific continuation NOT YET VERIFIED.