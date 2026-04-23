# openclaude-hub Git History

Snapshot classificado do histórico do repositório em 2026-04-23.

## Commits Relevantes

- `5358d2a chore(release): bump version to 0.6.19`
  - patch release mais recente; último sinal de estabilidade da trilha de deploy

- `294ed2a ci(deploy): route SSH through Tailscale userspace (SOCKS5)`
  - roteou o deploy VPS por Tailscale userspace; dependência de rede passou de SSH direto para SOCKS5 via Tailscale

- `787ef2d ci: install rsync+openssh-client in deploy stage`
  - estabilizou o estágio de deploy instalando rsync e openssh-client na imagem de CI

- `7e8a0bc chore(deps): vendor @jpglabs/cartesian-red as local workspace`
  - vendoring do design system compartilhado como workspace local; reduz acoplamento de release entre hub e portfólio

- `4193a17 Merge feat/shared-auth-realm-s1a into main`
  - merge da trilha S1A de auth compartilhada — Supabase OAuth + `/auth/exchange` + refresh interceptor; marca encerramento da sprint 1A

- `b9dc256 feat(login): Cartesian grid + remove GitHub + load IBM Plex Sans`
  - `LoginPage` alinhada ao `Axis/Cartesian Red`; remoção do fluxo GitHub (fallback via env); tipografia canônica carregada

- `d958733 feat(auth): S1A client-side OAuth — Supabase → /auth/exchange + refresh interceptor`
  - `LoginPage`, `AuthContext`, `Supabase client` sem `localStorage`, `AuthCallback`, `fetch interceptor` com mutex/retry em `401`

- `5ad1d17 feat(client): Axis visual refactor slice 1 — Cartesian Red + Fraunces + layout align`
  - primeira fatia do rebrand visual para `Axis`; Cartesian Red + Fraunces aplicados ao client

- `bdda5b5 fix(auth): derive sameSite from secureCookies (B1)`
  - `sameSite` passa a derivar de `secureCookies`; pré-requisito para cross-subdomain em produção

- `69d8ddb feat(auth): CORS middleware for portfolio cross-origin auth`
  - CORS dedicado para permitir `jpglabs-portfolio` consumir auth do hub sem relaxar política geral

## Leitura Operacional

- a trilha recente priorizou auth compartilhada (`shared-auth-realm-s1a`) e rebrand visual para `Axis`
- estabilidade de deploy foi reforçada via Tailscale userspace + patch releases frequentes
- o rebranding visual chegou ao cliente mas ainda não foi formalizado como rename do repositório ou do DNS — ação manual pendente
- a próxima fatia natural é Sprint 1B (continuação do `/auth/refresh` que ainda degrada para logout em `404`) e rename físico
