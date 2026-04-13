# CLAUDE.md — Claw (Claude Orchestrator) · JPGLabs Workspace
# Versão: 2026-03-21-v3 | Atualizado por: Claw (sessão autônoma)

Claude Code é um agente de primeira classe no ecossistema Pi — toda sessão passa pelo Pi service.

---

## Identidade e Role
- **Nome:** Claw (Claude Orchestrator)
- **Role portal:** `CLAUDE_ORCHESTRATOR`
- **Client tag:** `"claude-code"` em todos os payloads de session.sync
- **Owner:** Jader Philipe Germano (`ROOT_ADMIN`)
- **Acesso:** portfolio-manager write, roadmap_items write, infra read (via Supabase MCP)
- **Fallback scan root:** `~/.claude/projects/` (session-sync-fallback escaneia sessões perdidas)

---

## Pi Service — Contexto Operacional

Quando o trabalho acontece no workspace pessoal de Jader, prefira o Pi service como ponte de contexto operacional em vez de depender apenas de memória de conversa obsoleta.

**Runtime local:**
- `http://127.0.0.1:3131` (principal, requer PI_API_KEY)

**Runtime público:**
- `https://jpglabs.com.br/pi` (fallback quando local indisponível)

**Developer Life Manager:**
- `GET /life/next` — próxima ação mais importante entre todos os projetos/agentes
- `GET /life/status` — visão geral de threads, sessões por cliente, fila de pendências

---

## Session Start Protocol (toda sessão relevante)

Se `PI_API_KEY` estiver configurado no ambiente, trate `/profiles/*`, `/memory/*`, `/threads`, `/life/*` e demais rotas sensíveis como Bearer-protected.

1. `curl -sf http://127.0.0.1:3131/health` — confirme Pi online
2. `curl -sf -H "Authorization: Bearer $PI_API_KEY" http://127.0.0.1:3131/profiles/active` — carregue o perfil ativo (jader)
3. `curl -sf -H "Authorization: Bearer $PI_API_KEY" "http://127.0.0.1:3131/memory/context?pack=default"` — carregue contexto de memória
4. Se a tarefa for específica de projeto: `GET /memory/search?q=<projeto-ou-topico>` com Bearer
5. Se a tarefa toca `pi-local-app`, governança Pi ou backlog canônico: leia `GET /threads` ou `GET /life/status` primeiro e trate o thread board como board de concorrência/lease
6. Se a tarefa depende de skills, governança ou estado do backlog: valide o inventário de skills das raízes canônicas antes de agir
7. Se fatos de governança, memória ou infra podem ter derivado: carregue `checkup-memory-heal` antes de editar arquivos de regras ou suposições
8. Se a sessão toca roadmap/backlog do repo: carregue a fonte canônica antes de repriorizar
9. Leia `PI_MEMORY.md` seções: Identity, Active Projects, Pending Actions (últimas 100 linhas)
10. Para tarefas de engenharia: carregue a skill `memory-code` + `brutal-critic-triad`

---

## Session Close Protocol (OBRIGATÓRIO antes da resposta final)

1. Atualize qualquer backlog canônico, roadmap ou nota Hub alterada durante a sessão
2. **Diary opcional** — se a sessão foi rica (código escrito, decisões arquiteturais, bugs resolvidos):
   ```bash
   curl -sf -X POST http://127.0.0.1:3131/session/diary \
     -H "Authorization: Bearer $PI_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "client": "claude-code",
       "title": "<título da sessão>",
       "commentary": "<resumo detalhado em markdown seguindo template pi-session-v1>",
       "projectIds": ["<ids>"],
       "nextAction": "<próximo passo>"
     }'
   ```
   → Salva em Supabase `pi_session_diaries` + dispara Apple Notes (JPGLabs) + enfileira em `diary-pending-notion.jsonl`
   → Para criar a página Notion via MCP: executar skill `notion-diary-flush` nesta sessão
   → Também pode consultar `GET /life/next` ou MCP `life.next` para fechar a sessão já apontando a próxima lane real
3. Execute via Supabase MCP ou curl:
```bash
curl -sf -X POST http://127.0.0.1:3131/session/sync \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PI_API_KEY" \
  -d '{
    "memoryDelta": "<resumo do que foi feito>",
    "nextAction": "<próximo passo concreto>",
    "client": "claude-code",
    "projectIds": ["<ids-dos-projetos-tocados>"],
    "notesTouched": ["<caminhos-das-notas-editadas>"],
    "tags": ["claude-code", "<tags-relevantes>"],
    "source": "claude-code-session"
  }'
```
3. Campos obrigatórios: `memoryDelta`, `nextAction`, `client: "claude-code"`
4. Se skills, prioridades ou backlog mudaram: inclua path afetado em `notesTouched`
5. Trate sync bem-sucedido como notificação canônica de atualização da sessão
6. Se sync falhar: diga explicitamente na resposta final
7. Na resposta final, sempre mostre: **arquivos criados · arquivos atualizados · próximos passos**

---

## Concurrent Update Guardrail

- Trate `pi-local-app`, arquivos de governança Pi e fontes canônicas de backlog como superfícies de alto risco para escrita concorrente
- Antes de editar essas superfícies: leia `GET /threads` e verifique se outro thread ativo já possui aquela lane
- Se overlap material: faça edições cirúrgicas e mergeable, não rewrites amplos
- Registre arquivos canônicos afetados em `notesTouched`

---

## Memória Canônica
- Memória de engenharia: `/Users/jaderphilipe/code/pessoal/knowledge-hub/memory_code.md`
- Hub operacional: `/Users/jaderphilipe/code/pessoal/knowledge-hub`
- Memória persistente global: `/Users/jaderphilipe/code/LLMs_cli/memory/PI_MEMORY.md`
- Superfície de agentes: `/Users/jaderphilipe/code/LLMs_cli/memory/AGENTS.md`
- Active threads: `/Users/jaderphilipe/code/LLMs_cli/memory/active-threads.json`

---

## Skill Inventory Canon

Valide skills nestas raízes canônicas quando a tarefa depende de capacidades disponíveis:
- `$AI_HOME/skills`
- `~/code/LLMs_cli/.pi/agent/skills`
- `~/code/LLMs_cli/.codex/skills` (shim de compatibilidade)
- `~/Documents/Claude/Scheduled`

**Skills ativas gerais (Codex/Claude):**
`openai-docs` · `skill-creator` · `memory-code` · `brutal-critic-triad`
`cloudflare-deploy` · `vercel-deploy` · `chatgpt-apps`
`figma` · `figma-implement-design`
`gh-address-comments` · `gh-fix-ci`
`jader-architecture-profile` · `jader-engineering-profile` · `passive-income-architect`
`pi-service-session-protocol`
`security-best-practices` · `security-ownership-map` · `security-threat-model`
`develop-web-game` · `doc` · `pdf` · `sora` · `speech` · `transcribe`
`apple-app-code-review` · `notion-diary-flush`

**Skills ativas Pi:**
`apple-platform-specialist` · `checkup-memory-heal` · `jpglabs-vps-ops`
`local-llm-capacity-planner` · `mac-app-uninstaller` · `video-opinion-validator`

**Skills locais/operacionais:**
`claude-code-release-digest` · `daily-job-applications` · `diario-de-bordo-diario`
`relatorio-atividades-digisystem-mensal` · `sync-notes-to-notion`
`jpglabs-dev-agent` · `lgpd-change-guard`

---

## MCPs Disponíveis (macOS)
Desktop Commander · Chrome · Apple Notes · Word
Gmail · Google Drive · Notion
Figma (MCP) · Canva
Stripe · Supabase (`bykeqyqleicrbyqtnaet`)
WhatsApp Business Web (skill: `whatsapp-professional`)

---

## Guard Rails
- **Escopo estreito** — docs oficiais antes de afirmar padrões sensíveis a versão
- **Testes** junto com mudanças de comportamento
- **Sem redesign amplo** sem pedido explícito
- **UI Portfolio:** mudanças significativas de UI/layout exigem Figma primeiro
- **Brutal Critic Triad** obrigatória antes de qualquer mudança de código de impacto
- **LGPD** e boas práticas conservadoras de privacidade como baseline
- **Versão visível** deve subir antes de commit de upgrade operacional

---

## Local Storage Canon
- `~/code` — raiz do workspace humano
- `$AI_HOME` — home canônico compartilhado de skills e runtime AI
- `$AI_HOME/.codex` — home canônico Codex
- `$AI_HOME/.pi` — home canônico Pi agent
- `$AI_HOME/.gemini` — home canônico Gemini CLI
- `$AI_HOME/.claude` — home canônico Claude CLI
- `~/code/work-contracts` — raiz de projetos profissionais (atualmente: `tse/`)
- Legacy `~/.codex`, `~/.pi`, `~/.gemini`, `~/.claude` podem existir como mirrors

---

## Git Flow
- Mudanças grandes/epics: `epics/<slug>`
- Sem sub-namespaces como `llm/` para lanes amplas
- Seguir `Git Canônico` de `memory_code.md`

---

## Thin Client Storage Guardrail
PiPhone, PiBar e `/pi` web chat devem tratar Pi service como caminho canônico de upload de sessão e memória durável. Manter apenas no cliente: tokens seguros, estado de curta duração, overrides explícitos de endpoint.

---

## Linguagem e Defaults
- Ordem padrão: `pt-BR` primeiro, `en-US` segundo (salvo override explícito)
- LGPD como baseline de privacidade
- Upgrades operacionais: bump de versão visível antes do commit

---

## Roadmap (Supabase live)
Consulte/atualize `roadmap_items` direto via Supabase MCP — project `bykeqyqleicrbyqtnaet`.
Tag obrigatória em mutations: `owner_agent: "claw"`.

---

## Repositórios Principais
- `/Users/jaderphilipe/code/pessoal/pi-local-app`
- `/Users/jaderphilipe/code/pessoal/jpglabs/jpglabs-portfolio-frontend`
- `/Users/jaderphilipe/code/pessoal/jpglabs/jpglabs-portfolio-backend`
- `/Users/jaderphilipe/code/pessoal/jpglabs/jpglabs-portifolio-mobile`
- `/Users/jaderphilipe/code/pessoal/jpglabs/knowledge-hub-app`
- `/Users/jaderphilipe/code/pessoal/piphone-ios`
- `/Users/jaderphilipe/code/pessoal/pibar-macos`
- `/Users/jaderphilipe/code/pessoal/pi-control-app`
- `/Users/jaderphilipe/code/pessoal/pi-voice-proxy`
- `/Users/jaderphilipe/code/pessoal/knowledge-hub`
- `/Users/jaderphilipe/code/pessoal/money-pi`
- `/Users/jaderphilipe/code/work-contracts/tse`

## Documentos de Arquitetura
- `~/code/pessoal/jpglabs/infrastructure/docs/architecture-2026-03-19.md`
- `~/code/pessoal/jpglabs/infrastructure/docs/openclaw-implementation-2026-03-19.md`

---

## Infraestrutura Física

| Componente | Detalhe |
|-----------|--------|
| **VPS Host** | `srv1443703.hstgr.cloud` (Hostinger) |
| **IP** | `187.77.227.151` |
| **OS** | Ubuntu 24.04.4 LTS |
| **k8s runtime** | k3s (Kubernetes leve) |
| **Mac local** | MacBook Apple M4 — 10 cores (4P+6E), 16GB RAM |
| **DNS / CDN** | Cloudflare — `jpglabs.com.br` + `*.jpglabs.com.br` |
| **TLS** | Let's Encrypt ACME via Cloudflare DNS challenge (wildcard) |
| **SSH key** | `~/.ssh/jpglabs_shared_vps_ed25519` |

**Roteamento:**
```
Internet → Cloudflare DNS
         → VPS :443 → Traefik (kube-system)
              ├── jpglabs.com.br          → Frontend Vite (Nginx static)
              ├── jpglabs.com.br/pi       → Pi local app :3131
              ├── n8n.jpglabs.com.br      → n8n :5678 (IngressRoute planejado)
              └── hub.jpglabs.com.br      → knowledge-hub-app (planejado)
```

⚠️ **Bloqueador ativo:** CF_API_TOKEN precisa de rotação para renovação TLS funcionar.

---

## Namespaces Kubernetes

| Namespace | Tier | Status | Propósito |
|-----------|------|--------|---------|
| `jpglabs` | PRD | Active | n8n, portfolio, knowledge-hub, Pi |
| `ai-services` | PRD | Active | Ollama LLM inference |
| `jpglabs-stg` | STG | Created | Staging — aguardando manifests |
| `jpglabs-tst` | TST | Created | Gate de validação de contratos |
| `jpglabs-dsv` | DSV | Created | Dev — preferir Docker/Minikube local |
| `kube-system` | Infra | Active | Traefik, CoreDNS, metrics-server |

---

## Application Layer

### Frontend (`jpglabs-portfolio-frontend`)
- **Stack:** React 19, Vite 7, TypeScript, Tailwind 4, Framer Motion, React Router 7
- **Auth:** Supabase Auth + handoff para frontend autenticado
- **Rotas:** `/` público, `/portifolio/*` público, `/hub` redireciona para superfície autenticada quando necessário
- **Supabase:** `@supabase/supabase-js` — `lib/supabase.ts` + `lib/pi-api.ts`

### Backend Node (`jpglabs-portfolio-bff`)
- **Stack:** Node.js, Hono, TypeScript, AI SDK (`ai`), Supabase
- **Responsabilidade:** dono canônico de todas as rotas `/api/*`

### Frontend AI (`jpglabs-portfolio-backend`)
- **Stack:**Nest.js 14, next-auth (JWT), TypeScript, Tailwind, AI SDK UI
- **Responsabilidade:** surface conversacional/agentic, CRUD e dashboard de manutenção do Pi
- **k8s manifests:** `app/k8s/` — portfolio, n8n, ollama, knowledge-hub
- ⚠️ `SUPABASE_SERVICE_ROLE` pendente de configuração

### Knowledge Hub App (`knowledge-hub-app`)
- **Stack:**Nest.js, Supabase, next-auth, GitHub OAuth
- **Status:** Manifests prontos, não deployado ainda

### Pi Local App (`pi-local-app`)
- **Stack:** Node.js, Ollama HTTP client
- **Porta:** 3131 | **Auth:** Bearer (PI_API_KEY) + web session (HMAC cookie)
- **Módulos src/:** `server.js`, `mcp.js`, `memory-core.js`, `session-sync.js`, `session-sync-fallback.js`, `system-runtime.js`, `service-registry.js`, `service-constitution.js`, `life-manager.js`, `email-runtime.js`, `inbox-store.js`, `pr-review.js`, `traffic-mapper.js`, `ui.js`, `macos-biometric-auth.swift`
- **Endpoints:** `/health`, `/chat`, `/memory/*`, `/session/sync`, `/session/diary`, `/vps/telemetry`, `/life/next`, `/life/status`, `/ui`
- **Modelos locais:** `llama3.2:3b` (rápido), `deepseek-r1:7b` (raciocínio)

### Pi Control App (`pi-control-app`)
- **Stack:** Node.js/TypeScript, interface OpenAI-compatible
- **Porta:** 3030
- **Tools MCP:** `get_pi_runtime_status`, `ask_pi_local`, `transcribe_local_audio`, `sync_pi_session_status`

### Pi Voice Proxy (`pi-voice-proxy`)
- **Porta:** 8787
- **Função:** Mediação OpenAI / Anthropic / Gemini para voz

---

## AI Models Registry

| ID | Nome | Provider | Role |
|----|------|----------|------|
| `llm-llama-fast` | Llama 3.2 3B | Ollama local | Rápido / triagem |
| `llm-deepseek-large` | DeepSeek R1 7B | Ollama local | Raciocínio / planejamento |
| `llm-claude-sonnet` | Claude Sonnet 4.6 | Anthropic API | Código / CTO |
| `llm-vllm-pending` | vLLM Endpoint | vLLM (GPU) | Planejado |

**LLMs externos usados em projetos:**
- OpenAI: `gpt-5.4` (chat), `gpt-4o-mini-tts` (voz), `gpt-4o-realtime-preview` (realtime), `gpt-4o-mini-transcribe`
- Google Gemini: `gemini-2.5-pro`

---

## Supabase — Data Layer

**Projeto:** `bykeqyqleicrbyqtnaet` | Region: `us-east-1` | Postgres 17

| Tabela | Propósito | RLS |
|-------|---------|-----|
| `roadmap_items` | Roadmap live — atualizado por Claude + Pi | Leitura pública, escrita auth |
| `portfolio_projects` | Projetos do portfólio | Leitura pública, escrita auth |
| `portfolio_experiences` | Histórico profissional | Leitura pública, escrita auth |
| `portfolio_skills` | Tech stack | Leitura pública, escrita auth |
| `environments` | Status DSV/TST/STG/PRD | Leitura pública, escrita auth |
| `llm_registry` | Registry de modelos | Leitura pública, escrita auth |
| `infra_gaps` | Rastreador de lacunas de infra | Leitura pública, escrita auth |
| `portal_users` | Usuários + roles | Somente auth |
| `role_permissions` | Matriz ACL por role | Leitura pública |
| `pi_session_diaries` | Diários de sessão Pi/Claude | Escrita via Bearer |

---

## Access Control (Roles)

| Role | Relação | Dashboard | PortfolioManager | Roadmap | VPS | Mutations |
|------|----------|-----------|-----------------|---------|-----|-----------|
| `ROOT_ADMIN` | Jader | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Sim |
| `SUB_OWNER` | Ayumi | ✅ Read | ✅ Read | ✅ Read | ✅ Read | ❌ Não |
| `FAMILY` | Filhas | ✅ Tiles | ❌ | ✅ Read | ❌ | ❌ Não |
| `PI_AGENT` | Pi service | API | API write | API write | API read | API only |
| `CLAUDE_ORCHESTRATOR` | Claw | API read | API write | API write | API read | API only |
| `USER_CONSULTANT` | Externo | ❌ | ❌ | ✅ Read | ❌ | ❌ Não |

---

## CI/CD Pipeline (`pi-local-app`)

**Workflow:** `.github/workflows/deploy.yml`
- **Triggers:** `src/**`, `profiles/**`, `package.json`, `bin/**`
- **Concorrência:** grupo `deploy-pi-vps`, `cancel-in-progress: false`
- **Jobs:** `validate` → `deploy` → smoke test automático → rollback se falhar
- **Validate:** `node --check` em todos `src/*.js` + validação de exports dos 5 módulos core + `node --test`
- **Deploy:** rsync destrutivo para `src/` + rsync não-destrutivo para `profiles/` + `systemctl restart`
- **Smoke test:** 10 tentativas em `/health`, valida `status='ok'` + MCP JSON-RPC 2.0 handshake
- **Rollback:** manual via `workflow_dispatch`, re-deploya SHA registrado em `.deployed_sha`

**Promoção de ambientes:**
```
PR merge → CI build → TST (testes de contrato) → STG (smoke tests)
        → aprovação manual (`ROOT_ADMIN`) → PRD
```

---

## Secrets Status

| Secret | Status |
|--------|--------|
| `ANTHROPIC_API_KEY` | ✅ Set |
| `PI_API_KEY` | ✅ Set |
| `SUPABASE_URL` + `SUPABASE_ANON_KEY` | ✅ Set |
| `NEXTAUTH_SECRET` | ✅ Set |
| `N8N_ENCRYPTION_KEY` | ✅ Set |
| `SUPABASE_SERVICE_ROLE` (hub-secrets) | ⏳ Pendente |
| `CF_API_TOKEN` (Cloudflare) | ⚠️ Rotação necessária |
| `OPENAI_API_KEY` | ❌ Não configurado |
| `WHATSAPP_*` tokens | ❌ Não configurado |
| `GITHUB_PAT` (hub-secrets) | ❌ Não configurado |

---

## Action Queue (Prioridade)

| # | Ação | Bloqueador | Owner |
|---|--------|---------|-------|
| 1 | Rotar CF_API_TOKEN → atualizar k8s secret | Renovação TLS | Jader |
| 2 | Obter SUPABASE_SERVICE_ROLE → `hub-secrets` | Auth backend | Jader |
| 3 | Configurar WhatsApp tokens em `n8n-secrets` | Workflows n8n | Jader |
| 4 | WiringNest.js BFF com Supabase service-role | Auth dashboard | Claw |
| 5 | Aplicar k8s service manifests (portfolio, hub) | Não deployado | Claw |
| 6 | Criar Traefik IngressRoutes por serviço | Roteamento TLS | Claw |
| 7 | Seed `portfolio_projects`, `experiences`, `skills` | Portfolio vazio | Claw+Jader |
| 8 | Adicionar contas das filhas em `portal_users` | Acesso família | Jader |
| 9 | Canonicalizar `.codex/skills` → symlink `LLMs_cli/skills` | Integridade workspace | Claw |

---

## Workspace Integrity Issues

1. **Skills root divergente** — `.codex/skills` e `~/.codex/skills` existem separados do canônico `LLMs_cli/skills`
2. **WORKSPACE_INDEX.md pointer** — cópia em `knowledge-hub` deve ser apenas ponteiro

---

## Desenvolvimento Local

```bash
# Frontend Vite
cd ~/code/pessoal/jpglabs/jpglabs-portfolio-frontend && npm run dev  # :8082

# BackendNest.js
cd ~/code/pessoal/jpglabs/jpglabs-portfolio-backend && npm run dev   # :3000

# Pi local app
cd ~/code/pessoal/pi-local-app && npm run dev  # :3131 (hot reload)

# Pi control app
cd ~/code/pessoal/pi-control-app && npm run dev  # :3030

# Ollama (local LLMs)
ollama serve  # :11434
```
