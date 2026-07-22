from jarvis.youtube_rag.loader import YouTubeLoader
from jarvis.youtube_rag.splitter import TranscriptSplitter

def main() -> None:
    url = "https://www.youtube.com/watch?v=VzV3gww-nXk"

    loader = YouTubeLoader()
    documents = loader.load(url)

    splitter = TranscriptSplitter()

    chunks = splitter.split(documents)

    print(f"Original documents : {len(documents)}")
    print(f"Chunks created     : {len(chunks)}")

    print("\nFirst chunk:\n")
    print(chunks[0].page_content[:500])

    print("\nMetadata:\n")
    print(chunks[0].metadata)


if __name__ == "__main__":
    main()