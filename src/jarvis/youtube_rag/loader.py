"""
YouTube transcript loader using LangChain.
"""

from langchain_community.document_loaders import YoutubeLoader
from langchain_core.documents import Document


class YouTubeLoader:
    """Loads a YouTube transcript as LangChain Documents."""

    def load(self, url: str) -> list[Document]:
        loader = YoutubeLoader.from_youtube_url(
            url,
            add_video_info=False,
        )

        return loader.load()