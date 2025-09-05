"""Interactive chat agent that can poll Gmail using OpenAI tool calls."""

from __future__ import annotations

import json
import logging
import os
from typing import List

from openai import OpenAI

from .gmail_poller import Email, GmailPoller


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


def handle_gmail_poll(args: str) -> List[Email]:
    """Invoke :class:`GmailPoller` with the provided JSON arguments."""
    params = json.loads(args or "{}")
    poller = GmailPoller()
    return poller.poll(sender=params.get("sender"))


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logging.error("OPENAI_API_KEY is not set; chat will fail")
        return

    client = OpenAI(api_key=api_key)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. Use the gmail_poll tool to check for "
                "unread emails when the user requests it."
            ),
        }
    ]

    print("Type 'exit' to quit.")
    while True:
        user = input("User > ")
        if user.strip().lower() in {"exit", "quit"}:
            break
        messages.append({"role": "user", "content": user})

        # Ask the model for the next action, providing the Gmail tool definition.
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=GMAIL_POLL_TOOL,
            tool_choice="auto",
        )
        message = response.choices[0].message

        if message.tool_calls:
            # Execute each requested tool and append results for a final response.
            for call in message.tool_calls:
                if call.function.name == "gmail_poll":
                    emails = handle_gmail_poll(call.function.arguments)
                    content = json.dumps([email.__dict__ for email in emails])
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": call.id,
                            "content": content,
                        }
                    )

            followup = client.chat.completions.create(
                model="gpt-4o-mini", messages=messages
            )
            reply = followup.choices[0].message.content or ""
            messages.append({"role": "assistant", "content": reply})
            print(reply)
            continue

        # No tool calls; just print the assistant's message.
        reply = message.content or ""
        messages.append({"role": "assistant", "content": reply})
        print(reply)


if __name__ == "__main__":
    main()

