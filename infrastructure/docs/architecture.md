# JPGLabs Infrastructure — Approved Platform Baseline
> Owner: Jader Philipe Germano | Date: 2026-03-12

## Approved Direction
The approved production direction is now:

- **Kubernetes-first for app services**
- **CI/CD-ready deployment model**
- **No standalone Docker app services as the target runtime**
- **Mail remains standalone for now**
- **Open WebUI is removed from the intended platform**

This document describes the approved baseline that future infrastructure work must follow.

## Current Legacy Reality
The current VPS still contains legacy Docker runtime drift from an older model:
- Docker Traefik still owns public ports 80/443
- legacy n8n is still running in Docker
- a broken standalone portfolio container was attempted and failed with wrong-architecture image startup
- Open WebUI still exists as a leftover container, but it is **not part of the approved future platform**

Treat that runtime as migration residue, not as the target architecture.

## Approved Target Architecture

```text
Internet
  ↓
Cloudflare (DNS / proxy / TLS edge)
  ↓
Kubernetes ingress / edge
  ↓
App services on k3s
  ├── portfolio frontend / web edge (final owner still to be confirmed)
  ├── portfolio backend / BFF
  ├── n8n
  ├── pi-local-app / AI API
  ├── knowledge-hub
  └── supporting AI services such as Ollama where appropriate

Separate standalone lane:
  └── mailserver
```

## Platform Rules
1. App services belong to Kubernetes.
2. Standalone Docker is allowed only as a migration residue or for the standalone mail lane.
3. Do not add new public app services as standalone containers.
4. Do not keep mixed ingress ownership as a permanent design.
5. CI/CD must target image build + registry + Kubernetes rollout.

## Portfolio Split — still true
### Frontend
- Repo: `jpglabs-portfolio-frontend`
- Stack: Vite + React + Nginx

### Backend / BFF
- Repo: `jpglabs-portfolio-backend`
- Stack:Nest.js + Supabase + NextAuth

## Still Pending
The only intentionally unresolved architecture point is:

### Who owns the final production root domain in Kubernetes?
One of these must eventually become the final owner of `jpglabs.com.br`:
- `jpglabs-portfolio-frontend`
- a different integrated web edge built around theNest.js lane

Until that is explicitly decided, do not force a blind cutover of the root-domain ingress.

## Removed from Target Scope
These are not part of the intended rebuilt platform:
- Open WebUI public exposure
- `chat.jpglabs.com.br`
- standalone Docker portfolio runtime

## Mail Exception
Mail remains standalone for now because it is operationally different from the app platform and should not block the Kubernetes-first app rebuild.
