#!/usr/bin/env bash
# Sync Pi memory files from Mac → VPS k8s ConfigMap
# Run from Mac after every session or on demand
set -euo pipefail

VPS="${VPS:-root@srv1443703.hstgr.cloud}"
MEMORY_FILE="${MEMORY_FILE:-$HOME/code/jpglabs/docs/memory/PI_MEMORY.md}"
AGENTS_FILE="${AGENTS_FILE:-$HOME/code/jpglabs/docs/memory/AGENTS.md}"
KUBECTL="ssh $VPS k3s kubectl"

log() { echo "[$(date '+%H:%M:%S')] $*"; }
ok()  { echo "[$(date '+%H:%M:%S')] ✅ $*"; }

log "Syncing Pi memory to VPS k8s ConfigMap..."

# Build the kubectl patch payload
PI_MEMORY=$(cat "$MEMORY_FILE" | sed 's/\\/\\\\/g' | awk '{printf "%s\\n", $0}')
AGENTS=$(cat "$AGENTS_FILE" | sed 's/\\/\\\\/g' | awk '{printf "%s\\n", $0}')

$KUBECTL create configmap pi-memory \
  --from-file=PI_MEMORY.md="$MEMORY_FILE" \
  --from-file=AGENTS.md="$AGENTS_FILE" \
  --namespace=ai-services \
  --dry-run=client -o yaml | $KUBECTL apply -f -

ok "ConfigMap pi-memory updated"

# Restart pi-local-app to pick up new memory
$KUBECTL rollout restart deployment/pi-local-app -n ai-services
$KUBECTL rollout status deployment/pi-local-app -n ai-services --timeout=30s

ok "pi-local-app restarted with fresh memory"
log "VPS AI API is now context-aware: https://jpglabs.com.br/pi"
