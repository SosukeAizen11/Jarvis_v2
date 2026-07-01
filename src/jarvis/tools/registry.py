from jarvis.tools.calculator_tool import CalculatorTool
from jarvis.tools.time_tool import TimeTool


class ToolRegistry:
    """Stores and executes built-in tools."""

    def __init__(self) -> None:
        self.time_tool = TimeTool()
        self.calculator_tool = CalculatorTool()

    def execute(self, command: str) -> str | None:
        command = command.strip()

        if command.lower() == "time":
            return self.time_tool.execute()

        if command.lower().startswith("calc "):
            expression = command[5:]
            return self.calculator_tool.execute(expression)

        return None