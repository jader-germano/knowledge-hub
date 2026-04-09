# JPGLabs Docs

Este repositório em `/Users/philipegermano/code/jpglabs/docs` é a
única camada canônica de documentação compartilhada do workspace `code`.

Taxonomia:

- `ROADMAP.md` — estratégia e fases globais
- `WORKSPACE_INDEX.md` — visão indexada dos contextos ativos
- `GIT_HISTORY_INDEX.md` — snapshot classificado do histórico Git
- `DOC_INDEX.md` — classificação dos documentos do workspace
- `RULES.md` — regras operacionais
- `OWNERSHIP.md` — ownership da informação
- `agents/` — handoff e fechamento de sessão
- `llms/` — contexto compartilhado por LLM
- `memory/` — memória incorporada do workspace, working memories e logs técnicos
- `projects/` — contexto, histórico e roadmaps classificados por projeto ou slice operacional
- `reference/` — referências de design e capturas web
- `reports/` — relatórios operacionais e templates
- `research/` — artefatos de análise e experimentos
- `archive/` — documentos e repositórios legados preservados
- `manifests/` — índices legíveis por máquina
- `tools/` — scripts absorvidos do legado que ainda não viraram projeto próprio

Princípio central:

- o repo `docs` indexa e orquestra
- o contexto específico fica em `projects/`
- `llms/` vive dentro deste repositório, não em um diretório `hub/` separado
- `MCP_SETUP.md` é a referência transversal de MCP para Codex, Claude e Gemini
- `.agents/skills/` no root do workspace é a biblioteca canônica de skills
  compartilhadas entre providers
- o baseline compartilhado do Docker MCP vive em `/Users/philipegermano/code/config/mcp/`
- o antigo `_archive/` do root do workspace foi auditado; o conteúdo útil já
  absorvido vive em `context/`, `infrastructure/docs/` e `archive/`
- o diário pessoal por sessão vive no root do workspace em `/Users/philipegermano/code/daily/`
- `Jira` e `Confluence` são as superfícies-alvo de task, roadmap e especificação compartilhável
- `Notion` fica restrito ao Diário de Bordo
- roadmaps em `projects/*/ROADMAP.md` são mirrors de trabalho do workspace, não um segundo board canônico
- a configuração de runtime descoberta por convenção fixa continua no root do
  workspace; `config/` guarda apenas a configuração genérica compartilhada
- o bootstrap compartilhado da raiz continua em `WORKSPACE_BOOTSTRAP.md`
