from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """Generates semantic embeddings for text."""

    def __init__(self) -> None:
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def embed(
        self,
        text: str | list[str],
    ) -> list[float] | list[list[float]]:
        """Generate embeddings for one or many texts."""

        embeddings = self.model.encode(
            text,
            convert_to_numpy=True,
        )

        return embeddings.tolist()