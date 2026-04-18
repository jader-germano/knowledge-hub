# JPGLabs Roadmap

Atualizado em `16/04/2026`. Reestruturado com novo escopo em 3 lanes após auditoria de gaps em 2026-04-16.

## Escopo

Este documento consolida o roadmap geral do ciclo atual da JPG Labs.

**Reestruturação 2026-04-16**: O roadmap anterior operava com 4 trilhas paralelas (A-D) sem critérios de saída verificáveis, sem DRI explícito por entregável e com 11 dos 18 sistemas do workspace sem roadmap. O novo escopo consolida em 3 lanes sequenciais com critérios de saída objetivos.

Foco imediato aprovado:

- **Lane 1** (P0, 4 semanas): resolver ambiguidade de backend/BFF vs. frontend, canonicalizar contratos, decidir papel do portfolio-mobile, definir contrato do operator shell
- **Lane 2** (P0, 2-3 semanas, paralela com Lane 1): migrar governança de execução para Jira+Confluence, eliminar duplicação de discovery entre agentes
- **Lane 3** (P0/P1, 6-8 semanas, depende da Lane 1): alinhar design system e navegação entre web, mobile, desktop e operator shells

Superfícies de execução:

- `Jira`: tasks, prioridade e status
- `Confluence`: roadmap narrativo, especificações e decisões
- `Notion`: diário apenas
- `ROADMAP.md` local: mirror de trabalho do workspace

## North Star Do Ciclo

Ao fim deste ciclo, a JPG Labs deve ter:

- um `portfolio-backend` assumido explicitamente como backend/BFF
- uma trilha clara para o frontend visual do portfólio, separada do backend
- superfícies ativas do portfólio e da operação com UI/UX coerente entre web,
  mobile e shell interno, sem drift de navegação e hierarquia
- backlog e roadmap operando em `Jira + Confluence`, sem regressão para board
  de task no `Notion`

## Barra Técnica Transversal

Todas as trilhas deste ciclo devem perseguir a mesma barra técnica:

- `100%` de cobertura de testes como meta padrão
- evolução por desacoplamento, layering, SOLID, clean architecture e TDD
- nenhuma entrega considerada pronta apenas com validação manual
- gaps de cobertura precisam ficar explícitos no handoff e no próximo corte

## Trilhas Paralelas

### Trilha A — Governança De Execução (`P0`, paralela)

Objetivo:

- parar de tratar `Notion` como task board
- consolidar `Jira + Confluence` como superfícies de execução

Entregáveis:

- contrato de LLMs atualizado
- mirrors locais de roadmap alinhados aos sistemas reais
- política explícita para reduzir duplicação de discovery entre agentes

Critério de saída:

- qualquer nova task ou roadmap passa a nascer em `Jira + Confluence`
- `Notion` fica restrito ao diário

### Trilha B — Split Arquitetural Do Portfólio (`P0`, paralela)

Objetivo:

- separar o portfólio público da camada backend/BFF antes de novo deploy

Entregáveis:

- backend/BFF com contratos explícitos e sem ambiguidade de frontend primário
- decisão formal sobre a nova lane do frontend visual
- fronteiras claras de auth, sessão, upload, APIs e persistência
- inventário operacional de migração para `GitLab` com status repo a repo,
  alvo recomendado e bloqueios locais explícitos em
  [`PORTFOLIO_GITLAB_MIGRATION_INVENTORY.md`](/Users/philipegermano/code/jpglabs/docs/projects/jpglabs/PORTFOLIO_GITLAB_MIGRATION_INVENTORY.md)
- plano de execução de banco com `schema` por aplicativo documentado em
  [`APPLICATION_DATA_BOUNDARY_EXECUTION_PLAN.md`](/Users/philipegermano/code/jpglabs/docs/projects/jpglabs/APPLICATION_DATA_BOUNDARY_EXECUTION_PLAN.md)
- template fixo de contrato e checklist arquitetural prontos para a fase
  pós-migração:
  [`PLANNED_PROJECT_CONTRACT_TEMPLATE.md`](/Users/philipegermano/code/jpglabs/docs/projects/jpglabs/PLANNED_PROJECT_CONTRACT_TEMPLATE.md)
  e
  [`PLANNED_PROJECT_ARCHITECTURE_CHECKLIST.md`](/Users/philipegermano/code/jpglabs/docs/projects/jpglabs/PLANNED_PROJECT_ARCHITECTURE_CHECKLIST.md)

Dependência:

- nenhuma das demais trilhas depende de começar por aqui, mas o release do
  portfólio depende do fechamento desta trilha

Critério de saída:

- o backend deixa de competir com o frontend visual
- existe uma topologia clara de deploy e ownership por camada

### Trilha C — Redesign UI/UX Das Superfícies Ativas (`P0`, paralela)

Objetivo:

- alinhar as superfícies ativas do portfólio e da operação em torno de padrões
  atuais de UI/UX, sem reabrir dependências legadas fora do escopo

Sistemas-alvo:

- `jpglabs-portfolio`
- `portfolio-mobile`
- `knowledge-hub-app`
- `jpglabs-dashboard`

Entregáveis:

- linguagem visual e estrutural coerente entre as superfícies
- redução de drift entre web, desktop e mobile
- separação mais nítida entre shell de operador, superfícies autenticadas e
  portfólio público

Critério de saída:

- existe uma direção única de navegação, estados e hierarquia visual
- clientes finos deixam de carregar decisões conflitantes de produto

### Trilha D — Release Do Portfólio (`P1`, dependente da Trilha B)

Objetivo:

- subir o portfólio com as últimas atualizações depois que a separação
  front/back estiver clara

Entregáveis:

- build validado do backend/BFF
- frontend visual apontando para contratos corretos
- observabilidade, health checks e checklist de release mínimos

Critério de saída:

- deploy atualizado do portfólio em ambiente alvo
- sem ambiguidade de runtime entre superfície pública e superfície autenticada

## Novo Escopo — 3 Lanes (2026-04-16)

### Lane 1 — Architecture Clarity (P0 · 4 semanas)

**Objetivo**: encerrar a ambiguidade de backend/BFF vs. frontend e canonicalizar contratos antes de qualquer novo deploy.

Escopo:
- Auditar `portfolio-backend`: marcar em código o que é backend/BFF e o que é frontend-visual
- Documentar contrato canônico: endpoints, auth boundary, storage contracts (versionado)
- Decidir o papel do `portfolio-mobile`: companion autenticado, operator shell ou cliente público
Critérios de saída:
- `portfolio-backend` tem seções marcadas de backend vs. frontend em código
- Contrato canônico da API documentado e versionado no Confluence
- Decisão do papel do `portfolio-mobile` formalizada no Jira ([SCRUM-29](https://jpglabs.atlassian.net/browse/SCRUM-29))

> **Nota 17/04/2026**: `knowledge-hub-app`, `pibar-macos` e `piphone-ios` foram **arquivados**. O épico SCRUM-30 (Operator Shell Contract) foi cancelado. Lane 3 e as referências a operator shells Pi foram removidas do escopo.

### Lane 2 — Execution Governance (P0 · 2-3 semanas · paralela com Lane 1)

**Objetivo**: migrar autoridade de task/roadmap para Jira+Confluence e eliminar duplicação de discovery entre agentes.

Escopo:
- Formalizar épicos no Jira para split front/back e redesign de superfícies
- Espelhar todas as decisões de roadmap no Confluence (decisioning record)
- Definir política explícita de discovery de agentes: onde cada tipo de asset vive, sem re-indexação por agente
- Criar roadmap para `jpglabs-dashboard` (atualmente sem roadmap, mas alvo do redesign de Trilha C)
- Restringir Notion ao diário — nenhuma task nova nasce fora do Jira

Critérios de saída:
- Todas as tasks novas e tasks ativas migradas para o Jira
- Sem duplicação ativa entre sistemas
- Mirrors de roadmap existem no Confluence para os 7 sistemas com roadmap
- Roadmap de `jpglabs-dashboard` criado com escopo mínimo e DRI

### Lane 3 — Surface Coherence (P0/P1 · 6-8 semanas · depende da Lane 1)

> **Escopo revisado em 17/04/2026**: `knowledge-hub-app`, `pibar-macos` e `piphone-ios` foram **arquivados**. Os sistemas-alvo da Lane 3 foram reduzidos.

**Objetivo**: alinhar design system e navegação entre as superfícies ativas.

Sistemas-alvo (após arquivamento):
- `jpglabs-portfolio` (público)
- `portfolio-mobile` (cliente fino)
- `jpglabs-dashboard` (operator — requer roadmap da Lane 2)

Critérios de saída:
- Um artefato de design system compartilhado (Figma) referenciado pelos 3 sistemas
- Paths de navegação e state machines documentados e testados
- `jpglabs-dashboard` alinhado visualmente ao portfolio público
- Sem drift de hierarquia visual entre web e mobile

## Critérios de Saída do Ciclo

**Tier 1 — Obrigatório**:
- `portfolio-backend` tem separação backend/BFF de frontend-visual marcada em código
- Contrato canônico da API documentado e versionado
- Jira+Confluence são as superfícies de execução; Notion é diário apenas

**Tier 2 — Deve ter**:
- Papel do `portfolio-mobile` decidido e comunicado ([SCRUM-29](https://jpglabs.atlassian.net/browse/SCRUM-29))
- Design system baseline em uso pelos 3 sistemas ativos (`jpglabs-portfolio`, `portfolio-mobile`, `jpglabs-dashboard`)
- `jpglabs-dashboard` com roadmap e alinhamento visual ao portfolio

**Tier 3 — Desejável**:
- Portfolio release publicado com nova arquitetura
- Migração GitLab iniciada com inventory completo

> **17/04/2026**: `knowledge-hub-app`, `pibar-macos` e `piphone-ios` arquivados. SCRUM-30 (Operator Shell Contract) cancelado. Referências a esses sistemas removidas dos critérios de saída.

## Sequenciamento Recomendado

1. Iniciar Lane 1 e Lane 2 em paralelo imediatamente.
2. Lane 1 desbloqueia Lane 3 — não abrir surface coherence antes da clarity de contratos.
3. Lane 2 não depende de Lane 1, mas deve fechar antes do final de Lane 1.
4. Lane 3 começa com design system baseline enquanto Lane 1 ainda finaliza hardening.
5. Release do portfolio só após conclusão de Lane 1 Tier 1.

## Contextos E Roadmaps Por Sistema

- [`portfolio-backend/ROADMAP.md`](/Users/philipegermano/code/jpglabs/docs/projects/portfolio-backend/ROADMAP.md)
- [`portfolio-mobile/ROADMAP.md`](/Users/philipegermano/code/jpglabs/docs/projects/portfolio-mobile/ROADMAP.md)
- [`knowledge-hub-app/ROADMAP.md`](/Users/philipegermano/code/jpglabs/docs/projects/knowledge-hub-app/ROADMAP.md)
- `jpglabs-portfolio`
  - ainda não há roadmap específico no hub; usar
    [`PORTFOLIO_GITLAB_MIGRATION_INVENTORY.md`](/Users/philipegermano/code/jpglabs/docs/projects/jpglabs/PORTFOLIO_GITLAB_MIGRATION_INVENTORY.md)
    como referência canônica desta fase

## Fora Do Foco Imediato

- `jpglabs-saas` continua como trilha comercial importante, mas não é a lane
  técnica prioritária deste ciclo
- `imap-server` e `FrankMD` seguem como capacidades úteis, mas não devem
  disputar prioridade com o split do portfólio nem com a reorganização das
  superfícies ativas

## Próximas Ações

1. Formalizar em `Jira` os épicos do split front/back e do redesign das
   superfícies ativas.
2. Espelhar em `Confluence` a decisão de fronteira entre backend/BFF, frontend
   público e superfícies de operador.
3. Consolidar o isolamento operacional da Onda 0, mantendo
   `portfolio-backend` em `wip/resume-parse-contract`, `jpglabs-portfolio`
   limpo em `main` e `portfolio-mobile` em
   `chore/node-pin-and-async-storage`, sem abrir MR nesta rodada.
4. Auditar o `portfolio-backend` para separar o que permanece como backend do
   que deve sair para a lane visual.
