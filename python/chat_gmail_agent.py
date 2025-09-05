"""Interactive chat agent that can poll Gmail using Semantic Kernel."""
import asyncio
import logging
import os
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from gmail_poller import GmailPoller


def create_kernel() -> sk.Kernel:
    """Create and configure the Semantic Kernel."""
    kernel = sk.Kernel()

    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        service = OpenAIChatCompletion(ai_model_id="gpt-4o-mini", api_key=api_key)
        kernel.add_service(service)
    else:
        logging.warning("OPENAI_API_KEY is not set; chat will fail")

    poller = GmailPoller()
    kernel.add_function(
        plugin_name="gmail",
        function=poller.poll,
        function_name="poll",
        description="Poll Gmail for unread messages from a sender.",
    )
    return kernel


async def chat_loop(kernel: sk.Kernel) -> None:
    """Simple interactive chat loop."""
    print("Type 'exit' to quit.")
    while True:
        user = input("User > ")
        if user.strip().lower() in {"exit", "quit"}:
            break
        # Forward user message through the kernel so the model can decide to call functions.
        result = await kernel.invoke(
            plugin_name="chat",
            function_name="chat",
            input=user,
        )
        if result:
            print(result)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    kernel = create_kernel()
    # Register a basic chat function that relays messages to the model.
    kernel.add_function(
        plugin_name="chat",
        function_name="chat",
        description="General chat interface",
        prompt="""{{$input}}""",
    )
    asyncio.run(chat_loop(kernel))


if __name__ == "__main__":
    main()
