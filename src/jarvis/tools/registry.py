from jarvis.tools.calculator_tool import CalculatorTool
from jarvis.tools.time_tool import TimeTool


class ToolRegistry:
    """Stores and executes built-in tools."""

    def __init__(self) -> None:
        self.tools = {
            "time": TimeTool(),
            "calc": CalculatorTool(),
        }

    def execute(self, command: str) -> str | None:
        parts = command.strip().split(maxsplit=1)

        tool_name = parts[0].lower()

        arguments = parts[1] if len(parts) > 1 else ""

        tool = self.tools.get(tool_name)

        if tool is None:
            return None

        return tool.execute(arguments)