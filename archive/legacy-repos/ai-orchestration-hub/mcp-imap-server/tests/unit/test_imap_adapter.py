"""Unit tests for ImapClientAdapter — all network I/O is mocked via imapclient."""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import MagicMock, call, patch

import pytest

from src.domain.entities import EmailAddress, MessageFlag
from src.infrastructure.imap_adapter import ImapClientAdapter


# ── Helpers ───────────────────────────────────────────────────────────────────


def _make_credentials(
    host="imap.mail.me.com",
    port=993,
    username="user@icloud.com",
    password="xxxx-xxxx-xxxx-xxxx",
    ssl=True,
):
    creds = MagicMock()
    creds.get_host.return_value = host
    creds.get_port.return_value = port
    creds.get_username.return_value = username
    creds.get_password.return_value = password
    creds.use_ssl.return_value = ssl
    return creds


def _make_envelope_data(
    uid=1,
    subject=b"Test Subject",
    from_name=b"Sender",
    from_mailbox=b"sender",
    from_host=b"icloud.com",
    date=None,
    flags=(),
    size=1024,
):
    """Build a minimal imapclient ENVELOPE response dict for one UID."""
    addr = MagicMock()
    addr.name = from_name
    addr.mailbox = from_mailbox
    addr.host = from_host

    env = MagicMock()
    env.subject = subject
    env.from_ = [addr]
    env.message_id = b"<test@icloud.com>"
    env.date = date or datetime(2026, 3, 31, tzinfo=timezone.utc)

    return {
        uid: {
            b"ENVELOPE": env,
            b"FLAGS": list(flags),
            b"RFC822.SIZE": size,
        }
    }


# ── Connection ────────────────────────────────────────────────────────────────


class TestConnection:
    def test_connect_calls_login(self):
        creds = _make_credentials()
        adapter = ImapClientAdapter(creds)

        mock_client = MagicMock()
        with patch("imapclient.IMAPClient", return_value=mock_client):
            adapter.connect()

        mock_client.login.assert_called_once_with("user@icloud.com", "xxxx-xxxx-xxxx-xxxx")

    def test_connect_passes_ssl_flag(self):
        creds = _make_credentials(ssl=True)
        adapter = ImapClientAdapter(creds)

        with patch("imapclient.IMAPClient") as mock_cls:
            mock_cls.return_value = MagicMock()
            adapter.connect()
            mock_cls.assert_called_once_with("imap.mail.me.com", port=993, ssl=True)

    def test_disconnect_calls_logout(self):
        creds = _make_credentials()
        adapter = ImapClientAdapter(creds)

        mock_client = MagicMock()
        with patch("imapclient.IMAPClient", return_value=mock_client):
            adapter.connect()

        adapter.disconnect()
        mock_client.logout.assert_called_once()

    def test_disconnect_when_not_connected_is_noop(self):
        adapter = ImapClientAdapter(_make_credentials())
        adapter.disconnect()  # must not raise

    def test_disconnect_swallows_logout_error(self):
        creds = _make_credentials()
        adapter = ImapClientAdapter(creds)

        mock_client = MagicMock()
        mock_client.logout.side_effect = Exception("network gone")
        with patch("imapclient.IMAPClient", return_value=mock_client):
            adapter.connect()

        adapter.disconnect()  # must not raise
        assert adapter._client is None

    def test_operations_require_connected(self):
        adapter = ImapClientAdapter(_make_credentials())
        with pytest.raises(RuntimeError, match="ImapClientAdapter is not connected"):
            adapter.list_folders()

    def test_connect_then_disconnect_clears_client(self):
        adapter = ImapClientAdapter(_make_credentials())
        mock_client = MagicMock()
        with patch("imapclient.IMAPClient", return_value=mock_client):
            adapter.connect()
        assert adapter._client is not None
        adapter.disconnect()
        assert adapter._client is None


# ── list_folders ──────────────────────────────────────────────────────────────


class TestListFolders:
    def _adapter_with_client(self, client):
        adapter = ImapClientAdapter(_make_credentials())
        adapter._client = client
        return adapter

    def test_returns_folder_list(self):
        client = MagicMock()
        client.list_folders.return_value = [
            ([b"\\HasNoChildren"], b"/", b"INBOX"),
            ([b"\\HasNoChildren"], b"/", b"Sent Messages"),
        ]
        adapter = self._adapter_with_client(client)
        folders = adapter.list_folders()

        assert len(folders) == 2
        assert folders[0].name == "INBOX"
        assert folders[1].name == "Sent Messages"

    def test_folder_flags_decoded(self):
        client = MagicMock()
        client.list_folders.return_value = [
            ([b"\\HasNoChildren", b"\\Trash"], b"/", b"Deleted Messages"),
        ]
        adapter = self._adapter_with_client(client)
        folders = adapter.list_folders()
        assert "\\HasNoChildren" in folders[0].flags
        assert "\\Trash" in folders[0].flags


# ── search_messages ───────────────────────────────────────────────────────────


class TestSearchMessages:
    def _adapter_with_client(self, client):
        adapter = ImapClientAdapter(_make_credentials())
        adapter._client = client
        return adapter

    def test_returns_empty_when_no_unread(self):
        client = MagicMock()
        client.search.return_value = []
        adapter = self._adapter_with_client(client)

        result = adapter.search_messages()
        assert result == []

    def test_returns_envelopes_for_found_messages(self):
        client = MagicMock()
        client.search.return_value = [1]
        client.fetch.return_value = _make_envelope_data(uid=1)

        adapter = self._adapter_with_client(client)
        envelopes = adapter.search_messages()

        assert len(envelopes) == 1
        assert envelopes[0].uid == 1
        assert envelopes[0].subject == "Test Subject"

    def test_sender_parsed(self):
        client = MagicMock()
        client.search.return_value = [1]
        client.fetch.return_value = _make_envelope_data(
            uid=1, from_mailbox=b"jader", from_host=b"icloud.com"
        )
        adapter = self._adapter_with_client(client)
        env = adapter.search_messages()[0]

        assert env.sender.address == "jader@icloud.com"

    def test_limit_slices_uid_list(self):
        client = MagicMock()
        client.search.return_value = list(range(1, 101))  # 100 UIDs

        # Build fetch response for UIDs 96-100 (last 5)
        fetch_data = {}
        for uid in range(96, 101):
            fetch_data[uid] = list(_make_envelope_data(uid=uid).values())[0]
        client.fetch.return_value = fetch_data

        adapter = self._adapter_with_client(client)
        adapter.search_messages(limit=5)

        fetched_uids = client.fetch.call_args[0][0]
        assert fetched_uids == list(range(96, 101))

    def test_uses_unseen_criteria_by_default(self):
        client = MagicMock()
        client.search.return_value = []
        adapter = self._adapter_with_client(client)

        adapter.search_messages()
        client.search.assert_called_once_with(["UNSEEN"])

    def test_uses_readonly_select(self):
        client = MagicMock()
        client.search.return_value = []
        adapter = self._adapter_with_client(client)

        adapter.search_messages(folder="INBOX")
        client.select_folder.assert_called_once_with("INBOX", readonly=True)

    def test_skips_message_with_no_envelope(self):
        client = MagicMock()
        client.search.return_value = [1]
        client.fetch.return_value = {1: {b"FLAGS": [], b"RFC822.SIZE": 0}}  # no ENVELOPE
        adapter = self._adapter_with_client(client)

        result = adapter.search_messages()
        assert result == []

    def test_no_sender_produces_empty_address(self):
        client = MagicMock()
        client.search.return_value = [1]

        env_data = _make_envelope_data(uid=1)
        env_data[1][b"ENVELOPE"].from_ = None
        client.fetch.return_value = env_data

        adapter = self._adapter_with_client(client)
        env = adapter.search_messages()[0]
        assert env.sender == EmailAddress(name="", address="")


# ── fetch_body ────────────────────────────────────────────────────────────────


class TestFetchBody:
    _PLAIN_EMAIL = (
        b"From: sender@icloud.com\r\n"
        b"Content-Type: text/plain; charset=utf-8\r\n\r\n"
        b"Hello, this is a test."
    )

    _HTML_EMAIL = (
        b"From: sender@icloud.com\r\n"
        b"Content-Type: text/html; charset=utf-8\r\n\r\n"
        b"<p>Hello</p>"
    )

    _MULTIPART_EMAIL = (
        b"From: sender@icloud.com\r\n"
        b"MIME-Version: 1.0\r\n"
        b'Content-Type: multipart/mixed; boundary="boundary"\r\n\r\n'
        b"--boundary\r\n"
        b"Content-Type: text/plain; charset=utf-8\r\n\r\n"
        b"Plain text part\r\n"
        b"--boundary\r\n"
        b'Content-Type: application/pdf\r\n'
        b'Content-Disposition: attachment; filename="file.pdf"\r\n\r\n'
        b"PDF-DATA\r\n"
        b"--boundary--\r\n"
    )

    def _adapter_with_fetch(self, raw_bytes, uid=1):
        client = MagicMock()
        client.fetch.return_value = {uid: {b"RFC822": raw_bytes}}
        adapter = ImapClientAdapter(_make_credentials())
        adapter._client = client
        return adapter

    def test_reads_plain_text(self):
        adapter = self._adapter_with_fetch(self._PLAIN_EMAIL)
        body = adapter.fetch_body("INBOX", 1)
        assert "Hello, this is a test." in body.text_plain

    def test_reads_html_separately(self):
        adapter = self._adapter_with_fetch(self._HTML_EMAIL)
        body = adapter.fetch_body("INBOX", 1)
        assert "<p>Hello</p>" in body.text_html
        assert body.text_plain == ""

    def test_detects_attachment(self):
        adapter = self._adapter_with_fetch(self._MULTIPART_EMAIL)
        body = adapter.fetch_body("INBOX", 1)
        assert body.has_attachments is True
        assert "file.pdf" in body.attachment_names

    def test_uses_readonly_select(self):
        adapter = self._adapter_with_fetch(self._PLAIN_EMAIL)
        adapter.fetch_body("INBOX", 1)
        adapter._client.select_folder.assert_called_with("INBOX", readonly=True)

    def test_empty_raw_produces_empty_body(self):
        adapter = self._adapter_with_fetch(b"")
        body = adapter.fetch_body("INBOX", 1)
        assert body.text_plain == ""
        assert body.has_attachments is False


# ── Flag operations ───────────────────────────────────────────────────────────


class TestFlagOperations:
    def _adapter(self):
        adapter = ImapClientAdapter(_make_credentials())
        adapter._client = MagicMock()
        return adapter

    def test_mark_as_read_returns_count(self):
        adapter = self._adapter()
        count = adapter.mark_as_read("INBOX", [1, 2, 3])
        assert count == 3

    def test_mark_as_unread_returns_count(self):
        adapter = self._adapter()
        count = adapter.mark_as_unread("INBOX", [1])
        assert count == 1

    def test_move_message_returns_true(self):
        adapter = self._adapter()
        assert adapter.move_message("INBOX", 1, "Archive") is True
        adapter._client.move.assert_called_once_with([1], "Archive")

    def test_delete_message_returns_true(self):
        adapter = self._adapter()
        assert adapter.delete_message("INBOX", 1) is True

    def test_flag_message_returns_true(self):
        adapter = self._adapter()
        assert adapter.flag_message("INBOX", 1, "\\Flagged") is True

    def test_unflag_message_returns_true(self):
        adapter = self._adapter()
        assert adapter.unflag_message("INBOX", 1, "\\Flagged") is True


# ── _decode helper ────────────────────────────────────────────────────────────


class TestDecodeHelper:
    def test_decodes_bytes(self):
        assert ImapClientAdapter._decode(b"hello") == "hello"

    def test_passes_str_through(self):
        assert ImapClientAdapter._decode("world") == "world"

    def test_none_returns_empty(self):
        assert ImapClientAdapter._decode(None) == ""

    def test_invalid_utf8_uses_replace(self):
        result = ImapClientAdapter._decode(b"\xff\xfe")
        assert isinstance(result, str)

    def test_parse_address_builds_email_address(self):
        addr = MagicMock()
        addr.name = b"Alice"
        addr.mailbox = b"alice"
        addr.host = b"example.com"
        result = ImapClientAdapter._parse_address(addr)
        assert result.name == "Alice"
        assert result.address == "alice@example.com"

    def test_parse_address_no_host(self):
        addr = MagicMock()
        addr.name = b""
        addr.mailbox = b"local"
        addr.host = None
        result = ImapClientAdapter._parse_address(addr)
        assert result.address == "local"
