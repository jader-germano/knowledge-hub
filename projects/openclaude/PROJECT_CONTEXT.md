# PROJECT_CONTEXT — OpenClaude

> Open-source coding-agent CLI for cloud and local model providers.

## 1. Contexto Geral

- **Path no Workspace:** `/Users/philipegermano/code/openclaude`
- **Nicho:** CLI de agente de codificação baseado no *Claude Code*, mas aberto para múltiplos provedores (OpenAI, Gemini, Ollama, DeepSeek).
- **Missão:** Oferecer uma alternativa agnóstica de provedor ao *Claude Code* original, mantendo alta qualidade de ferramentas de sistema (bash, grep, file tools).

## 2. Tecnologias

- **Linguagem:** TypeScript
- **Runtime:** Bun (nativo) / Node.js (dist)
- **Framework de UI:** Ink (Terminal UI)
- **Provedores Suportados:**
  - Anthropic (Claude)
  - OpenAI (GPT-4o, etc.)
  - Google Gemini (Flash, Pro)
  - GitHub Models
  - Ollama (Local)
  - Codex (ChatGPT integration)

## 3. Estrutura Do Reposítório

- `src/` — Código fonte principal
  - `entrypoints/cli.tsx` — Ponto de entrada do CLI
  - `services/api/` — Shims de provedores (OpenAI, Codex, etc.)
  - `utils/providerProfile.ts` — Gerenciamento de perfis (`.openclaude-profile.json`)
- `bin/openclaude` — Launcher
- `scripts/` — Build, auditoria e doctor scripts
- `vscode-extension/` — Extensão integrada para VS Code

## 4. Workflows Operacionais

- **Build:** `bun run build`
- **Run:** `node dist/cli.mjs`
- **Diagnostics:** `bun run doctor:runtime`
- **Profiles:** `/provider` ou `bun run profile:init`

## 5. Status Atual

- [x] Repositório clonado e buildado
- [x] Runtime Bun instalado e validado
- [x] Suporte a Gemini verificado via source shims
- [x] Surface web ganhou `Workspace View` orientada a capability de MCP e handoff por agente

## 6. Prioridade Atual

- **Prioridade 0:** transformar o OpenClaude em um cockpit nativo de
  operabilidade para times agentic, em vez de manter a evolucao focada apenas
  em provedores e chat shell
- **Tese central:** handoff entre agentes precisa ser nativo no produto,
  baseado em `memory`, markdown por papel, readiness real de MCP e evidencias
  de entrega
- **Lanes principais:**
  - `Sistema`: `Workspace View`, dominios por agente, adapters nativos para
    `Jira`, `Figma`, `Git`, `GitHub/GitLab`, `Apple Speech` para transcript
    local, quality gates e proposals
  - `Renda`: empacotar o cockpit como oferta de operabilidade agentic depois
    que a trilha nativa estiver demoavel e repetivel

## 7. Próximos Passos

- [ ] consolidar `ROADMAP.md` do repo como surface oficial da prioridade de natividade
- [ ] conectar `Jira` e `Figma` como adapters nativos do contrato operacional
- [ ] definir e implementar a lane de transcript local com `Apple Speech` no macOS
- [ ] expor `GitLab/GitHub` e quality gates como readiness verificavel no cockpit
- [ ] manter a trilha de provedores subordinada a essa direcao de produto
