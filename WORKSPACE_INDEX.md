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

- `Playground 2`
  - Nicho: repositório experimental sem commits úteis ainda
  - Papel no workspace: área de bootstrap/experimentos
  - Contexto: `projects/playground-2/PROJECT_CONTEXT.md`

- `apple-study-checklist`
  - Nicho: app SwiftUI para plano técnico de estudos Apple
  - Papel no workspace: produto ativo com foco mobile-first
  - Contexto: `projects/apple-study-checklist/PROJECT_CONTEXT.md`

- `portfolio-backend`
  - Nicho: superfície web/backend do portfólio e do ecossistema Pi
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

- `knowledge-hub-app`
  - Nicho: app Next.js para a superfície operacional do knowledge hub
  - Papel no workspace: UI web do hub e fluxos financeiros
  - Contexto: `projects/knowledge-hub-app/PROJECT_CONTEXT.md`

- `pi-local-app`
  - Nicho: runtime local do Pi com memória e superfície HTTP
  - Papel no workspace: contrato central do ecossistema Pi
  - Contexto: `projects/pi-local-app/PROJECT_CONTEXT.md`

- `pibar-macos`
  - Nicho: cliente macOS do ecossistema Pi
  - Papel no workspace: shell desktop com UI recente em Liquid Glass
  - Contexto: `projects/pibar-macos/PROJECT_CONTEXT.md`

- `piphone-ios`
  - Nicho: cliente iOS do ecossistema Pi
  - Papel no workspace: shell iPhone integrada ao Pi service
  - Contexto: `projects/piphone-ios/PROJECT_CONTEXT.md`

- `PieCenter`
  - Nicho: shell Apple unificado para substituir PiPhone e PiBar
  - Papel no workspace: novo cliente compartilhado iPhone + macOS com menu bar e janela expandida
  - Contexto: `projects/PieCenter/PROJECT_CONTEXT.md`

- `openclaude`
  - Nicho: open-source coding-agent CLI para cloud e local model providers
  - Papel no workspace: alternativa aberta e agnóstica ao Claude Code integrada ao hub
  - Contexto: `projects/openclaude/PROJECT_CONTEXT.md`

- `jpglabs-saas`
  - Nicho: SaaS B2B Monitor de Licitações — produto comercial priorizado da JPGLabs
  - Papel no workspace: trilha de receita principal via JPGLABS TECNOLOGIA LTDA
  - Contexto: `projects/jpglabs-saas/PROJECT_CONTEXT.md`

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
