#!/usr/bin/env bash
set -uo pipefail
mkdir -p research2/qualification/output-local-server-v004
OUT="$PWD/research2/qualification/output-local-server-v004"
START="$(date +%s)"
MODEL_URL='https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf'
BIN_URL='https://github.com/ggml-org/llama.cpp/releases/download/b11512/llama-b11512-bin-ubuntu-x64.tar.gz'
EXPECTED_BIN_SHA='cf4083d1e89ccce41157b096d5c9d36e2ef4c8751cf96b709ed533a3a4fe98d3'
MODEL="$RUNNER_TEMP/qwen2.5-1.5b-instruct-q4_k_m.gguf"
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
printf '%s  %s\n' '6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e' "$MODEL" | sha256sum -c - > "$OUT/model_sha256_verification.txt" || { echo "FAIL: model checksum mismatch" > "$OUT/verdict.txt"; exit 18; }
PROMPT="In one concise sentence, explain why a failed scientific hypothesis should be retained in a research memory system."
printf '%s\n' "$PROMPT" > "$OUT/development_prompt.txt"

SERVE="$(find "$LOCAL_BIN" -type f -name llama-server -print -quit)"
if [ -z "$SERVE" ]; then
  echo 'BLOCKED: original llama-server absent from verified runtime archive' > "$OUT/verdict.txt"
  exit 30
fi
chmod +x "$SERVE"
"$SERVE" --model "$MODEL" --host 127.0.0.1 --port 8080 --threads 2 --ctx-size 1024 --parallel 1 > "$OUT/server_stdout.txt" 2> "$OUT/server_stderr.txt" &
SERVER_PID=$!
echo "$SERVER_PID" > "$OUT/llama_server_pid.txt"
trap 'kill "$SERVER_PID" 2>/dev/null || true' EXIT
READY=0
for attempt in $(seq 1 60); do
  if curl -fsS --max-time 2 "http://127.0.0.1:8080/health" -o "$OUT/health.json" 2> /dev/null; then
    READY=1
    break
  fi
  if ! kill -0 "$SERVER_PID" 2>/dev/null; then
    echo 'BLOCKED: original llama-server exited before health readiness' > "$OUT/verdict.txt"
    exit 31
  fi
  sleep 1
done
if [ "$READY" -ne 1 ]; then
  echo 'BLOCKED: local server unavailable after 60 seconds' > "$OUT/verdict.txt"
  exit 32
fi
curl -fsS --max-time 10 'http://127.0.0.1:8080/v1/models' -o "$OUT/models.json" || {
  echo 'BLOCKED: OpenAI-compatible models endpoint did not return' > "$OUT/verdict.txt"
  exit 33
}
python3 - "$OUT/models.json" "$OUT/development_prompt.txt" "$OUT/api_request.json" <<'PY'
import json, pathlib, sys
models=json.loads(pathlib.Path(sys.argv[1]).read_text())
data=models.get("data", [])
assert data and data[0].get("id"), "No stable local model identifier in /v1/models"
request={"model":data[0]["id"],"messages":[{"role":"user","content":pathlib.Path(sys.argv[2]).read_text().strip()}],"max_tokens":100,"temperature":0,"stream":False}
pathlib.Path(sys.argv[3]).write_text(json.dumps(request,sort_keys=True)+"\n")
print("ACTUAL_MODEL_ID",data[0]["id"])
PY
QUERY_START="$(date +%s)"
curl -fsS --max-time 110 -H 'Content-Type: application/json' \
  -X POST 'http://127.0.0.1:8080/v1/chat/completions' \
  --data-binary @"$OUT/api_request.json" \
  -w '%{http_code} %{time_total}\n' \
  -o "$OUT/chat_completion.json" > "$OUT/http_status_timing.txt" 2> "$OUT/curl_stderr.txt" || {
    echo 'FAIL: localhost completion request failed' > "$OUT/verdict.txt"
    exit 34
  }
printf '%s\n' "$(( $(date +%s) - QUERY_START ))" > "$OUT/request_wall_seconds.txt"
python3 - "$OUT/chat_completion.json" "$OUT/models.json" "$OUT/verdict.txt" <<'PY'
import json,pathlib,re,sys
reply=json.loads(pathlib.Path(sys.argv[1]).read_text())
models=json.loads(pathlib.Path(sys.argv[2]).read_text())
expected=models["data"][0]["id"]
content=reply["choices"][0]["message"]["content"]
usage=reply.get("usage",{})
ident=reply.get("model")
assert isinstance(content,str) and len(content.strip())>20, "No user-facing assistant response"
assert re.search(r"hypoth|fail|learn|eviden|future",content,re.I), "Non-topical response"
assert isinstance(ident,str) and ident, "Missing model ID in inference reply"
assert int(usage.get("prompt_tokens",0))>0, "Missing provider-side prompt-token receipt"
assert int(usage.get("completion_tokens",0))>0, "Missing provider-side completion-token receipt"
pathlib.Path(sys.argv[3]).write_text("PASS: genuine OpenAI-compatible localhost completion, positive prompt/completion token metering and returned model ID\nModel from /v1/models: "+str(expected)+"\nReturned model: "+str(ident)+"\n")
print("VERIFIED_FINAL_ANSWER",repr(content[:350]))
print("VERIFIED_PROVIDER_USAGE",json.dumps(usage,sort_keys=True))
print("VERIFIED_RETURNED_MODEL",ident)
PY
CODE=$?
if [ "$CODE" -ne 0 ]; then
  echo "FAIL: real localhost API receipt response validation" > "$OUT/verdict.txt"
  exit "$CODE"
fi
date -u +%FT%TZ > "$OUT/completed_at_utc.txt"
cat "$OUT/verdict.txt"
