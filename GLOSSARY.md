---
type: glossary
title: Glossário do Workspace
tags:
  - "#glossary"
  - "#wiki"
aliases:
  - glossario
  - glossário
  - termos
last_updated: "2026-04-08"
---

# Glossário — Workspace Docs

Fonte canônica de termos técnicos e conceituais usados nos projetos, sessões e
documentação do hub. Todo novo termo introduzido em qualquer sessão deve ser
registrado aqui.

**Linkagem:** Use `[[GLOSSARY#termo]]` ou `[[termo]]` para linkar de outros documentos.

**Formato de entrada:**
```
## termo
aliases: [variante1, variante2]
**Categoria:** infra / design / ai / produto / arquitetura / processo
**Contexto:** em qual projeto ou domínio o termo aparece
Definição clara em uma ou duas frases.
```

---

## Índice rápido

### Ferramentas

| Termo | Contexto |
|---|---|
| [[GLOSSARY#MCP\|MCP]] | pi-local-app, docs |
| [[GLOSSARY#style-dictionary\|style-dictionary]] | design-pipeline |

### Conceitos

| Termo | Categoria | Projeto |
|---|---|---|
| [[GLOSSARY#adaptive thinking\|adaptive thinking]] | ai | design-pipeline |
| [[GLOSSARY#bootstrap mínimo\|bootstrap mínimo]] | processo | docs |
| [[GLOSSARY#bus factor\|bus factor]] | processo | — |
| [[GLOSSARY#filesystem-first\|filesystem-first]] | arquitetura | FrankMD / apple-study-checklist |
| [[GLOSSARY#HITL\|HITL]] | processo | design-pipeline |
| [[GLOSSARY#local-first\|local-first]] | arquitetura | apple-study-checklist / FrankMD |
| [[GLOSSARY#LLM Wiki\|LLM Wiki]] | ai | docs |
| [[GLOSSARY#native shell\|native shell]] | arquitetura | apple-study-checklist |
| [[GLOSSARY#run-id\|run-id]] | processo | design-pipeline |

### Projetos

| Termo | Link |
|---|---|
| [[GLOSSARY#Signal Board\|Signal Board]] | design-pipeline |
| [[GLOSSARY#Token Atlas\|Token Atlas]] | design-pipeline |
| [[GLOSSARY#vault\|vault]] | apple-study-checklist / FrankMD |

### Infraestrutura

| Termo | Contexto |
|---|---|
| [[GLOSSARY#Change Tree\|Change Tree]] | docs, SESSION_CLOSE_TEMPLATE |
| [[GLOSSARY#codesign\|codesign]] | apple-study-checklist |
| [[GLOSSARY#DerivedData\|DerivedData]] | Xcode |
| [[GLOSSARY#workspace root\|workspace root]] | docs |

---

## adaptive thinking

**Aliases:** adaptive-thinking, extended thinking  
**Categoria:** ai  
**Contexto:** design-pipeline, Claude API  
Modo de raciocínio do modelo `claude-opus-4-6` onde o modelo decide
dinamicamente quanto raciocínio interno usar antes de responder, em vez de
usar um budget de thinking fixo. Ativado com `{"type": "adaptive"}`.

---

## bootstrap mínimo

**Aliases:** bootstrap-minimo  
**Categoria:** processo  
**Contexto:** docs  
Pasta local de cada provedor (`.codex/`, `.claude_code/`, `.gemini/`) que
contém apenas ponteiros para o conteúdo canônico no hub. Não duplica
informação — apenas inicializa o contexto do provedor na primeira leitura.

---

## bus factor

**Categoria:** processo  
**Contexto:** análise de repositórios (ownership-map)  
Número mínimo de pessoas cujo afastamento tornaria um projeto inoperável.
Bus factor 1 significa que uma única pessoa controla todo o conhecimento
crítico.

---

## Change Tree

**Aliases:** change-tree  
**Categoria:** processo  
**Contexto:** docs, SESSION_CLOSE_TEMPLATE  
Árvore de diretórios mínima incluída nos relatórios de sessão para localizar
rapidamente quais arquivos foram criados ou modificados. Não é um `git tree`
completo — só lista o que mudou.

---

## codesign

**Categoria:** infra  
**Contexto:** apple-study-checklist, build Apple  
Processo de assinatura digital de apps e binários Apple. Necessário para
rodar em dispositivos físicos e distribuir na App Store. Controlado pelo
Xcode e pelo `codesign` CLI.

---

## DerivedData

**Aliases:** derived-data  
**Categoria:** infra  
**Contexto:** apple-study-checklist, Xcode  
Diretório temporário onde o Xcode armazena artefatos de build intermediários
(índices, objetos compilados, bundles). Pode ser movido para `/tmp` para
evitar conflitos com iCloud Drive.

---

## filesystem-first

**Aliases:** filesystem first  
**Categoria:** arquitetura  
**Contexto:** FrankMD, apple-study-checklist  
Arquitetura onde arquivos reais no disco são a fonte de verdade, não um banco
de dados ou API. Edições acontecem diretamente no filesystem; o app reflete
o estado dos arquivos.

Ver também: [[GLOSSARY#local-first|local-first]]

---

## HITL

**Aliases:** human-in-the-loop, human in the loop  
**Categoria:** processo  
**Contexto:** design-pipeline  
**Human-in-the-Loop** — ponto de controle manual entre etapas de um pipeline
automatizado. O pipeline pausa, exibe o output gerado e aguarda uma decisão
humana (aprovar / editar / refazer / encerrar) antes de continuar. Em modo
CI, o HITL é substituído por validators automáticos.

---

## LLM Wiki

**Aliases:** llm-wiki, karpathy-wiki  
**Categoria:** ai  
**Contexto:** docs, memory/wiki/  
Padrão de knowledge base para LLMs proposto por Andrej Karpathy: 3 camadas
(`raw/` imutável → `wiki/` compilado → `schema` operacional). Mapeado ao
workspace em [[research/adr/ADR-001-llm-wiki-architecture]].

Ver wiki completa: [[memory/wiki/llm-wiki-pattern]]

---

## local-first

**Aliases:** local first  
**Categoria:** arquitetura  
**Contexto:** apple-study-checklist, FrankMD  
Arquitetura cujo fluxo principal funciona sem depender de serviços externos.
O dado vive no dispositivo ou no filesystem local; sync remoto é opcional e
não bloqueia o uso offline.

Ver também: [[GLOSSARY#filesystem-first|filesystem-first]]

---

## MCP

**Aliases:** model context protocol  
**Categoria:** ai  
**Contexto:** pi-local-app, docs  
**Model Context Protocol** — protocolo JSON-RPC que permite que modelos de
linguagem interajam com ferramentas e dados externos por meio de uma
interface padronizada de tools, resources e prompts.

Ver: [[MCP_SETUP]]

---

## native shell

**Aliases:** native-shell  
**Categoria:** arquitetura  
**Contexto:** apple-study-checklist  
Camada de interface nativa por plataforma (SwiftUI para iOS/macOS, Compose
para Android etc.) construída sobre o mesmo modelo de domínio compartilhado.
Contrasta com embutir um web app como runtime.

---

## run-id

**Aliases:** run id  
**Categoria:** processo  
**Contexto:** design-pipeline  
Identificador de uma execução do pipeline, gerado como timestamp
(`YYYYMMDD-HHMM` por default). Usado como nome da pasta de outputs para que
múltiplos runs coexistam sem sobrescrever resultados anteriores.

---

## Signal Board

**Aliases:** signal-board  
**Categoria:** design  
**Contexto:** design-pipeline, Token Atlas  
Meta-tema visual do [[GLOSSARY#Token Atlas|Token Atlas]] — identidade própria do relatório, separada
dos 4 sistemas documentados. Estética de quadro de referência cartográfico:
fundo `#0c0d0e`, grid de papel quadriculado, faixas coloridas de 3px por
tema, tipografia Inter + JetBrains Mono.

---

## style-dictionary

**Aliases:** style dictionary  
**Categoria:** design  
**Contexto:** design-pipeline (step 4)  
Formato JSON padrão para tokens de design portáveis entre plataformas,
mantido pela Amazon. Estrutura aninhada onde cada token tem `value` e
opcionalmente `type`, `description` e `attributes`.

---

## Token Atlas

**Aliases:** token-atlas  
**Categoria:** design  
**Contexto:** design-pipeline (step 5)  
Relatório HTML visual auto-contido gerado pelo step 5 do pipeline. Apresenta
os tokens extraídos dos 4 sistemas de design em 7 seções interativas
(Overview, Color, Typography, Spacing, Radius, Motion, Components) com
estética [[GLOSSARY#Signal Board|Signal Board]].

---

## vault

**Categoria:** produto  
**Contexto:** apple-study-checklist, FrankMD, Obsidian  
(1) Pasta de arquivos Markdown usada como fonte de verdade para o conteúdo do
app. Pode ser bundled, local editável ou externa.
(2) No contexto Obsidian: pasta raiz gerenciada pelo app, equivalente ao
`jpglabs/docs/` neste workspace.

---

## workspace root

**Aliases:** workspace-root, ~/code  
**Categoria:** infra  
**Contexto:** docs  
Diretório base compartilhado por todos os repositórios e configs ativas.
Migrado de `~/Library/Mobile Documents/com~apple~CloudDocs/code` para
`~/code` em 27/03/2026 para eliminar conflitos com o iCloud Drive.

---

*Última atualização: 2026-04-08 — Sessão Obsidian LLM Wiki*  
*Adicionar novos termos ao final da seção temática correspondente e atualizar o índice rápido.*

---

## Glossário Multilíngue — Referência de Sessões

> Termos técnicos recorrentes traduzidos em 4 idiomas.
> Atualizado automaticamente ao final de cada sessão Claude Code.

### Infraestrutura & DevOps

| Termo (pt-BR) | English | Français | Italiano | 日本語 (Nihongo) |
|---|---|---|---|---|
| Rede | Network | Réseau | Rete | ネットワーク (nettowāku) |
| Servidor | Server | Serveur | Server | サーバー (sābā) |
| Contêiner | Container | Conteneur | Contenitore | コンテナ (kontena) |
| Firewall | Firewall | Pare-feu | Firewall | ファイアウォール (faiawōru) |
| Sincronizar | Synchronize | Synchroniser | Sincronizzare | 同期する (dōki suru) |
| Chave | Key | Clé | Chiave | 鍵 (kagi) |
| Implantar | Deploy | Déployer | Distribuire | デプロイする (depuroi suru) |
| Atualizar | Update | Mettre à jour | Aggiornare | 更新する (kōshin suru) |
| Agendar | Schedule | Planifier | Programmare | スケジュールする (sukejūru suru) |
| Construir | Build | Construire | Costruire | ビルドする (birudo suru) |

### Programação & Arquitetura

| Termo (pt-BR) | English | Français | Italiano | 日本語 (Nihongo) |
|---|---|---|---|---|
| Código | Code | Code | Codice | コード (kōdo) |
| Banco de dados | Database | Base de données | Database | データベース (dētabēsu) |
| Memória | Memory | Mémoire | Memoria | メモリ (memori) / 記憶 (kioku) |
| Interface | Interface | Interface | Interfaccia | インターフェース (intāfēsu) |
| Fluxo | Flow / Pipeline | Flux / Pipeline | Flusso | フロー (furō) / 流れ (nagare) |

### Notas sobre cada idioma

**English (EN)**
Língua germânica com forte influência latina/francesa. Termos técnicos de TI são majoritariamente inglês nativo (build, deploy, code) por ser o berço da computação moderna. Ordem: SVO.

**Français (FR)**
Língua românica como o português. A *Académie Française* traduz ativamente termos de TI: firewall → *pare-feu*, software → *logiciel*, computer → *ordinateur*. É a língua que mais resiste ao anglicismo técnico.

**Italiano (IT)**
A mais conservadora das línguas românicas — próxima do latim vulgar. Regra das doppie (duplas): consoantes duplas mudam a pronúncia e o significado (*pala* = pá, *palla* = bola). Se lê como se escreve, similar ao português.

**日本語 / Japonês (JP)**
Usa 3 sistemas de escrita simultâneos:
- **カタカナ (Katakana):** silabário angular para palavras estrangeiras. A maioria dos termos de TI usa katakana: サーバー, コンテナ, デプロイ.
- **漢字 (Kanji):** ~2.000 caracteres chineses de uso diário. Cada um tem radicais com significado: 鍵 (kagi/chave) = 金 (metal) + 建 (construir).
- **ひらがな (Hiragana):** silabário cursivo para gramática e palavras nativas. する (suru = fazer) é hiragana.
- **Ordem SOV:** サーバーを同期する (sābā wo dōki suru) = servidor [obj] sincronizar — o verbo sempre vai no final.
- **Sem plural nem artigos:** サーバー pode ser o servidor, um servidor ou servidores — o contexto decide.

---

*Última atualização: 2026-04-09 — Sessão infra/sync Windows-VPS*
