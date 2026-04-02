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

Formato mínimo:

- Branch: `feature/<contexto>` | `fix/<contexto>` | `docs/<contexto>` | `hotfix/<contexto>`
- Commit: `type(scope): resumo curto`
- Review request: confirmar staging, diff e mensagem antes de consolidar

## References And Glossary

- Links estudados hoje
- Novos termos introduzidos nesta sessão → registrar em `GLOSSARY.md`
  - Formato: `` `termo` — definição curta ``
  - Após registrar, referenciar aqui apenas o link âncora:
    `[termo](/Users/philipegermano/code/jpglabs/docs/GLOSSARY.md#termo)`

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
