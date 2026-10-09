# Research #2 nondecisive EvoScientist later-task consumer — PRE-EXECUTION
Date 2026-10-09, Asia/Dhaka. This is a new development test, NOT a sealed AES tournament trial.
Source: upstream EvoScientist/EvoScientist git commit 3b382b92b8fdad6e1f13467c382dcdd91d9b19d2.
Environment: Home PC C:\Users\hasad\Research2\venvs\evosci312\Scripts\python.exe; source remains clean.
Predecessor: 17ZB source-native memory context test (2/2 independent fresh runs).

Question: does author-original search_observations -> read_memory expose a failed-direction observation to a
later deterministic external consumer strongly enough to alter a predeclared action? Distinguish
memory availability from downstream model cognition or actual EvoScientist scientific improvement.

Design: new independent temp dirs each trial; same source-native tool classes and invocation shapes.
A (relevant ON): official record_observation_file stores failure of calibration; later consumer issues
search_observations('calibration ...') and read_memory(exact returned id).
B (memory OFF): identical downstream tools and query against a clean, memory-empty directory;
expected search 0, no read, action DIRECT_MEASUREMENT (fails to use prior failure).
C (irrelevant ON): official record_observation_file stores unrelated habitat mapping negative memory;
same downstream search/query; expected no matching relevant observation, action DIRECT_MEASUREMENT.
D (cross-project): relevant A observation exists but search context is unrelated project;
expected no matching observation, action DIRECT_MEASUREMENT.
E (relevant ON but read denied): tool results available but no read_memory output passed to consumer;
expected DIRECT_MEASUREMENT; negative control for decision depending on full read.
No model API/LLM, no stochastic seeds, no sealed trials, no source edits.

Frozen deterministic external decision policy: choose CALIBRATE_FIRST only when the text from
a successfully invoked official read_memory contains 'calibration strategy produced irreproducible'
and 'check calibration' (case-insensitive). Otherwise choose DIRECT_MEASUREMENT.
No source file reads inside chooser; actions are synthetic labels, not actual research experiments.
Read tool must only be called after a source-native search result yields its exact ID.

Predeclared pass: A has search hit + read hit + CALIBRATE_FIRST; B/C/D/E DIRECT_MEASUREMENT,
B/C/D have zero matching hits. Predeclared fail: any role leakage, A not action-changed,
negative-memory creates spurious match, changed source repository, execution/runtime error.
Two clean fresh independent OS Python test processes; preserve stdout files and exit codes.
For C, irrelevant observation should include an actual *negative outcome* but no calibration terms.
Metadata record run timestamp, source hash, raw output hashes, no secret access.

Claim ceiling even after pass: source-native retrieval/tool IO can drive a deliberately
memory-conditioned external deterministic decision rule. NOT evidence of autonomous
EvoScientist researcher model invoking tools, ES-1/ES-2 completed lifecycle, or material
research outcome improvement. Full six-rival fidelity still BLOCKED. Independent reviewer OPEN.
Any postrun modifications create a separately versioned test and new preprotocol.
