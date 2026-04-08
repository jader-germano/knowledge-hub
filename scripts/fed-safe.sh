#!/bin/zsh

# Safe local wrapper for FrankMD without changing the upstream project.
#
# Usage:
#   zsh /Users/philipegermano/code/jpglabs/docs/scripts/fed-safe.sh
#   zsh /Users/philipegermano/code/jpglabs/docs/scripts/fed-safe.sh /Users/philipegermano/code/jpglabs/docs

set -euo pipefail

FRANKMD_FED_SCRIPT="/Users/philipegermano/code/FrankMD/config/fed/fed.sh"
DEFAULT_TARGET="/Users/philipegermano/code/jpglabs/docs"
TARGET_INPUT="${1:-$DEFAULT_TARGET}"

if [[ ! -f "$FRANKMD_FED_SCRIPT" ]]; then
  echo "[fed-safe] Error: FrankMD launcher not found at $FRANKMD_FED_SCRIPT" >&2
  exit 1
fi

if ! TARGET="$(realpath "$TARGET_INPUT" 2>/dev/null)"; then
  echo "[fed-safe] Error: invalid path: $TARGET_INPUT" >&2
  exit 1
fi

if [[ ! -d "$TARGET" ]]; then
  echo "[fed-safe] Error: directory not found: $TARGET" >&2
  exit 1
fi

case "$TARGET" in
  /Users/philipegermano/code/*) ;;
  *)
    echo "[fed-safe] Error: path must stay under /Users/philipegermano/code" >&2
    exit 1
    ;;
esac

source "$FRANKMD_FED_SCRIPT"

_fed_local_cleanup() {
  docker stop frankmd >/dev/null 2>&1 || true
  docker rm frankmd >/dev/null 2>&1 || true
}

_fed_restore_var() {
  local name="$1"
  local marker="$2"
  local value="$3"

  if [[ "$marker" == "set" ]]; then
    export "$name=$value"
  else
    unset "$name"
  fi
}

SENSITIVE_VARS=(
  FRANKMD_ENV
  AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_S3_BUCKET AWS_REGION
  YOUTUBE_API_KEY
  GOOGLE_API_KEY GOOGLE_CSE_ID
  AI_PROVIDER AI_MODEL
  OLLAMA_API_BASE OLLAMA_MODEL
  OPENROUTER_API_KEY OPENROUTER_MODEL
  ANTHROPIC_API_KEY ANTHROPIC_MODEL
  GEMINI_API_KEY GEMINI_MODEL
  OPENAI_API_KEY OPENAI_MODEL
  IMAGE_GENERATION_MODEL
)

typeset -a PREVIOUS_MARKERS
typeset -a PREVIOUS_VALUES

for var in "${SENSITIVE_VARS[@]}"; do
  if [[ -n "${(P)var+x}" ]]; then
    PREVIOUS_MARKERS+=("set")
    PREVIOUS_VALUES+=("${(P)var}")
  else
    PREVIOUS_MARKERS+=("unset")
    PREVIOUS_VALUES+=("")
  fi
  unset "$var"
done

_fed_local_cleanup
fed "$TARGET"
FED_STATUS=$?

INDEX=1
for var in "${SENSITIVE_VARS[@]}"; do
  _fed_restore_var "$var" "${PREVIOUS_MARKERS[$INDEX]}" "${PREVIOUS_VALUES[$INDEX]}"
  ((INDEX++))
done

exit "$FED_STATUS"
