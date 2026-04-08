# pibar-macos Roadmap

Atualizado em `02/04/2026`.

## Papel No Ecossistema

`pibar-macos` é o shell desktop do ecossistema Pi. Ele precisa maximizar
controle, contexto e densidade de informação sem competir com o runtime nem com
o hub operador web.

## Leitura Atual

- já houve redesign em Liquid Glass
- o app já expõe life manager e chat em cima do contrato Pi
- o próximo passo não é só polish visual; é reorganizar a UX com clareza de
  papel
- a fase 1 de homologação já reduziu quebra de texto, suavizou a shell e abriu
  testes de política visual/voz

## Progresso Recente

- branding visual atualizado para `PieBar`
- política de voz extraída para helper puro e testável
- suíte inicial verde com `5/5` testes
- build/test macOS validado localmente

## Trilhas

### Trilha 1 — Redesign Desktop (`P0`)

- revisar a arquitetura de informação do app
- equilibrar densidade de operador com estética recente
- manter a barra/menu app clara e previsível em estados normais e degradados

### Trilha 2 — Convergência Entre Clientes (`P0`)

- alinhar estados, terminologia e fluxo com `piphone-ios`
- preservar diferenças legítimas de desktop sem drift de produto

### Trilha 3 — Robustez De Runtime (`P1`)

- revisar mensagens de erro, indisponibilidade e fallback do Pi service
- melhorar visibilidade de sessão, contexto e ações pendentes

## Próximas Ações

1. Extrair subviews do [`PiBarView.swift`](/Users/philipegermano/code/jpglabs/pibar-macos/PiBar/PiBarView.swift) para reduzir churn e ampliar cobertura.
2. Materializar o protótipo visual no Figma a partir de [`FIGMA_HANDOFF.md`](/Users/philipegermano/code/jpglabs/docs/projects/pibar-macos/FIGMA_HANDOFF.md).
3. Alinhar a linguagem com `piphone-ios` antes da próxima rodada de UI.
4. Fechar a validação com assinatura real do app macOS quando o ambiente de provisioning estiver estável.
