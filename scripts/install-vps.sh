#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# JPGLabs VPS — Full stack install (run once after fresh OS)
# Executed remotely: ssh root@VPS "bash -s" < install-vps.sh
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

# Canonical lane naming lives in infrastructure/config/runtime-lanes.yml.
PI_SERVICE_PROD_URL="${PI_SERVICE_PROD_URL:-https://jpglabs.com.br/pi}"

log() { echo -e "\n\033[1;36m[$(date '+%H:%M:%S')] $*\033[0m"; }
ok()  { echo -e "\033[1;32m✅ $*\033[0m"; }

log "=== JPGLabs VPS Setup — Ubuntu 24.04 ==="

# ── 1. System packages ────────────────────────────────────────────────────────
log "Installing packages..."
apt-get update -qq
apt-get install -y -qq curl wget git htop ufw net-tools ca-certificates gnupg
ok "Packages installed"

# ── 2. Firewall ───────────────────────────────────────────────────────────────
log "Configuring firewall..."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 25/tcp
ufw allow 587/tcp
ufw allow 993/tcp
ufw --force enable
ok "Firewall active"

# ── 3. Docker ────────────────────────────────────────────────────────────────
log "Installing Docker..."
if ! command -v docker &>/dev/null; then
  curl -fsSL https://get.docker.com | sh
  systemctl enable --now docker
fi
docker --version
ok "Docker ready"

# ── 4. k3s (lightweight Kubernetes) ──────────────────────────────────────────
log "Installing k3s..."
if ! command -v k3s &>/dev/null; then
  curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--write-kubeconfig-mode=644" sh -
  sleep 20
fi
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
k3s kubectl get nodes
ok "k3s ready"

# ── 5. Ollama ────────────────────────────────────────────────────────────────
log "Installing Ollama..."
if ! command -v ollama &>/dev/null; then
  curl -fsSL https://ollama.com/install.sh | sh
  sleep 10
fi
systemctl enable --now ollama
ollama --version
ok "Ollama ready"

# ── 6. Pull AI models ────────────────────────────────────────────────────────
log "Pulling AI models (this takes a while)..."
ollama pull qwen2.5-coder:7b  &
ollama pull llama3.2:3b        &
wait
log "Pulling large model in background..."
nohup ollama pull deepseek-r1:7b > /var/log/ollama-pull.log 2>&1 &
echo "deepseek-r1:7b pulling in background — check: tail -f /var/log/ollama-pull.log"
ok "Models: qwen2.5-coder:7b + llama3.2:3b done | deepseek-r1:7b in background"

# ── 7. Node.js (for pi-local-app) ────────────────────────────────────────────
log "Installing Node.js 22..."
if ! command -v node &>/dev/null; then
  curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
  apt-get install -y nodejs
fi
node --version
ok "Node.js ready"

# ── 8. pi-local-app ──────────────────────────────────────────────────────────
log "Deploying pi-local-app..."
mkdir -p /opt/pi-local-app/src /opt/pi-local-app/memory /opt/pi-local-app/profiles /opt/pi-local-app/state /opt/pi-local-app/memory/recent /opt/pi-local-app/memory/pi-agent-log /opt/pi-local-app/memory/sessions

# Write server.js (will be replaced by scp later but bootstrap here)
cat > /opt/pi-local-app/package.json <<'PKG'
{"name":"pi-local","version":"1.0.0","main":"src/server.js","scripts":{"start":"node src/server.js"}}
PKG

# Env for VPS
cat > /opt/pi-local-app/.env <<ENV
PORT=3131
NODE_ENV=production
BIND_ADDR=localhost
PUBLIC_BASE_URL=$PI_SERVICE_PROD_URL
OLLAMA_BASE=http://localhost:11434
PI_SERVICE_DSV_URL=http://localhost:3131
PI_SERVICE_STG_URL=https://stg.jpglabs.com.br/pi
PI_SERVICE_PROD_URL=$PI_SERVICE_PROD_URL
PI_OLLAMA_BASE_URL=http://localhost:11434
PI_OLLAMA_ADMIN_URL=http://localhost:11434/api/tags
DEFAULT_MODEL=qwen2.5-coder:7b
FAST_MODEL=llama3.2:3b
LARGE_MODEL=deepseek-r1:7b
PI_API_KEY=
PI_PROFILE_ID="jader"
PI_PROFILE_NAME="Jader Philipe"
PI_PROFILES_DIR=/opt/pi-local-app/profiles
PI_ACTIVE_PROFILE_PATH=/opt/pi-local-app/state/active-profile.json
PI_MEMORY_PATH=/opt/pi-local-app/memory/PI_MEMORY.md
AGENTS_PATH=/opt/pi-local-app/memory/AGENTS.md
PI_THREADS_PATH=/opt/pi-local-app/memory/active-threads.json
PI_ARCHITECTURE_PATH=/opt/pi-local-app/memory/service-architecture.md
PI_RECENT_MEMORIES_DIR=/opt/pi-local-app/memory/recent
PI_SESSIONS_DIR=/opt/pi-local-app/memory/sessions
PI_AGENT_LOG_DIR=/opt/pi-local-app/memory/pi-agent-log
ENV

# Systemd service
cat > /etc/systemd/system/pi-local-app.service <<'SVC'
[Unit]
Description=Pi Personal Memory Service — AI bridge
After=network.target ollama.service
Wants=ollama.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/pi-local-app
EnvironmentFile=/opt/pi-local-app/.env
ExecStart=/usr/bin/node src/server.js
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SVC

systemctl daemon-reload
ok "pi-local-app service registered"

# ── 9. Nginx edge + k3s ingress isolation ───────────────────────────────────
log "Configuring Nginx edge..."
apt-get install -y -qq nginx openssl
mkdir -p /etc/nginx/ssl
mkdir -p /etc/nginx/snippets/pi-extra-routes
mkdir -p /var/www/jpglabs-portfolio/current

if [[ ! -f /etc/nginx/ssl/jpglabs-selfsigned.key ]]; then
  openssl req -x509 -nodes -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/jpglabs-selfsigned.key \
    -out /etc/nginx/ssl/jpglabs-selfsigned.crt \
    -days 3650 \
    -subj "/CN=jpglabs.com.br"
fi

cat > /etc/nginx/sites-available/pibar <<'NGINX'
server {
  listen 80 default_server;
  listen [::]:80 default_server;
  server_name jpglabs.com.br www.jpglabs.com.br _;

  location = /pi {
    return 308 /pi/;
  }

  location /pi/ {
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-Prefix /pi;
    proxy_pass http://localhost:3131/;
  }

  include /etc/nginx/snippets/pi-extra-routes/*.conf;

  location / {
    root /var/www/jpglabs-portfolio/current;
    try_files $uri $uri/ /index.html;
  }
}

server {
  listen 443 ssl http2 default_server;
  listen [::]:443 ssl http2 default_server;
  server_name jpglabs.com.br www.jpglabs.com.br _;

  ssl_certificate /etc/nginx/ssl/jpglabs-selfsigned.crt;
  ssl_certificate_key /etc/nginx/ssl/jpglabs-selfsigned.key;

  location = /pi {
    return 308 /pi/;
  }

  location /pi/ {
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-Prefix /pi;
    proxy_pass http://localhost:3131/;
  }

  include /etc/nginx/snippets/pi-extra-routes/*.conf;

  location / {
    root /var/www/jpglabs-portfolio/current;
    try_files $uri $uri/ /index.html;
  }
}
NGINX

rm -f /etc/nginx/sites-enabled/default
ln -sf /etc/nginx/sites-available/pibar /etc/nginx/sites-enabled/pibar
nginx -t

for _ in $(seq 1 30); do
  if k3s kubectl -n kube-system get svc traefik >/dev/null 2>&1; then
    k3s kubectl -n kube-system patch svc traefik --type merge -p '{"spec":{"type":"ClusterIP"}}' || true
    break
  fi
  sleep 2
done

systemctl disable --now caddy traefik 2>/dev/null || true
systemctl enable --now nginx
ok "Nginx edge configured"

# ── Done ────────────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════"
echo "  VPS base install complete"
echo "  Next: scp pi-local-app files, then start services"
echo "  Run from Mac: bash scripts/deploy-to-vps.sh"
echo "════════════════════════════════════════════════"
