#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   VPS_HOST=187.77.227.151 VPS_USER=root ./scripts/deploy-n8n-vps.sh
#
# Optional env vars:
#   SSH_KEY=/Users/jaderphilipe/.ssh/id_ed25519
#   N8N_CONTAINER=n8n
#   REMOTE_WORKFLOW_DIR=/docker/n8n/workflows

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WORKFLOW_DIR="${ROOT_DIR}/n8n-workflows"
VPS_HOST="${VPS_HOST:-}"
VPS_USER="${VPS_USER:-}"
SSH_KEY="${SSH_KEY:-$HOME/.ssh/id_ed25519}"
N8N_CONTAINER="${N8N_CONTAINER:-n8n}"
REMOTE_WORKFLOW_DIR="${REMOTE_WORKFLOW_DIR:-/docker/n8n/workflows}"

if [[ -z "${VPS_HOST}" || -z "${VPS_USER}" ]]; then
  echo "VPS_HOST and VPS_USER are required."
  exit 1
fi

FILES=(
  "ai-guardian-cleanup.json"
  "ai-lead-hunter.json"
  "ai-toolkit-delivery.json"
  "infrastructure-monitor.json"
  "kiwify-delivery-secure.json"
  "social-sales-hub.json"
  "whatsapp-bot.json"
)

SSH_OPTS=(-i "${SSH_KEY}" -o StrictHostKeyChecking=accept-new)

echo "Creating remote workflow directory..."
ssh "${SSH_OPTS[@]}" "${VPS_USER}@${VPS_HOST}" "mkdir -p '${REMOTE_WORKFLOW_DIR}'"

echo "Uploading workflows..."
for f in "${FILES[@]}"; do
  scp "${SSH_OPTS[@]}" "${WORKFLOW_DIR}/${f}" "${VPS_USER}@${VPS_HOST}:${REMOTE_WORKFLOW_DIR}/${f}"
done

echo "Importing workflows on VPS container '${N8N_CONTAINER}'..."
ssh "${SSH_OPTS[@]}" "${VPS_USER}@${VPS_HOST}" "bash -s" <<EOF
set -euo pipefail
for f in ${FILES[*]}; do
  docker cp "${REMOTE_WORKFLOW_DIR}/\${f}" "${N8N_CONTAINER}:/tmp/\${f}"
  docker exec "${N8N_CONTAINER}" n8n import:workflow --input="/tmp/\${f}"
done
echo "n8n workflow deploy complete."
EOF

echo "Done."
