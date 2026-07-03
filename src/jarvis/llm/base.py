from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """Base interface for all LLM providers."""

    @abstractmethod
    def chat(self, messages: list[dict]) -> str:
        """Send messages to the language model."""
        pass