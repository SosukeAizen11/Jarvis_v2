import logging
import os

from jarvis.commands.router import CommandRouter, CommandType
from jarvis.config.settings import settings
from jarvis.llm.factory import LLMFactory
from jarvis.memory.conversation import Conversation
from jarvis.services.chat_service import ChatService
from jarvis.tools.registry import ToolRegistry

logger = logging.getLogger(__name__)


class Application:
    """Coordinates the startup and lifecycle of the Jarvis application."""

    def __init__(self) -> None:
        self.router = CommandRouter()
        self.llm = LLMFactory.create()
        self.tool_registry = ToolRegistry()
        self.conversation = Conversation(
            system_prompt=(
                "You are Jarvis, a professional AI assistant. "
                "Be helpful, concise, and friendly."
            )
        )
        self.chat_service = ChatService(
            llm=self.llm,
            conversation=self.conversation,
            tools=self.tool_registry,
        )

    def initialize(self) -> None:
        logger.info("Initializing application...")

    def run(self) -> None:
        logger.info(
            "Application started (version=%s, environment=%s)",
            settings.app_version,
            "development",
        )

        print("=" * 50)
        print("🤖 Jarvis v2")
        print("Type 'help' to see available commands.")
        print("Type 'exit' to quit.")
        print("=" * 50)

        while True:
            prompt = input("\nYou: ")

            if not prompt.strip():
                continue

            command = self.router.route(prompt)

            if command == CommandType.EXIT:
                break

            if command == CommandType.HELP:
                print(
                    """
Available Commands
------------------
help    - Show available commands
clear   - Clear the terminal
exit    - Exit Jarvis

Anything else will be sent to the AI.
"""
                )
                continue

            if command == CommandType.CLEAR:
                os.system("cls" if os.name == "nt" else "clear")
                continue

            tool_result = self.tool_registry.execute(prompt)
            if tool_result is not None:
                print(f"\nJarvis: {tool_result}")
                continue

            try:
                print("\nJarvis: ", end="", flush=True)

                for chunk in self.chat_service.stream_chat(prompt):
                    print(chunk, end="", flush=True)

                print()

            except Exception:
                logger.exception("Failed to generate response")
                print("\nJarvis: Sorry, something went wrong.")

    def shutdown(self) -> None:
        logger.info("Shutting down application...")