from __future__ import annotations


RUBRIC_FIELDS = [
    "score_correctness",
    "score_coverage",
    "score_enterprise_context",
    "score_grounding",
    "score_clarity",
    "score_terminology",
    "score_uncertainty",
    "score_hallucination_risk",
]


def compute_average_score(scores: dict[str, int]) -> float:
    values = [scores[field] for field in RUBRIC_FIELDS]
    return sum(values) / len(values)


def suggest_final_decision(avg_score: float) -> str:
    if avg_score >= 4.5:
        return "Aprovado"
    if avg_score >= 3.5:
        return "Parcialmente aprovado"
    if avg_score >= 2.5:
        return "Inconclusivo"
    return "Reprovado"