#!/usr/bin/env python3
"""Backfill JSON sidecars from existing docs session reports."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_DOCS_ROOT = Path("/Users/philipegermano/code/jpglabs/docs")
DEFAULT_REPORT_GLOB = "projects/*/sessions/*/*/report.md"
DEFAULT_SCHEMA_PATH = DEFAULT_DOCS_ROOT / "memory/schemas/session-memory-sidecar.schema.json"


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def parse_sections(markdown: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = "_root"
    sections[current] = []
    for line in markdown.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
            continue
        sections.setdefault(current, []).append(line)
    return {name: "\n".join(lines).strip() for name, lines in sections.items()}


def parse_list_items(section_text: str) -> list[str]:
    items: list[str] = []
    current: str | None = None
    for raw_line in section_text.splitlines():
        line = raw_line.rstrip()
        match = re.match(r"^\s*(?:-|\d+\.)\s+(.*)$", line)
        if match:
            if current:
                items.append(current.strip())
            current = match.group(1).strip()
            continue
        if current and (line.startswith("  ") or line.startswith("\t")):
            current += " " + line.strip()
            continue
        if current and not line.strip():
            items.append(current.strip())
            current = None
            continue
        if current and line.strip():
            current += " " + line.strip()
    if current:
        items.append(current.strip())
    return items


def first_nonempty_line(section_text: str) -> str | None:
    for line in section_text.splitlines():
        stripped = line.strip()
        if stripped:
            stripped = re.sub(r"^(?:-|\d+\.)\s+", "", stripped)
            return stripped
    return None


def parse_metadata_items(items: list[str]) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for item in items:
        if ":" not in item:
            continue
        key, value = item.split(":", 1)
        metadata[key.strip().lower()] = value.strip()
    return metadata


def normalize_status(raw_status: str | None) -> str:
    if not raw_status:
        return "partial"
    lowered = raw_status.lower()
    if any(token in lowered for token in ("blocked", "bloque")):
        return "blocked"
    if any(token in lowered for token in ("hipótese", "hipotese", "não aprovada", "nao aprovada", "pending", "pendente", "partial", "parcial")):
        return "partial"
    return "completed"


@dataclass
class BackfillCandidate:
    report_path: Path
    sidecar_path: Path
    payload: dict[str, Any]


def load_existing_report_map(docs_root: Path) -> dict[str, Path]:
    existing: dict[str, Path] = {}
    for sidecar_path in docs_root.glob("memory/events/**/*.json"):
        if sidecar_path.name == "README.md":
            continue
        try:
            payload = json.loads(sidecar_path.read_text())
        except json.JSONDecodeError:
            continue
        artifacts = payload.get("artifacts", {})
        report_path = artifacts.get("report")
        if isinstance(report_path, str) and report_path:
            existing[report_path] = sidecar_path
    return existing


def build_candidate(docs_root: Path, report_path: Path) -> BackfillCandidate:
    relative = report_path.relative_to(docs_root)
    # projects/<project_id>/sessions/<feature_id>/<session_dir>/report.md
    _, project_id, _, feature_id, session_dir, _ = relative.parts
    session_date = session_dir.replace("-session", "")
    session_id = f"{project_id}-{feature_id}-{session_dir}"
    sidecar_path = docs_root / "memory" / "events" / session_date / f"{session_id}.json"

    sections = parse_sections(report_path.read_text())
    metadata = parse_metadata_items(parse_list_items(sections.get("Session Metadata", "")))

    summary_items = parse_list_items(sections.get("Summary", ""))
    if summary_items:
        summary = " | ".join(summary_items[:2])
    else:
        summary = (
            first_nonempty_line(sections.get("Summary", ""))
            or first_nonempty_line(sections.get("Recomendação Final", ""))
            or first_nonempty_line(sections.get("Decisão Recomendada", ""))
            or first_nonempty_line(sections.get("Problem Statement", ""))
            or f"Imported session report for {feature_id}."
        )

    next_action_items = parse_list_items(sections.get("Next Actions", ""))
    risk_items = (
        parse_list_items(sections.get("Risks And Gaps", ""))
        or parse_list_items(sections.get("Riscos", ""))
    )

    decision_items = (
        parse_list_items(sections.get("Decisão Recomendada", ""))
        or parse_list_items(sections.get("Recomendação Final", ""))
        or parse_list_items(sections.get("Decision", ""))
    )
    if not decision_items:
        recommendation_line = first_nonempty_line(sections.get("Recomendação Final", ""))
        if recommendation_line:
            decision_items = [recommendation_line]

    files_touched = []
    for section_name in ("Files Touched", "Files Created", "Files Modified"):
        files_touched.extend(parse_list_items(sections.get(section_name, "")))

    payload = {
        "$schema": str(DEFAULT_SCHEMA_PATH),
        "schema_version": "1.0",
        "session": {
            "id": session_id,
            "timestamp": f"{session_date}T00:00:00-03:00",
            "date": session_date,
            "provider": "unknown",
            "workspace": "/Users/philipegermano/code",
            "status": normalize_status(metadata.get("status")),
            "feature_id": feature_id,
            "summary": summary,
        },
        "projects": [
            {
                "id": project_id,
                "name": f"jpglabs/{project_id}",
                "path": str(docs_root if project_id == "docs" else docs_root.parent / project_id),
                "role": "imported from legacy session report",
            }
        ],
        "artifacts": {
            "report": str(report_path),
            "daily": f"/Users/philipegermano/code/daily/{session_date}.md",
            "evidence_dir": str(report_path.parent),
        },
        "tags": sorted({"imported", "session-report", project_id, feature_id}),
        "findings": [
            {
                "id": "legacy-import",
                "summary": "Imported from a legacy Markdown report. Timestamp and provider may be approximate and should be curated if higher fidelity is required.",
                "status": "imported",
                "project_ids": [project_id],
            }
        ],
        "next_actions": [
            {
                "id": f"imported-{slugify(action)[:48]}",
                "summary": action,
                "status": "imported",
                "project_ids": [project_id],
            }
            for action in next_action_items
        ],
        "decisions": [
            {
                "id": f"imported-{slugify(item)[:48]}",
                "summary": item,
                "status": "imported",
                "project_ids": [project_id],
            }
            for item in decision_items
        ],
        "files_touched": files_touched,
        "commands": [],
    }

    if risk_items:
        payload["findings"].extend(
            {
                "id": f"risk-{slugify(item)[:48]}",
                "summary": item,
                "status": "open",
                "project_ids": [project_id],
            }
            for item in risk_items
        )

    return BackfillCandidate(report_path=report_path, sidecar_path=sidecar_path, payload=payload)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Backfill sidecars from legacy session reports.")
    parser.add_argument("--docs-root", type=Path, default=DEFAULT_DOCS_ROOT)
    parser.add_argument("--report", action="append", type=Path, default=[])
    parser.add_argument("--write", action="store_true", help="Write the generated sidecars.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing generated sidecars.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    docs_root = args.docs_root.resolve()

    report_paths = [path.resolve() for path in args.report] or sorted(docs_root.glob(DEFAULT_REPORT_GLOB))
    existing_report_map = load_existing_report_map(docs_root)

    candidates: list[BackfillCandidate] = []
    skipped_existing: list[dict[str, str]] = []
    for report_path in report_paths:
        existing_sidecar = existing_report_map.get(str(report_path))
        if existing_sidecar and not args.overwrite:
            skipped_existing.append({"report": str(report_path), "sidecar": str(existing_sidecar)})
            continue
        candidates.append(build_candidate(docs_root, report_path))

    if args.write:
        for candidate in candidates:
            candidate.sidecar_path.parent.mkdir(parents=True, exist_ok=True)
            candidate.sidecar_path.write_text(json.dumps(candidate.payload, indent=2) + "\n")

    print(
        json.dumps(
            {
                "mode": "write" if args.write else "dry-run",
                "reports_scanned": len(report_paths),
                "generated": [
                    {
                        "report": str(candidate.report_path),
                        "sidecar": str(candidate.sidecar_path),
                        "summary": candidate.payload["session"]["summary"],
                        "status": candidate.payload["session"]["status"],
                    }
                    for candidate in candidates
                ],
                "skipped_existing": skipped_existing,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
