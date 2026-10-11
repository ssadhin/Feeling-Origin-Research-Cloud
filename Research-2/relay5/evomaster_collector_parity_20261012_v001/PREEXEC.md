Research #2 Relay5 PREEXEC 2026-10-12 v001. NONDECISIVE.
Predecessor status v020. Distinct from Relay1 IA5.
Original: sjtu-sai-agents/EvoMaster commit 36a52bc6c42a6b9fd710a41c52f3c3bb948b9ac9.
Collector blob 8dc739e0db3256d51ded0c12d534b752c1af465f.
Core exp blob 14896073e25d9c546e11606adc19c6f45f268f14.
Agent writer blob 696984729eda88eaac900db26ae7d1152f6f430b.
Hypothesis: native trace collector undercounts work in original multi-step core/exp trajectory compared with agent per-step trajectories.
Fixture A one entry with 3 steps each 1 tool call; fixture B three entries each 1 step; C single step; D empty; E second-step error; F count-all-steps mutation.
Predictions: A llm_call_count 1 tool_call_count 1; B 3/3; C 1/1; D 0/0; E second-step error missed; F 3/3.
Verify source-exact function body identity before execution. No provider calls or sealed tasks.
Any discrepancy is bounded accounting behavior, not whole-method failure. No 19C certificate, no decisive trial. Preserve raw evidence and negative controls.
Handoff: independent defender checks whether both trajectory formats reach evolution manager, then full native collector if unowned.