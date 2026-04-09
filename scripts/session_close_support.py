#!/usr/bin/env python3
"""Shared helpers for session closure sync and sidecar generation."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_DOCS_ROOT = Path("/Users/philipegermano/code/jpglabs/docs")
DEFAULT_DAILY_ROOT = Path("/Users/philipegermano/code/daily")
DEFAULT_BRIDGE_PATH = DEFAULT_DOCS_ROOT / "agents/AGENT_BRIDGE.md"
DEFAULT_SCHEMA_PATH = DEFAULT_DOCS_ROOT / "memory/schemas/session-memory-sidecar.schema.json"


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def strip_wrapping_code(value: str) -> str:
    stripped = value.strip()
    if stripped.startswith("`") and stripped.endswith("`") and len(stripped) >= 2:
        return stripped[1:-1]
    return stripped


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
        if not stripped:
            continue
        return re.sub(r"^(?:-|\d+\.)\s+", "", stripped)
    return None


def parse_metadata_items(items: list[str]) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for item in items:
        if ":" not in item:
            continue
        key, value = item.split(":", 1)
        normalized_key = strip_wrapping_code(key.strip()).lower()
        metadata[normalized_key] = strip_wrapping_code(value.strip())
    return metadata


def extract_metadata_value(metadata: dict[str, str], *keys: str) -> str | None:
    lowered = {key.lower(): value for key, value in metadata.items()}
    for key in keys:
        value = lowered.get(key.lower())
        if value:
            return value
    return None


def normalize_status(raw_status: str | None, default: str = "completed") -> str:
    if not raw_status:
        return default
    lowered = raw_status.lower()
    if any(token in lowered for token in ("blocked", "bloque")):
        return "blocked"
    if any(
        token in lowered
        for token in (
            "hipótese",
            "hipotese",
            "não aprovada",
            "nao aprovada",
            "pending",
            "pendente",
            "partial",
            "parcial",
            "imported",
        )
    ):
        return "partial"
    return "completed"


def normalize_timestamp(raw_value: str | None, fallback_date: str) -> str:
    cleaned = strip_wrapping_code(raw_value or "").strip()
    if not cleaned:
        return f"{fallback_date}T00:00:00-03:00"
    cleaned = cleaned.replace("`", "")
    if cleaned.endswith("Z"):
        cleaned = cleaned[:-1] + "+00:00"

    formats = (
        "%Y-%m-%d %H:%M:%S %z",
        "%Y-%m-%d %H:%M %z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M%z",
        "%Y-%m-%d",
    )
    for fmt in formats:
        try:
            parsed = datetime.strptime(cleaned, fmt)
        except ValueError:
            continue
        if fmt == "%Y-%m-%d":
            return f"{parsed:%Y-%m-%d}T00:00:00-03:00"
        return parsed.isoformat()
    raise ValueError(f"Unsupported timestamp format: {raw_value}")


def format_timestamp_display(timestamp_iso: str) -> str:
    parsed = datetime.fromisoformat(timestamp_iso)
    return parsed.strftime("%Y-%m-%d %H:%M:%S %z")


def parse_command_records(section_text: str) -> list[dict[str, str]]:
    commands: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    current_key: str | None = None

    for raw_line in section_text.splitlines():
        line = raw_line.rstrip()
        command_match = re.match(r"^\s*-\s+(`.+?`|.+)$", line)
        field_match = re.match(r"^\s*-\s*(Action|Result):\s*(.*)$", line)

        if command_match and not field_match:
            if current and all(current.values()):
                commands.append(current)
            current = {
                "command": strip_wrapping_code(command_match.group(1).strip()),
                "action": "",
                "result": "",
            }
            current_key = None
            continue

        if current is None:
            continue

        if field_match:
            current_key = field_match.group(1).lower()
            current[current_key] = field_match.group(2).strip()
            continue

        if current_key and (line.startswith("  ") or line.startswith("\t")) and line.strip():
            current[current_key] = f"{current[current_key]} {line.strip()}".strip()

    if current and all(current.values()):
        commands.append(current)
    return commands


def clean_path_items(items: list[str]) -> list[str]:
    cleaned: list[str] = []
    for item in items:
        normalized = strip_wrapping_code(item)
        if normalized and normalized not in cleaned:
            cleaned.append(normalized)
    return cleaned


def filter_placeholder_next_actions(items: list[str]) -> list[str]:
    placeholders = (
        "nenhuma ação adicional",
        "nenhuma acao adicional",
        "no further action",
        "none",
    )
    filtered: list[str] = []
    for item in items:
        lowered = item.strip().lower()
        if any(lowered.startswith(prefix) for prefix in placeholders):
            continue
        filtered.append(item)
    return filtered


def infer_timestamp_from_daily(
    daily_path: Path,
    tokens: list[str],
    fallback_date: str,
) -> str | None:
    if not daily_path.exists():
        return None

    lines = daily_path.read_text().splitlines()
    candidate_indexes: list[int] = []
    nonempty_tokens = [token for token in tokens if token]
    for index, line in enumerate(lines):
        if any(token in line for token in nonempty_tokens):
            candidate_indexes.append(index)

    timestamp_patterns = (
        re.compile(r"Timestamp completo do fechamento:\s*`?([^`]+)`?"),
        re.compile(r"^##\s+(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [+-]\d{4})\s+—"),
        re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [+-]\d{4})$"),
    )

    for index in candidate_indexes:
        lower_bound = max(0, index - 120)
        for cursor in range(index, lower_bound - 1, -1):
            line = lines[cursor].strip()
            for pattern in timestamp_patterns:
                match = pattern.search(line)
                if match:
                    return normalize_timestamp(match.group(1), fallback_date)
    return None


@dataclass(frozen=True)
class ReportContext:
    docs_root: Path
    report_path: Path
    project_id: str
    feature_dir: str
    session_dir: str
    session_date: str
    session_id: str
    daily_path: Path
    bridge_path: Path
    sidecar_path: Path
    evidence_dir: Path


@dataclass
class ParsedReport:
    context: ReportContext
    raw_text: str
    sections: dict[str, str]
    metadata: dict[str, str]
    reported_session_id: str | None
    timestamp_iso: str
    timestamp_display: str
    date: str
    workspace: str
    provider: str
    status: str
    branch: str | None
    objective: str | None
    summary_items: list[str]
    summary_text: str
    decision_items: list[str]
    finding_items: list[str]
    next_action_items: list[str]
    handoff_items: list[str]
    files_created: list[str]
    files_modified: list[str]
    files_touched: list[str]
    commands: list[dict[str, str]]


def build_report_context(
    report_path: Path,
    docs_root: Path = DEFAULT_DOCS_ROOT,
    daily_path: Path | None = None,
    bridge_path: Path | None = None,
    sidecar_path: Path | None = None,
) -> ReportContext:
    resolved_report = report_path.resolve()
    relative = resolved_report.relative_to(docs_root)
    # projects/<project_id>/sessions/<feature_dir>/<session_dir>/report.md
    _, project_id, _, feature_dir, session_dir, _ = relative.parts
    session_date = session_dir.replace("-session", "")
    session_id = f"{project_id}-{feature_dir}-{session_dir}"

    resolved_daily = (daily_path or DEFAULT_DAILY_ROOT / f"{session_date}.md").resolve()
    resolved_bridge = (bridge_path or DEFAULT_BRIDGE_PATH).resolve()
    resolved_sidecar = (
        sidecar_path or docs_root / "memory/events" / session_date / f"{session_id}.json"
    ).resolve()

    return ReportContext(
        docs_root=docs_root.resolve(),
        report_path=resolved_report,
        project_id=project_id,
        feature_dir=feature_dir,
        session_dir=session_dir,
        session_date=session_date,
        session_id=session_id,
        daily_path=resolved_daily,
        bridge_path=resolved_bridge,
        sidecar_path=resolved_sidecar,
        evidence_dir=resolved_report.parent,
    )


def parse_report(
    context: ReportContext,
    *,
    provider_override: str | None = None,
    timestamp_override: str | None = None,
    status_default: str = "completed",
) -> ParsedReport:
    raw_text = context.report_path.read_text()
    sections = parse_sections(raw_text)
    metadata = parse_metadata_items(parse_list_items(sections.get("Session Metadata", "")))

    reported_session_id = extract_metadata_value(
        metadata,
        "feature/session id",
        "feature id",
        "session id",
    )

    date = (
        extract_metadata_value(metadata, "data", "date", "session date")
        or context.session_date
    )
    tokens = [
        reported_session_id or "",
        context.session_id,
        context.feature_dir,
        str(context.report_path),
    ]
    timestamp_iso = normalize_timestamp(
        timestamp_override
        or extract_metadata_value(
            metadata,
            "timestamp completo do fechamento",
            "timestamp completo",
            "timestamp",
            "timestamp completo do report",
        )
        or infer_timestamp_from_daily(context.daily_path, tokens, date),
        date,
    )
    timestamp_display = format_timestamp_display(timestamp_iso)

    workspace = (
        extract_metadata_value(
            metadata,
            "repositório",
            "repositorio",
            "repository",
            "workspace",
            "workspace afetado",
        )
        or "/Users/philipegermano/code"
    )
    provider = provider_override or extract_metadata_value(metadata, "provider", "provedor") or "unknown"
    branch = extract_metadata_value(metadata, "branch ativa", "branch", "active branch")
    objective = extract_metadata_value(
        metadata,
        "objetivo aprovado",
        "objetivo",
        "scope",
        "foco",
    )
    status = normalize_status(extract_metadata_value(metadata, "status"), default=status_default)

    summary_items = parse_list_items(sections.get("Summary", ""))
    summary_text = (
        " | ".join(summary_items[:2])
        if summary_items
        else (
            first_nonempty_line(sections.get("Summary", ""))
            or first_nonempty_line(sections.get("Recomendação Final", ""))
            or first_nonempty_line(sections.get("Decisão Recomendada", ""))
            or first_nonempty_line(sections.get("Problem Statement", ""))
            or f"Session report for {context.feature_dir}."
        )
    )

    decision_items = (
        parse_list_items(sections.get("Decision", ""))
        or parse_list_items(sections.get("Decisão Recomendada", ""))
        or parse_list_items(sections.get("Recomendação Final", ""))
    )
    if not decision_items:
        recommendation = first_nonempty_line(sections.get("Recomendação Final", ""))
        if recommendation:
            decision_items = [recommendation]

    finding_items = (
        parse_list_items(sections.get("Risks And Gaps", ""))
        or parse_list_items(sections.get("Riscos", ""))
    )
    next_action_items = filter_placeholder_next_actions(
        parse_list_items(sections.get("Next Actions", ""))
    )
    handoff_items = parse_list_items(sections.get("Handoff Notes", ""))

    files_created = clean_path_items(parse_list_items(sections.get("Files Created", "")))
    files_modified = clean_path_items(parse_list_items(sections.get("Files Modified", "")))
    files_touched = clean_path_items(
        parse_list_items(sections.get("Files Touched", "")) + files_created + files_modified
    )
    commands = parse_command_records(sections.get("Commands Executed", ""))

    return ParsedReport(
        context=context,
        raw_text=raw_text,
        sections=sections,
        metadata=metadata,
        reported_session_id=reported_session_id,
        timestamp_iso=timestamp_iso,
        timestamp_display=timestamp_display,
        date=date,
        workspace=workspace,
        provider=provider,
        status=status,
        branch=branch,
        objective=objective,
        summary_items=summary_items,
        summary_text=summary_text,
        decision_items=decision_items,
        finding_items=finding_items,
        next_action_items=next_action_items,
        handoff_items=handoff_items,
        files_created=files_created,
        files_modified=files_modified,
        files_touched=files_touched,
        commands=commands,
    )


def make_named_records(
    items: list[str],
    prefix: str,
    project_id: str,
    *,
    status: str,
    rationale: str | None = None,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for item in items:
        record = {
            "id": f"{prefix}-{slugify(item)[:48]}",
            "summary": item,
            "status": status,
            "project_ids": [project_id],
        }
        if rationale:
            record["rationale"] = rationale
        records.append(record)
    return records


def build_sidecar_payload(
    report: ParsedReport,
    *,
    imported: bool = False,
) -> dict[str, Any]:
    tags = {report.context.project_id, report.context.feature_dir, "session-report"}
    if imported:
        tags.add("imported")

    findings = []
    if imported:
        findings.append(
            {
                "id": "legacy-import",
                "summary": "Imported from a legacy Markdown report. Timestamp and provider may be approximate and should be curated if higher fidelity is required.",
                "status": "imported",
                "project_ids": [report.context.project_id],
            }
        )
    findings.extend(
        make_named_records(
            report.finding_items,
            "risk",
            report.context.project_id,
            status="open" if imported else "recorded",
        )
    )

    payload = {
        "$schema": str(DEFAULT_SCHEMA_PATH),
        "schema_version": "1.0",
        "session": {
            "id": report.context.session_id,
            "timestamp": report.timestamp_iso,
            "date": report.date,
            "provider": report.provider,
            "workspace": report.workspace,
            "status": report.status,
            "feature_id": report.context.feature_dir,
            "summary": report.summary_text,
        },
        "projects": [
            {
                "id": report.context.project_id,
                "name": f"jpglabs/{report.context.project_id}",
                "path": str(
                    report.context.docs_root
                    if report.context.project_id == "docs"
                    else report.context.docs_root.parent / report.context.project_id
                ),
                "role": "imported from legacy session report"
                if imported
                else "canonical session report owner",
            }
        ],
        "artifacts": {
            "report": str(report.context.report_path),
            "daily": str(report.context.daily_path),
            "evidence_dir": str(report.context.evidence_dir),
        },
        "tags": sorted(tags),
        "decisions": make_named_records(
            report.decision_items,
            "decision" if not imported else "imported",
            report.context.project_id,
            status="recorded" if not imported else "imported",
        ),
        "findings": findings,
        "next_actions": make_named_records(
            report.next_action_items,
            "next-action" if not imported else "imported",
            report.context.project_id,
            status="open" if not imported else "imported",
        ),
        "files_touched": report.files_touched,
        "commands": report.commands,
    }

    session_payload = payload["session"]
    if report.reported_session_id:
        session_payload["reported_session_id"] = report.reported_session_id
    if report.branch:
        session_payload["branch"] = report.branch
    if report.objective:
        session_payload["objective"] = report.objective

    return payload


def render_daily_block(report: ParsedReport) -> str:
    label = report.reported_session_id or report.context.session_id
    body = report.raw_text.strip()
    body = re.sub(r"^# .*\n+", "", body, count=1)
    return (
        f"<!-- session-sync:{report.context.session_id}:start -->\n"
        f"## {report.timestamp_display} - {label}\n\n"
        f"{body}\n"
        f"<!-- session-sync:{report.context.session_id}:end -->\n"
    )


def render_bridge_block(report: ParsedReport) -> str:
    title = report.context.feature_dir.replace("-", " ")
    summary_items = report.summary_items or [report.summary_text]
    risk_items = report.finding_items or ["Nenhum risco adicional registrado nesta sessão."]
    next_actions = report.next_action_items or ["Nenhuma ação adicional ficou pendente nesta sessão."]
    handoff_items = report.handoff_items or ["Preservar o report e o sidecar como fontes desta sessão."]

    lines = [
        f"<!-- session-bridge:{report.context.session_id}:start -->",
        f"## {report.date} — {title}",
        "",
        "### Session Metadata",
        "",
        f"- Timestamp completo do fechamento: `{report.timestamp_display}`",
        f"- Feature/session id: `{report.reported_session_id or report.context.session_id}`",
        f"- Repositório: `{report.workspace}`",
    ]
    if report.branch:
        lines.append(f"- Branch ativa: `{report.branch}`")
    if report.provider != "unknown":
        lines.append(f"- Provider: `{report.provider}`")
    if report.objective:
        lines.append(f"- Objetivo aprovado: {report.objective}")

    lines.extend(["", "### Summary", ""])
    lines.extend([f"- {item}" for item in summary_items])

    lines.extend(["", "### Risks And Gaps", ""])
    lines.extend([f"- {item}" for item in risk_items])

    lines.extend(["", "### Next Actions", ""])
    lines.extend([f"- {item}" for item in next_actions])

    lines.extend(["", "### Handoff Notes", ""])
    lines.extend([f"- {item}" for item in handoff_items])
    lines.append(f"<!-- session-bridge:{report.context.session_id}:end -->")
    lines.append("")
    return "\n".join(lines)


def find_existing_block_span(text: str, tokens: list[str]) -> tuple[int, int] | None:
    lines = text.splitlines(keepends=True)
    nonempty_tokens = [token for token in tokens if token]
    if not nonempty_tokens:
        return None

    char_offsets: list[int] = []
    offset = 0
    for line in lines:
        char_offsets.append(offset)
        offset += len(line)

    for index, line in enumerate(lines):
        if not any(token in line for token in nonempty_tokens):
            continue
        start_index = index
        while start_index > 0 and not lines[start_index].startswith("## "):
            start_index -= 1
        if not lines[start_index].startswith("## "):
            start_index = 0

        end_index = len(lines)
        for cursor in range(index + 1, len(lines)):
            if lines[cursor].startswith("## "):
                end_index = cursor
                break
        return (char_offsets[start_index], char_offsets[end_index] if end_index < len(char_offsets) else len(text))
    return None


def upsert_markdown_block(
    path: Path,
    block: str,
    *,
    marker_prefix: str,
    session_id: str,
    lookup_tokens: list[str],
    create_header: str | None = None,
) -> tuple[str, Path]:
    start_marker = f"<!-- {marker_prefix}:{session_id}:start -->"
    end_marker = f"<!-- {marker_prefix}:{session_id}:end -->"

    if path.exists():
        original = path.read_text()
    else:
        original = f"{create_header}\n\n" if create_header else ""

    marker_pattern = re.compile(
        rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}\n?",
        re.DOTALL,
    )
    if marker_pattern.search(original):
        updated = marker_pattern.sub(block, original)
    else:
        span = find_existing_block_span(original, lookup_tokens)
        if span:
            updated = f"{original[:span[0]].rstrip()}\n\n{block}\n{original[span[1]:].lstrip()}"
        else:
            separator = "" if not original or original.endswith("\n\n") else "\n\n"
            updated = f"{original}{separator}{block}"

    path.parent.mkdir(parents=True, exist_ok=True)
    if updated != original:
        path.write_text(updated)
        return ("updated" if path.exists() else "created", path)
    return ("unchanged", path)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())
