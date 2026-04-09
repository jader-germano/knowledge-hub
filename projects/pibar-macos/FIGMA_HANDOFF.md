# PieBar Figma Handoff

Atualizado em `02/04/2026`.

## Estado Atual

- o app desktop foi suavizado para homologação inicial
- o branding visivel agora e `PieBar`
- o simbolo provisório da marca e `chart.pie.fill`
- esta sessão do plugin Figma nao expõe criacao automatica de arquivo; o handoff abaixo prepara a prototipação manual com base no código real

## Norte Visual

- menu bar shell elegante e densa
- mais calma visual, menos contraste estridente
- desktop operator shell, nao painel de provedor
- voz, contexto e quick actions devem parecer uma unica superficie

## Tokens Confirmados No Código

- accent: `#F97316`
- accent hi: `#F59E0B`
- sea: `#2DD4BF`
- steel: `#60A5FA`
- sand: `#F1E4D1`
- red: `#FB7185`
- background gradient: `#020509 -> #07101C -> #130B05`

Fonte factual: [`PiBarView.swift`](/Users/philipegermano/code/jpglabs/pibar-macos/PiBar/PiBarView.swift)

## Frames Prioritários

1. Panel shell
   - header compacto com status, provider e quick actions
   - largura ideal perto de `580`
2. Welcome state
   - orb central de voz
   - headline curta e subheadline em duas linhas
3. Chat state
   - bolhas enxutas, sem quebra agressiva
   - contexto lateral só se realmente necessário
4. Settings popover
   - configurações rápidas, nada de formulário pesado

## Regras De Layout

- largura ideal entre `580` e `720`
- evitar `lineLimit(1)` em textos longos de contexto
- status de runtime sempre curto: `Pensando...`, `Ouvindo...`, `Falando...`
- actions perigosas isoladas visualmente do provider switch

## Motion

- glow radial apenas em voz ativa ou streaming
- orb com pulso leve e sem ruído excessivo
- transitions rápidas e discretas para popover e troca de estado

## Próxima Entrega No Figma

- adicionar uma page `PieBar vNext` no mesmo arquivo `Pie Clients`
- prototipar `Panel`, `Welcome`, `Conversation`, `Settings`
- mapear a casca principal para [`PiBarView.swift`](/Users/philipegermano/code/jpglabs/pibar-macos/PiBar/PiBarView.swift)
