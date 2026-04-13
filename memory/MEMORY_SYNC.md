# MEMORY_SYNC.md — Unified Memory Center Protocol

> Cross-agent memory synchronization for Pi, Claude, Codex, and OpenClaude
> Proprietary to Jader Philipe Germano | Architecture: Unified Memory Center

---

## Overview

This document defines the protocol for a unified memory center that all agents
(Pi, Claude, Codex, OpenClaude) read from and write to. The goal is one
canonical source of truth in Markdown, with session logging and memory sync
extensions for each agent.

## Canonical Memory Root

```
~/code/jpglabs/docs/memory/
├── MEMORY_SYNC.md       # This protocol
├── PI_MEMORY.md         # Master ledger (identity, projects, pending actions)
├── AGENTS.md            # Agent governance, skills, models
├── SESSION_PROTOCOL.md   # Per-session memory contract
├── sessions/            # Per-agent session logs
│   ├── pi/
│   ├── claude/
│   ├── codex/
│   └── openclaude/
└── logs/                # Technical action logs
```

## Core Principle

**Progressive Disclosure over MCP Bulk**

Mario Zechner's Pi philosophy: Instead of dumping full tool schemas into
context (MCP style - 13-18k tokens), use CLI tools with READMEs that agents
read when needed. Token cost paid only when the tool is actually used.

- No built-in to-dos → use `TODO.md`
- No built-in plans → use `PLAN.md`
- No sub-agents with black-box context → spawn via bash with full observability
- Memory = single Markdown ledger + session logs

## Memory Delta Protocol

Every agent writes the following at session shutdown:

```markdown
## {timestamp} — {agent} Session

### Memory Delta
- Changed: {what changed in PI_MEMORY.md}
- Decided: {key decisions}
- Blockers: {open blockers}

### Next Action
- {concrete next step}

### Session Stats
- Duration: {time}
- Commands: {count}
- Files: {count}
```

## Agent Extensions

### 1. memory-sync.ts

Loads `PI_MEMORY.md` at session start and injects into system prompt.

**Location per agent:**
- Pi: `~/.pi/agent/extensions/memory-sync.ts`
- Claude: `~/.claude/extensions/memory-sync.ts`
- Codex: `~/.codex/extensions/memory-sync.ts`

### 2. session-logger.ts

Writes session log on shutdown to:
- `jpglabs/docs/memory/sessions/{agent}/{yyyy-mm-dd}-{hhmm}.md`
- Updates `jpglabs/docs/memory/logs/`

**Location per agent:**
- Pi: `~/.pi/agent/extensions/session-logger.ts`
- Claude: `~/.claude/extensions/session-logger.ts`
- Codex: `~/.codex/extensions/session-logger.ts`

## pi-skills Integration

Mario Zechner's skills are compatible with Pi, Claude Code, Codex, Amp, and Droid.

**Clone once:**
```bash
git clone https://github.com/badlogic/pi-skills ~/pi-skills
```

**Legacy model (kept only for provider-only `pi-skills` compatibility):**
```bash
# Provider-only skills may still be mirrored from `~/pi-skills/` when needed.
# Do not use symlink as the canonical path for the Claude runtime bootstrap.
```

**Current workspace model:**
```bash
# Shared workspace skills -> Claude runtime without replacing unmanaged skills
python3 /Users/philipegermano/code/.agents/scripts/sync_shared_skills.py \
  --target-root /Users/philipegermano/.claude/skills \
  --preserve-unmanaged

# Shared workspace skills -> workspace bootstrap wrappers
python3 /Users/philipegermano/code/.agents/scripts/sync_shared_skills.py
```

## Skills Available from pi-skills

| Skill | Description | Token Cost |
|-------|-------------|------------|
| brave-search | Web search via Brave Search | Paid on use |
| browser-tools | Chrome DevTools automation | Paid on use |
| gccli | Google Calendar CLI | Paid on use |
| gdcli | Google Drive CLI | Paid on use |
| gmcli | Gmail CLI | Paid on use |
| transcribe | Speech-to-text via Groq Whisper | Paid on use |
| vscode | VS Code integration | Paid on use |
| youtube-transcript | YouTube transcript fetch | Paid on use |

## Workspace Skills

Canonical workspace skills live in:
```
~/code/.agents/skills/
```

These are shared across all agents via `additionalDirectories` in settings.

## Session Handoff Contract

When switching between agents, the receiving agent should:

1. Read `PI_MEMORY.md` for context
2. Read `sessions/{previous-agent}/` for recent work
3. Check `logs/` for technical notes
4. Check `AGENTS.md` for governance rules

## No MCP Anti-Pattern

MCP servers like Playwright (21 tools, 13.7k tokens) or Chrome DevTools (26 tools, 18k tokens)
dump their entire tool descriptions into context on every session. That's 7-9% of your
context window gone before you even start working.

**Alternative:** CLI tools with READMEs. The agent reads the README when it needs the tool,
pays the token cost only when necessary (progressive disclosure).

## Files and Permissions

| File | Read By | Written By |
|------|---------|------------|
| PI_MEMORY.md | All agents | All agents |
| sessions/*/ | All agents | Respective agent |
| logs/ | All agents | All agents |
| AGENTS.md | All agents | Owner only |
| .agents/skills/* | All agents | Owner only |

## Sync on Startup

Each agent extension loads memory in this order:
1. `PI_MEMORY.md`
2. `AGENTS.md`
3. Recent session logs from `sessions/{agent}/`
4. Recent logs from `logs/`

## Maintenance

- Daily: Session logs consolidated
- Weekly: PI_MEMORY.md reviewed and sealed
- Monthly: Full memory audit and cleanup

---

_Last updated: 2026-04-07_
