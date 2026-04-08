"""In-memory AuditLogger — LGPD-compliant, zero PII.

Design decisions:
- Stores only action metadata (what happened, when, how many UIDs).
- No message subjects, senders, bodies or addresses are ever stored here.
- Capped at MAX_ENTRIES to prevent unbounded memory growth across long runs.
- Thread-safe via a simple lock (MCP servers can be called concurrently).
"""

from __future__ import annotations

import threading
from datetime import datetime, timezone

from ..domain.entities import AuditEntry
from ..domain.ports import AuditLogger

MAX_ENTRIES = 500


class InMemoryAuditLogger(AuditLogger):
    """Bounded in-memory ring buffer for audit entries.

    Entries are dropped (oldest first) when MAX_ENTRIES is reached.
    """

    def __init__(self, max_entries: int = MAX_ENTRIES) -> None:
        self._entries: list[AuditEntry] = []
        self._max = max_entries
        self._lock = threading.Lock()

    def log(self, entry: AuditEntry) -> None:
        with self._lock:
            self._entries.append(entry)
            if len(self._entries) > self._max:
                self._entries = self._entries[-self._max :]

    def get_entries(
        self,
        since: datetime | None = None,
        action: str | None = None,
        limit: int = 100,
    ) -> list[AuditEntry]:
        with self._lock:
            entries = list(self._entries)

        if since is not None:
            since_utc = since.replace(tzinfo=timezone.utc) if since.tzinfo is None else since
            entries = [e for e in entries if e.timestamp >= since_utc]

        if action is not None:
            entries = [e for e in entries if e.action == action]

        return entries[-limit:]
