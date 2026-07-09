from collections.abc import Generator

from groq import Groq

from jarvis.config.settings import settings
from jarvis.llm.base import BaseLLM


class GroqProvider(BaseLLM):
    """Handles communication with the Groq API."""

    def __init__(self) -> None:
        self.client = Groq(api_key=settings.groq_api_key)

    def _build_kwargs(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        stream: bool = False,
    ) -> dict:
        """Build the kwargs for the Groq API call."""

        kwargs = {
            "model": settings.default_model,
            "messages": messages,
        }

        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        if stream:
            kwargs["stream"] = True

        return kwargs

    def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ):
        kwargs = self._build_kwargs(messages, tools)
        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message

    def stream(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ):
        kwargs = self._build_kwargs(messages, tools, stream=True)
        response = self.client.chat.completions.create(**kwargs)

        for chunk in response:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta

            if delta.content:
                yield delta.content