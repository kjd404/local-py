"""Utilities for polling Gmail for new messages."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

TOKEN_PATH = Path(os.environ.get("GMAIL_TOKEN_PATH", "token.json"))
CREDENTIALS_PATH = Path(
    os.environ.get(
        "GMAIL_CREDENTIALS_FILE", str(Path(__file__).with_name("credentials.json"))
    )
)
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


@dataclass
class Email:
    """Simple representation of an email message."""

    id: str
    snippet: str


class GmailPoller:
    """Polls the Gmail API for messages from a specific sender."""

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

    def poll(self, sender: str) -> List[Email]:
        """Return unread messages from the given sender.

        Messages are marked as read so they are not returned again.
        """
        result = (
            self.service.users()
            .messages()
            .list(userId="me", q=f"from:{sender} is:unread")
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
