"""
Retriever for YouTube transcript chunks.
"""

from langchain_core.documents import Document

from jarvis.youtube_rag.vector_store import VectorStore


class YouTubeRetriever:
    """Retrieves relevant transcript chunks."""

    def __init__(
        self,
        store: VectorStore,
        k: int = 4,
    ) -> None:

        self.retriever = store.store.as_retriever(
            search_kwargs={"k": k},
        )

    def retrieve(
        self,
        question: str,
    ) -> list[Document]:

        return self.retriever.invoke(question)