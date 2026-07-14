import json
from collections.abc import Generator

from jarvis.builders.prompt_builder import PromptBuilder
from jarvis.llm.base import BaseLLM
from jarvis.memory.conversation import Conversation
from jarvis.memory.semantic_memory import SemanticMemory
from jarvis.tools.registry import ToolRegistry
from jarvis.planner.planner import Planner, Plan
from jarvis.services.search_result_formatter import SearchResultFormatter
from jarvis.documents.retriever import PDFRetriever


class ChatService:
    """Handles AI conversations."""

    MAX_TOOL_RESULT_CHARS = 3000

    def __init__(
        self,
        llm: BaseLLM,
        conversation: Conversation,
        tools: ToolRegistry,
        semantic_memory: SemanticMemory,
        pdf_retriever: PDFRetriever,
    ) -> None:
        self.llm = llm
        self.conversation = conversation
        self.tools = tools
        self.semantic_memory = semantic_memory
        self.planner = Planner()
        self.search_formatter = SearchResultFormatter()
        self.prompt_builder = PromptBuilder(
            conversation=conversation,
            semantic_memory=semantic_memory,
            pdf_retriever=pdf_retriever,
        )

    def _truncate_tool_result(self, result) -> str:
        """Extract key info from tool results and cap the size."""
        if isinstance(result, list):
            # Web search results: extract only title + content
            condensed = []
            for item in result:
                if isinstance(item, dict):
                    parts = []
                    if item.get("title"):
                        parts.append(item["title"])
                    if item.get("content"):
                        parts.append(item["content"])
                    condensed.append(" — ".join(parts))
                else:
                    condensed.append(str(item))
            text = "\n\n".join(condensed)
        else:
            text = json.dumps(result, default=str)

        if len(text) > self.MAX_TOOL_RESULT_CHARS:
            text = text[: self.MAX_TOOL_RESULT_CHARS] + "..."

        return text

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

        plans = self.planner.plan(prompt)
        print(plans)

        tool_definitions = []
        
        for plan in plans:
            if plan == Plan.CALCULATOR:
                tool_definitions.append(
                    self.tools.tools["calculator"].to_groq_tool()
                )

            elif plan == Plan.TIME:
                tool_definitions.append(
                    self.tools.tools["time"].to_groq_tool()
                )

            elif plan == Plan.WEB_SEARCH:
                tool_definitions.append(
                    self.tools.tools["web_search"].to_groq_tool()
                )
                
        if not tool_definitions:
            tool_definitions = None
            
        # print(f"Planner selected: {plan}")
        # print(f"Tool definitions: {tool_definitions}")

        response = self.llm.chat(
            messages,
            tools=tool_definitions,
        )
        
        print(response.tool_calls)

        
        # Tool Calling
        if response.tool_calls:

            followup_messages = messages.copy()

            # Add the assistant message containing ALL tool calls.
            followup_messages.append(
                {
                    "role": "assistant",
                    "content": response.content,
                    "tool_calls": [
                        {
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments,
                            },
                        }
                        for tool_call in response.tool_calls
                    ],
                }
            )

            # Execute every tool requested by the model.
            for tool_call in response.tool_calls:

                tool_name = tool_call.function.name

                arguments = json.loads(
                    tool_call.function.arguments
                )

                result = self.tools.execute_tool_call(
                    tool_name,
                    arguments,
                )
                print(f"Tool executed {tool_name}")

                if tool_name == "web_search":
                    tool_content = self.search_formatter.format(
                        result
                    )
                else:
                    tool_content = self._truncate_tool_result(
                        result
                    )

                followup_messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_content,
                    }
                )
            
            # FOLLOW UP MESSAGE BEFORE SENDING TO THE 2ND LLM CALL. 
            # print("\n===== FOLLOWUP MESSAGES =====")
            # for i, message in enumerate(followup_messages, start=1):
            #     print(f"\n[{i}] {message['role'].upper()}")
            #     print(message)
            # print("=============================\n")


            # Final LLM call with all tool results.
            full_response = ""

            for chunk in self.llm.stream(
                followup_messages
            ):
                full_response += chunk
                yield chunk

            self.conversation.add_assistant_message(
                full_response
            )

            return

        # Stream normal response (no tool was called)
        full_response = ""

        for chunk in self.llm.stream(messages):
            full_response += chunk
            yield chunk

        self.conversation.add_assistant_message(
            full_response
        )