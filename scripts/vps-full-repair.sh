#!/usr/bin/env bash
# ============================================================
# vps-full-repair.sh — Legacy Docker-path diagnosis and emergency repair
# NOTE: The approved app-platform direction is now Kubernetes-first.
# This script is retained only for legacy diagnosis or emergency containment,
# not as the target deployment model for app services.
# Run from Mac AFTER SSH key is authorized:
#   bash vps-full-repair.sh
# Author: Pi, on behalf of Jader Philipe Germano
# ============================================================
set -euo pipefail

VPS="${VPS:-root@srv1443703.hstgr.cloud}"
PORTFOLIO_DIR="${PORTFOLIO_DIR:-$HOME/code/jpglabs/portfolio-backend}"

log()  { echo ""; echo "[$(date '+%H:%M:%S')] ▶  $*"; }
ok()   { echo "[$(date '+%H:%M:%S')] ✅ $*"; }
warn() { echo "[$(date '+%H:%M:%S')] ⚠️  $*"; }
err()  { echo "[$(date '+%H:%M:%S')] ❌ $*"; }
sep()  { echo "──────────────────────────────────────────────────────"; }

# ── SSH connectivity test ───────────────────────────────────────────────────
log "Testing SSH..."
ssh -o ConnectTimeout=8 -o StrictHostKeyChecking=no $VPS "echo connected" || {
  err "SSH still failing. Complete Step 1 in hPanel first."; exit 1
}
ok "SSH OK"

# ══════════════════════════════════════════════════════════════
# PHASE 1 — SYSTEM DIAGNOSIS
# ══════════════════════════════════════════════════════════════
log "Phase 1: Full system diagnosis"
sep

ssh $VPS bash <<'REMOTE'
echo ""
echo "=== OS / Uptime ==="
uname -a && uptime

echo ""
echo "=== Disk Usage ==="
df -h /

echo ""
echo "=== Memory ==="
free -h

echo ""
echo "=== Docker containers ==="
docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'

echo ""
echo "=== Docker images (size) ==="
docker images --format 'table {{.Repository}}\t{{.Tag}}\t{{.Size}}' | head -20

echo ""
echo "=== k3s pods ==="
kubectl get pods -A --no-headers 2>/dev/null || echo "(k3s not available)"

echo ""
echo "=== UFW rules ==="
ufw status verbose

echo ""
echo "=== Traefik routes ==="
curl -sf http://localhost:8080/api/http/routers 2>/dev/null \
  | python3 -c "import sys,json; d=json.load(sys.stdin); [print(k,'→',v.get('rule','')) for k,v in d.items()]" \
  || echo "(Traefik API not on :8080)"

echo ""
echo "=== Active ports ==="
ss -tlnp | grep -E "LISTEN|:25|:80|:443|:587|:993|:5678|:8082|:3131"

echo ""
echo "=== Docker networks ==="
docker network ls

echo ""
echo "=== Logs: Traefik (last 20) ==="
docker logs n8n-traefik-1 --tail 20 2>/dev/null || echo "(traefik container not found)"

echo ""
echo "=== Logs: n8n (last 10) ==="
docker logs n8n-n8n-1 --tail 10 2>/dev/null || echo "(n8n container not found)"

echo ""
echo "=== Logs: portfolio (last 10) ==="
docker logs jpglabs-portfolio --tail 10 2>/dev/null || echo "(portfolio container not found)"

echo ""
echo "=== Mailserver status ==="
docker inspect mailserver --format '{{.State.Status}}' 2>/dev/null || echo "not running"
ls /docker/mailserver/ 2>/dev/null || echo "/docker/mailserver not found"
REMOTE

sep
ok "Phase 1 done"

# ══════════════════════════════════════════════════════════════
# PHASE 2 — DISK CLEANUP (if needed)
# ══════════════════════════════════════════════════════════════
log "Phase 2: Disk cleanup"

DISK_PCT=$(ssh $VPS "df / --output=pcent | tail -1 | tr -d '% '")
echo "  Disk usage: ${DISK_PCT}%"

if [[ "$DISK_PCT" -ge 80 ]]; then
  warn "Disk at ${DISK_PCT}% — pruning..."
  ssh $VPS bash <<'REMOTE'
    # Remove dangling images, stopped containers, unused volumes
    docker system prune -f
    # Remove old logs (keep last 50MB per container)
    find /var/lib/docker/containers -name "*.log" -exec truncate -s 50M {} \;
    # Clear apt cache
    apt-get clean -y 2>/dev/null || true
    echo "After prune:" && df -h /
REMOTE
  ok "Disk cleaned"
else
  ok "Disk OK (${DISK_PCT}%)"
fi

# ══════════════════════════════════════════════════════════════
# PHASE 3 — FIX UFW (mail + all service ports)
# ══════════════════════════════════════════════════════════════
log "Phase 3: Firewall fix"

ssh $VPS bash <<'REMOTE'
ufw allow 22/tcp   comment "SSH"
ufw allow 80/tcp   comment "HTTP"
ufw allow 443/tcp  comment "HTTPS"
ufw allow 25/tcp   comment "SMTP"
ufw allow 587/tcp  comment "SMTP submission"
ufw allow 465/tcp  comment "SMTPS"
ufw allow 993/tcp  comment "IMAPS"
ufw allow 143/tcp  comment "IMAP"
ufw --force enable
ufw status
REMOTE

ok "Firewall rules updated"

# ══════════════════════════════════════════════════════════════
# PHASE 4 — PORTFOLIO REDEPLOY
# ══════════════════════════════════════════════════════════════
log "Phase 4: Portfolio redeploy"

# Build locally and push
log "  Building portfolio Docker image..."
cd "$PORTFOLIO_DIR"
docker build -t jpglabs-portfolio:latest . 2>&1 | tail -5

log "  Saving image and uploading to VPS..."
docker save jpglabs-portfolio:latest | ssh $VPS "docker load"
ok "  Image uploaded"

# Ensure traefik_net exists and deploy
ssh $VPS bash <<'REMOTE'
# Create traefik_net if missing
docker network create traefik_net 2>/dev/null || true

# Kill existing portfolio container
docker rm -f jpglabs-portfolio 2>/dev/null || true

# Redeploy portfolio with correct Traefik labels
docker run -d \
  --name jpglabs-portfolio \
  --network traefik_net \
  --restart unless-stopped \
  -l "traefik.enable=true" \
  -l "traefik.http.routers.portfolio.rule=Host(\`jpglabs.com.br\`) || Host(\`www.jpglabs.com.br\`)" \
  -l "traefik.http.routers.portfolio.entrypoints=websecure" \
  -l "traefik.http.routers.portfolio.tls=true" \
  -l "traefik.http.routers.portfolio.tls.certresolver=letsencrypt" \
  -l "traefik.http.services.portfolio.loadbalancer.server.port=80" \
  jpglabs-portfolio:latest

# Verify
sleep 3
docker ps | grep portfolio
echo "Portfolio container started"
REMOTE

ok "Portfolio redeployed"

# ══════════════════════════════════════════════════════════════
# PHASE 5 — FIX n8n TRAEFIK ROUTE
# ══════════════════════════════════════════════════════════════
log "Phase 5: n8n Traefik fix"

ssh $VPS bash <<'REMOTE'
cd /docker/n8n
# Check if compose file has correct labels
if grep -q "n8n.jpglabs.com.br" docker-compose.yml 2>/dev/null; then
  docker compose up -d --force-recreate
  echo "n8n restarted"
else
  echo "⚠️  n8n compose file needs manual check at /docker/n8n/"
fi

# Restart Traefik to reload routes
docker restart n8n-traefik-1 2>/dev/null || docker restart traefik 2>/dev/null || true
echo "Traefik restarted"
REMOTE

ok "n8n + Traefik restarted"

# ══════════════════════════════════════════════════════════════
# PHASE 6 — MAILSERVER SETUP
# ══════════════════════════════════════════════════════════════
log "Phase 6: Mailserver setup"

# Check if the mailserver was ever started
MAIL_STATUS=$(ssh $VPS "docker inspect mailserver --format '{{.State.Status}}' 2>/dev/null || echo 'missing'")
echo "  Mailserver current status: $MAIL_STATUS"

if [[ "$MAIL_STATUS" == "missing" || "$MAIL_STATUS" == "exited" ]]; then
  warn "Mailserver not running — running finish-setup.sh if it exists..."
  ssh $VPS bash <<'REMOTE'
    if [[ -f /docker/mailserver/finish-setup.sh ]]; then
      cd /docker/mailserver
      bash finish-setup.sh 2>&1 | tail -30
    else
      echo "⚠️  finish-setup.sh not found at /docker/mailserver/"
      echo "   Manual setup required — see Phase 6 notes below"
    fi
REMOTE
fi

ok "Mailserver phase done"

# ══════════════════════════════════════════════════════════════
# PHASE 7 — CLOUDFLARE SSL FIX (526 → Full, not Strict)
# ══════════════════════════════════════════════════════════════
log "Phase 7: Cloudflare SSL fix"

CF_ZONE="bfdbc0633bf650f8451c3bed27d7965e"
CF_TOKEN_FILE="$HOME/.secrets/cloudflare-token.txt"

if [[ -f "$CF_TOKEN_FILE" ]]; then
  CF_TOKEN=$(cat "$CF_TOKEN_FILE")
  # Set SSL mode to "Full" (not Strict) — fixes 526
  RESULT=$(curl -sf -X PATCH \
    "https://api.cloudflare.com/client/v4/zones/${CF_ZONE}/settings/ssl" \
    -H "Authorization: Bearer ${CF_TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{"value":"full"}' 2>&1)
  echo "  CF SSL result: $RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin.read().split('result:')[1] if 'result:' in sys.stdin.read() else '{}'); print('Success:', d.get('success','?'))" 2>/dev/null || echo "  $RESULT"
  ok "Cloudflare SSL set to Full"
else
  warn "CF token not found at $CF_TOKEN_FILE — fix SSL manually:"
  echo "  Cloudflare Dashboard → jpglabs.com.br → SSL/TLS → set to 'Full' (not Strict)"
fi

# ══════════════════════════════════════════════════════════════
# PHASE 8 — HEALTH CHECK
# ══════════════════════════════════════════════════════════════
log "Phase 8: Final health check"
sep
sleep 10  # Wait for Traefik to re-read routes

declare -A CHECKS=(
  ["jpglabs.com.br"]="https://jpglabs.com.br"
  ["n8n"]="https://n8n.jpglabs.com.br"
)

for name in "${!CHECKS[@]}"; do
  URL="${CHECKS[$name]}"
  CODE=$(curl -sk -o /dev/null -w "%{http_code}" "$URL" 2>/dev/null)
  if [[ "$CODE" =~ ^(200|301|302|307|308)$ ]]; then
    ok "$name → $CODE"
  else
    warn "$name → $CODE"
  fi
done

sep
echo ""
echo "  Portfolio:  https://jpglabs.com.br"
echo "  n8n:        https://n8n.jpglabs.com.br"
echo "  Mail:       jader@jpglabs.com.br (see mail-setup output above)"
echo ""
ok "VPS repair complete"
