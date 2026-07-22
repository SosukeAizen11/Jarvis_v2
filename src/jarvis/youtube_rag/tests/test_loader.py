from jarvis.youtube_rag.loader import YouTubeLoader
from jarvis.youtube_rag.splitter import TranscriptSplitter
from jarvis.youtube_rag.vector_store import VectorStore


def main() -> None:

    url = "https://www.youtube.com/watch?v=VzV3gww-nXk"

    loader = YouTubeLoader()
    documents = loader.load(url)

    splitter = TranscriptSplitter()
    chunks = splitter.split(documents)

    store = VectorStore()

    store.add_documents(chunks)

    print(f"Chunks stored: {store.count()}")


if __name__ == "__main__":
    main()