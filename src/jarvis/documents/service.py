from pathlib import Path

from jarvis.documents.indexer import DocumentIndexer
from jarvis.memory.chroma_client import ChromaClient


class DocumentService:
    """High-level service for document operations."""

    def __init__(
        self,
        indexer: DocumentIndexer,
    ) -> None:
        self.indexer = indexer
        self.collection = (
            ChromaClient()
            .get_collection("documents")
        )

    def index_pdf(
        self,
        pdf_path: Path,
    ) -> None:
        self.indexer.index(pdf_path)

    def list_documents(self) -> dict:
        """Return all indexed documents."""

        return self.collection.get(
            include=["metadatas"]
        )
        
    def delete_document(
        self,
        document_name: str,
    ) -> int:
        """Delete all chunks belonging to a document."""

        results = self.collection.get(
            include=["metadatas"]
        )

        ids_to_delete = []

        for doc_id, metadata in zip(
            results["ids"],
            results["metadatas"],
        ):
            if metadata["document_name"] == document_name:
                ids_to_delete.append(doc_id)

        if ids_to_delete:
            self.collection.delete(ids=ids_to_delete)

        return len(ids_to_delete)