---
type: moc
title: "Index — JPGLabs Docs Vault"
tags:
  - "#moc"
  - "#index"
aliases:
  - home
  - MOC
  - inicio
created: "2026-04-08"
---

# JPGLabs Docs — Map of Content

> Vault Obsidian em `~/code/jpglabs/docs/`. Padrão LLM Wiki (Karpathy) adaptado.  
> Navegue por backlinks — as pastas são categorias, não hierarquia rígida.

---

## Entradas rápidas

| Tipo | Link | Descrição |
|------|------|-----------|
| Bootstrap | [[README]] | Entrada global do workspace |
| Regras | [[RULES]] | Regras operacionais |
| Glossário | [[GLOSSARY]] | Termos e aliases linkáveis |
| Roadmap | [[ROADMAP]] | Roadmap de plataforma |
| Ownership | [[OWNERSHIP]] | Ownership da documentação |
| MCP Setup | [[MCP_SETUP]] | Referência transversal MCP |

---

## Camadas LLM Wiki (Karpathy)

### raw/ — Fontes imutáveis `#raw`

> Transcrições, artigos, dumps. Nunca editado após captura.

- [[raw/videos/sboNwYmH3AY_karpathy-llm-wiki|Karpathy — LLM Wiki (transcrição)]]
- [[raw/README]]

### memory/wiki/ — Compilações temáticas `#wiki`

> Sínteses derivadas de `raw/`. Editável pelo LLM.

- [[memory/wiki/llm-wiki-pattern|LLM Wiki Pattern]]
- [[memory/wiki/pi-coding-agent|Pi Coding Agent]]
- [[memory/wiki/README]]

### Schema / Operacional

> Contratos e instruções que definem como o LLM opera.

- [[RULES]] · [[agents/AGENT_BRIDGE]] · [[agents/SESSION_CLOSE_TEMPLATE]]
- [[llms/CLAUDE]] · [[llms/CODEX]] · [[llms/GEMINI]]

---

## Projetos ativos `#project`

```dataview
LIST
FROM "projects"
WHERE type = "project-context"
SORT file.mtime DESC
```

<!-- Fallback sem Dataview: -->
- [[projects/jpglabs/PROJECT_CONTEXT|jpglabs]]
- [[projects/openclaude/PROJECT_CONTEXT|openclaude]]
- [[projects/apple-study-checklist/PROJECT_CONTEXT|apple-study-checklist]]
- [[projects/docs/llms/CLAUDE|docs/llms]]

---

## Daily Notes `#daily`

```dataview
LIST
FROM "daily"
SORT file.name DESC
LIMIT 10
```

<!-- Fallback: navegar pela pasta `daily/` no explorer -->

---

## Architecture Decision Records

- [[research/adr/ADR-001-llm-wiki-architecture|ADR-001 — LLM Wiki Architecture]]

---

## Memória operacional

- [[memory/PI_MEMORY|PI_MEMORY]] — ledger canônico
- [[memory/AGENTS|AGENTS]] — governança do agente Pi
- [[memory/sessions/README|sessions/]] — working memories

---

## Por tipo de conteúdo

| Tag | Conteúdo |
|-----|----------|
| `#raw` | Fontes imutáveis em `raw/` |
| `#wiki` | Compilações em `memory/wiki/` |
| `#project` | Contextos de projeto em `projects/` |
| `#daily` | Sessões diárias em `daily/` |
| `#glossary` | [[GLOSSARY]] |
| `#moc` | Este index e outros Maps of Content |

---

## Referências externas

- [Karpathy — LLM Wiki (YouTube)](https://youtu.be/sboNwYmH3AY)
- [ADR-001](research/adr/ADR-001-llm-wiki-architecture.md) — decisão arquitetural
- Jira: jpglabs.atlassian.net
- Confluence: jadergermano.atlassian.net/wiki

---

*Gerado em 2026-04-08. Atualizar ao adicionar novas seções ao vault.*
