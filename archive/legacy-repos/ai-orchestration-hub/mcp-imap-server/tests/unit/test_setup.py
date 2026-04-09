"""Unit tests for the mcp-imap-setup CLI — targets 100 % line coverage.

Strategy
────────
- All I/O (input, getpass, print) is mocked via builtins patches + capsys.
- All infra imports inside the CLI functions are patched at their module path
  so lazy imports pick up the mock.
- sys.exit is observed via pytest.raises(SystemExit).
"""

from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

import pytest

from src.presentation.setup import _abort, _check, _enroll, _header, _revoke, main


# ── _header ────────────────────────────────────────────────────────────────────


class TestHeader:
    def test_prints_banner(self, capsys):
        _header()
        out = capsys.readouterr().out
        assert "iCloud Mail MCP" in out


# ── _abort ─────────────────────────────────────────────────────────────────────


class TestAbort:
    def test_exits_with_code_1(self):
        with pytest.raises(SystemExit) as exc_info:
            _abort("Something went wrong")
        assert exc_info.value.code == 1

    def test_prints_message(self, capsys):
        with pytest.raises(SystemExit):
            _abort("Custom error message")
        assert "Custom error message" in capsys.readouterr().out


# ── main ───────────────────────────────────────────────────────────────────────


class TestMain:
    def test_routes_to_revoke(self):
        with patch("src.presentation.setup._revoke") as mock_revoke, \
             patch.object(sys, "argv", ["mcp-imap-setup", "--revoke"]):
            main()
        mock_revoke.assert_called_once()

    def test_routes_to_check(self):
        with patch("src.presentation.setup._check") as mock_check, \
             patch.object(sys, "argv", ["mcp-imap-setup", "--check"]):
            main()
        mock_check.assert_called_once()

    def test_routes_to_enroll_by_default(self):
        with patch("src.presentation.setup._enroll") as mock_enroll, \
             patch.object(sys, "argv", ["mcp-imap-setup"]):
            main()
        mock_enroll.assert_called_once()


# ── _check ─────────────────────────────────────────────────────────────────────


class TestCheck:
    def test_check_all_ok(self, capsys):
        with patch("src.infrastructure.biometric_auth.build_helper", return_value=True), \
             patch("src.infrastructure.biometric_auth.is_available", return_value=True), \
             patch("src.infrastructure.keychain_store.KeychainCredentialStore.is_enrolled",
                   return_value=True):
            _check()
        out = capsys.readouterr().out
        assert "Sim" in out

    def test_check_not_enrolled_exits_1(self):
        with patch("src.infrastructure.biometric_auth.build_helper", return_value=True), \
             patch("src.infrastructure.biometric_auth.is_available", return_value=False), \
             patch("src.infrastructure.keychain_store.KeychainCredentialStore.is_enrolled",
                   return_value=False):
            with pytest.raises(SystemExit) as exc_info:
                _check()
        assert exc_info.value.code == 1

    def test_check_built_false_skips_biometric_call(self, capsys):
        """When helper cannot be built, is_available should not be called."""
        mock_avail = MagicMock(return_value=True)
        with patch("src.infrastructure.biometric_auth.build_helper", return_value=False), \
             patch("src.infrastructure.biometric_auth.is_available", mock_avail), \
             patch("src.infrastructure.keychain_store.KeychainCredentialStore.is_enrolled",
                   return_value=True):
            _check()
        mock_avail.assert_not_called()

    def test_check_biometric_unavailable_shows_negative(self, capsys):
        """Enrolled + built but Touch ID reports unavailable."""
        with patch("src.infrastructure.biometric_auth.build_helper", return_value=True), \
             patch("src.infrastructure.biometric_auth.is_available", return_value=False), \
             patch("src.infrastructure.keychain_store.KeychainCredentialStore.is_enrolled",
                   return_value=True):
            _check()  # must not exit
        out = capsys.readouterr().out
        assert "Touch ID" in out


# ── _revoke ────────────────────────────────────────────────────────────────────


class TestRevoke:
    def test_not_enrolled_prints_info_and_returns(self, capsys):
        with patch("src.infrastructure.keychain_store.KeychainCredentialStore.is_enrolled",
                   return_value=False):
            _revoke()
        out = capsys.readouterr().out
        assert "Nenhuma credencial" in out

    def test_revoke_user_confirms_s(self, capsys):
        with patch("src.infrastructure.keychain_store.KeychainCredentialStore.is_enrolled",
                   return_value=True), \
             patch("src.infrastructure.keychain_store.KeychainCredentialStore.revoke"), \
             patch("builtins.input", return_value="s"):
            _revoke()
        out = capsys.readouterr().out
        assert "removidas" in out

    def test_revoke_user_cancels(self, capsys):
        with patch("src.infrastructure.keychain_store.KeychainCredentialStore.is_enrolled",
                   return_value=True), \
             patch("builtins.input", return_value="n"):
            _revoke()
        out = capsys.readouterr().out
        assert "cancelada" in out


# ── _enroll — build helper outcomes ───────────────────────────────────────────


class TestEnrollBuildHelperOutcomes:
    """Cover the three branches of the helper compilation block."""

    def _success_patches(self, **kwargs):
        """Common patches for a successful enrollment after the build block."""
        return [
            patch("src.infrastructure.keychain_store.KeychainCredentialStore.enroll"),
            patch("src.infrastructure.keychain_store.KeychainCredentialStore.is_enrolled",
                  return_value=True),
            patch("builtins.input", return_value="user@icloud.com"),
            patch("getpass.getpass", return_value="abcd-efgh-ijkl-mnop"),
        ]

    def test_compiled_touch_id_available(self, capsys):
        with patch("src.infrastructure.biometric_auth.build_helper", return_value=True), \
             patch("src.infrastructure.biometric_auth.is_available", return_value=True), \
             patch("src.infrastructure.keychain_store.KeychainCredentialStore.enroll"), \
             patch("src.infrastructure.keychain_store.KeychainCredentialStore.is_enrolled",
                   return_value=True), \
             patch("builtins.input", return_value="user@icloud.com"), \
             patch("getpass.getpass", return_value="abcd-efgh-ijkl-mnop"):
            _enroll()
        assert "Touch ID detectado" in capsys.readouterr().out

    def test_compiled_touch_id_unavailable(self, capsys):
        with patch("src.infrastructure.biometric_auth.build_helper", return_value=True), \
             patch("src.infrastructure.biometric_auth.is_available", return_value=False), \
             patch("src.infrastructure.keychain_store.KeychainCredentialStore.enroll"), \
             patch("src.infrastructure.keychain_store.KeychainCredentialStore.is_enrolled",
                   return_value=True), \
             patch("builtins.input", return_value="user@icloud.com"), \
             patch("getpass.getpass", return_value="abcd-efgh-ijkl-mnop"):
            _enroll()
        assert "Touch ID indisponível" in capsys.readouterr().out

    def test_compilation_failed_warns_user(self, capsys):
        with patch("src.infrastructure.biometric_auth.build_helper", return_value=False), \
             patch("src.infrastructure.keychain_store.KeychainCredentialStore.enroll"), \
             patch("src.infrastructure.keychain_store.KeychainCredentialStore.is_enrolled",
                   return_value=True), \
             patch("builtins.input", return_value="user@icloud.com"), \
             patch("getpass.getpass", return_value="abcd-efgh-ijkl-mnop"):
            _enroll()
        assert "helper Swift" in capsys.readouterr().out


# ── _enroll — email validation ─────────────────────────────────────────────────


class TestEnrollEmailValidation:
    def test_invalid_email_no_at_sign_aborts(self):
        with patch("src.infrastructure.biometric_auth.build_helper", return_value=False), \
             patch("builtins.input", return_value="notanemail"):
            with pytest.raises(SystemExit) as exc_info:
                _enroll()
        assert exc_info.value.code == 1

    def test_empty_email_aborts(self):
        with patch("src.infrastructure.biometric_auth.build_helper", return_value=False), \
             patch("builtins.input", return_value=""):
            with pytest.raises(SystemExit) as exc_info:
                _enroll()
        assert exc_info.value.code == 1


# ── _enroll — password validation ──────────────────────────────────────────────


class TestEnrollPasswordValidation:
    def test_empty_password_aborts(self):
        with patch("src.infrastructure.biometric_auth.build_helper", return_value=False), \
             patch("builtins.input", return_value="user@icloud.com"), \
             patch("getpass.getpass", return_value=""):
            with pytest.raises(SystemExit) as exc_info:
                _enroll()
        assert exc_info.value.code == 1

    def test_invalid_format_user_confirms_continues(self, capsys):
        """Bad format → warn → user types 's' → enrollment proceeds."""
        inputs = iter(["user@icloud.com", "s"])
        with patch("src.infrastructure.biometric_auth.build_helper", return_value=False), \
             patch("builtins.input", side_effect=inputs), \
             patch("getpass.getpass", return_value="tooshort"), \
             patch("src.infrastructure.keychain_store.KeychainCredentialStore.enroll"), \
             patch("src.infrastructure.keychain_store.KeychainCredentialStore.is_enrolled",
                   return_value=True):
            _enroll()
        assert "formato" in capsys.readouterr().out

    def test_invalid_format_user_cancels_aborts(self):
        """Bad format → warn → user types 'n' → sys.exit(1)."""
        inputs = iter(["user@icloud.com", "n"])
        with patch("src.infrastructure.biometric_auth.build_helper", return_value=False), \
             patch("builtins.input", side_effect=inputs), \
             patch("getpass.getpass", return_value="tooshort"):
            with pytest.raises(SystemExit) as exc_info:
                _enroll()
        assert exc_info.value.code == 1


# ── _enroll — keychain failures ────────────────────────────────────────────────


class TestEnrollKeychainFailures:
    def test_enroll_raises_aborts(self):
        with patch("src.infrastructure.biometric_auth.build_helper", return_value=False), \
             patch("builtins.input", return_value="user@icloud.com"), \
             patch("getpass.getpass", return_value="abcd-efgh-ijkl-mnop"), \
             patch("src.infrastructure.keychain_store.KeychainCredentialStore.enroll",
                   side_effect=Exception("Keychain locked")):
            with pytest.raises(SystemExit) as exc_info:
                _enroll()
        assert exc_info.value.code == 1

    def test_verify_after_enroll_fails_aborts(self):
        """is_enrolled() returns False after enroll → abort."""
        with patch("src.infrastructure.biometric_auth.build_helper", return_value=False), \
             patch("builtins.input", return_value="user@icloud.com"), \
             patch("getpass.getpass", return_value="abcd-efgh-ijkl-mnop"), \
             patch("src.infrastructure.keychain_store.KeychainCredentialStore.enroll"), \
             patch("src.infrastructure.keychain_store.KeychainCredentialStore.is_enrolled",
                   return_value=False):
            with pytest.raises(SystemExit) as exc_info:
                _enroll()
        assert exc_info.value.code == 1

    def test_successful_enroll_prints_confirmation(self, capsys):
        """Happy path: all succeeds → success message printed."""
        with patch("src.infrastructure.biometric_auth.build_helper", return_value=False), \
             patch("builtins.input", return_value="user@icloud.com"), \
             patch("getpass.getpass", return_value="abcd-efgh-ijkl-mnop"), \
             patch("src.infrastructure.keychain_store.KeychainCredentialStore.enroll"), \
             patch("src.infrastructure.keychain_store.KeychainCredentialStore.is_enrolled",
                   return_value=True):
            _enroll()
        out = capsys.readouterr().out
        assert "Configuração concluída" in out
