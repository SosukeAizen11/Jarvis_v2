from jarvis.youtube_rag.service import YouTubeRAGService


def main():

    service = YouTubeRAGService()

    service.index_video(
        "https://www.youtube.com/watch?v=VzV3gww-nXk"
    )

    results = service.retrieve(
        "What is this video all about?"
    )

    print(f"Retrieved {len(results)} chunks\n")

    for index, document in enumerate(results, start=1):
        print(f"Chunk {index}")
        print("-" * 50)
        print(document.page_content[:300])
        print()


if __name__ == "__main__":
    main()