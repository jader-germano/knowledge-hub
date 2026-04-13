# Agent Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar e deployar na VPS um dashboard web single-page com live update mostrando o status dos agentes (Claude, Codex, Gemini, OpenClaude, Pi) operando no workspace.

**Architecture:** rsync periódico do Mac para a VPS sincroniza os arquivos `.md` (daily/, AGENT_BRIDGE.md, WORKSPACE_INDEX.md); um backend FastAPI na VPS lê esses arquivos e expõe endpoints JSON; o frontend HTML com Alpine.js consome a API via polling a cada 30s e renderiza os painéis de status, timeline, projetos e infraestrutura.

**Tech Stack:** Python 3.11 + FastAPI + uvicorn, HTML + Tailwind CDN + Alpine.js, Docker + docker-compose, rsync (Mac→VPS via cron), bash.

---

## File Map

| Arquivo | Responsabilidade |
|---------|-----------------|
| `scripts/sync-to-vps.sh` (Mac) | rsync daily/, AGENT_BRIDGE.md, WORKSPACE_INDEX.md → VPS:/opt/jpglabs/agent-dashboard/data/ |
| `/opt/jpglabs/agent-dashboard/backend/main.py` | FastAPI app — monta os routers e serve o frontend estático |
| `/opt/jpglabs/agent-dashboard/backend/parsers.py` | Funções de parsing dos arquivos .md (daily, workspace index, bridge) |
| `/opt/jpglabs/agent-dashboard/backend/infra.py` | Coleta de status local da VPS (docker ps, tailscale, serviços) |
| `/opt/jpglabs/agent-dashboard/backend/requirements.txt` | Dependências Python |
| `/opt/jpglabs/agent-dashboard/frontend/index.html` | Dashboard SPA (Tailwind CDN + Alpine.js) |
| `/opt/jpglabs/agent-dashboard/Dockerfile` | Imagem Python que serve backend + frontend estático |
| `/opt/jpglabs/agent-dashboard/docker-compose.yml` | Orquestra container + volume de dados |

---

## Task 1: Script de Sync Mac → VPS

**Files:**
- Create: `scripts/sync-to-vps.sh` (no Mac, em `/Users/philipegermano/code/scripts/`)

- [ ] **Step 1.1: Criar o script rsync**

```bash
#!/usr/bin/env bash
# sync-to-vps.sh — sincroniza arquivos do workspace para o dashboard na VPS
set -euo pipefail

VPS_HOST="root@187.77.227.151"
VPS_KEY="$HOME/.ssh/id_ed25519_vps"
VPS_DATA="/opt/jpglabs/agent-dashboard/data"
WORKSPACE="$HOME/code"

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Iniciando sync para VPS..."

# Sincronizar pasta daily/
rsync -az --delete \
  -e "ssh -i $VPS_KEY -o StrictHostKeyChecking=no" \
  "$WORKSPACE/daily/" \
  "$VPS_HOST:$VPS_DATA/daily/"

# Sincronizar arquivos de contexto do workspace
rsync -az \
  -e "ssh -i $VPS_KEY -o StrictHostKeyChecking=no" \
  "$WORKSPACE/jpglabs/docs/agents/AGENT_BRIDGE.md" \
  "$WORKSPACE/jpglabs/docs/WORKSPACE_INDEX.md" \
  "$VPS_HOST:$VPS_DATA/"

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Sync concluído."
```

- [ ] **Step 1.2: Tornar executável e testar o sync**

```bash
chmod +x /Users/philipegermano/code/scripts/sync-to-vps.sh
/Users/philipegermano/code/scripts/sync-to-vps.sh
```

Esperado: saída sem erros, arquivos chegando em `/opt/jpglabs/agent-dashboard/data/` na VPS.

- [ ] **Step 1.3: Criar estrutura de diretórios na VPS**

```bash
ssh -i ~/.ssh/id_ed25519_vps root@187.77.227.151 \
  "mkdir -p /opt/jpglabs/agent-dashboard/{backend,frontend,data/daily}"
```

- [ ] **Step 1.4: Commit do script**

```bash
git -C /Users/philipegermano/code add scripts/sync-to-vps.sh
git -C /Users/philipegermano/code commit -m "feat: add rsync sync script for agent-dashboard VPS data"
```

---

## Task 2: Parsers de Markdown (backend/parsers.py)

**Files:**
- Create: `/opt/jpglabs/agent-dashboard/backend/parsers.py`

Este arquivo contém três funções puras que retornam dicts prontos para serialização JSON.

- [ ] **Step 2.1: Criar parsers.py completo**

```python
# /opt/jpglabs/agent-dashboard/backend/parsers.py
"""Parsers para os arquivos .md do workspace."""
from __future__ import annotations

import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

DATA_DIR = Path("/opt/jpglabs/agent-dashboard/data")


# ---------------------------------------------------------------------------
# Daily parser
# ---------------------------------------------------------------------------

_SESSION_HEADER = re.compile(r"^## Sessão \d+ — (.+)$", re.MULTILINE)
_TIMESTAMP = re.compile(r"\*\*Timestamp:\*\*\s*(.+)")
_PROVIDER = re.compile(r"\*\*Provider:\*\*\s*(.+)")
_FEATURE_ID = re.compile(r"\*\*Feature ID:\*\*\s*(.+)")
_SUMMARY_BLOCK = re.compile(r"### Summary\s*\n(.*?)(?=\n###|\Z)", re.DOTALL)
_FILES_MODIFIED = re.compile(r"### Files Modified\s*\n(.*?)(?=\n###|\Z)", re.DOTALL)
_FILES_CREATED = re.compile(r"### Files Created\s*\n(.*?)(?=\n###|\Z)", re.DOTALL)


def parse_daily(target_date: date | None = None) -> dict[str, Any]:
    """Lê daily/<date>.md e retorna sessions + agent summary."""
    if target_date is None:
        target_date = date.today()
    path = DATA_DIR / "daily" / f"{target_date}.md"
    if not path.exists():
        return {"date": str(target_date), "sessions": [], "agents": {}}

    text = path.read_text(encoding="utf-8")
    # Divide por blocos de sessão
    splits = _SESSION_HEADER.split(text)
    # splits[0] = preâmbulo, splits[1::2] = títulos, splits[2::2] = corpos
    titles = splits[1::2]
    bodies = splits[2::2]

    sessions = []
    agent_counts: dict[str, int] = {}

    for title, body in zip(titles, bodies):
        ts_m = _TIMESTAMP.search(body)
        prov_m = _PROVIDER.search(body)
        feat_m = _FEATURE_ID.search(body)
        sum_m = _SUMMARY_BLOCK.search(body)
        mod_m = _FILES_MODIFIED.search(body)
        cre_m = _FILES_CREATED.search(body)

        timestamp = ts_m.group(1).strip() if ts_m else ""
        provider = prov_m.group(1).strip() if prov_m else "Unknown"
        feature_id = feat_m.group(1).strip() if feat_m else ""
        summary = sum_m.group(1).strip() if sum_m else ""

        files_modified = (
            [l.strip("- ").strip() for l in mod_m.group(1).strip().splitlines() if l.strip()]
            if mod_m else []
        )
        files_created = (
            [l.strip("- ").strip() for l in cre_m.group(1).strip().splitlines() if l.strip()]
            if cre_m else []
        )

        # Normaliza nome do provider (ex: "Claude Code (claude-opus-4-6)" → "Claude")
        provider_key = _normalize_provider(provider)
        agent_counts[provider_key] = agent_counts.get(provider_key, 0) + 1

        sessions.append({
            "title": title.strip(),
            "timestamp": timestamp,
            "provider": provider,
            "provider_key": provider_key,
            "feature_id": feature_id,
            "summary": summary[:300],  # limita para o card
            "files_modified": files_modified,
            "files_created": files_created,
        })

    return {
        "date": str(target_date),
        "sessions": sessions,
        "agents": agent_counts,
    }


def _normalize_provider(raw: str) -> str:
    raw_lower = raw.lower()
    if "claude" in raw_lower:
        return "Claude"
    if "codex" in raw_lower:
        return "Codex"
    if "gemini" in raw_lower:
        return "Gemini"
    if "openclaude" in raw_lower:
        return "OpenClaude"
    if "pi" in raw_lower:
        return "Pi"
    return raw.split()[0] if raw else "Unknown"


# ---------------------------------------------------------------------------
# Workspace Index parser
# ---------------------------------------------------------------------------

_PROJECT_ENTRY = re.compile(
    r"^- `([^`]+)`\s*\n"          # nome do projeto
    r"(?:  - Nicho: (.+)\n)?"
    r"(?:  - Papel no workspace: (.+)\n)?"
    r"(?:  - Contexto: (.+))?",
    re.MULTILINE,
)


def parse_workspace_index() -> list[dict[str, str]]:
    """Lê WORKSPACE_INDEX.md e retorna lista de projetos ativos."""
    path = DATA_DIR / "WORKSPACE_INDEX.md"
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    # Só considera a seção antes de "## Legado Arquivado"
    active_section = text.split("## Legado Arquivado")[0]
    projects = []
    for m in _PROJECT_ENTRY.finditer(active_section):
        name, nicho, papel, contexto = m.group(1), m.group(2), m.group(3), m.group(4)
        projects.append({
            "name": name,
            "nicho": nicho or "",
            "papel": papel or "",
            "contexto": contexto or "",
        })
    return projects


# ---------------------------------------------------------------------------
# Agent Bridge parser
# ---------------------------------------------------------------------------

_BRIDGE_SESSION = re.compile(
    r"## Session Handoff - (\d{4}-\d{2}-\d{2} \d{2}:\d{2} [+-]\d{4})\s*\n"
    r"### Session Metadata\s*\n"
    r"(.*?)(?=\n## |\Z)",
    re.DOTALL,
)
_REPO = re.compile(r"- Repositório: `([^`]+)`")
_BRANCH = re.compile(r"- Branch ativa: `([^`]+)`")
_OBJETIVO = re.compile(r"- Objetivo aprovado: (.+)")
_HANDOFF_PROVIDER = re.compile(r"- Feature/session id: `([^`]+)`")
_SUMMARY_BRIDGE = re.compile(r"### Summary\s*\n(.*?)(?=\n###|\Z)", re.DOTALL)


def parse_agent_bridge() -> dict[str, Any]:
    """Lê AGENT_BRIDGE.md e retorna o handoff mais recente."""
    path = DATA_DIR / "AGENT_BRIDGE.md"
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    m = _BRIDGE_SESSION.search(text)
    if not m:
        return {}

    timestamp_str = m.group(1).strip()
    meta_block = m.group(2)

    repo_m = _REPO.search(meta_block)
    branch_m = _BRANCH.search(meta_block)
    obj_m = _OBJETIVO.search(meta_block)
    feat_m = _HANDOFF_PROVIDER.search(meta_block)

    # Detecta provider pelo feature id
    feature_id = feat_m.group(1) if feat_m else ""
    provider_key = _normalize_provider(feature_id)

    # Summary do handoff
    sum_m = _SUMMARY_BRIDGE.search(text)
    summary = sum_m.group(1).strip()[:300] if sum_m else ""

    return {
        "timestamp": timestamp_str,
        "provider_key": provider_key,
        "repository": repo_m.group(1) if repo_m else "",
        "branch": branch_m.group(1) if branch_m else "",
        "objective": obj_m.group(1).strip() if obj_m else "",
        "summary": summary,
    }
```

- [ ] **Step 2.2: Enviar parsers.py para a VPS**

```bash
scp -i ~/.ssh/id_ed25519_vps \
  /opt/jpglabs/agent-dashboard/backend/parsers.py \
  root@187.77.227.151:/opt/jpglabs/agent-dashboard/backend/parsers.py
```

> Nota: os arquivos serão criados diretamente na VPS via SSH nas tasks seguintes.

---

## Task 3: Backend FastAPI (backend/main.py + infra.py)

**Files:**
- Create: `/opt/jpglabs/agent-dashboard/backend/main.py`
- Create: `/opt/jpglabs/agent-dashboard/backend/infra.py`
- Create: `/opt/jpglabs/agent-dashboard/backend/requirements.txt`

- [ ] **Step 3.1: Criar requirements.txt na VPS**

```bash
ssh -i ~/.ssh/id_ed25519_vps root@187.77.227.151 "cat > /opt/jpglabs/agent-dashboard/backend/requirements.txt" << 'EOF'
fastapi==0.115.6
uvicorn[standard]==0.34.0
EOF
```

- [ ] **Step 3.2: Criar infra.py na VPS**

```bash
ssh -i ~/.ssh/id_ed25519_vps root@187.77.227.151 "cat > /opt/jpglabs/agent-dashboard/backend/infra.py" << 'PYEOF'
# infra.py — coleta status de infraestrutura da VPS
from __future__ import annotations

import subprocess
import re
from typing import Any


KNOWN_SERVICES = [
    {"name": "ollama", "check": ["docker", "ps", "--filter", "name=ollama", "--format", "{{.Names}}"]},
    {"name": "banana-slides", "check": ["docker", "ps", "--filter", "name=banana", "--format", "{{.Names}}"]},
]

TAILSCALE_PEERS = [
    {"name": "Mac (Philipe)", "ip": "100.64.53.33"},
    {"name": "Windows jprdtr", "ip": "100.77.34.128"},
    {"name": "Mac Ayumi", "ip": "100.68.87.26"},
    {"name": "VPS (self)", "ip": "100.68.217.36"},
]


def _run(cmd: list[str]) -> tuple[str, int]:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
    return result.stdout.strip(), result.returncode


def get_docker_services() -> list[dict[str, Any]]:
    """Retorna status dos containers Docker relevantes."""
    services = []
    for svc in KNOWN_SERVICES:
        out, rc = _run(svc["check"])
        services.append({
            "name": svc["name"],
            "running": bool(out and rc == 0),
            "container": out or None,
        })
    # Adiciona todos containers em execução
    all_out, _ = _run(["docker", "ps", "--format", "{{.Names}}\t{{.Status}}\t{{.Image}}"])
    containers = []
    for line in all_out.splitlines():
        parts = line.split("\t")
        if len(parts) >= 3:
            containers.append({"name": parts[0], "status": parts[1], "image": parts[2]})
    return {"services": services, "containers": containers}


def get_tailscale_peers() -> list[dict[str, Any]]:
    """Verifica conectividade com os peers Tailscale via ping."""
    peers = []
    for peer in TAILSCALE_PEERS:
        out, rc = _run(["ping", "-c", "1", "-W", "1", peer["ip"]])
        peers.append({
            "name": peer["name"],
            "ip": peer["ip"],
            "online": rc == 0,
        })
    return peers


def get_infra_status() -> dict[str, Any]:
    docker = get_docker_services()
    peers = get_tailscale_peers()
    return {"docker": docker, "tailscale_peers": peers}
PYEOF
```

- [ ] **Step 3.3: Criar main.py na VPS**

```bash
ssh -i ~/.ssh/id_ed25519_vps root@187.77.227.151 "cat > /opt/jpglabs/agent-dashboard/backend/main.py" << 'PYEOF'
# main.py — FastAPI backend do Agent Dashboard
from __future__ import annotations

import asyncio
from datetime import date, datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from parsers import parse_daily, parse_workspace_index, parse_agent_bridge
from infra import get_infra_status

app = FastAPI(title="Agent Dashboard", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

FRONTEND_DIR = Path("/opt/jpglabs/agent-dashboard/frontend")

AGENTS = ["Claude", "Codex", "Gemini", "OpenClaude", "Pi"]


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat() + "Z"}


@app.get("/api/agents")
def agents_status() -> dict[str, Any]:
    """Status de cada agente baseado no daily de hoje e no bridge."""
    daily = parse_daily(date.today())
    bridge = parse_agent_bridge()
    sessions = daily.get("sessions", [])
    agent_counts = daily.get("agents", {})

    result = []
    for agent in AGENTS:
        count = agent_counts.get(agent, 0)
        # Última sessão deste agente no daily
        agent_sessions = [s for s in sessions if s["provider_key"] == agent]
        last_session = agent_sessions[-1] if agent_sessions else None

        # Status: se o bridge aponta para este agente e é de hoje → running
        bridge_today = (
            bridge.get("provider_key") == agent
            and bridge.get("timestamp", "").startswith(str(date.today()))
        )
        status = "running" if bridge_today else ("idle" if count == 0 else "idle")

        result.append({
            "name": agent,
            "status": status,
            "sessions_today": count,
            "last_session_timestamp": last_session["timestamp"] if last_session else None,
            "last_project": last_session["feature_id"] if last_session else None,
            "last_summary": last_session["summary"] if last_session else None,
        })

    return {
        "date": str(date.today()),
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "agents": result,
        "bridge": bridge,
    }


@app.get("/api/timeline")
def timeline() -> dict[str, Any]:
    """Timeline de sessões do dia."""
    daily = parse_daily(date.today())
    return {
        "date": daily["date"],
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "sessions": daily["sessions"],
    }


@app.get("/api/projects")
def projects() -> dict[str, Any]:
    """Projetos ativos do WORKSPACE_INDEX."""
    items = parse_workspace_index()
    bridge = parse_agent_bridge()
    # Associa o último projeto tocado pelo bridge ao projeto correspondente
    last_repo = bridge.get("repository", "").split("/")[-1] if bridge else ""
    for p in items:
        p["last_agent"] = bridge.get("provider_key") if p["name"] == last_repo else None
    return {
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "projects": items,
    }


@app.get("/api/infra")
def infra() -> dict[str, Any]:
    """Status de infraestrutura da VPS."""
    status = get_infra_status()
    status["updated_at"] = datetime.utcnow().isoformat() + "Z"
    return status


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(FRONTEND_DIR / "index.html")
PYEOF
```

- [ ] **Step 3.4: Testar sintaxe dos arquivos Python na VPS**

```bash
ssh -i ~/.ssh/id_ed25519_vps root@187.77.227.151 \
  "python3 -c 'import ast; ast.parse(open(\"/opt/jpglabs/agent-dashboard/backend/main.py\").read()); print(\"main.py OK\")'"

ssh -i ~/.ssh/id_ed25519_vps root@187.77.227.151 \
  "python3 -c 'import ast; ast.parse(open(\"/opt/jpglabs/agent-dashboard/backend/parsers.py\").read()); print(\"parsers.py OK\")'"

ssh -i ~/.ssh/id_ed25519_vps root@187.77.227.151 \
  "python3 -c 'import ast; ast.parse(open(\"/opt/jpglabs/agent-dashboard/backend/infra.py\").read()); print(\"infra.py OK\")'"
```

Esperado: `main.py OK`, `parsers.py OK`, `infra.py OK`

---

## Task 4: Frontend HTML Dashboard (frontend/index.html)

**Files:**
- Create: `/opt/jpglabs/agent-dashboard/frontend/index.html`

Dark theme: azul-grafite (`#0d1117`, `#161b22`), ciano/teal (`#00bcd4`, `#26c6da`), laranja (`#ff6d00`). Glass morphism via `backdrop-filter: blur`.

- [ ] **Step 4.1: Criar index.html na VPS**

```bash
ssh -i ~/.ssh/id_ed25519_vps root@187.77.227.151 "cat > /opt/jpglabs/agent-dashboard/frontend/index.html" << 'HTMLEOF'
<!DOCTYPE html>
<html lang="pt-BR" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Agent Dashboard — JPGLabs</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            bg: { base: '#0d1117', surface: '#161b22', card: '#1c2128' },
            brand: { cyan: '#26c6da', teal: '#00bcd4', orange: '#ff6d00' }
          }
        }
      }
    }
  </script>
  <style>
    body { background: #0d1117; font-family: 'Inter', system-ui, sans-serif; }
    .glass {
      background: rgba(22, 27, 34, 0.7);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid rgba(38, 198, 218, 0.12);
    }
    .badge-running { background: rgba(38,198,218,0.15); color: #26c6da; }
    .badge-idle    { background: rgba(255,255,255,0.06); color: #8b949e; }
    .badge-error   { background: rgba(255,109,0,0.15); color: #ff6d00; }
    .dot-running { background: #26c6da; box-shadow: 0 0 6px #26c6da; }
    .dot-idle    { background: #8b949e; }
    .dot-error   { background: #ff6d00; }
    .pulse { animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
    @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.5} }
  </style>
</head>
<body class="min-h-screen text-gray-200"
  x-data="dashboard()"
  x-init="init()"
>
  <!-- Header -->
  <header class="border-b border-white/5 px-6 py-4 flex items-center justify-between">
    <div class="flex items-center gap-3">
      <div class="w-2 h-2 rounded-full dot-running pulse"></div>
      <h1 class="text-lg font-semibold text-white">Agent Dashboard</h1>
      <span class="text-xs text-gray-500">JPGLabs Workspace</span>
    </div>
    <div class="flex items-center gap-4 text-xs text-gray-500">
      <span>Último update: <span x-text="lastUpdate" class="text-brand-cyan"></span></span>
      <button @click="refresh()" class="px-3 py-1 rounded-md bg-white/5 hover:bg-white/10 transition text-gray-300">↻ Refresh</button>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 py-6 space-y-8">

    <!-- Seção 1: Status dos Agentes -->
    <section>
      <h2 class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Agentes</h2>
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
        <template x-for="agent in agents" :key="agent.name">
          <div class="glass rounded-xl p-4 space-y-3">
            <div class="flex items-center justify-between">
              <span class="font-semibold text-white text-sm" x-text="agent.name"></span>
              <span class="text-xs px-2 py-0.5 rounded-full font-medium"
                :class="'badge-' + agent.status"
                x-text="agent.status"></span>
            </div>
            <div class="space-y-1 text-xs text-gray-400">
              <div>Sessões hoje: <span class="text-brand-cyan font-semibold" x-text="agent.sessions_today"></span></div>
              <div x-show="agent.last_project" class="truncate" x-text="agent.last_project"></div>
              <div x-show="agent.last_session_timestamp" class="text-gray-600 truncate" x-text="agent.last_session_timestamp"></div>
            </div>
          </div>
        </template>
      </div>
    </section>

    <!-- Seção 2: Timeline de Sessões -->
    <section>
      <h2 class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">
        Timeline — <span x-text="timelineDate" class="text-brand-cyan"></span>
      </h2>
      <div class="space-y-2">
        <template x-for="(session, i) in sessions" :key="i">
          <div class="glass rounded-xl p-4 flex gap-4 items-start">
            <div class="w-20 flex-shrink-0 text-xs text-gray-500 mt-0.5" x-text="session.timestamp.split(' ')[1] || session.timestamp"></div>
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 flex-wrap">
                <span class="text-xs font-semibold px-2 py-0.5 rounded-md badge-running" x-text="session.provider_key"></span>
                <span class="text-sm text-white font-medium truncate" x-text="session.title"></span>
              </div>
              <p class="text-xs text-gray-400 mt-1 line-clamp-2" x-text="session.summary"></p>
              <div x-show="session.files_created.length || session.files_modified.length" class="flex gap-3 mt-2 text-xs text-gray-600">
                <span x-show="session.files_created.length">+<span x-text="session.files_created.length"></span> criados</span>
                <span x-show="session.files_modified.length">~<span x-text="session.files_modified.length"></span> modificados</span>
              </div>
            </div>
          </div>
        </template>
        <div x-show="sessions.length === 0" class="glass rounded-xl p-6 text-center text-gray-500 text-sm">
          Nenhuma sessão registrada hoje.
        </div>
      </div>
    </section>

    <!-- Grid inferior: Projetos + Infra -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

      <!-- Seção 3: Projetos Ativos -->
      <section>
        <h2 class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Projetos Ativos</h2>
        <div class="space-y-2">
          <template x-for="project in projects" :key="project.name">
            <div class="glass rounded-xl px-4 py-3 flex items-start gap-3">
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2">
                  <span class="font-mono text-brand-teal text-sm font-semibold" x-text="project.name"></span>
                  <span x-show="project.last_agent" class="text-xs badge-running px-2 py-0.5 rounded-full" x-text="project.last_agent"></span>
                </div>
                <p class="text-xs text-gray-500 mt-0.5 truncate" x-text="project.nicho"></p>
              </div>
            </div>
          </template>
        </div>
      </section>

      <!-- Seção 4: Infraestrutura -->
      <section>
        <h2 class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Infraestrutura</h2>

        <!-- Docker Services -->
        <div class="glass rounded-xl p-4 mb-3">
          <h3 class="text-xs font-semibold text-gray-500 mb-3">Docker / Serviços</h3>
          <div class="space-y-2">
            <template x-for="svc in dockerServices" :key="svc.name">
              <div class="flex items-center justify-between text-sm">
                <span class="text-gray-300" x-text="svc.name"></span>
                <div class="flex items-center gap-2">
                  <div class="w-2 h-2 rounded-full" :class="svc.running ? 'dot-running' : 'dot-error'"></div>
                  <span class="text-xs" :class="svc.running ? 'text-brand-cyan' : 'text-brand-orange'" x-text="svc.running ? 'online' : 'offline'"></span>
                </div>
              </div>
            </template>
          </div>
        </div>

        <!-- Tailscale Peers -->
        <div class="glass rounded-xl p-4">
          <h3 class="text-xs font-semibold text-gray-500 mb-3">Tailscale Peers</h3>
          <div class="space-y-2">
            <template x-for="peer in tailscalePeers" :key="peer.ip">
              <div class="flex items-center justify-between text-sm">
                <div>
                  <span class="text-gray-300" x-text="peer.name"></span>
                  <span class="text-xs text-gray-600 ml-2" x-text="peer.ip"></span>
                </div>
                <div class="flex items-center gap-2">
                  <div class="w-2 h-2 rounded-full" :class="peer.online ? 'dot-running pulse' : 'dot-idle'"></div>
                  <span class="text-xs" :class="peer.online ? 'text-brand-cyan' : 'text-gray-600'" x-text="peer.online ? 'online' : 'offline'"></span>
                </div>
              </div>
            </template>
          </div>
        </div>
      </section>
    </div>
  </main>

  <script>
    function dashboard() {
      return {
        agents: [],
        sessions: [],
        timelineDate: '',
        projects: [],
        dockerServices: [],
        tailscalePeers: [],
        lastUpdate: '—',
        _timer: null,

        async init() {
          await this.refresh();
          this._timer = setInterval(() => this.refresh(), 30000);
        },

        async refresh() {
          try {
            const [agentsRes, timelineRes, projectsRes, infraRes] = await Promise.all([
              fetch('/api/agents').then(r => r.json()),
              fetch('/api/timeline').then(r => r.json()),
              fetch('/api/projects').then(r => r.json()),
              fetch('/api/infra').then(r => r.json()),
            ]);

            this.agents = agentsRes.agents || [];
            this.sessions = (timelineRes.sessions || []).reverse();
            this.timelineDate = timelineRes.date || '';
            this.projects = projectsRes.projects || [];
            this.dockerServices = infraRes.docker?.services || [];
            this.tailscalePeers = infraRes.tailscale_peers || [];
            this.lastUpdate = new Date().toLocaleTimeString('pt-BR');
          } catch (e) {
            console.error('Erro ao atualizar dashboard:', e);
          }
        }
      }
    }
  </script>
</body>
</html>
HTMLEOF
```

---

## Task 5: Dockerfile e docker-compose

**Files:**
- Create: `/opt/jpglabs/agent-dashboard/Dockerfile`
- Create: `/opt/jpglabs/agent-dashboard/docker-compose.yml`

- [ ] **Step 5.1: Criar Dockerfile na VPS**

```bash
ssh -i ~/.ssh/id_ed25519_vps root@187.77.227.151 "cat > /opt/jpglabs/agent-dashboard/Dockerfile" << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Instalar ping para health check dos peers Tailscale
RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Adicionar backend ao PYTHONPATH
ENV PYTHONPATH=/app/backend

EXPOSE 8080

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]
EOF
```

- [ ] **Step 5.2: Criar docker-compose.yml na VPS**

```bash
ssh -i ~/.ssh/id_ed25519_vps root@187.77.227.151 "cat > /opt/jpglabs/agent-dashboard/docker-compose.yml" << 'EOF'
version: "3.9"

services:
  agent-dashboard:
    build: .
    container_name: agent-dashboard
    restart: unless-stopped
    ports:
      - "8080:8080"
    volumes:
      # Diretório de dados sincronizados via rsync
      - ./data:/opt/jpglabs/agent-dashboard/data:ro
      # Acesso ao socket Docker para inspecionar containers
      - /var/run/docker.sock:/var/run/docker.sock:ro
    environment:
      - TZ=America/Sao_Paulo
EOF
```

- [ ] **Step 5.3: Ajustar path do DATA_DIR no parsers.py para funcionar no container**

O container monta os dados em `/opt/jpglabs/agent-dashboard/data` (mesmo path do host). Confirmar que a linha no `parsers.py` está:
```python
DATA_DIR = Path("/opt/jpglabs/agent-dashboard/data")
```

- [ ] **Step 5.4: Ajustar FRONTEND_DIR no main.py para funcionar no container**

Confirmar que `main.py` tem:
```python
FRONTEND_DIR = Path("/app/frontend")
```

---

## Task 6: Primeiro Sync e Deploy

- [ ] **Step 6.1: Executar sync inicial do Mac para a VPS**

```bash
/Users/philipegermano/code/scripts/sync-to-vps.sh
```

Verificar na VPS:
```bash
ssh -i ~/.ssh/id_ed25519_vps root@187.77.227.151 \
  "ls -la /opt/jpglabs/agent-dashboard/data/ && ls /opt/jpglabs/agent-dashboard/data/daily/ | head -5"
```

- [ ] **Step 6.2: Build e start do container na VPS**

```bash
ssh -i ~/.ssh/id_ed25519_vps root@187.77.227.151 << 'SSHEOF'
cd /opt/jpglabs/agent-dashboard
docker compose build
docker compose up -d
SSHEOF
```

Esperado: container `agent-dashboard` em execução na porta 8080.

- [ ] **Step 6.3: Verificar health**

```bash
ssh -i ~/.ssh/id_ed25519_vps root@187.77.227.151 \
  "curl -s http://localhost:8080/api/health"
```

Esperado:
```json
{"status":"ok","timestamp":"2026-04-08T...Z"}
```

- [ ] **Step 6.4: Testar endpoints da API**

```bash
ssh -i ~/.ssh/id_ed25519_vps root@187.77.227.151 \
  "curl -s http://localhost:8080/api/agents | python3 -m json.tool | head -30"

ssh -i ~/.ssh/id_ed25519_vps root@187.77.227.151 \
  "curl -s http://localhost:8080/api/timeline | python3 -m json.tool | head -20"

ssh -i ~/.ssh/id_ed25519_vps root@187.77.227.151 \
  "curl -s http://localhost:8080/api/projects | python3 -m json.tool | head -20"
```

- [ ] **Step 6.5: Testar acesso via Tailscale do Mac**

```bash
curl -s http://100.68.217.36:8080/api/health
```

E acessar no browser: `http://100.68.217.36:8080`

- [ ] **Step 6.6: Configurar cron de sync no Mac (a cada 5 minutos)**

```bash
(crontab -l 2>/dev/null; echo "*/5 * * * * /Users/philipegermano/code/scripts/sync-to-vps.sh >> /tmp/vps-sync.log 2>&1") | crontab -
crontab -l
```

Esperado: linha `*/5 * * * * ...sync-to-vps.sh` visível no crontab.

---

## Task 7: Verificação Final e Commit

- [ ] **Step 7.1: Verificar logs do container**

```bash
ssh -i ~/.ssh/id_ed25519_vps root@187.77.227.151 \
  "docker logs agent-dashboard --tail 20"
```

Esperado: uvicorn started on `0.0.0.0:8080`, sem erros.

- [ ] **Step 7.2: Confirmar dashboard visível no browser**

Abrir `http://187.77.227.151:8080` ou `http://100.68.217.36:8080`.
Confirmar:
- Cards de agentes visíveis (Claude, Codex, Gemini, OpenClaude, Pi)
- Timeline com sessões do dia 2026-04-08
- Projetos listados (FrankMD, openclaude, jpglabs-saas, etc.)
- Painel de infra com Docker services e Tailscale peers

- [ ] **Step 7.3: Commit do script de sync**

```bash
git -C /Users/philipegermano/code add scripts/sync-to-vps.sh docs/superpowers/plans/2026-04-08-agent-dashboard.md
git -C /Users/philipegermano/code commit -m "feat: add agent-dashboard sync script and implementation plan"
```

---

## Self-Review

### Spec coverage
- [x] Cards de agentes com status/timestamp/projeto — Task 2 (parsers daily) + Task 3 (endpoint /api/agents) + Task 4 (frontend)
- [x] Timeline de sessões do dia — Task 2 (parse_daily) + Task 3 (/api/timeline) + Task 4 (frontend)
- [x] Projetos ativos do WORKSPACE_INDEX — Task 2 (parse_workspace_index) + Task 3 (/api/projects) + Task 4 (frontend)
- [x] Painel de infraestrutura (Docker, Tailscale) — Task 3 (infra.py + /api/infra) + Task 4 (frontend)
- [x] Live update a cada 30s — Task 4 (Alpine.js setInterval)
- [x] rsync Mac → VPS — Task 1 (sync-to-vps.sh) + Task 6 (cron)
- [x] Docker deploy porta 8080 — Task 5 (docker-compose.yml) + Task 6

### Gaps identificados
- MCP servers ativos (do MCP_SETUP.md) — não implementado explicitamente, pois requer leitura do MCP_SETUP.md na VPS. A infra.py cobre Docker containers que incluem os MCPs. Gap aceitável para v1.
- Duração estimada das sessões — o daily .md não registra timestamp de início e fim separados; campo omitido na v1.
