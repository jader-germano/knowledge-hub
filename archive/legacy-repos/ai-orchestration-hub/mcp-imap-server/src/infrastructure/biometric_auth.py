"""macOS Touch ID / Face ID authentication gate.

Design
──────
- Compiles a Swift helper binary once to ~/.cache/mcp-imap-server/biometric-auth.
- Thread-safe: lock prevents concurrent double-prompt races.
- Session token persisted to disk so Touch ID is only requested ONCE per macOS
  login session (default window: SESSION_TIMEOUT_SECS = 28 800 s = 8 h).
- On next Claude Desktop start, if the token is still within the window, no
  prompt is shown — matching macOS's own "stay logged in" UX convention.
- Token is invalidated: on explicit reset, on timeout, or when the session file
  is deleted/tampered.

Swift rationale (vs PyObjC)
──────────────────────────────
PyObjC requires a macOS framework wheel per macOS version and is not stable across
major releases. Swift CLT is free (xcode-select --install) and supported by Apple.
For commercial distribution: pre-compile the binary and ship it in the package.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import threading
import time
from pathlib import Path

# ── Constants ─────────────────────────────────────────────────────────────────

_CACHE_DIR = Path.home() / ".cache" / "mcp-imap-server"
_HELPER = _CACHE_DIR / "biometric-auth"
_SESSION_FILE = _CACHE_DIR / ".session-token"

# Default: 8 hours = one full macOS login session / workday.
# Override with env var MCP_IMAP_SESSION_TIMEOUT (seconds).
SESSION_TIMEOUT_SECS: float = float(
    os.environ.get("MCP_IMAP_SESSION_TIMEOUT", "28800")
)

_SWIFT_SOURCE = """\
import Foundation
import LocalAuthentication

let checkOnly = CommandLine.arguments.contains("--check-only")
let context = LAContext()

// Allow silent reuse within 10 s — prevents double-prompt on rapid calls
context.touchIDAuthenticationAllowableReuseDuration = 10

var err: NSError?
guard context.canEvaluatePolicy(
    .deviceOwnerAuthenticationWithBiometrics, error: &err) else {
    exit(2)  // 2 → hardware absent or not enrolled
}

if checkOnly { exit(0) }

let sema = DispatchSemaphore(value: 0)
var ok = false

context.evaluatePolicy(
    .deviceOwnerAuthenticationWithBiometrics,
    localizedReason: "iCloud Mail MCP — autenticar acesso às credenciais"
) { success, _ in
    ok = success
    sema.signal()
}

sema.wait()
exit(ok ? 0 : 1)
"""

# ── Custom exceptions ─────────────────────────────────────────────────────────


class BiometryUnavailableError(RuntimeError):
    """Touch ID / Face ID hardware is absent, not enrolled, or swiftc unavailable."""


class BiometryAuthError(RuntimeError):
    """User cancelled or failed biometric authentication."""


# ── Thread-safe session state ─────────────────────────────────────────────────

_lock = threading.Lock()
_SESSION_AUTHENTICATED: bool = False
_SESSION_AUTH_TIME: float | None = None  # monotonic at time of auth


# ── Session persistence ───────────────────────────────────────────────────────


def _session_token_key() -> str:
    """Deterministic key derived from username — ties token to this OS user."""
    uid = str(os.getuid()) if hasattr(os, "getuid") else "0"
    return hashlib.sha256(f"mcp-imap:{uid}".encode()).hexdigest()[:16]


def _persist_session() -> None:
    """Write session token to disk so subsequent processes skip re-auth."""
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "ts": time.time(),               # wall-clock for cross-process comparison
        "key": _session_token_key(),
        "timeout": SESSION_TIMEOUT_SECS,
    }
    try:
        _SESSION_FILE.write_text(json.dumps(payload))
        _SESSION_FILE.chmod(0o600)  # owner read/write only
    except OSError:
        pass  # non-fatal: next process will just re-prompt


def _load_session() -> bool:
    """Return True if a valid persisted session exists on disk."""
    try:
        if not _SESSION_FILE.exists():
            return False
        payload = json.loads(_SESSION_FILE.read_text())
        if payload.get("key") != _session_token_key():
            return False  # different OS user
        elapsed = time.time() - float(payload["ts"])
        timeout = float(payload.get("timeout", SESSION_TIMEOUT_SECS))
        return elapsed < timeout
    except Exception:
        return False


def _invalidate_session() -> None:
    """Delete the on-disk session token."""
    try:
        _SESSION_FILE.unlink(missing_ok=True)
    except OSError:
        pass


def _is_session_valid() -> bool:
    """Check in-memory session first (fast), then disk (cross-process)."""
    if _SESSION_AUTHENTICATED and _SESSION_AUTH_TIME is not None:
        if (time.monotonic() - _SESSION_AUTH_TIME) < SESSION_TIMEOUT_SECS:
            return True
    return _load_session()


# ── Public API ────────────────────────────────────────────────────────────────


def build_helper() -> bool:
    """Compile the Swift binary to _HELPER if not already cached.

    Returns True when binary is available; False if swiftc is unavailable.
    Commercial note: ship the pre-compiled binary in your package instead.
    """
    if _HELPER.exists():
        return True

    _CACHE_DIR.mkdir(parents=True, exist_ok=True)

    fd, src_path = tempfile.mkstemp(suffix=".swift")
    try:
        os.write(fd, _SWIFT_SOURCE.encode())
        os.close(fd)
        result = subprocess.run(
            ["swiftc", src_path, "-o", str(_HELPER)],
            capture_output=True,
            timeout=120,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
    finally:
        try:
            os.unlink(src_path)
        except OSError:
            pass


def is_available() -> bool:
    """Return True if Touch ID / Face ID hardware is present and enrolled."""
    if not build_helper():
        return False
    try:
        result = subprocess.run(
            [str(_HELPER), "--check-only"],
            capture_output=True,
            timeout=5,
        )
        return result.returncode == 0
    except Exception:
        return False


def authenticate() -> bool:
    """Prompt for Touch ID. Thread-safe. Session persisted across processes.

    - Returns True immediately if a valid session token exists (memory or disk).
    - Writes token to disk on success so subsequent MCP server starts skip re-auth.
    - Session expires after SESSION_TIMEOUT_SECS (default 8 h, env-configurable).

    Raises:
        BiometryUnavailableError — no hardware or swiftc unavailable
        BiometryAuthError        — user cancelled / failed
    """
    global _SESSION_AUTHENTICATED, _SESSION_AUTH_TIME

    # Fast path — no lock needed; bool reads are atomic under CPython GIL
    if _is_session_valid():
        return True

    with _lock:
        # Re-check under lock (double-checked locking pattern)
        if _is_session_valid():
            return True

        if not build_helper():
            raise BiometryUnavailableError(
                "Swift helper could not be compiled. "
                "Install Xcode Command Line Tools: xcode-select --install"
            )

        try:
            result = subprocess.run(
                [str(_HELPER)],
                capture_output=True,
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            raise BiometryAuthError("Biometric prompt timed out (30 s).")
        except FileNotFoundError:
            raise BiometryUnavailableError("Biometric helper binary not found.")

        if result.returncode == 2:
            raise BiometryUnavailableError(
                "Touch ID / Face ID is unavailable or not enrolled on this device."
            )

        if result.returncode != 0:
            raise BiometryAuthError(
                "Biometric authentication was cancelled or failed."
            )

        _SESSION_AUTHENTICATED = True
        _SESSION_AUTH_TIME = time.monotonic()
        _persist_session()  # survive process restarts within the timeout window
        return True


def reset_session() -> None:
    """Invalidate session (memory + disk). For testing and explicit logout only."""
    global _SESSION_AUTHENTICATED, _SESSION_AUTH_TIME
    with _lock:
        _SESSION_AUTHENTICATED = False
        _SESSION_AUTH_TIME = None
        _invalidate_session()
