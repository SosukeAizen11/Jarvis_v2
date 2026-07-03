from groq import Groq

from jarvis.config.settings import settings
from jarvis.llm.base import BaseLLM

class GroqProvider(BaseLLM):
    """Handles communication with the Groq API."""

    def __init__(self) -> None:
        self.client = Groq(api_key=settings.groq_api_key)

    def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ):
        try:
            response = self.client.chat.completions.create(
                model=settings.default_model,
                messages=messages,
                tools=tools,
            )

            return response.choices[0].message

        except Exception as e:
            return f"Error: {e}"