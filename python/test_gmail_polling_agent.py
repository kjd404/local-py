import asyncio
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

from local_py.gmail_polling_agent import GmailPollingAgent


class GmailPollingAgentTest(IsolatedAsyncioTestCase):
    async def test_run_polls_until_cancelled(self) -> None:
        poller = MagicMock()
        poller.poll.return_value = []

        agent = GmailPollingAgent(poller)
        task = asyncio.create_task(agent.run(interval=0))
        await asyncio.sleep(0.05)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertGreaterEqual(poller.poll.call_count, 1)

    async def test_run_uses_provided_interval(self) -> None:
        poller = MagicMock()
        poller.poll.return_value = []

        agent = GmailPollingAgent(poller, interval=10)
        sleep_mock = AsyncMock(side_effect=asyncio.CancelledError())
        with patch("local_py.gmail_polling_agent.asyncio.sleep", sleep_mock):
            with self.assertRaises(asyncio.CancelledError):
                await agent.run(interval=2)
        sleep_mock.assert_awaited_with(2)
