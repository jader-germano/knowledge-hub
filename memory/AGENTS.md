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
1. Prefer existing skills from `~/.pi/agent/skills/` or `~/.codex/skills/`
2. Combine skills only when genuinely multi-domain
3. Create a new skill for recurring capability with no home
4. Do NOT fragment into multiple pseudo-agents

## Skill Registry
| Skill | Location | Purpose |
|-------|----------|---------|
| `jader-engineering-profile` | `~/.codex/skills/jader-engineering-profile/` | Java/Spring/Angular stack |
| `passive-income-architect`  | `~/.codex/skills/passive-income-architect/` | Monetization |
| `chatgpt-apps`              | `~/.codex/skills/chatgpt-apps/` | ChatGPT Apps SDK / MCP |
| `jpglabs-vps-ops`           | `~/.pi/agent/skills/jpglabs-vps-ops/` | VPS SSH/Docker/Traefik |
| `mac-app-uninstaller`       | `~/.pi/agent/skills/mac-app-uninstaller/` | macOS app cleanup |
| `brave-search`              | `~/pi-skills/brave-search/` | Web search |
| `transcribe`                | `~/pi-skills/transcribe/` | Speech-to-text |
| `youtube-transcript`        | `~/pi-skills/youtube-transcript/` | YT transcripts |
| `browser-tools`             | `~/pi-skills/browser-tools/` | Chrome automation |

## Agent Bundle
| Agent | Location | Trigger |
|-------|----------|---------|
| `brutal-critic-triad` ← **MANDATORY pre-code** | `~/code/pessoal/jpglabs/jpglabs-ai-assets/agents-bundle/brutal-critic-triad.md` | Before any code change |
| `knowledge-curator`   | `…/agents-bundle/knowledge-curator.md` | Knowledge capture |
| `n8n-workflow-architect` | `…/agents-bundle/n8n-workflow-architect.md` | n8n design |
| `mcp-integration-architect` | `…/agents-bundle/mcp-integration-architect.md` | MCP/tools |
| `ui-design-crafter`   | `…/agents-bundle/ui-design-crafter.md` | UI/UX |
| `jpglabs-dev-agent`   | `…/agents-bundle/jpglabs-dev-agent/SKILL.md` | JPGLabs dev |

## Scheduled Agents (Claude)
| Agent | Schedule |
|-------|----------|
| `diario-de-bordo-diario` | Daily |
| `daily-job-applications` | Daily |
| `relatorio-atividades-digisystem-mensal` | Monthly |
| `sync-notes-to-notion` | Daily |
| `claude-code-release-digest` | Weekly |

## Models
- **Primary:** `openai-codex/gpt-5.4` (thinking: high)
- **Fallback:** `anthropic/claude-sonnet-4-6`
- **Local fast:** Ollama `llama3.2:3b` → http://localhost:11434
- **Local code:** Ollama `qwen2.5-coder:7b` → http://localhost:11434
- **Voice:** `pi -p` → gpt-5.4

## CPU Policy (Apple M4: 4P + 6E)
- Whisper STT: 8 threads (4P + 4E)
- Ollama: 4 threads (P-cores)
- Reserve: 2 E-cores always free

## Pre-Implementation Checklist
1. Confirm file/component when ambiguous
2. Show file plan before editing
3. **Run brutal-critic-triad** → `…/agents-bundle/brutal-critic-triad.md`
4. Update tests with every behavior change
5. Verify version-sensitive patterns against official docs

## Commit Policy
- Personal projects: commit after each stable implementation
- TSE projects: NEVER commit without explicit user confirmation

## Session Output
End every session with:
- `memory_delta`: what changed
- `next_action`: what comes next
