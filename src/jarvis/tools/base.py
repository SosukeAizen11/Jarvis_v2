from abc import ABC, abstractmethod


class BaseTool(ABC):
    """Base class for all Jarvis tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique tool name."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Describe what the tool does."""
        pass

    @abstractmethod
    def execute(self, arguments: str = "") -> str:
        """Execute the tool."""
        pass