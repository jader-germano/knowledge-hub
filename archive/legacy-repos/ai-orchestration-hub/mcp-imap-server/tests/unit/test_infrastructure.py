"""Unit tests for infrastructure layer — imapclient and credential store mocked."""

import os
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from src.infrastructure.audit_logger import InMemoryAuditLogger
from src.infrastructure.credential_store import EnvCredentialStore
from src.domain.entities import AuditEntry


# ---------------------------------------------------------------------------
# EnvCredentialStore
# ---------------------------------------------------------------------------

class TestEnvCredentialStore:
    def test_raises_when_required_vars_missing(self):
        with patch.dict(os.environ, {}, clear=True):
            # Remove any existing iCloud vars
            env = {k: v for k, v in os.environ.items()
                   if k not in ("ICLOUD_EMAIL", "ICLOUD_APP_PASSWORD")}
            with patch.dict(os.environ, env, clear=True):
                with pytest.raises(EnvironmentError, match="ICLOUD_EMAIL"):
                    EnvCredentialStore()

    def test_reads_icloud_defaults(self):
        with patch.dict(os.environ, {
            "ICLOUD_EMAIL": "user@icloud.com",
            "ICLOUD_APP_PASSWORD": "abcd-efgh-ijkl-mnop",
        }):
            store = EnvCredentialStore()
            assert store.get_host() == "imap.mail.me.com"
            assert store.get_port() == 993
            assert store.use_ssl() is True

    def test_reads_custom_host_and_port(self):
        with patch.dict(os.environ, {
            "ICLOUD_EMAIL": "user@gmail.com",
            "ICLOUD_APP_PASSWORD": "secret",
            "IMAP_HOST": "imap.gmail.com",
            "IMAP_PORT": "993",
        }):
            store = EnvCredentialStore()
            assert store.get_host() == "imap.gmail.com"

    def test_ssl_can_be_disabled(self):
        with patch.dict(os.environ, {
            "ICLOUD_EMAIL": "u@icloud.com",
            "ICLOUD_APP_PASSWORD": "s",
            "IMAP_SSL": "false",
        }):
            store = EnvCredentialStore()
            assert store.use_ssl() is False

    def test_password_not_in_error_message(self):
        """Ensures partial credentials don't leak in EnvironmentError text."""
        with patch.dict(os.environ, {"ICLOUD_APP_PASSWORD": "super_secret"}, clear=True):
            env = {k: v for k, v in os.environ.items() if k != "ICLOUD_EMAIL"}
            with patch.dict(os.environ, env, clear=True):
                with pytest.raises(EnvironmentError) as exc_info:
                    EnvCredentialStore()
                assert "super_secret" not in str(exc_info.value)

    def test_get_username_returns_env_value(self):
        with patch.dict(os.environ, {
            "ICLOUD_EMAIL": "jader@icloud.com",
            "ICLOUD_APP_PASSWORD": "abcd-efgh-ijkl-mnop",
        }):
            store = EnvCredentialStore()
            assert store.get_username() == "jader@icloud.com"

    def test_get_password_returns_env_value(self):
        with patch.dict(os.environ, {
            "ICLOUD_EMAIL": "jader@icloud.com",
            "ICLOUD_APP_PASSWORD": "abcd-efgh-ijkl-mnop",
        }):
            store = EnvCredentialStore()
            assert store.get_password() == "abcd-efgh-ijkl-mnop"


# ---------------------------------------------------------------------------
# InMemoryAuditLogger
# ---------------------------------------------------------------------------

class TestInMemoryAuditLogger:
    def _entry(self, action: str = "fetch_unread", uids: int = 1) -> AuditEntry:
        return AuditEntry(
            timestamp=datetime.now(tz=timezone.utc),
            action=action,
            folder="INBOX",
            uids_affected=uids,
        )

    def test_log_and_retrieve(self):
        logger = InMemoryAuditLogger()
        entry = self._entry()
        logger.log(entry)

        result = logger.get_entries()
        assert result == [entry]

    def test_filter_by_action(self):
        logger = InMemoryAuditLogger()
        logger.log(self._entry("fetch_unread"))
        logger.log(self._entry("fetch_body"))

        result = logger.get_entries(action="fetch_body")
        assert len(result) == 1
        assert result[0].action == "fetch_body"

    def test_respects_limit(self):
        logger = InMemoryAuditLogger()
        for _ in range(10):
            logger.log(self._entry())

        result = logger.get_entries(limit=3)
        assert len(result) == 3

    def test_evicts_oldest_when_max_exceeded(self):
        logger = InMemoryAuditLogger(max_entries=3)
        entries = [self._entry(action=f"action_{i}") for i in range(5)]
        for e in entries:
            logger.log(e)

        result = logger.get_entries(limit=10)
        assert len(result) == 3
        # Only the last 3 entries should remain
        assert result[-1].action == "action_4"

    def test_empty_logger_returns_empty_list(self):
        logger = InMemoryAuditLogger()
        assert logger.get_entries() == []

    def test_filter_by_since_naive_datetime(self):
        """get_entries(since=<naive datetime>) must auto-attach UTC tzinfo."""
        logger = InMemoryAuditLogger()
        old_entry = AuditEntry(
            timestamp=datetime(2024, 1, 1, tzinfo=timezone.utc),
            action="fetch_unread",
            folder="INBOX",
            uids_affected=1,
        )
        new_entry = AuditEntry(
            timestamp=datetime.now(tz=timezone.utc),
            action="fetch_body",
            folder="INBOX",
            uids_affected=1,
        )
        logger.log(old_entry)
        logger.log(new_entry)

        # Naive datetime (no tzinfo) — treated as UTC
        result = logger.get_entries(since=datetime(2025, 1, 1))
        assert len(result) == 1
        assert result[0].action == "fetch_body"

    def test_filter_by_since_aware_datetime(self):
        """get_entries(since=<aware datetime>) must work without modifying tzinfo."""
        logger = InMemoryAuditLogger()
        old_entry = AuditEntry(
            timestamp=datetime(2024, 1, 1, tzinfo=timezone.utc),
            action="fetch_unread",
            folder="INBOX",
            uids_affected=1,
        )
        new_entry = AuditEntry(
            timestamp=datetime.now(tz=timezone.utc),
            action="fetch_body",
            folder="INBOX",
            uids_affected=1,
        )
        logger.log(old_entry)
        logger.log(new_entry)

        # Aware datetime passed directly
        result = logger.get_entries(since=datetime(2025, 1, 1, tzinfo=timezone.utc))
        assert len(result) == 1
        assert result[0].action == "fetch_body"
