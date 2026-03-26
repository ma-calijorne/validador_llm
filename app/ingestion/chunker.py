from __future__ import annotations

from app.common.models import Document, Chunk


def split_text_with_overlap(text: str, chunk_size: int, overlap: int) -> list[str]:
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    chunks: list[str] = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == text_len:
            break
        start = end - overlap

    return chunks


def build_chunks(
    document: Document,
    chunk_size: int,
    overlap: int,
) -> list[Chunk]:
    raw_chunks = split_text_with_overlap(document.text, chunk_size, overlap)

    chunks: list[Chunk] = []
    for idx, chunk_text in enumerate(raw_chunks):
        chunks.append(
            Chunk(
                chunk_id=f"{document.doc_id}_chunk_{idx:04d}",
                doc_id=document.doc_id,
                title=document.title,
                source=document.source,
                source_type=document.source_type,
                credibility=document.credibility,
                theme=document.theme,
                language=document.language,
                year=document.year,
                text=chunk_text,
                chunk_index=idx,
            )
        )

    return chunks