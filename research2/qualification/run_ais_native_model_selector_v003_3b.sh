#!/usr/bin/env bash
set -uo pipefail
mkdir -p research2/qualification/output-ais-native-selector-v003
OUT="$PWD/research2/qualification/output-ais-native-selector-v003"
START="$(date +%s)"
MODEL_URL='https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf'
BIN_URL='https://github.com/ggml-org/llama.cpp/releases/download/b11512/llama-b11512-bin-ubuntu-x64.tar.gz'
EXPECTED_BIN_SHA='cf4083d1e89ccce41157b096d5c9d36e2ef4c8751cf96b709ed533a3a4fe98d3'
MODEL="$RUNNER_TEMP/qwen2.5-3b-instruct-q4_k_m.gguf"
ARCHIVE="$RUNNER_TEMP/llama-b11512-bin-ubuntu-x64.tar.gz"
LOCAL_BIN="$RUNNER_TEMP/llama-b11512"
mkdir -p "$LOCAL_BIN"
uname -a > "$OUT/platform.txt"
( nproc; free -m ) >> "$OUT/platform.txt"
printf 'MODEL=%s\nBINARY=%s\n' "$MODEL_URL" "$BIN_URL" > "$OUT/source_urls.txt"
download() {
  curl -fLsS --max-time 110 --retry 1 "$1" -o "$2"
}
if ! download "$BIN_URL" "$ARCHIVE" 2>"$OUT/bin_download_stderr.txt"; then
  echo 'FAILED runtime binary download' > "$OUT/verdict.txt"
  exit 11
fi
printf '%s  %s\n' "$EXPECTED_BIN_SHA" "$ARCHIVE" | sha256sum -c - > "$OUT/bin_sha256_verification.txt" || {
  echo 'FAILED pinned runtime checksum' > "$OUT/verdict.txt"
  exit 12
}
if ! tar -xzf "$ARCHIVE" -C "$LOCAL_BIN" > "$OUT/tar_stdout.txt" 2>"$OUT/tar_stderr.txt"; then
  echo 'FAILED tar extract' > "$OUT/verdict.txt"
  exit 13
fi
LLAMA="$(find "$LOCAL_BIN" -type f -name llama-cli -print -quit)"
if [ -z "$LLAMA" ]; then
  echo 'BLOCKED original llama-cli not found' > "$OUT/verdict.txt"
  find "$LOCAL_BIN" -maxdepth 3 -type f > "$OUT/extracted_file_inventory.txt"
  exit 14
fi
chmod +x "$LLAMA"
printf '%s\n' "$LLAMA" > "$OUT/llama_cli_path.txt"
if ! download "$MODEL_URL" "$MODEL" 2>"$OUT/model_download_stderr.txt"; then
  echo 'FAILED open-weight model download' > "$OUT/verdict.txt"
  exit 15
fi
sha256sum "$MODEL" > "$OUT/model_sha256.txt"
stat -c '%s' "$MODEL" > "$OUT/model_bytes.txt"
printf '%s  %s\n' '626b4a6678b86442240e33df819e00132d3ba7dddfe1cdc4fbb18e0a9615c62d' "$MODEL" | sha256sum -c - > "$OUT/model_sha256_verification.txt" || { echo "FAIL: model checksum mismatch" > "$OUT/verdict.txt"; exit 18; }
PROMPT="In one concise sentence, explain why a failed scientific hypothesis should be retained in a research memory system."
printf '%s\n' "$PROMPT" > "$OUT/development_prompt.txt"


echo "Original AIS import and model-directed test follows; exact upstream git checkout" > "$OUT/native_path.txt"
AIS="$RUNNER_TEMP/ais-pinned-original"
mkdir -p "$AIS"
git -C "$AIS" init -q
git -C "$AIS" remote add origin https://github.com/SakanaAI/AI-Scientist-v2.git
git -C "$AIS" -c protocol.version=2 fetch --quiet --depth=1 --no-tags origin 96bd51617cfdbb494a9fc283af00fe090edfae48
git -C "$AIS" checkout --quiet --detach FETCH_HEAD
git -C "$AIS" rev-parse HEAD > "$OUT/original_commit.txt"
python3 -m pip install -q --disable-pip-version-check \
  dataclasses-json humanize numpy black rich jsonschema backoff funcy \
  openai anthropic omegaconf > "$OUT/pip_stdout.txt" 2> "$OUT/pip_stderr.txt" || {
    echo 'BLOCKED: original source Python dependencies unavailable' > "$OUT/verdict.txt"
    exit 40
  }
python3 -m pip freeze > "$OUT/pip_freeze.txt"
SERVE="$(find "$LOCAL_BIN" -type f -name llama-server -print -quit)"
if [ -z "$SERVE" ]; then echo 'BLOCKED: llama-server absent' > "$OUT/verdict.txt"; exit 41; fi
chmod +x "$SERVE"
"$SERVE" --model "$MODEL" --host 127.0.0.1 --port 8080 \
  --threads 2 --ctx-size 4096 --parallel 1 --jinja --n-predict 384 \
  > "$OUT/llama_server_stdout.txt" 2> "$OUT/llama_server_stderr.txt" &
SERVER_PID=$!
trap 'kill "$SERVER_PID" 2>/dev/null || true' EXIT
READY=0
for i in $(seq 1 60); do
  if curl -fsS --max-time 2 'http://127.0.0.1:8080/health' -o "$OUT/health.json" 2>/dev/null; then READY=1; break; fi
  if ! kill -0 "$SERVER_PID" 2>/dev/null; then echo 'BLOCKED: llama-server did not start' > "$OUT/verdict.txt"; exit 42; fi
  sleep 1
done
if [ "$READY" -ne 1 ]; then echo 'BLOCKED: health timeout' > "$OUT/verdict.txt"; exit 43; fi
curl -fsS --max-time 10 'http://127.0.0.1:8080/v1/models' -o "$OUT/models.json"
export R2_REAL_MODEL_ID="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["data"][0]["id"])' "$OUT/models.json")"
export R2_AIS_ORIGINAL="$AIS"
export OPENAI_API_KEY='LOCAL_ONLY_NO_EXTERNAL_KEY'
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=0
timeout 150s python3 -B research2/qualification/ais_native_model_selector_v003_3b.py > "$OUT/probe_stdout.txt" 2> "$OUT/probe_stderr.txt"
CODE=$?
echo "$CODE" > "$OUT/probe_exit_code.txt"
if [ "$CODE" -ne 0 ]; then
  echo 'FAIL or BLOCKED: source-native model selection; see full receipt and logs' > "$OUT/verdict.txt"
  cat "$OUT/probe_stdout.txt" | tail -n 18
  exit "$CODE"
fi
echo 'PASS: original source-native model-driven journal selector, NOT full AIS 19C' > "$OUT/verdict.txt"
cat "$OUT/probe_stdout.txt" | tail -n 18
