from datetime import datetime


class TimeTool:
    """Returns the current system time."""

    def execute(self) -> str:
        return datetime.now().strftime("%I:%M:%S %p")