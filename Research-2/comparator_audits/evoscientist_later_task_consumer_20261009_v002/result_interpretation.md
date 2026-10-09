# Research #2 — EvoScientist ES-3/4/5 later-task tool-consumer sentinel v002
Date 2026-10-09, Asia/Dhaka. NONDECISIVE DEVELOPER-ONLY EVIDENCE; not an AES v2 trial.

## Pre-execution contract
See pre_execution_protocol.md, SHA256 87C76572BD6F0E49F145A105674ADE6464DF9A8E18A6EB0A496626BC1AE5192B.
Original repository EvoScientist/EvoScientist commit 3b382b92b8fdad6e1f13467c382dcdd91d9b19d2, same pinned official source as 17ZB.
Python interpreter: C:\Users\hasad\Research2\venvs\evosci312\Scripts\python.exe.
Test outside upstream repository: test_later_task_consumer.py, SHA256 FBCD0EAFBBA452971D2235AA0E7220731707A5BE0968922BBB483B291A320C5D.

## Results
Two fresh independent pytest processes; no provider API calls or direct source changes.
Run001: pytest exit 0, 1 PASS, internal 4.13s.
Run002: pytest exit 0, 1 PASS, internal 2.86s.
Upstream checkout was clean after both processes.
Raw run001 stdout SHA256 DA28BDB1DF95F6EA22322568CF055E023F8F36B54C6903026E0DC27A42D358D7.
Raw run002 stdout SHA256 116C3C3230EB9D56B5F45C7F4D1BE96D3D344C08FBCF5AA14E86C9B15B2FD1ED.

| Condition | Source-native search hits | Source-native read calls | Deterministic downstream choice |
|---|---:|---:|---|
| A project-specific failure recorded, memory ON | 1 | 1 | CALIBRATE_FIRST |
| B no memory (same source tool called) | 0 | 0 | DIRECT_MEASUREMENT |
| C different negative memory recorded | 0 | 0 | DIRECT_MEASUREMENT |
| D relevant memory in different project | 0 | 0 | DIRECT_MEASUREMENT |
| E relevant memory found, read withheld | 1 | 0 | DIRECT_MEASUREMENT |

## Epistemic result and limitations
This is an authored source-native search_observations -> read_memory tool round-trip:
the official search tool returned the observation ID; the official read tool supplied full text;
a predeclared OUTSIDE-system deterministic consumer selected action based only on that read output.
The memory storage and retrieval path does drive a hypothetical later action under these narrow
controlled conditions. The test does NOT demonstrate an EvoScientist autonomous researcher choosing
to call the tool, interpreting source quality, making scientific decisions, or achieving better task outcomes.
This is a scripted consumption oracle, NOT ES-1/2 end-to-end or genuine downstream autonomous policy validation.
Regex 'calibration' query is intentionally narrow; no ranked-recall robustness is established.
No knowledgeable independent rival-method defender reviewed it. No matched policy/tool token, time
or external provider comparisons were performed. Only behavior of this isolated official tooling
and external script was measured. Two fresh runs do not equal independent conceptual replication.

## Fidelity adjudication (19C/19G)
ES-1 researcher/engineer roles: NOT TESTED HERE.
ES-2 evolution/memory stores from completed genuine interactions: PARTIAL, observations recorded by official function
  but not an authentic completed agent lifecycle.
ES-3 failed directions eligible: PARTIAL SUPPORT, synthetic negative direction persisted using official source.
ES-4 later task/cycle can retrieve memory: PARTIAL SUPPORT at actual source-tool I/O, not autonomous reasoning.
ES-5 clean-start / memory ON separable: PARTIAL SUPPORT at isolated negative controls, not end-to-end mode.
Full EvoScientist source fidelity: BLOCKED/UNCERTIFIED. All six rivals remain eligible.
AES v2 prospective decisive trial count: ZERO. No AES advantage, tie, or inferiority inferred.

## Adversarial reading
Support: original official source tools function, optional exact read matters, project isolation observed,
irrelevant memory does not trigger selected keyword-conditioned scripted behavior.
Attack: the external consumer decision rule was hand-authored to respond to an exact string;
the true model may not call read_memory, may select another action, or may be overwhelmed by context.
The narrow regex search does not measure memory generalization, calibration improvement or transfer.

## Next executable science action
1. Build actual EvoScientist researcher/model-consumer test under a permitted base model with call log
   and masked equivalently budgeted ON/OFF/irrelevant controls, or source-native scripted fake
   model graph stepping if authorized access cannot be achieved; preserve distinction.
2. Independently inspect ES-1..ES-5 full source lifecycle and have knowledgeable defender attack fidelity.
3. Preserve first-provider model IDs, token counts, retries and cost if/when provider access is authorized;
   keep Gemini unused here under user's low-call preference.
4. Complete six-rival 19C/19G/19H and preregistration before sealed AES v2 decisive runs.
