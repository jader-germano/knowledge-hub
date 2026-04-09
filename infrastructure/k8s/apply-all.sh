#!/usr/bin/env bash
# AwesomePie VPS — One-command k8s deploy
# Run from VPS: bash apply-all.sh
# Run from Mac (SSH): ssh root@187.77.227.151 "bash -s" < apply-all.sh
set -euo pipefail

K8S_DIR="$(cd "$(dirname "$0")" && pwd)"
KUBECTL="kubectl"

log() { echo "[$(date '+%H:%M:%S')] $*"; }
ok()  { echo "[$(date '+%H:%M:%S')] ✅ $*"; }
err() { echo "[$(date '+%H:%M:%S')] ❌ $*" >&2; }

log "=== JPGLabs k8s deploy ==="

# ── Preflight ─────────────────────────────────────────────────────────────
if ! command -v kubectl &>/dev/null; then
  # k3s provides kubectl via symlink
  KUBECTL="k3s kubectl"
fi

$KUBECTL cluster-info &>/dev/null || { err "kubectl not reachable"; exit 1; }
ok "Cluster reachable"

# ── Disk check (VPS history: 100% full) ──────────────────────────────────
DISK_USE=$(df / --output=pcent | tail -1 | tr -d '% ')
log "Disk usage: ${DISK_USE}%"
if [[ "$DISK_USE" -ge 85 ]]; then
  log "⚠️  Disk ≥85% — running docker/containerd prune before deploy…"
  docker system prune -f 2>/dev/null || crictl rmi --prune 2>/dev/null || true
  ok "Prune done — recheck: $(df / --output=pcent | tail -1 | tr -d ' ')"
fi

# ── Secrets check ─────────────────────────────────────────────────────────
if [[ ! -f "$K8S_DIR/02-secrets.yaml" ]]; then
  err "02-secrets.yaml not found — copy from 02-secrets-template.yaml and fill values"
  exit 1
fi

# ── Apply in order ────────────────────────────────────────────────────────
apply() {
  log "Applying $1..."
  $KUBECTL apply -f "$1" && ok "$1"
}

apply "$K8S_DIR/00-namespaces.yaml"
apply "$K8S_DIR/01-storage.yaml"
apply "$K8S_DIR/02-secrets.yaml"
apply "$K8S_DIR/03-configmaps.yaml"
apply "$K8S_DIR/traefik/tls-config.yaml"

# Services
# Approved platform baseline:
# - App services are Kubernetes-first
# - Mail remains standalone for now
# - Open WebUI is intentionally removed from the target platform
# Portfolio root-domain ownership is still pending final cutover between
# `jpglabs-portfolio-frontend` and the Next.js backend lane, so the k8s
# portfolio manifest stays out of the auto-apply path until that decision is explicit.
for svc in ollama pi-local-app n8n knowledge-hub; do
  [[ -f "$K8S_DIR/services/$svc.yaml" ]] && apply "$K8S_DIR/services/$svc.yaml"
done

# ── Wait for critical pods ─────────────────────────────────────────────────
log "Waiting for Ollama..."
$KUBECTL rollout status deployment/ollama -n ai-services --timeout=120s && ok "Ollama ready"

log "Waiting for pi-local-app..."
$KUBECTL rollout status deployment/pi-local-app -n ai-services --timeout=60s && ok "pi-local-app ready"

# ── Pull models (if job doesn't exist yet) ────────────────────────────────
if ! $KUBECTL get job ollama-pull-models -n ai-services &>/dev/null; then
  log "Pulling AI models (this takes a while)..."
  apply "$K8S_DIR/jobs/ollama-pull-models.yaml"
  $KUBECTL wait --for=condition=complete job/ollama-pull-models -n ai-services --timeout=600s \
    && ok "Models pulled" || log "⚠️ Model pull timed out — check: kubectl logs -n ai-services job/ollama-pull-models"
fi

# ── Summary ───────────────────────────────────────────────────────────────
echo ""
echo "=== Deployed Services ==="
$KUBECTL get pods -A --field-selector=status.phase=Running \
  --no-headers | awk '{print $1, $2, $4}'

echo ""
echo "=== Ingress Endpoints ==="
$KUBECTL get ingress -A --no-headers | awk '{print $3, "→", $2, "(ns:"$1")"}'

echo ""
ok "Deploy complete — JPGLabs is live"
echo "  Portfolio:  https://jpglabs.com.br"
echo "  AI API:     https://api.jpglabs.com.br"
echo "  n8n:        https://n8n.jpglabs.com.br"
echo "  Hub:        https://hub.jpglabs.com.br"
