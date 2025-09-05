"""Script to obtain a Gmail API token.

Usage:
    python get_gmail_token.py --secrets client_secret.json --token token.json
"""
from __future__ import annotations

import argparse
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Gmail OAuth token")
    parser.add_argument(
        "--secrets",
        type=Path,
        required=True,
        help="Path to client secrets JSON",
    )
    parser.add_argument(
        "--token",
        type=Path,
        default=Path("token.json"),
        help="Path to write the OAuth token",
    )
    args = parser.parse_args()

    flow = InstalledAppFlow.from_client_secrets_file(str(args.secrets), SCOPES)
    creds = flow.run_local_server(port=0)
    args.token.write_text(creds.to_json())


if __name__ == "__main__":
    main()
