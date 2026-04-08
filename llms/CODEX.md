# Codex Shared Context

Objetivo: dar ao Codex uma entrada curta e estável para este workspace.

Consulta obrigatória:

1. `CODEX.md`
2. `RULES.md`
3. `OWNERSHIP.md`
4. `WORKSPACE_INDEX.md`
5. `GIT_HISTORY_INDEX.md`
6. `manifests/workspace.index.yaml`
7. `DOC_INDEX.md`
8. `agents/AGENT_BRIDGE.md`
9. `agents/SESSION_CLOSE_TEMPLATE.md`

Ao atuar em um repo:

- abrir `projects/<repo>/PROJECT_CONTEXT.md`
- abrir `projects/<repo>/GIT_HISTORY.md`
- abrir `projects/<repo>/llms/CODEX.md`
- validar o path real declarado no contexto do projeto
- tratar `jpglabs/docs` como fonte global compartilhada, não o bootstrap local
- antes de planejar, carregar guideline, `ROADMAP.md`, ticket em `Jira` ou
  espelho no `Confluence` se já existirem para evitar duplicação e gasto
  desnecessário de tokens
- tratar `Jira` como task/status board, `Confluence` como spec/roadmap mirror e
  `Notion` apenas como diário
- terminar tarefas substanciais com uma proposta concreta de próximo passo
  pronta para aprovação; se a UI suportar popup/card de permissão, preferir esse
  formato
