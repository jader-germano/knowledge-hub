# jpglabs-dashboard Roadmap

Criado em `17/04/2026`.

## Papel No Ecossistema

`jpglabs-dashboard` é a superfície de coordenação operacional do JPGLabs: trilhas de desenvolvimento, infra, MCP, estado do workspace e ações pre-prompt de squad. É parte do **operator shell** — o conjunto de superfícies autenticadas usadas por Jader para operar o ecossistema.

Não é portfólio público. Não substitui Jira ou Confluence. É o painel de controle interno.

## Estado Atual

- Stack: Next.js (Create Next App bootstrap) + React 19 + TypeScript + Tailwind CSS
- Local-first: roadmap em `src/data/roadmap.ts`, sem dependência de backend novo
- Um único commit inicial (`2026-04-03 890c749`)
- Dashboard já expõe narrativa operacional básica (status de MCP, roadmap, handoff)
- Figma integration pendente
- Sem alinhamento visual formal com os demais operator shells (`pibar-macos`, `piphone-ios`, `knowledge-hub-app`)

## Dependências

- **Lane 1** do roadmap JPGLabs (Architecture Clarity): contrato do operator shell precisa ser definido antes de alinhar navegação e estado
- **Figma**: trilha oficial via plugin/app — sem servidor Docker MCP adicional
- `knowledge-hub-app`, `pibar-macos`, `piphone-ios`: design system compartilhado nasce na Lane 3

## Trilhas

### Trilha 1 — Clareza De Escopo E Dados (`P0`) ✅ FECHADA `17/04/2026`

Objetivo: eliminar dados estáticos e indefinição sobre o que o dashboard deve mostrar.

Entregáveis:
- [x] Decisão formal: v1 opera local-first com dados estáticos em `src/data/`
- [x] Separação documentada: `src/data/*.ts` estático para v1; Jira API + MCP filesystem na Trilha 3
- [x] Seções obrigatórias v1 definidas: trilhas ativas, estado MCP, infra/plataforma, próximas ações
- [ ] Seções aprovadas pelo DRI (aguardando confirmação)

Contrato: [`DATA_CONTRACT_V1.md`](./DATA_CONTRACT_V1.md)

Critério de saída:
- [x] Existe um contrato de dados explícito para a v1
- [ ] As seções da v1 estão aprovadas pelo DRI

### Trilha 2 — Alinhamento Visual Com O Portfolio (`P0`, depende de Lane 3 do roadmap JPGLabs)

> **17/04/2026**: `knowledge-hub-app`, `pibar-macos` e `piphone-ios` **arquivados**. Trilha reorientada para alinhar o dashboard com as superfícies ativas restantes.

Objetivo: alinhar hierarquia visual e navegação com as superfícies ativas do portfólio.

Sistemas de referência:
- `jpglabs-portfolio` (público)
- `portfolio-mobile` (cliente fino)

Entregáveis:
- Aplicar design system baseline compartilhado (quando disponível na Lane 3)
- Alinhar navegação, estados e hierarquia visual com portfolio e portfolio-mobile
- Eliminar drift entre a paleta do dashboard e as demais superfícies ativas

Critério de saída:
- Hierarquia visual e terminologia do dashboard são consistentes com `jpglabs-portfolio` e `portfolio-mobile`
- Não há decisão visual conflitante entre as superfícies ativas

### Trilha 3 — Fontes De Dados Dinâmicas (`P1`, depende de Trilha 1)

Objetivo: substituir dados estáticos por fontes reais.

Candidatos:
- Jira API (épicos e status de tasks)
- Confluence API (specs e decisões)
- MCP servers ativos (estado real do gateway)
- `mcp-agent-bridge` (sessões e eventos cross-provider)

Entregáveis:
- Pelo menos uma fonte dinâmica integrada (Jira ou `mcp-agent-bridge`)
- Dashboard reflete estado real sem edição manual de `src/data/roadmap.ts`

Critério de saída:
- O estado do workspace visível no dashboard não requer atualização manual

### Trilha 4 — Figma E Design System (`P1`, paralela com Trilha 2)

Objetivo: ter um arquivo Figma com o layout do dashboard antes de implementar redesign.

Trilha oficial:
- Usar plugin/app Figma disponível no ambiente
- Não adicionar servidor Docker MCP específico para Figma neste ciclo

Entregáveis:
- Frame ou arquivo Figma com layout da v1 do dashboard
- Componentes reutilizáveis alinhados ao operator shell

Critério de saída:
- Existe um handoff Figma validado antes de iniciar Trilha 2

## Fora De Escopo

- Backend próprio dedicado ao dashboard (dados vêm de APIs externas ou MCP)
- Versão pública ou autenticação de terceiros
- Substituir Jira/Confluence como fonte de verdade de tasks e specs

## Próximas Ações

1. ~~Fechar Trilha 1~~ ✅ `DATA_CONTRACT_V1.md` entregue — aguardando aprovação do DRI
2. Abrir frame Figma com layout inicial antes de qualquer redesign (Trilha 4)
3. Aguardar Lane 1 do roadmap JPGLabs para definir contrato do operator shell (pré-requisito da Trilha 2)
4. Registrar épico no Jira: `jpglabs-dashboard v1 — clareza de escopo e dados` — **bloqueado**: Jira `jpglabs.atlassian.net` sem autorização no MCP atual
