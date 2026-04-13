# LLM Taxonomy Analyst

## Recomendacao Direta

Use um modelo local barato como `qwen2.5-coder:7b` apenas como analista de
taxonomia, drift e hardcodes. Nao use esse modelo como agente de escrita livre
ou orquestrador principal.

## Papel do analista local

- varrer roots permitidos
- gerar inventario deterministico
- detectar duplicatas e hardcodes
- resumir evidencias em JSON curto
- devolver achados para o modelo principal

## O que nao delegar ao modelo local

- mudancas em producao
- edicao livre de arquivos criticos
- decisoes arquiteturais sem evidencias
- consolidacao de estado entre providers

## Arquitetura recomendada

```text
request -> queue/inbox -> deterministic scan -> ollama(qwen2.5-coder:7b)
        -> result.json -> orchestrator/main LLM -> approved change
```

## Contratos

### Entrada

- job JSON com pergunta, roots, limites e patterns

### Saida

- `inventory.json` com evidencia objetiva
- `inventory.json` com contexto de estudo:
  - `study_context.executed_commands[]`
  - `glossary[]`
  - `language_glossary[]`
  - associacoes com `summary`, `next_actions` e `open_questions`
- `result.json` com:
  - `summary`
  - `confidence`
  - `findings`
  - `next_actions`
  - `open_questions`
  - `glossary`
  - `language_glossary`

## Por que isso reduz custo

- a busca pesada e feita por codigo deterministico
- o prompt enviado ao modelo local e pequeno e focado
- o modelo principal recebe conclusoes mais curtas e auditaveis

## Modelos

- `qwen2.5-coder:7b`
  - melhor default agora
  - bom para config, codigo e taxonomia
  - rapido o suficiente na VPS atual
- `qwen2.5:32b-instruct-q4_K_M`
  - usar apenas para escalacao
  - melhor para sintese mais complexa
  - custo de latencia maior

## Integracao com a VPS

- manter o worker em lane isolada, fora do runtime de produto
- ler do filesystem local da VPS
- chamar `http://127.0.0.1:11434`
- persistir resultados em `/srv/homelab/taxonomy-analyst/queue/artifacts`

## Evolucao recomendada

1. POC local na VPS com fila por arquivos
2. mover fila para Postgres ou Redis quando houver concorrencia real
3. expor uma API interna `POST /taxonomy/jobs`
4. adicionar politicas por lane: `dev`, `test`, `stage`, `prod`
5. separar `memory` global de `projects` no filesystem canonico
