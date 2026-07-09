import chromadb
from pathlib import Path


class ChromaClient:
    """Creates and manages the ChromaDB client."""

    def __init__(self) -> None:
        project_root = Path(__file__).resolve().parents[3]
        chroma_path = project_root / "data" / "chroma"
        
        self.client = chromadb.PersistentClient(
            path=str(chroma_path)
        )

    def get_collection(self):
        """Return the semantic memory collection."""

        return self.client.get_or_create_collection(
            name="semantic_memory"
        )