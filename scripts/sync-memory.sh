#!/usr/bin/env bash
# Sync canonical memory/bootstrap/provider shims from Mac -> VPS taxonomy roots.
# This replaces the legacy ai-services/pi-local-app ConfigMap flow.
set -euo pipefail

VPS="${VPS:-jpglabs-vps-tailnet}"
LOCAL_CODE_ROOT="${LOCAL_CODE_ROOT:-$HOME/code}"
LOCAL_MEMORY_ROOT="${LOCAL_MEMORY_ROOT:-$LOCAL_CODE_ROOT/jpglabs/docs/memory}"

REMOTE_CANONICAL_ROOT="${REMOTE_CANONICAL_ROOT:-/root/memory}"
REMOTE_LEGACY_MEMORY_ROOT="${REMOTE_LEGACY_MEMORY_ROOT:-/root/code/jpglabs/docs/memory}"
REMOTE_VAULT_MEMORY_ROOT="${REMOTE_VAULT_MEMORY_ROOT:-/root/obsidian-vault/memory}"

log() { echo "[$(date '+%H:%M:%S')] $*"; }
ok()  { echo "[$(date '+%H:%M:%S')] ✅ $*"; }
fail() { echo "[$(date '+%H:%M:%S')] ❌ $*" >&2; exit 1; }

require_file() {
  local path="$1"
  [ -f "$path" ] || fail "missing required file: $path"
}

remote_write_file() {
  local source="$1"
  local target="$2"
  ssh "$VPS" "mkdir -p \"$(dirname "$target")\""
  cat "$source" | ssh "$VPS" "cat > \"$target\""
}

sync_file() {
  local source="$1"
  local target="$2"
  require_file "$source"
  remote_write_file "$source" "$target"
  ok "$(basename "$source") -> $target"
}

log "Syncing memory and taxonomy shims to VPS canonical roots..."

sync_file "$LOCAL_CODE_ROOT/README.md" \
  "$REMOTE_CANONICAL_ROOT/bootstrap/README.md"
sync_file "$LOCAL_CODE_ROOT/WORKSPACE_BOOTSTRAP.md" \
  "$REMOTE_CANONICAL_ROOT/bootstrap/WORKSPACE_BOOTSTRAP.md"
sync_file "$LOCAL_CODE_ROOT/.mcp.json" \
  "$REMOTE_CANONICAL_ROOT/mcp/.mcp.json"

sync_file "$LOCAL_CODE_ROOT/AGENTS.md" \
  "$REMOTE_CANONICAL_ROOT/providers/AGENTS.md"
sync_file "$LOCAL_CODE_ROOT/CODEX.md" \
  "$REMOTE_CANONICAL_ROOT/providers/CODEX.md"
sync_file "$LOCAL_CODE_ROOT/CLAUDE.md" \
  "$REMOTE_CANONICAL_ROOT/providers/CLAUDE.md"
sync_file "$LOCAL_CODE_ROOT/GEMINI.md" \
  "$REMOTE_CANONICAL_ROOT/providers/GEMINI.md"
sync_file "$LOCAL_CODE_ROOT/OPENCLAUDE.md" \
  "$REMOTE_CANONICAL_ROOT/providers/OPENCLAUDE.md"

sync_file "$LOCAL_MEMORY_ROOT/PI_MEMORY.md" \
  "$REMOTE_LEGACY_MEMORY_ROOT/PI_MEMORY.md"
sync_file "$LOCAL_MEMORY_ROOT/AGENTS.md" \
  "$REMOTE_LEGACY_MEMORY_ROOT/AGENTS.md"
sync_file "$LOCAL_MEMORY_ROOT/MEMORY_SYNC.md" \
  "$REMOTE_LEGACY_MEMORY_ROOT/MEMORY_SYNC.md"
sync_file "$LOCAL_MEMORY_ROOT/PI_MEMORY.md" \
  "$REMOTE_VAULT_MEMORY_ROOT/PI_MEMORY.md"
sync_file "$LOCAL_MEMORY_ROOT/AGENTS.md" \
  "$REMOTE_VAULT_MEMORY_ROOT/AGENTS.md"

ssh "$VPS" \
  "test -f \"$REMOTE_CANONICAL_ROOT/providers/AGENTS.md\" \
    && test -f \"$REMOTE_CANONICAL_ROOT/bootstrap/WORKSPACE_BOOTSTRAP.md\" \
    && test -f \"$REMOTE_LEGACY_MEMORY_ROOT/PI_MEMORY.md\""

ok "VPS memory sync completed against canonical taxonomy roots"
log "No app restart was performed; sync is now decoupled from the removed pi-local-app runtime."
