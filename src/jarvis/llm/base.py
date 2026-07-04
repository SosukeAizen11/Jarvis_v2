from abc import ABC, abstractmethod
from collections.abc import Generator
from typing import Any


class BaseLLM(ABC):
    """Base interface for all LLM providers."""

    @abstractmethod
    def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> Any:
        """Return a complete response from the language model."""
        pass

    @abstractmethod
    
    def stream(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> Generator[str, None, None]:
        """Stream the response from the language model."""
        pass