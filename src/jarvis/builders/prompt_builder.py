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
    ) -> list[dict]:
        """Build the final prompt."""

        messages = self.conversation.get_recent_messages(limit=10).copy()

        relevant_memories = self.semantic_memory.search(prompt)

        if relevant_memories:

            memory_text = """
                You have access to the following long-term memories about the user.

                Use these memories only if they are relevant to answering the user's current question.

                Long-Term Memories:
                """

            memory_text += "\n".join(
                f"- {memory.text}"
                for memory in relevant_memories
            )

            messages.insert(
                1,
                {
                    "role": "system",
                    "content": memory_text,
                },
            )
            
            messages.insert(
                2,
                {
                    "role": "system",
                    "content": (
                        "The following messages are the recent "
                        "conversation with the user."
                    ),
                },
            )

        return messages