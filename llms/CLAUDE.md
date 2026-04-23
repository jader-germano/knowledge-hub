# Claude Shared Context

Objetivo: dar ao Claude uma entrada curta e estável para este workspace.

Consulta obrigatória:

1. `RULES.md`
2. `OWNERSHIP.md`
3. `WORKSPACE_INDEX.md`
4. `GIT_HISTORY_INDEX.md`
5. `manifests/workspace.index.yaml`
6. `DOC_INDEX.md`
7. `MCP_SETUP.md`
8. `agents/AGENT_BRIDGE.md`
9. `agents/SESSION_CLOSE_TEMPLATE.md`

Arquivos locais relevantes:

- `.claude/settings.json`
- `.claude/skills/teams/SKILL.md`

Ao atuar em um repo:

- abrir `projects/<repo>/PROJECT_CONTEXT.md`
- abrir `projects/<repo>/GIT_HISTORY.md`
- abrir `projects/<repo>/llms/CLAUDE.md`
- usar `jpglabs/docs` como referência transversal compartilhada
- antes de planejar, carregar guideline, `ROADMAP.md`, ticket em `Jira` ou
  espelho no `Confluence` se já existirem para evitar duplicação e gasto
  desnecessário de tokens
- tratar `Jira` como task/status board, `Confluence` como spec/roadmap mirror e
  `Notion` apenas como diário
- terminar tarefas substanciais com uma proposta concreta de próximo passo
  pronta para aprovação; se a UI suportar popup/card de permissão, preferir esse
  formato
