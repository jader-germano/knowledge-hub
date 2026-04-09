# Session Report - Memory Hybrid Sidecar Projector

## Session Metadata

- timestamp: `2026-04-06T11:06:05-03:00`
- session id: `docs-memory-hybrid-sidecar-projector`
- workspace: `/Users/philipegermano/code`
- provider: `codex`
- scope: formalizar a arquitetura híbrida `Markdown + JSON sidecar + projector`

## Delivery Contract

- entregar um contrato canônico de sidecar para memória operacional
- entregar um projector idempotente para o Docker MCP `memory`
- preservar `jpglabs/docs` como hub canônico

## Summary

- o namespace canônico de memória continua em Markdown
- `memory/events/` passa a ser a trilha estruturada de sidecars
- `docs/scripts/project-memory-graph.py` projeta sidecars para o grafo derivado
- `docs/scripts/backfill-session-sidecars.py` importa relatórios históricos para
  sidecars parciais sem inventar fidelidade inexistente
- a projeção do grafo ficou deliberadamente conservadora: `commands` e
  `files_touched` continuam no sidecar e não entram no grafo derivado
- o projector foi desenhado para ser rebuildable e para não bloquear fechamento
  de sessão quando a lane Docker MCP falhar
- o projector reconcilia observações gerenciadas por prefixo, removendo valores
  antigos antes de adicionar o estado atual do sidecar
- o `--apply` foi validado contra o gateway Docker real, reconciliou o sidecar
  final desta sessão e fechou em estado idempotente com `49` entidades e `90`
  relações no grafo derivado

## Validation

- `python3 -m py_compile /Users/philipegermano/code/jpglabs/docs/scripts/project-memory-graph.py`
  - resultado observado: compilação limpa do script
- `python3 -m py_compile /Users/philipegermano/code/jpglabs/docs/scripts/backfill-session-sidecars.py`
  - resultado observado: compilação limpa do script
- `python3 /Users/philipegermano/code/jpglabs/docs/scripts/project-memory-graph.py --dry-run --sidecar /Users/philipegermano/code/jpglabs/docs/memory/events/2026-04-06/docs-memory-hybrid-sidecar-projector.json`
  - resultado observado: plano consistente com `12` entidades e `16` relações
- `python3 /Users/philipegermano/code/jpglabs/docs/scripts/backfill-session-sidecars.py --write`
  - resultado observado: `4` sidecars históricos gerados e `1` sessão atual
    corretamente ignorada por já possuir sidecar
- `python3 /Users/philipegermano/code/jpglabs/docs/scripts/project-memory-graph.py --dry-run`
  - resultado observado: plano agregado consistente com `47` entidades e `86`
    relações para `5` sidecars
- `python3 /Users/philipegermano/code/jpglabs/docs/scripts/project-memory-graph.py --apply`
  - resultado observado: primeira aplicação criou `47` entidades e `86`
    relações no grafo derivado
- `python3 /Users/philipegermano/code/jpglabs/docs/scripts/project-memory-graph.py --apply`
  - resultado observado: segunda aplicação confirmou idempotência inicial com
    `0/0/0`
- `python3 /Users/philipegermano/code/jpglabs/docs/scripts/project-memory-graph.py --apply`
  - resultado observado: após enriquecer o sidecar final, a reaplicação criou
    `2` entidades, adicionou `3` observações e criou `4` relações
- `python3 /Users/philipegermano/code/jpglabs/docs/scripts/project-memory-graph.py --apply`
  - resultado observado: depois do endurecimento da reconciliação de
    observações, a reaplicação removeu `4` observações antigas, adicionou `1`
    observação consolidada e manteve o shape em `49/90`
- `python3 /Users/philipegermano/code/jpglabs/docs/scripts/project-memory-graph.py --apply`
  - resultado observado: a última reaplicação confirmou o estado final
    idempotente com `0/0/0` e shape consolidado de `49` entidades e `90`
    relações

## Files Created

- `/Users/philipegermano/code/jpglabs/docs/memory/EVENTS_CONTRACT.md`
- `/Users/philipegermano/code/jpglabs/docs/memory/events/README.md`
- `/Users/philipegermano/code/jpglabs/docs/memory/schemas/session-memory-sidecar.schema.json`
- `/Users/philipegermano/code/jpglabs/docs/scripts/backfill-session-sidecars.py`
- `/Users/philipegermano/code/jpglabs/docs/scripts/project-memory-graph.py`
- `/Users/philipegermano/code/jpglabs/docs/projects/docs/sessions/memory-hybrid-sidecar-projector/2026-04-06-session/report.md`
- `/Users/philipegermano/code/jpglabs/docs/memory/events/2026-04-06/docs-memory-hybrid-sidecar-projector.json`
- `/Users/philipegermano/code/jpglabs/docs/memory/events/2026-03-31/docs-claude-cli-teams-enable-2026-03-31-session.json`
- `/Users/philipegermano/code/jpglabs/docs/memory/events/2026-03-31/docs-code-root-reclassify-and-llm-context-2026-03-31-session.json`
- `/Users/philipegermano/code/jpglabs/docs/memory/events/2026-03-31/docs-root-bootstrap-decouple-2026-03-31-session.json`
- `/Users/philipegermano/code/jpglabs/docs/memory/events/2026-04-02/docs-kaidi-sdr-recovery-case-2026-04-02-session.json`

## Risks And Gaps

- o grafo Docker MCP continua um derivado operacional, não um ledger
- o backfill histórico é propositalmente parcial: provider e timestamp antigo
  permanecem aproximados quando o report legado não os traz explicitamente
- `AGENT_BRIDGE.md` e o diário raiz foram atualizados nesta fatia, mas o
  fechamento padrão ainda não automatiza a emissão do sidecar e a projeção
  do grafo

## Next Actions

- acoplar a emissão do sidecar ao fluxo padrão de `SESSION_CLOSE_TEMPLATE.md`
- curar os sidecars importados quando houver metadata histórica mais precisa
