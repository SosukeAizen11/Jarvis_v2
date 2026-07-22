"""
Persistent Chroma vector store.
"""

from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document

from jarvis.youtube_rag.embedding import EmbeddingService


class VectorStore:
    """Stores transcript chunks in Chroma."""

    def __init__(self) -> None:

        persist_directory = (
            Path("data") / "youtube_rag"
        )

        embedding_service = EmbeddingService()

        self.store = Chroma(
            collection_name="youtube_rag",
            persist_directory=str(persist_directory),
            embedding_function=embedding_service.embeddings,
        )

    def add_documents(
        self,
        documents: list[Document],
    ) -> None:

        self.store.add_documents(documents)

    def count(self) -> int:
        return self.store._collection.count()
    
    def delete_by_source(self, source: str) -> None:
        """Delete all chunks belonging to a specific source."""

        self.store._collection.delete(
            where={"source": source}
        )


    def get_sources(self) -> list[str]:
        """Return all indexed sources."""

        metadata = self.store._collection.get(
            include=["metadatas"]
        )

        return list(
            {
                item["source"]
                for item in metadata["metadatas"]
                if item and "source" in item
            }
        )