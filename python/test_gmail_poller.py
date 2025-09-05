import asyncio
from unittest import TestCase
from unittest.mock import MagicMock, patch

import semantic_kernel as sk

from gmail_poller import Email, GmailPoller


class GmailPollerTest(TestCase):
    def setUp(self) -> None:
        self.service = MagicMock()
        users = self.service.users.return_value
        self.messages = users.messages.return_value

        # Simulate two unread messages
        self.messages.list.return_value.execute.return_value = {
            "messages": [{"id": "1"}, {"id": "2"}]
        }

        def get_call(userId: str, id: str):  # noqa: D401 - short mock function
            msg = MagicMock()
            msg.execute.return_value = {
                "id": id,
                "snippet": f"snippet {id}",
            }
            return msg

        self.messages.get.side_effect = get_call

        def modify_call(userId: str, id: str, body: dict):
            mod = MagicMock()
            mod.execute.return_value = None
            return mod

        self.messages.modify.side_effect = modify_call

    def test_poll_returns_emails(self) -> None:
        with patch.object(GmailPoller, "_authorize", return_value=self.service):
            poller = GmailPoller()
            emails = poller.poll("sender@example.com")

        self.assertEqual(
            [
                Email(id="1", snippet="snippet 1"),
                Email(id="2", snippet="snippet 2"),
            ],
            emails,
        )
        self.assertEqual(2, self.messages.modify.call_count)
        self.messages.modify.assert_any_call(
            userId="me", id="1", body={"removeLabelIds": ["UNREAD"]}
        )
        self.messages.modify.assert_any_call(
            userId="me", id="2", body={"removeLabelIds": ["UNREAD"]}
        )

    def test_poll_kernel_function(self) -> None:
        with patch.object(GmailPoller, "_authorize", return_value=self.service):
            poller = GmailPoller()
            kernel = sk.Kernel()
            kernel.add_function("gmail", poller.poll, function_name="poll")
            emails = asyncio.run(
                kernel.invoke("gmail", "poll", sender="sender@example.com")
            )

        self.assertEqual(
            [
                Email(id="1", snippet="snippet 1"),
                Email(id="2", snippet="snippet 2"),
            ],
            emails,
        )
