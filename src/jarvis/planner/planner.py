from enum import Enum


class Plan(Enum):
    NONE = "none"
    CALCULATOR = "calculator"
    TIME = "time"
    WEB_SEARCH = "web_search"


class Planner:
    """Decides which tools Jarvis should use."""

    def plan(
        self,
        prompt: str,
    ) -> list[Plan]:

        prompt = prompt.lower()

        plans: list[Plan] = []

        # -----------------------------
        # Calculator
        # -----------------------------

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
            plans.append(Plan.CALCULATOR)

        # -----------------------------
        # Time
        # -----------------------------

        if any(
            word in prompt
            for word in [
                "time",
                "clock",
            ]
        ):
            plans.append(Plan.TIME)

        # -----------------------------
        # Web Search
        # -----------------------------

        if any(
            word in prompt
            for word in [
                "latest",
                "today",
                "recent",
                "current",
                "news",
                "who",
                "when",
                "where",
            ]
        ):
            plans.append(Plan.WEB_SEARCH)

        if not plans:
            plans.append(Plan.NONE)

        return plans