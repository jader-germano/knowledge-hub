#!/bin/bash
set -euo pipefail

BRANCH="${1:-$(git -C /sync/jpglabs-docs branch --show-current)}"
LOG="/var/log/mesh-sync.log"
TS=$(date "+%Y-%m-%d %H:%M:%S")

log() { echo "$TS | $1" | tee -a "$LOG"; }

log "=== mesh-sync START | branch: $BRANCH ==="

# 1. VPS — pull latest
cd /sync/jpglabs-docs
git fetch --all --prune 2>&1 | tee -a "$LOG"
git checkout "$BRANCH" 2>/dev/null || git checkout -b "$BRANCH" "origin/$BRANCH"
git pull origin "$BRANCH" 2>&1 | tee -a "$LOG"
log "VPS atualizada"

# 2. Windows (JPRDTR) — sync via Tailscale
WINDOWS="jader@jprdtr.tail4c4f3a.ts.net"
if ssh -o ConnectTimeout=5 -o BatchMode=yes "$WINDOWS" "echo ok" 2>/dev/null; then
  ssh "$WINDOWS" "cd /c/docker/jpglabs-docs 2>/dev/null && git pull origin $BRANCH 2>&1 || echo repo nao existe no Windows — skip" | tee -a "$LOG"
  log "Windows sync OK"
else
  log "Windows offline — skip"
fi

# 3. Mac (MacBook Air) — sync via Tailscale
MAC="jadergermano@macbook-air-de-jader.tail4c4f3a.ts.net"
if ssh -o ConnectTimeout=5 -o BatchMode=yes "$MAC" "echo ok" 2>/dev/null; then
  ssh "$MAC" "cd ~/code/jpglabs/docs 2>/dev/null && git pull origin $BRANCH 2>&1 || echo repo nao existe no Mac — skip" | tee -a "$LOG"
  log "Mac sync OK"
else
  log "Mac offline — skip"
fi

log "=== mesh-sync DONE ==="
