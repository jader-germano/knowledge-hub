# JPGLabs Kubernetes-First Migration Plan
> Approved model: app services on Kubernetes, mail standalone.
> Open WebUI is out of scope.

## Goals
- Rebuild the app platform around Kubernetes
- Prepare for CI/CD-friendly rollout
- Eliminate mixed app-runtime ownership
- Keep mail isolated so it does not block app delivery

## Target Runtime Split
### Kubernetes app services
- portfolio frontend or final web edge (pending explicit owner decision)
- portfolio backend / BFF
- n8n
- pi-local-app / AI API
- knowledge-hub
- Ollama or supporting AI workloads as needed

### Standalone service
- mailserver

## Legacy Runtime to Retire
- broken standalone `jpglabs-portfolio` container
- public Open WebUI exposure
- `chat.jpglabs.com.br`
- ad-hoc standalone Docker app service deployment flow

## Migration Sequence
### Phase 1 — Sanitize source of truth
- Remove Open WebUI from the intended platform baseline
- Remove chat references from active infra docs/scripts
- Freeze standalone Docker app-service expansion
- Keep mail as standalone exception

### Phase 2 — Inventory migration source
- Export n8n data/workflows if needed
- Inspect current k3s health
- Verify `/k8s` manifests and secrets presence
- Identify any missing DNS records or stale ACME routes

### Phase 3 — Decide root-domain web owner
Explicitly choose who owns `jpglabs.com.br` in Kubernetes:
- `jpglabs-portfolio-frontend`
- or another integrated web edge

This must be decided before final production ingress cutover.

### Phase 4 — Rebuild app services on k3s
- ingress controller / edge
- n8n
- AI API lane
- knowledge-hub
- portfolio lane after root-domain decision

### Phase 5 — CI/CD alignment
- build images in CI for the target architecture
- push to registry
- deploy via Kubernetes manifests or Helm/Kustomize path
- add rollout/health validation

## Immediate VPS Actions
- remove broken `jpglabs-portfolio` crash loop
- remove Open WebUI from the future app baseline
- stop invalid `api.jpglabs.com.br` ACME noise until DNS exists
- keep n8n available only as migration source until Kubernetes route is ready

## Non-Negotiable Rules
1. No new standalone Docker app services.
2. No public Open WebUI lane.
3. No mixed permanent ingress ownership.
4. No architecture-sensitive image build on the wrong CPU target for VPS runtime.
5. CI/CD must target Kubernetes deployment for app services.
