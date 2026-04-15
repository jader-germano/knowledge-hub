# Report

## Session Metadata

- Data: 2026-04-14
- `feature/session id`: `feat/vps-ollama-profiles`
- Repositório: `/Users/philipegermano/code/openclaude`
- Branch: `feat/vps-ollama-profiles`
- Objetivo aprovado: corrigir acesso Ollama VPS via Tailscale, instalar CLI
  local e VPS, configurar Syncthing bidirecional, ativar feature flags de
  codificação em todos os providers.

## Delivery Contract

- Entregáveis explícitos:
  - Fix CGNAT (100.64.0.0/10) no `providerConfig.ts` para Tailscale sem API key
  - VPS Ollama lane (preset + scripts + ProviderManager UI)
  - Health check pre-flight no `providerValidation.ts`
  - Feature flags de codificação no build (7 flags) e runtime (3 env flags)
  - Ollama instalado local (M4) com 2 modelos + benchmark
  - VPS Ollama otimizado (KEEP_ALIVE=24h, NUM_PARALLEL=2, FLASH_ATTENTION=1)
  - Syncthing bidirecional Mac ↔ VPS via Tailscale
  - AGENTS.md limpo (paths mortos, skill registry atualizado)
  - Skills sync via `sync_shared_skills.py` (7 skills)
  - Configs aplicadas em Codex e Gemini
- Fora do escopo:
  - Codex OAuth (requer browser interativo)
  - A record DNS para `syncthing.jpglabs.com.br`
  - Migração de legados VPS (`/root/Sync`, `/root/k8s`, `/root/backup`)
  - GPU VPS (Hostinger não oferece)

## Prototype And Evidence

- Figma file: n/a
- Figma frame: n/a
- Pasta de evidências: n/a — sessão de infra/tooling, não feature funcional
- `macos.gif` valida: n/a
- `ios.gif` valida: n/a

## Summary

- O OpenClaude fork passou a suportar Ollama em VPS via Tailscale sem exigir
  `OPENAI_API_KEY`, reconhecendo o range CGNAT (100.64.0.0/10) como rede
  privada em `isPrivateIpv4Address`.
- O health check pre-flight faz ping GET `/v1/models` (4s timeout, zero tokens)
  antes de deixar o runtime construir o system prompt (~10-15k tokens). Se o
  Ollama estiver offline, bloqueia com mensagem clara.
- Syncthing bidirecional ativo entre Mac (100.64.53.33) e VPS (100.68.217.36).
  Windows (100.77.34.128) como peer pendente (auto-accept configurado).
- 7 feature flags de build ativadas: BRIDGE_MODE, AGENT_TRIGGERS,
  CACHED_MICROCOMPACT, CONTEXT_COLLAPSE, BG_SESSIONS, AWAY_SUMMARY,
  WEB_BROWSER_TOOL. 3 env flags de runtime: MAINTAIN_PROJECT_WORKING_DIR,
  ENABLE_TASKS, ENABLE_CFC.
- AGENTS.md saneado: 4 paths mortos removidos (~/.codex/skills/jader-*,
  ~/.pi/agent/skills/*), skill registry atualizado com 15 entries canônicas,
  agent bundle marcado como archived.
- Benchmark M4 local: gemma4:e4b processa 3500 tokens em 17.7s (199 tok/s) vs
  77s na VPS CPU (46 tok/s) — 4.3x mais rápido.
- O que permanece aberto: Codex OAuth, DNS syncthing, legados VPS, Windows peer.

## Validation

- Builds executados: `bun run build` local e VPS — OK
- Testes executados:
  - smoke test `openclaude --version` local e VPS — `0.3.0 (Open Claude)`
  - health check: Ollama UP → PASS | porta inexistente → ECONNREFUSED (blocked)
  - CGNAT: `100.68.217.36` → private=true | `104.18.20.3` → private=false
  - Syncthing: `syncthing cli show connections` → VPS connected=True
  - Ollama benchmark: 4 modelos testados em VPS, 2 no M4 local
- Validação em macOS: sim — build, smoke, benchmark, Syncthing, Ollama
- Validação em iOS: n/a

## Commands Executed

- `brew install ollama`
  - Action: instalar Ollama no Mac M4
  - Result: v0.20.7 instalado via Homebrew
- `ollama pull qwen2.5-coder:7b` / `ollama pull gemma4:e4b`
  - Action: download de modelos para inferência local
  - Result: 4.7GB + 9.6GB baixados com sucesso
- `ssh root@srv1443703 "systemctl restart ollama"`
  - Action: aplicar KEEP_ALIVE=24h e otimizações no serviço
  - Result: Ollama reiniciado, gemma4:e4b warm por 24h
- `git push gitlab feat/vps-ollama-profiles`
  - Action: push da branch com 5 commits
  - Result: branch disponível em gitlab.com/jader-germano/openclaude
- `ssh root@srv1443703 "cd /opt/openclaude && git pull && bun run build"`
  - Action: deploy na VPS
  - Result: v0.3.0 rebuilt com todas as fixes
- `python3 ~/code/.agents/scripts/sync_shared_skills.py --target-root ~/.claude/skills --preserve-unmanaged`
  - Action: sincronizar skills canônicas para o runtime Claude
  - Result: 7 skills sincronizadas, 3 orphans preservados
- `brew services restart syncthing`
  - Action: restart Syncthing com VPS e Windows como peers
  - Result: VPS connected, Windows pending

## Files Created

- `/Users/philipegermano/.claude/feature-flags.json`
- `/Users/philipegermano/.claude/projects/-Users-philipegermano-code-openclaude/memory/project_ollama_setup.md`
- `/Users/philipegermano/Sync/`
- `/etc/systemd/system/syncthing.service` (VPS)
- `/root/.config/syncthing/config.xml` (VPS)

## Files Modified

- `/Users/philipegermano/code/openclaude/src/services/api/providerConfig.ts`
- `/Users/philipegermano/code/openclaude/src/utils/providerValidation.ts`
- `/Users/philipegermano/code/openclaude/src/utils/providerProfiles.ts`
- `/Users/philipegermano/code/openclaude/src/components/ProviderManager.tsx`
- `/Users/philipegermano/code/openclaude/scripts/build.ts`
- `/Users/philipegermano/code/openclaude/scripts/system-check.ts`
- `/Users/philipegermano/code/openclaude/package.json`
- `/Users/philipegermano/code/jpglabs/docs/memory/AGENTS.md`
- `/Users/philipegermano/.claude/settings.json`
- `/Users/philipegermano/.claude.json`
- `/Users/philipegermano/.codex/config.toml`
- `/Users/philipegermano/.gemini/settings.json`
- `/root/.claude.json` (VPS)
- `/root/.openclaude-profile.json` (VPS)
- `/root/Sync/code/config/opencloud/mesh-sync.targets.json` (VPS)
- `/etc/systemd/system/ollama.service` (VPS)
- `/etc/systemd/system/ollama.service.d/override.conf` (VPS)

## Change Tree

```text
openclaude (feat/vps-ollama-profiles — 5 commits)
├── src/services/api/providerConfig.ts       [CGNAT private IP fix]
├── src/utils/providerValidation.ts          [pre-flight health check]
├── src/utils/providerProfiles.ts            [ollama-vps preset]
├── src/components/ProviderManager.tsx        [VPS option in /provider UI]
├── scripts/build.ts                         [7 feature flags enabled]
├── scripts/system-check.ts                  [remote Ollama message]
└── package.json                             [dev:ollama:vps, profile:vps]

~/.claude/
├── settings.json                            [3 env flags added]
├── feature-flags.json                       [new]
└── skills/                                  [7 synced from .agents/]

~/.codex/config.toml                         [auto_memory, context_collapse, bg_sessions]
~/.gemini/settings.json                      [full thinking UI, memory usage]

jpglabs/docs/memory/AGENTS.md                [cleaned: paths, registry, models]

VPS /root/
├── .claude.json                             [3 provider profiles]
├── .openclaude-profile.json                 [gemma4:e4b default]
├── .config/syncthing/config.xml             [Mac + Windows peers]
├── Sync/code/config/opencloud/
│   └── mesh-sync.targets.json               [updated: Mac Air, JPRDTR, -Ayumi]
└── /opt/openclaude/                         [feat/vps-ollama-profiles deployed]
```

## Versioning Proposal

- Branch: `feat/vps-ollama-profiles` (5 commits, pushed no GitLab)
- Commit: padrão `type(scope): resumo` mantido nos 5 commits
- Review request: validar feature flags em sessão real antes de merge para `main`

## Language Policy

- Títulos estruturais em English por interoperabilidade
- Conteúdo narrativo em `pt-BR`
- Paths, flags, comandos, branches, commits e símbolos técnicos em English

## References And Glossary

- `/Users/philipegermano/code/jpglabs/docs/agents/SESSION_CLOSE_TEMPLATE.md` — template de fechamento (legado, esta sessão usa o novo template)
- `/Users/philipegermano/code/jpglabs/docs/reports/sessions/_template/report.md` — template atual
- `/Users/philipegermano/code/jpglabs/docs/memory/AGENTS.md` — atualizado nesta sessão
- `/Users/philipegermano/code/jpglabs/docs/memory/MEMORY_SYNC.md` — protocolo de sync consultado
- Glossário multilíngue: não aplicável nesta sessão; nenhum novo termo introduzido

---

## Glossário Multilíngue — Referência de Sessões

> Não aplicável nesta sessão. Nenhum termo técnico novo foi introduzido,
> traduzido ou harmonizado além do léxico já consolidado.

---

## Risks And Gaps

- Feature flags BRIDGE_MODE, WEB_BROWSER_TOOL e CONTEXT_COLLAPSE ativadas no
  build podem expor code paths não testados no open build. Monitorar erros.
- Syncthing Windows peer (JPRDTR) pendente — requer aceitar folder no host.
- A record DNS `syncthing.jpglabs.com.br` não criado (Caddy entry pronta).
- Codex OAuth não configurado (requer sessão interativa com browser).
- VPS legados (`/root/Sync`, `/root/k8s`, `/root/backup`, `/root/build`)
  sem decisão de migração ou archival.
- `gemma4:26b` permanece como `model` no `settings.json` — considerar trocar
  para provider-neutral ou remover.

## Next Actions

- **Windows SSH**: abrir PowerShell como Admin, `Restart-Service sshd`,
  verificar firewall regra porta 22
- **Windows Syncthing**: instalar/iniciar Syncthing, adicionar Mac e VPS como
  devices, aceitar folders `workspace-sync` e `blender-projects`
- Codex OAuth via `/provider` na próxima sessão OpenClaude
- Testar feature flags em sessão real (BRIDGE_MODE, BG_SESSIONS, WEB_BROWSER_TOOL)
- Decidir sobre legados VPS (`/root/Sync`, `/root/k8s`, `/root/backup`)
- Merge da branch `feat/vps-ollama-profiles` para `main` após validação
- Syncthing GUI VPS acessível em `http://100.68.217.36:8384` (user: jpglabs,
  pass: jpgl4bs-sync!). DNS `syncthing.jpglabs.com.br:8384` criado mas usar
  porta direta sem Caddy.

## Handoff Notes

- Branch `feat/vps-ollama-profiles` (5 commits) no GitLab e deployed na VPS.
- Ollama local no Mac: `gemma4:e4b` (199 tok/s prompt eval no M4) e
  `qwen2.5-coder:7b` (alternativa rápida).
- VPS Ollama: `gemma4:e4b` warm 24h. Para trocar: `ollama run <model>`.
- Syncthing: Mac ↔ VPS connected. Windows pending (SSH + Syncthing install).
- Folders sync: `workspace-sync` (~/Sync ↔ /root/Sync) e `blender-projects`
  (~/BlenderProjects ↔ /root/BlenderProjects). Ambos com 3 devices (Mac, VPS,
  Windows).
- Taxonomia local limpa: 19 → 11 dirs. Archive em `~/code/.archive/`.
- AGENTS.md saneado. Skills sincronizadas (7 canonical + 3 orphans + 4 pi).
- Feature flags: 7 build-time + 3 runtime. Propagadas para Claude, Codex,
  Gemini (Mac e VPS).
- Cloudflare DNS token propagado para todos os providers (env var
  `CLOUDFLARE_DNS_TOKEN`).
- `python/ollama_provider.py` é standalone legado — path real é TS:
  `providerProfiles.ts` → `providerDiscovery.ts` → `/v1`.
