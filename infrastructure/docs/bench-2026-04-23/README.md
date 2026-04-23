---
type: guide
title: Bench 2026-04-23 — Video MiniMax M2.7 Battery Replay
tags:
  - "#llm"
  - "#bench"
  - "#axis"
last_updated: "2026-04-23"
aliases:
  - bench video minimax
  - bench vps-ollama
---

# Bench 2026-04-23 — Replay da bateria do vídeo

## Objetivo

Replicar os 3 prompts usados no vídeo "MiniMax M2.7 localmente"
(YouTube `cGIXyqjZSD8`) nos modelos candidatos a default do Axis, com
métricas objetivas — não "vibe check".

## Setup

| Parâmetro | Valor |
|---|---|
| Host | `srv1443703` (AMD EPYC 9355P, 8 vCPU, 31 GiB RAM, CPU-only) |
| Ollama | 0.21.1 |
| `OLLAMA_NUM_CTX` | 16384 (aumentado de 4096) |
| Outros env | KEEP_ALIVE=24h, NUM_PARALLEL=2, NUM_THREADS=8, FLASH_ATTENTION=1 |
| Temperature | 0.7 |
| `num_predict` | 10000 |

## Prompts (3 tasks)

1. **keyboards** — "Crie um site HTML single-file para uma empresa de teclados mecânicos chamada KeyForge. Coloque alguma funcionalidade surpreendente fora da caixa (som, animações interativas, visualização 3D simples em canvas). Design moderno, cyberpunk, neon."
2. **pinball** — "Crie um jogo de pinball completo em HTML canvas single-file. Garanta que a bola sempre entre no campo de jogo ao iniciar e tenha física realista com as duas pazinhas controladas por setas. Inclua pontuação."
3. **angrybirds** — "Crie um clone de Angry Birds em HTML canvas single-file. Use um elástico para mirar e atirar pássaros em porquinhos. Inclua física de gravidade, colisão, pontuação e reinício."

## Métricas de velocidade

### Por run

| Modelo | Task | Tokens | Eval dur (s) | Tok/s |
|---|---|---:|---:|---:|
| `qwen3-coder:30b` | keyboards | 4 715 | 464.0 | 10.2 |
| `qwen3-coder:30b` | pinball | 2 131 | 134.3 | 15.9 |
| `qwen3-coder:30b` | angrybirds | 2 898 | 204.8 | 14.1 |
| `gpt-oss:20b` | keyboards | 2 362 | 110.2 | 21.4 |
| `gpt-oss:20b` | pinball | 2 464 | 114.0 | 21.6 |
| `gpt-oss:20b` | angrybirds | 2 049 | 92.6 | 22.1 |
| `qwen2.5:32b-instruct-q4_K_M` | keyboards | 589 | 118.7 | 5.0 |
| `qwen2.5:32b-instruct-q4_K_M` | pinball | 647 | 134.0 | 4.8 |
| `qwen2.5:32b-instruct-q4_K_M` | angrybirds | 969 | 210.7 | 4.6 |

### Agregado (tok/s médio ponderado)

| Modelo | Tok total | Dur total (s) | **Tok/s médio** | vs smoke test |
|---|---:|---:|---:|---|
| `gpt-oss:20b` (MoE MXFP4) | 6 875 | 316.8 | **21.7** | +6% (era 20.4) |
| `qwen3-coder:30b` (MoE A3B) | 9 744 | 803.1 | **12.1** | **-56% (era 27.3)** ⚠️ |
| `qwen2.5:32b` (denso) | 2 205 | 463.4 | **4.8** | — |

> ⚠️ qwen3-coder:30b perdeu ~56% de velocidade quando comparado ao
> smoke test com contexto curto. O aumento do NUM_CTX 4096→16384
> + verbosidade do modelo (gera 4715 tok no primeiro prompt!) derrubou
> o throughput. gpt-oss:20b manteve mesma performance — mais
> consistente para workload produtivo.

## Métricas de qualidade

Checagens programáticas em `analysis.txt` (script em `README.md`
desta pasta). Grep patterns: `<canvas>`, `<script>`, física
(`gravity|velocity|collision`), áudio (`AudioContext|<audio>`),
pontuação (`score`), `</html>` final.

| Modelo | Task | KB | JS KB | Canvas | Física | Áudio | Score | Veredito |
|---|---|---:|---:|:-:|:-:|:-:|:-:|---|
| `qwen3-coder:30b` | keyboards | 17.3 | 6.9 | — | — | — | — | Mais rico visualmente |
| `qwen3-coder:30b` | pinball | 8.7 | 7.9 | ✅ | ✅ | — | ✅ | App completo |
| `qwen3-coder:30b` | angrybirds | 13.2 | 12.9 | ✅ | ✅ | — | ✅ | App mais completo |
| `gpt-oss:20b` | keyboards | 5.8 | 1.6 | — | — | **✅** | ✅ | **Único com WebAudio** 🎵 |
| `gpt-oss:20b` | pinball | 5.1 | 4.7 | ✅ | ✅ | — | ✅ | OK |
| `gpt-oss:20b` | angrybirds | 4.6 | 4.1 | ✅ | ✅ | — | ✅ | OK |
| `qwen2.5:32b` | keyboards | 2.1 | 0.6 | — | — | — | — | Muito simples |
| `qwen2.5:32b` | pinball | 2.4 | 2.1 | ✅ | ✅ | — | ✅ | Funcional mas curto |
| `qwen2.5:32b` | angrybirds | 3.5 | 3.0 | ✅ | ✅ | — | — | Sem score |

Todos HTMLs com `</html>` fechado — nada truncado.

## Decisão

### Default para Axis `capability=coder`

**Tier 1 — qualidade**: `qwen3-coder:30b`
- Output 2–3× mais rico e completo
- Mais lento (12 tok/s) e verboso (gera muito token), custo por request maior
- Use para: refactor complexo, novos features, geração de componentes ricos

**Tier 2 — velocidade/Apache-2.0**: `gpt-oss:20b`
- 2× mais rápido que qwen3-coder (22 tok/s consistente)
- Licença Apache-2.0 — mais seguro para uso comercial
- **Surpresa do bench**: único que usou WebAudio no site de teclados ("fora da caixa" do prompt)
- Use para: tarefas objetivas, tool use, latency-sensitive

**Fallback**: `qwen2.5:32b-instruct-q4_K_M`
- 4.8 tok/s e outputs curtos — só quando coders específicos estiverem carregando
- Melhor para Q&A em PT-BR do que geração de código densa

### Roteamento final (atualiza preset)

```yaml
coder_complex:  qwen3-coder:30b   # qualidade > velocidade
coder_fast:     gpt-oss:20b       # latency + licença
coder_fallback: qwen2.5-coder:14b
```

## Arquivos

- `bench.log` — execução crua com timestamps
- `<modelo>__<task>.html` — 9 outputs (abrir no browser para inspecionar)
- `run.sh` está em `/tmp/bench/run.sh` na VPS (script do bench)
