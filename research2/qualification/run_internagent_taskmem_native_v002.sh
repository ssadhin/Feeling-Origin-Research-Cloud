#!/usr/bin/env bash
set -uo pipefail
OUT="$PWD/research2/qualification/output-internagent-taskmem-v002"
mkdir -p "$OUT"
PIN='fa8c3eedfa9751d3752ea6eb49220b303ac2397d'
AIS='https://github.com/InternScience/InternAgent.git'
ROOT="$RUNNER_TEMP/internagent-native"
mkdir -p "$ROOT"
git -C "$ROOT" init -q
git -C "$ROOT" remote add origin "$AIS"
if ! git -C "$ROOT" -c protocol.version=2 fetch --quiet --depth=1 --no-tags origin "$PIN" 2> "$OUT/git_stderr.txt"; then
  echo 'BLOCKED: original InternAgent git source not fetchable' > "$OUT/verdict.txt"
  exit 31
fi
git -C "$ROOT" checkout --quiet --detach FETCH_HEAD
git -C "$ROOT" rev-parse HEAD > "$OUT/original_commit.txt"
export R2_INTERNAGENT_ORIGINAL="$ROOT"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=0
export OMP_NUM_THREADS=2
export TOKENIZERS_PARALLELISM=false
export HF_HOME="$RUNNER_TEMP/r2_hf_home"
export HF_HUB_DISABLE_TELEMETRY=1
echo '2 CPU: original real embeddings+FAISS/BM25 memory; no paid provider' > "$OUT/execution_scope.txt"
if ! python3 -m pip install --disable-pip-version-check -q --index-url https://download.pytorch.org/whl/cpu torch > "$OUT/torch_pip_stdout.txt" 2> "$OUT/torch_pip_stderr.txt"; then
  echo 'BLOCKED: CPU PyTorch native embedding dependency unavailable' > "$OUT/verdict.txt"
  exit 32
fi
if ! python3 -m pip install --disable-pip-version-check -q sentence-transformers faiss-cpu rank-bm25 json-repair openai rich numpy scipy pyyaml > "$OUT/requirements_stdout.txt" 2> "$OUT/requirements_stderr.txt"; then
  echo 'BLOCKED: original native memory dependencies unavailable' > "$OUT/verdict.txt"
  exit 33
fi
python3 -m pip freeze > "$OUT/python_dependency_lock_observed.txt"
timeout 190s python3 -B research2/qualification/internagent_taskmem_native_v002.py > "$OUT/test_stdout.txt" 2> "$OUT/test_stderr.txt"
CODE=$?
echo "$CODE" > "$OUT/exit_code.txt"
if [ "$CODE" -ne 0 ]; then
  echo 'FAIL/BLOCKED: source-native original memory behavior; see exact receipts' > "$OUT/verdict.txt"
  tail -n 16 "$OUT/test_stdout.txt" || true
  tail -n 18 "$OUT/test_stderr.txt" || true
  exit "$CODE"
fi
echo 'PASS: original InternAgent signed task-memory retrieval and persistence (NOT full 19C)' > "$OUT/verdict.txt"
tail -n 15 "$OUT/test_stdout.txt"
