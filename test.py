from jarvis.memory.semantic_memory import SemanticMemory
from jarvis.services.embedding_service import EmbeddingService

embedding_service = EmbeddingService()

memory = SemanticMemory(embedding_service)

memory.add("I love Python.")
memory.add("I play cricket every Sunday.")
memory.add("My favorite drink is coffee.")

results = memory.search(
    "Which programming language do I enjoy?"
)

for result in results:
    print(result.text)