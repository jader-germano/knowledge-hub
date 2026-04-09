"""Domain ports — abstract interfaces following Dependency Inversion Principle (DIP).

All infrastructure must implement these interfaces.
Domain layer has ZERO dependencies on external libraries.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from .entities import (
    AuditEntry,
    EmailAddress,
    FolderInfo,
    MessageBody,
    MessageEnvelope,
)


class ImapGateway(ABC):
    """Port for IMAP server communication (Infrastructure adapter required)."""

    @abstractmethod
    def connect(self) -> None:
        """Establish connection and authenticate."""

    @abstractmethod
    def disconnect(self) -> None:
        """Close connection gracefully."""

    @abstractmethod
    def list_folders(self) -> list[FolderInfo]:
        """List all available mailbox folders."""

    @abstractmethod
    def search_messages(
        self,
        folder: str = "INBOX",
        criteria: str = "UNSEEN",
        limit: int = 50,
    ) -> list[MessageEnvelope]:
        """Search messages by IMAP criteria. Returns envelopes (no body)."""

    @abstractmethod
    def fetch_body(self, folder: str, uid: int) -> MessageBody:
        """Fetch full message body by UID."""

    @abstractmethod
    def mark_as_read(self, folder: str, uids: list[int]) -> int:
        """Mark messages as read. Returns count of messages affected."""

    @abstractmethod
    def mark_as_unread(self, folder: str, uids: list[int]) -> int:
        """Mark messages as unread. Returns count of messages affected."""

    @abstractmethod
    def move_message(self, folder: str, uid: int, destination: str) -> bool:
        """Move a message to another folder. Returns success."""

    @abstractmethod
    def delete_message(self, folder: str, uid: int) -> bool:
        """Mark message as deleted (soft delete). Returns success."""

    @abstractmethod
    def flag_message(self, folder: str, uid: int, flag: str) -> bool:
        """Add a flag to a message. Returns success."""

    @abstractmethod
    def unflag_message(self, folder: str, uid: int, flag: str) -> bool:
        """Remove a flag from a message. Returns success."""


class AuditLogger(ABC):
    """Port for LGPD-compliant audit logging."""

    @abstractmethod
    def log(self, entry: AuditEntry) -> None:
        """Record an audit entry. Must NOT contain PII."""

    @abstractmethod
    def get_entries(
        self,
        since: datetime | None = None,
        action: str | None = None,
        limit: int = 100,
    ) -> list[AuditEntry]:
        """Retrieve audit entries with optional filters."""


class CredentialStore(ABC):
    """Port for secure credential retrieval. Never hardcode secrets."""

    @abstractmethod
    def get_host(self) -> str:
        """IMAP server hostname."""

    @abstractmethod
    def get_port(self) -> int:
        """IMAP server port."""

    @abstractmethod
    def get_username(self) -> str:
        """IMAP username (email address)."""

    @abstractmethod
    def get_password(self) -> str:
        """IMAP password (app-specific password for iCloud)."""

    @abstractmethod
    def use_ssl(self) -> bool:
        """Whether to use SSL/TLS."""
