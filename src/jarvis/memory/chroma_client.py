from pathlib import Path

import chromadb


class ChromaClient:
    """Creates and manages the ChromaDB client."""

    def __init__(self) -> None:
        project_root = Path(__file__).resolve().parents[3]
        chroma_path = project_root / "data" / "chroma"

        self.client = chromadb.PersistentClient(
            path=str(chroma_path)
        )

    def get_collection(self, name: str):
        return self.client.get_or_create_collection(name=name)

    def delete_collection(self, name: str) -> None:
        """Delete a collection if it exists."""

        try:
            self.client.delete_collection(name)
        except Exception:
            pass

    def list_collections(self):
        """Return all collections."""

        return self.client.list_collections()