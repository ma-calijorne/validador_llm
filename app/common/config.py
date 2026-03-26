from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "llm_validation_mvp")
    data_dir: str = os.getenv("DATA_DIR", "./data")
    raw_pdf_dir: str = os.getenv("RAW_PDF_DIR", "./data/raw/pdf")
    processed_dir: str = os.getenv("PROCESSED_DIR", "./data/processed")
    vectordb_dir: str = os.getenv("VECTORDB_DIR", "./data/vectordb")
    sqlite_path: str = os.getenv("SQLITE_PATH", "./database/evaluations.db")

    embedding_model: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-base-en-v1.5")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

    chroma_collection: str = os.getenv(
        "CHROMA_COLLECTION", "enterprise_data_intelligence_docs"
    )
    top_k: int = int(os.getenv("TOP_K", "5"))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1200"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "200"))


settings = Settings()