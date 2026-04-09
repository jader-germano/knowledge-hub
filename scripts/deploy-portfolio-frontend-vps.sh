#!/usr/bin/env bash
set -euo pipefail

VPS="${VPS:-root@srv1443703.hstgr.cloud}"
PORTFOLIO_APP="${PORTFOLIO_APP:-$HOME/code/jpglabs/portfolio-frontend}"
PUBLIC_HOST="${PUBLIC_HOST:-jpglabs.com.br}"
PUBLIC_PREFIX="${PUBLIC_PREFIX:-/pi}"
PUBLIC_PI_URL="${PUBLIC_PI_URL:-https://jpglabs.com.br/pi}"
PORTFOLIO_WEB_ROOT="${PORTFOLIO_WEB_ROOT:-/var/www/jpglabs-portfolio/current}"
NPM_BIN="${NPM_BIN:-$(command -v npm || true)}"

log() { echo "[$(date '+%H:%M:%S')] $*"; }
ok()  { echo "[$(date '+%H:%M:%S')] ✅ $*"; }

if [[ -z "$NPM_BIN" ]]; then
  for candidate in \
    "$HOME/.nvm/versions/node/v22.22.0/bin/npm" \
    "$HOME/.nvm/versions/node/v22.19.0/bin/npm" \
    "$HOME/.nvm/versions/node/v20.2.0/bin/npm"
  do
    if [[ -x "$candidate" ]]; then
      NPM_BIN="$candidate"
      break
    fi
  done
fi

if [[ -z "$NPM_BIN" ]]; then
  echo "npm not found. Set NPM_BIN or ensure npm is on PATH." >&2
  exit 1
fi

NODE_BIN_DIR="$(dirname "$NPM_BIN")"
export PATH="$NODE_BIN_DIR:$PATH"

log "Building portfolio frontend..."
cd "$PORTFOLIO_APP"
"$NPM_BIN" ci
VITE_BASE_PATH=/ "$NPM_BIN" run build
ok "Portfolio build ready"

log "Syncing static files to VPS..."
ssh "$VPS" "mkdir -p '$PORTFOLIO_WEB_ROOT' && find '$PORTFOLIO_WEB_ROOT' -mindepth 1 -maxdepth 1 -exec rm -rf {} +"
scp -r "$PORTFOLIO_APP/dist/." "$VPS:$PORTFOLIO_WEB_ROOT/"
ok "Static files copied"

log "Refreshing Nginx edge..."
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
ssh "$VPS" "ln -sf /etc/nginx/sites-available/pibar /etc/nginx/sites-enabled/pibar && nginx -t && systemctl restart nginx"
ok "Nginx updated"

log "Validating public endpoints..."
curl -sfI "https://$PUBLIC_HOST/"
curl -sfI "https://$PUBLIC_HOST/offer"
curl -sfI "https://$PUBLIC_HOST/portifolio/jader-germano"
curl -sf "$PUBLIC_PI_URL/health" >/dev/null
ok "Public checks passed"

log "Portfolio live at https://$PUBLIC_HOST/"
