# pi-local-app Roadmap

Atualizado em `02/04/2026`.

## Papel No Ecossistema

`pi-local-app` é o contrato central do ecossistema Pi. Ele deve permanecer como
runtime, API e surface de integração, não como lugar onde regras de UI do
produto ficam acopladas por acidente.

## Leitura Atual

- já concentra memória, inbox, session sync e surface HTTP/MCP
- já serve clientes finos como `PiPhone` e `PiBar`
- agora precisa assumir melhor o papel de runtime/autenticação/ponte remota
  sem voltar a carregar naming legado como `OpenClaw`

## Trilhas

### Trilha 1 — Contrato De Runtime (`P0`)

- congelar a surface canônica consumida pelos clientes
- explicitar fronteiras entre auth, session, memory, inbox e chat
- reduzir drift entre rotas novas e aliases legados

### Trilha 2 — Split Runtime vs Shell Web (`P0`)

- separar decisões de produto/UI da camada de runtime
- manter a UI embutida apenas como shell operacional mínima
- impedir que o portfólio público ou decisões de cliente rico vazem para este
  repo

### Trilha 3 — Preparação Para Cliente Compartilhável (`P1`)

- isolar o contrato que poderá virar SDK/package compartilhável para web/mobile
- reduzir dependências acidentais do workspace local no consumo dos clientes

### Trilha 4 — Ponte Remota Autenticada (`P0`)

- usar o runtime como ponte segura para VPS, MCP memory e CLIs remotos
- preferir conectividade `Tailscale-first` com fallback público explícito
- tratar autenticação do usuário e autorização de provider como contratos
  centrais do runtime
### Trilha 5 — Observabilidade E Governança (`P1`)

- manter `threads` como lease board técnico
- alinhar backlog/roadmap à governança `Jira + Confluence`
- preservar `session.sync` como fechamento operacional

## Próximas Ações

1. Inventariar quais endpoints são contrato estável e quais ainda são
   compatibilidade.
2. Fechar a remoção de naming legado remanescente (`OpenClaw`) dos contratos
   ativos.
3. Documentar a ponte autenticada para VPS/CLI/MCP memory e o papel do
   `Tailscale`.
4. Delimitar o que permanece na UI embutida e o que deve migrar para clientes
   dedicados.
