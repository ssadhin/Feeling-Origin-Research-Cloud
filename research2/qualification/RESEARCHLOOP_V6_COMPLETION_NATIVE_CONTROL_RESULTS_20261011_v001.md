# Research #2 Q1 — original ResearchLoop V6 completion-gate controlled runtime result

**Date:** 2026-10-11 Asia/Dhaka. **Scope:** NONDECISIVE, source-original SOFTWARE CONTROL with a scripted external model chat method, NOT source-original LLM generation, NOT a fair AES head-to-head.

**Source:** unmodified official plan-lab-szu/ResearchLoop commit `7e0a4fbe0cf646f4c859b6d20e46870d73abb11a`, native `experiments/v6/harness/run_condition.py`, original V6 `condition_matrix.yaml`, `RTS11_ml_comparison/generate_workspace.py`, `oracle.py`. Source Git clean before and after independent runs. Original full condition declares passing pytest and required hash/log evidence for completion.

**Preexecution:** Research #2 Google Drive Docs [61 v001](https://docs.google.com/document/d/1FhRfX6mNgGzisqhTJ0QpDIRurOM2ZpodNoZd6m99z8k/edit) and [62 v002/v003 path/receipt corrections](https://docs.google.com/document/d/1TgT9Zr3LrN6x7I1AJQDbNFgzs8HtR99qw4oiVM6KRKo/edit). Exact v003 runner SHA256 `77959A9AD1F9E5363035D70970651BBB558CD9A4EFC5CCA946E39ACBEC4CFB7C`; test code frozen in repository `research2/qualification/researchloop_v6_original_run_one_gate_control_v003.py`.

**What actually ran:** original imported `run_one` with untouched task and full-condition config. Original workspace generator and oracle ran; original reports, 30 generated files per round and manifest were written and archived. The only substituted component was `ModelClient.chat`, which returned a plainly **synthetic** report asserting universally improved 99% accuracy while citing deliberately nonexistent `workspace/R2_CONTROL_NONEXISTENT_NO_EVIDENCE_20261011.csv`. No LLM API call, no paid inference and NO simulated output counted as research method performance.

**Independent process results:** run1 8/8 source and control sentinels PASS, receipt SHA256 `7b36234cfda90a916585ae11a620f368893a02662ebbc19a5906d720f0b59e30`; run2 8/8 PASS, receipt SHA256 `5843e7818ba87b10fe38f2fe0b88835eeba976b2fea0b19b2b5c2b1aa724d6f2`. Both original native full `run_one` returned `run_status=completed`, `completion_claim=completed` despite native oracle flags `generalizes=true, bounded=false, acknowledges_negative=false, references_all_datasets=false`, nonexistent evidence path and no recorded pytest result/exit. Negative control original provider exception returned failed/not completed; native dry-run refused completed and performed no provider call. Nonoriginal strict guard rejected the artificial unsupported report.

**FAIR FAILURE LINEAGE:** v001 runner SHA256 `935C726AC5247B64C6AD39E246945177A8D2FDDC99C11B8832077CCAF98B4B38` preserved exact original source's `transcript_path.relative_to(ROOT)` error when outputs were outside repo, 3 PASS/4 FAIL twice. v002 script SHA256 `A36F3F996EF346FE0B597A0036152341FD1841B86245E1BCB94EF0D659C68433` passed 8/8 twice but non-overwrite receipt guard exited1 after detection because v001 receipts already existed; archived source outputs and logs retained. v003 changed only output location/receipt file naming (after versioned preexec), original scientific control unchanged. All original source/output generation scratch cleaned after archive, git remained clean.

**Interpretation:** The tested original V6 `run_one` **does not enforce its own full-condition contract under a controlled scripted reply**. Other downstream ResearchLoop claim-admission gates might detect it; this is NOT proof the complete ResearchLoop methodology fails RL1–RL5 or AES v2 outperforms it. Require independent knowledgeable original-method defender and genuine matched-competence source-native trial before eligibility judgment. Original V6 audit's separate lexical evidence false positive and V0 mock-only status have their own permanent notes; do not conflate.

**Immutable indexed supporting artifacts in this branch:**
- `research2/qualification/researchloop_v6_original_run_one_gate_control_v003.py`
- `research2/qualification/researchloop_v6_completion_gate_run1_v003_receipt.json`
- `research2/qualification/researchloop_v6_completion_gate_run2_v003_receipt.json`
- `research2/qualification/rl_v6_original_success_run1_manifest.json`, `...run1_oracle_audit.json`
- `research2/qualification/rl_v6_original_success_run2_manifest.json`, `...run2_oracle_audit.json`
- Full remaining original generated artifacts and v001/v002 failures: `G:\My Drive\Consciousness Formula Research\09_Checkpoints\R2_Q1_RL_V6_COMPLETION_RUNTIME_20261011_v001` (individual Drive sync not independently guaranteed)
- Canonical mutable [result Google Doc 63](https://docs.google.com/document/d/14qSR8YroQ3wSkEOyjf5lV0FjWzRlpC0JNF1hfNg9dMo/edit) and [status v009](https://docs.google.com/document/d/1_K9VwCEKDnm3yAw7zTVwFtcPFWLJ01Ell1rhjsfeRqI/edit).

**Q1 total**: fully certified 19C six rivals 0/6, AES/P14/P15 parity OPEN, prereg21 NOT FROZEN, sealed affect v004 unopened, AES decisive prospective trials ZERO, claim ceiling Level0. Do not use this study as a tournament score.
