#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="${1:-n8n}"
WORKFLOW_DIR="${2:-$(cd "$(dirname "$0")/../n8n-workflows" && pwd)}"

if ! command -v docker >/dev/null 2>&1; then
  echo "docker is required but not installed."
  exit 1
fi

if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo "n8n container '${CONTAINER_NAME}' is not running."
  echo "Usage: $0 <container_name> [workflow_dir]"
  exit 1
fi

echo "Importing workflows from: ${WORKFLOW_DIR}"
echo "Target container: ${CONTAINER_NAME}"

declare -a DEFAULT_WORKFLOWS=(
  "ai-guardian-cleanup.json"
  "ai-lead-hunter.json"
  "ai-toolkit-delivery.json"
  "infrastructure-monitor.json"
  "kiwify-delivery-secure.json"
  "social-sales-hub.json"
  "whatsapp-bot.json"
)

if [[ "${N8N_IMPORT_ALL:-0}" == "1" ]]; then
  shopt -s nullglob
  WORKFLOWS=( "${WORKFLOW_DIR}"/*.json )
else
  WORKFLOWS=()
  for file in "${DEFAULT_WORKFLOWS[@]}"; do
    if [[ -f "${WORKFLOW_DIR}/${file}" ]]; then
      WORKFLOWS+=( "${WORKFLOW_DIR}/${file}" )
    fi
  done
fi

for wf in "${WORKFLOWS[@]}"; do
  name="$(basename "${wf}")"
  target="/tmp/${name}"
  echo "-> ${name}"
  docker cp "${wf}" "${CONTAINER_NAME}:${target}"
  docker exec "${CONTAINER_NAME}" n8n import:workflow --input="${target}"
done

echo "Done. Imported ${#WORKFLOWS[@]} workflow file(s)."
