# jpglabs-dashboard — Contrato de Dados v1

Criado em `17/04/2026`. Entregável da Trilha 1 (Clareza de Escopo e Dados).

## Decisão Formal

O dashboard v1 opera **local-first com dados estáticos** curados manualmente em `src/data/`.
Fontes dinâmicas (Jira API, MCP real-time, filesystem) entram na **Trilha 3**, após a Trilha 1 estar fechada.

## Seções Obrigatórias v1

| Seção | Arquivo-fonte | Tipo | Responsável pela atualização |
|---|---|---|---|
| Trilhas ativas | `src/data/roadmap.ts` → `trilhas` | estático | curação manual por sessão |
| Estado MCP | `src/data/roadmap.ts` → `mcpConnectors` | estático | curação manual |
| Infra e plataforma | `src/data/roadmap.ts` → `infraComponents`, `platformPhases` | estático | curação manual |
| Próximas ações (pre-prompt) | `src/data/roadmap.ts` → `prePromptActions` | estático | curação manual |
| Sessões recentes | **ausente na v1** — escopo da Trilha 3 | n/a | MCP filesystem / session memory |

## O Que É Estático e Permanece Estático na v1

```
src/data/
  roadmap.ts       → trilhas, mcpConnectors, infraComponents, platformPhases, prePromptActions
  cv.ts            → dados de CV (portfólio pessoal)
  learning.ts      → log de aprendizados
  marketing.ts     → ativos de marketing
  portfolio.ts     → projetos do portfólio
  product-spec.ts  → especificações de produto
  providers.ts     → provedores de runtime
  teams.ts         → composição de equipes
```

Todos os arquivos acima são **intencionalmente estáticos na v1**. Cada sessão de trabalho que altere estado relevante (novo bloqueio, trilha concluída, conector atualizado) deve atualizar o arquivo correspondente manualmente ou via agente.

## O Que Entra na Trilha 3 (Dinâmico)

| Dado | Fonte futura | Prioridade |
|---|---|---|
| Status real das trilhas | Jira API (`jpglabs.atlassian.net`) | P0 após Jira reconectar |
| Estado real dos MCP connectors | Docker MCP gateway health check | P1 |
| Sessões recentes | `workspaces/jpgermano-2026/memory/sessions/` via MCP filesystem | P1 |
| Histórico de commits por trilha | `git log` via MCP git | P2 |

## Bloqueio Conhecido (não impede v1)

O MCP Atlassian conectado em `jadergermano.atlassian.net` expõe apenas Confluence.
O Jira (`jpglabs.atlassian.net`) está bloqueado — requer reautorização com OAuth correto.
A trilha de dados dinâmicos (Trilha 3) depende desse desbloqueio para status de épicos em tempo real.

## Critérios de Saída da Trilha 1 — Verificação

- [x] Decisão formal de fontes de dados: **local-first estático para v1**
- [x] Separação documentada entre o que é hardcoded e o que será dinâmico
- [x] Seções obrigatórias da v1 definidas: 4 seções ativas + 1 (sessões recentes) na Trilha 3
- [ ] Seções aprovadas pelo DRI (Jader) — **aguardando confirmação**
