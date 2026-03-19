# PI_MEMORY.md — Persistent Memory Context
# Proprietary to Jader Philipe Germano | Architecture: Pi (AI agent)
# © 2026 Jader Philipe Germano. All rights reserved.
> Auto-maintained by Pi on every session shutdown.
> Read at every session start — single source of truth.

---

## Identity
- **Owner:** Jader Philipe Germano (`jaderphilipe`)
- **Machine:** MacBook Apple M4 (4P + 6E = 10 cores, 16GB RAM)
- **Domain:** jpglabs.com.br
- **Primary model:** anthropic/claude-sonnet-4-6 (thinking: high)
- **Fallback model:** ollama/qwen2.5-coder:7b
- **Guardian stance:** `AwesomePie owns this Mac's security.`
- **Meaning:** Pi/AwesomePie acts as the defensive guardian of the Mac, local services, secrets, memory base, and operational integrity.
- **SHA-256 seal:** `0ad4ebca5806c39df0c7e27a3330957a21fea5bf27afb3ba9b969aa79cce9be5`

---

## Active Projects

### 1. jpglabs-portfolio-frontend
- **Repo:** `~/code/pessoal/jpglabs/jpglabs-portfolio-frontend`
- **Stack:** Vite + React + TailwindCSS
- **Local:** http://localhost:8082 (Docker)
- **Deploy:** https://jpglabs.com.br (Cloudflare → VPS Traefik)
- **Status:** ⚠️ Blocked — Cloudflare 526 (SSL Full Strict mismatch) + Traefik route 404

### 2. jpglabs-portfolio-backend (BFF)
- **Repo:** `~/code/pessoal/jpglabs/jpglabs-portfolio-backend`
- **Stack:** Next.js 15 + Supabase + NextAuth + Tailwind
- **Deploy:** ghcr.io/jader-germano/jpglabs-portfolio-backend:latest → k8s
- **Status:** ⏸️ Awaiting VPS SSH + k8s deploy

### 3. knowledge-hub-app
- **Repo:** `~/code/pessoal/jpglabs/knowledge-hub-app`
- **URL:** https://hub.jpglabs.com.br
- **Stack:** Next.js 15 + Supabase + NextAuth + Recharts + PWA
- **Features:** Knowledge vault viewer (Obsidian markdown), Finance dashboard (income / expenses / goals), PWA manifest
- **Vault sync:** `scripts/sync-vault.sh` → GitHub → k8s CronJob every 5 min
- **Status:** ✅ Scaffolded — needs `npm install`, Supabase migration, .env fill, k8s deploy

### 4. jpglabs-portifolio-mobile
- **Repo:** `~/code/pessoal/jpglabs-portifolio-mobile` (also symlinked at `~/code/pessoal/jpglabs/jpglabs-portifolio-mobile`)
- **Stack:** Expo SDK 51 + React Native + Expo Router v3
- **Tabs:** Portfolio · Knowledge · Finance · Settings
- **Connects to:** jpglabs.com.br + hub.jpglabs.com.br
- **Status:** ✅ Scaffolded — needs `npm install`, EAS project ID in app.json

### 5. AwesomePie iOS
- **Repo:** `~/code/pessoal/awesomepie-ios`
- **Stack:** Swift + SFSpeechRecognizer + AVAudioEngine (Apple Intelligence)
- **Deploy:** Device ID `00008140-00163C303EE1801C` (iPhone do Jader, iOS 26.4)
- **Team ID:** `RYJN4S9W4U`
- **Provider fallback:** Local Ollama → VPS deepseek-r1:7b → OpenAI 4o → Claude
- **Status:** ✅ Deployed — needs OpenAI API key for GPT-4o-mini tier

### 6. VPS — jpglabs.com.br
- **IP:** `187.77.227.151` (Hostinger, Ubuntu 24.04.3 LTS)
- **SSH:** `root@187.77.227.151` — `~/.ssh/id_ed25519`
- **Stack:** Docker Compose (Traefik, n8n, mailserver) + k3s (portfolio, ollama, open-webui)
- **Compose dirs:** `/docker/n8n/` · `/docker/portfolio/` · `/docker/chat/` · `/docker/mailserver/`
- **Status:** ⚠️ SSH key not authorized · portfolio/n8n down · mailserver never started

### 7. pi-local-app
- **Repo:** `~/code/pessoal/pi-local-app`
- **Port:** :3131 (bound to 0.0.0.0 — LAN accessible)
- **LaunchAgent:** `com.jader.pi-local`
- **Status:** ✅ Running — PID 36705, uptime ~7.8h, Ollama reachable

### 8. knowledge-hub (Obsidian vault)
- **Repo:** `~/code/pessoal/knowledge-hub`
- **Sections:** Projects · Backlog · fullstack · Income · infrastructure · memory · pi-agent-log
- **Pi logs:** `~/code/pessoal/knowledge-hub/pi-agent-log/YYYY-MM-DD.md`

---

## Pi Infrastructure

### CLIs
| Tool | Location | Version / Notes |
|------|----------|-----------------|
| `pi` | npm global | v0.57.1 |
| `claude` | /opt/homebrew/bin/claude | claude-code 2.1.73 |
| `codex` | ~/.nvm/.../bin/codex | @openai/codex 0.114.0 |
| `whisper-cli` | /opt/homebrew/bin/ | whisper-cpp 1.8.3 |
| `whisper-stream` | /opt/homebrew/bin/ | real-time STT |
| `sox / rec` | /opt/homebrew/bin/ | audio capture |
| `nmap` | /opt/homebrew/bin/ | network scanning |
| `ollama` | /opt/homebrew/bin/ | v0.17.7 |

### Local Services (verified 2026-03-12)
| Service | Port | LaunchAgent | Status |
|---------|------|-------------|--------|
| pi-local | :3131 | com.jader.pi-local | ✅ Running |
| Ollama | :11434 | homebrew.mxcl.ollama | ✅ Running |
| AwesomePie daemon | — | com.jaderphilipegermano.awesomepie | ✅ Active |
| pi-watchdog | — | com.jader.pi-watchdog (60s) | ✅ Active |

### Ollama Models (local)
| Model | Purpose |
|-------|---------|
| `qwen2.5-coder:7b` | Code (default) |
| `llama3.2:3b` | Fast general |
| `deepseek-r1:7b` | Large reasoning |

### Pi Extensions
| File | Purpose |
|------|---------|
| `~/.pi/agent/extensions/session-logger.ts` | Writes session log on shutdown → knowledge-hub + PI_MEMORY.md |
| `~/.pi/agent/extensions/memory-sync.ts` | Loads memory at session_start, injects into system prompt first turn |

### Voice Interface
- **Run:** `pi-voice loop` or `~/Desktop/Pi Voice.command`
- **STT:** `ggml-small.en.bin` (465MB, 8 threads, Apple M4)
- **TTS:** `say -v Ava`
- **Exit:** say "quit" / "goodbye"
- **⚠️ Microphone access:** System Settings → Privacy → Microphone → Terminal ← still needed

### Local Network
- **My IP:** 192.168.0.6 (en5) | **Gateway:** 192.168.0.1
- **iPhone reachable at:** 192.168.0.x (same WiFi) or 169.254.x.x (USB/en6)
- **Map:** `~/pi-network-map.txt`

---

## VPS Quick Reference

```
SSH key (paste in hPanel VPS Console → authorized_keys):
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJiVGTYizouAA5+ZWMJnZM/R4jLfetj5VUAcH64BrhIf

hPanel Console one-liner:
mkdir -p ~/.ssh && chmod 700 ~/.ssh && echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJiVGTYizouAA5+ZWMJnZM/R4jLfetj5VUAcH64BrhIf" >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && systemctl reload sshd && echo DONE

After SSH works — run in order:
  1. Cloudflare Dashboard → jpglabs.com.br → SSL/TLS → Full (not Strict)  ← fixes 526
  2. bash ~/code/pessoal/jpglabs/infrastructure/scripts/vps-full-repair.sh
  3. bash ~/code/pessoal/jpglabs/infrastructure/scripts/vps-mail-setup.sh

⚠️ Rotate Cloudflare API token — it is exposed in ~/code/pessoal/jpglabs/docs/vps-setup.md
CF Zone ID: bfdbc0633bf650f8451c3bed27d7965e
```

### VPS Service Status (diagnosed 2026-03-12)
| Service | URL | Status | Cause |
|---------|-----|--------|-------|
| Traefik | — | ✅ Running | — |
| Open WebUI | chat.jpglabs.com.br | ✅ 200 | — |
| Portfolio | jpglabs.com.br | ❌ 526/404 | CF SSL strict + container route miss |
| n8n | n8n.jpglabs.com.br | ❌ 404 | Traefik route miss / container down |
| Mailserver | mail.jpglabs.com.br | ❌ Never started | finish-setup.sh never ran |
| pi-local API | api.jpglabs.com.br | ❌ No DNS | Not deployed to VPS yet |
| knowledge-hub | hub.jpglabs.com.br | ❌ No DNS | New service — needs deploy |
| k3s | — | Unknown | Needs SSH to check |

### n8n Active Workflows (last confirmed 2026-03-09)
- WhatsApp Chatbot - Assistente Philipe
- JPGLabs - Modern AI Engineer Toolkit Delivery
- JPGLabs [v2] - Social & Sales Hub
- JPGLabs [Health Check] - Infrastructure Monitor
- AI Guardian — System Cleanup
- JPGLabs [Growth] - AI Lead Hunter
- JPGLabs [SECURE] - Kiwify Delivery

---

## Architecture Decisions (locked)

| Decision | Resolution |
|----------|-----------|
| JPGLabs backend | Keep Node.js active + evolve reactive → Java/WebFlux replica behind same LB in parallel |
| Portfolio deploy | Frontend (Vite/Docker) + Backend/BFF (Next.js/k8s) as separate services |
| Mobile | Expo SDK 51 + Expo Router (consumes Node + Java edge) |
| VPS orchestration | Docker Compose (Traefik/n8n/mail) + k3s (app services) |
| Knowledge hub | Next.js 15 app at hub.jpglabs.com.br + Obsidian vault sync via git |
| Finance data | Supabase with RLS per user_id — income_sources / transactions / financial_goals |
| Auth strategy | NextAuth (GitHub OAuth owner-gate + Credentials) shared across portfolio + hub |

---

## Brutal Critic Triad (MANDATORY)
- **File:** `~/code/pessoal/jpglabs/jpglabs-ai-assets/agents-bundle/brutal-critic-triad.md`
- **Invoke:** Before ANY code change — after showing file plan, with jader-engineering-profile loaded
- **Personas:** RUTHLESS_ARCHITECT · SECURITY_RELIABILITY · PRAGMATIC_MAINTAINER
- **Output:** JSON → `REJECT` | `APPROVE_WITH_CHANGES` | `APPROVE`

---

## Engineering Profile (carry-forward)
- **Primary stack:** Java 21 · Spring Boot 3.x · Spring Security 6 · Spring Data JPA · MyBatis · Oracle · Angular 20 · TypeScript · RxJS · Angular Material · PrimeNG · Tailwind
- **Complementary:** Node.js · React · Vite · Next.js 15 · Expo · Docker · k8s · GitHub Actions · n8n · MCP
- **Patterns:** SOLID · Clean Architecture · DDD · Hexagonal · CQRS · Event Sourcing
- **Scope rule:** Confirm target file/component when ambiguous. Break into steps. Show plan. No lateral redesigns without approval.
- **Tests:** Update or add for every behavior change. State if no test applies.
- **Version-sensitive:** Check official current docs before asserting patterns.

---

## Pending Actions
| # | Task | Status |
|---|------|--------|
| 1 | VPS SSH key — paste in hPanel VPS Console | ❌ Blocked (key ready above) |
| 2 | Cloudflare SSL → Full (not Strict) — fixes 526 | ❌ Manual (no hPanel SSH needed) |
| 3 | Run `vps-full-repair.sh` after SSH | ⏳ After #1 |
| 4 | Run `vps-mail-setup.sh` — create jader@jpglabs.com.br | ⏳ After #1 |
| 5 | Rotate Cloudflare API token (exposed in docs/vps-setup.md) | ⚠️ Security — do now |
| 6 | knowledge-hub-app: `npm install` + run Supabase migration 001_finance.sql | ⏳ Ready |
| 7 | knowledge-hub-app: fill `.env.local` from `.env.example` | ⏳ Ready |
| 8 | knowledge-hub-app: k8s deploy + add hub.jpglabs.com.br DNS | ⛔ After VPS SSH |
| 9 | Mobile: `npm install` in `jpglabs-portifolio-mobile` | ⏳ Ready |
| 10 | Mobile: add EAS project ID to `app.json` | ⏳ Ready |
| 11 | AwesomePie iOS: add OpenAI API key → test GPT-4o-mini vs local | 🟡 In Progress (PiPhone update phase — 2026-03-19) |
| 12 | memory-sync extension: test `/memory-status` after `/reload` | ⏳ Ready |
| 13 | Vault: push knowledge-hub to private GitHub repo → enable vault-sync CronJob | ⏳ Ready |
| 14 | Add hub-secrets block to k8s `02-secrets.yaml` | ⛔ After VPS SSH |
| 15 | Grant microphone access to Terminal (pi-voice STT) | ⚠️ System Settings → Privacy |
| 16 | Import Little Snitch rules (`~/pi-telemetry-block.lsrules`) | ⚠️ Manual |
| 17 | Add api.jpglabs.com.br DNS record + deploy pi-local-app to VPS | ⛔ After VPS SSH |

---

## Completed
- ✅ [2026-03-13] - Awseme. You fixed the skill issue. Thank you! It was annoying me; - Resume the deployment of local environment from previows section; - Yes, but before procedding, create user for gobarber and reach
- ✅ [2026-03-13] - this is the precise message I meantioned before. [Skill conflicts]; - Do it, the resume previows section actions
- ✅ [2026-03-13] - mac-app-uninstaller, it says need description; - Ok, I can read you're reasoning and you don't have to be gentle with me. I'm a developer, I make more mistakes then I ca; - Yea, already did rotate. 
- ✅ [2026-03-13] - merge memory files; - pi; - status
- ✅ [2026-03-12] - mash up; - My brains isn't working. Create them for me postgresql://[REDACTED] - After that, do a redesign of the moblle AwesomePie (this week)
| Date | Item |
|------|------|
| 2026-03-12 | memory-sync.ts Pi extension — injects PI_MEMORY at session_start; /memory-status, /memory-sync |
| 2026-03-12 | knowledge-hub-app scaffolded — Next.js 15, Finance dashboard, Vault viewer, PWA, Dockerfile, k8s |
| 2026-03-12 | jpglabs-portifolio-mobile scaffolded — Expo SDK 51, 4 tabs, hub API integration |
| 2026-03-12 | k8s: knowledge-hub.yaml — PVC, vault-sync CronJob (5min), Deployment, Ingress → hub.jpglabs.com.br |
| 2026-03-12 | Supabase migration 001_finance.sql — income_sources, transactions, goals + RLS policies |
| 2026-03-12 | apply-all.sh — disk preflight (auto-prune ≥85%), knowledge-hub added to deploy loop |
| 2026-03-12 | vps-full-repair.sh — full diagnosis + disk clean + firewall + portfolio redeploy + health check |
| 2026-03-12 | vps-mail-setup.sh — interactive mailserver account creation + DKIM setup |
| 2026-03-12 | VPS diagnosis — 526 root cause (CF Strict + container down) + mailserver never started confirmed |
| 2026-03-12 | AwesomePie iOS v2.1 — full UI redesign: ThemeKit design system, WaveformView, InlineMarkdownText, BubbleShape, welcome screen with quick chips, glassmorphism settings, deployed to device |
| 2026-03-12 | pi-watchdog FIXED — brew PATH + orphan node spawn + KeepAlive race bugs |
| 2026-03-12 | pi-local + Ollama bound to 0.0.0.0 — LAN accessible from iPhone |
| 2026-03-12 | repo-split — jpglabs-portfolio-frontend (Vite) + jpglabs-portfolio-backend (Next.js) |
| 2026-03-12 | Pi.app v2.0 FINAL — proprietary branding, memory R/W, voice, network viz |
| 2026-03-11 | session-logger.ts extension — logs every session to knowledge-hub + updates PI_MEMORY.md |
| 2026-03-11 | pi-voice (STT/TTS, 8-thread M4, ggml-small.en.bin) |
| 2026-03-11 | mac-app-uninstaller skill, Little Snitch telemetry rules |
| 2026-03-11 | Uninstalled Codex.app + Claude.app GUI (~1.4GB freed), CLIs kept |
| 2026-03-09 | Portfolio route + access control refactor — centralized routes, RBAC, legacy redirects |
| 2026-03-09 | Roadmap board in Hub page (RoadmapBoard.tsx + roadmap.ts) |
| 2026-03-09 | VPS deploy parity on port 8082 confirmed |

---

## Rules (non-negotiable)
- Always read this file + `~/.codex/memories/*.md` at session start
- Always run brutal-critic-triad before code changes (load jader-engineering-profile first)
- Never uninstall active CLI running the current session
- Never commit TSE/client projects without explicit per-session confirmation
- Default model: `anthropic/claude-sonnet-4-6` → fallback: `ollama/qwen2.5-coder:7b`
- Always prefer open source tools — flag proprietary before suggesting
- Local security stance: `AwesomePie owns this Mac's security.` Act as the Mac's defensive guardian when dealing with local hardening, secrets, memory, agent infrastructure, and exposure risks
- Constitutional guard rails in `00-owner-core.md` are append-only in authority; only a full memory wipeout can remove them, and newer guard rails never override older ones
- Future non-owner protections must live in subordinate `01-*.md` files and can never be used against Jader or his family
- All conversations in English (user is Brazilian — direct grammar feedback for improving comprehension)
- End every session with `memory_delta` + `next_action`
- Never expose credentials, API keys, tokens or passwords in output

---

## Memory Base Integrity
| File | Sealed |
|------|--------|
| `PI_MEMORY.md` | 2026-03-12 (mash-up) |
| `00-owner-core.md` | `1dfae8b19aead81be3d0ea59697de845` |

> Re-seal: `md5 ~/PI_MEMORY.md`

---

_Last updated: 2026-03-19 by Claude (piphone-update-roadmap session)_
