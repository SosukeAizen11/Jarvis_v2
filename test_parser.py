from pathlib import Path

from jarvis.documents.chunker import TextChunker
from jarvis.documents.indexer import DocumentIndexer
from jarvis.documents.parser import PDFParser
from jarvis.documents.retriever import PDFRetriever
from jarvis.services.embedding_service import EmbeddingService

embedding = EmbeddingService()

parser = PDFParser()
chunker = TextChunker()

indexer = DocumentIndexer(
    parser,
    chunker,
    embedding,
)

# Run only once to index the PDF
indexer.index(
    Path(r"C:\Users\sumit mandaliya\Documents\Downloads\The Ultimate Python Handbook.pdf")
)

retriever = PDFRetriever(embedding)

results = retriever.search(
    "What is ArcForge?"
)

print(results)