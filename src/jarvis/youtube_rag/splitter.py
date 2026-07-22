"""
Text splitter for YouTube transcripts.
"""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class TranscriptSplitter:
    """Splits transcript documents into smaller chunks."""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> None:

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def split(
        self,
        documents: list[Document],
    ) -> list[Document]:

        return self.splitter.split_documents(documents)