# PIE Platform Migration Plan

Atualizado em `2026-04-04`.

Documento complementar obrigatório para a trilha de persistência:

- [`PIE_DB_SCHEMA_EXECUTION_PLAN.md`](/Users/philipegermano/code/jpglabs/docs/projects/jpglabs/PIE_DB_SCHEMA_EXECUTION_PLAN.md)

## Status

- documento de planejamento
- `portfolio-v2` já foi clonado localmente em
  `/Users/philipegermano/code/jpglabs/portfolio-v2`
- `jader-germano/jpglabs-portfolio` foi identificado na origem GitHub como
  candidato React/Vite sem `Next.js`
- achado crítico da Sprint 0: o repositório `portfolio-v2` atual ainda é
  `Next.js`, não um frontend React puro
- consequência: `portfolio-v2` deve ser tratado, por enquanto, como fonte de
  referência visual/funcional ou como base a ser convertida, não como runtime
  final aceitável
- consequência adicional: `jpglabs-portfolio` deve ser auditado como base
  preferencial do frontend público definitivo `jpglabs-portfolio`

## Decisões Canônicas

1. `Next.js` está rejeitado como stack-alvo para o portfólio e o dashboard.
2. `NestJS` passa a ser o backend canônico do portfólio e do dashboard.
3. Frontend e backend devem ser repositórios e runtimes separados, sem novo
   monólito `Next.js`.
4. O repositório `portfolio-v2` continua sendo fonte de referência obrigatória,
   mas não pode ser promovido como frontend final enquanto permanecer em
   `Next.js`.
5. O repositório `jader-germano/jpglabs-portfolio` passa a ser o melhor
   candidato conhecido para base React pura do frontend público.
6. Haverá um único frontend do portfólio em React em `:8083`, mantendo o nome
   `jpglabs-portfolio`.
7. O dashboard ficará em React em `:8085`, separado do portfólio.
8. A API NestJS deve ser a fonte única de verdade para auth, contratos,
   persistência, uploads, RBAC e integrações.
9. A separação de banco na primeira onda será por schema por aplicativo dentro
   de `1` banco físico canônico, evitando tanto o monólito lógico quanto a
   proliferação precoce de múltiplos bancos.
10. O alvo inicial mais defensável é `1` Postgres/Supabase canônico, operado
    exclusivamente pelo `pie-api`, com schemas por app, migrations, RLS e
    auditoria sob controle do backend.
11. Frontends não podem acessar Supabase/Postgres diretamente no estado final;
    qualquer leitura ou escrita de dado de negócio deve entrar via `pie-api`.
12. Não usar mocks nas lanes de integração final.
13. Portfólios genéricos, versões paralelas e lanes redundantes entram como
    fonte de migração temporária e devem ser removidos depois do cutover do
    frontend único.
14. Todo prefixo `pi-*` deve migrar para `pie-*`, com compatibilidade temporária
    quando o rename tocar contratos externos ou variáveis de ambiente. Essa
    regra não força rename do frontend público `jpglabs-portfolio`.
15. Antes de qualquer nova rodada de alteração de código em um repo Git, o
    check-up obrigatório deve:
    - ler `git status --short`
    - executar `git pull --ff-only` quando a worktree estiver limpa e houver
      upstream configurado
    - executar a suíte unitária padrão do repo logo após o sync
    - corrigir ou isolar explicitamente qualquer teste já quebrado antes de
      iniciar novas alterações
    - declarar bloqueio explicitamente quando a worktree estiver suja ou sem
      upstream, em vez de editar em cima de base possivelmente desatualizada
16. Até o fechamento da migração estrutural para `GitLab`, a trilha de
    portfólio fica restrita a:
    - migração de repositórios, remotes, namespace e estrutura
    - saneamento documental, governança e contratos de operação
    - zero alteração de código de produto nas superfícies de portfólio
17. Depois do fechamento da migração estrutural, a próxima ação obrigatória é
    definir templates fixos de contrato para criação de novos projetos e a
    arquitetura mínima obrigatória antes de qualquer implementação planejada.
18. Scripts não planejados, automações curtas e MVPs curtos não entram na lane
    planejada de `GitLab`; eles devem seguir por uma lane separada em `GitHub`.
19. A trilha de validação que usará código do `TSE` deve ser tratada como
    séria desde a origem: governança, auditabilidade, segurança e rigor de
    contrato acima de velocidade de iteração.

## Escopo Imediato

### Onda 0 — freeze estrutural obrigatório agora

- migrar a estrutura do portfólio para `GitLab`
- alinhar naming, remotes, ownership e topologia de repositórios
- fechar o contrato da nova estrutura antes de qualquer alteração de código
- manter as superfícies de portfólio em modo `no-code-change` até concluir essa
  migração estrutural

### Onda 1 — somente após a migração estrutural

- extrair o backend hoje embutido em `portfolio-backend`
- remover o papel de frontend primário do `portfolio-backend`
- consolidar o frontend único do portfólio em `jpglabs-portfolio`, sem
  `Next.js`, usando `portfolio-v2` como referência complementar de migração
- recriar o dashboard fora de `Next.js` como React puro
- sanitizar as funcionalidades espalhadas por múltiplos portfólios para um
  único frontend e um único backend
- formalizar a política de nomenclatura `pie-*`

### Onda 2 — saneamento do restante do workspace

- inventariar e migrar outras superfícies `Next.js` fora do corte imediato
- hoje o workspace já contém pelo menos:
  - `jpglabs-portfolio`
  - `knowledge-hub-app`
  - `portfolio-backend`
  - `jpglabs-dashboard`
  - `portfolio-v2`

## Estado Atual Resumido

### Monólito legado

- `portfolio-backend` é uma base `Next.js` que mistura:
  - páginas públicas do portfólio
  - autenticação via `next-auth`
  - APIs em `app/api`
  - dashboard autenticado
  - contratos de operador e integrações com `pi-local-app`

### Persistência legada

- há forte evidência de acoplamento atual a `Supabase/Postgres` no
  `portfolio-backend` e no `portfolio-v2`
- esse acoplamento hoje vaza detalhes de persistência para superfícies que não
  deveriam ser donas do banco no estado final
- a separação pedida pelo usuário exige mover a posse do acesso a dados para o
  `pie-api`, com fronteira explícita de contratos e schemas separados por
  aplicativo

### Dashboard legado

- `jpglabs-dashboard` é um app `Next.js` separado, mas ainda não segue a
  direção final pedida pelo usuário

### `portfolio-v2` clonado

- branch atual: `main`
- remote: `git@github.com:jader-germano/portfolio-v2.git`
- evidências de `Next.js` no clone:
  - `package.json` com scripts `next dev`, `next build`, `next start`
  - dependência `next: 14.2.35`
  - presença de `app/`
  - uso de `next-auth`
  - `README.md` padrão de `create-next-app`

### React puro já identificado na origem

- repositório: `jader-germano/jpglabs-portfolio`
- evidências verificadas:
  - `package.json` com scripts `vite`, `vite build` e `vite preview`
  - dependências `react`, `react-dom` e `react-router-dom`
  - `@vitejs/plugin-react`
  - `vite.config.ts`
  - ausência de `next.config.*`

### Runtime separado já existente

- `pi-local-app` já é um serviço Node.js separado e deve ser tratado como
  referência de separação backend/runtime
- `PieCenter` já materializa a nomenclatura `PIE` no ecossistema Apple

## Arquitetura Alvo

```text
pie-api                  NestJS API/BFF canônico                   :4000
jpglabs-data             Postgres/Supabase canônico                :5432 logical
jpglabs-portfolio        React frontend público                    :8083
pie-dashboard-react      React dashboard autenticado               :8085
pie-local-app            runtime operacional / memória / serviços  :3131
```

## Baseline De Capacidade Local

Auditoria local em `2026-04-04`:

- host: `Apple M4`
- CPU: `10` cores
- RAM física: `16 GB`
- Docker Desktop disponível para a VM Linux: `~8.2 GB`
- disco livre útil no momento da auditoria: `~32 GB`
- cluster `k3d` atual com consumo baixo, compatível com a stack leve do ciclo

Conclusão prática:

- este Mac suporta a topologia local da Sprint 0 e da fase inicial de
  implementação, desde que o escopo permaneça em:
  - `1` backend `NestJS`
  - `1` banco canônico leve (`Postgres/Supabase`)
  - `1` frontend público React
  - `1` dashboard React
  - `k3d/k3s` apenas para integração
  - serviços auxiliares leves
- este Mac não é alvo confortável para a mesma rodada quando somados:
  - LLM local pesada
  - observabilidade pesada
  - múltiplos bancos grandes
  - builds paralelos agressivos e tudo containerizado o tempo inteiro

Arranjo local recomendado:

- frontends no host:
  - portfólio React `:8083`
  - dashboard React `:8085`
- backend `NestJS` e auxiliares em Docker/k3d
- usar `k3d` para validação de integração, não como modo obrigatório de hot
  reload de todos os apps

Gates operacionais:

- elevar Docker Desktop para `10–12 GB` quando a fase de integração crescer
- buscar pelo menos `60 GB` livres em disco antes da fase pesada da migração
- não somar LLM local pesada nesta mesma estação durante a rodada principal

## Fronteiras De Responsabilidade

### `pie-api` (NestJS)

- autenticação
- emissão e rotação de tokens
- refresh flow
- RBAC/guards
- contratos OpenAPI
- DTOs e validação
- uploads, inbox, portfolio content, operator hub, dashboard runtime proxy
- integrações com `pie-local-app`
- observabilidade, health e auditoria
- ownership exclusivo do acesso ao banco, migrations e policies

### `jpglabs-data`

- Postgres/Supabase canônico da plataforma nesta primeira onda
- schemas próprios por aplicativo, por exemplo:
  - `pie_portfolio`
  - `pie_dashboard`
  - `pie_operator`
  - `pie_runtime`
  - `pie_audit`
- preservar e respeitar schemas gerenciados do Supabase quando existirem, como
  `auth` e `storage`, sem misturar dado de negócio neles
- RLS, roles técnicas, service-role controlada e migrations versionadas
- nenhum segredo de banco exposto para frontends

### `jpglabs-portfolio`

- superfície pública do portfólio
- login e request-access de usuário final
- consumo apenas via SDK/contrato gerado da API
- nenhuma lógica de persistência fora da API
- usa `jpglabs-portfolio` como base preferencial
- usa `portfolio-v2` como material complementar de migração, não como runtime
  final

### Portfólios Legados E Genéricos

- `portfolio-v2`, frontend embutido no `portfolio-backend` e outras variações
  paralelas entram apenas como fonte de descoberta, migração e rollback
  temporário
- depois do cutover validado do `jpglabs-portfolio`, essas lanes viram
  candidatas formais a remoção

### `pie-dashboard-react`

- dashboard autenticado
- instances, guardian, infra, MCP status, actions, provider sync
- sem versão Angular nesta fase
- consome a mesma API NestJS e os mesmos contratos canônicos

## Modelo De Auth, Contratos E Persistência

## Recomendação Direta

- usar `NestJS` com `JWT access token` de curta duração
- usar `refresh token` com rotação, entregue por cookie `HttpOnly`, `Secure`
  e `SameSite` adequado ao ambiente
- manter o access token apenas em memória no frontend
- evitar `localStorage` para tokens sensíveis
- expor `OpenAPI` como contrato canônico
- gerar SDKs tipados para `jpglabs-portfolio` e dashboard a partir do
  `OpenAPI`

## Recomendação Direta Para O Banco

- manter `Postgres/Supabase` como banco canônico da primeira onda
- centralizar acesso a dados no `pie-api` via módulos, services e repositórios
- separar o dado por schema de aplicativo, não por tabela solta num schema
  único
- isolar `service_role` apenas no backend
- aplicar `RLS` para superfícies sensíveis quando o acesso vier do contexto de
  usuário autenticado
- manter migrations versionadas e rollback scriptado por release
- evitar criar múltiplos bancos físicos antes de medir volume, isolamento e
  custo operacional reais

## Trade-off

- `JWT + refresh cookie` é mais seguro que guardar tudo em storage do browser
- contratos gerados a partir do backend reduzem drift entre o portfólio, o
  dashboard e qualquer consumidor web futuro
- o custo é maior disciplina de versionamento de contratos, mas esse custo é
  aceitável e desejável neste contexto
- um banco canônico com schemas por aplicativo é mais simples de operar e
  validar no Mac local do que abrir múltiplos bancos agora
- o trade-off é que o isolamento de blast radius será mais lógico do que
  físico na primeira onda; isso é aceitável para o tamanho atual do sistema

## Contrato Canônico De Integração

1. Backend define DTO, schema e OpenAPI.
2. Frontends consomem SDK gerado ou package `@pie/contracts`.
3. Nenhum frontend escreve chamadas HTTP ad-hoc sem contrato versionado.
4. Toda mudança breaking exige:
   - versão de contrato
   - changelog
   - plano de rollback

## Plano De Separação Do Banco

### Premissa

- a meta imediata é sair do banco monolítico lógico atual para `1` banco
  físico com separação de schema por aplicativo
- isso remove o acoplamento do banco ao frontend e ao legado `Next.js` sem
  introduzir custo prematuro de múltiplos bancos

### Fase 1 — Descoberta E Ownership

- inventariar tabelas, buckets, roles, policies e secrets hoje usados por
  `portfolio-backend` e `portfolio-v2`
- classificar cada recurso no schema-alvo do aplicativo correspondente
- declarar owner de cada schema no `pie-api`

### Fase 2 — Modelo Canônico

- consolidar schemas por aplicativo no banco canônico
- mapear o corte inicial recomendado:
  - `pie_portfolio` para conteúdo público, currículo e assets de portfólio
  - `pie_dashboard` para preferências e estados internos do dashboard
  - `pie_operator` para acesso operacional, filas e decisões internas
  - `pie_runtime` para integrações e snapshots operacionais persistidos
  - `pie_audit` para trilhas de auditoria e eventos sensíveis
- definir convenções de migrations, seeds, rollback e ambientes
- mover validação de schema para DTO + validation pipe + contract test no
  backend
- impedir novo acesso direto do frontend a tabelas e buckets

### Fase 3 — Migração Controlada

- migrar leitura e escrita endpoint por endpoint
- adotar estratégia preferencial de `expand -> migrate -> contract`
- manter compatibilidade temporária apenas enquanto houver rollback claro
- medir divergência entre legado e `pie-api` antes de desligar caminhos antigos

### Fase 4 — Cutover E Selo De Implementação

- desligar credenciais de banco no frontend
- bloquear novos writes fora do `pie-api`
- validar smoke real de login, leitura, escrita, upload e dashboard sem mock
- fechar evidência de rollback testado e observabilidade limpa

## Selo De Implementação Da Separação Do Banco

- nenhum frontend usa chave de banco para dado de negócio
- `pie-api` é o único writer oficial
- cada aplicativo tem schema próprio e owner explícito
- migrations e rollback do release estão versionados
- auth, RBAC e policies foram revalidados após o cutover
- logs, métricas e auditoria conseguem rastrear a origem das mutações
- não existe endpoint legado crítico dependente de acesso direto ao banco fora
  do plano de compatibilidade temporária

## Política De Nomenclatura

### Regra

- qualquer repo, app, package, image, doc ou serviço `pi-*` deve migrar para
  `pie-*`

### Rename em ondas

1. docs, ADRs, roadmap, nomes de produto e package names
2. Docker images, manifests e service names
3. env vars e chaves de integração
4. DNS/domínios externos, apenas quando houver aprovação explícita

### Compatibilidade Temporária

- durante a transição, aceitar `PI_*` e `PIE_*` em paralelo quando a troca
  imediata quebrar automações ou clientes já em operação
- a remoção dos aliases só acontece depois de observabilidade limpa

## Matriz De Migração Por Superfície

| Superfície atual | Destino | Observação |
| --- | --- | --- |
| `app/page.tsx` e páginas públicas do `portfolio-backend` | `jpglabs-portfolio` | frontend sai do backend |
| `app/login/page.tsx` | `jpglabs-portfolio` | auth UX separada, backend continua dono do fluxo |
| `app/dashboard/*` do `portfolio-backend` | `pie-dashboard-react` | dashboard sai do monólito |
| `app/api/*` do `portfolio-backend` | `pie-api` NestJS | contrato canônico |
| `next-auth` | auth NestJS | substituir por auth própria do backend |
| `jpglabs-dashboard` Next | `pie-dashboard-react` | reimplementação em React |
| `jpglabs-portfolio` | base React preferencial | Vite + React puro, sem Next |
| `portfolio-v2` atual | referência/migração | não usar como produto final enquanto estiver em Next |
| `knowledge-hub-app` Next | onda posterior | fora do corte imediato do portfólio |

## Inventário Funcional Inicial

### Portfólio público

- navegação
- hero
- skills
- experiências
- projetos
- snippets / prova técnica
- CTA
- termos
- privacidade
- login / request access
- upload de currículo, se continuar público ou autenticado

### Dashboard

- instances
- guardian
- infra health
- provider sync
- MCP status
- action cards
- learning / trilhas / marketing, se permanecerem no escopo real do dashboard

### Backend

- auth
- portfolio content
- inbox
- resume parse
- operator hub
- dashboard runtime
- mobile/operator decisions
- ownership do acesso ao banco

## User Stories Por Épico

### Épico 1 — Arquitetura Canônica E Freeze De Next.js

- como owner, quero congelar novo desenvolvimento em `Next.js`, para evitar
  expandir uma direção rejeitada
- como arquiteto, quero formalizar `NestJS + React` como stack alvo do
  portfólio e React separado para o dashboard, para reduzir ambiguidade
- como time, quero um inventário explícito de apps `Next.js` no workspace, para
  planejar a migração completa

### Épico 2 — Contratos E Auth Do `pie-api`

- como frontend React, quero consumir contratos gerados da API, para não manter
  chamadas HTTP soltas
- como dashboard React, quero consumir os mesmos contratos tipados, para
  evitar drift com o frontend público
- como operador, quero autenticação segura com refresh controlado, para evitar
  sessão frágil ou insegura

### Épico 3 — Separação De Persistência E Banco

- como arquiteto, quero um banco canônico com schema por aplicativo operado
  pelo `pie-api`, para remover acoplamento de persistência do frontend e do
  legado `Next.js`
- como time, quero migrations, rollback e ownership de schema explícitos por
  aplicativo, para reduzir risco de drift e regressão operacional
- como operador, quero trilha de cutover observável e reversível, para não
  quebrar login, uploads e dashboard em produção

### Épico 4 — React Público Sem `Next.js`

- como visitante, quero acessar o portfólio React em `:8083`, para navegar sem
  depender do backend monolítico legado
- como time, quero partir de uma base React/Vite já existente quando ela for
  aderente, para reduzir retrabalho e acelerar a migração
- como time, quero migrar o valor funcional/visual de `portfolio-v2` para uma
  implementação React pura, para não carregar `Next.js` para o estado final

### Épico 5 — Dashboard React

- como operador, quero um dashboard React separado em `:8085`, para não manter
  o dashboard preso ao `Next.js`
- como operador, quero o dashboard consumindo API real e runtime real, para
  evitar mocks e inconsistência operacional

### Épico 6 — Rename `pi-*` Para `pie-*`

- como time, quero renomear gradualmente os artefatos `pi-*`, para alinhar a
  plataforma ao branding `PIE`
- como SRE, quero preservar compatibilidade temporária onde houver risco de
  quebra operacional, para evitar regressão desnecessária

### Épico 7 — Descomissionamento Do Legado

- como owner, quero transformar o `portfolio-backend` legado em fonte de
  migração e não em produto final, para encerrar a ambiguidade
- como time, quero desativar o frontend embutido no backend apenas depois de
  cutover validado, para manter rollback claro

## Sprints Recomendadas

### Sprint 0 — Descoberta, Freeze e Provenance

- registrar ADR: `NestJS`, `jpglabs-portfolio` como base React preferencial,
  `portfolio-v2` como fonte complementar de migração e React dashboard
- clonar e auditar `portfolio-v2`
- auditar `jpglabs-portfolio` como candidato principal do frontend React
- formalizar o achado de que o clone atual ainda está em `Next.js`
- auditar funcionalidades do `portfolio-backend` e do `jpglabs-dashboard`
- mapear os componentes atuais do portfólio e do dashboard
- mapear quais portfólios genéricos serão descomissionados após o cutover
- inventariar todo `Next.js` restante no workspace
- definir rollback de cada lane antes de qualquer escrita

### Sprint 1 — Fundação Do `pie-api`

- scaffold do `NestJS`
- módulos de auth, portfolio, dashboard, operator e integration
- OpenAPI inicial
- strategy de JWT + refresh token
- inventário inicial do schema legado e surface de `Supabase/Postgres`
- policy inicial de ownership do banco pelo backend
- desenho inicial dos schemas por aplicativo
- executar o bootstrap descrito em
  [`PIE_DB_SCHEMA_EXECUTION_PLAN.md`](/Users/philipegermano/code/jpglabs/docs/projects/jpglabs/PIE_DB_SCHEMA_EXECUTION_PLAN.md)
- testes unitários e contract tests

### Sprint 2 — Extração De Contratos E Corte Do Monólito

- mover endpoints do `portfolio-backend` para o `pie-api`
- criar SDK gerado para frontends
- isolar conteúdo e dados de portfólio no backend novo
- iniciar a trilha `expand -> migrate -> contract` no banco
- marcar explicitamente o que será removido do monólito legado

### Sprint 3 — React Público Em `:8083`

- partir de `jpglabs-portfolio` quando a auditoria confirmar aderência
- usar `portfolio-v2` como referência/migração, não como runtime final
- integrar com `pie-api`
- migrar páginas públicas e login
- remover credenciais e acessos diretos a banco do frontend público
- remover dependências do frontend antigo em `portfolio-backend`

### Sprint 4 — Dashboard React Em `:8085`

- reconstruir `instances`, `guardian`, `infra`, `mcp-status`, `actions`
- integrar auth e runtime real
- remover credenciais e acessos diretos a banco do dashboard
- garantir que o dashboard não dependa mais de `Next.js`

### Sprint 5 — Rename E Cutover

- aplicar rename `pi-*` para `pie-*`
- manter aliases transitórios onde necessário
- ajustar Docker/Kubernetes/Vercel
- executar smoke real sem mock
- validar o selo de separação do banco e cortar caminhos legados restantes
- descomissionar as lanes `Next.js` aprovadas para corte
- remover portfólios genéricos e versões redundantes após o frontend único
  assumir produção

## Team Plan Para `/teams`

### Objetivo

Planejar e depois executar a migração do portfólio/dashboard do legado
`Next.js` para uma arquitetura separada em `NestJS + React`, com
rename `pi-* -> pie-*`, contratos canônicos e integração sem mock.

### Teammates E Responsabilidades

- `lead`
  - dono do plano, gates, priorização e aprovação humana
  - revisa todos os diffs finais
  - decide corte e rollback
- `researcher`
  - inventário funcional e técnico do legado
  - localiza o escopo real de `portfolio-v2`
  - audita `jpglabs-portfolio` como base React preferencial
  - mapeia rename blast radius de `pi-* -> pie-*`
- `implementer-api`
  - define `pie-api` NestJS
  - auth, OpenAPI, DTOs, contracts e testes
- `implementer-web`
  - lidera `jpglabs-portfolio`
  - lidera `pie-dashboard-react`
  - consome SDK gerado
- `reviewer`
  - contract review, testes, rollback, coverage e security gates
- `doc-owner`
  - atualiza `FrankMD/notes`, handoff, ADR e mirrors locais

### Dependências E Conflitos De Arquivo

- nenhum teammate deve editar simultaneamente o mesmo contrato OpenAPI/DTO
- `implementer-api` é dono exclusivo da superfície de contrato
- `implementer-web` só consome contrato aprovado
- `doc-owner` não bloqueia implementação, mas fecha a rodada obrigatoriamente

### Quality Gates

1. nenhum teammate edita arquivos antes de aprovação do plano
2. toda história com escrita deve declarar teste e rollback
3. auth e contratos só entram via `pie-api`
4. integração final sem mock
5. `100%` de cobertura como meta por slice alterado
6. sem `Co-Authored-By`; autoria humana e disclosure em handoff/PR/ADR
7. antes de qualquer edição em repo Git, rodar o preflight:
   - `git status --short`
   - `git pull --ff-only` se a worktree estiver limpa
   - rodar testes unitários do repo
   - corrigir falha pré-existente ou declarar bloqueio antes de nova alteração
   - bloqueio explícito se houver sujeira ou ausência de upstream

## Prompt Recomendado Para O Lead

```text
Create an agent team for this workspace.
Goal: migrate the portfolio and dashboard away from Next.js into a separated architecture with a single NestJS API, a single React portfolio frontend named jpglabs-portfolio, a React dashboard, and staged pi-* -> pie-* renaming where applicable.
Use five teammates: researcher, implementer-api, implementer-web, reviewer, doc-owner.
Require plan approval before any teammate edits files.
Reject plans without explicit test, rollback, contract-versioning, repo pull preflight and no-mock integration steps.
Reserve doc-owner to update FrankMD/notes plus workspace handoff surfaces before closure.
Keep human authorship on commits and record AI assistance outside Co-Authored-By.
```

## Fora De Escopo Desta Rodada

- criar o scaffold NestJS
- reimplementar React ou dashboard
- renomear repositórios ou pacotes
- executar deploys locais, Vercel ou Kubernetes

## Próximo Passo Recomendado

Abrir a Sprint 0 em `/teams`, com aprovação humana explícita do plano antes de
qualquer scaffold, rename ou refactor.
