"""Utilities for polling Gmail for new messages."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from semantic_kernel.functions import kernel_function

TOKEN_PATH = Path(os.environ.get("GMAIL_TOKEN_PATH", "token.json"))
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

    def __init__(self) -> None:
        self.service = self._authorize()

    def _authorize(self):
        creds: Credentials | None = None
        if TOKEN_PATH.exists():
            creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CREDENTIALS_PATH), SCOPES
                )
                creds = flow.run_local_server(port=0)
            TOKEN_PATH.write_text(creds.to_json())
        return build("gmail", "v1", credentials=creds)

    @kernel_function(description="Poll Gmail for unread messages, optionally filtered by sender.")
    def poll(self, sender: Optional[str] = None) -> List[Email]:
        """Return unread messages.

        If *sender* is provided, only messages from that address are returned.
        Messages are marked as read so they are not returned again.
        """
        query = f"from:{sender} is:unread" if sender else "is:unread"
        result = (
            self.service.users()
            .messages()
            .list(userId="me", q=query)
            .execute()
        )
        messages = result.get("messages", [])
        emails: List[Email] = []
        for msg in messages:
            full = self.service.users().messages().get(userId="me", id=msg["id"]).execute()
            emails.append(Email(id=full["id"], snippet=full.get("snippet", "")))
            self.service.users().messages().modify(
                userId="me", id=full["id"], body={"removeLabelIds": ["UNREAD"]}
            ).execute()
        return emails
