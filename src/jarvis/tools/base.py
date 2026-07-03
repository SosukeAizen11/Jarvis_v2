from abc import ABC, abstractmethod


class BaseTool(ABC):
    """Base class for all Jarvis tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def parameters(self) -> dict:
        """JSON Schema describing this tool."""
        pass

    @abstractmethod
    def execute(self, arguments: str = "") -> str:
        pass

    def to_groq_tool(self) -> dict:
        """Convert this tool into Groq's function definition format."""

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }