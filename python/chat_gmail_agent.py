"""Interactive chat agent that can poll Gmail using OpenAI tool calls."""

from __future__ import annotations

import json
import logging
import os
from dataclasses import asdict
from typing import Any, Callable, List

from openai import OpenAI

from local_py.gmail_poller import Email, GmailPoller


# Description of the Gmail poll function exposed to the model.
GMAIL_POLL_TOOL = [
    {
        "type": "function",
        "function": {
            "name": "gmail_poll",
            "description": (
                "Poll Gmail for unread messages, optionally filtered by sender."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "sender": {
                        "type": "string",
                        "description": "Only return unread emails from this address.",
                    }
                },
            },
        },
    }
]


class ChatGmailAgent:
    """Chat agent that can poll Gmail via tool calls."""

    def __init__(self, poller: GmailPoller, client: Any | None = None) -> None:
        self.poller = poller
        api_key = os.environ.get("OPENAI_API_KEY")
        self.client: Any = client or OpenAI(api_key=api_key) if api_key else OpenAI()

    def _handle_gmail_poll(self, args: str) -> List[Email]:
        """Invoke :class:`GmailPoller` with the provided JSON arguments."""
        params = json.loads(args or "{}")
        return self.poller.poll(sender=params.get("sender"))

    def run(
        self,
        input_fn: Callable[[str], str] = input,
        print_fn: Callable[[str], None] = print,
    ) -> None:
        """Start the interactive chat loop."""

        logging.basicConfig(level=logging.INFO)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Use the gmail_poll tool to check for "
                    "unread emails when the user requests it."
                ),
            }
        ]

        print_fn("Type 'exit' to quit.")
        while True:
            user = input_fn("User > ")
            if user.strip().lower() in {"exit", "quit"}:
                break
            messages.append({"role": "user", "content": user})

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=GMAIL_POLL_TOOL,
                tool_choice="auto",
            )
            message = response.choices[0].message

            if getattr(message, "tool_calls", None):
                for call in message.tool_calls:
                    if call.function.name == "gmail_poll":
                        print_fn("Checking Gmail...")
                        emails = self._handle_gmail_poll(call.function.arguments)
                        count = len(emails)
                        print_fn(
                            f"Found {count} unread email{'s' if count != 1 else ''}."
                        )
                        content = json.dumps([asdict(email) for email in emails])
                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": call.id,
                                "content": content,
                            }
                        )

                followup = self.client.chat.completions.create(
                    model="gpt-4o-mini", messages=messages
                )
                reply = followup.choices[0].message.content or ""
                messages.append({"role": "assistant", "content": reply})
                print_fn(reply)
                continue

            reply = message.content or ""
            messages.append({"role": "assistant", "content": reply})
            print_fn(reply)


def main() -> None:
    poller = GmailPoller()
    ChatGmailAgent(poller).run()


if __name__ == "__main__":
    main()
