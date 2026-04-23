# openclaude-hub Project Context

## Nicho

- web UI gateway multi-provider para CLIs de coding
- camada de chat autenticada do stack JPGLabs
- absorveu funcionalidade do legado `knowledge-hub-app` (descontinuado em 2026-04-16)

## Identidade E Rebrand

- nome de código histórico: `openclaude-hub`
- nome visual atual: `Axis`
- rename físico do repositório no GitHub e DNS do `chat.jpglabs.com.br` são ações manuais pendentes do owner; por enquanto, path e serviço seguem `openclaude-hub`

## Stack

- **Frontend:** React 19 + Vite (bun build) + TypeScript
- **Backend:** Express 5 (Node.js/Bun) + Drizzle ORM + Postgres (Supabase, via PgBouncer porta 6543)
- **Auth:** Supabase custom auth (JWT + refresh com pepper HMAC), fallback GitHub OAuth legacy via `AUTH_PROVIDER`
- **Streaming:** gRPC para adapters de provider, WebSocket/SSE para o cliente
- **Providers suportados:** OpenAI-compatible (Ollama, Gemini, OpenRouter, LM Studio) e Anthropic
- **Design system:** `@jpglabs/cartesian-red` (vendored local de `../jpglabs-portfolio/packages/cartesian-red/`)
- **Tipografia canônica:** Fraunces (display), IBM Plex Sans (body), JetBrains Mono (mono)

## Arquitetura

- `server/index.ts` — entrypoint HTTP + WebSocket + gRPC
- `server/app.ts` — Express setup + route mounting
- `server/{routes,controllers,services}` — Clean Architecture (SOLID)
- `server/adapters/{grpc.ts,cli.ts}` — bridges para os providers
- `server/grpc/{standalone-server.ts,anthropic-stream.ts}` — server gRPC + adapter SSE Anthropic
- `server/proto/openclaude.proto` — proto definition
- `client/src/` — SPA React (dark theme, estilo ChatGPT)
- `tests/{domain,behavior,contracts,*.test.ts}` — organização BDD/TDD/DDD

## Quality Gates

- pre-commit hook: lint → typecheck → tests (todos devem passar)
- ESLint com typescript-eslint strict rules
- suite de testes com `bun test --max-concurrency=1`; último sinal conhecido `102 tests, 0 failures`

## Deploy

- VPS com `systemd openclaude-hub.service`
- Caddy reverse proxy + auto-TLS via Cloudflare DNS
- processo único Node serve HTTP (`:3100`) + gRPC (`:50051`)
- site canônico: `https://chat.jpglabs.com.br`
- release mais recente observada: `v0.6.19` (bump em `5358d2a`)
- CI recente rota deploy via Tailscale userspace (SOCKS5) pelo estágio de deploy

## Sinal Atual

- branch ativa: `main`
- trilha recente consolidou `feat/shared-auth-realm-s1a` (Supabase client-side OAuth + `/auth/exchange` + refresh interceptor) com merge em `4193a17`
- vendoring do `@jpglabs/cartesian-red` como workspace local foi a última mudança estrutural antes da rodada de patch releases
- gap documental ativo: este `PROJECT_CONTEXT.md` nasceu em 2026-04-23 após migração do repo para dentro de `jpglabs/`; `ROADMAP.md` e `sessions/` ainda não foram materializados

## Env E Segredos

Template canônico em `/Users/philipegermano/code/jpglabs/openclaude-hub/.env.example`.

Variáveis críticas:

- `AUTH_PROVIDER` — `supabase` (padrão) ou `github` (legacy)
- `DATABASE_URL` — Postgres Supabase via PgBouncer (porta `6543`, não `5432`)
- `JWT_SECRET_CURRENT` / `JWT_SECRET_PREVIOUS` — segredo atual e anterior (rotação)
- `REFRESH_PEPPER_V1` — HMAC pepper para refresh tokens (S1A)
- `SUPABASE_URL` / `SUPABASE_STAGING_URL`
- `COOKIE_DOMAIN` — `.jpglabs.com.br` em prod (cross-subdomain)
- `SMTP_HOST/PORT/USER/PASS` — SMTP jpglabs
- `GITHUB_CLIENT_ID` / `GITHUB_CLIENT_SECRET` / `ALLOWED_GITHUB_USERS` — apenas quando `AUTH_PROVIDER=github`

Secrets em produção vivem em `/opt/openclaude-hub/.env` na VPS (nunca versionado).

## Repo Real

- `/Users/philipegermano/code/jpglabs/openclaude-hub`
- migrado para `jpglabs/` em 2026-04-22/23 (antes: `/Users/philipegermano/code/openclaude-hub`)
- sidecars históricos em `docs/memory/events/` e reports em `docs/projects/docs/sessions/daily-technical-closure/` referenciam o path antigo — isso é fato histórico preservado, não drift
