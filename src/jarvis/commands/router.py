from enum import Enum


class CommandType(Enum):
    EXIT = "exit"
    HELP = "help"
    CLEAR = "clear"
    CHAT = "chat"


class CommandRouter:
    """Routes user input to the correct handler."""

    def route(self, prompt: str) -> CommandType:
        command = prompt.strip().lower()

        if command in ("exit", "quit"):
            return CommandType.EXIT

        if command == "help":
            return CommandType.HELP

        if command == "clear":
            return CommandType.CLEAR

        return CommandType.CHAT