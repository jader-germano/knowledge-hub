# Agent Governance — Unified Memory Center
# Proprietary to Jader Philipe Germano | Architecture: Unified Memory Center

## Persistent Memory (Canonical)
- Always read canonical memory at session start:
  - `~/code/jpglabs/docs/memory/PI_MEMORY.md` (master ledger)
  - `~/code/jpglabs/docs/memory/AGENTS.md` (this file)
  - `~/code/jpglabs/docs/memory/MEMORY_SYNC.md` (sync protocol)
- Auto-updated on every session shutdown by session-logger extension.
- Cross-agent session logs: `~/code/jpglabs/docs/memory/sessions/{agent}/`

## pi-skills (Mario Zechner)
Shared across Pi, Claude Code, Codex, Amp, Droid.
Installed at: `~/pi-skills/`

| Skill | Description |
|-------|-------------|
| brave-search | Web search via Brave Search |
| browser-tools | Chrome DevTools automation |
| transcribe | Speech-to-text via Groq Whisper |
| youtube-transcript | YouTube transcript fetch |
| vscode | VS Code integration |
| gccli | Google Calendar CLI |
| gdcli | Google Drive CLI |
| gmcli | Gmail CLI |

## Workspace Skills
Canonical location: `~/code/.agents/skills/`

## Identity & Language
- Agent identity: `agent_master`
- All conversations in **English**. If user writes Portuguese, remind kindly.
- User is Jader Philipe Germano (Brazilian). Gentle spelling/grammar feedback.

## Execution Model
1. Prefer existing skills from `~/code/.agents/skills/` (canonical) or `~/pi-skills/`
2. Runtime wrappers live in `~/.claude/skills/` (synced via `sync_shared_skills.py`)
3. Combine skills only when genuinely multi-domain
4. Create a new skill for recurring capability with no home
5. Do NOT fragment into multiple pseudo-agents

## Skill Registry
| Skill | Location | Purpose |
|-------|----------|---------|
| `brave-search`              | `~/pi-skills/brave-search/` | Web search via Brave |
| `browser-tools`             | `~/pi-skills/browser-tools/` | Chrome DevTools automation |
| `transcribe`                | `~/pi-skills/transcribe/` | Speech-to-text via Groq Whisper |
| `youtube-transcript`        | `~/pi-skills/youtube-transcript/` | YT transcripts |
| `email-daily-triage`        | `~/code/.agents/skills/email-daily-triage/` | Email triage |
| `github-activity-digest`    | `~/code/.agents/skills/github-activity-digest/` | GitHub digest |
| `income-roadmap-scanner`    | `~/code/.agents/skills/income-roadmap-scanner/` | Monetization scanner |
| `infra-health-check`        | `~/code/.agents/skills/infra-health-check/` | VPS/infra health |
| `job-opportunities-scanner` | `~/code/.agents/skills/job-opportunities-scanner/` | Job scanner |
| `relatorio-mensal-tse`      | `~/code/.agents/skills/relatorio-mensal-tse/` | TSE monthly report |
| `teams`                     | `~/code/.agents/skills/teams/` | Agent team orchestration |
| `memory-sync`               | `~/.claude/skills/memory-sync/` | Cross-agent memory sync |
| `scraper`                   | `~/.claude/skills/scraper/` | URL scraping |
| `session-init`              | `~/.claude/skills/session-init/` | Session machine ID |
| `chatgpt-apps`              | `~/.codex/skills/chatgpt-apps/` | ChatGPT Apps SDK / MCP |

## Agent Bundle
| Agent | Status | Trigger |
|-------|--------|---------|
| `brutal-critic-triad` | **archived** — path removed from workspace | Was: pre-code review |
| `knowledge-curator`   | **archived** | Was: knowledge capture |
| `n8n-workflow-architect` | **archived** | Was: n8n design |
| `mcp-integration-architect` | **archived** | Was: MCP/tools |
| `ui-design-crafter`   | **archived** | Was: UI/UX |
| `jpglabs-dev-agent`   | **archived** | Was: JPGLabs dev |

> Legacy agent bundles were at `~/code/pessoal/jpglabs/jpglabs-ai-assets/agents-bundle/`.
> Path no longer exists. Skills that survive are now in `~/code/.agents/skills/` or `~/.claude/skills/`.

## Scheduled Agents (Claude)
| Agent | Schedule |
|-------|----------|
| `diario-de-bordo-diario` | Daily |
| `daily-job-applications` | Daily |
| `relatorio-atividades-digisystem-mensal` | Monthly |
| `sync-notes-to-notion` | Daily |
| `claude-code-release-digest` | Weekly |

## Models
- **Primary:** `anthropic/claude-opus-4-6` or `openai-codex/gpt-5.4` (thinking: high)
- **Fallback:** `anthropic/claude-sonnet-4-6`
- **Local (M4):** Ollama `qwen2.5-coder:7b` or `gemma4:e4b` → http://localhost:11434
- **VPS (Tailscale):** Ollama `gemma4:e4b` or `qwen2.5-coder:14b` → http://100.68.217.36:11434
- **Cloud free:** Google Gemini `gemini-3.1-flash-preview`, OpenRouter `nemotron-3-super-free`
- **Voice:** `pi -p` → gpt-5.4

## CPU Policy (Apple M4: 4P + 6E)
- Whisper STT: 8 threads (4P + 4E)
- Ollama: 4 threads (P-cores)
- Reserve: 2 E-cores always free

## Pre-Implementation Checklist
1. Confirm file/component when ambiguous
2. Show file plan before editing
3. Update tests with every behavior change
4. Verify version-sensitive patterns against official docs

## Commit Policy
- Personal projects: commit after each stable implementation
- TSE projects: NEVER commit without explicit user confirmation

## Session Output
End every session with:
- `memory_delta`: what changed
- `next_action`: what comes next
