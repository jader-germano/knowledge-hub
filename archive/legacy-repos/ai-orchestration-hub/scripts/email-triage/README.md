# Email Daily Triage

Script standalone de triagem de e-mail Gmail. Compativel com Codex CLI e Claude Code.

## Setup

```bash
pip3 install -r requirements.txt
```

### Credenciais OAuth2

1. Acesse [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Crie um OAuth 2.0 Client ID (tipo Desktop)
3. Baixe o `credentials.json`
4. Coloque em `~/.config/email-triage/credentials.json`

```bash
python3 email_triage.py --auth   # Primeira autenticacao
```

## Uso

```bash
python3 email_triage.py              # Executa triagem e cria draft
python3 email_triage.py --dry-run    # Preview sem criar draft
python3 email_triage.py --max 100    # Processa ate 100 e-mails
```

## Codex CLI

```bash
codex run "Execute python3 /path/to/email_triage.py"
```

## Auditoria

Logs em `~/.config/email-triage/logs/triage-YYYY-MM-DD.json` (sem PII, LGPD compliant).
