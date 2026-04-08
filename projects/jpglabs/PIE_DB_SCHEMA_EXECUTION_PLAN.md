# PIE DB Schema Execution Plan

Atualizado em `2026-04-04`.

## Objetivo

Materializar o próximo corte técnico da migração `PIE` para persistência:

- `1` banco físico `Postgres/Supabase`
- separação por `schema` de aplicativo
- ownership exclusivo do banco pelo `pie-api`
- nenhum frontend acessando banco diretamente

## Escopo Deste Corte

- definir a topologia inicial de schemas
- definir ownership por módulo do `pie-api`
- definir convenções de migration, rollback, roles e RLS
- definir backlog executável da Sprint 1
- explicitar `Risks And Gaps`

## Fora De Escopo

- criar migrations reais nesta sessão
- escolher e instalar todo o stack de acesso a dados
- migrar dados legados nesta sessão
- fechar o cutover de produção

## Decisão Canônica

### Direção aprovada

- manter `1` banco físico canônico
- separar o dado por `schema` de aplicativo
- impedir qualquer acesso direto do frontend a `Supabase/Postgres`
- concentrar DDL, DML, policies, roles técnicas e secrets no `pie-api`

### Direção rejeitada

- `public` monolítico com tabelas de todos os apps misturadas
- credenciais de banco expostas em frontend público ou dashboard
- múltiplos bancos físicos antes de necessidade objetiva de isolamento

## Recomendação Direta

- usar `NestJS` com uma camada de persistência SQL-first
- preferir migrations em SQL explícito e queries com schema qualificado
- manter o query layer fino e previsível; evitar ORM pesado com abstração demais
- tratar `auth` e `storage` do Supabase como schemas gerenciados, não como
  destino de dado de negócio arbitrário

## Topologia Inicial De Schemas

### `pie_access`

Owner no `pie-api`:
- `AccessModule`

Responsabilidade:
- identidade da aplicação
- sessão e refresh token
- RBAC e grants
- request access / approval flow

Tabelas iniciais recomendadas:
- `pie_access.users`
- `pie_access.refresh_sessions`
- `pie_access.roles`
- `pie_access.role_bindings`
- `pie_access.permission_grants`
- `pie_access.access_requests`

### `pie_portfolio`

Owner no `pie-api`:
- `PortfolioModule`

Responsabilidade:
- conteúdo público do portfólio
- currículo estruturado
- projetos, skills, experiência e snippets

Tabelas iniciais recomendadas:
- `pie_portfolio.profiles`
- `pie_portfolio.experiences`
- `pie_portfolio.skills`
- `pie_portfolio.projects`
- `pie_portfolio.snippets`
- `pie_portfolio.resume_assets`
- `pie_portfolio.contact_intakes`

### `pie_dashboard`

Owner no `pie-api`:
- `DashboardModule`

Responsabilidade:
- preferências persistidas do dashboard
- filtros, visões salvas e anotações operacionais
- estado que não é apenas derivado do runtime

Tabelas iniciais recomendadas:
- `pie_dashboard.preferences`
- `pie_dashboard.saved_views`
- `pie_dashboard.annotations`
- `pie_dashboard.action_overrides`

### `pie_operator`

Owner no `pie-api`:
- `OperatorModule`

Responsabilidade:
- filas e decisões internas
- workflows operacionais
- tasks e notas internas que não pertencem ao dashboard público do operador

Tabelas iniciais recomendadas:
- `pie_operator.action_queue`
- `pie_operator.decisions`
- `pie_operator.notes`
- `pie_operator.followups`

### `pie_runtime`

Owner no `pie-api`:
- `IntegrationModule` ou `RuntimeModule`

Responsabilidade:
- snapshots persistidos de integrações
- heartbeat e inventário técnico
- dados transitórios úteis ao dashboard e à auditoria

Tabelas iniciais recomendadas:
- `pie_runtime.instance_heartbeats`
- `pie_runtime.provider_sync_snapshots`
- `pie_runtime.mcp_server_registry`
- `pie_runtime.runtime_health_snapshots`

### `pie_audit`

Owner no `pie-api`:
- `AuditModule`

Responsabilidade:
- trilha de auditoria
- eventos sensíveis de segurança e mudança
- checkpoints de release e cutover

Tabelas iniciais recomendadas:
- `pie_audit.audit_events`
- `pie_audit.security_events`
- `pie_audit.release_checkpoints`
- `pie_audit.data_change_log`

## Schemas Gerenciados Externamente

- `auth`
  - usar apenas se o stack final mantiver parte da identidade delegada ao
    Supabase
  - não misturar tabela de negócio aqui
- `storage`
  - usar para objetos/binários quando necessário
  - metadado de negócio continua nos schemas `pie_*`
- `public`
  - não usar como destino padrão de novas tabelas de negócio

## Regras De Modelagem

1. Toda tabela nova de negócio entra em schema `pie_*` explícito.
2. Toda query do backend usa schema qualificado.
3. Cada módulo do `pie-api` tem owner explícito do schema primário.
4. Relacionamentos cross-schema devem ser poucos e intencionais.
5. Preferir referência estável por `UUID` e service composition a joins largos
   entre vários schemas.
6. Exceção aceitável:
   - referências para `pie_access.users`
   - referências para tabelas de auditoria quando houver obrigação de trilha

## Regras De Segurança

- frontend público e dashboard não recebem chave de banco
- `service_role` ou equivalente fica restrita ao backend
- RLS habilitada para superfícies sensíveis quando houver acesso sob contexto
  de usuário
- tabelas estritamente internas podem ficar sem RLS se forem acessadas somente
  por role técnica do backend, mas isso precisa de justificativa explícita
- secrets de banco e storage ficam fora do cliente

## Convenção De Migrations

### Recomendação

- migrations SQL-first, versionadas por release
- diretório organizado por schema
- rollback explícito por mudança crítica

### Estrutura sugerida

```text
pie-api/
└── database/
    ├── migrations/
    │   ├── pie_access/
    │   ├── pie_portfolio/
    │   ├── pie_dashboard/
    │   ├── pie_operator/
    │   ├── pie_runtime/
    │   └── pie_audit/
    ├── seeds/
    └── policies/
```

### Regra de naming

- `YYYYMMDDHHMM__schema__short_description.sql`

Exemplo:

- `202604041130__pie_access__create_users_and_refresh_sessions.sql`

## Estratégia De Cutover

### Padrão preferencial

- `expand -> migrate -> contract`

### Tradução prática

1. criar schema/tabela/policy nova
2. escrever via `pie-api` nos dois caminhos quando necessário
3. medir consistência
4. cortar leitura legada
5. cortar write legado
6. remover compatibilidade temporária

## Critérios De Aceite Do Corte

- schemas `pie_*` definidos e aprovados
- owner de cada schema definido no `pie-api`
- convenção de migration e rollback aprovada
- regra “frontend sem acesso direto ao banco” fixada como contrato
- `Risks And Gaps` explícitos antes de qualquer scaffold real

## Backlog Executável Da Sprint 1

### `P0`

- escolher o query layer final do `pie-api`
  - recomendação inicial: query layer leve com SQL explícito
- criar o scaffold de `database/` no `pie-api`
- criar roles técnicas mínimas:
  - `pie_api_rw`
  - `pie_api_ro`
  - `pie_migration`
- criar os schemas vazios:
  - `pie_access`
  - `pie_portfolio`
  - `pie_dashboard`
  - `pie_operator`
  - `pie_runtime`
  - `pie_audit`
- definir a primeira migration de bootstrap
- definir os primeiros contratos de `AccessModule` e `PortfolioModule`

### `P1`

- mapear as tabelas legadas do `portfolio-backend`
- mapear buckets e documentos que exigem persistência
- desenhar a migração de conteúdo público para `pie_portfolio`
- desenhar a migração de sessões e grants para `pie_access`

### `P2`

- definir retenção de snapshots em `pie_runtime`
- definir retenção e expurgo em `pie_audit`
- rever necessidade real de todas as tabelas persistidas do dashboard

## Risks And Gaps

### Riscos

- o legado ainda não foi completamente inventariado; podem existir tabelas,
  buckets ou dependências implícitas fora do mapeamento atual
- a convivência com schemas gerenciados do Supabase precisa de disciplina para
  evitar novo acoplamento acidental
- se o dashboard persistir estado demais, o schema `pie_dashboard` pode virar
  um novo pseudo-monólito
- cross-schema joins demais podem corroer o benefício da separação
- migração de auth é sensível; qualquer erro afeta login, sessão e approvals

### Gaps

- query layer final ainda não está fechado
- catálogo real de tabelas legadas ainda não está consolidado
- política final de RLS por tabela ainda não existe
- política de retenção de auditoria e runtime ainda não foi aprovada
- falta decidir se parte da identidade continuará usando recursos nativos do
  Supabase ou se tudo ficará 100% em `pie_access`

## Recomendação Final

O próximo corte técnico correto é este:

- abrir o `pie-api`
- materializar o bootstrap de `database/`
- criar os schemas `pie_*`
- subir a primeira migration de infraestrutura
- começar por `pie_access` e `pie_portfolio`

Isso dá a menor superfície útil com o melhor custo-benefício. Tentar migrar
dashboard, runtime e operator ao mesmo tempo aumenta risco sem benefício
proporcional nesta fase.
