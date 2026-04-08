# raw/ — Fontes Brutas Imutáveis

Esta camada implementa o **raw layer** da arquitetura LLM Wiki (padrão Karpathy).

## Princípio

Arquivos aqui são **fontes primárias imutáveis** — o LLM nunca edita o conteúdo
desta pasta, apenas cria compilações derivadas em `memory/wiki/`.

> "Keep the raw source around forever and let the wiki be editable."
> — Andrej Karpathy, LLM Wiki (2024)

## Subdiretórios

### `videos/`

Transcrições brutas de vídeos referenciados no workspace.

- Formato: `<youtube-id>_<slug>.md`
- Campos de frontmatter obrigatórios: `url`, `author`, `date`, `captured_at`
- O conteúdo é a transcrição literal, sem edição nem resumo

### `articles/`

Textos integrais de artigos, papers e posts referenciados.

- Formato: `<slug>.md` ou `<slug>.html` conforme o original
- Campos de frontmatter obrigatórios: `url`, `author`, `date`, `captured_at`
- O conteúdo é o texto integral capturado, sem edição

## Regras

1. **Nunca editar** o conteúdo de uma fonte após captura
2. **Nunca resumir** nesta camada — resumos e compilações vão para `memory/wiki/`
3. **Sempre registrar** `captured_at` (data ISO 8601) para rastreabilidade
4. Se a fonte mudar, criar um novo arquivo versionado ao lado do original
5. Esta pasta é append-only para agentes LLM

## Mapeamento Karpathy → Workspace

| Camada Karpathy | Equivalente no workspace |
|-----------------|--------------------------|
| `raw/`          | `jpglabs/docs/raw/`      |
| `wiki/`         | `jpglabs/docs/memory/wiki/` |
| `schema`        | `WORKSPACE_BOOTSTRAP.md` + `CLAUDE.md` + `AGENTS.md` |
| `log`           | `daily/*.md` + `agents/AGENT_BRIDGE.md` |

Ver ADR completo em `jpglabs/docs/research/adr/ADR-001-llm-wiki-architecture.md`.
