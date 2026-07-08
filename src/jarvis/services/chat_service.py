import json
from collections.abc import Generator

from jarvis.builders.prompt_builder import PromptBuilder
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

        self.prompt_builder = PromptBuilder(
            conversation=conversation,
            semantic_memory=semantic_memory,
        )

    def _should_enable_tools(
        self,
        prompt: str,
    ) -> bool:
        """Return True if the prompt is likely requesting a tool."""

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

        return any(
            keyword in prompt
            for keyword in tool_keywords
        )

    def chat(
        self,
        prompt: str,
    ) -> Generator[str, None, None]:
        """Handle a user prompt and yield the response."""

        # Store conversation history
        self.conversation.add_user_message(prompt)

        # Build the final prompt
        messages = self.prompt_builder.build(prompt)
        
        # TO SEE THE PROMPT SEND TO THE LLM
        # print("\n" + "=" * 60)
        # print("PROMPT SENT TO THE LLM")
        # print("=" * 60)

        # for i, message in enumerate(messages, start=1):
        #     print(f"\n[{i}] ROLE: {message['role'].upper()}")
        #     print(message["content"])

        # print("=" * 60 + "\n")
        
        # Store semantic memory
        self.semantic_memory.add(prompt)

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

                self.conversation.add_assistant_message(
                    result
                )

                yield result
                return

        # Stream normal response
        full_response = ""

        for chunk in self.llm.stream(messages):
            full_response += chunk
            yield chunk

        self.conversation.add_assistant_message(
            full_response
        )