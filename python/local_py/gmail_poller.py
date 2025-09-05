"""Utilities for polling Gmail for new messages."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Optional

import httplib2
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google_auth_httplib2 import AuthorizedHttp
from semantic_kernel.functions import kernel_function

TOKEN_PATH = Path(os.environ.get("GMAIL_TOKEN_PATH", "token.json"))
# Copy credentials.sample.json to credentials.json and fill in your
# OAuth credentials.
CREDENTIALS_PATH = Path(
    os.environ.get(
        "GMAIL_CREDENTIALS_FILE",
        str(Path(__file__).resolve().parent.parent / "credentials.json"),
    )
)
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


@dataclass
class Email:
    """Simple representation of an email message."""

    id: str
    snippet: str


class GmailPoller:
    """Poll the Gmail API for unread messages, optionally filtered by sender."""

    def __init__(
        self,
        *,
        token_path: Path | str = TOKEN_PATH,
        credentials_path: Path | str = CREDENTIALS_PATH,
        service: Any | None = None,
        timeout: float = 10.0,
    ) -> None:
        """Create a new :class:`GmailPoller`.

        Args:
            token_path: Path to the OAuth token JSON file. Defaults to
                :data:`TOKEN_PATH`.
            credentials_path: Path to the OAuth client credentials. Defaults to
                :data:`CREDENTIALS_PATH`.
            service: Pre-authorized Gmail API service. If provided, authorization
                is skipped.
            timeout: Timeout in seconds for Gmail API requests.
        """

        self.token_path = Path(token_path)
        self.credentials_path = Path(credentials_path)
        self.timeout = timeout
        self.service: Any = service or self._authorize(
            self.token_path, self.credentials_path, timeout
        )

    @staticmethod
    def _authorize(token_path: Path, credentials_path: Path, timeout: float) -> Any:
        """Return an authorized Gmail API service."""
        creds: Credentials | None = None
        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(credentials_path), SCOPES
                )
                creds = flow.run_local_server(port=0)
            token_path.write_text(creds.to_json())
        authed_http = AuthorizedHttp(creds, http=httplib2.Http(timeout=timeout))
        return build("gmail", "v1", http=authed_http)

    @kernel_function(
        description="Poll Gmail for unread messages, optionally filtered by sender."
    )
    def poll(self, sender: Optional[str] = None) -> List[Email]:
        """Return unread messages.

        If *sender* is provided, only messages from that address are returned.
        Messages are marked as read so they are not returned again.
        """
        query = f"from:{sender} is:unread" if sender else "is:unread"
        try:
            result = (
                self.service.users().messages().list(userId="me", q=query).execute()
            )
        except Exception as exc:  # pragma: no cover - network failure
            logging.warning("Failed to poll Gmail: %s", exc)
            return []
        messages = result.get("messages", [])
        emails: List[Email] = []
        for msg in messages:
            full = (
                self.service.users().messages().get(userId="me", id=msg["id"]).execute()
            )
            emails.append(Email(id=full["id"], snippet=full.get("snippet", "")))
            self.service.users().messages().modify(
                userId="me",
                id=full["id"],
                body={"removeLabelIds": ["UNREAD"]},  # pragma: no cover - network
            ).execute()
        return emails
