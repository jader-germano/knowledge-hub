# Claude Desktop App — Curated Context for Future Sessions
**Date:** 2026-03-07 | **Purpose:** Actionable automation & configuration reference

---

## 1. MCP Server Configuration

**Active MCP Server:**
```json
{
  "name": "MCP_DOCKER",
  "command": "docker",
  "args": ["mcp", "gateway", "run"]
}
```

**Usage Pattern:** Docker-based MCP gateway for extending Claude capabilities
**Next Step:** Integrate n8n workflows via MCP gateway for automation

---

## 2. Keyboard Shortcuts & Quick Entry

| Action | Shortcut | Use Case |
|--------|----------|----------|
| **Quick Entry** | `Cmd+Shift+Space` | Fast chat/command entry from anywhere |
| **Dictation** | `F5` | Voice input for quick notes/commands |

**Automation Opportunity:** F5 dictation useful for voice-to-text workflows on JPG Labs VPS

---

## 3. App Preferences

| Preference | Value | Impact |
|-----------|-------|--------|
| **Locale** | `pt-BR` (Portuguese Brazil) | UI language, number/date formats |
| **Theme Mode** | `system` | Follows macOS dark/light preference |
| **Sidebar** | `task` mode | Task-focused workflow |
| **Keep Awake** | Enabled | Prevents sleep during long operations |
| **Web Search** | Enabled (Cowork) | Real-time internet access in sessions |
| **Scheduled Tasks** | Enabled (both Cowork + Code) | Automation scheduling available |
| **Trusted Folder** | `/Users/jaderphilipe` | Local Agent Mode can access this directory |

**Automation Opportunities:**
- Scheduled Tasks enabled → can orchestrate periodic Claude Code runs
- Web Search enabled → can pull live data for n8n workflows
- Trusted folder spans all projects → safe for cross-project agents

---

## 4. Installed Extensions

### Chrome Control (ant.dir.ant.anthropic.chrome-control v0.1.5)

**Available Tools:**
```
- open_url(url)                    # Open URL in Chrome
- get_current_tab()                # Get active tab metadata
- list_tabs()                       # Enumerate all tabs
- close_tab(tab_id)                # Close specific tab
- switch_to_tab(tab_id)            # Switch focus to tab
- reload_tab(tab_id)               # Refresh tab
- go_back() / go_forward()         # Navigate history
- execute_javascript(code)         # Run JS in active tab
- get_page_content()               # Extract page text
```

**Practical Uses:**
- Automate browser-based workflows (e.g., scrape JPG Labs dashboards)
- Control Claude.ai tab directly from Claude Code
- Read page content for document processing
- Testing UI/UX scenarios programmatically

**Status:** Unsigned (registry source) — safe, no security concerns

---

## 5. Runtime & Local Agent Mode

### Claude Code Version
- **Current:** 2.1.63
- **Updated:** 2026-03-06 11:05
- **Usage:** Local code execution, project development

### Local Agents Available
1. **Default Agent** (`e2bfefd0-7d58-4043-922b-16b0136594ee`)
   - Created: 2026-03-02
   - Recommended for: General development tasks

2. **Skills Plugin** (`skills-plugin`)
   - Specialized: Custom skill/capability agent
   - Recommended for: Domain-specific automations (e.g., JPG Labs deployments)

### Virtual Machine (claudevm.bundle)
- **Size:** 9.7 GB
- **Purpose:** Linux sandbox for Claude Code execution
- **Last Active:** 2026-03-07 02:14
- **Architecture:** gVisor-based (secure containment)
- **Use Case:** Run untrusted code, database operations, Docker commands safely

---

## 6. Session Persistence

### Claude Code Sessions
- **Location:** `~/.claude-app/claude-code-sessions/`
- **Format:** JSON transcripts per session
- **Retention:** Automatic — indexed by UUID
- **Useful for:** Resuming interrupted tasks, session replay, audit trails

### Local Agent Mode Sessions
- **Agents:** 2 persistent agents configured
- **Auto-save:** Session state preserved between restarts
- **Useful for:** Background automation agents, scheduled task runners

---

## 7. Media Management

**Pending Uploads:** 6 images staged for upload
- Status: Ready
- Format: PNG (screenshots) + JPEG
- Total Size: ~661 KB
- Created: 2026-03-04 to 2026-03-06

**Action:** These are screenshot artifacts from previous sessions — ready to attach to Claude conversations

---

## 8. Integration Patterns for JPG Labs

### Pattern 1: Docker MCP Gateway + n8n
```
Claude Code (local)
  → MCP Docker Gateway
  → VPS /docker/n8n (n8n workflows)
  → External APIs / Email
```

**Use Case:** Orchestrate complex multi-step automation via n8n from Claude Code

### Pattern 2: Chrome Control + Data Extraction
```
Claude Code
  → Chrome Control (AppleScript)
  → JPG Labs dashboards (https://n8n.jpglabs.com.br)
  → Extract data → Process in Claude Code
```

**Use Case:** Monitor n8n workflows, extract execution logs, validate deployments

### Pattern 3: Scheduled Tasks + Local Agent
```
Cowork Scheduled Task (enabled)
  → Local Agent Mode (skills-plugin)
  → VPS SSH/API call
  → Database updates / Email notifications
```

**Use Case:** Nightly sync of JPG Labs data, weekly reports, health checks

---

## 9. Configuration Files to Back Up

**Critical files for setup recovery:**
```bash
# Config (small, essential)
~/.claude-app/claude_desktop_config.json     # MCP servers + shortcuts
~/.claude-app/config.json                    # Locale, theme, auth
~/.claude-app/window-state.json              # Layout (optional)

# Extensions state
~/.claude-app/extensions-installations.json  # Chrome Control version
~/.claude-app/extensions-blocklist.json      # (empty, safe)

# Automation state
~/.claude-app/claude-code-sessions/          # Session transcripts
~/.claude-app/local-agent-mode-sessions/     # Agent config
```

**Do NOT back up:**
```bash
# Large, auto-managed (will corrupt if copied while app running)
vm_bundles/claudevm.bundle                   # 9.7 GB VM
Cache/, IndexedDB/, Storage/, etc.           # Chromium internals
```

---

## 10. Recommended Next Steps

1. **Validate Docker MCP:** Test `docker mcp gateway run` connectivity
2. **Extend Chrome Control:** Build scripts using available tools for JPG Labs dashboards
3. **Configure Skills Plugin:** Set up domain-specific agent for infrastructure tasks
4. **Enable Scheduled Tasks:** Schedule weekly health checks via Local Agent Mode
5. **Document Workflows:** Record automation patterns in `~/.claude/automations/`
6. **Monitor VM Health:** Schedule monthly cleanup of sessiondata.img to keep VM responsive

---

## 11. Quick Reference — Useful Commands

```bash
# List current config
cat /Users/jaderphilipe/Library/Application\ Support/Claude/claude_desktop_config.json

# Check Claude Code version
ls -d /Users/jaderphilipe/Library/Application\ Support/Claude/claude-code/*/

# Monitor VM usage
du -sh /Users/jaderphilipe/Library/Application\ Support/Claude/vm_bundles/claudevm.bundle

# View recent sessions
ls -lrt /Users/jaderphilipe/Library/Application\ Support/Claude/claude-code-sessions/*/

# Extract pending uploads
ls /Users/jaderphilipe/Library/Application\ Support/Claude/pending-uploads/ | wc -l
```

---

## 12. Security & Privacy Notes

- **OAuth tokens:** Stored encrypted in `config.json` — safe
- **Session data:** JSON transcripts in `claude-code-sessions/` — may contain sensitive data
- **VM state:** 10GB image contains full Linux filesystem — handle with care
- **Chrome Control:** Unsigned but registry-verified — safe to use
- **MCP Gateway:** Docker-based isolation — requests limited to host capabilities

**Recommendation:** Encrypt backup files before storing on external media

---

*Context curated for automation planning and future session recovery. This document complements MANIFEST.md with actionable workflows and integration patterns.*
