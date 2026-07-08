import json
from collections.abc import Generator

from jarvis.llm.base import BaseLLM
from jarvis.memory.conversation import Conversation
from jarvis.memory.semantic_memory import SemanticMemory
from jarvis.tools.registry import ToolRegistry


class ChatService:
    """Handles AI conversations."""

    def __init__(
        self,
        llm: BaseLLM,
        conversation: Conversation,
        tools: ToolRegistry,
        semantic_memory: SemanticMemory,
    ) -> None:
        self.llm = llm
        self.conversation = conversation
        self.tools = tools
        self.semantic_memory = semantic_memory
        
    def _should_enable_tools(self, prompt: str) -> bool:
        prompt = prompt.lower()

        tool_keywords = [
            "calculate",
            "what is",
            "+",
            "-",
            "*",
            "/",
            "%",
            "time",
        ]

        return any(keyword in prompt for keyword in tool_keywords)

    def chat(self, prompt: str) -> Generator[str, None, None]:
        """Handle a user prompt and yield the response."""

        # Store conversation history
        self.conversation.add_user_message(prompt)
        # Search for relevant memories
        relevant_memories = self.semantic_memory.search(prompt)
        # Store semantic memory
        self.semantic_memory.add(prompt)
        

        messages = self.conversation.get_messages().copy()

        if relevant_memories:

            memory_context = "\n".join(
                f"- {memory.text}"
                for memory in relevant_memories
            )

            messages.insert(
                1,
                {
                    "role": "system",
                    "content": (
                        "Relevant memories:\n"
                        f"{memory_context}"
                    ),
                },
            )

        tool_definitions = None
        
        if self._should_enable_tools(prompt):
            tool_definitions = [
                tool.to_groq_tool()
                for tool in self.tools.get_tools()
            ]

        response = self.llm.chat(
            messages,
            tools=tool_definitions,
        )

        # Tool Calling
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

                self.conversation.add_assistant_message(result)

                yield result
                return

        # Stream normal response
        full_response = ""

        for chunk in self.llm.stream(messages):
            full_response += chunk
            yield chunk

        self.conversation.add_assistant_message(full_response)