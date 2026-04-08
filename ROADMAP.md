# Roadmap de Plataforma MCP e Agent Teams

## Contexto

Este roadmap consolida o material existente no workspace sobre:

- configuração MCP compartilhada entre ferramentas
- operação de `agent teams`
- revisão e qualidade de código
- integração futura com Figma para prototipagem e design systems

O escopo atual é de enablement de plataforma de engenharia. Não é um roadmap de
produto. O roadmap estratégico da JPG Labs agora vive em
`projects/jpglabs/ROADMAP.md`.

## Estado Atual

Hoje o workspace já possui:

- `agent teams` habilitado localmente
- um gateway MCP definido em `.mcp.json`
- um skill `/teams` com papéis e quality gates básicos
- baseline inicial de servidores voltados a engenharia
- clientes `claude-code`, `claude-desktop`, `codex` e `gemini` conectados ao gateway Docker global

Os bloqueios e inconsistências já identificados são:

- divergência entre documentação e configuração efetiva do gateway
- contrato de paths inconsistente entre servidores: `git` e `filesystem` aceitam paths absolutos do host, enquanto `ast-grep` exige caminho relativo ao workspace ou `/src/...`
- `semgrep` do catálogo Docker não entra na baseline funcional sem autenticação OAuth e hoje responde `Unauthorized`
- a validação operacional de uma execução real de `/teams` ainda não foi concluída

## Atualização Operacional

Validação base em `2026-03-31`:

- `docker version` validado com Docker Desktop `4.66.0` e Engine `29.3.0`
- `docker mcp server ls` retornou `22 enabled` no host atual
- `docker mcp client ls --global` confirmou `claude-code`, `claude-desktop`, `codex` e `gemini` conectados ao gateway Docker
- `docker mcp gateway run --dry-run` com a configuração do workspace validou `git`, `filesystem`, `desktop-commander`, `playwright`, `fetch`, `context7`, `memory`, `sequentialthinking` e `ast-grep`
- `semgrep` ficou fora da baseline funcional por falhar na inicialização com `Unauthorized`
- a trilha oficial de Figma neste ambiente passa pelo plugin/app já disponível, fora do catálogo Docker atual

Revalidação em `2026-04-02` no host, fora do sandbox do Codex:

- `docker mcp server ls` confirmou `22 enabled` no catálogo disponível neste host
- `docker mcp gateway run --dry-run` reconfirmou a baseline funcional do workspace com `git`, `filesystem`, `desktop-commander`, `playwright`, `fetch`, `context7`, `memory`, `sequentialthinking` e `ast-grep`
- o drift identificado não estava em `.mcp.json`; estava no próprio roadmap, que ainda insinuava `semgrep` como servidor declarado na baseline ativa
- chamadas Docker feitas dentro do sandbox do Codex podem retornar falso negativo do tipo `Docker Desktop is not running`; a validação canônica do host deve ser feita fora do sandbox quando houver esse sintoma

## Status Atual Por Fase

- Fase 1 `Infraestrutura Base`: em progresso
  - `docker mcp server ls` e `docker mcp client ls --global` já foram validados
  - a rodada de `2026-04-02` confirmou que a validação de host precisa ser feita fora do sandbox quando Docker retornar falso negativo
  - ainda falta fechar a reconciliação final entre a estrutura nova do workspace e o bootstrap real usado pelo gateway
- Fase 2 `Estabilização do Stack MCP`: em progresso
  - a baseline funcional em runtime hoje é `git`, `filesystem`, `desktop-commander`, `playwright`, `fetch`, `context7`, `memory`, `sequentialthinking` e `ast-grep`
  - `.mcp.json` não anuncia `semgrep`; o drift estava no mirror local do roadmap, não na configuração efetiva
- Fase 3 `Review e Qualidade de Código`: não iniciada
  - ainda não existe playbook compartilhado com checklist mínimo de review e métricas obrigatórias para merge
- Fase 4 `Operação de Agent Teams`: em progresso
  - o skill `/teams` existe, mas ainda não há execução controlada validada de ponta a ponta
- Fase 5 `Integração com Figma`: em progresso
  - a trilha oficial foi decidida, mas ainda falta validação em arquivo ou frame real
- Fase 6 `Governança e Documentação`: em progresso
  - o hub canônico foi consolidado em `/Users/philipegermano/code/jpglabs/docs`
  - ainda faltam limpeza final de referências legadas e verificação de manifests secundários

## Frentes Ativas

1. `lead` + `researcher`: finalizar a limpeza das referências legadas após a fusão do `ai-orchestration-hub` e absorção do antigo `jpglabs`.
2. `implementer` + `reviewer`: manter `.mcp.json` alinhado à baseline funcional real e publicar uma matriz curta de smoke tests por servidor.
3. `researcher` + `implementer`: validar um caso controlado de `/teams` e um caso real do fluxo oficial de Figma via plugin/app.

## Objetivo

Fechar um ambiente consistente de engenharia com:

- interoperabilidade real entre MCPs
- fluxo padronizado de revisão e conferência de código
- ferramentas mínimas de análise estrutural e qualidade
- operação previsível de agent teams
- trilha definida para Figma e design system

## Fase 1: Infraestrutura Base

Prioridade: P0

Entregáveis:

- validar `docker mcp server ls`
- validar `docker mcp tools ls`
- confirmar que o gateway sobe com a configuração atual
- reconciliar os paths usados pelo gateway com o workspace real

Critério de conclusão:

- servidores MCP sobem sem erro
- ferramentas MCP respondem no workspace alvo
- não há path ambíguo ou duplicado na configuração

## Fase 2: Estabilização do Stack MCP

Prioridade: P0

Baseline funcional atual:

- `git`
- `filesystem`
- `desktop-commander`
- `playwright`
- `fetch`
- `context7`
- `memory`
- `sequentialthinking`
- `ast-grep`

Stack opcional pós-credenciais:

- `semgrep`
- `sonarqube`
- `n8n`
- `resend`

Entregáveis:

- smoke tests por servidor
- validação cruzada entre leitura, busca estrutural, automação e análise
- inventário objetivo do que está ativo, do que está documentado e do que será removido

Critério de conclusão:

- baseline MCP validada em runtime
- documentação alinhada ao ambiente real

## Fase 3: Review e Qualidade de Código

Prioridade: P1

Entregáveis:

- fluxo padrão de revisão usando `git` + `ast-grep` + `sequentialthinking`,
  com `context7` como gate obrigatório de conferência documental antes de
  implementação e com `semgrep` autenticado quando disponível
- checklist mínimo de review técnico
- definição de métricas obrigatórias para merge
- decisão sobre adoção ou adiamento de métricas mais pesadas

Critério de conclusão:

- existe um fluxo repetível para revisão e conferência de código
- qualidade mínima deixa de depender de inspeção manual ad hoc

## Fase 4: Operação de Agent Teams

Prioridade: P1

Entregáveis:

- validar uma execução real do `/teams`
- formalizar o time-base `lead`, `researcher`, `implementer` e `reviewer`
- exigir plano aprovado antes de escrita, CI, deploy ou versionamento
- exigir testes e rollback em tarefas com alteração

Critério de conclusão:

- o fluxo com teammates funciona de ponta a ponta
- papéis, gates e cleanup ficam padronizados

## Fase 5: Integração com Figma

Prioridade: P1

Trilha oficial:

- usar o plugin/app de Figma já disponível no ambiente
- não adicionar servidor Docker MCP específico para Figma neste ciclo

Entregáveis:

- decisão de arquitetura para Figma
- definição de escopo mínimo para prototipagem e design system
- validação do fluxo escolhido com arquivo ou frame real

Critério de conclusão:

- existe uma única trilha oficial para Figma no workspace
- o tema deixa de ser uma dependência em aberto

## Fase 6: Governança e Documentação

Prioridade: P2

Entregáveis:

- atualizar relatórios e instruções para refletir a configuração real
- remover referências obsoletas ou não ativas
- deixar explícito o que é recurso nativo e o que é convenção local

Critério de conclusão:

- documentação e ambiente deixam de divergir
- onboarding e manutenção ficam previsíveis

## Dependências Críticas

- Docker Desktop ativo
- acesso estável ao catálogo MCP usado pelo gateway
- autenticação válida do plugin/app de Figma antes de validar leitura e escrita em arquivo real

## Próximos Passos Imediatos

1. Formalizar no playbook que validações Docker devem usar evidência fora do sandbox quando o runtime local acusar falso negativo.
2. Formalizar no playbook o contrato de path do `ast-grep` para evitar uso de paths absolutos do host no `dir`.
3. Rodar um primeiro teste controlado com `/teams` em uma sessão Claude.
4. Decidir se `semgrep` receberá OAuth para entrar na baseline funcional ou seguirá opcional.
5. Validar o fluxo oficial de Figma com um arquivo ou frame real via plugin/app.
