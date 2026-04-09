# Claude Desktop App — Application Support Inventory
**Generated:** 2026-03-07 | **Source:** `/Users/jaderphilipe/Library/Application Support/Claude/`

---

## 1. Configuration Files

### `claude_desktop_config.json`
**MCP Servers:**
- **MCP_DOCKER** — Docker gateway runtime
  - Command: `docker`
  - Args: `["mcp", "gateway", "run"]`

**Preferences:**
- Locale: Portuguese (BR) — via `config.json`
- Theme: System default
- Quick Entry Shortcut: `Cmd+Shift+Space`
- Dictation Shortcut: `F5`
- Sidebar Mode: Task
- Keep Awake: Enabled
- Cowork Scheduled Tasks: Enabled
- Cowork Web Search: Enabled
- Claude Code Scheduled Tasks: Enabled
- Local Agent Mode Trusted Folder: `/Users/jaderphilipe`

### `config.json`
```json
{
  "locale": "pt-BR",
  "userThemeMode": "system",
  "hasTrackedInitialActivation": true
}
```
**Note:** Contains encrypted OAuth token cache (dxt allowlist + token)

### `window-state.json`
- Dimensions: 982×1018 px
- Position: (215, 40)
- Maximized: No
- Fullscreen: No
- Display bounds: 1710×1112

### `git-worktrees.json`
- Status: Empty (no git worktrees configured)

### `extensions-blocklist.json`
- Status: Empty (no extensions blocked)
- Last updated: 2026-03-07T07:14:06.557Z

---

## 2. Extensions Installed

### Chrome Control (`ant.dir.ant.anthropic.chrome-control`)
| Property | Value |
|----------|-------|
| **ID** | `ant.dir.ant.anthropic.chrome-control` |
| **Version** | 0.1.5 |
| **Status** | Unsigned (registry) |
| **Installed** | 2026-03-02T19:43:04.197Z |
| **Hash** | `cdf80805449e371c8b59b97168c7b5e29ef33432efd3e86c44a3bf08b205f40b` |

**Tools Provided:**
- `open_url` — Open URL in Chrome
- `get_current_tab` — Get active tab info
- `list_tabs` — List all tabs
- `close_tab` — Close specific tab
- `switch_to_tab` — Switch to a tab
- `reload_tab` — Reload tab
- `go_back` / `go_forward` — Navigate history
- `execute_javascript` — Run JS in current tab
- `get_page_content` — Get page text

**Description:** AppleScript-based Chrome automation for tab/window management and browser control

**Compatibility:**
- Claude Desktop: ≥0.10.0
- Platform: macOS only
- Node.js: ≥16.0.0

---

## 3. Runtime Directories

### `claude-code/`
- Version installed: **2.1.63**
- Last modified: 2026-03-06 11:05
- Purpose: Local Claude Code runtime

### `claude-code-sessions/`
- Session structure: `{uuid}/{org-id}/local_*.json`
- Active session: `e2bfefd0-7d58-4043-922b-16b0136594ee` (2026-03-04)
- Contains: Local session transcripts and state

### `local-agent-mode-sessions/`
- Sessions:
  - `e2bfefd0-7d58-4043-922b-16b0136594ee` (default agent)
  - `skills-plugin` (custom agent)
- Purpose: Persistent local agent mode state

### `vm_bundles/`
- Bundle: **claudevm.bundle** (Linux VM for Claude Code)
- Size: 9.7 GB
- Modified: 2026-03-07 02:14
- Contents:
  - `rootfs.img` — 10.7 GB (VM root filesystem)
  - `rootfs.img.zst` — 2.2 GB (compressed backup)
  - `sessiondata.img` — 136 MB (session state)
  - `efivars.fd` — 128 KB (UEFI variables)
  - `machineIdentifier`, `macAddress`, `vmIP`, `gvisorMacAddress` (VM metadata)

---

## 4. Pending Uploads

**Directory:** `pending-uploads/`
**Total files:** 6 images
**Status:** Ready to upload to Claude

| Filename | Size | Modified |
|----------|------|----------|
| `2c0bbd46-4b59-4078-bf7c-006e2ec7e0d2-1772828158469_CleanShot 2026-03-06 at 17.15.51.png` | 100K | 2026-03-06 17:15 |
| `2d97ddd8-2159-498d-9bf6-9b6be9f71034-1772828091937_CleanShot 2026-03-06 at 17.14.44@2x.png` | 138K | 2026-03-06 17:14 |
| `4512f2cb-e487-4f75-a6e2-52b771d428f4-1772610331884_6367A65B-ECD1-4297-A2CC-8EBEAD6B1CF7_4_5005_c.jpeg` | 39K | 2026-03-04 04:45 |
| `4b82a5ac-de5b-4747-8fdc-3cfa1b4810ad-1772828128404_CleanShot 2026-03-06 at 17.15.19.png` | 124K | 2026-03-06 17:15 |
| `5c76725f-cf9e-44bd-a568-925cae7c98d0-1772616128385_CleanShot 2026-03-04 at 06.12.06@2x.png` | 130K | 2026-03-04 06:22 |
| `f3cdc40b-6192-4588-8c0f-9096ec1224d6-1772828068901_CleanShot 2026-03-06 at 17.14.20@2x.png` | 130K | 2026-03-06 17:14 |

---

## 5. Internal/Chromium Directories (Do NOT Touch)

These are auto-managed Electron/Chromium internals — do not modify:

| Directory | Purpose | Notes |
|-----------|---------|-------|
| `blob_storage/` | Blob storage cache | Auto-managed |
| `Cache/` | HTTP cache | Auto-managed |
| `GPUCache/` | GPU cache | Auto-managed |
| `Crashpad/` | Crash reports | Auto-managed |
| `DawnGraphiteCache/` | Graphics cache | Auto-managed |
| `DawnWebGPUCache/` | WebGPU cache | Auto-managed |
| `IndexedDB/` | Indexed DB storage | Auto-managed |
| `VideoDecodeStats/` | Codec stats | Auto-managed |
| `WebStorage/` | DOM storage | Auto-managed |
| `Storage/` | Service worker storage | Auto-managed |
| `shared_proto_db/` | Protocol buffers | Auto-managed |
| `Dictionary/` | Spell check dict | Auto-managed |
| `sentry/` | Error tracking | Auto-managed |
| `Settings/` | Chromium settings | Auto-managed |

---

## 6. Key Observations

1. **Single Extension:** Only Chrome Control installed (for browser automation)
2. **No Git Worktrees:** Empty config — not actively used
3. **Linux VM Present:** claudevm.bundle is ~10GB, active as of 07/03/2026 02:14
4. **Encryption:** OAuth tokens stored encrypted in `config.json`
5. **Locale:** Brazilian Portuguese (`pt-BR`) — matches user preference
6. **MCP Gateway:** Docker-based MCP server configured for extensibility
7. **Local Agent Mode:** Two agents present (default + skills-plugin)
8. **Session History:** Claude Code sessions logged since 2026-03-04
9. **Pending Media:** 6 screenshots ready for upload (3/4/6 are CleanShot format, 1 is JPEG)

---

## 7. File Organization Summary

```
Application Support/Claude/
├── Config Files (6 JSON)
│   ├── claude_desktop_config.json     ✓ Read
│   ├── config.json                    ✓ Read
│   ├── extensions-installations.json  ✓ Read
│   ├── extensions-blocklist.json      ✓ Read
│   ├── window-state.json              ✓ Read
│   └── git-worktrees.json             ✓ Read
├── Extensions/                        (node_modules deps only)
├── Claude Extensions/                 (chrome-control code)
├── Runtime/
│   ├── claude-code/2.1.63/           (version directory)
│   ├── claude-code-sessions/         (1 session)
│   ├── local-agent-mode-sessions/    (2 agents)
│   └── vm_bundles/claudevm.bundle/   (9.7 GB Linux VM)
├── Media/
│   └── pending-uploads/              (6 PNG/JPEG images)
└── Chromium Internal/                (Cache, IndexedDB, Storage, etc. — DO NOT TOUCH)
```

---

*Inventory generated by automated scanner. No files were modified, deleted, or moved.*
