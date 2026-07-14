import logging
import os
from pathlib import Path

from jarvis.commands.router import CommandRouter, CommandType
from jarvis.config.settings import settings
from jarvis.llm.factory import LLMFactory
from jarvis.memory.conversation import Conversation
from jarvis.services.chat_service import ChatService
from jarvis.tools.registry import ToolRegistry
from jarvis.services.embedding_service import EmbeddingService
from jarvis.documents.chunker import TextChunker
from jarvis.documents.indexer import DocumentIndexer
from jarvis.documents.parser import PDFParser
from jarvis.documents.service import DocumentService
from jarvis.memory.semantic_memory import SemanticMemory
from jarvis.documents.retriever import PDFRetriever
from jarvis.memory.chroma_client import ChromaClient

logger = logging.getLogger(__name__)

class Application:
    """Coordinates the startup and lifecycle of the Jarvis application."""

    def __init__(self) -> None:
        self.router = CommandRouter()
        self.llm = LLMFactory.create()
        self.tool_registry = ToolRegistry()

        self.conversation = Conversation(
            system_prompt=(
                "You are Jarvis, a professional AI assistant. "
                "Be helpful, concise, and friendly."
            )
        )

        # Shared services
        self.embedding_service = EmbeddingService()
        
        self.chroma = ChromaClient()

        self.semantic_memory = SemanticMemory(
            self.embedding_service
        )

        # Document pipeline
        self.pdf_parser = PDFParser()
        self.text_chunker = TextChunker()

        self.document_indexer = DocumentIndexer(
            parser=self.pdf_parser,
            chunker=self.text_chunker,
            embedding_service=self.embedding_service,
        )

        self.document_service = DocumentService(
            self.document_indexer
        )

        self.pdf_retriever = PDFRetriever(
            self.embedding_service
        )

        # Chat service (create LAST)
        self.chat_service = ChatService(
            llm=self.llm,
            conversation=self.conversation,
            tools=self.tool_registry,
            semantic_memory=self.semantic_memory,
            pdf_retriever=self.pdf_retriever,
        )
        
    def initialize(self) -> None:
        logger.info("Initializing application...")

    def run(self) -> None:
        logger.info(
            "Application started (version=%s, environment=%s)",
            settings.app_version,
            "development",
        )

        print("=" * 50)
        print("🤖 Jarvis v2")
        print("Type 'help' to see available commands.")
        print("Type 'exit' to quit.")
        print("=" * 50)

        try: 
            while True:
                prompt = input("\nYou: ")

                if not prompt.strip():
                    continue

                command = self.router.route(prompt)

                if command == CommandType.EXIT:
                    break

                if command == CommandType.HELP:
                    print(
                        """
                        Available Commands
                        ------------------
                        help    - Show available commands
                        clear   - Clear the terminal
                        exit    - Exit Jarvis

                        Anything else will be sent to the AI.
                        """
                    )
                    continue

                if command == CommandType.CLEAR:
                    os.system("cls" if os.name == "nt" else "clear")
                    continue
                
                if command == CommandType.INDEX_PDF:
                    pdf_path = (
                        prompt.replace("index ", "", 1)
                        .strip()
                        .strip('"')
                    )
                    try:
                        self.document_service.index_pdf(Path(pdf_path))
                        print("\nPDF indexed successfully.")
                    except Exception as e:
                        print(f"\nFailed to index PDF: {e}")
                    continue
                
                if command == CommandType.CLEAR_DOCUMENTS:
                    self.chroma.delete_collection("documents")
                    print("\nDocuments cleared.")
                    continue

                if command == CommandType.CLEAR_MEMORY:
                    self.chroma.delete_collection("semantic_memory")
                    print("\nSemantic memory cleared.")
                    continue

                if command == CommandType.CLEAR_ALL:
                    self.chroma.delete_collection("documents")
                    self.chroma.delete_collection("semantic_memory")
                    print("\nAll vector data cleared.")
                    continue
                
                if command == CommandType.DOCUMENTS:
                    results = self.document_service.list_documents()
                    metadata = results.get("metadatas", [])
                    if not metadata:
                        print("\nNo indexed documents.")
                        continue
                    print("\nIndexed Documents\n")
                    documents = {}
                    for item in metadata:
                        name = item["document_name"]
                        documents[name] = documents.get(name, 0) + 1
                    for name, chunks in documents.items():
                        print(f"{name} ({chunks} chunks)")
                    continue
                
                if command == CommandType.DELETE_DOCUMENT:
                    document_name = (
                        prompt.replace(
                            "delete document ",
                            "",
                            1,
                        )
                        .strip()
                    )
                    deleted = self.document_service.delete_document(
                        document_name
                    )
                    print(
                        f"\nDeleted {deleted} chunks "
                        f"from '{document_name}'."
                    )
                    continue
                # tool_result = self.tool_registry.execute(prompt)
                # if tool_result is not None:
                #     print(f"\nJarvis: {tool_result}")
                #     continue
                
                try:
                    print("\nJarvis: ", end="", flush=True)

                    for chunk in self.chat_service.chat(prompt):
                        print(chunk, end="", flush=True)

                    print()

                except Exception:
                    logger.exception("Failed to generate response")
                    print("\nJarvis: Sorry, something went wrong.")
        finally:
            self.shutdown()

    def shutdown(self) -> None:
        logger.info("Shutting down application...")
        self.conversation.close()