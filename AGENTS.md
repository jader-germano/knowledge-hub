# AGENTS.md

General guide for agents working in the workspace rooted at:

`/Users/philipegermano/code`

## Workspace Layout

- `jpglabs/docs/`: only canonical documentation hub, MCP setup,
  handoff protocol, markdown classification, shared `llms/`
- `jpglabs/imap-server/`: standalone MCP mail project separated from the docs layer
- `jpglabs/apple-study-checklist/`: SwiftUI project
- `jpglabs/knowledge-hub-app/`: web app for the workspace hub
- `jpglabs/pi-local-app/`: local Pi runtime and AI API surface
- `jpglabs/portfolio-backend/`: portfolio and Pi web surface
- `jpglabs/portfolio-mobile/`: portfolio mobile client
- `jpglabs/piphone-ios/`: iOS client related to the Pi ecosystem
- `jpglabs/pibar-macos/`: macOS client related to the Pi ecosystem
- `jpglabs/PieCenter/`: unified Apple shell under active construction
- `jpglabs/docs/tools/`: imported active artifacts from legacy orchestration
- `jpglabs/docs/archive/legacy-repos/`: archived repositories and legacy snapshots
- `FrankMD/`: filesystem-first Rails application
- `Playground 2/`: experimental sandbox

## Workspace Rules

- No symlinks are part of the intended workspace topology.
- Physical repositories in `code/` are the main locations for code.
- `jpglabs/docs/` keeps the shared markdown classification, MCP rules,
  cross-agent handoff notes, and the shared `llms/` directory.
- `ai-orchestration-hub` is no longer an active standalone hub.
- Shared ownership and bootstrap rules are canonical in:
  - `WORKSPACE_INDEX.md`
  - `OWNERSHIP.md`
  - `RULES.md`
  - `manifests/workspace.index.yaml`
- When the workspace topology changes, update:
  - `README.md`
  - `MCP_SETUP.md`
  - `CLAUDE.md`
  - `GEMINI.md`
  - `WORKSPACE_INDEX.md`
  - `manifests/workspace.index.yaml`

## Agent Coordination

- Codex, Claude, Gemini e demais agentes compartilham handoff através de:
  - `agents/AGENT_BRIDGE.md`
  - `agents/SESSION_CLOSE_TEMPLATE.md`
- A ordem canônica de resolução do workspace é:
  - `RULES.md`
  - `OWNERSHIP.md`
  - `WORKSPACE_INDEX.md`
  - `manifests/workspace.index.yaml`
- Skills compartilhadas devem ser resolvidas pelo índice:
  - `manifests/skills.index.yaml`
- Pastas de provedor como `.codex/`, `.claude_code/` e `.gemini/` devem servir
  apenas como bootstrap local mínimo.
- Use factual file references from the workspace before relying on remembered
  paths or obsolete repo locations.

## Documentation Discipline

- Keep markdown references classified in the hub.
- If a markdown file becomes a shared reference for a project or workflow,
  reflect it in the hub and in the manifests or indexes do próprio hub.
- Avoid turning the hub into a runtime dump of logs, caches, or ephemeral state.

## Companion Containers

- `FrankMD` pode ser usado como companion de leitura e edição documental.
- O wrapper recomendado é `scripts/fed-safe.sh`.
- O wrapper melhora higiene operacional, mas não substitui isolamento real.
- Para Docker, o controle mais importante continua sendo:
  - escopo do diretório montado
  - modo somente leitura quando aplicável
  - evitar mount bruto do workspace inteiro quando um recorte curado basta
