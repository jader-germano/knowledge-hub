# Session Close Template

Use esta estrutura no fechamento de sessão e em handoffs entre provedores.

Esta estrutura deve ser usada em dois lugares no fechamento:

1. no resumo final em texto da sessão
2. na entrada correspondente em `/Users/philipegermano/code/daily/<yyyy-mm-dd>.md`

O relatório diário deve receber uma nova entrada por sessão, sempre iniciada
com timestamp completo do fechamento.

Obrigatoriedade adicional para qualquer resumo final de sessão:

- sempre incluir `Commands Executed`, mesmo quando os comandos forem poucos
- sempre incluir `Change Tree`, mesmo quando a árvore precisar ser curta ou
  truncada
- sempre incluir `References And Glossary`, mesmo quando não houver termo novo
  para registrar
- quando a sessão introduzir, traduzir, normalizar ou corrigir terminologia em
  múltiplos idiomas, incluir também a assinatura `Glossário multilíngue`
- quando não houver comandos relevantes ou alterações em arquivo, declarar isso
  explicitamente em vez de omitir a seção
- sempre registrar a mesma sessão no diário raiz do workspace

Para sessões de `feature`, os blocos `Session Metadata`, `Delivery Contract`,
`Prototype And Evidence` e `Validation` são obrigatórios.

Referência transversal:

- `agents/FEATURE_DELIVERY_RITUAL.md`

## Session Metadata

- Timestamp completo do fechamento
- Data da sessão
- `feature/session id`
- `Provider`, quando conhecido
- Repositório
- Branch ativa
- Objetivo aprovado

## Delivery Contract

- Entregáveis explícitos da sessão
- O que ficou fora do escopo

## Prototype And Evidence

- Link do arquivo ou frame Figma
- Pasta de evidências:
  `/Users/philipegermano/code/jpglabs/docs/projects/<repo>/sessions/<feature-id>/<yyyy-mm-dd-session>/`
- `macos.gif`: fluxo validado e contexto
- `ios.gif`: fluxo validado e contexto
- screenshots e logs auxiliares, se existirem

Se a sessão não for uma entrega funcional de feature, declarar isso aqui de
forma explícita.

## Summary

- O que foi implementado, ajustado ou descoberto
- O que permanece aberto

## Validation

- Builds executados
- Testes executados
- Cobertura atingida na fatia entregue
- Gaps de cobertura remanescentes e justificativa técnica
- Validação em macOS
- Validação em iOS

## Commands Executed

Obrigatório em todo fechamento de sessão.

- `command`
  - Action: propósito do comando
  - Result: resultado observado na sessão

## Files Created

- Caminho absoluto

## Files Modified

- Caminho absoluto

## Change Tree

Obrigatório em todo fechamento de sessão.

Inclua a menor árvore útil para localizar as mudanças no Git ou no projeto.
Se a lista for extensa, trunque e priorize a localização.

```text
jpglabs/docs
├── agents
│   └── SESSION_CLOSE_TEMPLATE.md [modified]
├── manifests
│   └── skills.index.yaml [new]
└── skills
    └── ptbr-docs-standard
        └── SKILL.md [new]
```

## Versioning Proposal

Quando as mudanças da sessão forem aceitas, propor imediatamente:

- branch nova no padrão Gitflow, relacionada ao contexto da alteração
- commit message objetiva e contextual
- pedido de revisão do commit antes de seguir para push ou PR
- manter autoria humana do commit por default, sem `Co-Authored-By` para
  agentes, salvo decisão explícita em sentido contrário
- quando agentes tiverem participado materialmente da sessão, registrar o uso
  de IA em `PR`, handoff, `ADR` ou diário, não no rodapé do commit por padrão
- quando a sessão tocar `MCP`, distinguir explicitamente:
  - servidores apenas disponíveis no catálogo
  - servidores configurados no `.mcp.json`
  - servidores realmente validados por `dry-run` no host

Formato mínimo:

- Branch: `feature/<contexto>` | `fix/<contexto>` | `docs/<contexto>` | `hotfix/<contexto>`
- Commit: `type(scope): resumo curto`
- Review request: confirmar staging, diff e mensagem antes de consolidar

Política complementar de autoria:

- por padrão, commits continuam com autoria humana e não devem incluir
  `Co-Authored-By` de agentes quando o trabalho tiver sido conduzido sob
  direção, revisão e aprovação humanas
- quando houver apoio de IA relevante, registrar isso no resumo da sessão,
  no handoff, no `PR` ou em `ADR`, com descrição objetiva da participação:
  pesquisa, arquitetura, Figma handoff, implementação, testes, revisão ou
  observabilidade

## References And Glossary

Obrigatório em todo fechamento de sessão.

- fontes consultadas hoje, com indicação objetiva do que foi acessado ou
  extraído
  - exemplo local:
    - `/Users/philipegermano/code/WORKSPACE_BOOTSTRAP.md` — bootstrap relido
      para validar o contrato de fechamento
  - exemplo remoto/origem Git:
    - `GitHub origin via gh repo list jader-germano --limit 200` — listados os
      repositórios do owner; confirmados `portfolio-v2` e
      `jpglabs-portfolio`
    - `GitHub origin via gh api repos/jader-germano/jpglabs-portfolio/contents/package.json`
      — confirmado `Vite + React`, sem `Next.js`
- sempre declarar explicitamente quando nenhum termo novo entrar no glossário
- Novos termos introduzidos nesta sessão → registrar em `GLOSSARY.md`
  - Formato: `` `termo` — definição curta ``
  - Após registrar, referenciar aqui apenas o link âncora:
    `[termo](/Users/philipegermano/code/jpglabs/docs/GLOSSARY.md#termo)`

## Glossário multilíngue

Assinatura adicional do fechamento.

Obrigatório quando a sessão introduzir ou consolidar termos em mais de um
idioma, ou quando houver decisão relevante de nomenclatura, tradução, prompt,
copy, UX ou documentação bilíngue/multilíngue.

Quando não se aplicar, declarar explicitamente:

- `Glossário multilíngue: não aplicável nesta sessão.`

Formato mínimo quando aplicável:

- tabela com colunas `Termo (pt-BR) | English | Français | Italiano | 日本語`
- listar apenas os termos realmente introduzidos, corrigidos, validados ou
  harmonizados na sessão
- após a tabela, usar `Curiosidades linguísticas` apenas quando isso preservar
  contexto técnico, etimologia útil, diferença semântica entre idiomas ou
  convenção operacional importante
- se o termo também precisar entrar no glossário canônico do workspace,
  registrar em `GLOSSARY.md` e citar a referência em `References And Glossary`

## Risks And Gaps

- Pendências que impedem fechar a feature inteira
- Riscos residuais após a validação atual

## Next Actions

- Ações curtas, explícitas e verificáveis
- Se uma ação não revogar nem desviar do comando original aprovado, ela deve
  ser executada na sessão atual; deixe em `Next Actions` apenas o que ficou
  bloqueado, depende de nova aprovação ou saiu de escopo

## Handoff Notes

- Tudo que o próximo agente/provedor precisa preservar

## Comando Canônico De Sync

Depois que `report.md` estiver fechado, o sync canônico do fechamento passa a
ser:

```bash
python3 /Users/philipegermano/code/jpglabs/docs/scripts/sync-session-close.py \
  --report /Users/philipegermano/code/jpglabs/docs/projects/<repo>/sessions/<feature-id>/<yyyy-mm-dd-session>/report.md \
  --write
```

Esse comando:

- sincroniza a entrada correspondente em `/Users/philipegermano/code/daily/`
- sincroniza um resumo operacional em `agents/AGENT_BRIDGE.md`
- emite ou atualiza o sidecar JSON em `memory/events/`
- tenta projetar o sidecar no grafo derivado
- não invalida o fechamento se a projeção falhar, desde que `report.md`,
  diário e sidecar tenham sido gravados com sucesso
