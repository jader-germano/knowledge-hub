# 🏠 JPGLabs — Workspace Docs And Memory

> **Owner:** Jader Philipe Germano  
> **Updated:** auto-synced by session-logger  
> **Stack:** Java · Spring Boot · Angular · Swift · k3s · Ollama

---

## 🗺️ Map of Content

### 🚀 Active Projects
- [[Projects/AwesomePie]] — Native Swift macOS + iOS AI assistant
- [[Projects/JPGLabs-Portfolio]] — jpglabs.com.br (Next.js + Supabase)
- [[Projects/Pi-Agent]] — Local AI agent (pi CLI + Ollama)
- [[Projects/VPS-Infrastructure]] — k3s on Hostinger VPS

### 💰 Income
- [[Income/Pay-On-Delivery]] — Codementor · Fiverr · Upwork · Contra
- [[Income/Job-Applications]] — Daily pipeline (local AI → brutal-critic-triad)

### 📋 Backlog
- [[Backlog/00-Backlog]] — All open items with status

### 🧠 Memory
- [[PI_MEMORY.md]] — Persistent agent memory
- [[AGENTS.md]] — Agent governance

---

## ⚡ Quick Status

| Item | Status |
|------|--------|
| VPS reinstall | 🔄 In progress |
| AwesomePie Mac | 🟡 Built — needs `xcodebuild -license accept` |
| AwesomePie iOS | 🟡 Built — needs `xcodegen generate` |
| k8s manifests | ✅ Ready to deploy |
| pi-local-app | ✅ VPS-ready (server.js updated) |
| iOS SettingsView | ✅ Written |
| Mac ChatService | ✅ Direct API calls (no subprocess) |
| workspace docs git | 🔴 Blocked — `git` needs Xcode license |

---

## 🔗 Connections

```
AwesomePie ──uses──► pi-local-app ──calls──► Ollama (Mac / VPS)
AwesomePie ──falls back──► OpenAI / Gemini / Anthropic

Pi-Agent ──reads──► PI_MEMORY.md ──synced to──► VPS ConfigMap
Pi-Agent ──runs──► n8n workflows ──triggers──► WhatsApp / Discord / Email

VPS-Infrastructure ──serves──► api.jpglabs.com.br (pi-local-app)
VPS-Infrastructure ──serves──► n8n.jpglabs.com.br
VPS-Infrastructure ──serves──► chat.jpglabs.com.br (Open-WebUI)
VPS-Infrastructure ──serves──► jpglabs.com.br (portfolio)

Job-Applications ──generate──► local Ollama (free)
Job-Applications ──validate──► brutal-critic-triad (paid, end only)
```
