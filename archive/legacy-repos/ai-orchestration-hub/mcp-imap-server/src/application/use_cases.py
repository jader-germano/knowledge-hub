"""Application use cases — orchestrate domain ports, contain no framework logic.

Each use case:
- Depends only on domain abstractions (ports), never on infrastructure.
- Handles connection lifecycle (connect → execute → disconnect) reliably.
- Records an audit entry after every successful operation (LGPD compliance).
- Is a plain class — easy to unit-test with mocked ports.
"""

from __future__ import annotations

from datetime import datetime, timezone

from ..domain.entities import AuditEntry, FolderInfo, MessageBody, MessageEnvelope
from ..domain.ports import AuditLogger, ImapGateway


class FetchUnreadEmails:
    """Retrieve unread message envelopes from a mailbox folder.

    Returns lightweight envelopes (no body) — callers must use
    FetchMessageBody to get full content when needed.
    """

    def __init__(self, gateway: ImapGateway, audit: AuditLogger) -> None:
        self._gateway = gateway
        self._audit = audit

    def execute(self, folder: str = "INBOX", limit: int = 50) -> list[MessageEnvelope]:
        if limit < 1 or limit > 200:
            raise ValueError(f"limit must be between 1 and 200, got {limit}")

        self._gateway.connect()
        try:
            messages = self._gateway.search_messages(
                folder=folder,
                criteria="UNSEEN",
                limit=limit,
            )
            self._audit.log(
                AuditEntry(
                    timestamp=datetime.now(tz=timezone.utc),
                    action="fetch_unread",
                    folder=folder,
                    uids_affected=len(messages),
                )
            )
            return messages
        finally:
            self._gateway.disconnect()


class FetchMessageBody:
    """Retrieve the full body of a single message by UID.

    Fetches only plain-text and attachment metadata (no HTML blob exposed
    via MCP tools) to minimise accidental PII leakage.
    """

    def __init__(self, gateway: ImapGateway, audit: AuditLogger) -> None:
        self._gateway = gateway
        self._audit = audit

    def execute(self, folder: str, uid: int) -> MessageBody:
        if uid <= 0:
            raise ValueError(f"uid must be a positive integer, got {uid}")

        self._gateway.connect()
        try:
            body = self._gateway.fetch_body(folder=folder, uid=uid)
            self._audit.log(
                AuditEntry(
                    timestamp=datetime.now(tz=timezone.utc),
                    action="fetch_body",
                    folder=folder,
                    uids_affected=1,
                )
            )
            return body
        finally:
            self._gateway.disconnect()


class ListFolders:
    """Return all available mailbox folders."""

    def __init__(self, gateway: ImapGateway) -> None:
        self._gateway = gateway

    def execute(self) -> list[FolderInfo]:
        self._gateway.connect()
        try:
            return self._gateway.list_folders()
        finally:
            self._gateway.disconnect()
