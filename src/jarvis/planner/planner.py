from enum import Enum


class Plan(Enum):
    NONE = "none"
    CALCULATOR = "calculator"
    TIME = "time"
    WEB_SEARCH = "web_search"
    
class Planner:
    """Decides how Jarvis should answer a question."""

    def plan(
        self,
        prompt: str,
    ) -> Plan:

        prompt = prompt.lower()

        if any(
            operator in prompt
            for operator in [
                "+",
                "-",
                "*",
                "/",
                "%",
                "calculate",
            ]
        ):
            return Plan.CALCULATOR

        if "time" in prompt:
            return Plan.TIME

        if any(
            word in prompt
            for word in [
                "latest",
                "today",
                "news",
                "current",
                "recent",
                "yesterday",
            ]
        ):
            return Plan.WEB_SEARCH

        return Plan.NONE