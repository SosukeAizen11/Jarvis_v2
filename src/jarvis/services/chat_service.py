from jarvis.llm.base import BaseLLM
from jarvis.memory.conversation import Conversation


class ChatService:
    """Handles AI conversations."""

    def __init__(
        self,
        llm: BaseLLM,
        conversation: Conversation,
    ) -> None:
        self.llm = llm
        self.conversation = conversation

    def chat(self, prompt: str) -> str:
        self.conversation.add_user_message(prompt)

        response = self.llm.chat(
            self.conversation.get_messages()
        )

        self.conversation.add_assistant_message(response)

        return response