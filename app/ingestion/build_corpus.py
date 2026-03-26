from __future__ import annotations

from pathlib import Path

from app.common.config import settings
from app.common.utils import ensure_dir, write_jsonl
from app.ingestion.parse_pdf import parse_pdf_to_document
from app.ingestion.chunker import build_chunks


def build_corpus() -> None:
    ensure_dir(settings.processed_dir)

    pdf_dir = Path(settings.raw_pdf_dir)
    pdf_files = sorted(pdf_dir.glob("*.pdf"))

    documents = []
    chunks = []

    for idx, pdf_file in enumerate(pdf_files, start=1):
        doc = parse_pdf_to_document(
            pdf_path=str(pdf_file),
            doc_id=f"doc_{idx:03d}",
            title=pdf_file.stem,
            source="manual_import",
            source_type="pdf",
            credibility="B",
            theme=["enterprise_data_intelligence"],
            language="en",
            year=None,
        )
        documents.append(doc.model_dump())

        doc_chunks = build_chunks(
            document=doc,
            chunk_size=settings.chunk_size,
            overlap=settings.chunk_overlap,
        )
        chunks.extend([c.model_dump() for c in doc_chunks])

    write_jsonl(Path(settings.processed_dir) / "documents.jsonl", documents)
    write_jsonl(Path(settings.processed_dir) / "chunks.jsonl", chunks)

    print(f"Documents processed: {len(documents)}")
    print(f"Chunks generated: {len(chunks)}")