from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """Generates semantic embeddings for text."""

    def __init__(self) -> None:
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def embed(self, text: str) -> list[float]:
        """Convert text into an embedding vector."""

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
        )

        return embedding.tolist()