from dataclasses import dataclass
import math

from jarvis.services.embedding_service import EmbeddingService


@dataclass
class MemoryRecord:
    """Represents one semantic memory."""

    text: str
    embedding: list[float]


class SemanticMemory:
    """Stores embeddings and performs semantic search."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
    ) -> None:
        self.embedding_service = embedding_service
        self.memories: list[MemoryRecord] = []

    def add(self, text: str) -> None:
        """Generate an embedding and store it."""

        embedding = self.embedding_service.embed(text)

        self.memories.append(
            MemoryRecord(
                text=text,
                embedding=embedding,
            )
        )

    def search(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[MemoryRecord]:
        """Return the most semantically similar memories."""

        query_embedding = self.embedding_service.embed(query)

        scored_memories = []

        for memory in self.memories:

            score = self._cosine_similarity(
                query_embedding,
                memory.embedding,
            )

            scored_memories.append(
                (
                    score,
                    memory,
                )
            )

        scored_memories.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            memory
            for _, memory in scored_memories[:top_k]
        ]

    def _cosine_similarity(
        self,
        vector_a: list[float],
        vector_b: list[float],
    ) -> float:
        """Calculate cosine similarity between two vectors."""

        dot_product = sum(
            a * b
            for a, b in zip(vector_a, vector_b)
        )

        magnitude_a = math.sqrt(
            sum(a * a for a in vector_a)
        )

        magnitude_b = math.sqrt(
            sum(b * b for b in vector_b)
        )

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return dot_product / (
            magnitude_a * magnitude_b
        )

    def get_all(self) -> list[MemoryRecord]:
        """Return all stored memories."""

        return self.memories