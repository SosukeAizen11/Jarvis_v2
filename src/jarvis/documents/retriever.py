from jarvis.memory.chroma_client import ChromaClient
from jarvis.services.embedding_service import EmbeddingService


class PDFRetriever:
    """Retrieves relevant chunks from indexed documents."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
    ) -> None:
        self.embedding_service = embedding_service

        self.collection = (
            ChromaClient()
            .get_collection("documents")
        )
        
    def search(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[str]:
        """Return relevant document chunks."""

        query_embedding = self.embedding_service.embed(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        documents = results["documents"][0]

        return documents