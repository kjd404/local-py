"""Tests for :mod:`chat_gmail_agent` using mocked services."""

import json
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import MagicMock

from chat_gmail_agent import ChatGmailAgent
from local_py.gmail_poller import Email


class ChatGmailAgentTest(TestCase):
    """Verify chat agent interactions with the Gmail poller."""

    def test_run_polls_and_prints_reply(self) -> None:
        """Poll Gmail and print the agent's reply using mocks."""
        poller = MagicMock()
        poller.poll.return_value = [Email(id="1", snippet="snippet 1")]

        first_message = SimpleNamespace(
            tool_calls=[
                SimpleNamespace(
                    id="1",
                    function=SimpleNamespace(name="gmail_poll", arguments="{}"),
                )
            ],
            content=None,
        )
        second_message = SimpleNamespace(tool_calls=None, content="All done")

        client = MagicMock()
        client.chat.completions.create.side_effect = [
            SimpleNamespace(choices=[SimpleNamespace(message=first_message)]),
            SimpleNamespace(choices=[SimpleNamespace(message=second_message)]),
        ]

        inputs = iter(["check", "exit"])
        outputs: list[str] = []

        def fake_input(prompt: str) -> str:
            return next(inputs)

        def fake_print(msg: str) -> None:
            outputs.append(msg)

        agent = ChatGmailAgent(poller, client=client)
        agent.run(input_fn=fake_input, print_fn=fake_print)

        poller.poll.assert_called_once_with(sender=None)
        self.assertEqual(
            [
                "Type 'exit' to quit.",
                "Checking Gmail...",
                "Found 1 unread email.",
                "All done",
            ],
            outputs,
        )

        tool_message = client.chat.completions.create.call_args_list[1].kwargs[
            "messages"
        ][-1]
        self.assertEqual(
            [{"id": "1", "snippet": "snippet 1"}],
            json.loads(tool_message["content"]),
        )
