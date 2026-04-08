# PieCenter Project Context

## Nicho

- cliente Apple unificado para substituir, no futuro, `PiPhone` e `PiBar`
- shell leve e nativa para iPhone + macOS

## Stack

- SwiftUI
- Observation
- XcodeGen

## Sinal Atual

- o projeto nasce como substituto de duas shells separadas
- o macOS deve ter menu bar + janela expandida
- o iPhone deve manter uma navegação simples e objetiva
- scaffold já gerado e validado com `xcodegen` + `xcodebuild` para iOS
  e macOS CLI com `CODE_SIGNING_ALLOWED=NO`

## Decisão De Nome

- `PieCenter` foi escolhido como nome-umbrella porque descreve um centro de
  controle, não um dispositivo específico
- isso reduz o drift conceitual entre o cliente de bolso e o cliente desktop

## Repo Real

- `/Users/philipegermano/code/jpglabs/PieCenter`
