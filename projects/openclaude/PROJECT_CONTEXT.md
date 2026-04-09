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

## 6. Próximos Passos

- [ ] Integrar configuração de Gemini com o novo modelo `Gemini 3 Flash`
- [ ] Validar execução de ferramentas em modo bare
- [ ] Indexar na governança global do workspace
