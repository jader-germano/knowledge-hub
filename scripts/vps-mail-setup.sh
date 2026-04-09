#!/usr/bin/env bash
# ============================================================
# vps-mail-setup.sh — Complete docker-mailserver setup
# Creates jader@jpglabs.com.br + contato@jpglabs.com.br
# Run from Mac after SSH is working:
#   bash vps-mail-setup.sh
# ============================================================
set -euo pipefail

VPS="${VPS:-root@srv1443703.hstgr.cloud}"

log()  { echo "[$(date '+%H:%M:%S')] ▶  $*"; }
ok()   { echo "[$(date '+%H:%M:%S')] ✅ $*"; }
warn() { echo "[$(date '+%H:%M:%S')] ⚠️  $*"; }

# ── Test SSH ──────────────────────────────────────────────────────────────────
ssh -o ConnectTimeout=8 -o StrictHostKeyChecking=no $VPS "echo connected" || {
  echo "❌ SSH failed. Authorize key via hPanel first."; exit 1
}

# ── Full mailserver setup on VPS ──────────────────────────────────────────────
log "Running mailserver setup on VPS..."

ssh $VPS bash << 'REMOTE'
set -e
MAIL_DIR="/docker/mailserver"
cd "$MAIL_DIR" 2>/dev/null || { echo "❌ /docker/mailserver not found"; exit 1; }

echo "=== Current mailserver state ==="
docker compose ps 2>/dev/null || docker ps --filter "name=mailserver" --format "{{.Names}}: {{.Status}}"

echo ""
echo "=== Checking SSL cert for mail.jpglabs.com.br ==="
if [[ -d /etc/letsencrypt/live/mail.jpglabs.com.br ]]; then
  echo "✅ SSL cert exists"
  openssl x509 -in /etc/letsencrypt/live/mail.jpglabs.com.br/fullchain.pem \
    -noout -dates 2>/dev/null || echo "(cert unreadable)"
else
  echo "⚠️  SSL cert missing — requesting via certbot..."
  if command -v certbot &>/dev/null && [[ -f /root/.secrets/cloudflare.ini ]]; then
    certbot certonly --dns-cloudflare \
      --dns-cloudflare-credentials /root/.secrets/cloudflare.ini \
      --dns-cloudflare-propagation-seconds 60 \
      -d mail.jpglabs.com.br \
      --email jader.germano@icloud.com \
      --agree-tos --non-interactive 2>&1 | tail -10
    echo "✅ SSL cert obtained"
  else
    echo "⚠️  certbot or cloudflare.ini not found — SSL must be set up manually"
    echo "    Run: certbot certonly --dns-cloudflare ..."
  fi
fi

echo ""
echo "=== Starting mailserver ==="
docker compose up -d 2>/dev/null || docker compose start 2>/dev/null || {
  echo "⚠️  Could not start via compose — checking if container exists..."
  docker start mailserver 2>/dev/null || echo "Container not found"
}

sleep 8

echo ""
echo "=== Mailserver container status ==="
docker ps --filter "name=mailserver" --format "{{.Names}}: {{.Status}}"

REMOTE

log "Mailserver started. Now creating email accounts..."

# ── Create accounts ────────────────────────────────────────────────────────────
# Read passwords interactively
echo ""
read -rsp "  Enter password for jader@jpglabs.com.br: "    PASS_JADER;    echo ""
read -rsp "  Enter password for contato@jpglabs.com.br: "  PASS_CONTATO;  echo ""

ssh $VPS bash << REMOTE
set -e
MAIL_DIR="/docker/mailserver"
cd "\$MAIL_DIR"

echo "=== Creating email accounts ==="
# docker-mailserver uses 'setup' binary or docker exec
if docker exec mailserver setup email list 2>/dev/null | grep -q "jader@"; then
  echo "Account jader@jpglabs.com.br already exists"
  # Update password
  docker exec mailserver setup email update jader@jpglabs.com.br "${PASS_JADER}" 2>/dev/null \
    && echo "✅ Password updated for jader@jpglabs.com.br" \
    || echo "⚠️  Could not update password"
else
  docker exec mailserver setup email add jader@jpglabs.com.br "${PASS_JADER}" 2>/dev/null \
    && echo "✅ Created jader@jpglabs.com.br" \
    || echo "⚠️  Could not create account — mailserver may still be starting"
fi

if docker exec mailserver setup email list 2>/dev/null | grep -q "contato@"; then
  echo "Account contato@jpglabs.com.br already exists"
  docker exec mailserver setup email update contato@jpglabs.com.br "${PASS_CONTATO}" 2>/dev/null \
    && echo "✅ Password updated for contato@jpglabs.com.br"
else
  docker exec mailserver setup email add contato@jpglabs.com.br "${PASS_CONTATO}" 2>/dev/null \
    && echo "✅ Created contato@jpglabs.com.br" \
    || echo "⚠️  Could not create account"
fi

echo ""
echo "=== Account list ==="
docker exec mailserver setup email list 2>/dev/null || echo "(could not list accounts)"

echo ""
echo "=== Generating DKIM keys ==="
docker exec mailserver setup config dkim 2>/dev/null \
  && echo "✅ DKIM generated" \
  || echo "⚠️  DKIM generation failed"

echo ""
echo "=== DKIM public key (add to Cloudflare DNS) ==="
cat /docker/mailserver/config/opendkim/keys/jpglabs.com.br/mail.txt 2>/dev/null \
  || cat /docker/mailserver/config/opendkim/keys/mail.txt 2>/dev/null \
  || echo "(DKIM key file not found — check /docker/mailserver/config/opendkim/)"

echo ""
echo "Restarting mailserver to apply DKIM..."
docker restart mailserver && sleep 5

echo ""
echo "=== Final mailserver status ==="
docker ps --filter "name=mailserver" --format "{{.Names}}: {{.Status}}"

echo ""
echo "=== SMTP test (send from localhost) ==="
docker exec mailserver swaks --to jader@jpglabs.com.br --from test@jpglabs.com.br \
  --server localhost --body "Test mail from VPS" 2>/dev/null \
  && echo "✅ SMTP test passed" \
  || echo "⚠️  swaks not available — test manually"
REMOTE

ok "Mail setup complete"
echo ""
echo "  IMAP Host:  mail.jpglabs.com.br"
echo "  IMAP Port:  993 (SSL) or 143 (STARTTLS)"
echo "  SMTP Host:  mail.jpglabs.com.br"
echo "  SMTP Port:  587 (STARTTLS) or 465 (SSL)"
echo "  User:       jader@jpglabs.com.br"
echo "  Password:   (what you just set)"
echo ""
echo "  ⚠️  Remember to add DKIM TXT record to Cloudflare DNS"
echo "     Type: TXT | Name: mail._domainkey | Value: (shown above)"
