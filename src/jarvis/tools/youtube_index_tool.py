from jarvis.tools.base import BaseTool
from jarvis.youtube_rag.service import YouTubeRAGService


class YouTubeIndexTool(BaseTool):
    """Indexes a YouTube video into Jarvis knowledge."""

    def __init__(self) -> None:
        self.service = YouTubeRAGService()

    @property
    def name(self) -> str:
        return "youtube_index"

    @property
    def description(self) -> str:
        return (
            "Indexes a YouTube video so it can be used to answer future questions."
        )

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL of the YouTube video to index.",
                }
            },
            "required": ["url"],
        }

    def execute(self, url: str = "") -> str:
        """Index the YouTube video."""

        self.service.index_video(url)

        return "Successfully indexed the YouTube video."

    def execute_from_arguments(
        self,
        arguments: dict,
    ) -> str:
        """Execute from LLM tool arguments."""

        url = arguments["url"]

        return self.execute(url)