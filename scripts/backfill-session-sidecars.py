#!/usr/bin/env python3
"""Backfill JSON sidecars from existing docs session reports."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from session_close_support import (
    DEFAULT_DOCS_ROOT,
    DEFAULT_SCHEMA_PATH,
    build_report_context,
    build_sidecar_payload,
    parse_report,
)

DEFAULT_REPORT_GLOB = "projects/*/sessions/*/*/report.md"


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
    context = build_report_context(report_path=report_path, docs_root=docs_root)
    parsed = parse_report(context, status_default="partial")
    payload = build_sidecar_payload(parsed, imported=True)
    payload["$schema"] = str(DEFAULT_SCHEMA_PATH)
    return BackfillCandidate(
        report_path=report_path,
        sidecar_path=context.sidecar_path,
        payload=payload,
    )


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
