from __future__ import annotations

from pathlib import Path
import chromadb

from app.common.config import settings
from app.common.utils import read_jsonl, ensure_dir
from app.embeddings.embedder import EmbeddingService


def build_index() -> None:
    ensure_dir(settings.vectordb_dir)

    chunks = read_jsonl(Path(settings.processed_dir) / "chunks.jsonl")
    texts = [chunk["text"] for chunk in chunks]
    ids = [chunk["chunk_id"] for chunk in chunks]

    metadatas = []
    for chunk in chunks:
        metadata = {
            "doc_id": chunk["doc_id"],
            "title": chunk["title"],
            "source": chunk["source"],
            "source_type": chunk["source_type"],
            "credibility": chunk["credibility"],
            "language": chunk["language"],
            "year": chunk["year"] if chunk["year"] is not None else -1,
            "chunk_index": chunk["chunk_index"],
            "theme": ", ".join(chunk["theme"]),
        }
        metadatas.append(metadata)

    embedder = EmbeddingService(settings.embedding_model)
    embeddings = embedder.embed_texts(texts)

    client = chromadb.PersistentClient(path=settings.vectordb_dir)

    try:
        client.delete_collection(settings.chroma_collection)
    except Exception:
        pass

    collection = client.create_collection(name=settings.chroma_collection)

    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    print(f"Indexed chunks: {len(ids)}")