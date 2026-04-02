# Memory — Shared Pi And Session Context
> Proprietary to Jader Philipe Germano | Auto-synced every session shutdown

## Files
- [[PI_MEMORY.md]] — Main persistent memory ledger for the workspace
- [[AGENTS.md]] — Agent governance, skills, models
- [[sessions/]] — Per-session working memories (codex memories)
- [[logs/]] — Technical action logs and session sink

## Sync
Updated automatically by the `session-logger` Pi extension on every session shutdown.
Manual sync: `cp ~/PI_MEMORY.md /Users/philipegermano/code/jpglabs/docs/memory/PI_MEMORY.md`

## Status

- Este namespace é a memória incorporada e canônica do workspace.
- Sessões incorporadas vivem em `memory/sessions/`.
- Logs técnicos vivem em `memory/logs/`.
- Não criar variantes paralelas em `reports/`, mirrors legados ou outras raízes.
