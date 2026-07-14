from datetime import datetime

from jarvis.documents.retriever import PDFRetriever
from jarvis.memory.conversation import Conversation
from jarvis.memory.semantic_memory import SemanticMemory


class PromptBuilder:
    """Builds the final prompt sent to the LLM."""

    def __init__(
        self,
        conversation: Conversation,
        semantic_memory: SemanticMemory,
        pdf_retriever: PDFRetriever,
    ) -> None:
        self.conversation = conversation
        self.semantic_memory = semantic_memory
        self.pdf_retriever = pdf_retriever

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
                    "- Ignore outdated information unless explicitly requested.\n"
                    "- If sources conflict, prefer the newest reliable source."
                ),
            },
        )

        insert_index += 1

        # -------------------------------------------------
        # Semantic Memory
        # -------------------------------------------------

        relevant_memories = self.semantic_memory.search(prompt)

        if relevant_memories:

            memory_text = (
                "Relevant Long-Term User Memories\n"
                "--------------------------------\n"
                "Use these memories ONLY if they are relevant to the current request.\n\n"
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
        # PDF Knowledge
        # -------------------------------------------------

        pdf_chunks = self.pdf_retriever.search(prompt)

        if pdf_chunks:

            pdf_text = (
                "Retrieved Knowledge Base\n"
                "------------------------\n"
                "The following information was retrieved from indexed PDF documents.\n"
                "When it is relevant to the user's question:\n"
                "- Treat this as the primary knowledge source.\n"
                "- Base your answer on this information.\n"
                "- Do NOT invent facts that are not supported by the retrieved text.\n"
                "- If the retrieved text is incomplete, say so instead of guessing.\n\n"
                "Retrieved Content:\n\n"
            )

            pdf_text += "\n\n".join(pdf_chunks)

            messages.insert(
                insert_index,
                {
                    "role": "system",
                    "content": pdf_text,
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
                        "External Tool Results\n"
                        "---------------------\n"
                        "The following information was retrieved from external tools.\n"
                        "Use it only if it is relevant to the user's request.\n\n"
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
                    "The following messages contain the recent conversation with the user."
                ),
            },
        )

        return messages