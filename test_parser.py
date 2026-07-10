from pathlib import Path

from jarvis.documents.chunker import TextChunker
from jarvis.documents.parser import PDFParser

parser = PDFParser()
chunker = TextChunker()

text = parser.parse(
    Path(r"C:\Users\sumit mandaliya\Documents\Downloads\ARCForge.pdf")
)

chunks = chunker.split(text)

print(f"Chunks: {len(chunks)}")
print()
print(chunks[0])