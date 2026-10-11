# Research #2 — zero-API open-weight CPU inference feasibility (nondecisive, PRE-EXECUTION)

Timestamp: 2026-10-11 Asia/Dhaka. GitHub branch `research2-qualification-cloud-20261011` is isolated from legacy Research-1 code/branch, and the Google Drive Research #2 status remains the mutable scientific canonical record.

**Question**: Can GitHub-hosted 2-vCPU private Actions compute produce a genuine model-originated text response **without user credentials, paid model provider or proprietary API**, using an intact reproducible publicly licensed open-weight model?

**Predeclared materials**:
- Model: `ggml-org/Qwen3.5-0.8B-GGUF` public Apache-2.0, filename `Qwen3.5-0.8B-Q4_0.gguf` (~563MB); source URL https://huggingface.co/ggml-org/Qwen3.5-0.8B-GGUF/resolve/main/Qwen3.5-0.8B-Q4_0.gguf .
- Runtime: official `ggml-org/llama.cpp` Ubuntu x64 CPU release `b11512`, https://github.com/ggml-org/llama.cpp/releases/download/b11512/llama-b11512-bin-ubuntu-x64.tar.gz ; independently published release attestation SHA256 `cf4083d1e89ccce41157b096d5c9d36e2ef4c8751cf96b709ed533a3a4fe98d3`.
- Platform: GitHub Actions `ubuntu-latest`, ordinary CPU runner, CPU threads 2, no GPU, no secrets. Time cap 8 minutes, model generation subprocess cap 120 seconds, total model download cap 120 seconds. No changes to any six pinned competitor repos, AES/P14/P15 contestants, sealed benchmarks, official benchmark metrics or preregistration.

**Predeclared developmental prompt** (not a scientific decisive task): `In one concise sentence, explain why a failed scientific hypothesis should be retained in a research memory system.` Generate max 64 new tokens with temperature zero and deterministic seed 17. Success standard: upstream llama.cpp process exits zero and creates a nonempty textual transcript that is not merely a command echo; save full raw stdout/stderr, CPU/memory, binary and model SHA256, startup and generation elapsed time, license/source paths. If runtime or download is inaccessible, output a transparent BLOCKED or FAIL record.

This is **only a provider-free model availability test**, not a valid original AI Scientist-v2/InternAgent/EvoScientist/ResearchLoop/OmniScientist/EvoMaster autonomous behavior test. A 0.8B Q4 quantized model may be too weak for research agents and must NOT be silently treated as equivalent to a strong external API LLM. Full 19C method behavioral passes remain 0/6 until unbiased matched-input/tool/budget model-quality, original source autonomy and independent knowledgeable defender requirements pass. AES v2 decisive head-to-head trials 0, preregistration21 not frozen. Private GitHub Actions consumption is restricted by a hard timeout; beyond included minutes may be billable, so no paid upgrade or model API consumption authorized.

Running this public-key-free test can produce evidence for a possible *development* provider route. Stronger free-tier cloud inference with metered model ID/usage is a separate route and would require a user-provisioned authorized secret scoped to the isolated Research #2 branch.
