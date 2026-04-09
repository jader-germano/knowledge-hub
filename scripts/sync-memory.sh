#!/usr/bin/env bash
# Sync local memory center → VPS (rsync + optional k8s ConfigMap)
# Run from Mac after every session or on demand
set -euo pipefail

MEMORY_ROOT="${MEMORY_ROOT:-$HOME/code/jpglabs/docs/memory}"
VPS_HOST="${VPS_HOST:-root@187.77.227.151}"
VPS_MEMORY_DIR="/root/memory"
KUBECTL="ssh $VPS_HOST k3s kubectl"

log() { echo "[$(date '+%H:%M:%S')] $*"; }
ok()  { echo "[$(date '+%H:%M:%S')] ✅ $*"; }
err() { echo "[$(date '+%H:%M:%S')] ❌ $*" >&2; }

# --- 1. Verify local memory exists ---
if [[ ! -f "$MEMORY_ROOT/PI_MEMORY.md" ]]; then
  err "PI_MEMORY.md not found at $MEMORY_ROOT"
  exit 1
fi

# --- 2. Verify VPS connectivity ---
log "Testing VPS SSH..."
if ! ssh -o ConnectTimeout=5 "$VPS_HOST" "echo OK" >/dev/null 2>&1; then
  err "VPS SSH unreachable at $VPS_HOST"
  exit 1
fi
ok "VPS SSH reachable"

# --- 3. Rsync core memory files to VPS ---
log "Syncing memory files to VPS $VPS_MEMORY_DIR..."
ssh "$VPS_HOST" "mkdir -p $VPS_MEMORY_DIR/sessions $VPS_MEMORY_DIR/logs"

rsync -avz --delete \
  "$MEMORY_ROOT/PI_MEMORY.md" \
  "$MEMORY_ROOT/AGENTS.md" \
  "$MEMORY_ROOT/MEMORY_SYNC.md" \
  "$VPS_HOST:$VPS_MEMORY_DIR/"

ok "Core memory files synced"

# --- 4. Sync session logs (latest 10 per agent) ---
log "Syncing recent session logs..."
for agent_dir in "$MEMORY_ROOT/sessions"/*/; do
  agent=$(basename "$agent_dir")
  ssh "$VPS_HOST" "mkdir -p $VPS_MEMORY_DIR/sessions/$agent"
  # sync only the 10 most recent session files
  recent=$(ls -t "$agent_dir"*.md 2>/dev/null | head -10 || true)
  if [[ -n "$recent" ]]; then
    rsync -avz $recent "$VPS_HOST:$VPS_MEMORY_DIR/sessions/$agent/"
  else
    log "  $agent: no session files to sync"
  fi
done
ok "Session logs synced"

# --- 5. Optional: k8s ConfigMap in automation namespace ---
if ssh "$VPS_HOST" "k3s kubectl get ns automation" >/dev/null 2>&1; then
  log "Updating k8s ConfigMap pi-memory in automation namespace..."
  $KUBECTL create configmap pi-memory \
    --from-file=PI_MEMORY.md="$VPS_MEMORY_DIR/PI_MEMORY.md" \
    --from-file=AGENTS.md="$VPS_MEMORY_DIR/AGENTS.md" \
    --namespace=automation \
    --dry-run=client -o yaml | $KUBECTL apply -f -
  ok "ConfigMap pi-memory updated in automation namespace"
else
  log "Skipping k8s ConfigMap (automation namespace not found)"
fi

# --- 6. Summary ---
VPS_FILES=$(ssh "$VPS_HOST" "ls -la $VPS_MEMORY_DIR/*.md 2>/dev/null | wc -l")
VPS_SESSIONS=$(ssh "$VPS_HOST" "find $VPS_MEMORY_DIR/sessions -name '*.md' 2>/dev/null | wc -l")
ok "Sync complete — $VPS_FILES core files, $VPS_SESSIONS session logs on VPS"
