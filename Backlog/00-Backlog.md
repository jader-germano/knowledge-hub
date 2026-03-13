# 📋 Backlog

> All open items. Updated each session.  
> Status: ✅ Done · 🟡 In Progress · 🔄 Waiting · 🔴 Blocked · 💡 Idea

---

## 🔴 Needs User Action

| Item | Blocker | Next |
|------|---------|------|
| Xcode license | `sudo xcodebuild -license accept` | unblocks `swift build`, `git`, `xcodegen` |
| VPS reinstall | hPanel → OS reinstall | → run `apply-all.sh` |
| OpenAI key | add to `~/.pi/agent/auth.json` | activates GPT tiers 4-5 |
| Gemini key | add to `~/.pi/agent/auth.json` | activates Gemini tiers 6-7 |

---

## 🔄 In Progress (waiting VPS)

| Item | File | Notes |
|------|------|-------|
| k8s deploy | `infrastructure/k8s/apply-all.sh` | ready — run after VPS reinstall |
| Ollama model pull | `k8s/jobs/ollama-pull-models.yaml` | pulls deepseek-r1:7b |
| pi-local-app deploy | `k8s/services/pi-local-app.yaml` | api.jpglabs.com.br |
| knowledge-hub deploy | `k8s/services/knowledge-hub.yaml` | hub.jpglabs.com.br |
| vault-sync CronJob | `k8s/services/knowledge-hub.yaml` | requires VAULT_GIT_TOKEN in hub-secrets |
| n8n WhatsApp bot | n8n workflow on VPS | import after n8n is up |
| Discord bot | n8n workflow on VPS | import after n8n is up |
| Email notifications | VPS mailserver | jader@jpglabs.com.br |
| memory sync | `scripts/sync-vault.sh` | run to push vault to GitHub |

---

## 🟡 Built — Needs Build Test

| Item | File | Blocker |
|------|------|---------|
| AwesomePie Mac | `~/code/pessoal/awesomepie/` | Xcode license |
| AwesomePie iOS | `~/code/pessoal/awesomepie-ios/` | Xcode license + xcodegen |
| knowledge-hub git | `~/code/pessoal/knowledge-hub/` | Xcode license (git) |

---

## ✅ Done

| Item | Notes |
|------|-------|
| Mac ChatService | Direct API calls — no pi subprocess |
| iOS ChatService | Direct API calls + VPS tier |
| iOS SettingsView | Full settings screen with test |
| pi-local-app/server.js | VPS-ready: env vars, 0.0.0.0 bind, large model |
| pi-local-app/Dockerfile | k8s-ready container |
| k8s manifests | All services: ollama, pi-local-app, n8n, portfolio |
| Traefik TLS config | Wildcard *.jpglabs.com.br via Cloudflare |
| apply-all.sh | One-command deploy |
| sync-memory.sh | Mac → VPS ConfigMap sync |
| architecture.md | Portfolio documentation |
| PAY_ON_DELIVERY.md | Codementor · Fiverr · Upwork · Contra |
| Job app AI rules | Local Ollama only — brutal-triad at end |
| pi-voice v2.1 | `~/bin/pi-voice` updated |
| Obsidian vault | knowledge-hub structure with connections |

---

## 💡 Ideas / Future

| Idea | Link | Priority |
|------|------|----------|
| Spring Boot AI backend (Spring AI + Ollama) | replaces Node.js pi-local-app | Medium |
| AwesomePie watch app | extend iOS companion | Low |
| Fine-tuned model on VPS | trained on Jader's codebase | Future |
| GitHub Actions CI/CD | auto-build portfolio + pi-local-app images | Medium |
| Passive income skill | Codementor profile, Fiverr gigs | High |
