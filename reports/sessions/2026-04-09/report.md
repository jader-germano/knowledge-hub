# Report — 2026-04-09

## Session Metadata

- Data: 2026-04-09
- Repositório: knowledge-hub
- Branch: feature/unified-memory-center
- Objetivo: Infra Tailscale + Docker sync + Fix 522 + Glossário multilíngue + CI GitLab

## Delivery Contract

- Entregáveis explícitos: VPS sync container, fix 522, co-author cleanup, CI mesh-sync
- Fora do escopo: Blender/Maya install, GitLab CI variable (pendente token)

## Summary

### Infraestrutura
- Windows PC adicionado à rede Tailscale (100.77.34.128)
- Docker Desktop instalado no Windows com WSL2
- Container vps-sync criado: sync VPS → Windows a cada 30min via SSH+tar
- SSH keys configuradas: MacBook → VPS, Windows → ayuminha

### Cloudflare 522 — RESOLVIDO
- **Causa raiz:** DOCKER-USER chain do iptables dropava tráfego após DNAT do k3s
- k3s svclb faz DNAT de :443 → porta interna do pod Traefik
- Regras DOCKER-USER só permitiam multiport 80,443 — após DNAT, porta mudava → DROP
- **Fix:** `iptables -I DOCKER-USER 2 -d 10.42.0.0/16 -j RETURN`
- **Persistência:** /etc/network/if-up.d/k3s-docker-fix
- **Bonus:** Caddy recriado com --network host (antes bridge não alcançava localhost:31936)

### Git cleanup
- Removido Co-Authored-By do commit 1e5dfce → 14cf724 (amend local)
- Regra salva: nunca co-author em commits

### CI/CD
- .gitlab-ci.yml criado: pipeline mesh-sync em push/MR
- scripts/mesh-sync.sh: pull VPS → sync Windows/Mac via Tailscale
- Pendente: variável VPS_SSH_KEY no GitLab CI (requer Personal Access Token)

### Glossário multilíngue
- Template _templates/daily-session.md atualizado com seção glossário
- GLOSSARY.md expandido com 15+ termos em 4 idiomas
- Memória Claude (local + VPS) atualizada com template de fechamento

## Files Created

- /sync/jpglabs-docs/.gitlab-ci.yml
- /sync/jpglabs-docs/scripts/mesh-sync.sh
- /etc/network/if-up.d/k3s-docker-fix
- C:\docker\sync\{Dockerfile,sync.sh,entrypoint.sh,docker-compose.yml}
- ~/.claude/projects/.../memory/rules_git.md

## Files Modified

- /sync/jpglabs-docs/_templates/daily-session.md
- /sync/jpglabs-docs/GLOSSARY.md
- /docker/caddy/Caddyfile (tls internal + auto_https off)
- Caddy container (recreated --network host)
- iptables DOCKER-USER chain
- Memória local e VPS (feedback_language, infra_vps, project_522, rules_git)

## Change Tree

```text
knowledge-hub (feature/unified-memory-center)
├── .gitlab-ci.yml [created]
├── scripts/mesh-sync.sh [created]
├── _templates/daily-session.md [modified]
└── GLOSSARY.md [modified]

VPS infra
├── /etc/network/if-up.d/k3s-docker-fix [created]
├── /docker/caddy/Caddyfile [modified]
└── Caddy container [recreated --network host]

Windows (C:\docker\sync\)
├── Dockerfile [created]
├── sync.sh [created]
├── entrypoint.sh [created]
└── docker-compose.yml [created]
```

## Versioning Proposal

- Branch: feature/unified-memory-center
- Commits: 14cf724 (glossary), 508ee46 (ci: mesh-sync)
- Pushed: GitHub ✅ | GitLab ✅

## Risks And Gaps

- GitLab CI variable VPS_SSH_KEY pendente (pipeline não funciona sem ela)
- iptables fix depende de /etc/network/if-up.d — se Docker/k3s reiniciar, pode precisar re-aplicar
- Cloudflare SSL mode Full aceita self-signed — considerar gerar Origin Certificate futuramente

## Next Actions

- Adicionar VPS_SSH_KEY como variável File no GitLab CI/CD
- Considerar Cloudflare Origin Certificate para segurança extra
- Merge feature/unified-memory-center → main quando estável

## Glossário multilíngue

| Termo (pt-BR) | English | Français | Italiano | 日本語 |
|---|---|---|---|---|
| Regra de firewall | Firewall rule | Règle de pare-feu | Regola firewall | ファイアウォールルール |
| Encaminhamento | Forwarding | Redirection | Inoltro | 転送 (tensō) |
| Gancho (hook) | Hook | Crochet | Gancio | フック (fukku) |
| Malha (mesh) | Mesh | Maillage | Maglia | メッシュ (messhu) |
| Implantação contínua | CI/CD | Déploiement continu | Distribuzione continua | 継続的デプロイ |

### Curiosidades linguísticas

**EN** — *Forwarding* vem do inglês antigo *foreweard*. Em networking, forwarding (encaminhar pacotes) ≠ routing (decidir o caminho) — camadas diferentes do modelo OSI.

**FR** — *Pare-feu* (firewall) = literalmente para-fogo. *Crochet* (hook) = diminutivo de *croc* — mesma raiz do crochê em português.

**IT** — *Maglia* (mesh) vem do latim *macula* (nó de rede). Também significa camiseta — contexto decide tudo.

**JP** — 転送 (tensō): 転 (ten, virar — radical 車/roda) + 送 (sō, enviar — radical 辶/caminho). VPSはパケットを転送します — O VPS encaminha os pacotes (SOV, partícula を marca objeto direto).
