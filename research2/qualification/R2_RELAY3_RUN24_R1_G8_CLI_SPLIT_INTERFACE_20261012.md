# Research #2 Relay3 Run24 — original Research1 G8 CLI split exposure (bounded)
Date: 2026-10-12 Asia/Dhaka. NONDECISIVE. No hidden split executed.
Original Research1 commit: 633fc711e34e9bf1be37f5760147a5918276d31a.
Exact original benchmark_v002.py Git blob: 47fc8c9f2d85646ade45b846d49efbd2db8d93c4; SHA256: 894788122336f5f330187bc2d6a00f76e98898f2688f8558e5f1d1ed02fc4ff2.
Exact original frozen_config_v001.json Git blob: 4fe694e7c4a40293fc71f3a0cc22939b8bd9ded4.
Source v002 main() exposes `--split {train,validation,locked_test,ood}` while frozen config says development_cli_splits=[train,validation] and locked_test intentionally not exposed by development CLI/workflow.
Original v002 argparse --help executed with NONORIGINAL neutral core-import shim; no original full core, no world generation, no locked/OOD invocation. Two independent fresh processes each 12/12 PASS, identical receipt SHA256 3ba159ea7416ba6ccc02d83ebbd71240f9165ab8166095d207e8d18f49921ff7, zero stderr. Causal removal mutant detected, benign comment unchanged, invalid split exit2, world-access sentinel zero.
Preexecution protocol frozen SHA256 f64a2685af7f7d848d45acdec74fad9edc848cd9bcfa97160f124de838805431 before test. Runner SHA256 76ed7fb8470a7fdad4d96dc40c17ca3be4f47f6db7a08045df29dd9658a16f15. Local report SHA256 15887fe17a7e3186f0a578d5256098811bc1c5c81831031ba47c5ad4cf60899c.
INTERPRETATION: apparent original CLI/config interface mismatch, NOT proof of actual locked-test leak or policy exposure; possible config applies to narrower development workflow. Knowledgeable independent defender must resolve intended interface, workflow invocation, historical receipts. No frozen source edits, no sealed affect-v004, no paid calls, no AES/rival full agent.
G1–G8 remain BLOCKED; six 19C full certs 0/6; native AES A1–A4 0/4; prereg21 draft; decisive AES-vs-six ZERO; claim Level0.
NEXT: source-native read-only authoritative dev workflow/CLI route audit WITHOUT invoking locked_test/OOD; prioritize full AES/rival 19C fidelity and H011 real usage.
