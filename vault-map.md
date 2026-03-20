# 🗂️ Knowledge Hub — Visual Map
> JPGLabs · Owner: Jader Philipe Germano
> Auto-reference for navigation and agent context

---

```
knowledge-hub/
│
├── 🏠 Home.md                          ← Dashboard · quick status · connection diagram
├── README.md                           ← Brief intro
│
├── Projects/                           ← ACTIVE PROJECTS
│   ├── AwesomePie.md                   ← Swift macOS + iOS AI assistant · fallback chain
│   ├── PiPhone-UX-Design.md            ← ← UX design system · tokens · screens · components
│   └── VPS-Infrastructure.md           ← k3s on Hostinger · Docker Compose · deploy guide
│
├── Backlog/
│   └── 00-Backlog.md                   ← All open items · 🟡🔴✅🔄💡 status badges
│
├── infrastructure/
│   └── portfolio-k3s.md                ← k3s architecture · Traefik · manifests walkthrough
│
├── memory/                             ← AGENT PERSISTENT STATE
│   ├── PI_MEMORY.md                    ← ★ Single source of truth · read every session
│   ├── AGENTS.md                       ← Skill registry · bundles · scheduled agents
│   ├── README.md                       ← Memory sync docs
│   └── sessions/                       ← Per-session working memory
│       ├── 00-owner-core.md            ← ★ CONSTITUTIONAL LAYER · append-only authority
│       ├── 2026-03-09-jpglabs-roadmap-diagnostics-and-8082-deploy.md
│       ├── 2026-03-09-portfolio-route-access-control.md
│       ├── 2026-03-09-docentes-working-principles.md
│       ├── 2026-03-10-user-engineering-scope-and-docs-first.md
│       ├── 2026-03-12-pi-v2-install.md
│       ├── 2026-03-12-infrastructure-fixes.md
│       ├── 2026-03-12-awesomepie-ios-patterns.md
│       └── 2026-03-19-piphone-update-phase.md  ← PiPhone update · tier chain · steps
│
└── pi-agent-log/                       ← TECHNICAL ACTION LOGS
    ├── README.md
    ├── technical-actions.md
    ├── 2026-03-11.md
    ├── 2026-03-12.md
    └── 2026-03-13.md
```

---

## Connection Graph

```
                      ┌─────────────────────────────┐
                      │      PI_MEMORY.md  ★         │
                      │   (single source of truth)   │
                      └──────────┬──────────────────┘
                                 │ informs
              ┌──────────────────┼──────────────────┐
              ▼                  ▼                   ▼
     Projects/             Backlog/            sessions/
   AwesomePie.md         00-Backlog.md      (per-session)
   PiPhone-UX.md
   VPS-Infra.md
              │
              │ implements
              ▼
     ┌──────────────────────┐     ┌─────────────────────┐
     │  AwesomePie iOS      │     │  jpglabs-portfolio  │
     │  ~/code/awesomepie-  │     │  ~/code/jpglabs/    │
     │  ios  (Swift)        │     │  (Vite + Next.js)   │
     └──────────┬───────────┘     └─────────────────────┘
                │ connects to
                ▼
     ┌──────────────────────┐
     │  pi-local-app :3131  │ ──► Ollama :11434 (local models)
     │  (Node.js LAN API)   │ ──► VPS api.jpglabs.com.br
     └──────────────────────┘
```

---

## Reading Order (new session)

1. `memory/PI_MEMORY.md` — load full context
2. `memory/sessions/00-owner-core.md` — constitutional rules
3. `Backlog/00-Backlog.md` — current work state
4. Relevant `Projects/*.md` for the session task

---

_Last updated: 2026-03-19_
