#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Deploy pi-local-app + memory files to VPS (run from Mac anytime)
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

# Canonical lane naming lives in infrastructure/config/runtime-lanes.yml.
VPS="${VPS:-root@srv1443703.hstgr.cloud}"
PI_LOCAL="${PI_LOCAL:-$HOME/code/jpglabs/pi-local-app}"
MEMORY_FILE="${MEMORY_FILE:-$HOME/code/jpglabs/docs/memory/PI_MEMORY.md}"
AGENTS_FILE="${AGENTS_FILE:-$HOME/code/jpglabs/docs/memory/AGENTS.md}"
THREADS_FILE="${THREADS_FILE:-$HOME/code/jpglabs/docs/memory/active-threads.json}"
ARCHITECTURE_FILE="${ARCHITECTURE_FILE:-$HOME/code/jpglabs/docs/infrastructure/docs/architecture.md}"
DOCS_ROOT="${DOCS_ROOT:-${KNOWLEDGE_HUB_ROOT:-$HOME/code/jpglabs/docs}}"
INFRA_DOCS_DIR="${INFRA_DOCS_DIR:-$HOME/code/jpglabs/docs/infrastructure/docs}"
PORTFOLIO_PUBLIC_DOCS_DIR="${PORTFOLIO_PUBLIC_DOCS_DIR:-$HOME/code/jpglabs/portfolio-backend/docs}"
RECENT_MEMORIES_DIR="${RECENT_MEMORIES_DIR:-$HOME/.codex/memories}"
PI_AGENT_LOG_DIR="${PI_AGENT_LOG_DIR:-$HOME/code/jpglabs/docs/memory/logs}"
SESSIONS_DIR="${SESSIONS_DIR:-$HOME/code/jpglabs/docs/memory/sessions}"
PROFILES_DIR="${PROFILES_DIR:-$PI_LOCAL/profiles}"
PROFILE_ID="${PROFILE_ID:-jader}"
PROFILE_NAME="${PROFILE_NAME:-Jader Philipe}"
PI_SERVICE_DSV_URL="${PI_SERVICE_DSV_URL:-http://localhost:3131}"
PI_SERVICE_STG_URL="${PI_SERVICE_STG_URL:-https://stg.jpglabs.com.br/pi}"
PI_SERVICE_PROD_URL="${PI_SERVICE_PROD_URL:-https://jpglabs.com.br/pi}"
PUBLIC_BASE_URL="${PUBLIC_BASE_URL:-$PI_SERVICE_PROD_URL}"
PUBLIC_HOST="${PUBLIC_HOST:-jpglabs.com.br}"
PUBLIC_PREFIX="${PUBLIC_PREFIX:-/pi}"
PORTFOLIO_WEB_ROOT="${PORTFOLIO_WEB_ROOT:-/var/www/jpglabs-portfolio/current}"
REMOTE_ROOT="${REMOTE_ROOT:-/opt/pi-local-app}"
REMOTE_MEMORY_DIR="$REMOTE_ROOT/memory"
REMOTE_PROFILES_DIR="$REMOTE_ROOT/profiles"
REMOTE_STATE_DIR="$REMOTE_ROOT/state"
REMOTE_RECENT_DIR="$REMOTE_MEMORY_DIR/recent"
REMOTE_LOG_DIR="$REMOTE_MEMORY_DIR/logs"
REMOTE_SESSIONS_DIR="$REMOTE_MEMORY_DIR/sessions"
REMOTE_DOCS_DIR="$REMOTE_MEMORY_DIR/docs"
REMOTE_INFRA_DOCS_DIR="$REMOTE_MEMORY_DIR/infrastructure-docs"
REMOTE_PORTFOLIO_PUBLIC_DOCS_DIR="$REMOTE_MEMORY_DIR/portfolio-public-docs"

log() { echo "[$(date '+%H:%M:%S')] $*"; }
ok()  { echo "[$(date '+%H:%M:%S')] ✅ $*"; }
warn(){ echo "[$(date '+%H:%M:%S')] ⚠️  $*"; }

sync_dir_contents_if_present() {
  local local_dir="$1"
  local remote_dir="$2"
  if [[ ! -d "$local_dir" ]]; then
    warn "Skipping missing directory: $local_dir"
    return 0
  fi
  ssh "$VPS" "mkdir -p '$remote_dir'"
  scp -r "$local_dir/." "$VPS:$remote_dir/"
}

sync_file_if_present() {
  local local_file="$1"
  local remote_file="$2"
  if [[ ! -f "$local_file" ]]; then
    warn "Skipping missing file: $local_file"
    return 0
  fi
  scp "$local_file" "$VPS:$remote_file"
}

sync_hub_canonical_docs() {
  local local_root="$1"
  local remote_root="$2"
  sync_dir_contents_if_present "$local_root/projects" "$remote_root/projects"
  sync_dir_contents_if_present "$local_root/agents" "$remote_root/agents"
  sync_dir_contents_if_present "$local_root/llms" "$remote_root/llms"
  sync_file_if_present "$local_root/README.md" "$remote_root/README.md"
  sync_file_if_present "$local_root/WORKSPACE_INDEX.md" "$remote_root/WORKSPACE_INDEX.md"
  sync_file_if_present "$local_root/RULES.md" "$remote_root/RULES.md"
  sync_file_if_present "$local_root/OWNERSHIP.md" "$remote_root/OWNERSHIP.md"
  sync_file_if_present "$local_root/cloudflare-email-structure.md" "$remote_root/cloudflare-email-structure.md"
}

log "Deploying to VPS..."

# 0. Ensure remote paths exist
ssh "$VPS" "mkdir -p '$REMOTE_ROOT/src' '$REMOTE_MEMORY_DIR' '$REMOTE_PROFILES_DIR' '$REMOTE_STATE_DIR' '$REMOTE_RECENT_DIR' '$REMOTE_LOG_DIR' '$REMOTE_SESSIONS_DIR' '$REMOTE_DOCS_DIR' '$REMOTE_INFRA_DOCS_DIR' '$REMOTE_PORTFOLIO_PUBLIC_DOCS_DIR' '$PORTFOLIO_WEB_ROOT' && find '$REMOTE_ROOT/src' -mindepth 1 -maxdepth 1 -exec rm -rf {} + && find '$REMOTE_PROFILES_DIR' -mindepth 1 -maxdepth 1 -exec rm -rf {} + && find '$REMOTE_RECENT_DIR' -mindepth 1 -maxdepth 1 -exec rm -rf {} + && find '$REMOTE_LOG_DIR' -mindepth 1 -maxdepth 1 -exec rm -rf {} + && find '$REMOTE_SESSIONS_DIR' -mindepth 1 -maxdepth 1 -exec rm -rf {} + && find '$REMOTE_DOCS_DIR' -mindepth 1 -maxdepth 1 -exec rm -rf {} + && find '$REMOTE_INFRA_DOCS_DIR' -mindepth 1 -maxdepth 1 -exec rm -rf {} + && find '$REMOTE_PORTFOLIO_PUBLIC_DOCS_DIR' -mindepth 1 -maxdepth 1 -exec rm -rf {} + && rm -f '$REMOTE_MEMORY_DIR/active-threads.json'"

# 1. Copy pi-local-app source
scp -r "$PI_LOCAL/src/." "$VPS:$REMOTE_ROOT/src/"
scp "$PI_LOCAL/package.json" "$VPS:$REMOTE_ROOT/"
ok "Source copied"

# 2. Sync memory files and optional profile assets
scp "$MEMORY_FILE" "$VPS:$REMOTE_MEMORY_DIR/PI_MEMORY.md"
scp "$AGENTS_FILE" "$VPS:$REMOTE_MEMORY_DIR/AGENTS.md"
sync_file_if_present "$THREADS_FILE" "$REMOTE_MEMORY_DIR/active-threads.json"
sync_file_if_present "$ARCHITECTURE_FILE" "$REMOTE_MEMORY_DIR/service-architecture.md"
sync_dir_contents_if_present "$RECENT_MEMORIES_DIR" "$REMOTE_RECENT_DIR"
sync_dir_contents_if_present "$PI_AGENT_LOG_DIR" "$REMOTE_LOG_DIR"
sync_dir_contents_if_present "$SESSIONS_DIR" "$REMOTE_SESSIONS_DIR"
sync_hub_canonical_docs "$DOCS_ROOT" "$REMOTE_DOCS_DIR"
sync_dir_contents_if_present "$INFRA_DOCS_DIR" "$REMOTE_INFRA_DOCS_DIR"
sync_dir_contents_if_present "$PORTFOLIO_PUBLIC_DOCS_DIR" "$REMOTE_PORTFOLIO_PUBLIC_DOCS_DIR"
if [[ -d "$PROFILES_DIR" ]] && [[ -n "$(find "$PROFILES_DIR" -maxdepth 1 -type f -name '*.json' -print -quit)" ]]; then
  sync_dir_contents_if_present "$PROFILES_DIR" "$REMOTE_PROFILES_DIR"
else
  warn "No profile JSON files found under $PROFILES_DIR; built-in profile will be used"
fi
ok "Memory and profile assets synced"

# 3. Resolve/persist API key
PI_API_KEY_VALUE="${PI_API_KEY:-}"
if [[ -z "$PI_API_KEY_VALUE" ]]; then
  PI_API_KEY_VALUE="$(ssh "$VPS" "umask 077; mkdir -p '$REMOTE_STATE_DIR'; if [ -s '$REMOTE_STATE_DIR/pi_api_key' ]; then cat '$REMOTE_STATE_DIR/pi_api_key'; else openssl rand -hex 32 | tee '$REMOTE_STATE_DIR/pi_api_key' >/dev/null; cat '$REMOTE_STATE_DIR/pi_api_key'; fi")"
fi

# 4. Refresh runtime config
ssh "$VPS" "cat > '$REMOTE_ROOT/.env'" <<ENV
PORT=3131
NODE_ENV=production
BIND_ADDR=localhost
PUBLIC_BASE_URL=$PUBLIC_BASE_URL
OLLAMA_BASE=http://localhost:11434
PI_SERVICE_DSV_URL=$PI_SERVICE_DSV_URL
PI_SERVICE_STG_URL=$PI_SERVICE_STG_URL
PI_SERVICE_PROD_URL=$PI_SERVICE_PROD_URL
PI_OLLAMA_BASE_URL=http://localhost:11434
PI_OLLAMA_ADMIN_URL=http://localhost:11434/api/tags
DEFAULT_MODEL=qwen2.5-coder:7b
FAST_MODEL=llama3.2:3b
LARGE_MODEL=deepseek-r1:7b
PI_API_KEY=$PI_API_KEY_VALUE
PI_PROFILE_ID="$PROFILE_ID"
PI_PROFILE_NAME="$PROFILE_NAME"
PI_PROFILES_DIR=$REMOTE_PROFILES_DIR
PI_ACTIVE_PROFILE_PATH=$REMOTE_STATE_DIR/active-profile.json
PI_MEMORY_PATH=$REMOTE_MEMORY_DIR/PI_MEMORY.md
AGENTS_PATH=$REMOTE_MEMORY_DIR/AGENTS.md
PI_THREADS_PATH=$REMOTE_MEMORY_DIR/active-threads.json
PI_ARCHITECTURE_PATH=$REMOTE_MEMORY_DIR/service-architecture.md
PI_DOCS_ROOT=$REMOTE_DOCS_DIR
PI_KNOWLEDGE_HUB_ROOT=$REMOTE_DOCS_DIR
PI_INFRA_DOCS_DIR=$REMOTE_INFRA_DOCS_DIR
PI_PORTFOLIO_PUBLIC_DOCS_DIR=$REMOTE_PORTFOLIO_PUBLIC_DOCS_DIR
PI_RECENT_MEMORIES_DIR=$REMOTE_RECENT_DIR
PI_SESSIONS_DIR=$REMOTE_SESSIONS_DIR
PI_AGENT_LOG_DIR=$REMOTE_LOG_DIR
ENV

ssh "$VPS" "mkdir -p /etc/nginx/ssl"
ssh "$VPS" "mkdir -p /etc/nginx/snippets/pi-extra-routes"
ssh "$VPS" "if [ ! -f /etc/nginx/ssl/jpglabs-selfsigned.key ]; then openssl req -x509 -nodes -newkey rsa:2048 -keyout /etc/nginx/ssl/jpglabs-selfsigned.key -out /etc/nginx/ssl/jpglabs-selfsigned.crt -days 3650 -subj '/CN=$PUBLIC_HOST'; fi"
ssh "$VPS" "cat > /etc/nginx/sites-available/pibar" <<NGINX
server {
  listen 80 default_server;
  listen [::]:80 default_server;
  server_name $PUBLIC_HOST www.$PUBLIC_HOST _;

  location = $PUBLIC_PREFIX {
    return 308 $PUBLIC_PREFIX/;
  }

  location $PUBLIC_PREFIX/ {
    proxy_http_version 1.1;
    proxy_set_header Host \$host;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto \$scheme;
    proxy_set_header X-Forwarded-Host \$host;
    proxy_set_header X-Forwarded-Prefix $PUBLIC_PREFIX;
    proxy_pass http://localhost:3131/;
  }

  include /etc/nginx/snippets/pi-extra-routes/*.conf;

  location / {
    root $PORTFOLIO_WEB_ROOT;
    try_files \$uri \$uri/ /index.html;
  }
}

server {
  listen 443 ssl http2 default_server;
  listen [::]:443 ssl http2 default_server;
  server_name $PUBLIC_HOST www.$PUBLIC_HOST _;

  ssl_certificate /etc/nginx/ssl/jpglabs-selfsigned.crt;
  ssl_certificate_key /etc/nginx/ssl/jpglabs-selfsigned.key;

  location = $PUBLIC_PREFIX {
    return 308 $PUBLIC_PREFIX/;
  }

  location $PUBLIC_PREFIX/ {
    proxy_http_version 1.1;
    proxy_set_header Host \$host;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto \$scheme;
    proxy_set_header X-Forwarded-Host \$host;
    proxy_set_header X-Forwarded-Prefix $PUBLIC_PREFIX;
    proxy_pass http://localhost:3131/;
  }

  include /etc/nginx/snippets/pi-extra-routes/*.conf;

  location / {
    root $PORTFOLIO_WEB_ROOT;
    try_files \$uri \$uri/ /index.html;
  }
}
NGINX
ssh "$VPS" "rm -f /etc/nginx/sites-enabled/default && ln -sf /etc/nginx/sites-available/pibar /etc/nginx/sites-enabled/pibar && nginx -t"
ssh "$VPS" "if k3s kubectl -n kube-system get svc traefik >/dev/null 2>&1; then k3s kubectl -n kube-system patch svc traefik --type merge -p '{\"spec\":{\"type\":\"ClusterIP\"}}'; fi"
ok "Runtime config refreshed"

# 5. Install deps + restart
ssh "$VPS" "cd '$REMOTE_ROOT' && npm ci --only=production 2>/dev/null || npm install --only=production"
ssh "$VPS" "systemctl disable --now caddy traefik 2>/dev/null || true && systemctl enable --now ollama nginx pi-local-app && systemctl restart nginx pi-local-app && sleep 3 && systemctl is-active pi-local-app"
ok "pi-local-app restarted"

# 6. Health and MCP check
sleep 2
HEALTH=$(ssh "$VPS" "curl -sf http://localhost:3131/health" 2>/dev/null || echo "fail")
PROFILES=$(curl -sf -H "Authorization: Bearer $PI_API_KEY_VALUE" "$PUBLIC_BASE_URL/profiles" 2>/dev/null || echo "fail")
echo "$HEALTH" | grep -Eq '"status"[[:space:]]*:[[:space:]]*"ok"' && ok "Health check passed" || warn "Health check: $HEALTH"
echo "$PROFILES" | grep -Eq '"profiles"' && ok "Protected MCP/profile route validated" || warn "Protected route check: $PROFILES"

log "VPS live at $PUBLIC_BASE_URL"
log "Protected MCP token stored on VPS at $REMOTE_STATE_DIR/pi_api_key"
