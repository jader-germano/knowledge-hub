# Curated Context Delta (vs `AI-Context/CLAUDE.md`)

This file captures context extracted from Claude session markdown files that was not explicitly documented in `AI-Context/CLAUDE.md` before this import.

## New Context Added

1. Daily job automation operational details
- Primary repository: `github.com/jader-germano/daily-log` (private).
- Practical cadence observed in generated outputs: weekdays at `09:00`.
- Supporting operational note exists for one-time Git authentication (`SETUP_GIT.md` with PAT flow).

2. WhatsApp chatbot automation in n8n
- Workflow ID: `1w34rK2QP45XmmvE`.
- URL: `https://n8n.srv1443703.hstgr.cloud/workflow/1w34rK2QP45XmmvE`.
- 16-node architecture using GPT-4o-mini for message classification and response.
- Required credentials/secrets: OpenAI key, Meta WhatsApp token, Pushover token/user key, owner email.
- Integration dependencies: Meta webhook registration (`messages`), SMTP credential for summary email node.

## Imported Snapshots (for traceability)
- Legacy memory snapshot (`claude_memory_code.md`) from local-agent session output.
- Daily log samples (`README`, `resumo_diario`, `resumo_dia_04_03_2026`, `diario/2026-03-04`).
- Skill uploads (`daily-job-applications`, `sync-notes-to-notion`) preserved with source-local IDs.
