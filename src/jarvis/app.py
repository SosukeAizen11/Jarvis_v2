import logging
from jarvis.config.settings import settings
from jarvis.llm.groq_provider import GroqProvider

logger = logging.getLogger(__name__)

class Application:
    """Coordinates the startup and lifecycle of the Jarvis application."""
    def __init__(self) -> None:
        self.llm = GroqProvider()
        
    def initialize(self) -> None:
        logger.info("Initializing application...")
        
    def run(self) -> None:
        logger.info(
            "Application started (version=%s, environment=%s)",
            settings.app_version,
            "development",
        )
        
        while True:
            prompt = input("\nYou:")
            
            if prompt.lower() in ["exit", "quit"]:
                break
            elif not prompt.strip():
                continue
            
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are Jarvis, a professional AI assistant. "
                        "Be helpful, concise and friendly."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
            
            try:
                response = self.llm.chat(messages)
                print(f"\nJarvis: {response}")

            except Exception:
                print("\nJarvis: Sorry, something went wrong.")
            
    def shutdown(self) -> None:
        logger.info("Shutting down application...")
