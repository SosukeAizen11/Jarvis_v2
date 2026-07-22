from jarvis.youtube_rag.loader import YouTubeLoader


def main() -> None:
    url = "https://www.youtube.com/watch?v=VzV3gww-nXk"

    loader = YouTubeLoader()

    documents = loader.load(url)

    print(f"Documents: {len(documents)}")
    print()
    print(documents[0].page_content[:500])


if __name__ == "__main__":
    main()