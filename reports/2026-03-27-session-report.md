# Relatório da Sessão — 2026-03-27

## Summary

- O host iOS do `apple-study-checklist` foi estabilizado como app bundle real.
- A referência quebrada ao produto Swift Package `AppleStudyChecklist` foi corrigida no projeto Xcode host.
- A assinatura automática passou a funcionar com a conta Apple ativa.
- O build iOS foi validado com sucesso quando o `DerivedData` ficou fora do iCloud Drive.
- O workspace inteiro foi movido de `~/Library/Mobile Documents/com~apple~CloudDocs/code` para `~/code`.
- Configurações ativas de Codex, Claude e docs principais foram reancoradas para o novo root.
- Foi documentado um plano transversal de proteção para AI agents e operação local-first.

## Commands Executed

- `xcodebuild -project AppleStudyChecklistHost.xcodeproj -scheme AppleStudyChecklistiOS -destination 'generic/platform=iOS' ... build`
  - Action: validar o host iOS e isolar erros de assinatura e empacotamento.
  - Result: o build resolveu package, signing e bundle; falhou no root antigo por metadata do iCloud e passou com `DerivedData` em `/tmp`.

- `xcrun xctrace list devices`
  - Action: verificar se o iPhone conectado estava visível ao toolchain.
  - Result: o aparelho apareceu como `Offline`, então a instalação física ainda depende da reconexão do device no Xcode.

- `xattr -lr ...` e `xattr -rc ...`
  - Action: identificar e limpar extended attributes que bloqueavam o `codesign`.
  - Result: confirmou `com.apple.provenance` e `FinderInfo` no bundle gerado em iCloud; limpeza local ajudou no diagnóstico, mas a solução real foi tirar o `DerivedData` do iCloud.

- `mv ~/Library/Mobile\\ Documents/com~apple~CloudDocs/code/* ~/code/`
  - Action: mover o workspace físico inteiro para fora do iCloud Drive.
  - Result: os repositórios principais foram movidos com sucesso para `~/code`.

- `rg -uu -l 'old-path' ...`
  - Action: localizar referências absolutas para o root antigo.
  - Result: configs ativas e documentação viva foram atualizadas para o novo root.

## Files Created

- `/Users/philipegermano/code/jpglabs-knowledge-hub/AI_AGENT_PROTECTION_PLAN.md`
- `/Users/philipegermano/code/apple-study-checklist/docs/product/roadmap.md`
- `/Users/philipegermano/code/jpglabs-knowledge-hub/reports/2026-03-27-session-report.md`

## Files Modified

- `/Users/philipegermano/code/apple-study-checklist/AppleStudyChecklistHost.xcodeproj/project.pbxproj`
- `/Users/philipegermano/code/apple-study-checklist/Configs/Signing.xcconfig`
- `/Users/philipegermano/code/apple-study-checklist/README.md`
- `/Users/philipegermano/code/apple-study-checklist/docs/README.md`
- `/Users/philipegermano/code/apple-study-checklist/docs/product/README.md`
- `/Users/philipegermano/code/jpglabs-knowledge-hub/.codex/docker-mcp-config.yaml`
- `/Users/philipegermano/code/jpglabs-knowledge-hub/README.md`
- `/Users/philipegermano/code/jpglabs-knowledge-hub/MCP_SETUP.md`
- `/Users/philipegermano/code/jpglabs-knowledge-hub/.codex/AGENT_BRIDGE.md`
- `/Users/philipegermano/.codex/config.toml`
- `/Users/philipegermano/Library/Application Support/Claude/claude_desktop_config.json`

## Build Planning

### Build local

- Manter o projeto em `~/code/apple-study-checklist`.
- Para builds iOS assinados por CLI, usar `DerivedData` fora de iCloud, por exemplo:
  - `DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer xcodebuild -project AppleStudyChecklistHost.xcodeproj -scheme AppleStudyChecklistiOS -destination 'generic/platform=iOS' -derivedDataPath /tmp/apple-study-checklist-xcode-device-build build`
- Para macOS e testes do pacote:
  - `DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer swift test`
- Para abrir no Xcode:
  - `open /Users/philipegermano/code/apple-study-checklist/AppleStudyChecklistHost.xcodeproj`

### Build para iPhone

- Garantir que o iPhone esteja `Online` no Xcode.
- Validar novamente com:
  - `DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer xcrun xctrace list devices`
- Quando o device estiver online, rodar:
  - `DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer xcodebuild -project AppleStudyChecklistHost.xcodeproj -scheme AppleStudyChecklistiOS -destination 'id=00008030-001805182128202E' -derivedDataPath /tmp/apple-study-checklist-xcode-device-build build`
- Se a UI do Xcode for usada, manter `Automatically manage signing` com o time já ativo.

## Sandbox Changes

- O root operacional do workspace passou a ser:
  - `/Users/philipegermano/code`
- O root antigo em iCloud deixou de ser o caminho canônico para builds e edição.
- Configs ativas de Codex e Claude foram reancoradas para o novo root.
- A prática nova para builds assinados é evitar `DerivedData` dentro de iCloud Drive.
- Ficou um stub residual antigo em `~/Library/Mobile Documents/com~apple~CloudDocs/code/jpglabs-knowledge-hub/.codex/docker-mcp-config.yaml`, indicando que algum app ainda aberto pode recriar o caminho antigo.

## References And Glossary

- [Akita: AI Agents - Garantindo a Proteção do seu Sistema](https://akitaonrails.com/2026/01/10/ai-agents-garantindo-a-protecao-do-seu-sistema/)
- [FrankMD upstream](https://github.com/akitaonrails/FrankMD)
- [Open Source Guides](https://opensource.guide/)

Glossário mínimo:

- `DerivedData`: diretório temporário de build do Xcode.
- `codesign`: assinatura do app e dos binários Apple.
- `local-first`: arquitetura cujo fluxo principal funciona sem depender de serviços externos.
- `workspace root`: diretório base compartilhado pelos repositórios e configs ativas.

## Next Actions

1. Reiniciar Codex, Claude e Xcode para parar qualquer recriação do path antigo em iCloud.
2. Revalidar o iPhone conectado até ele aparecer como `Online`.
3. Rodar o build físico do aparelho usando `DerivedData` em `/tmp`.
4. Commitar as mudanças pendentes em `apple-study-checklist` e `jpglabs-knowledge-hub`.

## Handoff Notes

- O package product quebrado do host iOS já foi corrigido.
- O signing CLI agora funciona, desde que o build não grave o bundle final em iCloud Drive.
- O novo root operacional é `~/code`; documentação e configs vivas já foram reancoradas.
- Não usar o root antigo como referência nova.
