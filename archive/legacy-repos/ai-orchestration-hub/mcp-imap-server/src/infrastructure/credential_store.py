"""Environment-based CredentialStore — reads secrets from OS env vars only.

Security contract:
- Credentials are NEVER logged, serialised or stored beyond process lifetime.
- Raises KeyError with a clear message when a required var is missing so the
  operator knows exactly what to set, without leaking a partial value.
- use_ssl defaults to True (STARTTLS/TLS); must be explicitly disabled.
"""

from __future__ import annotations

import os

from ..domain.ports import CredentialStore

_REQUIRED = ("ICLOUD_EMAIL", "ICLOUD_APP_PASSWORD")
_DEFAULTS = {
    "IMAP_HOST": "imap.mail.me.com",
    "IMAP_PORT": "993",
    "IMAP_SSL": "true",
}


class EnvCredentialStore(CredentialStore):
    """Reads IMAP credentials exclusively from environment variables.

    Required env vars:
        ICLOUD_EMAIL          — IMAP username (e.g. user@icloud.com)
        ICLOUD_APP_PASSWORD   — Apple app-specific password (NOT your Apple ID password)

    Optional env vars (with iCloud defaults):
        IMAP_HOST   — default: imap.mail.me.com
        IMAP_PORT   — default: 993
        IMAP_SSL    — default: true
    """

    def __init__(self) -> None:
        missing = [v for v in _REQUIRED if not os.environ.get(v)]
        if missing:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing)}. "
                "Set them before starting the MCP server."
            )

    def get_host(self) -> str:
        return os.environ.get("IMAP_HOST", _DEFAULTS["IMAP_HOST"])

    def get_port(self) -> int:
        return int(os.environ.get("IMAP_PORT", _DEFAULTS["IMAP_PORT"]))

    def get_username(self) -> str:
        return os.environ["ICLOUD_EMAIL"]

    def get_password(self) -> str:
        return os.environ["ICLOUD_APP_PASSWORD"]

    def use_ssl(self) -> bool:
        return os.environ.get("IMAP_SSL", _DEFAULTS["IMAP_SSL"]).lower() == "true"
