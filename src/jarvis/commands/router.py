from enum import Enum


class CommandType(Enum):
    EXIT = "exit"
    HELP = "help"
    CLEAR = "clear"
    CHAT = "chat"
    INDEX_PDF = "index"
    CLEAR_DOCUMENTS = "clear_documents"
    CLEAR_MEMORY = "clear_memory"
    CLEAR_ALL = "clear_all"
    DOCUMENTS = "documents"
    DELETE_DOCUMENT = "delete_document"

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
        
        if command.startswith("index "):
            return CommandType.INDEX_PDF
        
        if command == "clear documents":
            return CommandType.CLEAR_DOCUMENTS

        if command == "clear memory":
            return CommandType.CLEAR_MEMORY

        if command == "clear all":
            return CommandType.CLEAR_ALL
        
        if command == "documents":
            return CommandType.DOCUMENTS

        if command.startswith("delete document "):
            return CommandType.DELETE_DOCUMENT
        
        return CommandType.CHAT