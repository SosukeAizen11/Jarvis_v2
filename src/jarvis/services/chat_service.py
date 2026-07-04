import json
from collections.abc import Generator

from jarvis.llm.base import BaseLLM
from jarvis.memory.conversation import Conversation
from jarvis.tools.registry import ToolRegistry


class ChatService:
    """Handles AI conversations."""

    def __init__(
        self,
        llm: BaseLLM,
        conversation: Conversation,
        tools: ToolRegistry,
    ) -> None:
        self.llm = llm
        self.conversation = conversation
        self.tools = tools

    def chat(self, prompt: str) -> str:

        self.conversation.add_user_message(prompt)

        tool_definitions = [
            tool.to_groq_tool()
            for tool in self.tools.get_tools()
        ]

        response = self.llm.chat(
            self.conversation.get_messages(),
            tools=tool_definitions,
        )

        if response.tool_calls:

            tool_call = response.tool_calls[0]

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            if tool_name == "calculator":

                expression = arguments["expression"]

                result = self.tools.tools[
                    tool_name
                ].execute(expression)

                print(result)

                return result

        self.conversation.add_assistant_message(response.content)

        return response.content

    def stream_chat(self, prompt: str) -> Generator[str, None, None]:
        """Stream a normal AI response."""

        self.conversation.add_user_message(prompt)

        full_response = ""

        for chunk in self.llm.stream(
            self.conversation.get_messages()
        ):
            full_response += chunk
            yield chunk

        self.conversation.add_assistant_message(full_response)