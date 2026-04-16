# DEPRECATED — MIGRAÇÃO BLOQUEADA

Este diretório deveria ser migrado para:
`/Users/philipegermano/code/jpglabs/infrastructure/docs/`

## Status

**BLOQUEADO** — O repositório de destino `/code/jpglabs/infrastructure/` não existe
como repositório git independente no filesystem em 2026-04-16.

O `infrastructure/` encontrado em `jpglabs/docs/infrastructure/` e no worktree
`/code/.worktrees/knowledge-hub-sync/infrastructure/` é um subdiretório do knowledge-hub,
não um repositório separado.

## Ação necessária

Quando o repo `infrastructure` for criado como repositório independente, executar a migração:

```bash
cp -r /Users/philipegermano/code/jpglabs/docs/projects/infrastructure/* \
      /path/to/infrastructure/docs/
```

## Data do bloqueio

2026-04-16T00:00:00Z

> Os arquivos originais permanecem aqui e não foram deletados.
