from __future__ import annotations

import chromadb

from app.common.config import settings
from app.common.models import RetrievedChunk
from app.embeddings.embedder import EmbeddingService


class Retriever:
    def __init__(self) -> None:
        self.client = chromadb.PersistentClient(path=settings.vectordb_dir)
        self.collection = self.client.get_collection(settings.chroma_collection)
        self.embedder = EmbeddingService(settings.embedding_model)

    def search(self, query: str, top_k: int | None = None) -> list[RetrievedChunk]:
        query_embedding = self.embedder.embed_query(query)
        k = top_k or settings.top_k

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
        )

        retrieved: list[RetrievedChunk] = []
        ids = results["ids"][0]
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        distances = results["distances"][0] if "distances" in results else [0.0] * len(ids)

        for chunk_id, doc_text, meta, score in zip(ids, docs, metas, distances):
            retrieved.append(
                RetrievedChunk(
                    chunk_id=chunk_id,
                    doc_id=meta["doc_id"],
                    title=meta["title"],
                    source=meta["source"],
                    text=doc_text,
                    score=float(score),
                    metadata=meta,
                )
            )

        return retrieved