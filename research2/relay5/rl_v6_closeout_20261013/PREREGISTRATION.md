# Research #2 / Relay 5 — ResearchLoop V6 closure/evidence consistency source audit
Date: 2026-10-13 (Asia/Dhaka). PRE-EXECUTION scoped protocol. NONDECISIVE, no sealed data.

## Source / scope / transparency
Official plan-lab-szu/ResearchLoop@7e0a4fbe0cf646f4c859b6d20e46870d73abb11a. Exact original tracked Git blobs:
- docs/research/V6/STATUS.yaml: 7f5ed4394269a16859ae098ef42e8547f6c7e8a2.
- docs/research/V6/rqs/RQ01/TASKS.yaml: 9aff84c87ba7dde1b28394cf855fc8e443d87b.
- docs/research/V6/rqs/RQ02/TASKS.yaml: dba9bae33545b05c2d97553daa79796208c282bf.
- experiments/researchloop/scripts/audit_sources.py: a9ae4eecd47efe1679ae849f17b6c5b6905f4056.
No upstream source copied or committed to our GitHub: ResearchLoop pinned root license unresolved.

Read-only original checkout on Home Laptop G:\My Drive\Consciousness Formula Research\RL_v003, if available and pinned-clean; otherwise exact GitHub blobs only; controlled synthetic YAML in NEW temporary directory only. Never modify an upstream checkout, shared inputs, sealed benchmark, benchmark inclusion, 19C or 21.

## Adversarial question and prior disclosure
Does the original V6 status declare completed RQs while its task status records remain planned? Are declared closeout artifacts present? What does actual upstream code enforce? This protocol is NOT blinded: before registration we inspected GitHub-file contents for STATUS.yaml and both TASKS.yaml and saw closed_negative / completed_rqs entries and planned task entries. This is source-follow-up scrutiny, not a prospective efficacy claim.

## Prospective bounded checks
T01: verify exact Git commit, source blob identity and read-only checkout. If pin mismatch, BLOCK no source-original verdict.
T02: count RQ01 and RQ02 declared task statuses and relation to completed_rqs. Prediction: discrepancy present (already inspected, do not call prospective discovery).
T03: inspect all declared V6 closeout_artifacts for real tracked files at the same commit; prediction deliberately UNSPECIFIED (could all exist, some missing, or all missing). Count separately.
T04: inspect docs/research/V6/STATUS current_gate and paper_binding.allowed, without equating them to empirical truth.
T05: test independent strict diagnostic checker that rejects closed RQ with any task status not in {completed,done,passed}; mutation with all tasks marked completed should pass status coherence; mutation with reinserted planned task should fail.
T06: strict diagnostic checker rejects deletion of a required claimed closeout artifact; synthetic repair/restoration should pass file-reference presence.
T07: verify that original available executable audit_sources.py is V0-specific; do not assert it should validate V6. Test V0 checker (only if yaml dependency and repo checkout allow) against untouched repo, but do not count V0 success/failure as V6 controller pass.
T08: independently inspect pinned source tree for a source-original V6 runtime/controller enforcing task closure; report found implementation or BLOCKED, never invent.
T09: preserve fail/null diagnostics, hashes, interpreter version and exact limits. Two independent processes when feasible; strictly label test oracles diagnostic-not-upstream.
T10: negative control unclosed status with planned tasks must not be called a contradiction by coherence oracle; this tests discrimination, NOT original algorithm behavior.

## Interpretation precommit
Even if T02 shows stale statuses, do NOT classify V6 methodology failure without an author-defined rule that TASKS.yaml is live authoritative state. Possibilities: planned statuses are frozen work plan; independent closeout records supersede them; actual evidence artifacts exist; V6 status may intentionally reflect manual adjudication. If native runtime absent: NATIVE_V6_COMPLETION_ENFORCEMENT_BLOCKED, not FAILED. Any new finding limited to public static dossier consistency + controlled diagnostic.
No model inference, paid provider, or tool parity, so no 19C full PASS, no AES superiority, no GOAL_RESOLVED.
## Publication
Write raw results, independent verifier, source SHA, strict control results, failure log, and Relay 1 :36 handoff as append-only new Research2 files, canonical Drive folder 1PXwQlCDQfRLKvPQo3QuGX5-DiI7L4LbQ, isolated Git branch. Do not replace 17 current status, only additive amendment after result.
