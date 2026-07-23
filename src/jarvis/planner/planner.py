from enum import Enum


class Plan(Enum):
    NONE = "none"
    CALCULATOR = "calculator"
    TIME = "time"
    WEB_SEARCH = "web_search"
    YOUTUBE_INDEX = "youtube_index"


class Planner:
    """Decides which tools Jarvis should use."""

    def plan(
        self,
        prompt: str,
    ) -> list[Plan]:

        prompt = prompt.lower()

        plans: list[Plan] = []

        has_url = "http://" in prompt or "https://" in prompt

        # -----------------------------
        # Calculator
        # -----------------------------

        if not has_url and any(
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

        references_indexed_content = any(
            phrase in prompt
            for phrase in [
                "this video",
                "the video",
                "the transcript",
                "the speaker",
                "this transcript",
            ]
        )

        if not references_indexed_content and any(
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
            
        # -----------------------------
        # YouTube Index
        # -----------------------------

        if (
            ("youtube.com" in prompt or "youtu.be" in prompt)
            and any(
                word in prompt
                for word in [
                    "index",
                    "learn",
                    "remember",
                    "save",
                ]
            )
        ):
            plans.append(Plan.YOUTUBE_INDEX)

        if not plans:
            plans.append(Plan.NONE)

        return plans