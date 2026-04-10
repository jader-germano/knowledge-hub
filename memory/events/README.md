# Memory Events

This namespace stores the machine-readable sidecars that complement canonical
Markdown session closure.

## Rules

- one JSON file per closed session or durable operational event
- store files under `memory/events/<yyyy-mm-dd>/`
- keep filenames stable and derived from `session.id`
- keep data compact, explicit, and rebuild-friendly
- never treat this directory as a replacement for `report.md` or `daily/`

## Naming

Recommended filename:

```text
memory/events/<yyyy-mm-dd>/<session-id>.json
```

Example:

```text
memory/events/2026-04-06/docs-memory-hybrid-sidecar-projector.json
```

## Canonical Close Flow

For a new or updated `report.md`, use:

```bash
python3 /Users/philipegermano/code/jpglabs/docs/scripts/sync-session-close.py \
  --report /Users/philipegermano/code/jpglabs/docs/projects/<repo>/sessions/<feature-id>/<yyyy-mm-dd-session>/report.md \
  --write
```

This command:

- syncs the corresponding `daily/<yyyy-mm-dd>.md` entry
- syncs a concise `AGENT_BRIDGE.md` handoff entry
- emits or updates the JSON sidecar under `memory/events/`
- attempts to project the sidecar into the derived graph

## Projection

Bootstrap legacy session reports into sidecars with:

```bash
python3 /Users/philipegermano/code/jpglabs/docs/scripts/backfill-session-sidecars.py
python3 /Users/philipegermano/code/jpglabs/docs/scripts/backfill-session-sidecars.py --write
```

Then project sidecars into the derived Docker MCP graph with:

```bash
python3 /Users/philipegermano/code/jpglabs/docs/scripts/project-memory-graph.py --dry-run
python3 /Users/philipegermano/code/jpglabs/docs/scripts/project-memory-graph.py --apply
```

If the graph projection fails, do not delete or rewrite the sidecar. Fix the
runtime and re-run the projector.
