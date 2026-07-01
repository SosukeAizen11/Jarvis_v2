from datetime import datetime

from jarvis.tools.base import BaseTool


class TimeTool(BaseTool):

    @property
    def name(self) -> str:
        return "time"

    @property
    def description(self) -> str:
        return "Returns the current system time."

    def execute(self, arguments: str = "") -> str:
        return datetime.now().strftime("%I:%M:%S %p")