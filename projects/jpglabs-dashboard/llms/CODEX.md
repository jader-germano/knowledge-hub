# Codex Repo Context - jpglabs-dashboard

Objetivo: dar ao Codex um bootstrap fino para operar em `jpglabs-dashboard` sem
duplicar a fonte canônica do workspace.

Consulta obrigatória:

1. `CODEX.md`
2. `llms/CODEX.md`
3. `projects/jpglabs-dashboard/PROJECT_CONTEXT.md`
4. `projects/jpglabs-dashboard/GIT_HISTORY.md`

Ao atuar neste repo:

- trabalhar no repo real em `/Users/philipegermano/code/jpglabs/jpglabs-dashboard`
- usar `projects/jpglabs-dashboard/PROJECT_CONTEXT.md` como resumo estável
- usar `projects/jpglabs-dashboard/GIT_HISTORY.md` para sinal recente antes de editar
- preferir `next` docs oficiais quando tocar APIs version-sensitive
- evitar inventar integração com Figma sem arquivo/url concreto
- tratar agentes como squad de apoio técnico e preservar autoria humana dos
  commits; registrar assistência de IA em `PR`, handoff, `ADR` ou sessão, não
  em `Co-Authored-By` por default
- registrar histórico específico em `projects/jpglabs-dashboard/sessions/` quando houver material novo
- tratar agentes como squad de apoio para pesquisa, arquitetura, Figma handoff,
  implementação, testes, revisão e observabilidade, sem converter isso em
  coautoria automática de commit
- manter commits com autoria humana; quando necessário, registrar uso de IA em
  handoff, ADR ou PR description, não em `Co-Authored-By`
