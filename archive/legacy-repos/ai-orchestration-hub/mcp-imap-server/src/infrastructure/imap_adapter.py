"""ImapClientAdapter — imapclient-based implementation of ImapGateway.

Responsibilities:
- Open/close authenticated IMAP connections (context-manager safe).
- Translate low-level imapclient responses into clean domain entities.
- NEVER expose raw byte sequences or library types outside this module.

Security notes:
- SSL is always preferred; disable only via explicit env var.
- Credentials come exclusively via CredentialStore (no literals here).
- Message bodies are read-only by default (readonly=True on select_folder).
"""

from __future__ import annotations

import email as email_lib
from datetime import datetime
from typing import Any

import imapclient

from ..domain.entities import EmailAddress, FolderInfo, MessageBody, MessageEnvelope
from ..domain.ports import CredentialStore, ImapGateway


class ImapClientAdapter(ImapGateway):
    """Concrete IMAP adapter using the imapclient library."""

    def __init__(self, credentials: CredentialStore) -> None:
        self._creds = credentials
        self._client: imapclient.IMAPClient | None = None

    # ------------------------------------------------------------------
    # Connection lifecycle
    # ------------------------------------------------------------------

    def connect(self) -> None:
        self._client = imapclient.IMAPClient(
            self._creds.get_host(),
            port=self._creds.get_port(),
            ssl=self._creds.use_ssl(),
        )
        self._client.login(self._creds.get_username(), self._creds.get_password())

    def disconnect(self) -> None:
        if self._client is not None:
            try:
                self._client.logout()
            except Exception:
                pass
            finally:
                self._client = None

    # ------------------------------------------------------------------
    # Folder operations
    # ------------------------------------------------------------------

    def list_folders(self) -> list[FolderInfo]:
        self._require_connected()
        result: list[FolderInfo] = []
        for flags, delimiter, name in self._client.list_folders():  # type: ignore[union-attr]
            result.append(
                FolderInfo(
                    name=self._decode(name),
                    delimiter=self._decode(delimiter) if delimiter else "/",
                    flags=[self._decode(f) for f in flags],
                )
            )
        return result

    # ------------------------------------------------------------------
    # Message search
    # ------------------------------------------------------------------

    def search_messages(
        self,
        folder: str = "INBOX",
        criteria: str = "UNSEEN",
        limit: int = 50,
    ) -> list[MessageEnvelope]:
        self._require_connected()
        self._client.select_folder(folder, readonly=True)  # type: ignore[union-attr]

        uids: list[int] = list(self._client.search([criteria]))  # type: ignore[union-attr]
        if not uids:
            return []

        uids = uids[-limit:]  # most recent N
        raw_data = self._client.fetch(uids, ["ENVELOPE", "FLAGS", "RFC822.SIZE"])  # type: ignore[union-attr]

        envelopes: list[MessageEnvelope] = []
        for uid, msg_data in raw_data.items():
            envelope = msg_data.get(b"ENVELOPE")
            if envelope is None:
                continue

            sender = (
                self._parse_address(envelope.from_[0])
                if envelope.from_
                else EmailAddress(name="", address="")
            )
            subject = self._decode(envelope.subject) if envelope.subject else "(no subject)"
            flags = [self._decode(f) for f in msg_data.get(b"FLAGS", [])]
            date: datetime | None = (
                envelope.date if isinstance(envelope.date, datetime) else None
            )

            envelopes.append(
                MessageEnvelope(
                    uid=uid,
                    message_id=self._decode(envelope.message_id) if envelope.message_id else "",
                    subject=subject,
                    sender=sender,
                    recipients=[],
                    date=date,
                    flags=flags,
                    folder=folder,
                    size=msg_data.get(b"RFC822.SIZE", 0),
                )
            )
        return envelopes

    # ------------------------------------------------------------------
    # Body fetch
    # ------------------------------------------------------------------

    def fetch_body(self, folder: str, uid: int) -> MessageBody:
        self._require_connected()
        self._client.select_folder(folder, readonly=True)  # type: ignore[union-attr]

        raw_data = self._client.fetch([uid], ["RFC822"])  # type: ignore[union-attr]
        raw_bytes: bytes = raw_data.get(uid, {}).get(b"RFC822", b"")

        msg = email_lib.message_from_bytes(raw_bytes)
        text_plain = ""
        text_html = ""
        attachments: list[str] = []

        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition", ""))

            if "attachment" in disposition:
                attachments.append(part.get_filename() or "attachment")
                continue

            payload = part.get_payload(decode=True)
            if not isinstance(payload, bytes):
                continue

            charset = part.get_content_charset() or "utf-8"
            decoded = payload.decode(charset, errors="replace")

            if content_type == "text/plain" and not text_plain:
                text_plain = decoded
            elif content_type == "text/html" and not text_html:
                text_html = decoded

        return MessageBody(
            uid=uid,
            text_plain=text_plain,
            text_html=text_html,
            has_attachments=bool(attachments),
            attachment_names=attachments,
        )

    # ------------------------------------------------------------------
    # Flag operations
    # ------------------------------------------------------------------

    def mark_as_read(self, folder: str, uids: list[int]) -> int:
        self._require_connected()
        self._client.select_folder(folder)  # type: ignore[union-attr]
        self._client.add_flags(uids, [imapclient.SEEN])  # type: ignore[union-attr]
        return len(uids)

    def mark_as_unread(self, folder: str, uids: list[int]) -> int:
        self._require_connected()
        self._client.select_folder(folder)  # type: ignore[union-attr]
        self._client.remove_flags(uids, [imapclient.SEEN])  # type: ignore[union-attr]
        return len(uids)

    def move_message(self, folder: str, uid: int, destination: str) -> bool:
        self._require_connected()
        self._client.select_folder(folder)  # type: ignore[union-attr]
        self._client.move([uid], destination)  # type: ignore[union-attr]
        return True

    def delete_message(self, folder: str, uid: int) -> bool:
        self._require_connected()
        self._client.select_folder(folder)  # type: ignore[union-attr]
        self._client.delete_messages([uid])  # type: ignore[union-attr]
        return True

    def flag_message(self, folder: str, uid: int, flag: str) -> bool:
        self._require_connected()
        self._client.select_folder(folder)  # type: ignore[union-attr]
        self._client.add_flags([uid], [flag.encode()])  # type: ignore[union-attr]
        return True

    def unflag_message(self, folder: str, uid: int, flag: str) -> bool:
        self._require_connected()
        self._client.select_folder(folder)  # type: ignore[union-attr]
        self._client.remove_flags([uid], [flag.encode()])  # type: ignore[union-attr]
        return True

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _require_connected(self) -> None:
        if self._client is None:
            raise RuntimeError(
                "ImapClientAdapter is not connected. Call connect() first."
            )

    @staticmethod
    def _decode(value: Any) -> str:
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="replace")
        return str(value) if value is not None else ""

    @classmethod
    def _parse_address(cls, addr: Any) -> EmailAddress:
        name = cls._decode(addr.name) if addr.name else ""
        mailbox = cls._decode(addr.mailbox) if addr.mailbox else ""
        host = cls._decode(addr.host) if addr.host else ""
        address = f"{mailbox}@{host}" if host else mailbox
        return EmailAddress(name=name, address=address)
