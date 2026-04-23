# Gemini Repo Context — openclaude-hub

Objetivo: dar ao Gemini um bootstrap fino para operar em `openclaude-hub`
(rebrand visual `Axis`) sem duplicar a fonte canônica do workspace.

Consulta obrigatória:

1. `GEMINI.md` raiz do workspace
2. `jpglabs/docs/llms/GEMINI.md`
3. `projects/openclaude-hub/PROJECT_CONTEXT.md`
4. `projects/openclaude-hub/GIT_HISTORY.md`

Ao atuar neste repo:

- trabalhar no repo real em `/Users/philipegermano/code/jpglabs/openclaude-hub`
- usar `projects/openclaude-hub/PROJECT_CONTEXT.md` como resumo estável
- usar `projects/openclaude-hub/GIT_HISTORY.md` para sinal recente antes de editar
- respeitar o rebrand: nome de código `openclaude-hub`; nome visual `Axis`
- `AUTH_PROVIDER=supabase` é o caminho canônico; `github` é fallback legacy
- validação padrão: `npm run validate`
- registrar histórico específico em `projects/openclaude-hub/sessions/` quando houver material novo
