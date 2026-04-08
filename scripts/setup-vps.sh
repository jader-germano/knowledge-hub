#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# JPGLabs VPS — First-time setup after fresh OS install
# Run from MAC: bash setup-vps.sh <root-password>
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

VPS_SSH_TARGET="${VPS_SSH_TARGET:-root@srv1443703.hstgr.cloud}"
INFRA_DIR="$(cd "$(dirname "$0")/.." && pwd)"

log() { echo "[$(date '+%H:%M:%S')] $*"; }
ok()  { echo "[$(date '+%H:%M:%S')] ✅ $*"; }

log "=== JPGLabs VPS Setup ==="
log "Target: $VPS_SSH_TARGET"

# ── 1. Wait for SSH ───────────────────────────────────────────────────────────
log "Waiting for SSH..."
for i in $(seq 1 30); do
  ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no "$VPS_SSH_TARGET" "echo ok" &>/dev/null && break
  echo "  attempt $i/30..."
  sleep 5
done
ok "SSH reachable"

# ── 2. VPS base config ────────────────────────────────────────────────────────
log "Configuring VPS..."
ssh -o StrictHostKeyChecking=no "$VPS_SSH_TARGET" bash <<'REMOTE'
set -e
# Install essentials
apt-get update -qq
apt-get install -y -qq curl wget git htop ufw

# Firewall
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 25/tcp    # SMTP
ufw allow 587/tcp   # SMTP submission
ufw allow 993/tcp   # IMAPS
ufw --force enable

# SSH hardening
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config || true
systemctl reload sshd || true

echo "✅ Base config done"
REMOTE
ok "VPS base configured"

# ── 3. Copy SSH key ───────────────────────────────────────────────────────────
log "Copying SSH key..."
ssh-copy-id -o StrictHostKeyChecking=no "$VPS_SSH_TARGET" 2>/dev/null || true
ok "SSH key installed"

# ── 4. Install k3s ───────────────────────────────────────────────────────────
log "Installing k3s..."
ssh "$VPS_SSH_TARGET" bash <<'REMOTE'
set -e
if command -v k3s &>/dev/null; then
  echo "k3s already installed: $(k3s --version)"
else
  curl -sfL https://get.k3s.io | sh -s - \
    --write-kubeconfig-mode 644 \
    --disable traefik   # app platform is Kubernetes-first, but edge cutover must remain explicit during migration
  sleep 15
  k3s kubectl get nodes
fi
REMOTE
ok "k3s installed"

# ── 5. Copy manifests ────────────────────────────────────────────────────────
log "Copying k8s manifests to VPS..."
ssh "$VPS_SSH_TARGET" "mkdir -p /k8s"
scp -r "$INFRA_DIR/k8s/"* "$VPS_SSH_TARGET:/k8s/"
ok "Manifests copied to /k8s/"

# ── 6. Secrets check ─────────────────────────────────────────────────────────
log "Checking secrets..."
if ssh "$VPS_SSH_TARGET" "test -f /k8s/02-secrets.yaml"; then
  ok "Secrets file found"
else
  log "⚠️  No 02-secrets.yaml on VPS — you must create it:"
  log "    ssh $VPS_SSH_TARGET"
  log "    cp /k8s/02-secrets-template.yaml /k8s/02-secrets.yaml"
  log "    nano /k8s/02-secrets.yaml   # fill real values"
  log ""
  log "Then re-run: ssh $VPS_SSH_TARGET 'bash /k8s/apply-all.sh'"
  exit 0
fi

# ── 7. Deploy ────────────────────────────────────────────────────────────────
log "Deploying all services..."
ssh "$VPS_SSH_TARGET" "bash /k8s/apply-all.sh"
ok "Deploy complete"

echo ""
echo "════════════════════════════════════════"
echo "  JPGLabs VPS is live"
echo "  Portfolio:  https://jpglabs.com.br"
echo "  AI API:     https://jpglabs.com.br/pi"
echo "  n8n:        https://n8n.jpglabs.com.br"
echo "════════════════════════════════════════"
