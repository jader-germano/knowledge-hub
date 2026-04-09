# Claude Shared Capabilities Audit

Data de referência: `2026-04-01`

## Escopo auditado

- `~/.claude.json`
- `~/.claude/scheduled-tasks/*/SKILL.md`
- `~/.claude/plugins/`
- runtime local do workspace em `/Users/philipegermano/code/.claude/`

## Achados

### Conectores e MCPs

- MCP efetivamente configurado no Claude global: `MCP_DOCKER`
- Esse conector já é compartilhável e deve continuar centralizado em:
  - `/Users/philipegermano/code/.mcp.json`
  - `/Users/philipegermano/code/config/mcp/docker-mcp-config.yaml`
  - `/Users/philipegermano/code/config/mcp/docker-mcp-shared-catalog.yaml`

Conclusão:

- não há evidência de novos conectores locais do Claude que precisem de
  migração adicional além do baseline Docker MCP já centralizado

### Plugins

Achados no Claude global:

- flags de marketplace/plugins oficiais na configuração interna
- `blocklist.json` com entradas de teste
- nenhuma instalação local de plugin com payload reutilizável no workspace

Conclusão:

- plugins/marketplace do Claude continuam provider-only
- só devem entrar na camada compartilhada se houver equivalente local
  executável via MCP, CLI ou skill canônico

### Skills

#### Skills custom encontradas no Claude

- `email-daily-triage`
- `github-activity-digest`
- `infra-health-check`
- `job-opportunities-scanner`
- `relatorio-mensal-tse`
- `teams` no runtime local do workspace

#### Skills Anthropic/Claude observadas em uso

- `xlsx`
- `mcp-builder`
- `relatorio-atividades-digisystem-mensal`

Conclusão:

- as skills custom acima são compartilháveis no workspace e devem viver em
  `/Users/philipegermano/code/.agents/skills/`
- as skills Anthropic continuam provider-only até existir equivalente local
  canônico

## Política recomendada

1. Skill reutilizável nasce em `/.agents/skills/`.
2. Claude recebe wrappers gerados em `/.claude/skills/`.
3. Codex consome a biblioteca compartilhada diretamente.
4. Gemini consulta a biblioteca compartilhada via bootstrap até existir loader
   local equivalente.
5. Novos conectores entram primeiro no baseline MCP compartilhado; não em
   configuração isolada de provider.
