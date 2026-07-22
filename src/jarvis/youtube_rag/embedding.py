"""
Embedding model used by YouTube RAG.
"""

from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingService:
    """Creates the embedding model."""

    def __init__(self) -> None:

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )