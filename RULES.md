# Rules

Regras operacionais do repositório documental canônico em `code/jpglabs/docs`.

## Regra 1: Fonte Canônica

- conteúdo compartilhado vive neste repositório
- contexto específico vive em `projects/`
- runtime local continua no root ou em pastas específicas de provider

## Regra 2: Ordem De Consulta

Toda LLM ou agente deve iniciar por:

1. `RULES.md`
2. `OWNERSHIP.md`
3. `WORKSPACE_INDEX.md`
4. `GIT_HISTORY_INDEX.md`
5. `manifests/workspace.index.yaml`
6. `DOC_INDEX.md`
7. `agents/AGENT_BRIDGE.md`
8. `agents/SESSION_CLOSE_TEMPLATE.md`

## Regra 3: Conteúdo Compartilhado

- material genérico sobe para o root deste hub
- material específico de repo vai para `projects/<repo>/`
- histórico Git classificado por repo vive em `projects/<repo>/GIT_HISTORY.md`
- contexto por provider e por repo vive em `projects/<repo>/llms/`
- histórico de sessão vai para `projects/<repo>/sessions/`

## Regra 4: Não Duplicar Código Nem Produto

- o hub não substitui README, arquitetura ou docs internas dos repositórios reais
- o hub indexa, resume e aponta

## Regra 5: Bootstrap De Provider

- `WORKSPACE_BOOTSTRAP.md` é a entrada compartilhada da raiz
- `AGENTS.md` é apenas shim do fluxo Codex
- `CODEX.md`, `CLAUDE.md` e `GEMINI.md` são deltas específicos por provider
- arquivos locais de provider devem ser finos e apontar para o bootstrap compartilhado
- contexto fino por repo deve apontar para `projects/<repo>/llms/<provider>.md`

## Regra 6: Handoff Obrigatório

Toda sessão com mudança relevante deve:

1. atualizar `agents/AGENT_BRIDGE.md` quando houver impacto transversal
2. registrar ou atualizar o resumo em `daily/<yyyy-mm-dd>.md`
3. sincronizar a memória compartilhada do Docker MCP

## Regra 6A: Glossário Obrigatório No Fechamento

- todo fechamento de sessão deve conter a seção `References And Glossary`
- `References` deve registrar as superfícies realmente acessadas e o que foi
  obtido delas, não apenas listar caminhos soltos
- quando não houver termo novo, o agente deve registrar explicitamente:
  `Nenhum novo termo precisou entrar em GLOSSARY.md nesta rodada.`
- quando houver termo novo, ele deve ser adicionado ao `GLOSSARY.md` canônico e
  referenciado no fechamento
- quando a sessão introduzir ou harmonizar terminologia em múltiplos idiomas,
  o fechamento deve conter também `Glossário multilíngue`
- quando essa assinatura adicional não se aplicar, o agente deve declarar
  explicitamente: `Glossário multilíngue: não aplicável nesta sessão.`

## Regra 7: Idioma

- documentação compartilhada em `pt-BR`
- código, símbolos, tipos, testes e contratos técnicos em inglês

## Regra 8: Git E Prioridade

- usar `GIT_HISTORY_INDEX.md` para contexto rápido
- validar o repo real antes de propor mudanças
- não confundir espelho documental com fonte real de código

## Regra 8A: Preflight Git Obrigatório Antes De Código

- toda nova rodada de alteração de código em um repo Git deve começar com
  check-up de sincronização
- o check-up mínimo obrigatório é:
  - `git status --short`
  - `git pull --ff-only`, quando a worktree estiver limpa e o branch tiver
    upstream configurado
- logo após o sync, rodar a suíte unitária padrão do repo
- se houver teste já quebrado no início da rodada, corrigir ou isolar o
  problema explicitamente antes de abrir nova alteração de código
- se o repo ainda não tiver suíte unitária executável, declarar esse gap antes
  de editar e tratar a criação da suíte como primeira fatia técnica
- se a worktree estiver suja, o agente não deve puxar às cegas nem editar em
  cima de base potencialmente desatualizada; deve declarar o bloqueio
- se o branch não tiver upstream, o agente deve declarar isso explicitamente
  antes de editar código
- a intenção é reduzir drift, conflitos evitáveis e implementação sobre base
  antiga

## Regra 9: Planejamento E Execução

- `Jira` é a fonte canônica de task, status e prioridade operacional quando a
  trilha já estiver espelhada no Atlassian
- `Confluence` é a fonte canônica de especificação, decisão e narrativa de
  roadmap
- `Notion` fica restrito ao Diário de Bordo e não deve ser reutilizado como
  board de task ou roadmap
- exceção temporária aprovada:
  até `2026-05-31`, a trilha de migração/estabilização deve manter espelho
  paralelo em `Jira + Confluence` e `Notion`, com decisão formal em
  `2026-05-31` sobre encerramento ou continuidade do paralelismo
- `ROADMAP.md` em Markdown continua válido como espelho local, briefing e
  apoio de contexto, mas não substitui o board canônico de execução

## Regra 10: Concorrência E Tokens

- antes de abrir discovery amplo, carregar contexto local já existente do
  projeto
- não iniciar processo novo se já houver guideline, roadmap, ADR ou ticket
  cobrindo a trilha
- priorizar leituras pequenas e específicas em vez de scans globais
- respeitar surfaces de concorrência existentes como `threads`, handoffs e
  lanes de branch

## Regra 11: Continuidade Com Aprovação

- toda tarefa substancial deve terminar com uma proposta concreta de próximo
  passo
- essa proposta deve aproveitar o contexto já consolidado e pedir apenas a
  autorização, não um novo briefing
- quando a UI do cliente suportar popup/card de aprovação, preferir esse
  formato

## Regra 12: Cobertura Como Barra De Qualidade

- a barra padrão do workspace é cobertura **alta** das unidades criadas ou
  alteradas no slice (caminho feliz, bordas e falhas previsíveis), não métrica
  cega de `100%` global
- `100%` é aspiração quando o custo do teste é menor que o custo do escape;
  não deve ser exigido como meta pré-sprint nem como vara de medir qualidade
- código novo, refatorado ou estabilizado só é considerado entregue quando
  houver cobertura automatizada para os comportamentos que importam; validação
  manual, build verde ou smoke test não substituem teste automatizado
- quando houver gap de cobertura deliberado, o agente deve registrar:
  - qual comportamento ficou sem teste
  - por que testá-lo hoje não compensa (custo > risco, dependência instável,
    fatia próxima que já vai refatorar, etc.)
  - qual sinal de mudança exigiria fechar o gap
- decisões de arquitetura devem favorecer testabilidade: desacoplamento,
  layering, SOLID, clean architecture e TDD — isso reduz a escolha falsa
  entre cobertura e velocidade
- o `review-qa-engineer` é a autoridade caso a caso sobre o que precisa de
  teste e onde `100%` vira cerimônia

## Regra 13: Context7 Antes De Docs E Implementação

- `context7` passa a ser obrigatório antes de atualizar documentação técnica
  ou implementar contra biblioteca, framework, SDK, API ou MCP externo
- a consulta serve como gate de conferência de contrato, versão, parâmetros,
  limitações e exemplos atuais
- quando `context7` não cobrir a tecnologia, usar a documentação oficial mais
  atual e declarar explicitamente o fallback

## Regra 14: Autoria Humana E Uso De IA

- commits continuam com autoria e responsabilidade humanas; em repositórios
  corporativos, regulados ou sensíveis, preservar assinatura humana inequívoca
  no histórico Git é a regra default
- por padrão, não adicionar `Co-Authored-By` para agentes como `Codex`,
  `Claude` ou equivalentes quando atuarem como assistentes sob direção e
  revisão humana
- o uso de agentes deve ser tratado como assistência operacional, não como
  coautoria automática de código; agentes apoiam pesquisa, arquitetura, Figma
  handoff, implementação, testes, revisão, observabilidade e documentação, mas
  não entram como coautores por padrão
- quando a sessão usar IA de forma relevante, registrar isso fora do commit,
  em `PR`, `ADR`, handoff, diário técnico, relatório diário ou sessão
  classificada, com resumo factual do apoio prestado
- escopo, revisão de diff, aprovação, merge e responsabilização final
  permanecem humanos
- qualquer exceção — incluindo adicionar `Co-Authored-By` para agente — precisa
  ser decisão humana explícita e contextual, deliberada pelo responsável do
  repositório ou pela governança da trilha

## Regra 15: AIJL Como Padrão de Segurança para Agentes

- todo projeto JPGLabs deve incluir `.ai-jail` na raiz do repositório
- sessões de desenvolvimento com agentes de IA iniciam com `ai-jail claude` (ou
  equivalente para o agente em uso), nunca diretamente
- `ai-jail --bootstrap` deve ser executado na configuração inicial do ambiente
- a especificação completa e justificativa estão em `AI_JAIL_STANDARD.md`
- se o usuário solicitar uma sessão ou arquitetura que contradiga este padrão
  (ex: sem sandbox, `--dangerously-skip-permissions` sem camada externa, deploy
  direto de agente sem revisão), Claude deve identificar o conflito, citá-lo
  explicitamente e aguardar confirmação antes de prosseguir
- exceções válidas (CI/CD sem bubblewrap, container já isolado, tool quebrada
  pelo sandbox-exec) devem ser documentadas como ADR no projeto
