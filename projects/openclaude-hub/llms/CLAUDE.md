# Claude Repo Context — openclaude-hub

Objetivo: dar ao Claude um bootstrap fino para operar em `openclaude-hub`
(rebrand visual `Axis`) sem duplicar a fonte canônica do workspace.

Consulta obrigatória:

1. `CLAUDE.md` raiz do workspace
2. `jpglabs/docs/llms/CLAUDE.md`
3. `projects/openclaude-hub/PROJECT_CONTEXT.md`
4. `projects/openclaude-hub/GIT_HISTORY.md`

Ao atuar neste repo:

- trabalhar no repo real em `/Users/philipegermano/code/jpglabs/openclaude-hub`
- usar `projects/openclaude-hub/PROJECT_CONTEXT.md` como resumo estável (stack, deploy, env, quality gates)
- usar `projects/openclaude-hub/GIT_HISTORY.md` para sinal recente antes de editar
- respeitar o rebrand em curso: nome de código `openclaude-hub`; nome visual `Axis`; rename físico do repo e DNS continuam pendentes
- preferir `supabase` como `AUTH_PROVIDER`; a rota `github` segue como fallback legacy
- validação padrão: `npm run validate` (lint + typecheck + test)
- registrar histórico específico em `projects/openclaude-hub/sessions/` quando houver material novo
