import json


class SearchResultFormatter:
    """Formats search results before sending them to the LLM."""

    MAX_CHARS = 3000

    def format(
        self,
        results: list[dict],
    ) -> str:

        formatted = []

        for item in results:

            block = []

            if item.get("title"):
                block.append(f"Title: {item['title']}")

            if item.get("content"):
                block.append(f"Content: {item['content']}")

            if item.get("url"):
                block.append(f"Source: {item['url']}")

            formatted.append("\n".join(block))

        text = "\n\n".join(formatted)

        if len(text) > self.MAX_CHARS:
            text = text[: self.MAX_CHARS] + "..."

        return text