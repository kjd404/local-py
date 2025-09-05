import asyncio
import logging
from typing import Optional

from .gmail_poller import GmailPoller


class GmailPollingAgent:
    """Continuously poll Gmail for new messages."""

    def __init__(
        self,
        poller: GmailPoller,
        *,
        sender: Optional[str] = None,
        interval: int = 60,
    ) -> None:
        self.poller = poller
        self.sender = sender
        self.interval = interval

    async def run(self, interval: Optional[int] = None) -> None:
        """Start polling until cancelled.

        Args:
            interval: Polling interval in seconds. Defaults to the value
                provided at construction.
        """
        delay = interval if interval is not None else self.interval
        try:
            while True:
                for email in self.poller.poll(sender=self.sender):
                    logging.info("New email %s: %s", email.id, email.snippet)
                await asyncio.sleep(delay)
        except asyncio.CancelledError:
            logging.info("Polling cancelled")
            raise
