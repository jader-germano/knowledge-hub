# Indice de Documentacao — ~/Library/Mobile Documents/com~apple~CloudDocs/code

> Atualizado em 2026-03-27 apos a migracao fisica dos repositorios de
> `/Users/philipegermano/Documents/GitHub` para `code/`, sem symlinks.
> A referencia unificada de markdown fica mantida em
> `code/jpglabs-knowledge-hub`.

---

## 1. Hub documental e operacional

### `jpglabs-knowledge-hub/README.md`
**Tipo:** README do hub
**Papel:** descreve o hub como superficie documental, de handoff entre agentes
e de classificacao dos markdowns relevantes do workspace.

### `jpglabs-knowledge-hub/AGENTS.md`
**Tipo:** guia geral de agentes
**Papel:** define o layout do workspace, a regra de nao usar symlinks e o papel do hub
como fonte de classificacao documental.

### `jpglabs-knowledge-hub/CLAUDE.md`
**Tipo:** entrada operacional do Claude
**Papel:** alinha o Claude ao mesmo layout, handoff e classificacao mantidos no
hub.

### `jpglabs-knowledge-hub/GEMINI.md`
**Tipo:** entrada operacional do Gemini / Antigravity
**Papel:** alinha o Gemini ao mesmo layout do workspace e evita divergencia de
instrucoes.

### `jpglabs-knowledge-hub/MCP_SETUP.md`
**Tipo:** configuracao MCP
**Papel:** documenta o stack MCP ativo e o escopo repo-only aplicado ao hub.

### `jpglabs-knowledge-hub/.codex/AGENT_BRIDGE.md`
**Tipo:** ponte de handoff
**Papel:** define a superficie de transferencia de contexto entre agentes.

### `jpglabs-knowledge-hub/.codex/SESSION_CLOSE_TEMPLATE.md`
**Tipo:** template de encerramento
**Papel:** padrao para fechamento tecnico, handoff e proximos passos.

---

## 2. Repositorios de codigo adjacentes

### `jpglabs/README.md`
**Tipo:** README de infraestrutura e automacao
**Papel:** panorama de VPS, n8n, Cloudflare, WhatsApp bot e scripts
operacionais da JPG Labs.

### `jpglabs/docs/vps-setup.md`
**Tipo:** documentacao de infraestrutura
**Papel:** setup detalhado e operacao tecnica da VPS.

### `ai-orchestration-hub/AGENTS.md`
**Tipo:** legado/importado
**Papel:** origem historica de diretrizes de agentes antes da unificacao no
hub.

### `ai-orchestration-hub/CLAUDE.md`
**Tipo:** legado/importado
**Papel:** contexto operacional anterior do Claude, preservado para consulta.

### `ai-orchestration-hub/GEMINI.md`
**Tipo:** legado/importado
**Papel:** contexto operacional anterior do Gemini, preservado para consulta.

### `apple-study-checklist/README.md`
**Tipo:** documentacao de projeto
**Papel:** app macOS em SwiftUI para cronograma de estudos Apple, com
persistencia local em JSON.

---

## 3. Referencias HTML locais

### `JPGLabs | Pi Products and Services.html`
**Tipo:** referencia HTML local
**Papel:** pagina/export local relacionada a produtos e servicos Pi/JPGLabs.

### `Stripe Press — Ideas for progress.html`
**Tipo:** referencia HTML local
**Papel:** captura local do site Stripe Press usada como referencia editorial
ou de produto.

---

## Resumo por area

| Area | Caminho base | Papel |
|------|--------------|-------|
| Hub documental | `code/jpglabs-knowledge-hub` | Handoff, MCP, classificacao de markdown |
| Infra e automacao | `code/jpglabs` | VPS, workflows n8n, scripts, contexto |
| Orquestracao historica | `code/ai-orchestration-hub` | Fonte legada de instrucoes de agentes |
| Produto Apple | `code/apple-study-checklist` | App SwiftUI |
| Referencias web | `code/*.html` | Capturas e materiais locais |
