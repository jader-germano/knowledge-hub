# ADR-001 — LLM Wiki Architecture (padrão Karpathy)

**Data:** 2026-04-08  
**Status:** Aceito  
**Autor:** Philipe Germano (via Claude Code)  
**Referência:** [Andrej Karpathy — LLM Wiki](https://youtu.be/sboNwYmH3AY)

---

## Contexto

O workspace em `~/code` já possuía ~80% da estrutura equivalente ao padrão Karpathy
antes desta decisão. O objetivo é formalizar o mapeamento das camadas propostas por
Karpathy sobre o que já existe — sem duplicar, sem reestruturar radicalmente.

### O Padrão Karpathy (3 camadas)

Karpathy propõe que um sistema de knowledge base para LLMs deve ter:

1. **`raw/`** — fontes primárias imutáveis (transcrições, artigos, dumps). O LLM
   nunca edita esta camada; apenas lê e deriva.
2. **`wiki/`** — compilações temáticas editáveis pelo LLM. É a memória
   interpretada, sintetizada, cross-referenciada.
3. **`schema`** — contratos e instruções que definem como o LLM opera: prompts,
   regras, estrutura de sessão.

Referência complementar: [Mario Zechner — Pi Coding Agent](https://youtu.be/Dli5slNaJu0)
(4 tools only, minimal system prompt, markdown-first).

---

## Decisão

Adotar o padrão Karpathy **sem reestruturação** do hub existente — apenas
formalizar o mapeamento e adicionar as peças ausentes.

### Mapeamento Karpathy → workspace existente

| Camada Karpathy | Equivalente no workspace | Notas |
|-----------------|--------------------------|-------|
| `raw/`          | `jpglabs/docs/raw/`      | **Novo** — criado nesta sessão. Fontes brutas imutáveis. |
| `wiki/`         | `jpglabs/docs/memory/wiki/` | **Novo subdir** em `memory/`. Compilações temáticas. Ver nota abaixo. |
| `schema`        | `WORKSPACE_BOOTSTRAP.md` + `CLAUDE.md` + `AGENTS.md` + `RULES.md` | Já existia. |
| `log`           | `daily/*.md` + `agents/AGENT_BRIDGE.md` | Já existia. |

#### Por que `memory/wiki/` e não um `wiki/` separado?

`jpglabs/docs/memory/` já cumpre o papel de memória persistente, cross-agent e
atualizada continuamente. Criar um `wiki/` paralelo seria duplicação. A solução
adotada:

- `memory/PI_MEMORY.md` e `memory/AGENTS.md` — memória operacional (ledger)
- `memory/sessions/` — logs de sessão incorporados
- `memory/wiki/` — **compilações temáticas** derivadas de `raw/` (wiki no sentido Karpathy)

A fronteira entre `wiki/` e o restante de `memory/` é:
- `memory/*.md` — estado operacional, muda com frequência (ledger)
- `memory/wiki/*.md` — sínteses temáticas, muda quando o conhecimento evolui

---

## Fluxo Operacional

```
raw/videos/          raw/articles/
     │                     │
     └──────────┬──────────┘
                ▼
        (LLM lê, deriva)
                │
                ▼
        memory/wiki/
        (compilações temáticas)
                │
                ▼
        RULES.md / CLAUDE.md / AGENTS.md
        (schema — injeção em contexto)
```

---

## Regras Decorrentes

1. `raw/` é append-only para agentes. Nunca editar conteúdo após captura.
2. `memory/wiki/` é editável pelo LLM, mas sempre derivado de fontes em `raw/`
   ou citado com referência rastreável.
3. Todo novo vídeo ou artigo referenciado num `daily/*.md` deve ter entrada em
   `raw/` antes de ser sintetizado em `memory/wiki/`.
4. A camada `schema` (CLAUDE.md, RULES.md etc.) não vai para `raw/` — é contrato
   operacional, não fonte de conhecimento.

---

## Consequências

**Positivo:**
- Zero duplicação — estrutura existente reaproveitada integralmente
- Rastreabilidade: toda compilação em `wiki/` tem referência à fonte em `raw/`
- Compatível com progressive disclosure: `raw/` só é carregado quando necessário

**Negativo / Atenção:**
- `memory/wiki/` é novo subdir — requer atualização do `DOC_INDEX.md`
- `raw/` cresce com cada transcrição — gerenciar tamanho com cuidado
- O `youtube_transcript` MCP precisa estar ativo para captura automatizada

---

## Alternativas Descartadas

| Alternativa | Motivo do descarte |
|-------------|-------------------|
| Criar `wiki/` separado no root de `docs/` | Duplicaria `memory/` já existente |
| Usar vector DB / embeddings | Contradiz o princípio Karpathy de markdown puro + grep |
| Manter apenas `memory/` sem `raw/` | Perderia a distinção imutável/editável; fontes ficam misturadas |
