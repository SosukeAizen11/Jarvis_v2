import uuid
from pathlib import Path

from jarvis.documents.chunker import TextChunker
from jarvis.documents.parser import PDFParser
from jarvis.memory.chroma_client import ChromaClient
from jarvis.services.embedding_service import EmbeddingService


class DocumentIndexer:
    """Indexes PDF documents into ChromaDB."""

    def __init__(
        self,
        parser: PDFParser,
        chunker: TextChunker,
        embedding_service: EmbeddingService,
    ) -> None:
        self.parser = parser
        self.chunker = chunker
        self.embedding_service = embedding_service

        self.collection = (
            ChromaClient()
            .get_collection("documents")
        )
    
    def index(
        self,
        pdf_path: Path,
    ) -> None:
        """Parse, chunk, embed and store a PDF."""

        text = self.parser.parse(pdf_path)

        chunks = self.chunker.split(text)

        document_id = str(uuid.uuid4())

        embeddings = self.embedding_service.embed(chunks)

        ids = []
        metadatas = []

        for index, _ in enumerate(chunks):

            ids.append(str(uuid.uuid4()))

            metadatas.append(
                {
                    "document_id": document_id,
                    "document_name": pdf_path.name,
                    "chunk_index": index,
                    "source": "pdf",
                }
            )

        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )