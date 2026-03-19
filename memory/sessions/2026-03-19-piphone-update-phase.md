# 2026-03-19 — PiPhone Update Phase

**Branch:** `claude/piphone-update-roadmap-uZs8j`
**Triggered by:** Jader — "connect to Pi and start the faze to update the PiPhone"

---

## Context

AwesomePie iOS (PiPhone) is at v2.1, deployed to device `00008140-00163C303EE1801C` (iPhone do Jader, iOS 26.4).
It works on tiers 1–2 (local Ollama) and tier 8 (Anthropic fallback). Tiers 3–7 are blocked pending keys and VPS.

**Pi local-app (:3131):** Not reachable from cloud session. Runs on Mac — connect from Mac terminal.

---

## Phase Goal

Bring AwesomePie iOS to full operational state across the complete 8-tier fallback chain.

---

## Steps

| # | Task | Status | Gate |
|---|------|--------|------|
| 1 | `sudo xcodebuild -license accept` | ⏳ Waiting (Jader) | Manual |
| 2 | `xcodegen generate` in `~/code/pessoal/awesomepie-ios` | ⏳ After #1 | Xcode license |
| 3 | Add OpenAI API key to `~/.pi/agent/auth.json` | ⏳ Waiting (Jader) | Manual |
| 4 | Test GPT-4o-mini (tier 5) on device | ⏳ After #3 | OpenAI key |
| 5 | Add Gemini key to auth.json | ⏳ Waiting (Jader) | Manual |
| 6 | Test Gemini Flash/Pro tiers (6-7) on device | ⏳ After #5 | Gemini key |
| 7 | VPS SSH + deploy pi-local-app (tier 3) | ⏳ Blocked | VPS SSH access |
| 8 | Full chain smoke test: tiers 1→8 on iPhone | ⏳ Final | All above |

---

## Fallback Chain Reference

```
1. Local Ollama      localhost:3131         qwen2.5-coder:7b   ✅ Active
2. Local Ollama      localhost:3131         llama3.2:3b         ✅ Active
3. VPS               api.jpglabs.com.br     deepseek-r1:7b      ❌ VPS SSH blocked
4. OpenAI            api.openai.com         gpt-4o              ❌ Key missing
5. OpenAI            api.openai.com         gpt-4o-mini         ❌ Key missing
6. Gemini            googleapis.com         gemini-2.0-flash    ❌ Key missing
7. Gemini            googleapis.com         gemini-1.5-pro      ❌ Key missing
8. Anthropic         api.anthropic.com      claude-sonnet-4-6   ✅ Active
```

---

## Pi Connection Note

Pi local-app is a Mac-local process (LaunchAgent `com.jader.pi-local`).
To verify connectivity from the Mac:

```bash
curl http://localhost:3131/health
# or
curl http://192.168.0.6:3131/health   # from iPhone on same WiFi
```

---

_Opened: 2026-03-19 by Claude (piphone-update-roadmap session)_
