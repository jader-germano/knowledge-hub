"""Unit tests for biometric_auth — covers build_helper, is_available, session persistence."""

from __future__ import annotations

import json
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

import src.infrastructure.biometric_auth as ba
from src.infrastructure.biometric_auth import (
    BiometryAuthError,
    BiometryUnavailableError,
    SESSION_TIMEOUT_SECS,
    _SESSION_FILE,
    _invalidate_session,
    _load_session,
    _persist_session,
    _session_token_key,
    authenticate,
    build_helper,
    is_available,
    reset_session,
)


@pytest.fixture(autouse=True)
def clean_state(tmp_path, monkeypatch):
    """Reset all session state before each test."""
    reset_session()
    # Redirect session file to tmp so tests don't touch real cache
    monkeypatch.setattr(ba, "_SESSION_FILE", tmp_path / ".session-token")
    monkeypatch.setattr(ba, "_CACHE_DIR", tmp_path)
    monkeypatch.setattr(ba, "_HELPER", tmp_path / "biometric-auth")
    yield
    reset_session()


# ── build_helper ──────────────────────────────────────────────────────────────


class TestBuildHelper:
    def test_returns_true_when_binary_already_exists(self, tmp_path, monkeypatch):
        helper = tmp_path / "biometric-auth"
        helper.touch()
        monkeypatch.setattr(ba, "_HELPER", helper)
        assert build_helper() is True

    def test_returns_false_when_swiftc_missing(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ba, "_HELPER", tmp_path / "biometric-auth")
        with patch("src.infrastructure.biometric_auth.subprocess.run",
                   side_effect=FileNotFoundError):
            assert build_helper() is False

    def test_returns_false_on_compilation_failure(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ba, "_HELPER", tmp_path / "biometric-auth")
        mock_result = MagicMock()
        mock_result.returncode = 1
        with patch("src.infrastructure.biometric_auth.subprocess.run",
                   return_value=mock_result):
            assert build_helper() is False

    def test_returns_false_on_timeout(self, tmp_path, monkeypatch):
        import subprocess
        monkeypatch.setattr(ba, "_HELPER", tmp_path / "biometric-auth")
        with patch("src.infrastructure.biometric_auth.subprocess.run",
                   side_effect=subprocess.TimeoutExpired("swiftc", 120)):
            assert build_helper() is False

    def test_cleans_up_temp_source_file(self, tmp_path, monkeypatch):
        """Temp .swift file must be deleted even on failure."""
        monkeypatch.setattr(ba, "_HELPER", tmp_path / "biometric-auth")
        mock_result = MagicMock()
        mock_result.returncode = 1
        with patch("src.infrastructure.biometric_auth.subprocess.run",
                   return_value=mock_result):
            build_helper()
        # No .swift files should remain
        swift_files = list(tmp_path.glob("*.swift"))
        assert swift_files == []

    def test_build_helper_unlink_oserror_is_silenced(self, tmp_path, monkeypatch):
        """os.unlink failure in finally block must not propagate."""
        monkeypatch.setattr(ba, "_HELPER", tmp_path / "biometric-auth")
        mock_result = MagicMock()
        mock_result.returncode = 1  # compilation "fails" but finally still runs

        with patch("src.infrastructure.biometric_auth.subprocess.run",
                   return_value=mock_result), \
             patch("src.infrastructure.biometric_auth.os.unlink",
                   side_effect=OSError("disk error")):
            result = build_helper()  # must NOT raise

        assert result is False


# ── is_available ──────────────────────────────────────────────────────────────


class TestIsAvailable:
    def test_false_when_build_fails(self):
        with patch.object(ba, "build_helper", return_value=False):
            assert is_available() is False

    def test_false_when_helper_returns_exit_2(self, tmp_path, monkeypatch):
        fake_helper = tmp_path / "biometric-auth"
        fake_helper.touch()
        monkeypatch.setattr(ba, "_HELPER", fake_helper)

        mock_result = MagicMock()
        mock_result.returncode = 2
        with patch.object(ba, "build_helper", return_value=True), \
             patch("src.infrastructure.biometric_auth.subprocess.run",
                   return_value=mock_result):
            assert is_available() is False

    def test_true_when_helper_returns_exit_0(self, tmp_path, monkeypatch):
        mock_result = MagicMock()
        mock_result.returncode = 0
        with patch.object(ba, "build_helper", return_value=True), \
             patch("src.infrastructure.biometric_auth.subprocess.run",
                   return_value=mock_result):
            assert is_available() is True

    def test_false_on_exception(self):
        with patch.object(ba, "build_helper", return_value=True), \
             patch("src.infrastructure.biometric_auth.subprocess.run",
                   side_effect=Exception("oops")):
            assert is_available() is False


# ── Session persistence ───────────────────────────────────────────────────────


class TestSessionPersistence:
    def test_persist_and_load_session(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ba, "_SESSION_FILE", tmp_path / ".session-token")
        _persist_session()
        assert _load_session() is True

    def test_load_returns_false_when_file_missing(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ba, "_SESSION_FILE", tmp_path / ".session-token")
        assert _load_session() is False

    def test_load_returns_false_after_timeout(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ba, "_SESSION_FILE", tmp_path / ".session-token")
        # Write a token with timestamp in the past
        payload = {
            "ts": time.time() - SESSION_TIMEOUT_SECS - 1,
            "key": _session_token_key(),
            "timeout": SESSION_TIMEOUT_SECS,
        }
        (tmp_path / ".session-token").write_text(json.dumps(payload))
        assert _load_session() is False

    def test_load_returns_false_for_different_user_key(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ba, "_SESSION_FILE", tmp_path / ".session-token")
        payload = {
            "ts": time.time(),
            "key": "wrong_key_000",
            "timeout": SESSION_TIMEOUT_SECS,
        }
        (tmp_path / ".session-token").write_text(json.dumps(payload))
        assert _load_session() is False

    def test_load_returns_false_on_corrupt_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ba, "_SESSION_FILE", tmp_path / ".session-token")
        (tmp_path / ".session-token").write_text("not-json{{{")
        assert _load_session() is False

    def test_invalidate_deletes_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ba, "_SESSION_FILE", tmp_path / ".session-token")
        _persist_session()
        _invalidate_session()
        assert not (tmp_path / ".session-token").exists()

    def test_invalidate_is_idempotent(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ba, "_SESSION_FILE", tmp_path / ".session-token")
        _invalidate_session()  # file doesn't exist — must not raise
        _invalidate_session()

    def test_persist_session_survives_oserror(self, monkeypatch):
        """_persist_session must silently swallow OSError on write."""
        mock_file = MagicMock()
        mock_file.write_text.side_effect = OSError("disk full")
        monkeypatch.setattr(ba, "_SESSION_FILE", mock_file)
        _persist_session()  # must NOT raise

    def test_invalidate_session_survives_oserror(self, monkeypatch):
        """_invalidate_session must silently swallow OSError on unlink."""
        mock_file = MagicMock()
        mock_file.unlink.side_effect = OSError("permission denied")
        monkeypatch.setattr(ba, "_SESSION_FILE", mock_file)
        _invalidate_session()  # must NOT raise

    def test_session_file_permissions(self, tmp_path, monkeypatch):
        import stat

        monkeypatch.setattr(ba, "_SESSION_FILE", tmp_path / ".session-token")
        _persist_session()
        mode = (tmp_path / ".session-token").stat().st_mode
        # Should be owner rw only (0o600)
        assert stat.S_IMODE(mode) == 0o600


# ── authenticate ──────────────────────────────────────────────────────────────


class TestAuthenticate:
    def test_returns_true_if_session_valid(self, tmp_path, monkeypatch):
        """Disk session should allow skipping Touch ID on restart."""
        monkeypatch.setattr(ba, "_SESSION_FILE", tmp_path / ".session-token")
        _persist_session()
        result = authenticate()
        assert result is True

    def test_raises_unavailable_when_build_fails(self):
        with patch.object(ba, "build_helper", return_value=False):
            with pytest.raises(BiometryUnavailableError, match="xcode-select"):
                authenticate()

    def test_raises_unavailable_when_returncode_2(self):
        mock_result = MagicMock()
        mock_result.returncode = 2
        with patch.object(ba, "build_helper", return_value=True), \
             patch("src.infrastructure.biometric_auth.subprocess.run",
                   return_value=mock_result):
            with pytest.raises(BiometryUnavailableError):
                authenticate()

    def test_raises_auth_error_when_returncode_1(self):
        mock_result = MagicMock()
        mock_result.returncode = 1
        with patch.object(ba, "build_helper", return_value=True), \
             patch("src.infrastructure.biometric_auth.subprocess.run",
                   return_value=mock_result):
            with pytest.raises(BiometryAuthError):
                authenticate()

    def test_success_persists_token_to_disk(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ba, "_SESSION_FILE", tmp_path / ".session-token")
        mock_result = MagicMock()
        mock_result.returncode = 0
        with patch.object(ba, "build_helper", return_value=True), \
             patch("src.infrastructure.biometric_auth.subprocess.run",
                   return_value=mock_result):
            authenticate()

        assert (tmp_path / ".session-token").exists()
        assert _load_session() is True

    def test_success_caches_in_memory(self):
        mock_result = MagicMock()
        mock_result.returncode = 0
        with patch.object(ba, "build_helper", return_value=True), \
             patch("src.infrastructure.biometric_auth.subprocess.run",
                   return_value=mock_result):
            authenticate()

        assert ba._SESSION_AUTHENTICATED is True

    def test_subsequent_calls_skip_subprocess(self):
        """Second authenticate() must NOT call subprocess.run again."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        with patch.object(ba, "build_helper", return_value=True), \
             patch("src.infrastructure.biometric_auth.subprocess.run",
                   return_value=mock_result) as mock_run:
            authenticate()
            authenticate()

        assert mock_run.call_count == 1

    def test_timeout_triggers_error(self):
        import subprocess

        with patch.object(ba, "build_helper", return_value=True), \
             patch("src.infrastructure.biometric_auth.subprocess.run",
                   side_effect=subprocess.TimeoutExpired("helper", 30)):
            with pytest.raises(BiometryAuthError, match="timed out"):
                authenticate()

    def test_raises_unavailable_on_file_not_found_during_auth(self):
        """FileNotFoundError on subprocess.run → BiometryUnavailableError."""
        with patch.object(ba, "build_helper", return_value=True), \
             patch("src.infrastructure.biometric_auth.subprocess.run",
                   side_effect=FileNotFoundError("helper gone")):
            with pytest.raises(BiometryUnavailableError, match="not found"):
                authenticate()

    def test_double_checked_locking_skips_auth_under_lock(self):
        """Second _is_session_valid() check inside the lock must short-circuit."""
        # Simulate: first check (fast path) returns False, but between the
        # fast-path check and lock acquisition another thread authenticates,
        # so the second check (under lock) returns True.
        with patch("src.infrastructure.biometric_auth._is_session_valid",
                   side_effect=[False, True]):
            result = authenticate()
        assert result is True


# ── reset_session ─────────────────────────────────────────────────────────────


class TestResetSession:
    def test_clears_memory_and_disk(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ba, "_SESSION_FILE", tmp_path / ".session-token")
        _persist_session()
        ba._SESSION_AUTHENTICATED = True

        reset_session()

        assert ba._SESSION_AUTHENTICATED is False
        assert not (tmp_path / ".session-token").exists()
