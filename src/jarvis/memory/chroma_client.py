import chromadb


class ChromaClient:
    """Creates and manages the ChromaDB client."""

    def __init__(self) -> None:
        self.client = chromadb.PersistentClient(
            path="data/chroma"
        )

    def get_collection(self):
        """Return the semantic memory collection."""

        return self.client.get_or_create_collection(
            name="semantic_memory"
        )