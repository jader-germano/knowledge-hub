"""MCP server entry point — exposes IMAP email tools via Model Context Protocol.

Tool surface:
  search_messages  → unread envelopes (no body)
  fetch_message    → plain-text body, capped at 5 KB for token safety
  list_folders     → available mailbox folders

Credential resolution order (highest priority first)
─────────────────────────────────────────────────────
  1. KeychainCredentialStore  — macOS Keychain + Touch ID gate (preferred)
  2. EnvCredentialStore       — ICLOUD_EMAIL + ICLOUD_APP_PASSWORD env vars (CI/fallback)

Run setup once before using with Keychain:
  uv run mcp-imap-setup

Privacy / LGPD:
  - No message content is persisted beyond the tool call lifetime.
  - Body text is truncated before being returned to the LLM.
  - HTML bodies are never exposed (plain-text only).
"""

from __future__ import annotations

import logging

from mcp.server.fastmcp import FastMCP

from ..application.use_cases import FetchMessageBody, FetchUnreadEmails, ListFolders
from ..domain.ports import CredentialStore
from ..infrastructure.audit_logger import InMemoryAuditLogger
from ..infrastructure.imap_adapter import ImapClientAdapter

logger = logging.getLogger(__name__)

# ── MCP server ────────────────────────────────────────────────────────────────

mcp = FastMCP(
    "icloud-mail",
    description=(
        "IMAP email access for iCloud (and any IMAP server). "
        "Credentials stored in macOS Keychain, protected by Touch ID. "
        "Provides read-only message listing and body retrieval. LGPD-compliant."
    ),
)

_audit = InMemoryAuditLogger()
_BODY_CHAR_LIMIT = 5_000  # ~1.25 K tokens — keeps context manageable


# ── Credential resolution ─────────────────────────────────────────────────────


def _resolve_credentials() -> CredentialStore:
    """Return the best available credential store.

    Prefers Keychain (with Touch ID) over env vars.
    Env vars are kept as a fallback for non-interactive / CI contexts.
    """
    # 1. Try Keychain (macOS-native, Touch ID)
    try:
        from ..infrastructure.keychain_store import KeychainCredentialStore

        if KeychainCredentialStore.is_enrolled():
            return KeychainCredentialStore()
    except Exception as exc:
        logger.warning("Keychain unavailable (%s), falling back to env vars.", exc)

    # 2. Fallback: env vars
    from ..infrastructure.credential_store import EnvCredentialStore

    return EnvCredentialStore()


def _make_gateway() -> ImapClientAdapter:
    return ImapClientAdapter(_resolve_credentials())


# ── Tools ─────────────────────────────────────────────────────────────────────


@mcp.tool()
def search_messages(folder: str = "INBOX", limit: int = 50) -> list[dict]:
    """List unread messages in a mailbox folder.

    Returns lightweight envelopes — no body content is fetched.
    Use fetch_message(uid, folder) when you need the full text.

    Args:
        folder: IMAP folder name. Defaults to INBOX.
        limit:  Maximum messages to return (1–50).
    """
    capped = max(1, min(limit, 50))
    envelopes = FetchUnreadEmails(_make_gateway(), _audit).execute(
        folder=folder, limit=capped
    )
    return [
        {
            "uid": e.uid,
            "subject": e.subject,
            "from_name": e.sender.name,
            "from_address": e.sender.address,
            "date": e.date.isoformat() if e.date else None,
            "is_read": e.is_read,
            "size_bytes": e.size,
            "folder": e.folder,
        }
        for e in envelopes
    ]


@mcp.tool()
def fetch_message(uid: int, folder: str = "INBOX") -> dict:
    """Fetch the plain-text body of a message by its UID.

    Body is truncated at 5 000 characters. HTML is never returned.

    Args:
        uid:    IMAP unique identifier (from search_messages).
        folder: IMAP folder that contains the message. Defaults to INBOX.
    """
    body = FetchMessageBody(_make_gateway(), _audit).execute(folder=folder, uid=uid)
    return {
        "uid": body.uid,
        "text": body.text_plain[:_BODY_CHAR_LIMIT],
        "truncated": len(body.text_plain) > _BODY_CHAR_LIMIT,
        "has_attachments": body.has_attachments,
        "attachment_names": body.attachment_names,
    }


@mcp.tool()
def list_folders() -> list[dict]:
    """List all available mailbox folders on the IMAP server."""
    folders = ListFolders(_make_gateway()).execute()
    return [{"name": f.name, "flags": f.flags} for f in folders]


# ── Entry point ───────────────────────────────────────────────────────────────


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
