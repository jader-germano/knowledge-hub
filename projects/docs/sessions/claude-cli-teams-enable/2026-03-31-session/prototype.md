# Prototype

## Context

- `feature/session id`: `claude-cli-teams-enable/2026-03-31-session`
- Objetivo do protótipo: N/A
- Escopo validado nesta sessão: tooling local do Claude Code, agent teams e base MCP do workspace

## Figma Source

- File URL: N/A
- Frame URL: N/A
- Status do frame: não aplicável; sessão sem prototipagem visual

## Screens And Flows

- Tela 1: N/A
- Tela 2: N/A
- Fluxo principal: atualização do Claude Code, exposição do CLI, habilitação local de teams e configuração MCP
- Estados alternativos: fallback para uso do binário por caminho absoluto se `PATH` global ainda não estiver ajustado

## Platform Coverage

- macOS: validado para CLI e configuração local
- iPhone: N/A
- iPad: N/A

## Design Decisions

- Decisão: habilitar `agent teams` por `env` local em `.claude/settings.json`
- Impacto: reduz risco global e limita a ativação experimental a este workspace

- Decisão: expor `/teams` como skill local, e não como suposto comando nativo
- Impacto: mantém aderência à documentação oficial e reduz ambiguidade operacional

- Decisão: espelhar o gateway MCP do Claude Desktop em `.mcp.json`
- Impacto: melhora interoperabilidade entre Desktop e CLI no mesmo workspace

## Open Questions

- Questão: haverá um servidor MCP de Figma no catálogo Docker usado por este ambiente?
- Dono: próxima sessão de tooling/MCP

- Questão: o `PATH` global do usuário será corrigido via `~/.zshrc` ou ficará explícito por wrapper/local bin?
- Dono: configuração local do host

## Handoff

- O que o implementador deve preservar:
  - `.mcp.json`
  - `.claude/settings.json`
  - `.claude/skills/teams/SKILL.md`
- O que ainda precisa ser validado antes de código:
  - runtime do Docker MCP
  - execução real de uma equipe via `/teams`
