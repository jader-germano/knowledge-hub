# MCP Setup

Canonical MCP reference for Codex, Claude, Gemini, and compatible agents in
the workspace rooted at:

- `/Users/philipegermano/code`

The workspace entrypoint and shared MCP config are:

- `/Users/philipegermano/code/.mcp.json`
- `/Users/philipegermano/code/config/mcp/docker-mcp-config.yaml`
- `/Users/philipegermano/code/config/mcp/docker-mcp-quality.yaml`
- `/Users/philipegermano/code/config/mcp/docker-mcp-shared-catalog.yaml`
- `/Users/philipegermano/code/docker/docker-compose.yml`
- `/Users/philipegermano/code/scripts/bootstrap.sh`
- `/Users/philipegermano/code/scripts/healthcheck.sh`

Provider-specific runtime directories that clients discover only from the root
remain in the workspace root as real files or directories. They are not
canonical shared config and should not be centralized via symlink.

## Role of this repository

`docs` is the documentation and handoff surface for:

- MCP topology
- agent interoperability
- markdown classification and workspace references

JPG Labs products now live under `jpglabs/`:

- `../apple-study-checklist`
- `../knowledge-hub-app`
- `../portfolio-backend`
- `../portfolio-mobile`

External or non-JPG Labs repositories remain at the workspace root:

- `../../FrankMD`
- `../../Playground 2`

Legacy material merged into this hub:

- `../imap-server`
- `tools/ai-orchestration-scripts`
- `archive/legacy-repos/ai-orchestration-hub`
- `archive/legacy-repos/jpglabs-infra-repo`

## Selected MCPs

The active Docker baseline is oriented to documentation, code review, and local
engineering support:

- `git`: local versioning, diffs, branch inspection, commit/staging workflows
- `filesystem`: controlled read/write access scoped to the workspace root
- `desktop-commander`: richer file and shell operations for local engineering workflows
- `playwright`: browser automation when UI or browser validation is needed
- `fetch`: web/document retrieval when up-to-date external context is needed
- `context7`: current library and framework documentation lookup
- `memory`: persistent engineering context and relationship tracking
- `sequentialthinking`: structured multi-step analysis for architecture and debugging

Optional or adjacent lanes:

- `docker`: host/container inspection kept outside the default baseline because
  the current Docker MCP server advertises at least one tool with empty object
  schema, which is rejected by the current Codex/OpenAI runtime during tool
  registration
- `github`: PR-oriented review, issue triage, and remote repository automation
  once `github.personal_access_token` is loaded in the Docker MCP keychain; it
  stays outside the shared baseline because Codex already has a richer
  provider-native GitHub lane and the Docker server becomes noisy without the
  token
- `semgrep`: structural/code-quality/security scanning once the Docker MCP
  server initializes cleanly on this host
- `sonarqube`: quality gates, metrics, issue tracking, and report-oriented review, enabled through the optional local `quality` profile plus `docker-mcp-quality.yaml`
- `youtube_transcript`: lightweight research lane for extracting tutorial,
  demo, and architecture video transcripts without polluting the default coding
  baseline
- `ast-grep`: currently unavailable in the Docker MCP catalog on this host and therefore kept out of the baseline
- `n8n`: workflow orchestration and email-automation composition when explicitly enabled in `docker-mcp-config.yaml`
- `resend`: outbound email delivery once credentials are present and the server is enabled
- `figma`: plugin/app-based integration for prototyping and design-system workflows, outside the Docker catalog on this host
- `piecenter`: experimental local `stdio` bridge for human-in-the-loop review, intentionally kept outside the Docker gateway baseline

## Current State

- Docker MCP Toolkit remains connected globally to `claude-code`,
  `claude-desktop`, `codex`, and `gemini` through the Docker gateway.
- `/Users/philipegermano/.codex/config.toml` also keeps a local `MCP_DOCKER`
  block aligned with the workspace baseline, so Codex is not dependent on the
  wide server selection from the Docker Desktop catalog.
- The workspace root `.mcp.json` currently enables `git`, `filesystem`,
  `desktop-commander`, `playwright`, `fetch`, `context7`, `memory`,
  and `sequentialthinking`.
- `/Users/philipegermano/.codex/config.toml` is now aligned to the same
  canonical wrapper and no longer references the defunct
  `jpglabs-knowledge-hub/.codex` path.
- Host-level revalidation on `2026-04-03` confirmed that
  `docker mcp server ls` returns `22 enabled` on this machine and that
  `docker mcp gateway run --dry-run` validates `git`, `filesystem`,
  `desktop-commander`, `playwright`, `fetch`, `context7`, `memory`,
  and `sequentialthinking`.
- Runtime revalidation on `2026-04-04` confirmed `docker mcp client ls --global`
  with `claude-code`, `claude-desktop`, `codex`, and `gemini` connected to the
  same `MCP_DOCKER` gateway.
- Host-level revalidation on `2026-04-05` first confirmed `22 enabled` MCP
  servers with Docker Desktop healthy on the host; after disabling the broken
  `docker` server, the active global surface moved to `21 enabled`.
- Host-level revalidation on `2026-04-12` reconfirmed `21 enabled` MCP
  servers, with `docker mcp client ls --global` still showing `claude-code`,
  `claude-desktop`, `codex`, and `gemini` connected to the same Docker gateway.
- Runtime revalidation on `2026-04-05` identified a new Codex-specific break:
  the global Docker Desktop catalog still exposed a tool named `docker` with
  `inputSchema: {"type":"object"}` and no `properties`, which the current
  OpenAI/Codex runtime rejects during tool registration.
- An attempt to mitigate that by disconnecting only the global `codex` client
  did not persist while the app remained active; Codex reconnected itself to
  the global Docker Desktop integration.
- The definitive corrective action on `2026-04-05` was therefore twofold:
  restore the local `MCP_DOCKER` block in `/Users/philipegermano/.codex/config.toml`
  and disable the global Docker MCP server `docker` on this host. That removed
  the invalid tool from the active surface while preserving the rest of the
  Docker MCP catalog for other clients.
- `git`, `filesystem`, and `desktop-commander` are configured in
  `config/mcp/docker-mcp-config.yaml` against `/Users/philipegermano/code`, not a
  repo-scoped subpath.
- `docker mcp gateway run --dry-run` validated the functional baseline for
  `git`, `filesystem`, `desktop-commander`, `playwright`, `fetch`,
  `context7`, `memory`, and `sequentialthinking`.
- The root `.mcp.json` was corrected on `2026-04-12` to restore parity with
  `/Users/philipegermano/.codex/config.toml`: the shared baseline remains only
  `git`, `filesystem`, `desktop-commander`, `playwright`, `fetch`,
  `context7`, `memory`, and `sequentialthinking`, while `github` and
  `youtube_transcript` stay opt-in lanes.
- On `2026-04-05`, the `docker` server was removed from the shared Codex
  baseline because the current runtime rejects at least one tool advertised by
  that server with `Invalid schema ... object schema missing properties`.
  Runtime/container inspection remains available through direct CLI usage and
  can return to the MCP baseline after an upstream schema fix.
- `piecenter` was removed from the Docker gateway baseline on `2026-04-05`
  because the shared catalog entry had no valid OCI image reference and broke
  `dry-run` for the whole gateway. It remains an experimental local bridge and
  must not be treated as part of the Docker baseline until it is packaged
  correctly.
- `ast-grep` is no longer present in `docker mcp server ls` on this host and
  must not be treated as part of the production baseline until Docker ships it
  again.
- When Docker commands are executed from the Codex sandbox, this host can
  produce false negatives such as `Docker Desktop is not running`; the
  canonical runtime check for this workspace should be treated as the
  host-level validation outside the sandbox.
- The adjacent repositories under `code/` are reachable through the
  workspace-scoped config and are no longer isolated behind a repo-only MCP
  contract.
- `/Users/philipegermano/code/docker/docker-compose.yml` now provides an
  optional `quality` profile with `sonarqube + postgres`, isolated network,
  loopback-only exposure, `json-file` logs, and healthchecks; the compose stack
  is support infrastructure for the Docker MCP quality lane, not the baseline
  transport for the gateway itself.
- `/Users/philipegermano/code/config/mcp/docker-mcp-quality.yaml` keeps the
  `sonarqube` MCP lane out of the default `.mcp.json` baseline and allows
  targeted validation once the support stack and token are ready.
- `gmail-mcp` was evaluated for inbox automation but is not activated on this
  Apple Silicon machine because the published Docker image has no
  `linux/arm64` manifest and fails during gateway initialization.
- `figma` remains the official plugin/app-based integration outside the Docker
  MCP catalog on this host.
- `.codex/config.toml` keeps `figma` enabled via `https://mcp.figma.com/mcp`
  and `FIGMA_OAUTH_TOKEN`; that is the canonical route for prototyping and
  design-system work on this host.
- Atlassian MCP auth (atualizado 07/04/2026):
  - **Jira**: `jpglabs.atlassian.net/jira` — cloudId `d9f316a4-b4d8-40c9-a90a-0539675e39a1` — projeto SCRUM
  - **Confluence**: `jadergermano.atlassian.net/wiki` — cloudId `f2d06056-c0d3-4c77-af10-8c964f76218f` — space SD
  - MCP OAuth autorizado para Confluence; para Jira reconectar adicionando `jpglabs.atlassian.net`
- `sonarqube` remains optional because the MCP lane still depends on
  `sonarqube.token`; the local support stack is now provisioned in
  `docker/docker-compose.yml`, and the recommended MCP URL is
  `http://host.docker.internal:9000`.
- `/Users/philipegermano/code/config/mcp/bin/docker-mcp-gateway.sh mcp gateway run --dry-run --servers sonarqube`
  with `docker-mcp-quality.yaml` on `2026-04-12` listed `17 tools`, but the
  host still emitted `Secret 'sonarqube.token' not found`; keep SonarQube as an
  optional quality lane until the token is loaded and the local stack is
  healthy.
- `github` OAuth is now authorized in Docker MCP, but it is still outside the
  workspace `.mcp.json` baseline because GitHub connector coverage in this
  runtime is already richer through the app/plugin lane.
- `docker mcp gateway run --dry-run ... --servers github` on `2026-04-12`
  listed `26 tools`, but the host still warned that
  `github.personal_access_token` is missing; keep GitHub outside the shared
  baseline until that secret exists in the Docker MCP keychain.
- `semgrep` is authorized in Docker MCP on this host, but it remains outside
  the functional baseline because `dry-run` still fails during initialize with
  `Internal Server Error` after an OAuth token refresh, so no Semgrep tool can
  be treated as runtime-stable yet.
- `/Users/philipegermano/code/config/mcp/bin/docker-mcp-gateway.sh mcp gateway run --dry-run --servers semgrep`
  on `2026-04-12` still failed with
  `Can't start semgrep: failed to connect: calling "initialize": rejected by transport: sending "initialize": Internal Server Error`;
  Semgrep remains non-baseline on this host.
- `/Users/philipegermano/code/config/mcp/bin/docker-mcp-gateway.sh mcp gateway run --dry-run ... --servers semgrep`
  on `2026-04-05` listed the baseline tools successfully, but `semgrep`
  itself failed with `Can't start semgrep: failed to connect: calling
  "initialize": rejected by transport: sending "initialize": Internal Server Error`;
  keep Semgrep out of `.mcp.json` until this host/server combination stops
  flapping.
- `docker compose -f /Users/philipegermano/code/docker/docker-compose.yml --profile quality config`
  on `2026-04-05` failed because `SONARQUBE_JDBC_PASSWORD` is still absent and
  `/Users/philipegermano/code/docker/secrets/` currently holds only example
  files; the SonarQube lane is configured but not activatable yet.
- `youtube_transcript` is present in the Docker MCP catalog on this host and
  `docker mcp gateway run --dry-run --servers youtube_transcript` validated
  successfully on `2026-04-05`; it remains opt-in via `ENABLE_YOUTUBE_TRANSCRIPT_MCP=1`
  and the helper entrypoints `make video-info` / `make video-transcript`.
- `docker mcp server inspect youtube_transcript` on `2026-04-12` reconfirmed
  that the canonical server name uses underscore, not hyphen.
- The `youtube_transcript` lane is appropriate for tutorial reverse engineering
  and technical research, but it should not be treated as mission-critical:
  real executions can still receive `429` or anti-bot challenges from YouTube.
- `FIGMA_OAUTH_TOKEN` was not present in the shell environment observed during
  the `2026-04-05` revalidation session; the canonical Figma route remains the
  provider-native MCP entry in `/Users/philipegermano/.codex/config.toml`, but
  end-to-end validation still depends on a live token in the active runtime.

## Operational Support Stack

The shared Docker MCP gateway remains host-managed by Docker Desktop. The
compose stack under `/Users/philipegermano/code/docker/` only provisions
supporting infrastructure for heavier lanes that should not inflate the
baseline latency of every session.

- Default mode:
  - `COMPOSE_PROFILES` empty
  - no auxiliary services are started
  - `make bootstrap` validates only the stable MCP baseline
- Quality mode:
  - `COMPOSE_PROFILES=quality`
  - starts `postgres + sonarqube`
  - `bootstrap.sh` lifts the JDBC password from the Docker secret file into a
    transient environment variable only for the SonarQube container process,
    because the official image expects `SONAR_JDBC_PASSWORD`
  - `healthcheck.sh` validates both the HTTP health of SonarQube and the MCP
    `dry-run` for the `sonarqube` server when `ENABLE_SONARQUBE_MCP=1`
- Structural review mode:
  - `semgrep` becomes the primary optional lane for structural/static review
  - no dedicated config file is required, only OAuth plus explicit `dry-run`
  - `ast-grep` is intentionally absent because the server does not exist in the
    current catalog
- Research mode:
  - `youtube_transcript` stays outside the default `.mcp.json` baseline to keep
    coding sessions lean
  - `healthcheck.sh` validates the lane when `ENABLE_YOUTUBE_TRANSCRIPT_MCP=1`
  - `make video-info` and `make video-transcript` expose the lane through the
    canonical Docker MCP wrapper without custom scraping
  - callers must tolerate transient upstream throttling from YouTube and retry
    instead of treating the lane as a guaranteed dependency
- Figma mode:
  - stays outside Docker on this host
  - uses the provider runtime configuration via `FIGMA_OAUTH_TOKEN`

## Local OpenClaude + Ollama

Recommended implementation for a local-first coding runtime on this host:

1. Bootstrap the local provider with Ollama as primary:
   - `cd /Users/philipegermano/code/openclaude`
   - `bun run profile:init -- --provider ollama --goal coding`
   - `bun run dev:profile`
2. Keep OpenAI as the first cloud fallback when local inference is unavailable
   or economically unfit for the task:
   - `export OPENAI_API_KEY=...`
   - `bun run profile:init -- --provider openai --api-key "$OPENAI_API_KEY"`
   - `bun run dev:openai`
3. Use `bun run profile:auto -- --goal coding` only when you explicitly want
   best-effort switching between local `ollama` and cloud `openai`.

Practical rule:

- For local engineering work, keep `ollama` as the primary path and `openai`
  as the controlled online fallback, because `openclaude` already implements
  this failover path in `profile:init` and `dev:profile`.
- Add `anthropic` or `gemini` only as explicit secondary profiles after
  defining cost, latency, and credential policy; do not broaden the automatic
  fallback chain by default.
- `pi-local-app`, `piphone-ios`, `pibar-macos` e `PieCenter` foram descontinuados
  e arquivados; não há contrato de thin-client ou `cloudPriority` ativo a preservar.
- Workspace bootstrap helper:
  - `cp /Users/philipegermano/code/config/opencloud/opencloud-local.env.example /Users/philipegermano/code/config/opencloud/.env.local`
  - `set -a; . /Users/philipegermano/code/config/opencloud/.env.local; set +a`
  - `/Users/philipegermano/code/scripts/opencloud-local.sh status`
  - `/Users/philipegermano/code/scripts/opencloud-local.sh resolve`
  - `/Users/philipegermano/code/scripts/opencloud-local.sh bootstrap`
  - `/Users/philipegermano/code/scripts/opencloud-local.sh doctor`
  - `/Users/philipegermano/code/scripts/opencloud-local.sh launch`
- Dynamic mode:
  - `launch` resolve o provider a cada execucao, em vez de depender de um
    profile estatico persistido
  - o resolvedor grava um snapshot legivel por maquina em
    `/Users/philipegermano/code/config/opencloud/runtime-state.json`
  - isso aproxima o comportamento operacional do fluxo dinamico esperado nos
    runtimes tipo Claude Code e Codex: local primeiro, fallback controlado e
    decisao baseada no estado real do host

## Authentication Priority Matrix

Recommended order for software-engineering enablement on this host:

1. `semgrep`
   - Value: security review, code-quality scanning, and pre-implementation checks.
   - Current status: `docker mcp oauth ls` currently shows
     `semgrep | authorized`, but `dry-run` still fails during server
     initialization with `Internal Server Error`.
   - Required flow: reauthorize only if the token is suspected stale; the real
     gate is a clean `dry-run` with Semgrep tools exposed.
   - Practical rule: keep Semgrep out of the shared `.mcp.json` until OAuth is
     both healthy and the Docker MCP server passes `dry-run`.

2. `atlassian`
   - Value: make `Jira + Confluence` operational as the canonical execution and
     narrative surfaces for roadmap/spec work.
   - Required values:
     - `CONFLUENCE_URL`
     - `CONFLUENCE_USERNAME`
     - `CONFLUENCE_API_TOKEN` or `CONFLUENCE_PERSONAL_TOKEN`
     - `JIRA_URL`
     - `JIRA_USERNAME`
     - `JIRA_API_TOKEN` or `JIRA_PERSONAL_TOKEN`
   - Practical rule: high priority, but token-based; it cannot be completed by
     browser automation alone.

3. `sonarqube`
   - Value: code-quality metrics, issue tracking, quality gates, and PR quality
     visibility.
   - Local support stack:
     - `docker/docker-compose.yml` profile `quality`
     - `docker/secrets/sonarqube_db_password`
     - `docker/secrets/sonarqube.token`
   - MCP values:
     - `url: http://host.docker.internal:9000`
     - `org: local`
     - `docker mcp secret set sonarqube.token`
   - Practical rule: keep `sonarqube` outside the default `.mcp.json`; enable
     it only through the dedicated overlay after the local service and token are
     healthy.

4. `n8n`
   - Value: workflow automation for engineering support.
   - Current status: `n8n.api_url` is already configured in
     `config/mcp/docker-mcp-config.yaml`.
   - Missing secret:
     - `N8N_API_KEY`
   - Practical rule: low friction after the API key is available.

5. `notion`
   - Value: optional for Docker MCP only; low priority here because the Codex
     runtime already has a richer native Notion connector.
   - Required value:
     - `INTERNAL_INTEGRATION_TOKEN`

6. `grafana`, `dynatrace-mcp-server`, `firecrawl`
   - Value: useful, but not first-order priorities for the current roadmap
     slice.
   - Required values:
     - `grafana`: `GRAFANA_URL` + `GRAFANA_API_KEY`
     - `dynatrace-mcp-server`: `DT_ENVIRONMENT` + `OAUTH_CLIENT_ID` +
       `OAUTH_CLIENT_SECRET`
     - `firecrawl`: `FIRECRAWL_API_KEY` and optional `FIRECRAWL_API_URL`

## Browser-Based OAuth And What Was Actually Validated

- `docker mcp oauth ls` currently exposes:
  - `github | authorized`
  - `semgrep | authorized`
- `docker mcp oauth authorize github` is already complete for the current host.
- `docker mcp oauth authorize semgrep` is no longer the main blocker; the
  blocker is Semgrep failing to initialize cleanly after token refresh.
- Runtime validation on `2026-04-03` showed:
  - `github` OAuth is healthy at the Docker layer
- Conclusion:
  - OAuth authorization alone is not sufficient to treat a server as
    production-ready in the baseline
  - a server only enters the shared `.mcp.json` after dry-run validation passes
  - token-based servers like `atlassian`, `sonarqube`, `n8n`, `notion`,
    `grafana`, `dynatrace-mcp-server`, and `firecrawl` still require secrets
    generated or supplied outside the MCP browser flow

## Shared Memory Contract

- The canonical persistent memory for this workspace lives in the filesystem
  under `/Users/philipegermano/code/jpglabs/docs/memory/`.
- The Docker MCP `memory` server is a shared, provider-neutral derived layer
  backed by the Docker volume `shared-memory`.
- Source-of-truth order:
  1. `/Users/philipegermano/code/jpglabs/docs/memory/PI_MEMORY.md`
  2. `/Users/philipegermano/code/jpglabs/docs/memory/AGENTS.md`
  3. `/Users/philipegermano/code/jpglabs/docs/memory/sessions/`
  4. Docker MCP knowledge graph (`memory`)
- Practical rule:
  - session shutdown and service-backed sync should update the filesystem
    ledger first
  - the MCP graph should hold compact operational entities/relations for
    cross-provider discovery, not compete with the markdown ledger
- Drift policy:
  - if the graph is sparse or stale, reseed it from the canonical filesystem
    memory instead of treating the graph as authoritative

## Planning Contract

- `Jira` is the target canonical execution surface for task status, priority,
  and roadmap tracking.
- `Confluence` is the target canonical narrative surface for specs, roadmap
  mirrors, and design/engineering decisions.
- `Notion` remains restricted to the daily journal.
- Temporary exception approved by the user:
  until `2026-05-31`, keep operational updates mirrored in `Jira + Confluence`
  and `Notion` in parallel while the Atlassian lane is stabilized and the
  migration is completed. A formal keep-or-stop decision is required on
  `2026-05-31`.
- Until Jira becomes operational in this runtime, agents must surface the
  blocker explicitly instead of silently moving execution tracking back into
  `Notion`.

## Email Automation

- Recommended Docker MCP lane: `n8n` for orchestration plus `resend` for
  outbound notifications.
- For Gmail inbox automation, prefer Gmail nodes inside n8n or the native
  Gmail connector while `gmail-mcp` stays incompatible with this host.
- Workspace-scoped non-secret config lives in `config/mcp/docker-mcp-config.yaml`:
  - `n8n.api_url`
  - `resend.sender`
  - `resend.reply_to`
- Local quality overlay lives in `config/mcp/docker-mcp-quality.yaml`:
  - `sonarqube.url`
  - `sonarqube.org`
- Secrets should be stored in the Docker MCP keychain:
  - `docker mcp secret set n8n.api_key`
  - `docker mcp secret set resend.api_key`
  - `docker mcp secret set sonarqube.token`

## Notes

- This repository should remain small and documentation-focused.
- Workspace markdown should be classified and maintained from this repository.
