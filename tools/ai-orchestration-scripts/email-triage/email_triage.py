"""
Email Daily Triage — Standalone Script
Compatible with Codex CLI and Claude Code.

Reads unread Gmail messages, classifies them, and creates a summary draft.
Uses Gmail API via OAuth2 (credentials.json required).

Usage:
    python3 email_triage.py                # Run triage
    python3 email_triage.py --dry-run      # Preview without creating draft
    python3 email_triage.py --auth          # First-time OAuth setup
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Protocol

# --- Domain Layer ---

class Category(Enum):
    CONTRATO_ACAO = "CONTRATO/ACAO"
    INFORMATIVO = "INFORMATIVO"
    DESCARTAVEL = "DESCARTAVEL"


@dataclass
class EmailMessage:
    message_id: str
    thread_id: str
    sender: str
    sender_email: str
    subject: str
    snippet: str
    labels: list[str]
    date: str

    @property
    def sender_domain(self) -> str:
        match = re.search(r"@([\w.-]+)", self.sender_email)
        return match.group(1).lower() if match else ""

    @property
    def display_sender(self) -> str:
        match = re.match(r'"?([^"<]+)"?\s*<', self.sender)
        return match.group(1).strip() if match else self.sender_email.split("@")[0]


@dataclass
class ClassifiedEmail:
    email: EmailMessage
    category: Category
    reason: str


@dataclass
class TriageReport:
    date: str
    classified: list[ClassifiedEmail] = field(default_factory=list)
    total_unread: int = 0

    @property
    def by_category(self) -> dict[Category, list[ClassifiedEmail]]:
        result: dict[Category, list[ClassifiedEmail]] = {c: [] for c in Category}
        for item in self.classified:
            result[item.category].append(item)
        return result


# --- Application Layer (Classification Rules) ---

CONTRATO_DOMAINS = [
    "tse.jus.br",
]

ACAO_KEYWORDS_SUBJECT = [
    "action required", "billing", "pagamento", "vencimento",
    "cobranca", "cobrança", "suspended", "urgente", "prazo",
    "obrigatorio", "obrigatório", "payment", "fatura", "pendente",
    "agendamento", "exame",
]

DESCARTAVEL_KEYWORDS_SUBJECT = [
    "last chance", "limited time", "% off", "don't miss",
    "act now", "unsubscribe", "oferta especial", "promocao",
    "promoção", "desconto",
]

DESCARTAVEL_SENDER_PATTERNS = [
    r"^noreply@",
    r"^no-reply@",
    r"^team@mail\.",
    r"@mail\.\w+\.\w+",
    r"@marketing\.",
    r"@novidades\.",
    r"@r\.mercadopago",
    r"@promocion@",
]


class EmailClassifier:
    """Classifies emails into triage categories using rule-based logic."""

    def classify(self, email: EmailMessage) -> ClassifiedEmail:
        if self._is_contrato_acao(email):
            return ClassifiedEmail(email, Category.CONTRATO_ACAO, "contrato/acao match")
        if self._is_descartavel(email):
            return ClassifiedEmail(email, Category.DESCARTAVEL, "descartavel match")
        return ClassifiedEmail(email, Category.INFORMATIVO, "default")

    def _is_contrato_acao(self, email: EmailMessage) -> bool:
        if any(email.sender_domain.endswith(d) for d in CONTRATO_DOMAINS):
            return True
        subject_lower = email.subject.lower()
        snippet_lower = email.snippet.lower()
        combined = subject_lower + " " + snippet_lower
        return any(kw in combined for kw in ACAO_KEYWORDS_SUBJECT)

    def _is_descartavel(self, email: EmailMessage) -> bool:
        if "CATEGORY_PROMOTIONS" in email.labels:
            return True
        subject_lower = email.subject.lower()
        if any(kw in subject_lower for kw in DESCARTAVEL_KEYWORDS_SUBJECT):
            return True
        email_addr = email.sender_email.lower()
        return any(re.search(p, email_addr) for p in DESCARTAVEL_SENDER_PATTERNS)


# --- Infrastructure Layer (Gmail API) ---

class GmailGateway(Protocol):
    def search_unread(self, max_results: int) -> list[EmailMessage]: ...
    def create_draft(self, to: str, subject: str, body_html: str) -> str: ...


class GmailApiGateway:
    """Gmail API gateway using google-auth + google-api-python-client."""

    SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.compose",
    ]

    def __init__(self, credentials_path: str | None = None):
        self._credentials_path = credentials_path or self._default_credentials_path()
        self._service = None

    def _default_credentials_path(self) -> str:
        return str(Path.home() / ".config" / "email-triage" / "credentials.json")

    def _token_path(self) -> str:
        return str(Path(self._credentials_path).parent / "token.json")

    def _get_service(self):
        if self._service:
            return self._service

        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build

        creds = None
        token_path = self._token_path()

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self._credentials_path):
                    print(f"ERROR: credentials.json not found at {self._credentials_path}")
                    print("Download from Google Cloud Console > APIs & Services > Credentials")
                    print(f"Place at: {self._credentials_path}")
                    sys.exit(1)
                flow = InstalledAppFlow.from_client_secrets_file(
                    self._credentials_path, self.SCOPES
                )
                creds = flow.run_local_server(port=0)

            os.makedirs(os.path.dirname(token_path), exist_ok=True)
            with open(token_path, "w") as f:
                f.write(creds.to_json())

        self._service = build("gmail", "v1", credentials=creds)
        return self._service

    def search_unread(self, max_results: int = 50) -> list[EmailMessage]:
        service = self._get_service()
        results = (
            service.users()
            .messages()
            .list(userId="me", q="is:unread in:inbox", maxResults=max_results)
            .execute()
        )
        messages_data = results.get("messages", [])
        emails: list[EmailMessage] = []

        for msg_ref in messages_data:
            msg = (
                service.users()
                .messages()
                .get(userId="me", id=msg_ref["id"], format="metadata",
                     metadataHeaders=["From", "Subject", "Date"])
                .execute()
            )
            headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
            sender_raw = headers.get("From", "")
            sender_email_match = re.search(r"<([^>]+)>", sender_raw)
            sender_email = sender_email_match.group(1) if sender_email_match else sender_raw

            emails.append(EmailMessage(
                message_id=msg["id"],
                thread_id=msg["threadId"],
                sender=sender_raw,
                sender_email=sender_email,
                subject=headers.get("Subject", "(sem assunto)"),
                snippet=msg.get("snippet", ""),
                labels=msg.get("labelIds", []),
                date=headers.get("Date", ""),
            ))

        return emails

    def get_total_unread(self) -> int:
        service = self._get_service()
        results = (
            service.users()
            .messages()
            .list(userId="me", q="is:unread in:inbox", maxResults=1)
            .execute()
        )
        return results.get("resultSizeEstimate", 0)

    def create_draft(self, to: str, subject: str, body_html: str) -> str:
        import base64
        from email.mime.text import MIMEText

        service = self._get_service()
        message = MIMEText(body_html, "html")
        message["to"] = to
        message["subject"] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        draft = (
            service.users()
            .drafts()
            .create(userId="me", body={"message": {"raw": raw}})
            .execute()
        )
        return draft["id"]


# --- Presentation Layer (Report Builder) ---

class ReportBuilder:
    """Builds HTML report from TriageReport."""

    CATEGORY_COLORS = {
        Category.CONTRATO_ACAO: "#d32f2f",
        Category.INFORMATIVO: "#1565c0",
        Category.DESCARTAVEL: "#757575",
    }

    def build_html(self, report: TriageReport) -> str:
        by_cat = report.by_category
        sections = []

        for cat in Category:
            items = by_cat[cat]
            color = self.CATEGORY_COLORS[cat]
            grouped = self._group_by_sender(items)

            section = f'<h3 style="color: {color};">{cat.value} ({len(items)} e-mails)</h3>\n<ol>\n'
            for entry in grouped:
                section += f"<li>{entry}</li>\n"
            if not grouped:
                section += "<li><i>Nenhum e-mail nesta categoria</i></li>\n"
            section += "</ol>\n"
            sections.append(section)

        total = len(report.classified)
        highlights = self._build_highlights(by_cat[Category.CONTRATO_ACAO])

        return f"""<h2>Triagem Inbox - {report.date}</h2>

{''.join(sections)}

<hr>
{highlights}
<p><b>Total processado:</b> {total} e-mails{f' (de ~{report.total_unread} nao lidos)' if report.total_unread > total else ''}</p>
<p><b>Sugestao:</b> E-mails "DESCARTAVEL" podem ser arquivados sem acao.</p>
<p style="font-size: 11px; color: #999;">Gerado automaticamente — {report.date}</p>"""

    def _group_by_sender(self, items: list[ClassifiedEmail]) -> list[str]:
        sender_groups: dict[str, list[ClassifiedEmail]] = {}
        for item in items:
            key = item.email.display_sender
            sender_groups.setdefault(key, []).append(item)

        result = []
        for sender, group in sender_groups.items():
            if len(group) == 1:
                e = group[0].email
                result.append(f"<b>[{sender}]</b> {e.subject} — <i>{e.snippet[:100]}</i>")
            else:
                subjects = ", ".join(e.email.subject[:50] for e in group[:3])
                result.append(f"<b>[{sender}]</b> {len(group)}x — <i>{subjects}</i>")
        return result

    def _build_highlights(self, acao_items: list[ClassifiedEmail]) -> str:
        if not acao_items:
            return ""
        lines = []
        for item in acao_items[:5]:
            e = item.email
            lines.append(f'<li style="color: #d32f2f;"><b>[{e.display_sender}]</b> {e.subject[:80]}</li>')
        return f"<p><b>Destaques criticos:</b></p>\n<ul>\n{''.join(lines)}\n</ul>\n"


# --- Use Case Orchestrator ---

class EmailTriageUseCase:
    """Orchestrates the full triage flow."""

    TARGET_EMAIL = "jader.gp15@gmail.com"

    def __init__(self, gateway: GmailApiGateway, classifier: EmailClassifier,
                 report_builder: ReportBuilder):
        self._gateway = gateway
        self._classifier = classifier
        self._report_builder = report_builder

    def execute(self, dry_run: bool = False, max_results: int = 50) -> TriageReport:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        print(f"[triage] Buscando ate {max_results} e-mails nao lidos...")

        emails = self._gateway.search_unread(max_results=max_results)
        total_unread = self._gateway.get_total_unread()

        print(f"[triage] {len(emails)} e-mails obtidos (total nao lidos: ~{total_unread})")

        report = TriageReport(date=today, total_unread=total_unread)
        for email in emails:
            classified = self._classifier.classify(email)
            report.classified.append(classified)

        by_cat = report.by_category
        for cat in Category:
            print(f"  {cat.value}: {len(by_cat[cat])}")

        html = self._report_builder.build_html(report)

        if dry_run:
            print("\n[dry-run] HTML do resumo:")
            print(html)
            print("\n[dry-run] Draft NAO criado.")
        else:
            subject = f"[Triagem Inbox] Resumo {today}"
            draft_id = self._gateway.create_draft(self.TARGET_EMAIL, subject, html)
            print(f"\n[triage] Draft criado: {draft_id}")
            print(f"[triage] Assunto: {subject}")

        return report


# --- Audit Log ---

def write_audit_log(report: TriageReport, log_dir: str | None = None):
    """Writes a minimal audit log (no PII, LGPD compliant)."""
    log_dir = log_dir or str(Path.home() / ".config" / "email-triage" / "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "date": report.date,
        "total_processed": len(report.classified),
        "total_unread": report.total_unread,
        "counts": {cat.value: len(items) for cat, items in report.by_category.items()},
    }
    log_path = os.path.join(log_dir, f"triage-{report.date}.json")
    with open(log_path, "w") as f:
        json.dump(log_entry, f, indent=2)
    print(f"[audit] Log salvo: {log_path}")


# --- CLI Entry Point ---

def main():
    parser = argparse.ArgumentParser(description="Email Daily Triage")
    parser.add_argument("--dry-run", action="store_true", help="Preview without creating draft")
    parser.add_argument("--auth", action="store_true", help="Run OAuth setup only")
    parser.add_argument("--max", type=int, default=50, help="Max emails to process (default: 50)")
    parser.add_argument("--credentials", type=str, help="Path to credentials.json")
    args = parser.parse_args()

    gateway = GmailApiGateway(credentials_path=args.credentials)

    if args.auth:
        print("[auth] Iniciando autenticacao OAuth2...")
        gateway._get_service()
        print("[auth] Autenticacao concluida com sucesso.")
        return

    classifier = EmailClassifier()
    report_builder = ReportBuilder()
    use_case = EmailTriageUseCase(gateway, classifier, report_builder)

    report = use_case.execute(dry_run=args.dry_run, max_results=args.max)
    write_audit_log(report)

    print(f"\n[done] Triagem concluida: {report.date}")


if __name__ == "__main__":
    main()
