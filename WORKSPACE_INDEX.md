# Workspace Index

Índice global dos contextos ativos sob `/Users/philipegermano/code`.

## Ordem De Consulta

1. `RULES.md`
2. `OWNERSHIP.md`
3. `WORKSPACE_INDEX.md`
4. `GIT_HISTORY_INDEX.md`
5. `manifests/workspace.index.yaml`
6. `DOC_INDEX.md`
7. `MCP_SETUP.md`
8. `agents/AGENT_BRIDGE.md`
9. `agents/SESSION_CLOSE_TEMPLATE.md`

## Contextos Indexados

- `docs`
  - Nicho: repositório documental compartilhado e única fonte canônica do workspace
  - Papel no workspace: governança, bootstrap, manifests, handoff e indexação
  - Contexto: `projects/docs/PROJECT_CONTEXT.md`

- `infrastructure`
  - Nicho: automação, scripts, k8s e operação absorvidos do legado `jpglabs`
  - Papel no workspace: slice operacional interno ao hub
  - Contexto: `projects/infrastructure/PROJECT_CONTEXT.md`

- `jpglabs`
  - Nicho: contexto estratégico da JPG Labs como estúdio/produto
  - Papel no workspace: alinhar veículo jurídico, portfólio ativo e roadmap
  - Contexto: `projects/jpglabs/PROJECT_CONTEXT.md`

- `FrankMD`
  - Nicho: app Rails 8 filesystem-first para notas Markdown
  - Papel no workspace: companion documental e referência de vault/editor
  - Contexto: `projects/FrankMD/PROJECT_CONTEXT.md`

- `portfolio-backend`
  - Nicho: superfície web/backend do portfólio
  - Papel no workspace: backend web com governança de release
  - Contexto: `projects/portfolio-backend/PROJECT_CONTEXT.md`

- `portfolio-mobile`
  - Nicho: cliente mobile Expo do portfólio
  - Papel no workspace: app mobile em estágio inicial
  - Contexto: `projects/portfolio-mobile/PROJECT_CONTEXT.md`

- `imap-server`
  - Nicho: servidor MCP de IMAP/iCloud com foco em segurança e privacidade
  - Papel no workspace: projeto produto separado da camada documental
  - Contexto: `projects/imap-server/PROJECT_CONTEXT.md`

- `openclaude`
  - Nicho: open-source coding-agent CLI para cloud e local model providers
  - Papel no workspace: alternativa aberta e agnóstica ao Claude Code integrada ao hub
  - Contexto: `projects/openclaude/PROJECT_CONTEXT.md`

- `openclaude-hub`
  - Nicho: web UI gateway multi-provider para CLIs de coding (WebSocket → gRPC/CLI); rebrand visual em curso como `Axis`
  - Papel no workspace: superfície web autenticada que absorveu o legado `knowledge-hub-app`; deploy canônico em `chat.jpglabs.com.br`
  - Contexto: `projects/openclaude-hub/PROJECT_CONTEXT.md`

- `jpglabs-dashboard`
  - Nicho: dashboard operacional do JPGLabs para trilhas, infra, MCP e ações pre-prompt
  - Papel no workspace: cockpit local-first de coordenação do workspace
  - Contexto: `projects/jpglabs-dashboard/PROJECT_CONTEXT.md`

## Repositórios Operacionais Sem Contexto Próprio No Hub

- `jpglabs-portfolio`
  - Nicho: frontend visual público do portfólio
  - Papel no workspace: superfície web ativa da lane visual do portfólio
  - Contexto canônico desta fase: `projects/jpglabs/PORTFOLIO_GITLAB_MIGRATION_INVENTORY.md`

- `portfolio-v2`
  - Nicho: referência visual/funcional do portfólio
  - Papel no workspace: baseline comparativa, não runtime final
  - Contexto canônico desta fase: `projects/jpglabs/PORTFOLIO_GITLAB_MIGRATION_INVENTORY.md`

## Contextos Planejados Ou Sem Materialização Local

- `apple-study-checklist`
  - Status: contexto mantido no hub, mas sem diretório real no workspace nesta rodada
  - Referência: `projects/apple-study-checklist/PROJECT_CONTEXT.md`

- `knowledge-hub-app`
  - Status: contexto mantido no hub, mas sem diretório real no workspace nesta rodada
  - Referência: `projects/knowledge-hub-app/PROJECT_CONTEXT.md`

- `Playground 2`
  - Status: área experimental referenciada no hub, sem diretório real no workspace nesta rodada
  - Referência: `projects/playground-2/PROJECT_CONTEXT.md`

- `jpglabs-saas`
  - Status: contexto estratégico/comercial ativo, sem repo materializado localmente neste workspace
  - Referência: `projects/jpglabs-saas/PROJECT_CONTEXT.md`

## Legado Arquivado

Os contextos abaixo permanecem apenas como referência histórica e não fazem mais
parte da taxonomia ativa do workspace.

- `pi-local-app`
  - Status: descontinuado — diretório real vazio (apenas `.idea/workspace.xml`)
  - Referência histórica: `projects/pi-local-app/PROJECT_CONTEXT.md`
  - Git/GitLab: arquivado como projeto encerrado

- `pibar-macos`
  - Status: descontinuado — sem git history local
  - Referência histórica: `projects/pibar-macos/PROJECT_CONTEXT.md`
  - Git/GitLab: arquivado como projeto encerrado

- `piphone-ios`
  - Status: descontinuado — sem git history local
  - Referência histórica: `projects/piphone-ios/PROJECT_CONTEXT.md`
  - Git/GitLab: arquivado como projeto encerrado

- `PieCenter`
  - Status: descontinuado — tinha git history mas projeto foi descontinuado
  - Referência histórica: `projects/PieCenter/PROJECT_CONTEXT.md`
  - Git/GitLab: arquivado como projeto encerrado

- `awesomepie-ios`
  - Status: descontinuado — arquivado em 2026-04-07
  - Repo: `~/code/pessoal/awesomepie-ios` (Swift + SFSpeechRecognizer + AVAudioEngine)
  - Git/GitLab: arquivado como projeto encerrado

## Legado Absorvido

- `ai-orchestration-hub`
  - Status: absorvido pelo `docs`
  - Ativos úteis: `../imap-server/` e `tools/ai-orchestration-scripts/`
  - Arquivo histórico: `archive/legacy-repos/ai-orchestration-hub/`

## Escopo Deste Espelho

Este workspace em `code/` usa o repositório `docs` como índice operacional e
documental. As alterações em código continuam acontecendo nos repositórios
reais declarados em cada `PROJECT_CONTEXT.md`.

## Artefatos Por Contexto

Cada contexto indexado deve expor, no mínimo:

- `projects/<repo>/PROJECT_CONTEXT.md`
- `projects/<repo>/GIT_HISTORY.md`
- `projects/<repo>/llms/CODEX.md`
- `projects/<repo>/llms/CLAUDE.md`
- `projects/<repo>/llms/GEMINI.md`
