#!/bin/bash
set -euo pipefail

LOG="/var/log/memory-sync.log"
TS=$(date "+%Y-%m-%d %H:%M:%S")
log() { echo "$TS | $1" | tee -a "$LOG"; }

log "=== FORCE SYNC MEMORY START ==="

BRANCH="feature/unified-memory-center"
WINDOWS="jader@100.77.34.128"
MAC="jadergermano@100.64.53.33"

# --- 1. VPS vault: commit local changes, push to remotes ---
cd /sync/jpglabs-docs
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "sync: auto-sync $(date +%Y-%m-%d-%H%M)" || true
  log "VPS: committed local changes"
fi

git fetch --all --prune 2>&1 | tee -a "$LOG"

# Merge de cada remote (preferir rebase para histórico limpo)
for remote in origin gitlab; do
  if git rev-parse --verify "$remote/$BRANCH" >/dev/null 2>&1; then
    git merge "$remote/$BRANCH" --no-edit 2>&1 | tee -a "$LOG" || {
      log "CONFLITO com $remote — tentando auto-resolve (theirs para .obsidian, ours para memory)"
      # .obsidian e gerados: aceita remote. memory/: preserva VPS (source of truth)
      git checkout --theirs -- .obsidian/ 2>/dev/null || true
      git checkout --ours -- memory/ reports/ scripts/ 2>/dev/null || true
      git add -A && git commit --no-edit 2>/dev/null || true
    }
  fi
done

# Push VPS (source of truth) para ambos remotes
git push origin "$BRANCH" 2>&1 | tee -a "$LOG" || true
git push gitlab "$BRANCH" 2>&1 | tee -a "$LOG" || true
log "VPS: remotes atualizados"

# --- 2. Mac Air: git pull em cada repo de ~/code ---
if ssh -o ConnectTimeout=5 -o BatchMode=yes $MAC "echo ok" 2>/dev/null; then
  ssh $MAC bash -s << MACSYNC
    cd ~/code 2>/dev/null || exit 0
    for repo in $(find . -maxdepth 2 -name .git -type d 2>/dev/null); do
      dir=$(dirname "$repo")
      cd ~/code/"$dir"
      branch=$(git branch --show-current 2>/dev/null)
      [ -z "$branch" ] && continue
      echo "[Mac] Syncing $dir (branch: $branch)"
      git fetch --all --prune 2>/dev/null
      git pull --rebase --autostash origin "$branch" 2>/dev/null || git pull --no-rebase origin "$branch" 2>/dev/null || echo "[Mac] SKIP $dir — conflito manual"
    done
MACSYNC
  log "Mac: repos atualizados via git pull"
else
  log "Mac offline — skip"
fi

# --- 3. Windows: git pull nos repos conhecidos ---
if ssh -o ConnectTimeout=5 -o BatchMode=yes $WINDOWS "echo ok" 2>/dev/null; then
  ssh $WINDOWS bash -s << WINSYNC
    for dir in /c/docker/jpglabs-docs /c/Users/jader/Documents/TSE/Projetos/Docentes/docentes-backend; do
      [ -d "$dir/.git" ] || continue
      cd "$dir"
      branch=$(git branch --show-current 2>/dev/null)
      [ -z "$branch" ] && continue
      echo "[Win] Syncing $dir (branch: $branch)"
      git fetch --all --prune 2>/dev/null
      git pull --rebase --autostash origin "$branch" 2>/dev/null || echo "[Win] SKIP $dir"
    done
WINSYNC
  log "Windows: repos atualizados"
else
  log "Windows offline — skip"
fi

# --- 4. Claude memory: sync VPS → devices ---
VPS_MEM="/root/.claude/projects/sync-jpglabs-docs/memory"

if ssh -o ConnectTimeout=5 -o BatchMode=yes $MAC "echo ok" 2>/dev/null; then
  MAC_DIRS=$(ssh $MAC "find ~/.claude/projects -type d -name memory 2>/dev/null" || true)
  for dir in $MAC_DIRS; do
    tar czf - -C "$VPS_MEM" . | ssh $MAC "tar xzf - -C \"$dir\"" 2>/dev/null || true
  done
  log "Claude memory → Mac OK"
fi

if ssh -o ConnectTimeout=5 -o BatchMode=yes $WINDOWS "echo ok" 2>/dev/null; then
  WIN_DIRS=$(ssh $WINDOWS "find /c/Users/jader/.claude/projects -type d -name memory 2>/dev/null" || true)
  for dir in $WIN_DIRS; do
    tar czf - -C "$VPS_MEM" . | ssh $WINDOWS "tar xzf - -C \"$dir\"" 2>/dev/null || true
  done
  log "Claude memory → Windows OK"
fi

log "=== FORCE SYNC MEMORY DONE ==="
