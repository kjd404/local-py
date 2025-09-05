import argparse
import asyncio
import logging
import os

from .gmail_poller import GmailPoller
from .gmail_polling_agent import GmailPollingAgent


async def main(interval: int) -> None:
    """Poll Gmail for new messages and log them."""
    logging.basicConfig(level=logging.INFO)

    poller = GmailPoller()
    agent = GmailPollingAgent(
        poller,
        sender=os.environ.get("GMAIL_SENDER"),
        interval=interval,
    )
    await agent.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Poll Gmail for new messages")
    parser.add_argument("--interval", type=int, default=60, help="Polling interval in seconds")
    args = parser.parse_args()
    asyncio.run(main(args.interval))
