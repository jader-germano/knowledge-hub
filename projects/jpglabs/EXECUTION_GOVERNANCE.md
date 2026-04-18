# Execution Governance — JPGLabs

Criado em `17/04/2026`. Lane 2 do roadmap JPGLabs.

## Regra Fundamental

Toda task, épico, decisão arquitetural e roadmap do JPGLabs nasce em **Jira** ou **Confluence**. Não em Notion, não em arquivos locais soltos, não em mensagens de chat.

---

## Superfícies De Execução

### Jira — Tasks E Status

**O que vai aqui:**
- Épicos, stories, tasks e sub-tasks de desenvolvimento
- Status atual de cada item (To Do / In Progress / Done / Blocked)
- Labels de tipo (feature, bug, chore, spike, release)
- DRI (Directly Responsible Individual) por task

**Regras:**
- Toda task nova nasce no Jira — nenhum agente ou desenvolvedor começa trabalho sem ticket
- Status deve ser atualizado no início e no final de cada sessão de trabalho
- Tasks bloqueadas recebem label `blocked` e comentário com o bloqueio explícito
- Nenhuma task fica em `In Progress` por mais de 7 dias sem comentário de progresso

### Confluence — Specs, Decisões E Roadmap Mirror

**O que vai aqui:**
- Specs de features com critérios de aceite verificáveis
- ADRs (Architecture Decision Records)
- Roadmap mirror — cópia navegável do `ROADMAP.md` local
- Guias de integração e onboarding técnico
- Contratos canônicos de API

**Regras:**
- Specs vivem no Confluence, não no Notion
- Todo ADR deve seguir: Contexto → Decisão → Consequências → Status
- Roadmap mirror é atualizado sempre que o `ROADMAP.md` local muda
- Não duplicar conteúdo entre Jira e Confluence — tasks no Jira linkam para specs no Confluence

### Notion — Diário Apenas

**O que vai aqui:**
- Diário técnico diário (notas pessoais, reflexões, rascunhos)
- Nada mais

**Regras:**
- Specs, roadmaps, tasks e decisões arquiteturais **não** vivem no Notion
- Se um rascunho do Notion virar decisão formal, migrar para Confluence imediatamente
- Notion não é consultado por agentes para estado de tasks ou specs

---

## Política De Discovery De Agentes

### Problema

Sem política explícita, múltiplos agentes re-indexam as mesmas fontes de dados a cada sessão, gerando:
- Duplicação de tokens desnecessária
- Inconsistências quando fontes divergem
- Descoberta de contexto fragmentada por sessão

### Fontes Canônicas Por Tipo De Dado

| Tipo de dado | Fonte canônica | Onde agentes buscam |
|---|---|---|
| Tasks e status | Jira | MCP `mcp__claude_ai_Atlassian_Rovo` |
| Specs e decisões | Confluence | MCP `mcp__claude_ai_Atlassian_Rovo` |
| Roadmaps | `jpglabs/docs/projects/*/ROADMAP.md` | filesystem MCP |
| Contratos de API | Confluence + `docs/projects/*/` | filesystem MCP |
| Docs de biblioteca | Context7 | MCP `mcp__plugin_context7_context7` |
| Histórico Git | `git log` via MCP `git` | MCP `git` |
| Sessões cross-agent | `workspaces/jpgermano-2026/memory/sessions/` | filesystem MCP |
| Memória operacional | `jpglabs/docs/memory/PI_MEMORY.md` | filesystem MCP |

### Regras

1. Agentes não re-indexam o que já está disponível em fonte canônica — consultam diretamente
2. Quando duas fontes divergirem, a fonte canônica da tabela acima prevalece
3. Nenhum agente cria sua própria cópia local de dado que já tem fonte canônica
4. Discovery de codebase usa `ast-grep` + `git` antes de leitura manual de arquivos
5. Docs de bibliotecas externas usam Context7 — não fetch direto de documentação

---

## Épicos Do Ciclo Atual

Formalizados no Jira em `17/04/2026`. Projeto: `SCRUM` — `jpglabs.atlassian.net`.

| Épico | Jira | Lane | Prioridade | Repos afetados |
|---|---|---|---|---|
| `Portfolio Backend/BFF Split` | [SCRUM-27](https://jpglabs.atlassian.net/browse/SCRUM-27) | Lane 1 | P0 | `portfolio-backend` |
| `Portfolio Frontend Lane` | [SCRUM-28](https://jpglabs.atlassian.net/browse/SCRUM-28) | Lane 1 | P0 | `jpglabs-portfolio` |
| `Portfolio Mobile Role Decision` | [SCRUM-29](https://jpglabs.atlassian.net/browse/SCRUM-29) | Lane 1 | P0 | `portfolio-mobile` |
| ~~`Operator Shell Contract`~~ | ~~SCRUM-30~~ — **cancelado** | Lane 1 | — | `knowledge-hub-app`, `pibar-macos`, `piphone-ios` **arquivados em 17/04/2026** |
| `Jira+Confluence Migration` | [SCRUM-31](https://jpglabs.atlassian.net/browse/SCRUM-31) | Lane 2 | P0 | workspace-level |
| `Dashboard Roadmap v1` | [SCRUM-32](https://jpglabs.atlassian.net/browse/SCRUM-32) | Lane 2 | P0 | `jpglabs-dashboard` |
| `Surface Coherence Design System` | [SCRUM-33](https://jpglabs.atlassian.net/browse/SCRUM-33) | Lane 3 | P0/P1 | 5 superfícies |

---

## Critério De Saída Da Lane 2

- [ ] Todos os épicos acima formalizados no Jira com DRI e critérios de aceite
- [ ] Roadmap mirror de todos os 7 sistemas com roadmap publicado no Confluence
- [ ] Notion restrito ao diário — nenhuma task ativa fora do Jira
- [ ] Esta política (`EXECUTION_GOVERNANCE.md`) linkada no `PROJECT_CONTEXT.md` do workspace
- [ ] Agentes têm contrato explícito de discovery (tabela acima no Confluence)
