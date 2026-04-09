# piphone-ios Roadmap

Atualizado em `02/04/2026`.

## Papel No Ecossistema

`piphone-ios` é o shell iPhone do ecossistema Pi. Ele deve continuar fino,
mas a interação principal agora deve ser `LLM first`, com provedores diretos e
fallback local protegido só para contingência e superfícies sensíveis.

## Leitura Atual

- o app já foi reduzido para poucas superfícies centrais
- já possui integração direta com Anthropic, OpenAI e Gemini
- o próximo salto útil é UI/UX + fechamento das superfícies protegidas que ainda
  carregam linguagem e contratos Pi-first
- a fase 1 de homologação já suavizou header, voice lane e settings
- o fluxo de voz foi endurecido com isolamento melhor de estado e testes iniciais

## Progresso Recente

- branding visual atualizado para `PiePhone`
- política de apresentação de voz extraída para helper puro e testável
- suíte inicial verde com `3/3` testes
- build e teste validados no simulador local

## Trilhas

### Trilha 1 — Redesign Da Shell iPhone (`P0`)

- redesenhar a navegação e a hierarquia das superfícies atuais
- alinhar portfolio view, management panel e voice lane
- aplicar padrões mais recentes de iOS sem descaracterizar o papel de cliente
  fino

### Trilha 2 — Provedores Diretos + Fallback Protegido (`P0`)

- manter Anthropic, OpenAI e Gemini como caminho primário de interação
- restringir o `pi-local-app` a fallback local, `session.sync` e superfícies
  gerenciais protegidas
- impedir drift entre experiência pública/pessoal e operações protegidas

### Trilha 3 — Fechamento Operacional (`P1`)

- alinhar melhor `session.sync`, inbox e estados de erro
- fechar estados vazios, indisponibilidade do serviço e feedback de voz

## Próximas Ações

1. Fechar a revisão de `AgentControlCenterView`, `MemorySync` e fluxos de copy
   ainda Pi-first.
2. Materializar o protótipo visual no Figma a partir de [`FIGMA_HANDOFF.md`](/Users/philipegermano/code/jpglabs/docs/projects/piphone-ios/FIGMA_HANDOFF.md).
3. Validar instalação em device com provisioning ativo após a fase 1.
4. Definir a ponte autenticada para VPS/CLI remoto sem reintroduzir o Pi como
   caminho principal de chat.
