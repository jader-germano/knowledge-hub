#!/usr/bin/env python3
"""Project JPGLabs session sidecars into the derived Docker MCP memory graph."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


DEFAULT_DOCS_ROOT = Path("/Users/philipegermano/code/jpglabs/docs")
DEFAULT_SIDECAR_GLOB = "memory/events/**/*.json"
DEFAULT_SCHEMA_PATH = DEFAULT_DOCS_ROOT / "memory/schemas/session-memory-sidecar.schema.json"
DEFAULT_GATEWAY_COMMAND = [
    "/Users/philipegermano/code/config/mcp/bin/docker-mcp-gateway.sh",
    "mcp",
    "gateway",
    "run",
    "--additional-catalog",
    "/Users/philipegermano/code/config/mcp/docker-mcp-shared-catalog.yaml",
    "--servers",
    "memory",
    "--additional-config",
    "/Users/philipegermano/code/config/mcp/docker-mcp-config.yaml",
]


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def stable_text(prefix: str, value: str | None) -> str | None:
    if not value:
        return None
    return f"{prefix}: {value}"


def observation_key(observation: str) -> str:
    if ":" not in observation:
        return observation
    return observation.split(":", 1)[0].strip()


@dataclass
class EntityRecord:
    name: str
    entity_type: str
    observations: set[str] = field(default_factory=set)
    managed_keys: set[str] = field(default_factory=set)


@dataclass(frozen=True)
class RelationRecord:
    source: str
    relation_type: str
    target: str


@dataclass
class ProjectionPlan:
    entities: dict[str, EntityRecord] = field(default_factory=dict)
    relations: set[RelationRecord] = field(default_factory=set)
    sidecar_paths: list[Path] = field(default_factory=list)

    def add_entity(
        self,
        name: str,
        entity_type: str,
        observations: list[str],
        managed_keys: list[str] | None = None,
    ) -> None:
        record = self.entities.get(name)
        if record is None:
            record = EntityRecord(name=name, entity_type=entity_type)
            self.entities[name] = record
        elif record.entity_type != entity_type:
            raise ValueError(
                f"Entity type mismatch for {name}: {record.entity_type} != {entity_type}"
            )
        if managed_keys:
            record.managed_keys.update(managed_keys)
        for observation in observations:
            if observation:
                record.observations.add(observation)
                record.managed_keys.add(observation_key(observation))

    def add_relation(self, source: str, relation_type: str, target: str) -> None:
        self.relations.add(RelationRecord(source=source, relation_type=relation_type, target=target))


def validate_sidecar(data: dict[str, Any], path: Path) -> list[str]:
    errors: list[str] = []

    def expect(condition: bool, message: str) -> None:
        if not condition:
            errors.append(f"{path}: {message}")

    expect(data.get("schema_version") == "1.0", "schema_version must be 1.0")

    session = data.get("session")
    expect(isinstance(session, dict), "session must be an object")
    if isinstance(session, dict):
        for key in ("id", "timestamp", "date", "provider", "workspace", "status", "summary"):
            expect(isinstance(session.get(key), str) and session.get(key), f"session.{key} is required")
        expect(session.get("status") in {"completed", "partial", "blocked"}, "session.status is invalid")

    projects = data.get("projects")
    expect(isinstance(projects, list) and len(projects) > 0, "projects must be a non-empty array")
    if isinstance(projects, list):
        for index, project in enumerate(projects):
            expect(isinstance(project, dict), f"projects[{index}] must be an object")
            if isinstance(project, dict):
                for key in ("id", "name", "path"):
                    expect(
                        isinstance(project.get(key), str) and project.get(key),
                        f"projects[{index}].{key} is required",
                    )

    artifacts = data.get("artifacts")
    expect(isinstance(artifacts, dict), "artifacts must be an object")
    if isinstance(artifacts, dict):
        for key in ("report", "daily"):
            expect(isinstance(artifacts.get(key), str) and artifacts.get(key), f"artifacts.{key} is required")

    for list_name in ("tags", "files_touched"):
        if list_name in data:
            expect(isinstance(data[list_name], list), f"{list_name} must be an array")

    for list_name in ("decisions", "findings", "next_actions", "commands"):
        if list_name in data:
            expect(isinstance(data[list_name], list), f"{list_name} must be an array")

    return errors


def load_sidecars(docs_root: Path, explicit_paths: list[Path]) -> list[tuple[Path, dict[str, Any]]]:
    sidecar_paths = explicit_paths or sorted(docs_root.glob(DEFAULT_SIDECAR_GLOB))
    loaded: list[tuple[Path, dict[str, Any]]] = []
    errors: list[str] = []

    for path in sidecar_paths:
        if path.name == "README.md":
            continue
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            errors.append(f"{path}: invalid JSON: {exc}")
            continue
        errors.extend(validate_sidecar(data, path))
        loaded.append((path, data))

    if errors:
        raise SystemExit("Sidecar validation failed:\n- " + "\n- ".join(errors))

    return loaded


def build_projection(sidecars: list[tuple[Path, dict[str, Any]]]) -> ProjectionPlan:
    plan = ProjectionPlan()

    for path, sidecar in sidecars:
        plan.sidecar_paths.append(path)
        session = sidecar["session"]
        artifacts = sidecar["artifacts"]
        projects = sidecar["projects"]
        tags = sorted({tag.strip() for tag in sidecar.get("tags", []) if tag.strip()})

        session_name = f"session:{session['id']}"
        plan.add_entity(
            name=session_name,
            entity_type="session",
            observations=[
                stable_text("Timestamp", session["timestamp"]),
                stable_text("Date", session["date"]),
                stable_text("Provider", session["provider"]),
                stable_text("Workspace", session["workspace"]),
                stable_text("Status", session["status"]),
                stable_text("Feature", session.get("feature_id")),
                stable_text("Summary", session["summary"]),
                stable_text("Report", artifacts["report"]),
                stable_text("Daily", artifacts["daily"]),
                stable_text("Evidence dir", artifacts.get("evidence_dir")),
                stable_text("Tags", ", ".join(tags) if tags else None),
            ],
            managed_keys=[
                "Timestamp",
                "Date",
                "Provider",
                "Workspace",
                "Status",
                "Feature",
                "Summary",
                "Report",
                "Daily",
                "Evidence dir",
                "Tags",
                "Files touched",
                "Commands",
            ],
        )

        for project in projects:
            project_name = f"project:{project['id']}"
            plan.add_entity(
                name=project_name,
                entity_type="project",
                observations=[
                    stable_text("Name", project["name"]),
                    stable_text("Path", project["path"]),
                    stable_text("Role", project.get("role")),
                ],
                managed_keys=["Name", "Path", "Role"],
            )
            plan.add_relation(session_name, "touches", project_name)

        for tag in tags:
            tag_name = f"tag:{slugify(tag)}"
            plan.add_entity(
                name=tag_name,
                entity_type="tag",
                observations=[stable_text("Label", tag)],
                managed_keys=["Label"],
            )
            plan.add_relation(session_name, "references", tag_name)

        for field_name, entity_type, relation_type in (
            ("decisions", "decision", "records"),
            ("findings", "finding", "captures"),
            ("next_actions", "action", "plans"),
        ):
            for item in sidecar.get(field_name, []):
                item_name = f"{entity_type}:{session['id']}:{item['id']}"
                plan.add_entity(
                    name=item_name,
                    entity_type=entity_type,
                    observations=[
                        stable_text("Summary", item["summary"]),
                        stable_text("Status", item.get("status")),
                        stable_text("Rationale", item.get("rationale")),
                    ],
                    managed_keys=["Summary", "Status", "Rationale"],
                )
                plan.add_relation(session_name, relation_type, item_name)
                for project_id in item.get("project_ids", []):
                    plan.add_relation(item_name, "impacts", f"project:{project_id}")

    return plan


class McpClient:
    def __init__(self, command: list[str]) -> None:
        self.command = command
        self.proc: subprocess.Popen[bytes] | None = None
        self._request_id = 0

    def __enter__(self) -> "McpClient":
        self.proc = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False,
            bufsize=0,
            env=os.environ.copy(),
        )
        self._initialize()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.proc is None:
            return
        if self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait(timeout=5)

    def _initialize(self) -> None:
        response = self._request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "jpglabs-memory-projector",
                    "version": "1.0",
                },
            },
        )
        if "error" in response:
            raise RuntimeError(f"MCP initialize failed: {response['error']}")
        self._notify("notifications/initialized", {})

    def _notify(self, method: str, params: dict[str, Any]) -> None:
        self._send({"jsonrpc": "2.0", "method": method, "params": params})

    def _request(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        self._request_id += 1
        request_id = self._request_id
        self._send(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "method": method,
                "params": params,
            }
        )
        while True:
            response = self._recv()
            if "method" in response and "id" not in response:
                continue
            if response.get("id") != request_id:
                raise RuntimeError(f"Unexpected MCP response id: {response}")
            return response

    def _send(self, payload: dict[str, Any]) -> None:
        if self.proc is None or self.proc.stdin is None:
            raise RuntimeError("MCP client is not connected")
        body = (json.dumps(payload, ensure_ascii=True) + "\n").encode("utf-8")
        # Docker MCP gateway stdio on this host reads newline-delimited JSON-RPC
        # payloads instead of Content-Length framed messages.
        self.proc.stdin.write(body)
        self.proc.stdin.flush()

    def _recv(self, timeout: int = 30) -> dict[str, Any]:
        if self.proc is None or self.proc.stdout is None:
            raise RuntimeError("MCP client is not connected")
        start = time.time()
        while True:
            if time.time() - start > timeout:
                raise TimeoutError("Timed out while waiting for MCP response")
            line = self.proc.stdout.readline()
            if not line:
                raise RuntimeError(self._closed_message("stdout closed before response"))
            stripped = line.decode("utf-8", "replace").strip()
            if not stripped:
                continue
            try:
                return json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise RuntimeError(f"Invalid JSON-RPC response from gateway: {stripped}") from exc

    def _closed_message(self, prefix: str) -> str:
        if self.proc is None or self.proc.stderr is None:
            return prefix
        rc = self.proc.poll()
        stderr = self.proc.stderr.read().decode("utf-8", "replace")
        return f"{prefix}; rc={rc}; stderr={stderr}"

    def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        response = self._request("tools/call", {"name": name, "arguments": arguments})
        if "error" in response:
            raise RuntimeError(f"MCP tools/call failed for {name}: {response['error']}")
        return unwrap_tool_result(response["result"])


def unwrap_tool_result(result: dict[str, Any]) -> Any:
    if "structuredContent" in result:
        return result["structuredContent"]
    if "content" in result:
        text_fragments = [
            item.get("text", "")
            for item in result["content"]
            if isinstance(item, dict) and item.get("type") == "text"
        ]
        if text_fragments:
            text = "".join(text_fragments).strip()
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return text
    return result


def batched(items: list[Any], size: int) -> list[list[Any]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def sync_plan(plan: ProjectionPlan, command: list[str]) -> dict[str, Any]:
    created_entities = 0
    deleted_observations = 0
    added_observations = 0
    created_relations = 0

    with McpClient(command) as client:
        graph = client.call_tool("read_graph", {})
        existing_entities = {
            item["name"]: set(item.get("observations", [])) for item in graph.get("entities", [])
        }
        existing_relations = {
            (item["from"], item["relationType"], item["to"]) for item in graph.get("relations", [])
        }

        missing_entities = []
        observation_deletes = []
        observation_delta = []
        for entity in plan.entities.values():
            current = existing_entities.get(entity.name)
            if current is None:
                missing_entities.append(
                    {
                        "name": entity.name,
                        "entityType": entity.entity_type,
                        "observations": sorted(entity.observations),
                    }
                )
            else:
                stale = sorted(
                    item
                    for item in current
                    if observation_key(item) in entity.managed_keys and item not in entity.observations
                )
                if stale:
                    observation_deletes.append(
                        {"entityName": entity.name, "observations": stale}
                    )
                missing = sorted(entity.observations - current)
                if missing:
                    observation_delta.append(
                        {"entityName": entity.name, "contents": missing}
                    )

        missing_relations = [
            {
                "from": relation.source,
                "relationType": relation.relation_type,
                "to": relation.target,
            }
            for relation in sorted(
                plan.relations, key=lambda item: (item.source, item.relation_type, item.target)
            )
            if (relation.source, relation.relation_type, relation.target) not in existing_relations
        ]

        for chunk in batched(missing_entities, 25):
            client.call_tool("create_entities", {"entities": chunk})
            created_entities += len(chunk)

        for chunk in batched(observation_deletes, 25):
            client.call_tool("delete_observations", {"deletions": chunk})
            deleted_observations += sum(len(item["observations"]) for item in chunk)

        for chunk in batched(observation_delta, 25):
            client.call_tool("add_observations", {"observations": chunk})
            added_observations += sum(len(item["contents"]) for item in chunk)

        for chunk in batched(missing_relations, 50):
            client.call_tool("create_relations", {"relations": chunk})
            created_relations += len(chunk)

    return {
        "created_entities": created_entities,
        "deleted_observations": deleted_observations,
        "added_observations": added_observations,
        "created_relations": created_relations,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Project JPGLabs memory sidecars into the Docker MCP memory graph."
    )
    parser.add_argument(
        "--docs-root",
        type=Path,
        default=DEFAULT_DOCS_ROOT,
        help="Docs root that contains memory/events and schemas.",
    )
    parser.add_argument(
        "--sidecar",
        action="append",
        type=Path,
        default=[],
        help="Explicit sidecar path. Can be passed multiple times.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the projection plan without touching the Docker MCP graph.",
    )
    mode.add_argument(
        "--apply",
        action="store_true",
        help="Apply the projection to the Docker MCP memory graph.",
    )
    parser.add_argument(
        "--gateway-command",
        nargs="+",
        help="Override the gateway command used for MCP stdio.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    docs_root = args.docs_root.resolve()
    schema_path = docs_root / "memory/schemas/session-memory-sidecar.schema.json"
    if schema_path != DEFAULT_SCHEMA_PATH and not schema_path.exists():
        parser.error(f"Schema file not found: {schema_path}")

    sidecars = load_sidecars(docs_root, [path.resolve() for path in args.sidecar])
    if not sidecars:
        print("No sidecars found.", file=sys.stderr)
        return 1

    plan = build_projection(sidecars)

    summary = {
        "sidecars": [str(path) for path in plan.sidecar_paths],
        "entity_count": len(plan.entities),
        "relation_count": len(plan.relations),
        "entities": sorted(plan.entities.keys()),
        "relations": [
            {"from": item.source, "relationType": item.relation_type, "to": item.target}
            for item in sorted(plan.relations, key=lambda item: (item.source, item.relation_type, item.target))
        ],
    }

    if not args.apply:
        print(json.dumps({"mode": "dry-run", **summary}, indent=2))
        return 0

    command = args.gateway_command or DEFAULT_GATEWAY_COMMAND
    result = sync_plan(plan, command)
    print(json.dumps({"mode": "apply", **summary, "sync": result}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
