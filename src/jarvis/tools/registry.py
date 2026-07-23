from jarvis.tools.calculator_tool import CalculatorTool
from jarvis.tools.time_tool import TimeTool
from jarvis.tools.web_search_tool import WebSearchTool
from jarvis.tools.youtube_index_tool import YouTubeIndexTool


class ToolRegistry:
    """Stores and executes built-in tools."""

    def __init__(self) -> None:
        self.tools = {
            "time": TimeTool(),
            "calculator": CalculatorTool(),
            "web_search": WebSearchTool(),
            "youtube_index": YouTubeIndexTool(),
        }
        
    def get_tools(self) -> list:
        return list(self.tools.values())

    def execute(self, command: str) -> str | None:
        parts = command.strip().split(maxsplit=1)

        tool_name = parts[0].lower()

        arguments = parts[1] if len(parts) > 1 else ""

        tool = self.tools.get(tool_name)

        if tool is None:
            return None

        return tool.execute(arguments)

    def execute_tool_call(
        self,
        tool_name: str,
        arguments: dict,
    ):
        """Execute a tool requested by the LLM."""

        tool = self.tools.get(tool_name)

        if tool is None:
            raise ValueError(
                f"Unknown tool: {tool_name}"
            )

        return tool.execute_from_arguments(arguments)