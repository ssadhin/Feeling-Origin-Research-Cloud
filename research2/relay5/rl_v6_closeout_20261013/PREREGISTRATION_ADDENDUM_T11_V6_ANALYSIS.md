# Additive T11 preregistration — ResearchLoop V6 statistical analysis path lineage
Date: 2026-10-13 Asia/Dhaka; before T11 execution. NONDECISIVE source-origin scope.

Discovered during the preregistered T08 source inspection, prior to this T11 amendment:
- official docs/research/V6/rqs/RQ01/TASKS.yaml@9aff84c87ba7dde1b28394cf855fc8e443d87b8b specifies T07 statistical analysis of V6 tasks, using the command: python experiments/v6/analysis/compare_conditions.py --blocks 15.
- official experiments/v6/analysis/compare_conditions.py@b8f4ccb2b27875b57a887ccc74b26bce21962fdc has V5 data/report paths, a 6-task TASKS list, 3 conditions, and docstring 'RQ01 T06'. This static discrepancy is **already observed** and not a fresh predictive discovery.
Test prospectively whether actual native source when run with V6-only fixture input still attempts to access V5 paths; whether with archived V5 data present it produces a V5 report instead of V6 report; if runtime dependencies prevent execution, classify BLOCKED rather than simulating native result.

Checks:
T11a exact pinned source hash, infer from source to record path/shape, compare T07 command and actual source constants; mark static observation only.
T11b actual native source under fresh isolated scratch copy of source, with V6-only minimal data but no V5 data; expect FileNotFoundError on V5 path (or import dependency BLOCKED). No modifications to shared original.
T11c independent negative control: supply V5 fixture in scratch, verify module takes V5 input and V5 output path, not V6 output, or record exact exception.
T11d mutation control on diagnostic path matcher: replacing V5 with V6 must flip mismatch decision; no claim that patched version equals genuine upstream.
T11e two distinct processes if capable, SHA-256 receipts; ledger any invalid controls and dependency blockers.

Do not change frozen scientific criteria, original source, task records, model permissions, provider funding, or sensitive credentials. If original compare_conditions.py is historical carryover intentionally and V6 uses another analysis script, classify this as T07 command/source provenance mismatch, NOT entire V6 scientific statistical result invalidation. Exact next step would be author-defended intended V6 analysis entrypoint identification and sampled output lineage validation. 19C full fidelity remains BLOCKED and GOAL_RESOLVED NO.
