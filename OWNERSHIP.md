# Ownership

## Nível 1: Hub Global

Ownership: `/Users/philipegermano/code/jpglabs/docs`

Escopo:

- regras compartilhadas
- índices humanos e manifests
- roadmap global
- handoff e rotina diária
- contexto por LLM

## Superfícies Externas Canônicas

Ownership operacional fora do workspace:

- `Jira`:
  - tasks
  - status
  - prioridades
  - roadmap de execução
- `Confluence`:
  - especificações
  - decisões
  - roadmap narrativo
  - espelho compartilhável de handoff
- `Notion`:
  - Diário de Bordo e journal operacional

Regra:

- `Notion` não deve ser usado como board de task ou roadmap
- `ROADMAP.md` local é mirror de trabalho; não substitui `Jira` como quadro
  canônico de execução

## Nível 2: Contexto Por Repositório

Ownership: `projects/<repo>/`

Escopo:

- contexto resumido do repositório
- snapshots de histórico Git
- contexto fino por provider para cada repo
- histórico de sessão classificado por repositório
- slices internos absorvidos pelo hub, como `projects/infrastructure/`

## Nível 3: Bootstrap E Runtime

Ownership: root e pastas locais de provider

Escopo:

- `.mcp.json`
- `WORKSPACE_BOOTSTRAP.md`
- `AGENTS.md`
- `.claude/settings.json`
- `.claude/skills/`
- arquivos de setup local necessários ao runtime

Regra:

- bootstrap aponta para o hub
- bootstrap não vira fonte canônica

## Nível 4: Repositórios Reais

Ownership:

- JPG Labs: `/Users/philipegermano/code/jpglabs/<repo>`
- externos ao grupo JPG Labs: `/Users/philipegermano/code/<repo>`

Escopo:

- código-fonte
- testes
- documentação de produto e arquitetura do próprio projeto

Observação:

- a antiga trilha `jpglabs` foi absorvida pelo repositório `docs`; contexto
  operacional e scripts compartilhados agora vivem no hub documental canônico

## Nível 5: Conteúdo Efêmero

Ownership: runtime local

Escopo:

- logs
- caches
- artefatos transitórios

Regra:

- nunca tratar conteúdo efêmero como fonte de verdade
