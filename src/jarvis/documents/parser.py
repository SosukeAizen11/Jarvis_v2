from pathlib import Path

import fitz


class PDFParser:
    """Extracts text from PDF documents."""

    def parse(self, pdf_path: Path) -> str:
        """Extract all text from a PDF."""

        document = fitz.open(pdf_path)

        pages = []

        for page in document:
            pages.append(page.get_text())

        document.close()

        return "\n\n".join(pages)