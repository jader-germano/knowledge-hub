"""CLI for one-time iCloud credential enrollment in macOS Keychain.

Commands
────────
  mcp-imap-setup              Interactive enrollment (email + app-specific password)
  mcp-imap-setup --check      Verify enrollment status and biometric availability
  mcp-imap-setup --revoke     Remove credentials from Keychain

App-Specific Password
─────────────────────
  Apple ID password ≠ app-specific password.
  Generate one at: https://appleid.apple.com → Security → App passwords
  Label it "iCloud Mail MCP" for traceability.
"""

from __future__ import annotations

import getpass
import sys
from textwrap import dedent


# ── Entry point ───────────────────────────────────────────────────────────────


def main() -> None:
    args = sys.argv[1:]

    if "--revoke" in args:
        _revoke()
    elif "--check" in args:
        _check()
    else:
        _enroll()


# ── Commands ──────────────────────────────────────────────────────────────────


def _enroll() -> None:
    _header()

    # ── Step 1: Build biometric helper ──────────────────────────────────────
    from ..infrastructure.biometric_auth import build_helper, is_available

    print("→ Compilando helper de autenticação biométrica (Touch ID)…")
    compiled = build_helper()

    if compiled:
        if is_available():
            print("  ✅ Touch ID detectado e disponível\n")
        else:
            print("  ℹ️  Touch ID indisponível neste dispositivo")
            print("     → Keychain será protegido pela senha do sistema macOS\n")
    else:
        print("  ⚠️  Não foi possível compilar o helper Swift.")
        print("     Verifique se o Xcode Command Line Tools está instalado:")
        print("     xcode-select --install\n")
        print("     → Continuando sem autenticação biométrica\n")

    # ── Step 2: Prompt for credentials ──────────────────────────────────────
    print("Insira as credenciais do iCloud Mail:\n")

    email = input("  Email iCloud (ex: user@icloud.com): ").strip()
    if not email or "@" not in email:
        _abort("Email inválido.")

    print(
        dedent("""
        Para gerar uma App-Specific Password:
          1. Acesse: https://appleid.apple.com
          2. Segurança → Senhas de app → Gerar senha
          3. Use o nome: "iCloud Mail MCP"
          4. Copie o código no formato xxxx-xxxx-xxxx-xxxx
        """).rstrip()
    )

    app_password = getpass.getpass("\n  App-Specific Password: ").strip()
    if not app_password:
        _abort("A senha não pode estar vazia.")

    # Basic format validation (xxxx-xxxx-xxxx-xxxx)
    parts = app_password.replace(" ", "-").split("-")
    if len(parts) != 4 or not all(len(p) == 4 and p.isalnum() for p in parts):
        print(
            "  ⚠️  O formato esperado é xxxx-xxxx-xxxx-xxxx (letras ou dígitos, 4 grupos de 4)."
        )
        confirm = input("  Continuar mesmo assim? [s/N]: ").strip().lower()
        if confirm != "s":
            _abort("Operação cancelada pelo usuário.")

    # ── Step 3: Store in Keychain ────────────────────────────────────────────
    print("\n→ Armazenando credenciais no Keychain do macOS…")
    from ..infrastructure.keychain_store import KeychainCredentialStore

    try:
        KeychainCredentialStore.enroll(email=email, app_password=app_password)
    except Exception as exc:
        _abort(f"Erro ao salvar no Keychain: {exc}")

    # ── Step 4: Verify ───────────────────────────────────────────────────────
    if not KeychainCredentialStore.is_enrolled():
        _abort("Verificação falhou após o salvamento. Tente novamente.")

    print("  ✅ Credenciais armazenadas com sucesso!\n")
    print("─" * 52)
    print("✅ Configuração concluída!")
    print()
    print("   Próximos passos:")
    print("   1. Reinicie o Claude Desktop")
    print("   2. Na próxima triagem, Touch ID será solicitado uma vez")
    print("   3. Para revogar: mcp-imap-setup --revoke")
    print()


def _check() -> None:
    from ..infrastructure.biometric_auth import build_helper, is_available
    from ..infrastructure.keychain_store import KeychainCredentialStore

    _header()
    enrolled = KeychainCredentialStore.is_enrolled()
    built = build_helper()
    biometric = is_available() if built else False

    print(f"  Credenciais no Keychain : {'✅ Sim' if enrolled else '❌ Não (execute mcp-imap-setup)'}")
    print(f"  Helper Swift compilado  : {'✅ Sim' if built else '⚠️  Não (execute mcp-imap-setup)'}")
    print(f"  Touch ID disponível     : {'✅ Sim' if biometric else '❌ Não (usando proteção do Keychain)'}")
    print()

    if not enrolled:
        sys.exit(1)


def _revoke() -> None:
    _header()
    from ..infrastructure.keychain_store import KeychainCredentialStore

    if not KeychainCredentialStore.is_enrolled():
        print("  ℹ️  Nenhuma credencial encontrada no Keychain.")
        return

    confirm = input(
        "  ⚠️  Remover credenciais iCloud do Keychain? [s/N]: "
    ).strip().lower()

    if confirm != "s":
        print("  Operação cancelada.")
        return

    KeychainCredentialStore.revoke()
    print("  ✅ Credenciais removidas do Keychain.")
    print("     Execute 'mcp-imap-setup' para re-enrollar.")


# ── Helpers ───────────────────────────────────────────────────────────────────


def _header() -> None:
    print()
    print("╔══════════════════════════════════════════════════╗")
    print("║   iCloud Mail MCP — Gerenciamento de Credenciais  ║")
    print("╚══════════════════════════════════════════════════╝")
    print()


def _abort(message: str) -> None:
    print(f"\n❌ {message}")
    sys.exit(1)


if __name__ == "__main__":
    main()
