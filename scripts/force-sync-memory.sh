#!/bin/bash
set -euo pipefail

LOG="/var/log/memory-sync.log"
TS=$(date "+%Y-%m-%d %H:%M:%S")
log() { echo "$TS | $1" | tee -a "$LOG"; }

log "=== FORCE SYNC MEMORY START ==="

# --- 1. Git: pull all remotes into VPS vault ---
cd /sync/jpglabs-docs
BRANCH=$(git branch --show-current)
git fetch --all --prune 2>&1 | tee -a "$LOG"
git pull origin "$BRANCH" --no-edit 2>&1 | tee -a "$LOG" || true
git pull gitlab "$BRANCH" --no-edit 2>&1 | tee -a "$LOG" || true
log "VPS vault atualizado (branch: $BRANCH)"

# --- 2. Sync Claude memory: VPS ↔ devices via Tailscale ---
VPS_MEM="/root/.claude/projects/sync-jpglabs-docs/memory"
WINDOWS="jader@100.77.34.128"
MAC="jadergermano@100.64.53.33"

# 2a. Windows → VPS (pull memory files)
if ssh -o ConnectTimeout=5 -o BatchMode=yes $WINDOWS "echo ok" 2>/dev/null; then
  WIN_MEM_DIRS=$(ssh $WINDOWS "find /c/Users/jader/.claude/projects -type d -name memory 2>/dev/null" || true)
  for dir in $WIN_MEM_DIRS; do
    log "Syncing Windows: $dir"
    ssh $WINDOWS "tar czf - -C \"$dir\" ." 2>/dev/null | tar xzf - -C /tmp/win-memory-import 2>/dev/null || true
  done
  # Merge: copy new/updated files into VPS memory
  if [ -d /tmp/win-memory-import ]; then
    for f in /tmp/win-memory-import/*.md; do
      [ -f "$f" ] || continue
      fname=$(basename "$f")
      if [ ! -f "$VPS_MEM/$fname" ] || ! diff -q "$f" "$VPS_MEM/$fname" > /dev/null 2>&1; then
        cp "$f" "$VPS_MEM/$fname"
        log "Imported from Windows: $fname"
      fi
    done
    rm -rf /tmp/win-memory-import
  fi
  log "Windows sync OK"
else
  log "Windows offline — skip"
fi

# 2b. Mac → VPS (pull memory files)
if ssh -o ConnectTimeout=5 -o BatchMode=yes $MAC "echo ok" 2>/dev/null; then
  MAC_MEM_DIRS=$(ssh $MAC "find ~/.claude/projects -type d -name memory 2>/dev/null" || true)
  for dir in $MAC_MEM_DIRS; do
    log "Syncing Mac: $dir"
    mkdir -p /tmp/mac-memory-import
    ssh $MAC "tar czf - -C \"$dir\" ." 2>/dev/null | tar xzf - -C /tmp/mac-memory-import 2>/dev/null || true
  done
  if [ -d /tmp/mac-memory-import ]; then
    for f in /tmp/mac-memory-import/*.md; do
      [ -f "$f" ] || continue
      fname=$(basename "$f")
      if [ ! -f "$VPS_MEM/$fname" ] || ! diff -q "$f" "$VPS_MEM/$fname" > /dev/null 2>&1; then
        cp "$f" "$VPS_MEM/$fname"
        log "Imported from Mac: $fname"
      fi
    done
    rm -rf /tmp/mac-memory-import
  fi
  log "Mac sync OK"
else
  log "Mac offline — skip"
fi

# --- 3. Push VPS memory back to online devices ---
if ssh -o ConnectTimeout=5 -o BatchMode=yes $WINDOWS "echo ok" 2>/dev/null; then
  for dir in $(ssh $WINDOWS "find /c/Users/jader/.claude/projects -type d -name memory 2>/dev/null" || true); do
    tar czf - -C "$VPS_MEM" . | ssh $WINDOWS "tar xzf - -C \"$dir\"" 2>/dev/null || true
  done
  log "Pushed memory → Windows"
fi

if ssh -o ConnectTimeout=5 -o BatchMode=yes $MAC "echo ok" 2>/dev/null; then
  for dir in $(ssh $MAC "find ~/.claude/projects -type d -name memory 2>/dev/null" || true); do
    tar czf - -C "$VPS_MEM" . | ssh $MAC "tar xzf - -C \"$dir\"" 2>/dev/null || true
  done
  log "Pushed memory → Mac"
fi

# --- 4. Commit vault changes if any ---
cd /sync/jpglabs-docs
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "sync: memory force-sync $(date +%Y-%m-%d-%H%M)"
  git push origin "$BRANCH" 2>&1 | tee -a "$LOG" || true
  git push gitlab "$BRANCH" 2>&1 | tee -a "$LOG" || true
  log "Changes committed and pushed"
else
  log "No changes to commit"
fi

log "=== FORCE SYNC MEMORY DONE ==="
