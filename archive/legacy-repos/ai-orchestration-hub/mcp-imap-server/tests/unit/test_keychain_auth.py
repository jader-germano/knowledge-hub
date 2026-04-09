"""Unit tests for KeychainCredentialStore and biometric_auth module."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

import src.infrastructure.keychain_store as ks_module
from src.infrastructure.keychain_store import KeychainCredentialStore, _reset_process_auth


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture(autouse=True)
def reset_auth_state():
    """Ensure biometric gate is reset before every test."""
    _reset_process_auth()
    import src.infrastructure.biometric_auth as ba
    ba.reset_session()
    yield
    _reset_process_auth()
    ba.reset_session()


# ── KeychainCredentialStore ───────────────────────────────────────────────────


class TestKeychainCredentialStore:
    def _mock_keyring(self, email: str = "user@icloud.com", password: str = "xxxx") -> MagicMock:
        mock = MagicMock()
        def get_password(service, key):
            return email if key == "__email__" else password
        mock.get_password.side_effect = get_password
        return mock

    def test_returns_icloud_host_and_port(self):
        with patch("src.infrastructure.keychain_store._gate_biometric"), \
             patch("src.infrastructure.keychain_store.ks_module", create=True), \
             patch("keyring.get_password", side_effect=lambda s, k: {
                 "__email__": "a@icloud.com", "__app_password__": "xxxx"
             }.get(k)):
            store = KeychainCredentialStore(require_biometric=False)
            assert store.get_host() == "imap.mail.me.com"
            assert store.get_port() == 993
            assert store.use_ssl() is True

    def test_retrieves_credentials_from_keychain(self):
        with patch("keyring.get_password", side_effect=lambda s, k: {
            "__email__": "jader@icloud.com",
            "__app_password__": "abcd-efgh-ijkl-mnop",
        }.get(k)):
            store = KeychainCredentialStore(require_biometric=False)
            assert store.get_username() == "jader@icloud.com"
            assert store.get_password() == "abcd-efgh-ijkl-mnop"

    def test_raises_environment_error_when_not_enrolled(self):
        with patch("keyring.get_password", return_value=None):
            with pytest.raises(EnvironmentError, match="mcp-imap-setup"):
                KeychainCredentialStore(require_biometric=False)

    def test_raises_environment_error_on_keyring_exception(self):
        from keyring.errors import KeyringError

        with patch("keyring.get_password", side_effect=KeyringError("locked")):
            with pytest.raises(EnvironmentError, match="Keychain"):
                KeychainCredentialStore(require_biometric=False)

    def test_is_enrolled_true_when_both_keys_present(self):
        with patch("keyring.get_password", return_value="some_value"):
            assert KeychainCredentialStore.is_enrolled() is True

    def test_is_enrolled_false_when_missing(self):
        with patch("keyring.get_password", return_value=None):
            assert KeychainCredentialStore.is_enrolled() is False

    def test_is_enrolled_returns_false_on_keyring_error(self):
        """KeyringError inside is_enrolled() must return False, not raise."""
        from keyring.errors import KeyringError
        with patch("keyring.get_password", side_effect=KeyringError("backend locked")):
            assert KeychainCredentialStore.is_enrolled() is False

    def test_enroll_sets_both_keys(self):
        with patch("keyring.set_password") as mock_set:
            KeychainCredentialStore.enroll("u@icloud.com", "xxxx-xxxx-xxxx-xxxx")
            calls = {call.args[1]: call.args[2] for call in mock_set.call_args_list}
            assert calls["__email__"] == "u@icloud.com"
            assert calls["__app_password__"] == "xxxx-xxxx-xxxx-xxxx"

    def test_revoke_deletes_both_keys(self):
        with patch("keyring.delete_password") as mock_del:
            KeychainCredentialStore.revoke()
            deleted_keys = {call.args[1] for call in mock_del.call_args_list}
            assert "__email__" in deleted_keys
            assert "__app_password__" in deleted_keys

    def test_revoke_ignores_keyring_errors(self):
        from keyring.errors import KeyringError
        with patch("keyring.delete_password", side_effect=KeyringError("gone")):
            KeychainCredentialStore.revoke()  # must not raise


# ── Biometric gate ─────────────────────────────────────────────────────────────


class TestBiometricGate:
    def test_gate_skipped_when_biometry_unavailable(self):
        """Should not raise; silently passes if no Touch ID hardware."""
        with patch("src.infrastructure.biometric_auth.is_available", return_value=False), \
             patch("keyring.get_password", side_effect=lambda s, k: {
                 "__email__": "a@icloud.com", "__app_password__": "pw"
             }.get(k)):
            # require_biometric=True but hardware is absent — should still succeed
            store = KeychainCredentialStore(require_biometric=True)
            assert store.get_username() == "a@icloud.com"

    def test_gate_succeeds_when_touch_id_passes(self):
        with patch("src.infrastructure.biometric_auth.is_available", return_value=True), \
             patch("src.infrastructure.biometric_auth.authenticate", return_value=True), \
             patch("keyring.get_password", side_effect=lambda s, k: {
                 "__email__": "a@icloud.com", "__app_password__": "pw"
             }.get(k)):
            store = KeychainCredentialStore(require_biometric=True)
            assert store.get_username() == "a@icloud.com"

    def test_gate_raises_permission_error_on_cancelled_auth(self):
        from src.infrastructure.biometric_auth import BiometryAuthError
        with patch("src.infrastructure.biometric_auth.is_available", return_value=True), \
             patch("src.infrastructure.biometric_auth.authenticate",
                   side_effect=BiometryAuthError("cancelled")):
            with pytest.raises(PermissionError, match="Biometric"):
                KeychainCredentialStore(require_biometric=True)

    def test_gate_silently_passes_on_biometric_unavailable_error(self):
        """BiometryUnavailableError from authenticate() is silently swallowed."""
        from src.infrastructure.biometric_auth import BiometryUnavailableError
        with patch("src.infrastructure.biometric_auth.authenticate",
                   side_effect=BiometryUnavailableError("no hw")), \
             patch("keyring.get_password", side_effect=lambda s, k: {
                 "__email__": "a@icloud.com", "__app_password__": "pw"
             }.get(k)):
            # Must NOT raise — Keychain protection is the fallback
            store = KeychainCredentialStore(require_biometric=True)
            assert store.get_username() == "a@icloud.com"

    def test_gate_called_only_once_per_process(self, tmp_path, monkeypatch):
        """Second instantiation must skip the biometric prompt (real session caching)."""
        import src.infrastructure.biometric_auth as ba

        # Redirect session file so the test is hermetic
        monkeypatch.setattr(ba, "_SESSION_FILE", tmp_path / ".session-token")
        monkeypatch.setattr(ba, "_CACHE_DIR", tmp_path)

        mock_result = MagicMock()
        mock_result.returncode = 0

        with patch.object(ba, "build_helper", return_value=True), \
             patch("src.infrastructure.biometric_auth.subprocess.run",
                   return_value=mock_result) as mock_run, \
             patch("keyring.get_password", side_effect=lambda s, k: {
                 "__email__": "a@icloud.com", "__app_password__": "pw"
             }.get(k)):
            # First init: Touch ID prompt → subprocess.run called once
            KeychainCredentialStore(require_biometric=True)
            # Second init: in-memory session valid → subprocess.run NOT called again
            KeychainCredentialStore(require_biometric=True)

        assert mock_run.call_count == 1, "Biometric subprocess should only be called once per session"


# ── biometric_auth module ─────────────────────────────────────────────────────


class TestBiometricAuth:
    def test_is_available_returns_false_when_swiftc_missing(self):
        from src.infrastructure import biometric_auth as ba

        with patch.object(ba, "build_helper", return_value=False):
            assert ba.is_available() is False

    def test_authenticate_returns_true_if_already_authenticated(self):
        from src.infrastructure import biometric_auth as ba

        ba._SESSION_AUTHENTICATED = True
        result = ba.authenticate()
        assert result is True

    def test_authenticate_raises_unavailable_when_returncode_2(self):
        from src.infrastructure import biometric_auth as ba
        from src.infrastructure.biometric_auth import BiometryUnavailableError

        ba._SESSION_AUTHENTICATED = False
        mock_result = MagicMock()
        mock_result.returncode = 2

        # Patch build_helper to True AND subprocess.run to simulate exit(2)
        with patch.object(ba, "build_helper", return_value=True), \
             patch("src.infrastructure.biometric_auth.subprocess.run",
                   return_value=mock_result):
            with pytest.raises(BiometryUnavailableError):
                ba.authenticate()

    def test_authenticate_raises_auth_error_when_returncode_1(self):
        from src.infrastructure import biometric_auth as ba
        from src.infrastructure.biometric_auth import BiometryAuthError

        ba._SESSION_AUTHENTICATED = False
        mock_result = MagicMock()
        mock_result.returncode = 1

        with patch.object(ba, "build_helper", return_value=True), \
             patch("src.infrastructure.biometric_auth.subprocess.run",
                   return_value=mock_result):
            with pytest.raises(BiometryAuthError):
                ba.authenticate()

    def test_authenticate_caches_success(self):
        from src.infrastructure import biometric_auth as ba

        ba._SESSION_AUTHENTICATED = False
        mock_result = MagicMock()
        mock_result.returncode = 0

        with patch.object(ba, "build_helper", return_value=True), \
             patch("src.infrastructure.biometric_auth.subprocess.run",
                   return_value=mock_result):
            result = ba.authenticate()

        assert result is True
        assert ba._SESSION_AUTHENTICATED is True

    def test_reset_session_clears_state(self):
        from src.infrastructure import biometric_auth as ba

        ba._SESSION_AUTHENTICATED = True
        ba.reset_session()
        assert ba._SESSION_AUTHENTICATED is False
