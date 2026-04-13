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
- sempre incluir `Language Policy`, mesmo quando a política aplicada for a
  padrão do workspace
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

## Language Policy

Obrigatório em todo fechamento de sessão.

- manter os títulos estruturais do template em English por interoperabilidade
  entre providers, automações e artefatos derivados
- preencher o conteúdo narrativo da sessão em `pt-BR` por default
- preservar em English nomes de arquivos, paths, comandos, branches, commits,
  APIs, MCPs, símbolos de código e contratos técnicos
- usar o `Glossário multilíngue` para contraste semântico, tradução de termos
  menos óbvios e decisão de nomenclatura; não repetir ali o que já foi
  explicado em `Summary`

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

Estilo desejado quando aplicável:

- manter útil e memorável, não acadêmico nem burocrático
- preferir tom leve, direto e um pouco mais solto, como nota de linguagem de
  trabalho
- usar o glossário para preservar contraste semântico entre idiomas, não para
  inflar a sessão com taxonomia desnecessária

Quando não se aplicar, declarar explicitamente:

- `Glossário multilíngue: não aplicável nesta sessão.`

Formato mínimo quando aplicável:

- preferir entre `5` e `10` termos realmente relevantes para a sessão
- tabela com colunas padronizadas
  `Termo (pt-BR) | ES | EN | IT | FR | 日本語 | 中文`
- listar apenas os termos realmente introduzidos, corrigidos, validados ou
  harmonizados na sessão
- em `日本語`, preferir grafia principal + apoio em kana ou `romaji` quando isso
  ajudar a leitura
- em `中文`, preferir `简体中文`; `pinyin` entra apenas quando houver ambiguidade
- após a tabela, preferir uma seção `Curiosidades linguísticas` curta, leve e
  útil, especialmente quando houver:
  - etimologia prática
  - contraste semântico relevante
  - analogia de engenharia que ajude a fixar o conceito
- se o termo também precisar entrar no glossário canônico do workspace,
  registrar em `GLOSSARY.md` e citar a referência em `References And Glossary`

Exemplo de tom aceitável:

```md
## Glossário multilíngue

| Termo (pt-BR) | ES | EN | IT | FR | 日本語 | 中文 |
|---|---|---|---|---|---|---|
| Desacoplamento | Desacoplamiento | Decoupling | Disaccoppiamento | Découplage | 疎結合 / そけつごう (soketsugo) | 解耦 |
| Esquema de banco | Esquema de base de datos | Database schema | Schema del database | Schéma de base de données | データベーススキーマ | 数据库模式 |

### Curiosidades linguísticas

- `Decoupling` veio da engenharia elétrica e continua sendo uma ótima analogia
  para separar componentes sem propagar interferência.
- `疎結合` significa literalmente algo como “ligação frouxa”, o que comunica
  bem a ideia de baixo acoplamento.
```

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
