# portfolio-backend Roadmap

Atualizado em `02/04/2026`.

## Papel No Ecossistema

`portfolio-backend` deve ser tratado como a lane de backend/BFF do portfólio.
Ele não deve continuar competindo com o frontend visual como se fosse a
superfície pública primária.

## Leitura Atual

- a documentação do próprio repo já declara `backend/BFF lane`
- ainda existe ambiguidade histórica porque o repo nasceu como appNest.js
  completa
- o release do portfólio depende de encerrar essa ambiguidade

## Trilhas

### Trilha 1 — Split Front-End vs Back-End (`P0`)

- separar explicitamente o que é contrato de backend do que é UI pública
- manter auth, sessão, uploads, APIs protegidas e persistência neste repo
- mover ou planejar mover a apresentação pública para uma lane própria de
  frontend visual

### Trilha 2 — Contratos Canônicos (`P0`)

- documentar endpoints, schema, auth boundary e storage contracts
- garantir que mobile e frontend público consumam a mesma API/BFF
- impedir lógica de apresentação acidental dentro do core de backend

### Trilha 3 — Hardening De Release (`P1`)

- health checks, envs, observabilidade e checklist de deploy
- validação de build sem dependência de componentes que deveriam estar no
  frontend

### Trilha 4 — Réplica Futura (`P2`)

- manter a trilha Java/Quarkus apenas como replicação futura do contrato, não
  como distração do release atual

## Próximas Ações

1. Auditar `app/`, `components/` e `lib/` para marcar o que é backend/BFF e o
   que é frontend visual.
2. Definir a lista de rotas e contratos que permanecem canônicos neste repo.
3. Abrir a lane do frontend visual separado antes do próximo deploy público.
4. Revalidar o build do backend depois da limpeza de fronteiras.
