# EvoScientist ES-1 original-source role distinction / wiring — RESULT v001
Date: 2026-10-09 Asia/Dhaka | Research #2 | NONDECISIVE development audit.

RESULT: Two fresh independent Python 3.12 processes exited 0. The unchanged EvoScientist loader identified 7 source roles including research-agent and code-agent. The official source loaded distinct prompts and declared tools (research: tavily_search + think_tool; code: think_tool). Both _build_base_kwargs and load_mcp_and_build_kwargs ASTs called load_subagents and returned subagents: subs. All three staged negative mutants were detected: omitted code role, duplicate prompts, and collapsed research tools. No model calls.

REPRODUCIBILITY: Official pinned commit 3b382b92b8fdad6e1f13467c382dcdd91d9b19d2, git clean after runs. Frozen protocol SHA256 BB18C64435454A4569D95DCD0C186BD3C7FD3D4E6941C20464FB63A3D1BC9C47. Runner SHA256 3A1AFA0D2D5AC1C5450D7F0D43A3982CC29DF4AAFAC72B45C63245247806BA58. Run001 and Run002 raw stdout each SHA256 56B5A28754AD249F829BAC089F2D909DB8D245A7736BA9552797655A7EF0D9E3. Original code hashes in the stdout. Temp-mutated copies only; upstream untouched.

SURVIVAL LOOP: Native role distinction is executable via source loader. Both assembler paths visibly include the loaded subagents. A missing or collapsed role fails these targeted gates.

DESTRUCTION LOOP: NOT a real researcher-to-engineer handoff test; AST wiring is structural, not delegation proof. Original _build_base_kwargs conditionally adds tavily_search only when TAVILY_API_KEY is configured; declared capability need not be available at runtime. These targeted mutants do not exhaust source-fidelity threats. A knowledgeable independent defender should audit actual tools, roles, handoff, resource use and memory in complete work.

ADJUDICATION: ES-1 structural/configuration PARTIAL PASS; full behavioral ES-1 NOT CERTIFIED. ES-2/3/4/5 still partial from previous source tests. Six strong external rivals remain eligible and none is fully certified. AES v2 decisive prospective trial count zero; no superior/inferior/equivalent comparison.

SEPARATE MODEL TEST FAILURE: ES-3/4/5 model-consumer v001 froze before execution, constructed official EvoScientist ChatGoogleGenerativeAI with in-memory key, and made one metered request. Provider raised GoogleModelNotFoundError for gemini-2.5-flash-lite; protocol stopped without retries, verdict BLOCKED_PROVIDER. Account-specific catalog follow-up was blocked by tool safety and was not circumvented. No subsequent network request in this loop.

NEXT EXECUTABLE: independent knowledgeable ES-1 handoff audit or real EvoScientist agent/model source-native tool-call test using an approved available model with metered matched memory ON/OFF/irrelevant controls, after provider access is established. Frozen tournament and 19C/19G/19H gates unchanged.
