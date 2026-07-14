import uuid
from dataclasses import dataclass

from jarvis.memory.chroma_client import ChromaClient
from jarvis.services.embedding_service import EmbeddingService


@dataclass
class MemoryRecord:
    """Represents one semantic memory."""

    text: str


class SemanticMemory:
    """Stores and searches semantic memories using ChromaDB."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
    ) -> None:
        self.embedding_service = embedding_service

        self.collection = (
            ChromaClient()
            .get_collection("semantic_memory")
        )

    def add(self, text: str) -> None:
        """Generate an embedding and store it."""

        embedding = self.embedding_service.embed(text)

        self.collection.add(
            ids=[str(uuid.uuid4())],
            documents=[text],
            embeddings=[embedding],
        )

    def search(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[MemoryRecord]:
        """Return the most relevant memories."""

        query_embedding = self.embedding_service.embed(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        documents = results["documents"][0]

        return [
            MemoryRecord(text=document)
            for document in documents
        ]