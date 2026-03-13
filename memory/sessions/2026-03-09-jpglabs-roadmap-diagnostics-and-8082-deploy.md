# Session Memory - 2026-03-09 - JPGLabs Roadmap, Diagnostics, and 8082 Deploy

## Context
Operational review and product-structure pass across the JPGLabs stack, with focus on dashboard improvements, portfolio/documentation depth, VPS visibility, n8n pending configuration, task decomposition by agent, and deployment parity on port `8082`.

## Implemented In `jpglabs-portfolio`
- Added an interactive roadmap board to the hub in `src/components/RoadmapBoard.tsx` and `src/data/roadmap.ts`.
- Added a dedicated `Roadmap` tab in `src/pages/Hub.tsx`.
- Expanded portfolio experience entries with:
  - delivered solutions
  - repository sources
  - versioned technology references
- Added centralized documentation metadata in `src/data/documentation.ts` for:
  - JPGLabs repositories
  - official docs links tied to concrete stack versions
- Added/normalized mock access users in `src/context/AuthContext.tsx`:
  - `jader@jpglabs.com.br`
  - `consultant@jpglabs.com.br`
  - `ops@jpglabs.com.br`
  - `client@jpglabs.com.br`
- Changed local Docker host exposure from `8080` to `8082` in `docker-compose.yml`.

## Validation Completed
- `npm run build`: pass
- `npm run lint`: pass
- Local Docker runtime: pass on `http://127.0.0.1:8082`
- VPS deploy: portfolio rebuilt and exposed on `0.0.0.0:8082->80`
- VPS served bundle updated to the new build, including `index-u8IiHvEI.js`

## VPS / DNS / Edge Findings
- `jpglabs.com.br` is behind Cloudflare name servers:
  - `dane.ns.cloudflare.com`
  - `ingrid.ns.cloudflare.com`
- `n8n.jpglabs.com.br` resolves directly to VPS `187.77.227.151`
- Mail routing and baseline records exist:
  - MX configured
  - SPF present
  - DMARC present
- Mail service ports were listening on the VPS:
  - `25`
  - `143`
  - `465`
  - `587`
  - `993`

## Active VPS Services Confirmed
- `jpglabs-portfolio`
- `n8n-n8n-1`
- `open-webui`
- `ollama`
- `n8n-traefik-1`
- `mailserver`

## Active n8n Workflows Confirmed
- `WhatsApp Chatbot - Assistente Philipe`
- `JPGLabs - Modern AI Engineer Toolkit Delivery`
- `JPGLabs [v2] - Social & Sales Hub`
- `JPGLabs [Health Check] - Infrastructure Monitor`
- `AI Guardian — System Cleanup`
- `JPGLabs [Growth] - AI Lead Hunter`
- `JPGLabs [SECURE] - Kiwify Delivery`

## Documentation / Ops Findings
- Current ops repo remains `~/code/jpglabs`.
- Current assets repo remains `~/code/jpglabs-ai-assets`.
- There is workflow drift in `~/code/jpglabs/n8n-workflows`; canonical workflow set needs consolidation.
- `~/code/jpglabs/docs/vps-setup.md` currently exposes a Cloudflare token and needs sanitization plus token rotation.
- Existing n8n `.env.example` does not yet document all required runtime keys.

## Pending Keys / Config Still Not Formalized
- `KIWIFY_DELIVERY_API_KEY`
- `KIWIFY_DELIVERY_ENDPOINT`
- `WHATSAPP_WEBHOOK_SECRET`
- `SLACK_WEBHOOK_URL`
- review of all n8n workflow-specific secrets before publishing any unified docs repo

## Open Infrastructure Issues
- `https://jpglabs.com.br` still returns `404` through Cloudflare and needs edge/router correction.
- `https://n8n.jpglabs.com.br` still shows an SSL chain problem and needs certificate-chain correction in the current edge path.
- Cloudflare configuration should be treated as an active work item, not as already closed.

## Product / Delivery Structure Decided
- Agent-task decomposition was formalized in the roadmap with these owners:
  - `Agent Atlas`
  - `Agent Mercury`
  - `Agent Scribe`
  - `Agent Edge`
  - `Agent Flow`
  - `Agent Forge`
  - `Agent Babel`
  - `Agent Gate`
  - `Agent Cortex`
  - `Agent Reactor`
  - `Agent Launch`
- PT/EN/ES support, docs-repo consolidation, private PDF repo split, LLM reassessment, and scalable backend work were recorded as roadmap items, not completed work.

## Architecture Note
- User clarified the target architecture on 2026-03-10.
- Keep the current Node backend active and evolve it with reactive/evented scaling patterns.
- Open a separate Java/WebFlux repository as a replica service behind the same load balancer.
- Maintain both services in parity for contract changes and showcase use cases.
- The next priority after systems stabilization and documentation is the mobile app consuming the load-balanced Node + Java edge.

## Operating Guidance For Next Session
- Fix the Cloudflare apex `404` and `n8n` certificate chain before treating the public stack as production-ready.
- Sanitize secrets from docs before repo consolidation.
- Build the unified documentation repo only after defining canonical workflow files and pending secret placeholders.
- Implement PT/EN/ES only after the content model is finalized, otherwise translation work will drift with documentation changes.
