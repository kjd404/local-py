import logging
import os
import time

import semantic_kernel as sk

from gmail_poller import GmailPoller


def main() -> None:
    """Poll Gmail for new messages and log them."""
    logging.basicConfig(level=logging.INFO)

    kernel = sk.Kernel()
    poller = GmailPoller()

    # Register a skill/function that calls `GmailPoller.poll`.
    kernel.add_native_function("gmail", "poll", poller.poll)

    sender = os.environ.get("GMAIL_SENDER", "")
    while True:
        emails = kernel.invoke("gmail", "poll", sender)
        for email in emails:
            logging.info("New email %s: %s", email.id, email.snippet)
        time.sleep(60)


if __name__ == "__main__":
    main()
