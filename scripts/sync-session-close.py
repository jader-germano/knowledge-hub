#!/usr/bin/env python3
"""Sync canonical session closure artifacts from a report.md."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from session_close_support import (
    DEFAULT_BRIDGE_PATH,
    DEFAULT_DAILY_ROOT,
    DEFAULT_DOCS_ROOT,
    build_report_context,
    build_sidecar_payload,
    parse_report,
    render_bridge_block,
    render_daily_block,
    upsert_markdown_block,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Sync daily, AGENT_BRIDGE, JSON sidecar, and derived graph from a report.md.",
    )
    parser.add_argument("--report", required=True, type=Path, help="Absolute path to the report.md file.")
    parser.add_argument("--docs-root", type=Path, default=DEFAULT_DOCS_ROOT)
    parser.add_argument("--daily-path", type=Path, help="Override the daily markdown path.")
    parser.add_argument("--bridge-path", type=Path, default=DEFAULT_BRIDGE_PATH)
    parser.add_argument("--sidecar-path", type=Path, help="Override the output sidecar path.")
    parser.add_argument("--provider", help="Explicit provider override for the sidecar.")
    parser.add_argument("--timestamp", help="Explicit close timestamp override.")
    parser.add_argument(
        "--projector-mode",
        choices=("none", "dry-run", "apply"),
        default="apply",
        help="Whether to skip, dry-run, or apply the derived graph projection.",
    )
    parser.add_argument("--skip-daily", action="store_true", help="Do not sync the daily entry.")
    parser.add_argument("--skip-bridge", action="store_true", help="Do not sync AGENT_BRIDGE.")
    parser.add_argument("--skip-sidecar", action="store_true", help="Do not write the JSON sidecar.")
    parser.add_argument("--write", action="store_true", help="Persist the synchronized outputs.")
    return parser


def run_projector(docs_root: Path, sidecar_path: Path, mode: str) -> dict[str, Any]:
    if mode == "none":
        return {"status": "skipped"}

    command = [
        "python3",
        str(docs_root / "scripts/project-memory-graph.py"),
        "--sidecar",
        str(sidecar_path),
        "--apply" if mode == "apply" else "--dry-run",
    ]
    proc = subprocess.run(command, capture_output=True, text=True)
    result: dict[str, Any] = {
        "status": "applied" if mode == "apply" and proc.returncode == 0 else "planned",
        "command": command,
        "returncode": proc.returncode,
    }

    if proc.stdout.strip():
        try:
            result["result"] = json.loads(proc.stdout)
        except json.JSONDecodeError:
            result["stdout"] = proc.stdout.strip()
    if proc.stderr.strip():
        result["stderr"] = proc.stderr.strip()

    if proc.returncode != 0:
        result["status"] = "failed"
    return result


def main() -> int:
    args = build_parser().parse_args()
    docs_root = args.docs_root.resolve()
    context = build_report_context(
        report_path=args.report,
        docs_root=docs_root,
        daily_path=args.daily_path,
        bridge_path=args.bridge_path,
        sidecar_path=args.sidecar_path,
    )
    report = parse_report(
        context,
        provider_override=args.provider,
        timestamp_override=args.timestamp,
        status_default="completed",
    )
    payload = build_sidecar_payload(report, imported=False)

    daily_block = render_daily_block(report)
    bridge_block = render_bridge_block(report)
    lookup_tokens = [
        report.reported_session_id or "",
        report.context.session_id,
        str(report.context.report_path),
    ]

    summary: dict[str, Any] = {
        "mode": "write" if args.write else "dry-run",
        "report": str(report.context.report_path),
        "daily_path": str(report.context.daily_path),
        "bridge_path": str(report.context.bridge_path),
        "sidecar_path": str(report.context.sidecar_path),
        "session": {
            "id": report.context.session_id,
            "reported_session_id": report.reported_session_id,
            "timestamp": report.timestamp_iso,
            "provider": report.provider,
            "status": report.status,
        },
        "operations": [],
    }

    if not args.write:
        summary["daily_preview"] = None if args.skip_daily else daily_block
        summary["bridge_preview"] = None if args.skip_bridge else bridge_block
        summary["sidecar_preview"] = None if args.skip_sidecar else payload
        print(json.dumps(summary, indent=2))
        return 0

    if not args.skip_daily:
        existed_before = report.context.daily_path.exists()
        status, _ = upsert_markdown_block(
            report.context.daily_path,
            daily_block,
            marker_prefix="session-sync",
            session_id=report.context.session_id,
            lookup_tokens=lookup_tokens,
            create_header=f"# Daily Summary - {report.date}",
        )
        summary["operations"].append(
            {
                "target": str(report.context.daily_path),
                "kind": "daily",
                "status": "created" if not existed_before else status,
            }
        )

    if not args.skip_bridge:
        existed_before = report.context.bridge_path.exists()
        status, _ = upsert_markdown_block(
            report.context.bridge_path,
            bridge_block,
            marker_prefix="session-bridge",
            session_id=report.context.session_id,
            lookup_tokens=lookup_tokens,
        )
        summary["operations"].append(
            {
                "target": str(report.context.bridge_path),
                "kind": "bridge",
                "status": "created" if not existed_before else status,
            }
        )

    if not args.skip_sidecar:
        existed_before = report.context.sidecar_path.exists()
        report.context.sidecar_path.parent.mkdir(parents=True, exist_ok=True)
        report.context.sidecar_path.write_text(json.dumps(payload, indent=2) + "\n")
        summary["operations"].append(
            {
                "target": str(report.context.sidecar_path),
                "kind": "sidecar",
                "status": "created" if not existed_before else "updated",
            }
        )

    if not args.skip_sidecar:
        summary["graph_sync"] = run_projector(docs_root, report.context.sidecar_path, args.projector_mode)
    else:
        summary["graph_sync"] = {"status": "skipped", "reason": "sidecar emission skipped"}

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
