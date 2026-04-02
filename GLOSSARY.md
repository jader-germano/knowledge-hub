# Glossário — Workspace Docs

Fonte canônica de termos técnicos e conceituais usados nos projetos, sessões e
documentação do hub. Todo novo termo introduzido em qualquer sessão deve ser
registrado aqui.

**Formato de entrada:**
```
## `termo`
**Categoria:** infra / design / ai / produto / arquitetura / processo
**Contexto:** em qual projeto ou domínio o termo aparece
Definição clara em uma ou duas frases.
```

---

## Índice rápido

| Termo | Categoria | Projeto |
|---|---|---|
| [adaptive thinking](#adaptive-thinking) | ai | design-pipeline |
| [bootstrap mínimo](#bootstrap-mínimo) | processo | docs |
| [bus factor](#bus-factor) | processo | — |
| [Change Tree](#change-tree) | processo | docs |
| [codesign](#codesign) | infra | apple-study-checklist |
| [DerivedData](#deriveddata) | infra | apple-study-checklist |
| [filesystem-first](#filesystem-first) | arquitetura | FrankMD / apple-study-checklist |
| [HITL](#hitl) | processo | design-pipeline |
| [local-first](#local-first) | arquitetura | apple-study-checklist / FrankMD |
| [MCP](#mcp) | ai | pi-local-app / jpglabs |
| [native shell](#native-shell) | arquitetura | apple-study-checklist |
| [run-id](#run-id) | processo | design-pipeline |
| [Signal Board](#signal-board) | design | design-pipeline |
| [style-dictionary](#style-dictionary) | design | design-pipeline |
| [Token Atlas](#token-atlas) | design | design-pipeline |
| [vault](#vault) | produto | apple-study-checklist / FrankMD |
| [workspace root](#workspace-root) | infra | docs |

---

## `adaptive thinking`
**Categoria:** ai
**Contexto:** design-pipeline, Claude API
Modo de raciocínio do modelo `claude-opus-4-6` onde o modelo decide
dinamicamente quanto raciocínio interno usar antes de responder, em vez de
usar um budget de thinking fixo. Ativado com `{"type": "adaptive"}`.

---

## `bootstrap mínimo`
**Categoria:** processo
**Contexto:** docs
Pasta local de cada provedor (`.codex/`, `.claude_code/`, `.gemini/`) que
contém apenas ponteiros para o conteúdo canônico no hub. Não duplica
informação — apenas inicializa o contexto do provedor na primeira leitura.

---

## `bus factor`
**Categoria:** processo
**Contexto:** análise de repositórios (ownership-map)
Número mínimo de pessoas cujo afastamento tornaria um projeto inoperável.
Bus factor 1 significa que uma única pessoa controla todo o conhecimento
crítico.

---

## `Change Tree`
**Categoria:** processo
**Contexto:** docs, SESSION_CLOSE_TEMPLATE
Árvore de diretórios mínima incluída nos relatórios de sessão para localizar
rapidamente quais arquivos foram criados ou modificados. Não é um `git tree`
completo — só lista o que mudou.

---

## `codesign`
**Categoria:** infra
**Contexto:** apple-study-checklist, build Apple
Processo de assinatura digital de apps e binários Apple. Necessário para
rodar em dispositivos físicos e distribuir na App Store. Controlado pelo
Xcode e pelo `codesign` CLI.

---

## `DerivedData`
**Categoria:** infra
**Contexto:** apple-study-checklist, Xcode
Diretório temporário onde o Xcode armazena artefatos de build intermediários
(índices, objetos compilados, bundles). Pode ser movido para `/tmp` para
evitar conflitos com iCloud Drive.

---

## `filesystem-first`
**Categoria:** arquitetura
**Contexto:** FrankMD, apple-study-checklist
Arquitetura onde arquivos reais no disco são a fonte de verdade, não um banco
de dados ou API. Edições acontecem diretamente no filesystem; o app reflete
o estado dos arquivos.

---

## `HITL`
**Categoria:** processo
**Contexto:** design-pipeline
**Human-in-the-Loop** — ponto de controle manual entre etapas de um pipeline
automatizado. O pipeline pausa, exibe o output gerado e aguarda uma decisão
humana (aprovar / editar / refazer / encerrar) antes de continuar. Em modo
CI, o HITL é substituído por validators automáticos.

---

## `local-first`
**Categoria:** arquitetura
**Contexto:** apple-study-checklist, FrankMD
Arquitetura cujo fluxo principal funciona sem depender de serviços externos.
O dado vive no dispositivo ou no filesystem local; sync remoto é opcional e
não bloqueia o uso offline.

---

## `MCP`
**Categoria:** ai
**Contexto:** pi-local-app, docs
**Model Context Protocol** — protocolo JSON-RPC que permite que modelos de
linguagem interajam com ferramentas e dados externos por meio de uma
interface padronizada de tools, resources e prompts.

---

## `native shell`
**Categoria:** arquitetura
**Contexto:** apple-study-checklist
Camada de interface nativa por plataforma (SwiftUI para iOS/macOS, Compose
para Android etc.) construída sobre o mesmo modelo de domínio compartilhado.
Contrasta com embutir um web app como runtime.

---

## `run-id`
**Categoria:** processo
**Contexto:** design-pipeline
Identificador de uma execução do pipeline, gerado como timestamp
(`YYYYMMDD-HHMM` por default). Usado como nome da pasta de outputs para que
múltiplos runs coexistam sem sobrescrever resultados anteriores.

---

## `Signal Board`
**Categoria:** design
**Contexto:** design-pipeline, Token Atlas
Meta-tema visual do Token Atlas — identidade própria do relatório, separada
dos 4 sistemas documentados. Estética de quadro de referência cartográfico:
fundo `#0c0d0e`, grid de papel quadriculado, faixas coloridas de 3px por
tema, tipografia Inter + JetBrains Mono.

---

## `style-dictionary`
**Categoria:** design
**Contexto:** design-pipeline (step 4)
Formato JSON padrão para tokens de design portáveis entre plataformas,
mantido pela Amazon. Estrutura aninhada onde cada token tem `value` e
opcionalmente `type`, `description` e `attributes`.

---

## `Token Atlas`
**Categoria:** design
**Contexto:** design-pipeline (step 5)
Relatório HTML visual auto-contido gerado pelo step 5 do pipeline. Apresenta
os tokens extraídos dos 4 sistemas de design em 7 seções interativas
(Overview, Color, Typography, Spacing, Radius, Motion, Components) com
estética Signal Board.

---

## `vault`
**Categoria:** produto
**Contexto:** apple-study-checklist, FrankMD
Pasta de arquivos Markdown usada como fonte de verdade para o conteúdo do
app. Pode ser bundled (somente leitura, embutida no app), local editável
(cópia em Application Support) ou externa (pasta escolhida pelo usuário via
file picker).

---

## `workspace root`
**Categoria:** infra
**Contexto:** docs
Diretório base compartilhado por todos os repositórios e configs ativas.
Migrado de `~/Library/Mobile Documents/com~apple~CloudDocs/code` para
`~/code` em 27/03/2026 para eliminar conflitos com o iCloud Drive.

---

*Última atualização: 2026-03-28 — Sessão 4*
*Adicionar novos termos ao final da seção alfabética correspondente e atualizar o índice.*
