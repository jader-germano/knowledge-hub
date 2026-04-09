"""Unit tests for domain entities — pure logic, zero I/O."""

from datetime import datetime, timezone

import pytest

from src.domain.entities import (
    AuditEntry,
    EmailAddress,
    FolderInfo,
    MessageBody,
    MessageEnvelope,
    MessageFlag,
)


class TestEmailAddress:
    def test_parse_full_format(self):
        addr = EmailAddress.parse('"John Doe" <john@example.com>')
        assert addr.name == "John Doe"
        assert addr.address == "john@example.com"

    def test_parse_bare_email(self):
        addr = EmailAddress.parse("john@example.com")
        assert addr.name == ""
        assert addr.address == "john@example.com"

    def test_parse_angle_bracket_no_name(self):
        addr = EmailAddress.parse("<john@example.com>")
        assert addr.address == "john@example.com"

    def test_domain_extracted(self):
        addr = EmailAddress(name="", address="user@icloud.com")
        assert addr.domain == "icloud.com"

    def test_domain_empty_when_no_at(self):
        addr = EmailAddress(name="", address="notanemail")
        assert addr.domain == ""

    def test_str_with_name(self):
        addr = EmailAddress(name="Alice", address="alice@example.com")
        assert str(addr) == "Alice <alice@example.com>"

    def test_str_without_name(self):
        addr = EmailAddress(name="", address="alice@example.com")
        assert str(addr) == "alice@example.com"

    def test_frozen_immutable(self):
        addr = EmailAddress(name="Alice", address="alice@example.com")
        with pytest.raises((AttributeError, TypeError)):
            addr.name = "Bob"  # type: ignore[misc]


class TestMessageEnvelope:
    def _make_envelope(self, flags: list[str]) -> MessageEnvelope:
        return MessageEnvelope(
            uid=1,
            message_id="<abc@test>",
            subject="Test",
            sender=EmailAddress(name="", address="a@b.com"),
            recipients=[],
            date=datetime.now(tz=timezone.utc),
            flags=flags,
            folder="INBOX",
        )

    def test_is_read_when_seen_flag_present(self):
        env = self._make_envelope([MessageFlag.SEEN.value])
        assert env.is_read is True

    def test_is_not_read_without_seen_flag(self):
        env = self._make_envelope([])
        assert env.is_read is False

    def test_is_flagged(self):
        env = self._make_envelope([MessageFlag.FLAGGED.value])
        assert env.is_flagged is True


class TestMessageBody:
    def test_default_empty_body(self):
        body = MessageBody(uid=1)
        assert body.text_plain == ""
        assert body.has_attachments is False
        assert body.attachment_names == []


class TestAuditEntry:
    def test_no_pii_fields(self):
        entry = AuditEntry(
            timestamp=datetime.now(tz=timezone.utc),
            action="fetch_unread",
            folder="INBOX",
            uids_affected=5,
        )
        # Verify the entry has no subject/sender fields (PII guard)
        assert not hasattr(entry, "subject")
        assert not hasattr(entry, "sender")
        assert not hasattr(entry, "body")
