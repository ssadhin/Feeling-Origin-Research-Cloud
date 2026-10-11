#!/usr/bin/env bash
set -uo pipefail
mkdir -p research2/qualification/output-local-model-v002
OUT="$PWD/research2/qualification/output-local-model-v002"
START="$(date +%s)"
MODEL_URL='https://huggingface.co/ggml-org/Qwen3.5-0.8B-GGUF/resolve/main/Qwen3.5-0.8B-Q4_0.gguf'
BIN_URL='https://github.com/ggml-org/llama.cpp/releases/download/b11512/llama-b11512-bin-ubuntu-x64.tar.gz'
EXPECTED_BIN_SHA='cf4083d1e89ccce41157b096d5c9d36e2ef4c8751cf96b709ed533a3a4fe98d3'
MODEL="$RUNNER_TEMP/Qwen3.5-0.8B-Q4_0.gguf"
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
PROMPT="In one concise sentence, explain why a failed scientific hypothesis should be retained in a research memory system."
printf '%s\n' "$PROMPT" > "$OUT/development_prompt.txt"
RUN_START="$(date +%s)"
timeout 120s "$LLAMA" --model "$MODEL" --threads 2 --ctx-size 1024 --predict 512 --temp 0 --seed 17 --no-display-prompt --prompt "$PROMPT" > "$OUT/model_stdout.txt" 2> "$OUT/model_stderr.txt"
EXIT_CODE=$?
RUN_END="$(date +%s)"
printf '%s\n' "$EXIT_CODE" > "$OUT/inference_exit_code.txt"
printf '%s\n' "$((RUN_END - RUN_START))" > "$OUT/inference_wall_seconds.txt"
printf '%s\n' "$((RUN_END - START))" > "$OUT/total_wall_seconds.txt"
if [ "$EXIT_CODE" -ne 0 ]; then
  echo 'FAIL actual model generation did not exit zero' > "$OUT/verdict.txt"
  exit 16
fi
python3 - "$OUT/model_stdout.txt" "$OUT/verdict.txt" <<'PY'
import pathlib, re, sys
s = pathlib.Path(sys.argv[1]).read_text(errors='replace')
answer_file = pathlib.Path(sys.argv[2])
m = re.search(r'\\[End thinking\\]|</think>|\\[End of thinking\\]', s, flags=re.I)
if m:
    remaining = s[m.end():]
    remaining = remaining.split('[ Prompt:')[0].strip()
else:
    remaining = ''
if len(remaining) < 20:
    answer_file.write_text('BLOCKED: source model produced no verified substantive final answer after thinking marker\\n')
    print('NO_VERIFIED_FINAL_ANSWER')
    print('TRANSCRIPT_TAIL', repr(s[-850:]))
    raise SystemExit(19)
answer_file.write_text('PASS: genuine CPU model produced a verified final-answer span after thinking marker\\n')
print('FINAL_ANSWER_SPAN',repr(remaining[:400]))
PY
CHECK_CODE=$?
if [ "$CHECK_CODE" -ne 0 ]; then
  exit 19
fi
echo 'Research2 nondecisive: provider-free CPU inference, model Qwen3.5-0.8B-Q4_0, NO full 19C behavior or AES decisive trial.' >> "$OUT/verdict.txt"
echo '== SUMMARY ==' && cat "$OUT/verdict.txt" && tail -c 1200 "$OUT/model_stdout.txt" && echo
