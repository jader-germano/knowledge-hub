# Reports Sessions

Este diretório não é mais o ledger canônico das sessões.

Use este namespace apenas para:

- `_template/`, como base de estrutura reutilizável
- views derivadas ou material auxiliar que não seja a fonte primária da sessão

O path canônico para novas sessões é:

- `/Users/philipegermano/code/jpglabs/docs/projects/<repo>/sessions/<feature-id>/<yyyy-mm-dd-session>/`

## Convenção de pasta

Não grave novas sessões em:

`reports/sessions/<feature-id>/<yyyy-mm-dd-session>/`

Grave em:

`/Users/philipegermano/code/jpglabs/docs/projects/<repo>/sessions/<feature-id>/<yyyy-mm-dd-session>/`

Exemplo canônico:

```text
/Users/philipegermano/code/jpglabs/docs/projects/docs/sessions/vault-local-workspace/2026-03-30-session/
├── report.md
├── prototype.md
├── macos.gif
├── ios.gif
└── screenshot-empty-vault.png
```

## Conteúdo mínimo

- `report.md`: fechamento estruturado da sessão
- `prototype.md`: link para o frame ou arquivo Figma e resumo do protótipo
- `macos.gif`: evidência funcional no macOS
- `ios.gif`: evidência funcional no iOS

## Regras

- sem a pasta de evidências, a sessão não fecha como entrega funcional
- `feature-id` deve permanecer estável entre sessões da mesma fatia
- uma nova sessão gera uma nova pasta datada dentro da mesma feature
- se a sessão for apenas de planejamento, registrar isso no `report.md`
- `reports/sessions/` não deve voltar a receber novos `report.md` canônicos

## Template

Use os arquivos em `_template/` como ponto de partida, mas salve o resultado no
path canônico em `projects/<repo>/sessions/`.
