from tavily import TavilyClient

from jarvis.config.settings import settings


class WebSearchTool:
    """Search the web using Tavily."""

    def __init__(self) -> None:
        self.client = TavilyClient(
            api_key=settings.tavily_api_key,
        )

    @property
    def name(self) -> str:
        return "web_search"

    def execute(
        self,
        query: str,
    ) -> list[dict]:
        """Search the web and return the results."""

        query_lower = query.lower()

        is_recent_query = any(
            word in query_lower
            for word in [
                "today",
                "latest",
                "recent",
                "current",
                "news",
                "now",
            ]
        )

        response = self.client.search(
            query=query,
            topic="news" if is_recent_query else "general",
            search_depth="advanced",
            max_results=5,
        )

        return response["results"]

    def to_groq_tool(self) -> dict:
        """Return the tool definition for Groq."""

        return {
            "type": "function",
            "function": {
                "name": "web_search",
                "description": (
                    "Search the web for current, recent, or factual information "
                    "that is not available from other knowledge sources."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query",
                        }
                    },
                    "required": ["query"],
                },
            },
        }
        
    def execute_from_arguments(
        self,
        arguments: dict,
    ) -> list[dict]:
        """Execute from LLM tool arguments."""

        query = arguments["query"]

        return self.execute(query)