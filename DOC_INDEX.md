# Document Index

Classificação atual dos documentos no workspace.

## Workspace Entry

- `README.md` — entrada do workspace e mapa rápido da taxonomia
- `WORKSPACE_BOOTSTRAP.md` — bootstrap compartilhado entre providers e agentes
- `AGENTS.md` — shim do fluxo Codex/AGENTS

## Global / Workspace Docs

- `jpglabs/docs/README.md` — entrada global
- `jpglabs/docs/ROADMAP.md` — roadmap de plataforma MCP e agent teams
- `jpglabs/docs/WORKSPACE_INDEX.md` — índice humano dos contextos ativos
- `jpglabs/docs/GIT_HISTORY_INDEX.md` — snapshot classificado do histórico Git
- `jpglabs/docs/RULES.md` — regras operacionais
- `jpglabs/docs/OWNERSHIP.md` — ownership da documentação
- `jpglabs/docs/MCP_SETUP.md` — referência transversal de MCP e gateway Docker
- `jpglabs/docs/agents/AGENT_BRIDGE.md` — handoff transversal mais recente
- `jpglabs/docs/agents/SESSION_CLOSE_TEMPLATE.md` — template obrigatório de fechamento
- `daily/README.md` — contrato canônico do diário raiz do workspace
- `daily/AUTOMATION_PROMPT.md` — prompt-base da sessão diária automatizada
- `daily/*.md` — relatórios diários por sessão do workspace
- `jpglabs/docs/manifests/workspace.index.yaml` — índice de contextos
- `jpglabs/docs/manifests/docs.index.yaml` — índice classificatório dos documentos
- `jpglabs/docs/manifests/skills.index.yaml` — índice de skills compartilhadas
- `.agents/skills/README.md` — catálogo canônico de skills compartilhadas do workspace
- `jpglabs/docs/llms/CODEX.md` — contexto do Codex
- `jpglabs/docs/llms/CLAUDE.md` — contexto do Claude
- `jpglabs/docs/llms/GEMINI.md` — contexto do Gemini

## References / Workspace Docs

- `jpglabs/docs/reference/design/design-system-extraction-4-sites.md` — análise de referência para design system
- `jpglabs/docs/reference/design/design-system-claude-codex.html` — comparação visual entre Claude.app e Codex.app
- `jpglabs/docs/reference/web-captures/google-antigravity-auth-success.html` — captura web de referência Google Antigravity
- `jpglabs/docs/reference/web-captures/jpglabs-pi-products-and-services.html` — captura web de referência da superfície Pi/JPGLabs
- `jpglabs/docs/reference/web-captures/monkeytype-typing-test.html` — captura web de referência Monkeytype

## Reports

- `jpglabs/docs/reports/claude-code/claude-code-daily-report-2026-03-21.md` — relatório diário consolidado do Claude Code
- `jpglabs/docs/reports/claude-code/claude-code-daily-report-2026-03-21.html` — versão HTML do relatório diário
- `jpglabs/docs/reports/claude-code/claude-code-report-template.html` — template HTML reutilizável para novos relatórios

## Research

- `jpglabs/docs/research/roadmap-pressure-tests/brutal-critic-triad-pressure-test-2026-03-21.json` — artefato bruto do teste de pressão de roadmap
- `jpglabs/docs/research/claude-shared-capabilities-audit.md` — audit do Claude para separar o que é compartilhável no workspace

## Archive / Legacy

- `jpglabs/docs/archive/root-docs/DOCS_INDEX.legacy-2026-03-27.md` — índice anterior à unificação final
- `jpglabs/docs/archive/legacy-repos/ai-orchestration-hub/` — recorte legado absorvido
- `jpglabs/docs/archive/legacy-repos/jpglabs-infra-repo/` — snapshot do repositório legado `jpglabs`
- `_archive/` no root do workspace foi aposentado após auditoria; o material
  útil já estava refletido em `context/`, `infrastructure/docs/` e no
  `archive/` canônico deste repositório

## Project Context

- `jpglabs/docs/projects/*/PROJECT_CONTEXT.md` — contexto classificado por projeto ou slice operacional
- `jpglabs/docs/projects/*/ROADMAP.md` — roadmap específico do contexto, quando existir

## Project Git History

- `jpglabs/docs/projects/*/GIT_HISTORY.md` — histórico Git classificado por contexto

## Project Provider Context

- `jpglabs/docs/projects/*/llms/CODEX.md` — bootstrap fino por contexto para Codex
- `jpglabs/docs/projects/*/llms/CLAUDE.md` — bootstrap fino por contexto para Claude
- `jpglabs/docs/projects/*/llms/GEMINI.md` — bootstrap fino por contexto para Gemini

## Session History

- `jpglabs/docs/projects/*/sessions/**/report.md` — relatório classificado de sessão
- `jpglabs/docs/projects/*/sessions/**/prototype.md` — artefato complementar de sessão, quando existir

Contrato:

- `jpglabs/docs/projects/*/sessions/**` é o ledger canônico e gravável de sessão
- `jpglabs/docs/reports/sessions/` fica restrito a template/view derivada

## Provider Bootstrap

- `WORKSPACE_BOOTSTRAP.md`
- `AGENTS.md`
- `CODEX.md`
- `CLAUDE.md`
- `GEMINI.md`
- `.codex/README.md`
- `.claude/README.md`
- `.gemini/README.md`

## Runtime / Operational Config

- `.mcp.json` — entrypoint operacional do cliente MCP no root do workspace
- `config/mcp/docker-mcp-config.yaml` — baseline compartilhado do gateway Docker MCP
- `config/mcp/docker-mcp-shared-catalog.yaml` — catálogo compartilhado com overrides de memória e afins
- `.claude/settings.json` — runtime local do Claude
- `.claude/skills/README.md` — wrappers locais gerados a partir de `/.agents/skills/`

## Shared Memory

- `jpglabs/docs/memory/PI_MEMORY.md` — ledger canônico de memória incorporada
- `jpglabs/docs/memory/AGENTS.md` — governança operacional do agente Pi
- `jpglabs/docs/memory/sessions/` — working memories incorporadas
- `jpglabs/docs/memory/logs/` — logs técnicos e trilha operacional do Pi
- `jpglabs/docs/memory/wiki/` — compilações temáticas derivadas de `raw/` (wiki layer Karpathy)

Contrato:

- `jpglabs/docs/memory/` é o namespace canônico e gravável de memória
- `memory/wiki/` é editável pelo LLM; derivar sempre de fontes em `raw/`
- não criar variantes paralelas em `reports/`, mirrors antigos ou raízes legadas

## Raw Sources

- `jpglabs/docs/raw/README.md` — contrato da camada imutável
- `jpglabs/docs/raw/videos/` — transcrições brutas de vídeos (append-only)
- `jpglabs/docs/raw/articles/` — textos integrais de artigos/papers (append-only)

Contrato:

- `jpglabs/docs/raw/` é append-only para agentes LLM
- nunca editar conteúdo após captura; apenas adicionar novas entradas versionadas
- toda compilação em `memory/wiki/` deve referenciar fonte em `raw/`

## Architecture Decision Records

- `jpglabs/docs/research/adr/ADR-001-llm-wiki-architecture.md` — mapeamento LLM Wiki (Karpathy) ao workspace

## Obsidian Vault Config

- `jpglabs/docs/.obsidian/graph.json` — graph view com cores por pasta (raw=verde, memory=azul, projects=laranja, agents=vermelho)
- `jpglabs/docs/.obsidian/templates.json` — aponta para `_templates/` como pasta de templates
- `jpglabs/docs/.obsidian/daily-notes.json` — daily notes em `daily/`, template `_templates/daily-session`
- `jpglabs/docs/.obsidian/community-plugins.json` — plugins recomendados (Dataview, Templater, Calendar)
- `jpglabs/docs/.obsidian/plugins/README.md` — guia de instalação e plugins a evitar

## Templates

- `jpglabs/docs/_templates/raw-video.md` — template para transcrição de vídeo (raw layer)
- `jpglabs/docs/_templates/raw-article.md` — template para artigo capturado (raw layer)
- `jpglabs/docs/_templates/wiki-page.md` — template para compilação temática (wiki layer)
- `jpglabs/docs/_templates/daily-session.md` — template para sessão no daily
- `jpglabs/docs/_templates/project-context.md` — template para PROJECT_CONTEXT de novo projeto

## Index / MOC

- `jpglabs/docs/index.md` — Map of Content principal do vault Obsidian (entrada por tipo, projeto e layer Karpathy)

## Regras De Classificação

- genérico e compartilhado sobe para `jpglabs/docs/`
- específico de contexto vai para `jpglabs/docs/projects/<repo>/`
- histórico Git vai para `jpglabs/docs/projects/<repo>/GIT_HISTORY.md`
- contexto por provider vai para `jpglabs/docs/projects/<repo>/llms/`
- histórico de sessão fica em `jpglabs/docs/projects/<repo>/sessions/`
- `reports/` não compete com o ledger; serve para template, render derivado e relatórios auxiliares
- `memory/` concentra memória persistente, sessões incorporadas e logs técnicos
- runtime local continua fora do repositório documental canônico
- bootstrap compartilhado da raiz vive em `WORKSPACE_BOOTSTRAP.md`
