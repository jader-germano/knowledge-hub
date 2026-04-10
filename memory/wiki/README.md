# memory/wiki/ — Compilações Temáticas (LLM Wiki)

Esta pasta implementa a **wiki layer** do padrão Karpathy dentro do namespace
canônico de memória do workspace.

## Propósito

Compilações temáticas, sínteses e cross-references derivados das fontes brutas em
`jpglabs/docs/raw/`. O LLM é o editor ativo desta pasta — atualiza conforme novos
vídeos, artigos ou sessões são processados.

## Distinção com o restante de `memory/`

| Pasta | Tipo de conteúdo | Quem atualiza |
|-------|-----------------|---------------|
| `memory/PI_MEMORY.md` | Ledger operacional (estado, infra, projetos) | Agente ao fim de sessão |
| `memory/sessions/` | Logs de sessão incorporados | Agente ao fim de sessão |
| `memory/wiki/` | Sínteses temáticas de conhecimento | Agente ao compilar raw/ |

## Convenção de nomes

- `llm-wiki-pattern.md` — conceitos gerais (ex.: padrão Karpathy)
- `pi-coding-agent.md` — insights do vídeo Pi Coding Agent (Zechner)
- `<tema>.md` — qualquer compilação temática transversal

## Regras

1. Todo arquivo aqui deve citar a fonte em `raw/` ou URL rastreável
2. O conteúdo é editável — reescrever quando o conhecimento evoluir
3. Manter compacto: sínteses, não dumps; o dump fica em `raw/`
4. Referenciar em `MEMORY.md` (auto-memory pessoal) apenas quando for
   relevante para comportamento futuro do agente

## Ver também

- `jpglabs/docs/raw/README.md` — camada imutável
- `jpglabs/docs/research/adr/ADR-001-llm-wiki-architecture.md` — decisão arquitetural
