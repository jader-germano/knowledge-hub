# MCP Setup

Referência canônica de MCP para o workspace JPG Labs.

## Entrypoints

- Workspace root: `$WORKSPACE_ROOT`
- Cliente MCP: `$WORKSPACE_ROOT/.mcp.json`
- Config compartilhada: `$WORKSPACE_ROOT/config/mcp/docker-mcp-config.yaml`
- Catálogo compartilhado: `$WORKSPACE_ROOT/config/mcp/docker-mcp-shared-catalog.yaml`

## Baseline Validada

Baseline atual orientada a desenvolvimento de software, revisão, arquitetura e
debug:

- `git` — diffs, histórico, branches e staging
- `filesystem` — leitura/escrita controlada no workspace
- `desktop-commander` — operações locais e apoio operacional
- `docker` — inspeção de containers e do próprio gateway
- `playwright` — validação de UI e fluxos web
- `fetch` — recuperação documental/web
- `context7` — documentação atualizada de bibliotecas e frameworks
- `memory` — memória compartilhada entre providers
- `sequentialthinking` — raciocínio estruturado para arquitetura e debugging
- `ast-grep` — revisão estrutural e lint orientado a AST

## Lanes Condicionais

- `semgrep` — OAuth autorizado no host, mas ainda fora do baseline enquanto o
  `dry-run` falhar em `initialize`
- `sonarqube` — fora do baseline até existir `SONARQUBE_URL`, `SONARQUBE_ORG`
  e `SONARQUBE_TOKEN`
- `figma` — integração mantida fora do catálogo Docker; usar plugin/app do
  runtime

## Regras Práticas

- só promover um servidor para `.mcp.json` depois de `dry-run` verde no host
- tratar `origin` deste repositório como fonte canônica da documentação MCP do
  workspace
- registrar o bootstrap por provider em `llms/`
- registrar o contexto do próprio repositório privado em
  `Projects/Knowledge-Hub.md`
