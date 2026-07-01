from jarvis.tools.time_tool import TimeTool


class ToolRegistry:
    """Stores and executes built-in tools."""

    def __init__(self) -> None:
        self.time_tool = TimeTool()

    def execute(self, command: str) -> str | None:
        command = command.lower().strip()

        if command == "time":
            return self.time_tool.execute()

        return None