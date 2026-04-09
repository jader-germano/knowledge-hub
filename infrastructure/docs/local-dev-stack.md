# Local Development Stack

This local ops lane is the single control surface for the Mac development ground.

The canonical lane naming and endpoint registry lives in `~/code/jpglabs/docs/infrastructure/config/runtime-lanes.yml`.

## Managed services

| Service | Repo | Mode | Local URL / Port |
|---|---|---|---|
| Portfolio Frontend | `~/code/jpglabs/portfolio-frontend` | Vite dev | `http://localhost:8082` |
| Portfolio Backend | `~/code/jpglabs/portfolio-backend` | Next.js dev | `http://localhost:3000` |
| Knowledge Hub / Finance App | `~/code/jpglabs/knowledge-hub-app` | Next.js dev (UI + API) | `http://localhost:3001` |
| GoBarber DB | `~/code/pessoal/backend-goBarber` | Docker Compose `db` only | `localhost:5432` |
| GoBarber Backend | `~/code/pessoal/backend-goBarber` | Node/TS dev | `http://localhost:3333` |
| GoBarber Frontend | `~/code/pessoal/frontend-gobarber` | Vite dev | `http://localhost:8084` |

## Why this shape

- Portfolio remains split into frontend and backend/BFF.
- Knowledge Hub stays as one deployable because the repo contains both frontend and backend routes together.
- GoBarber uses local Docker only for Postgres. The API and frontend run in dev mode for easier debugging.
- SMTP is intentionally excluded from local development.

## Control script

```bash
bash ~/code/jpglabs/docs/scripts/infrastructure/local-dev-stack.sh status
bash ~/code/jpglabs/docs/scripts/infrastructure/local-dev-stack.sh start all
bash ~/code/jpglabs/docs/scripts/infrastructure/local-dev-stack.sh stop all
bash ~/code/jpglabs/docs/scripts/infrastructure/local-dev-stack.sh restart hub
bash ~/code/jpglabs/docs/scripts/infrastructure/local-dev-stack.sh logs portfolio-be
bash ~/code/jpglabs/docs/scripts/infrastructure/local-dev-stack.sh prune
```

## Logs and runtime state

- Logs: `~/code/jpglabs/docs/infrastructure/local-dev/logs/`
- PID files: `~/code/jpglabs/docs/infrastructure/local-dev/run/`

This is the base needed for guard/restart behavior:
- status checks
- tail logs
- controlled restarts
- Docker prune hooks

## Bootstrap behavior

The bootstrap helper creates `jpglabs-portfolio-backend/.env.local` if it does not exist.
It reuses local knowledge-hub Supabase values when available and generates a fresh `NEXTAUTH_SECRET`.

```bash
bash ~/code/jpglabs/docs/scripts/infrastructure/local-dev-bootstrap.sh
```

## Kubernetes visibility

The control script exposes Kubernetes helper commands for Docker Desktop Kubernetes when available:

```bash
bash ~/code/jpglabs/docs/scripts/infrastructure/local-dev-stack.sh k8s-status
bash ~/code/jpglabs/docs/scripts/infrastructure/local-dev-stack.sh k8s-logs jpglabs knowledge-hub
bash ~/code/jpglabs/docs/scripts/infrastructure/local-dev-stack.sh k8s-restart jpglabs knowledge-hub
bash ~/code/jpglabs/docs/scripts/infrastructure/local-dev-stack.sh k8s-prune
```

If Docker Desktop Kubernetes is not enabled or not the current context, the script exits cleanly and says so.

## Operational stance

This local lane is for:
- development verification
- log tracing
- safe restarts
- health observation
- cache/image pruning

This local lane is not the production or release control plane. Test, release, and prod remain on the VPS.
