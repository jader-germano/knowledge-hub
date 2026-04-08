"""macOS Keychain credential store with Touch ID biometric gate.

Storage layout in Keychain
──────────────────────────
  service  = "icloud-mail-mcp"
  account  = "__email__"         → IMAP username (e.g. jader.germano@icloud.com)
  account  = "__app_password__"  → Apple app-specific password

Auth flow (per process, thread-safe)
──────────────────────────────────────
  1. First call triggers Touch ID via biometric_auth.authenticate().
  2. Session cached for SESSION_TIMEOUT_SECS (default 30 min, configurable).
  3. Concurrent calls are serialised by biometric_auth's internal lock.
  4. If hardware absent: silently degrades to Keychain-only protection.
  5. BiometryAuthError (cancel/fail) → raises PermissionError to caller.
     It is NOT silently bypassed — this was a prior security regression.

Requires:
  keyring >= 25.0  (pip install keyring)
  swiftc           (Xcode CLT: xcode-select --install)
"""

from __future__ import annotations

from keyring.errors import KeyringError

from ..domain.ports import CredentialStore

_SERVICE = "icloud-mail-mcp"
_KEY_EMAIL = "__email__"
_KEY_PASSWORD = "__app_password__"


def _gate_biometric() -> None:
    """Authenticate with Touch ID. Delegates entirely to biometric_auth.

    Graceful degradation:
      - BiometryUnavailableError → silent pass (Keychain protects the secret).
      - BiometryAuthError        → re-raised as PermissionError (no bypass).
    """
    from .biometric_auth import BiometryAuthError, BiometryUnavailableError, authenticate

    try:
        authenticate()
    except BiometryUnavailableError:
        # No Touch ID hardware or swiftc not installed.
        # Keychain OS-level encryption is the fallback security boundary.
        pass
    except BiometryAuthError as exc:
        raise PermissionError(
            "Biometric authentication failed or was cancelled. "
            "Cannot access iCloud credentials in Keychain."
        ) from exc


class KeychainCredentialStore(CredentialStore):
    """IMAP credentials from macOS Keychain, gated by Touch ID.

    Raises:
        EnvironmentError:  credentials not enrolled — run `mcp-imap-setup`
        PermissionError:   Touch ID cancelled by user
        KeyringError:      OS-level Keychain access failure
    """

    _HOST = "imap.mail.me.com"
    _PORT = 993
    _SSL = True

    def __init__(self, require_biometric: bool = True) -> None:
        if require_biometric:
            _gate_biometric()

        self._email = self._fetch("email", _KEY_EMAIL)
        self._password = self._fetch("app password", _KEY_PASSWORD)

    # ── CredentialStore interface ─────────────────────────────────────────────

    def get_host(self) -> str:
        return self._HOST

    def get_port(self) -> int:
        return self._PORT

    def get_username(self) -> str:
        return self._email

    def get_password(self) -> str:
        return self._password

    def use_ssl(self) -> bool:
        return self._SSL

    # ── Keychain lifecycle (called by setup CLI) ──────────────────────────────

    @classmethod
    def enroll(cls, email: str, app_password: str) -> None:
        """Store credentials in macOS Keychain. Called once during setup."""
        import keyring

        keyring.set_password(_SERVICE, _KEY_EMAIL, email)
        keyring.set_password(_SERVICE, _KEY_PASSWORD, app_password)

    @classmethod
    def is_enrolled(cls) -> bool:
        """True if both credentials are present in Keychain."""
        import keyring

        try:
            return bool(
                keyring.get_password(_SERVICE, _KEY_EMAIL)
                and keyring.get_password(_SERVICE, _KEY_PASSWORD)
            )
        except KeyringError:
            return False

    @classmethod
    def revoke(cls) -> None:
        """Remove both credentials from Keychain."""
        import keyring

        for key in (_KEY_EMAIL, _KEY_PASSWORD):
            try:
                keyring.delete_password(_SERVICE, key)
            except KeyringError:
                pass

    # ── Private ───────────────────────────────────────────────────────────────

    @staticmethod
    def _fetch(label: str, key: str) -> str:
        import keyring

        try:
            value = keyring.get_password(_SERVICE, key)
        except KeyringError as exc:
            raise EnvironmentError(
                f"Cannot read iCloud {label} from Keychain. "
                f"Run 'mcp-imap-setup' to enroll credentials. Details: {exc}"
            ) from exc

        if not value:
            raise EnvironmentError(
                f"iCloud {label} not found in Keychain. "
                "Run 'mcp-imap-setup' to enroll credentials."
            )
        return value


def _reset_process_auth() -> None:
    """Reset biometric gate. TESTING ONLY — delegates to biometric_auth.reset_session."""
    from .biometric_auth import reset_session
    reset_session()
