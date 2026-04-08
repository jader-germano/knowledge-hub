# Memory Events Contract

## Purpose

This workspace uses a hybrid memory model:

- Markdown remains the canonical, human-auditable source of truth.
- JSON sidecars provide a stable machine-readable write path.
- The Docker MCP `memory` graph is a derived projection for discovery.

This contract exists to make session closure and memory sync:

- provider-neutral
- rebuildable
- easy to diff in Git
- safe to operate when the graph layer is degraded

## Canonical Order

When a session closes, the write path is mandatory and ordered:

1. update the canonical Markdown artifacts
2. emit one JSON sidecar under `memory/events/`
3. project the sidecar into the Docker MCP `memory` graph

If step 3 fails, the session is still considered closed as long as steps 1 and 2
completed successfully. The graph is an index, not the ledger.

## Directory Layout

```text
memory/
├── EVENTS_CONTRACT.md
├── README.md
├── events/
│   └── <yyyy-mm-dd>/
│       └── <session-id>.json
└── schemas/
    └── session-memory-sidecar.schema.json
```

## Sidecar Scope

Each JSON sidecar represents one closed session or one durable operational event
that is important enough to be discoverable across providers.

Each sidecar must reference the canonical Markdown surfaces that explain the
event in human terms:

- the project session report in `projects/<repo>/sessions/.../report.md`
- the daily journal entry in `/Users/philipegermano/code/daily/<yyyy-mm-dd>.md`

The sidecar does not replace those documents. It complements them.

## Required Sidecar Content

Each sidecar must carry, at minimum:

- stable `schema_version`
- stable `session.id`
- close timestamp
- provider name
- workspace path
- short summary
- at least one project reference
- artifact paths for `report` and `daily`

Optional but recommended sections:

- `tags`
- `decisions`
- `findings`
- `next_actions`
- `files_touched`
- `commands`

## Projection Rules

The projector must stay intentionally conservative.

It should create compact graph entities for:

- sessions
- projects
- tags
- decisions
- findings
- next actions

It should not project:

- raw secrets
- access tokens
- browser session data
- full transcripts
- large prompt bodies
- arbitrary file contents
- volatile audit trails such as full command histories and file inventories

The graph should store operational facts only, such as:

- what session happened
- which projects it touched
- which decisions were recorded
- which findings remained open
- where the canonical Markdown report lives

## Idempotence

The projector must be idempotent.

Practical rules:

- entity names are deterministic
- relation triples are deterministic
- repeated runs must not duplicate nodes
- repeated runs may add only missing observations
- the graph may be deleted and rebuilt from the sidecars at any time

## Failure Semantics

If the projector cannot reach the Docker MCP gateway:

- do not treat the sidecar as invalid
- do not block session closure
- mark the graph sync as stale or pending in the session report
- rerun the projector later from the same sidecar set

## Security And Privacy

This lane is secure-by-default only if the sidecars stay compact.

Do not place in sidecars:

- API keys
- OAuth tokens
- bearer tokens
- passwords
- LGPD-sensitive personal data without operational need
- raw customer payloads

Prefer references to canonical files over copying sensitive content into the
graph.

## Recommended Workflow

```bash
python3 /Users/philipegermano/code/jpglabs/docs/scripts/sync-session-close.py \
  --report /Users/philipegermano/code/jpglabs/docs/projects/<repo>/sessions/<feature-id>/<yyyy-mm-dd-session>/report.md \
  --write
```

Legacy import and curation workflow:

```bash
python3 /Users/philipegermano/code/jpglabs/docs/scripts/backfill-session-sidecars.py
python3 /Users/philipegermano/code/jpglabs/docs/scripts/backfill-session-sidecars.py --write
python3 /Users/philipegermano/code/jpglabs/docs/scripts/project-memory-graph.py --apply
```

## Decision

For this workspace, the recommended architecture is:

- Markdown as the canonical human ledger
- JSON sidecars as the canonical machine write path
- Docker MCP `memory` as a derived, disposable discovery layer
