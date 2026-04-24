# Design: GitLab CI — AI Code Audit Pipeline

**Data:** 2026-04-24  
**Status:** Aprovado  
**Autor:** Philipe Germano + Claude  
**Skill origem:** `ai-code-audit` (extraída de https://youtu.be/MvFO-W9zZRk — Uncle Bob, Apr 2026)

---

## Contexto

Com a adoção crescente de código gerado por IA (taxa de aceitação ~30–55% em 2026, SWE-bench >70%), revisão linha a linha deixou de escalar. A abordagem adotada substitui o code review manual por **4 provas objetivas automáticas** rodando em todo MR, complementadas por análise semântica via LLM local (Ollama na VPS).

---

## Escopo

### Repos alvo

Todos os repos ativos do workspace JPGLabs, exceto `openclaude` (CLI) e `apple-checklist`:

- `jpglabs-dashboard` (Next.js/TypeScript)
- `openclaude-hub` (Bun/TypeScript)
- `portfolio-backend` (Node.js/TypeScript)
- `portfolio-mobile` (React Native)
- `imap-server` (Node.js)
- `docs` (hub canônico)

### Fora do escopo agora

- Merge de `docs/` no `red-cartesian-motion` (backlog)
- Suporte a repos non-JS/TS (Java, Python) — sem repos ativos no momento

---

## Arquitetura

### Localização do componente

```
red-cartesian-motion/
└── packages/
    └── ci/
        └── components/
            └── ai-code-audit/
                ├── template.yml          ← GitLab CI Component (entry point)
                └── scripts/
                    ├── static-audit.sh   ← Job A: análise estática
                    └── ai-audit.sh       ← Job B: Ollama na VPS
```

Publicado como **GitLab CI Component** (`red-cartesian-motion`), versionado por tag semver.

### Inclusão em cada repo (3 linhas)

```yaml
include:
  - component: gitlab.com/jpglabs/red-cartesian-motion/ci/ai-code-audit@~latest
    # ~latest = última minor; fixar em versão específica em produção (ex: @1.0.0)

stages: [audit, validate, deploy]
```

### Fluxo por MR

```
MR aberto / novo commit pushed
          │
          ▼
    stage: audit  (jobs paralelos)
    ┌──────────────────┐   ┌─────────────────┐
    │   audit-static   │   │    audit-ai      │
    │  (runner padrão) │   │  (tag: vps)      │
    │  node:22-slim    │   │  Tailscale→Ollama│
    └────────┬─────────┘   └────────┬─────────┘
             │                      │
             └──────────┬───────────┘
                        ▼
               audit-report.md (artifact)
               comentário automático no MR
                        │
                        ▼
                 stage: validate
              (test / lint / build)
```

**Regra:** `audit` bloqueia `validate`. MR não avança se qualquer check bloqueador reprovar.

---

## Job A — Análise Estática

**Runtime:** `node:22-slim`, runner padrão (sem custo de VPS)

### Checks

| # | Check | Ferramenta | Threshold padrão | Comportamento |
|---|---|---|---|---|
| 1 | Complexidade ciclomática | ESLint `complexity` rule | CCN > 20 | Bloqueia MR |
| 2 | Tamanho de módulo | `wc -l` (shell) | > 300 linhas/arquivo | Bloqueia MR |
| 3 | Imports circulares | `madge --circular` | qualquer circular | Bloqueia MR |
| 4 | Estrutura de camadas | `madge --image` + grep | violações configuráveis | Warning (não bloqueia) |

### Variáveis configuráveis por repo

```yaml
variables:
  AUDIT_CCN_MAX: "20"
  AUDIT_MAX_LINES: "300"
  AUDIT_BLOCK_ON_CIRCULAR: "true"
  AUDIT_LAYER_VIOLATIONS: "warn"   # "error" para bloquear
```

### Saída

- Exit 1 em falha bloqueadora → pipeline reprovado
- Arquivo `static-audit-results.txt` passado para o job B via artifact

---

## Job B — Agente IA (Ollama na VPS)

**Runtime:** runner com tag `vps`, conexão Tailscale ephemeral (padrão do `openclaude-hub`)

### Smoke Test de Modelos (pré-requisito — roda uma vez)

Antes de fixar o modelo em produção, o job especial `audit-model-smoke` avalia todos os modelos instalados no Ollama:

**Fluxo:**
1. `GET /api/tags` → lista modelos disponíveis
2. Para cada modelo, envia um diff sintético contendo:
   - Função com CCN = 25 (10 `if`s aninhados)
   - Arquivo com 420 linhas
   - Import circular A→B→A
3. Mede e pontua cada modelo

**Critérios de pontuação:**

| Critério | Peso |
|---|---|
| Identifica corretamente os 3 problemas | 50% |
| Tempo de resposta ≤ 30s | 30% |
| Output estruturado (JSON ou Markdown parseável) | 20% |

**Output:** `smoke-report.md` como artifact GitLab + ranking dos modelos. O modelo vencedor é declarado na variável `AUDIT_AI_MODEL` no componente.

### Job B em produção

```
1. git diff origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME  →  extrai diff
2. tailscale up --authkey=$TS_AUTHKEY --ephemeral
3. POST http://<ollama-vps>/api/generate
   - model: $AUDIT_AI_MODEL
   - prompt: template padrão + métricas do Job A + diff (limitado a 4000 tokens)
4. Parse response  →  audit-report.md
5. POST GitLab API  →  comentário no MR
6. Upload artifact: audit-report.md
```

### Template de prompt

```
Você é um auditor de código sênior. Analise o diff abaixo e os resultados
da análise estática. Identifique: riscos de manutenibilidade, violações
de arquitetura, e sugira refatorações objetivas e concisas.

Formato de resposta: Markdown com seções
## Riscos Críticos, ## Avisos, ## Sugestões

[MÉTRICAS ESTÁTICAS]
{saída do job A}

[DIFF DO MR — {N} linhas]
{git diff limitado a 4000 tokens}
```

### Variáveis necessárias (GitLab CI/CD Settings)

| Variável | Tipo | Descrição |
|---|---|---|
| `TS_AUTHKEY` | Secret | Tailscale auth key ephemeral |
| `GITLAB_TOKEN` | Secret | Token com scope `api` para comentário no MR |
| `AUDIT_AI_MODEL` | Variable | Nome do modelo Ollama (definido pós smoke test) |
| `OLLAMA_HOST` | Variable | Hostname/IP do Ollama na tailnet |

---

## Artifact e Comentário no MR

### artifact: `audit-report.md`

```markdown
# AI Code Audit — MR !{id}

**Modelo:** {AUDIT_AI_MODEL}  
**Data:** {timestamp}  
**Commit:** {SHA}

## Análise Estática
{saída formatada do Job A}

## Análise Semântica (IA)
{resposta do Ollama}
```

### Comentário no MR

Postado via GitLab API (`POST /projects/:id/merge_requests/:iid/notes`) com o conteúdo completo do `audit-report.md`. Se já existe um comentário de auditoria anterior no MR, o job **edita** o comentário existente via `PUT /notes/:note_id` (evita spam a cada push). Identificação do comentário próprio via marcador HTML `<!-- ai-code-audit-bot -->` no corpo — o job busca esse marcador antes de decidir criar ou editar.

---

## Plano de Implementação (alto nível)

1. Criar `packages/ci/` em `red-cartesian-motion`
2. Implementar `static-audit.sh` com os 4 checks
3. Implementar `audit-model-smoke` job + `ai-audit.sh`
4. Criar `template.yml` (GitLab CI Component)
5. Publicar como componente (tag `v0.1.0`)
6. Adicionar `include` nos 6 repos alvo
7. Rodar smoke test na VPS → definir `AUDIT_AI_MODEL`
8. Validar em MR real no `jpglabs-dashboard`

---

## Decisões fora do escopo (backlog)

- Merge de `docs/` no `red-cartesian-motion` — impacto no hub canônico, avaliar separado
- Suporte a Java/Python quando repos não-TS entrarem no workspace
- Dashboard de métricas acumuladas por repo (histórico de audit scores)
