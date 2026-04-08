#!/usr/bin/env bash
set -euo pipefail

# Canonical lane naming lives in infrastructure/config/runtime-lanes.yml.
VPS="${VPS:-root@srv1443703.hstgr.cloud}"
PI_CONTROL_LOCAL="${PI_CONTROL_LOCAL:-$HOME/code/pessoal/pi-control-app}"
PUBLIC_HOST="${PUBLIC_HOST:-jpglabs.com.br}"
REMOTE_ROOT="${REMOTE_ROOT:-/opt/pi-control-app}"
REMOTE_STATE_DIR="$REMOTE_ROOT/state"
REMOTE_SNIPPET_PATH="/etc/nginx/snippets/pi-extra-routes/pi-control-app.conf"

log() { echo "[$(date '+%H:%M:%S')] $*"; }
ok()  { echo "[$(date '+%H:%M:%S')] ✅ $*"; }

log "Building pi-control-app locally..."
(cd "$PI_CONTROL_LOCAL" && npm run build >/dev/null)
ok "Local build ready"

log "Preparing remote directories..."
ssh "$VPS" "mkdir -p '$REMOTE_ROOT/dist' '$REMOTE_STATE_DIR' /etc/nginx/snippets/pi-extra-routes && find '$REMOTE_ROOT/dist' -mindepth 1 -maxdepth 1 -exec rm -rf {} +"

scp -r "$PI_CONTROL_LOCAL/dist/." "$VPS:$REMOTE_ROOT/dist/"
scp "$PI_CONTROL_LOCAL/package.json" "$VPS:$REMOTE_ROOT/"
scp "$PI_CONTROL_LOCAL/package-lock.json" "$VPS:$REMOTE_ROOT/"
ok "Artifacts copied"

PI_LOCAL_API_KEY_VALUE="$(ssh "$VPS" "cat /opt/pi-local-app/state/pi_api_key")"
PUBLIC_CONTROL_PREFIX="${PUBLIC_CONTROL_PREFIX:-}"

if [[ -z "$PUBLIC_CONTROL_PREFIX" ]]; then
  PUBLIC_CONTROL_PREFIX="$(ssh "$VPS" "umask 077; mkdir -p '$REMOTE_STATE_DIR'; if [ -s '$REMOTE_STATE_DIR/public_prefix_token' ]; then TOKEN=\$(cat '$REMOTE_STATE_DIR/public_prefix_token'); else TOKEN=\$(openssl rand -hex 8); echo \$TOKEN > '$REMOTE_STATE_DIR/public_prefix_token'; fi; printf '/pi-control-%s' \"\$TOKEN\"")"
fi

ssh "$VPS" "cat > '$REMOTE_ROOT/.env'" <<ENV
HOST=localhost
PORT=3030
PI_LOCAL_API_BASE=http://localhost:3131
PI_LOCAL_API_KEY=$PI_LOCAL_API_KEY_VALUE
ENV

ssh "$VPS" "cat > /etc/systemd/system/pi-control-app.service" <<'SVC'
[Unit]
Description=Pi Control App — GPT-facing MCP surface
After=network.target pi-local-app.service
Wants=pi-local-app.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/pi-control-app
EnvironmentFile=/opt/pi-control-app/.env
ExecStart=/usr/bin/node dist/server.js
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SVC

ssh "$VPS" "cat > '$REMOTE_SNIPPET_PATH'" <<NGINX
location = $PUBLIC_CONTROL_PREFIX {
  return 308 $PUBLIC_CONTROL_PREFIX/;
}

location $PUBLIC_CONTROL_PREFIX/ {
  proxy_http_version 1.1;
  proxy_set_header Host \$host;
  proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
  proxy_set_header X-Forwarded-Proto \$scheme;
  proxy_set_header X-Forwarded-Host \$host;
  proxy_set_header X-Forwarded-Prefix $PUBLIC_CONTROL_PREFIX;
  proxy_pass http://localhost:3030/;
}
NGINX

ssh "$VPS" "systemctl daemon-reload && cd '$REMOTE_ROOT' && npm ci --omit=dev && systemctl enable --now pi-control-app && nginx -t && systemctl restart nginx pi-control-app && sleep 3 && systemctl is-active pi-control-app"
ok "pi-control-app restarted on VPS"

PUBLIC_BASE_URL="https://$PUBLIC_HOST$PUBLIC_CONTROL_PREFIX"
SUMMARY="$(curl -sf "$PUBLIC_BASE_URL/" 2>/dev/null || true)"
HEALTH="$(curl -sf "$PUBLIC_BASE_URL/health" 2>/dev/null || true)"
INIT="$(curl -sf -X POST "$PUBLIC_BASE_URL/mcp" -H 'Accept: application/json, text/event-stream' -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","id":"init-1","method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"deploy-smoke","version":"1.0"}}}' 2>/dev/null || true)"

echo "$SUMMARY" | grep -q '"name":"pi-control-app"' && ok "Public summary check passed" || { echo "$SUMMARY"; exit 1; }
echo "$HEALTH" | grep -q '"status":"ok"' && ok "Public health check passed" || { echo "$HEALTH"; exit 1; }
echo "$INIT" | grep -q '"protocolVersion":"2025-03-26"' && ok "Public MCP initialize check passed" || { echo "$INIT"; exit 1; }

log "pi-control-app live at $PUBLIC_BASE_URL"
log "Use MCP endpoint: $PUBLIC_BASE_URL/mcp"
