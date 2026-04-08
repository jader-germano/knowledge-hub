"""Unit tests for application use cases — all I/O is mocked via ports."""

from datetime import datetime, timezone
from unittest.mock import MagicMock, call

import pytest

from src.domain.entities import (
    AuditEntry,
    EmailAddress,
    FolderInfo,
    MessageBody,
    MessageEnvelope,
)
from src.application.use_cases import FetchMessageBody, FetchUnreadEmails, ListFolders


def _make_envelope(uid: int = 1) -> MessageEnvelope:
    return MessageEnvelope(
        uid=uid,
        message_id=f"<{uid}@test>",
        subject="Test subject",
        sender=EmailAddress(name="Sender", address="sender@icloud.com"),
        recipients=[],
        date=datetime.now(tz=timezone.utc),
        flags=[],
        folder="INBOX",
    )


class TestFetchUnreadEmails:
    def setup_method(self):
        self.gateway = MagicMock()
        self.audit = MagicMock()
        self.use_case = FetchUnreadEmails(self.gateway, self.audit)

    def test_returns_messages_from_gateway(self):
        envelopes = [_make_envelope(1), _make_envelope(2)]
        self.gateway.search_messages.return_value = envelopes

        result = self.use_case.execute()

        assert result == envelopes

    def test_connects_before_search_and_disconnects_after(self):
        self.gateway.search_messages.return_value = []

        self.use_case.execute()

        assert self.gateway.connect.call_count == 1
        assert self.gateway.disconnect.call_count == 1
        # connect must precede search_messages
        expected_order = [call.connect(), call.search_messages(folder="INBOX", criteria="UNSEEN", limit=50), call.disconnect()]
        self.gateway.assert_has_calls(expected_order)

    def test_disconnects_even_when_search_raises(self):
        self.gateway.search_messages.side_effect = RuntimeError("IMAP error")

        with pytest.raises(RuntimeError):
            self.use_case.execute()

        self.gateway.disconnect.assert_called_once()

    def test_logs_audit_entry_after_success(self):
        self.gateway.search_messages.return_value = [_make_envelope()]

        self.use_case.execute()

        self.audit.log.assert_called_once()
        entry: AuditEntry = self.audit.log.call_args[0][0]
        assert entry.action == "fetch_unread"
        assert entry.uids_affected == 1
        assert entry.folder == "INBOX"

    def test_audit_not_logged_when_search_raises(self):
        self.gateway.search_messages.side_effect = RuntimeError("boom")

        with pytest.raises(RuntimeError):
            self.use_case.execute()

        self.audit.log.assert_not_called()

    def test_custom_folder_passed_through(self):
        self.gateway.search_messages.return_value = []

        self.use_case.execute(folder="Sent Messages")

        self.gateway.search_messages.assert_called_once_with(
            folder="Sent Messages", criteria="UNSEEN", limit=50
        )

    def test_invalid_limit_raises_value_error(self):
        with pytest.raises(ValueError):
            self.use_case.execute(limit=0)

        with pytest.raises(ValueError):
            self.use_case.execute(limit=201)


class TestFetchMessageBody:
    def setup_method(self):
        self.gateway = MagicMock()
        self.audit = MagicMock()
        self.use_case = FetchMessageBody(self.gateway, self.audit)

    def test_returns_body_from_gateway(self):
        expected = MessageBody(uid=42, text_plain="Hello world")
        self.gateway.fetch_body.return_value = expected

        result = self.use_case.execute(folder="INBOX", uid=42)

        assert result == expected

    def test_disconnects_even_when_fetch_raises(self):
        self.gateway.fetch_body.side_effect = RuntimeError("network error")

        with pytest.raises(RuntimeError):
            self.use_case.execute(folder="INBOX", uid=1)

        self.gateway.disconnect.assert_called_once()

    def test_invalid_uid_raises_value_error(self):
        with pytest.raises(ValueError):
            self.use_case.execute(folder="INBOX", uid=0)

        with pytest.raises(ValueError):
            self.use_case.execute(folder="INBOX", uid=-5)

    def test_audit_entry_recorded(self):
        self.gateway.fetch_body.return_value = MessageBody(uid=7)

        self.use_case.execute(folder="INBOX", uid=7)

        entry: AuditEntry = self.audit.log.call_args[0][0]
        assert entry.action == "fetch_body"
        assert entry.uids_affected == 1


class TestListFolders:
    def setup_method(self):
        self.gateway = MagicMock()
        self.use_case = ListFolders(self.gateway)

    def test_returns_folder_list(self):
        folders = [FolderInfo(name="INBOX", delimiter="/", flags=[])]
        self.gateway.list_folders.return_value = folders

        result = self.use_case.execute()

        assert result == folders

    def test_disconnects_always(self):
        self.gateway.list_folders.return_value = []

        self.use_case.execute()

        self.gateway.disconnect.assert_called_once()
