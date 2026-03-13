# Session Memory - 2026-03-09 - JPGLabs Portfolio Route + Access Control

## Context
Route and access-control refactor for `~/code/jpglabs-portfolio` to align local and Docker behavior.

## Key Decisions
- Centralized canonical routes in `src/config/routes.ts`.
- Kept current visual style and components; no redesign.
- Enforced role-based route protection:
  - `ADMIN`: full access (guardian, upsell, detailed service pages).
  - `USER_CONSULTANT`: access to instances with sanitized data.
  - `PUBLIC`: only public routes.
- Implemented legacy redirects:
  - `/assets -> /downloads`
  - `/gardian -> /guardian`

## Product/Service Structure
- Added/confirmed product catalog with dedicated detail routes:
  - `ai-toolkit-v3`
  - `k8s-blueprint`
  - `traefik-edge-proxy`
  - `local-llm-models`
  - `llm-infrastructure-model`
- Service detail route added: `/dashboard/instances/:serviceSlug` with admin-only pod-level details.

## Docker Parity Fix
- Added edge redirects in `nginx.conf` for legacy paths.
- Important Docker fix: preserve host+port in redirects using `$scheme://$http_host/...`.
  - This avoids redirecting from `:8080` to port 80 during local Docker checks.

## Verification Summary
- `npm run build`: pass.
- `npm run lint`: pass.
- `docker compose up -d --build`: pass.
- Browser checks (Playwright via `host.docker.internal`):
  - Public routes: pass.
  - Role-based redirects: pass.
  - Consultant sanitized views: pass.
  - Admin pod-level detail visibility: pass.
  - `/assets` and `/gardian` legacy redirects: pass after nginx host+port fix.

## Commits Recorded
- `4d3748a` chore: checkpoint before route and access-control refactor
- `849f361` chore: checkpoint ongoing route and access-control refactor
- `bd4f7f9` fix(nginx): preserve host+port on legacy redirects
