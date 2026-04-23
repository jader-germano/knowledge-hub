---
type: guide
title: VPS Ollama Roster — Upgrade 2026-04-23
tags:
  - "#llm"
  - "#infra"
  - "#vps"
  - "#axis"
last_updated: "2026-04-23"
aliases:
  - vps ollama roster
  - axis llm backbone
  - modelos locais vps
---

# VPS Ollama Roster — Upgrade 2026-04-23

## Contexto

Gatilho: vídeo "MiniMax M2.7 localmente" (cGIXyqjZSD8) reafirmando que o
caminho prático para rodar modelos capazes sem GPU é **MoE com poucos
parâmetros ativos** + **quantização agressiva**. A VPS `srv1443703` é
CPU-only (Hostinger), então os modelos-alvo do vídeo (MiniMax M2.7 229 B em
185 GB Q6, GLM 5.1 700 B) são inviáveis. Porém o princípio se aplica
diretamente: usar MoE tipo `*-A3B` (poucos ativos) e quantização Q4/Q5.

## Hardware real da VPS (2026-04-23)

| Recurso | Valor |
|---|---|
| CPU | AMD EPYC 9355P (Zen 5), 8 vCPU, 2.0 GHz |
| RAM | 31 GiB (27 GiB livres em idle) |
| Swap | 0 B |
| Disco | 387 GB total, 287 GB livres em `/` |
| OS | Ubuntu 24.04.3 LTS, kernel 6.8.0-107 |
| Ollama | 0.20.3 |
| Endpoint | `http://100.68.217.36:11434` (Tailscale `srv1443703`) + `http://187.77.227.151:11434` (público) |
| Env | `OLLAMA_KEEP_ALIVE=24h`, `OLLAMA_NUM_PARALLEL=2`, `OLLAMA_NUM_THREADS=8`, `OLLAMA_FLASH_ATTENTION=1`, `OLLAMA_NUM_CTX=4096`, `OLLAMA_MAX_LOADED_MODELS=2` |

> ⚠️ `PI_MEMORY.md` (pre-2026-04-23) listava `deepseek-r1:7b` e
> `nemotron-3-super` como presentes na VPS. Verificação real mostrou que
> nenhum dos dois está instalado. Este documento é a fonte de verdade até
> que o `PI_MEMORY.md` seja atualizado.

## Roster atual (antes do upgrade)

| Modelo | Tamanho | Tipo | Uso |
|---|---|---|---|
| `qwen2.5-coder:7b` | 4.7 GB | denso | coding leve, fallback |
| `qwen2.5-coder:14b` | 9.0 GB | denso | coding médio |
| `qwen2.5:32b-instruct-q4_K_M` | 19 GB | denso | general top (lento) |
| `deepseek-coder-v2:16b` | 8.9 GB | MoE 16B/2.4B | **coding rápido (principal MoE)** |
| `gemma4:e4b` | 9.6 GB | — | multilíngue |
| `gemma4:26b` | 17 GB | denso | multilíngue pesado |

## Upgrade aplicado

Três modelos puxados em 2026-04-23 para cobrir os buckets fracos do
roster atual: coder MoE grande, reasoning/tool-use Apache-2.0, e
math/reasoning denso pequeno.

| Modelo | Tamanho | Tipo | Licença | Razão |
|---|---|---|---|---|
| `qwen3-coder:30b` | ~18 GB | MoE (A3B) | Qwen | Principal upgrade de coding — substitui `qwen2.5-coder:14b` como default do Axis |
| `gpt-oss:20b` | ~13 GB | MoE MXFP4 | Apache-2.0 | Reasoning/tool-use com licença permissiva — seguro para uso comercial |
| `phi4:14b` | ~8 GB | denso | MIT | Raciocínio/matemática barato, fallback CPU |

Total adicionado: ~39 GB (cabem folgados nos 287 GB livres).

## Roteamento recomendado para Axis

```
coder        → qwen3-coder:30b         [fallback] qwen2.5-coder:14b
reasoning    → gpt-oss:20b             [fallback] phi4:14b
general/PT   → qwen2.5:32b-instruct    [fallback] gemma4:26b
math         → phi4:14b                [fallback] qwen2.5:32b-instruct
fast/cheap   → qwen2.5-coder:7b        (único)
```

Integração: endpoint OpenAI-compatible nativo do Ollama
(`/v1/chat/completions`). Usar Tailscale (`100.68.217.36:11434`) como
padrão, público como fallback só se o peer Tailnet estiver offline
(regra do `CLAUDE.md` do workspace).

## Descartados explicitamente

| Modelo | Por quê |
|---|---|
| MiniMax M2.7 | 185 GB mesmo em Q6 — não cabe em 31 GiB RAM |
| GLM 4.5 / 5.1 | 400 GB+ em qualquer quant viável — inviável |
| Kimi K2.5 | idem |
| Llama 3.3 70B Q4 | ~40 GB carregado — passa do limite RAM (27 GiB livre) |
| `deepseek-r1:7b` | PI_MEMORY listava, mas após 2 semanas não foi mantido — substituído por `deepseek-coder-v2:16b` (MoE) |
| `nemotron-3-super` | idem — licença NVIDIA restritiva e sobreposição com `gpt-oss:20b` |

## Drama de licença (lição do vídeo)

MiniMax M2.7 foi lançado como "open source" e depois re-classificado como
"open weight" com licença não-comercial que vazou em cláusulas amplas
sobre "trabalhos derivados". Cursor/Composer 2 teve caso similar com
Kimi K2.5. **Regra para Axis**: nenhum modelo com licença ambígua entra
em roster de produção. Só Apache-2.0 / MIT / licença explícita permitindo
uso comercial. `qwen3-coder` e `gpt-oss` passam; `nemotron-3-super` e
qualquer MiniMax não passam.

## Smoke test (2026-04-23)

Prompt: `Write a JS function fibonacci(n) that returns the nth Fibonacci number iteratively. Code only, no prose.`
Execução: sequencial, AMD EPYC 9355P 8 vCPU, 31 GiB RAM, Ollama 0.20.3.

| Modelo | Load (cold) | Prompt eval | Eval rate | Output |
|---|---|---|---|---|
| `qwen3-coder:30b` (MoE A3B) | 8.9 s | 55 tok/s | **27.3 tok/s** | ✅ correto, conciso |
| `gpt-oss:20b` (MoE MXFP4) | 6.1 s | 57 tok/s | **20.4 tok/s** | ✅ correto, trata n=1 |
| `phi4:14b` (denso) | 41.8 s | 22.8 tok/s | **11.9 tok/s** | ✅ correto, destructuring |

Confirma o princípio do vídeo: **MoE é mais rápido em CPU mesmo sendo
maior em parâmetros totais**. qwen3-coder (30 B/3 B ativos) roda a
2.3× a velocidade de phi4:14b denso. Load lenta do phi4 sugere que
`OLLAMA_MAX_LOADED_MODELS=2` descarregou ele durante o smoke test
sequencial — em produção com KEEP_ALIVE=24h o load só paga uma vez.

Decisão: **qwen3-coder:30b vira default de coding**, gpt-oss:20b
vira default de reasoning/tool-use, phi4:14b fica como especialista
math/reasoning barato.

## Próximos passos (pendente)

- [ ] Replicar bateria do vídeo (site teclados + pinball + Angry Birds) nos 3 novos vs `qwen2.5:32b` — critério objetivo de default
- [ ] Adicionar preset do Axis com roteamento por capability (coder/reasoning/general)
- [ ] Avaliar bump de `OLLAMA_NUM_CTX` de 4096 → 16384 (qwen3-coder suporta 256k nativo, mas trade-off de RAM)
- [ ] Investigar upgrade Ollama 0.20.3 → versão corrente (há fixes de perf p/ MoE novos)

## Comandos de verificação rápida

```bash
# Listar modelos na VPS
ssh root@100.68.217.36 'ollama list'

# Smoke test de um modelo
ssh root@100.68.217.36 'ollama run qwen3-coder:30b "hello" --verbose'

# Ver logs do serviço
ssh root@100.68.217.36 'journalctl -u ollama -n 50 --no-pager'

# Endpoint OpenAI-compatible
curl http://100.68.217.36:11434/v1/models | jq
```
