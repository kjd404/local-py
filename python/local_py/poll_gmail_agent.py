import asyncio
import logging
import os

import semantic_kernel as sk

from .gmail_poller import GmailPoller


async def main() -> None:
    """Poll Gmail for new messages and log them."""
    logging.basicConfig(level=logging.INFO)

    kernel = sk.Kernel()
    poller = GmailPoller()

    # Register a skill/function that calls `GmailPoller.poll`.
    kernel.add_function(
        plugin_name="gmail", function=poller.poll, function_name="poll"
    )

    sender = os.environ.get("GMAIL_SENDER", "")
    while True:
        result = await kernel.invoke(
            function_name="poll", plugin_name="gmail", sender=sender
        )
        for email in result.value if result else []:
            logging.info("New email %s: %s", email.id, email.snippet)
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
