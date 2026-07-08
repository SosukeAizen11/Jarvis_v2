from jarvis.memory.repository import ConversationRepository


class Conversation:
    """Stores and manages the conversation history."""

    def __init__(self, system_prompt: str):
        self.repository = ConversationRepository()

        stored_messages = self.repository.load_messages()

        self.messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        self.messages.extend(stored_messages)

    def add_user_message(self, message: str) -> None:
        self.messages.append(
            {
                "role": "user",
                "content": message,
            }
        )

        self.repository.save_message(
            role="user",
            content=message,
        )

    def add_assistant_message(self, message: str) -> None:
        self.messages.append(
            {
                "role": "assistant",
                "content": message,
            }
        )

        self.repository.save_message(
            role="assistant",
            content=message,
        )

    def get_messages(self) -> list[dict]:
        return self.messages

    def get_recent_messages(
        self,
        limit: int = 10,
    ) -> list[dict]:
        """
        Return the system prompt and the most recent messages.
        """
        system_prompt = self.messages[0]
        recent_messages = self.messages[-limit:]
        return [
            system_prompt,
            *recent_messages,
        ]

    def clear(self) -> None:
        """Clear the current conversation."""

        self.messages = [self.messages[0]]
        self.repository.clear()

    def close(self) -> None:
        """Close any resources owned by the conversation."""

        self.repository.close()