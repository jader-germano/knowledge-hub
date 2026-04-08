# portfolio-mobile Roadmap

Atualizado em `02/04/2026`.

## Papel No Ecossistema

`portfolio-mobile` deve ser um cliente fino do ecossistema do portfólio, não um
segundo backend nem um lugar para compensar indefinições do `portfolio-backend`.

## Leitura Atual

- base ainda próxima do starter do Expo
- já recebeu uma trilha inicial de OAuth puxada do contexto Pi
- ainda falta clareza sobre o papel final do app no ecossistema

## Trilhas

### Trilha 1 — Clarificação De Escopo (`P0`)

- decidir se o app será:
  - companion autenticado do portfólio
  - shell de dono/operator
  - cliente público simplificado
- evitar abrir feature antes dessa decisão

### Trilha 2 — Consumo De Contrato Canônico (`P1`)

- consumir somente contratos do `portfolio-backend` e do `pi-local-app` quando
  fizer sentido
- não recriar fluxo de auth, sessão ou dados localmente

### Trilha 3 — Redesign Mobile (`P1`)

- aplicar a linguagem nova de UI/UX depois que o papel do app estiver fechado
- alinhar navegação e estados com `PiPhone` quando houver sobreposição real

## Próximas Ações

1. Fechar a missão do app antes de adicionar novas telas.
2. Remover ou isolar restos do starter que não correspondem ao papel final.
3. Mapear quais fluxos dependem do `portfolio-backend` e quais dependem do
   contrato Pi.
4. Só então iniciar o redesign visual.
