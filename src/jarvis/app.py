import logging

from jarvis.config.settings import settings
from jarvis.llm.groq_provider import GroqProvider
from jarvis.memory.conversation import Conversation

logger = logging.getLogger(__name__)


class Application:
    """Coordinates the startup and lifecycle of the Jarvis application."""

    def __init__(self) -> None:
        self.llm = GroqProvider()

        self.conversation = Conversation(
            system_prompt=(
                "You are Jarvis, a professional AI assistant. "
                "Be helpful, concise, and friendly."
            )
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
        print("Type 'exit' to quit.")
        print("=" * 50)

        while True:
            prompt = input("\nYou: ")

            if not prompt.strip():
                continue

            if prompt.lower() in ("exit", "quit"):
                break

            self.conversation.add_user_message(prompt)

            try:
                response = self.llm.chat(
                    self.conversation.get_messages()
                )

                self.conversation.add_assistant_message(response)

                print(f"\nJarvis: {response}")

            except Exception as e:
                logger.exception("Failed to generate response")
                print("\nJarvis: Sorry, something went wrong.")

    def shutdown(self) -> None:
        logger.info("Shutting down application...")