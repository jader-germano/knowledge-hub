# Portfolio GitLab Migration Inventory

Atualizado em `2026-04-13`.

Documento operacional da Onda 0 para transformar a migração estrutural do
portfólio para `GitLab` em execução local controlada.

## Objetivo

- inventariar o estado local real dos repositórios do portfólio
- registrar alvo recomendado de `GitLab` por repositório
- explicitar bloqueios antes de qualquer troca de upstream
- definir ordem de execução com menor risco arquitetural e operacional

## Premissas Explícitas

1. o repositório documental canônico desta trilha é
   `/Users/philipegermano/code/jpglabs/docs`
2. nenhuma worktree suja deve sofrer troca de upstream, `pull` cego ou
   sincronização contínua de migração
3. o namespace alvo recomendado é `gitlab.com/jader-germano/*`, porque:
   - o repositório `docs` já opera com `origin + gitlab`
   - `jpglabs-saas` já foi aberto nesse namespace
4. se o namespace definitivo divergir de `jader-germano`, a migração deve ser
   replanejada antes de alterar os repositórios locais
5. `portfolio-v2` não deve voltar a ser tratado como runtime final do
   portfólio

## Decisão Executiva

- migrar na Onda 0:
  - `portfolio-backend`
  - `jpglabs-portfolio`
  - `portfolio-mobile`
- manter fora do corte principal:
  - `portfolio-v2` como referência visual/funcional
  - `jpglabs-dashboard` como superfície local-first de coordenação, fora do
    caminho crítico do release do portfólio

## Inventário Local

| Repo | Papel atual | Path local | Branch atual | Remotes atuais | Estado local | GitLab target | Status GitLab | Decisão |
|---|---|---|---|---|---|---|---|
| `portfolio-backend` | backend/BFF canônico do portfólio | `/Users/philipegermano/code/jpglabs/portfolio-backend` | `develop` | `origin = git@github.com:jader-germano/jpglabs-portfolio-backend.git`<br>`gitlab = git@gitlab.com:jader-germano/portfolio-backend.git` | `dirty` | `git@gitlab.com:jader-germano/portfolio-backend.git` | provisionado + `main` default/protected + `develop` protected | migrar primeiro |
| `jpglabs-portfolio` | candidato forte para frontend público | `/Users/philipegermano/code/jpglabs/jpglabs-portfolio` | `main` | `origin = git@github.com:jader-germano/jpglabs-portfolio.git`<br>`gitlab = git@gitlab.com:jader-germano/jpglabs-portfolio.git` | `dirty` | `git@gitlab.com:jader-germano/jpglabs-portfolio.git` | provisionado + `main` default/protected | migrar depois do backend |
| `portfolio-mobile` | cliente mobile do portfólio | `/Users/philipegermano/code/jpglabs/portfolio-mobile` | `main` | `origin = git@github.com:jader-germano/jpglabs-portifolio-mobile.git`<br>`gitlab = git@gitlab.com:jader-germano/portfolio-mobile.git` | `dirty` | `git@gitlab.com:jader-germano/portfolio-mobile.git` | provisionado + `main` default/protected | migrar com correção de naming |
| `portfolio-v2` | referência visual/funcional, não runtime final | `/Users/philipegermano/code/jpglabs/portfolio-v2` | `feature/gitlab-cicd-pipeline` | `origin = git@github.com:jader-germano/portfolio-v2.git` | `dirty` | `n/a nesta onda` | não provisionar nesta onda | congelar como referência |
| `jpglabs-dashboard` | cockpit local-first de coordenação | `/Users/philipegermano/code/jpglabs/jpglabs-dashboard` | `main` | `sem remote configurado` | `dirty` | `n/a nesta onda` | fora da Onda 0 | reavaliar depois |

## Bloqueios Reais Observados

### Provisionamento e proteção já concluídos

- os repositórios `portfolio-backend`, `jpglabs-portfolio` e
  `portfolio-mobile` já foram criados no namespace `jader-germano` no GitLab
- o `remote` secundário `gitlab` já foi adicionado localmente nesses três
  repositórios
- os branches canônicos já foram publicados no GitLab:
  - `portfolio-backend`: `main` e `develop`
  - `jpglabs-portfolio`: `main`
  - `portfolio-mobile`: `main`
- as branches canônicas no GitLab já estão protegidas e alinhadas com o
  default esperado:
  - `portfolio-backend`: `main` = default/protected; `develop` = protected
  - `jpglabs-portfolio`: `main` = default/protected
  - `portfolio-mobile`: `main` = default/protected
- o próximo bloqueio real deixou de ser provisionamento e passou a ser:
  limpeza/isolation das worktrees antes de troca de upstream e sincronização
  contínua

### `portfolio-backend`

- worktree suja com alterações rastreadas e arquivos novos
- o repo ainda carrega naming legado no `origin`
- é a superfície que define contrato de backend/BFF; qualquer erro aqui
  propaga para web e mobile

### `jpglabs-portfolio`

- worktree suja com mudanças locais de app/documentação
- o `remote` `gitlab` já existe e o branch `main` já está default/protected no
  GitLab
- depende de fechamento prévio da fronteira do `portfolio-backend`

### `portfolio-mobile`

- worktree suja
- o `origin` atual tem typo legado em `portifolio`
- a correção de naming deve acontecer junto da migração para evitar novo drift

### `portfolio-v2`

- worktree suja
- o repo está explicitamente classificado como referência, não runtime final
- mover este repo como se fosse lane principal reabriria ambiguidade

### `jpglabs-dashboard`

- worktree suja e sem `remote`
- o projeto é útil para coordenação operacional, mas não é dependência direta
  da migração estrutural do portfólio
- não deve competir com o split front/back nem com o release do portfólio

## Ordem Recomendada De Execução

1. `portfolio-backend`
   - motivo: é o boundary canônico do backend/BFF e precisa estabilizar
     naming, ownership e destino antes das superfícies consumidoras
2. `jpglabs-portfolio`
   - motivo: representa a lane provável do frontend público e depende da
     clareza do backend
3. `portfolio-mobile`
   - motivo: cliente fino; deve migrar já apontando para naming e contratos
     estáveis
4. `portfolio-v2`
   - motivo: manter somente como referência até existir decisão explícita de
     arquivamento ou absorção
5. `jpglabs-dashboard`
   - motivo: revisar só depois que o caminho crítico do portfólio estiver fora
     de risco

## Checklist Local Antes De Trocar Upstream

- [ ] confirmar se a worktree do repo está limpa ou isolada por branch/commit
- [ ] confirmar se o branch atual é o branch canônico que deve subir no
      `GitLab`
- [x] confirmar se o projeto já existe no namespace alvo do `GitLab`
- [ ] confirmar se o nome final do repositório elimina naming legado
- [x] registrar ownership e objetivo do repo no hub antes do corte
- [x] adicionar `remote` `gitlab` somente depois das verificações acima
- [x] validar `remote -v` após o corte
- [x] publicar o branch canônico inicial no GitLab
- [x] proteger os branches canônicos no GitLab
- [ ] só então trocar upstream local quando a worktree estiver limpa e a
      estratégia de sync estiver aprovada

## Sequência Operacional Recomendada

```bash
# 1. inspeção obrigatória
git -C <repo> status --short
git -C <repo> remote -v

# 2. sync só quando a worktree estiver limpa
git -C <repo> pull --ff-only

# 3. corte local de remote após confirmar repo existente no GitLab
git -C <repo> remote add gitlab git@gitlab.com:jader-germano/<repo>.git

# 4. validação local
git -C <repo> remote -v

# 5. publicação inicial quando o repo remoto existir e o branch canônico estiver aprovado
git -C <repo> push gitlab <branch>:<branch>

# 6. alinhamento de default/protection no GitLab
glab repo update jader-germano/<repo> --defaultBranch <default-branch>
glab api projects/<project-id>/protected_branches -X POST -f name=<branch>
```

## Riscos E Trade-offs

- cortar `remote` em worktree suja reduz rastreabilidade e aumenta risco de
  merge sobre base errada
- manter `portfolio-backend` para depois economiza esforço imediato, mas
  prolonga a ambiguidade central do portfólio
- migrar `portfolio-v2` nesta onda simplificaria a lista de repositórios, mas
  reintroduziria a leitura errada de que ele ainda é runtime válido
- deixar `portfolio-mobile` com o naming legado no `origin` diminui atrito de
  curto prazo, mas cristaliza um erro de nomenclatura no destino novo

## Recomendação Direta

1. não trocar upstream nem iniciar sincronização contínua de nenhum repo do
   portfólio enquanto as worktrees permanecerem sujas
2. tratar `portfolio-backend` como primeiro repositório a limpar e migrar
3. usar `jpglabs-portfolio` como frontend público alvo e `portfolio-mobile`
   como cliente dependente
4. considerar provisionamento GitLab e proteção de branch como concluídos na
   Onda 0, deixando o risco remanescente concentrado em limpeza de worktree e
   cutover de upstream
5. manter `portfolio-v2` fora da Onda 0 e registrar isso explicitamente na
   governança

## Referências

- [`APPLICATION_STRUCTURE_MIGRATION_PLAN.md`](/Users/philipegermano/code/jpglabs/docs/projects/jpglabs/APPLICATION_STRUCTURE_MIGRATION_PLAN.md)
- [`ROADMAP.md`](/Users/philipegermano/code/jpglabs/docs/projects/jpglabs/ROADMAP.md)
- [`projects/portfolio-backend/PROJECT_CONTEXT.md`](/Users/philipegermano/code/jpglabs/docs/projects/portfolio-backend/PROJECT_CONTEXT.md)
- [`projects/portfolio-mobile/PROJECT_CONTEXT.md`](/Users/philipegermano/code/jpglabs/docs/projects/portfolio-mobile/PROJECT_CONTEXT.md)
- [`projects/jpglabs-dashboard/PROJECT_CONTEXT.md`](/Users/philipegermano/code/jpglabs/docs/projects/jpglabs-dashboard/PROJECT_CONTEXT.md)
