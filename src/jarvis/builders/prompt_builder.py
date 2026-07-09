from datetime import datetime

from jarvis.memory.conversation import Conversation
from jarvis.memory.semantic_memory import SemanticMemory


class PromptBuilder:
    """Builds the final prompt sent to the LLM."""

    def __init__(
        self,
        conversation: Conversation,
        semantic_memory: SemanticMemory,
    ) -> None:
        self.conversation = conversation
        self.semantic_memory = semantic_memory

    def build(
        self,
        prompt: str,
        tool_context: str | None = None,
    ) -> list[dict]:
        """Build the final prompt."""

        messages = (
            self.conversation
            .get_recent_messages(limit=10)
            .copy()
        )

        insert_index = 1

        # -------------------------------------------------
        # Current Date
        # -------------------------------------------------

        today = datetime.now().strftime("%B %d, %Y")

        messages.insert(
            insert_index,
            {
                "role": "system",
                "content": (
                    f"Today's date is {today}.\n\n"
                    "If external search results are provided:\n"
                    "- Prefer the newest information.\n"
                    "- Ignore outdated information unless the user "
                    "explicitly asks for historical facts.\n"
                    "- If multiple sources conflict, prioritize the "
                    "most recent and reliable sources."
                ),
            },
        )

        insert_index += 1

        # -------------------------------------------------
        # Semantic Memory
        # -------------------------------------------------

        relevant_memories = self.semantic_memory.search(
            prompt
        )

        if relevant_memories:

            memory_text = (
                "You have access to the following "
                "long-term memories about the user.\n\n"
                "Use these memories only if they are "
                "relevant to answering the user's "
                "current question.\n\n"
                "Long-Term Memories:\n"
            )

            memory_text += "\n".join(
                f"- {memory.text}"
                for memory in relevant_memories
            )

            messages.insert(
                insert_index,
                {
                    "role": "system",
                    "content": memory_text,
                },
            )

            insert_index += 1

        # -------------------------------------------------
        # Tool Context
        # -------------------------------------------------

        if tool_context:

            messages.insert(
                insert_index,
                {
                    "role": "system",
                    "content": (
                        "External information retrieved "
                        "for this request:\n\n"
                        f"{tool_context}"
                    ),
                },
            )

            insert_index += 1

        # -------------------------------------------------
        # Conversation Marker
        # -------------------------------------------------

        messages.insert(
            insert_index,
            {
                "role": "system",
                "content": (
                    "The following messages are the "
                    "recent conversation with the user."
                ),
            },
        )

        return messages