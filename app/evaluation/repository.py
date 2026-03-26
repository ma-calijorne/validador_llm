from __future__ import annotations

import sqlite3
from datetime import datetime

from app.common.config import settings
from app.common.models import EvaluationRecord


class EvaluationRepository:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(settings.sqlite_path, check_same_thread=False)
        self._create_table()

    def _create_table(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                evaluator_name TEXT,
                prompt TEXT NOT NULL,
                target_model_response TEXT NOT NULL,
                rag_assistant_response TEXT,
                retrieved_sources TEXT,
                score_correctness INTEGER,
                score_coverage INTEGER,
                score_enterprise_context INTEGER,
                score_grounding INTEGER,
                score_clarity INTEGER,
                score_terminology INTEGER,
                score_uncertainty INTEGER,
                score_hallucination_risk INTEGER,
                final_decision TEXT,
                evaluator_notes TEXT
            )
            """
        )
        self.conn.commit()

    def save(self, record: EvaluationRecord) -> None:
        self.conn.execute(
            """
            INSERT INTO evaluations (
                created_at,
                evaluator_name,
                prompt,
                target_model_response,
                rag_assistant_response,
                retrieved_sources,
                score_correctness,
                score_coverage,
                score_enterprise_context,
                score_grounding,
                score_clarity,
                score_terminology,
                score_uncertainty,
                score_hallucination_risk,
                final_decision,
                evaluator_notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.utcnow().isoformat(),
                record.evaluator_name,
                record.prompt,
                record.target_model_response,
                record.rag_assistant_response,
                record.retrieved_sources,
                record.score_correctness,
                record.score_coverage,
                record.score_enterprise_context,
                record.score_grounding,
                record.score_clarity,
                record.score_terminology,
                record.score_uncertainty,
                record.score_hallucination_risk,
                record.final_decision,
                record.evaluator_notes,
            ),
        )
        self.conn.commit()