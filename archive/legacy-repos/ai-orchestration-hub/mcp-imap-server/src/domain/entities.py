"""Domain entities — pure data objects, no framework dependencies."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class MailboxFolder(Enum):
    INBOX = "INBOX"
    SENT = "Sent Messages"
    DRAFTS = "Drafts"
    TRASH = "Deleted Messages"
    JUNK = "Junk"
    ARCHIVE = "Archive"


class MessageFlag(Enum):
    SEEN = r"\Seen"
    ANSWERED = r"\Answered"
    FLAGGED = r"\Flagged"
    DELETED = r"\Deleted"
    DRAFT = r"\Draft"


@dataclass(frozen=True)
class EmailAddress:
    name: str
    address: str

    @staticmethod
    def parse(raw: str) -> EmailAddress:
        """Parse 'Name <email@domain>' or bare 'email@domain'."""
        import re
        match = re.match(r'"?([^"<]*)"?\s*<([^>]+)>', raw.strip())
        if match:
            return EmailAddress(name=match.group(1).strip(), address=match.group(2).strip())
        return EmailAddress(name="", address=raw.strip())

    @property
    def domain(self) -> str:
        parts = self.address.split("@")
        return parts[1].lower() if len(parts) == 2 else ""

    def __str__(self) -> str:
        return f"{self.name} <{self.address}>" if self.name else self.address


@dataclass(frozen=True)
class MessageEnvelope:
    """Lightweight message metadata (no body loaded)."""
    uid: int
    message_id: str
    subject: str
    sender: EmailAddress
    recipients: list[EmailAddress]
    date: datetime | None
    flags: list[str]
    folder: str
    size: int = 0

    @property
    def is_read(self) -> bool:
        return MessageFlag.SEEN.value in self.flags

    @property
    def is_flagged(self) -> bool:
        return MessageFlag.FLAGGED.value in self.flags


@dataclass(frozen=True)
class MessageBody:
    """Full message content."""
    uid: int
    text_plain: str = ""
    text_html: str = ""
    has_attachments: bool = False
    attachment_names: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class FolderInfo:
    """IMAP folder metadata."""
    name: str
    delimiter: str
    flags: list[str]
    total_messages: int = 0
    unread_messages: int = 0


@dataclass(frozen=True)
class AuditEntry:
    """Immutable audit record — no PII stored (LGPD)."""
    timestamp: datetime
    action: str
    folder: str
    uids_affected: int
    details: str = ""
