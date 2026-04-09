# PiePhone Figma Handoff

Atualizado em `02/04/2026`.

## Estado Atual

- o redesign fase 1 ja saiu do papel no app SwiftUI
- o branding visivel passou para `PiePhone`
- o simbolo provisório da marca e `chart.pie.fill`
- esta sessão do plugin Figma nao expõe criacao automatica de arquivo; por isso este handoff descreve o que deve ser materializado no arquivo de design assim que o file key existir

## Norte Visual

- shell editorial suave, nao futurista agressiva
- foco em leitura, voz e troca entre provedores diretos
- fundos profundos com calor de `sand` e acento `accent`
- nada de cards pesados e nada de grid corporativo

## Tokens Confirmados No Código

- background: `#050608`
- surface: `#10131A`
- elevated: `#181C25`
- accent: `#E8A155`
- accent hi: `#F4C97A`
- sea: `#7DD3C5`
- steel: `#7DA0F0`
- sand: `#E8E1D6`

Fonte factual: [`ThemeKit.swift`](/Users/philipegermano/code/jpglabs/piphone-ios/PiPhone/ThemeKit.swift)

## Frames Prioritários

1. Shell header
   - logomarca `PiePhone`
   - pills compactas `LLM FIRST`, estado de acesso e superficie ativa
   - subtitulo em no maximo duas linhas
2. Voice lane
   - status title curto
   - hint em ate duas linhas
   - CTA principal compacto: `Conectar`, `Falar`, `Interromper`
3. Portfolio dashboard
   - cards editoriais com menos ruído
   - prioridade para narrativa e estado, nao para chrome
4. Settings
   - provider selection e fallback em blocos claros
   - linguagem menos `Pi-first`

## Regras De Layout

- evitar qualquer titulo maior que duas linhas
- usar pills com altura curta e largura elástica
- manter a barra inferior com cinco destinos sem truncamento duro
- todas as mensagens de estado devem caber em duas linhas com `minimumScaleFactor`

## Motion

- pulsos suaves de 0.9s a 1.2s
- sem motion contínuo fora de estados ativos de voz
- glow só quando houver captura, resposta ou streaming

## Próxima Entrega No Figma

- criar um arquivo `Pie Clients`
- adicionar uma page `PiePhone vNext`
- desenhar pelo menos `Shell`, `Voice`, `Portfolio`, `Protected Surface`
- mapear o frame principal para [`ContentView.swift`](/Users/philipegermano/code/jpglabs/piphone-ios/PiPhone/ContentView.swift) e a lane de voz para [`WaveformView.swift`](/Users/philipegermano/code/jpglabs/piphone-ios/PiPhone/WaveformView.swift)
