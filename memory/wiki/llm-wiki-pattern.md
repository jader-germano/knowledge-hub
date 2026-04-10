# LLM Wiki — Padrão Karpathy

> Compilado de: `raw/videos/sboNwYmH3AY_karpathy-llm-wiki.md`  
> Última atualização: 2026-04-08

## O que é

Sistema de knowledge base pessoal onde o LLM é o editor ativo de um grafo de
arquivos Markdown. Proposto por Andrej Karpathy em post que viralizou em 2026.

**Premissa central:** não precisamos de vector database, embeddings ou chunking
pipelines. Um LLM com bom contexto + arquivos Markdown organizados + grep é
suficiente para centenas de documentos (~100 artigos, ~500K palavras).

## Arquitetura (3 camadas)

```
vault/
├── raw/          ← fontes brutas, imutáveis (PDFs, transcrições, artigos)
│   └── *.md
└── wiki/         ← compilações editáveis pelo LLM
    ├── CLAUDE.md ← schema: como operar este vault
    ├── index.md  ← índice de todos os nodes e relações
    ├── log.md    ← histórico de operações (quando foi ingerido o quê)
    └── <tema>.md ← wiki pages temáticas com backlinks
```

## Fluxo Operacional

1. **Ingest:** jogar fonte em `raw/` → dizer ao LLM "ingira isso"
2. **Compile:** LLM lê a fonte, cria N wiki pages temáticas com backlinks
3. **Query:** perguntar ao LLM sobre o domínio — ele navega pelo índice + wiki
4. **Lint:** rodar health check periódico para encontrar dados inconsistentes,
   preencher gaps com web search, encontrar conexões novas

## Princípios Chave

| Princípio | Descrição |
|-----------|-----------|
| **Raw é imutável** | Fontes nunca são editadas após captura |
| **Wiki é editável** | LLM reescreve quando conhecimento evolui |
| **Flat > nested** | Karpathy prefere sem subpastas quando escala é pequena |
| **Index + backlinks** | Navegação por links, não similarity search |
| **CLAUDE.md como schema** | O contrato operacional fica no vault |

## Comparação com Semantic Search / RAG

| Critério | LLM Wiki | Semantic RAG |
|----------|----------|-------------|
| Infraestrutura | Markdown puro | Embedding model + vector DB + chunking |
| Custo | Apenas tokens | Compute + storage contínuos |
| Escala sweet spot | < milhares de docs | Milhões de docs |
| Manutenção | Lint periódico | Re-embed quando há mudanças |
| Relações | Links explícitos | Similaridade aproximada |
| Observabilidade | Alta (tudo é arquivo) | Baixa (vetores são opacos) |

## Hot Cache (opcional)

Para assistentes executivos ou agentes com memória operacional frequente:
- `wiki/hot.md` — ~500 palavras do contexto mais recente
- Evita ter que rastrear múltiplas wiki pages para perguntas recorrentes

## Ganho Real (dado do vídeo)

> Um usuário transformou 383 arquivos dispersos + 100 transcrições de meetings
> em um wiki compacto → **redução de 95% no uso de tokens** ao consultar com Claude.

## Aplicação no workspace JPGLabs

O mapeamento para este workspace está em:
`jpglabs/docs/research/adr/ADR-001-llm-wiki-architecture.md`

- `raw/` → `jpglabs/docs/raw/`
- `wiki/` → `jpglabs/docs/memory/wiki/` (esta pasta)
- `schema` → `WORKSPACE_BOOTSTRAP.md` + `CLAUDE.md` + `RULES.md`
- `log` → `daily/*.md` + `agents/AGENT_BRIDGE.md`
