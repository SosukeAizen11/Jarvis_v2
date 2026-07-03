from jarvis.config.settings import settings
from jarvis.llm.base import BaseLLM
from jarvis.llm.groq_provider import GroqProvider


class LLMFactory:
    """Creates LLM provider instances."""

    @staticmethod
    def create() -> BaseLLM:
        provider = settings.llm_provider.lower()

        if provider == "groq":
            return GroqProvider()

        raise ValueError(
            f"Unsupported LLM provider: {provider}"
        )