from jarvis.youtube_rag.loader import YouTubeLoader
from jarvis.youtube_rag.retriever import YouTubeRetriever
from jarvis.youtube_rag.splitter import TranscriptSplitter
from jarvis.youtube_rag.vector_store import VectorStore


class YouTubeRAGService:
    """Coordinates YouTube RAG operations."""

    def __init__(self) -> None:
        self.loader = YouTubeLoader()
        self.splitter = TranscriptSplitter()
        self.store = VectorStore()
        self.retriever = YouTubeRetriever(self.store)

    def index_video(self, url: str) -> None:
        documents = self.loader.load(url)

        source = documents[0].metadata.get("source")

        if source:
            self.store.delete_by_source(source)
            VectorStore.set_active_source(source)

        chunks = self.splitter.split(documents)

        self.store.add_documents(chunks)

        print(f"Indexed {len(chunks)} chunks.")

    def retrieve(self, question: str):
        return self.retriever.retrieve(question)