from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class Document(BaseModel):
    doc_id: str
    title: str
    source: str
    source_type: str
    credibility: str
    theme: List[str]
    language: str
    year: Optional[int] = None
    file_path: str
    text: str


class Chunk(BaseModel):
    chunk_id: str
    doc_id: str
    title: str
    source: str
    source_type: str
    credibility: str
    theme: List[str]
    language: str
    year: Optional[int] = None
    text: str
    chunk_index: int
    page_start: Optional[int] = None
    page_end: Optional[int] = None


class RetrievedChunk(BaseModel):
    chunk_id: str
    doc_id: str
    title: str
    source: str
    text: str
    score: float
    metadata: dict = Field(default_factory=dict)


class EvaluationRecord(BaseModel):
    evaluator_name: Optional[str] = None
    prompt: str
    target_model_response: str
    rag_assistant_response: Optional[str] = None
    retrieved_sources: str
    score_correctness: int
    score_coverage: int
    score_enterprise_context: int
    score_grounding: int
    score_clarity: int
    score_terminology: int
    score_uncertainty: int
    score_hallucination_risk: int
    final_decision: str
    evaluator_notes: Optional[str] = None