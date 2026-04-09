# JPGLabs Current Deploy Truth
> Canonical operational note — use this before changing any ingress, DNS or deployment path.
> Date: 2026-03-12

## Why this file exists
The repository accumulated conflicting assumptions about Docker versus Kubernetes ownership.
That drift produced operational waste and contributed to the current outage state.

## Current Reality
### Legacy live runtime
The VPS is still carrying legacy Docker state:
- Docker Traefik on ports 80/443
- Docker n8n
- a broken standalone portfolio container attempt
- leftover Open WebUI container

This is **not** the approved target platform.

## Approved Operating Rule
### App services
All app services are now **Kubernetes-first**.
That includes future production ownership for:
- portfolio-related services
- n8n
- AI API / pi-local-app
- knowledge-hub
- supporting AI workloads where appropriate

### Standalone exception
- `mailserver` remains standalone for now

### Explicitly removed from target platform
- Open WebUI
- `chat.jpglabs.com.br`
- any new standalone Docker app-service deployment path

## Current Hostname Situation
| Hostname | Current state | Intended future |
|---|---|---|
| `jpglabs.com.br` | broken legacy path / root-domain 404 | Kubernetes-managed app entrypoint after final portfolio owner decision |
| `www.jpglabs.com.br` | same as root domain | Kubernetes-managed alias |
| `n8n.jpglabs.com.br` | Docker n8n currently alive but route broken | Kubernetes-managed n8n |
| `api.jpglabs.com.br` | not active / DNS missing | Kubernetes-managed app/API lane later |
| `hub.jpglabs.com.br` | planned app lane | Kubernetes-managed knowledge hub |
| `mail.jpglabs.com.br` | standalone exception | standalone mail lane |

## Known Current Facts
- Cloudflare SSL mode was corrected from Strict to Full.
- Portfolio legacy container failed due to wrong image architecture (`exec format error`).
- n8n app process is alive, but its public custom-domain route is still broken.
- Traefik is wasting ACME attempts on `api.jpglabs.com.br`, which currently has no DNS record.

## Immediate Platform Guidance
1. Stop extending the legacy standalone Docker app path.
2. Remove Open WebUI from the intended platform and docs.
3. Use the current VPS only as a migration source and temporary diagnostic environment.
4. Rebuild the app platform with Kubernetes as the source of truth.

## Still Pending
The only major unresolved app-platform question is the final root-domain web owner inside Kubernetes:
- `jpglabs-portfolio-frontend`
- or an alternative integrated web edge

Do not fake resolution of that point in manifests until it is explicit.
