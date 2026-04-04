# JPGLabs Knowledge Hub

Repositório privado canônico de documentação do workspace JPG Labs.

- Remote canônico: `origin`
- Repositório: `git@github.com:jader-germano/knowledge-hub.git`
- Path real no workspace: `/Users/philipegermano/code/jpglabs/docs`

## Estrutura Atual

- `MCP_SETUP.md` — baseline MCP e integrações de desenvolvimento
- `llms/` — bootstrap transversal por provider
- `Projects/Knowledge-Hub.md` — contexto do próprio repositório privado
- `memory/` — memória compartilhada e governança operacional
- `Projects/` e `Backlog/` — superfícies herdadas do hub anterior, mantidas como
  mirror até a migração estrutural completa

## Regra Operacional

- este repo é o `Knowledge Hub` do workspace
- documentação por LLM deve viver em `llms/`
- documentação do próprio repo privado deve viver em `Projects/Knowledge-Hub.md`
- mudanças operacionais transversais devem preferir este repositório antes de
  espalhar bootstrap em notas locais ou clientes específicos
