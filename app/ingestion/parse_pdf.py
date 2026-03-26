from __future__ import annotations

from pathlib import Path
import fitz

from app.common.models import Document
from app.ingestion.clean_text import clean_text


def parse_pdf_to_document(
    pdf_path: str,
    doc_id: str,
    title: str,
    source: str,
    source_type: str,
    credibility: str,
    theme: list[str],
    language: str = "en",
    year: int | None = None,
) -> Document:
    pdf_file = Path(pdf_path)
    full_text_parts: list[str] = []

    with fitz.open(pdf_file) as doc:
        for page in doc:
            full_text_parts.append(page.get_text("text"))

    text = clean_text("\n\n".join(full_text_parts))

    return Document(
        doc_id=doc_id,
        title=title,
        source=source,
        source_type=source_type,
        credibility=credibility,
        theme=theme,
        language=language,
        year=year,
        file_path=str(pdf_file),
        text=text,
    )