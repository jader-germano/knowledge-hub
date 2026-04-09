# Pi — Agente de Coding Mínimo e Extensível

> Compilado de: `raw/videos/Dli5slNaJu0_mario-zechner-pi-coding-agent.md`  
> Última atualização: 2026-04-08  
> Autor: Mario Zechner (@badlogic)  
> Repo: https://github.com/badlogic/pi-mono

## O que é

Pi é um coding agent harness construído pelo princípio oposto ao Claude Code:
**menos features, mais controle e extensibilidade**. Criado por Mario Zechner
(Austrian, libGDX fame) como reação a harnesses "espaçonave".

## Filosofia Central

> "Adapt your coding agent to your needs instead of the other way around."

**Tese:** ninguém sabe ainda qual é o coding agent ideal. Precisamos de
ferramentas maleáveis para experimentos rápidos — não spaceships com 90% de
features que ninguém usa.

## Arquitetura

```
pi-mono/
├── @ai/            ← abstração sobre múltiplos providers (OpenAI, Anthropic, Ollama, etc.)
├── @agent-core/    ← agent loop genérico: tool dispatch, verification
├── @tui/           ← terminal UI em ~600 linhas (sem React no terminal)
└── pi/             ← coding agent = SDK + TUI
```

## As 4 Ferramentas Únicas

Pi entrega apenas 4 tools ao modelo:

| Tool | Função |
|------|--------|
| `read_file` | Lê arquivo |
| `write_file` | Escreve arquivo |
| `edit_file` | Edição de arquivo |
| `bash` | Executa shell |

**O que NÃO existe (e por quê):**

| Ausente | Alternativa Pi | Motivo |
|---------|---------------|--------|
| MCP | CLI tools + skills | MCP carrega tudo upfront |
| Sub-agents | tmux + spawn | Sub-agents não são observáveis |
| Plan mode | Escrever `plan.md` | Artefato persistente > UI janky |
| Background bash | tmux | Mesmo resultado |
| Built-in to-dos | Escrever `todo.md` | Mesmo resultado |
| LSP inline | Só ao final | LSP mid-edit confunde o modelo |

## System Prompt

Mínimo. Frontier models já foram RL-treinados para saber que são coding agents.
Não precisa explicar novamente.

## Extensibilidade

- TypeScript puro, hot reload
- Custom tools: o LLM pode chamar tools que **você** define
- Custom compaction: cada harness implementa de forma diferente; Pi deixa aberto
- Permission gates: 50 linhas de TypeScript cobrem todos os casos
- Custom providers: proxies, self-hosted, sem precisar de fork
- UI customizável: acesso completo ao TUI (exemplos: pi-annotate, pi-messenger)

## Performance

No T-Bench (Terminal Bench), Pi com Claude Opus 4.5 ficou logo atrás do
Terminus 2 — sem nem ter compaction implementado na época.

**Implicação:** features extras dos harnesses não são necessárias para boa
performance. O modelo faz o trabalho; o harness só atrapalha quando é
opaco/instável.

## Crítica ao Claude Code

- Instabilidade de contexto: mudanças diárias no que é injetado no contexto
  atrás do usuário
- Observabilidade limitada por design (UI simplifica demais para a maioria)
- Extensibilidade real baixa vs. hooks baseados em processos externos (caro)
- Sem escolha de modelo (lock-in Anthropic)
- TUI com React no terminal → flicker → overhead desnecessário

**Nota:** Mario reconhece que Claude Code é o líder da categoria e inventou o
gênero. A crítica é de fit pessoal, não de qualidade objetiva.

## OSSification

Estratégia de Mario para manter o repo saudável frente a spam de clankers:
1. Fechar issues/PRs em lote por semanas quando necessário
2. Allowlist de contribuidores: PR só passa se o autor está em arquivo Markdown
3. "Apresente-se em voz humana via issue antes de mandar PR"

## Relação com este workspace

Pi foi a inspiração para o Unified Memory Center (2026-04-07):
- pi-skills instalados e linkados para Claude, Codex e Pi
- extensions `memory-sync` e `session-logger` seguem o padrão Pi de extensions shell
- Filosofia de 4 tools → razão de preferir CLI + skills sobre MCP bloated

**Ver também:** `jpglabs/docs/memory/PI_MEMORY.md` seção Pi Infrastructure
