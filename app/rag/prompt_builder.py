from __future__ import annotations

from app.common.models import RetrievedChunk


def build_rag_prompt(user_question: str, chunks: list[RetrievedChunk]) -> str:
    context_parts = []
    for idx, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"[SOURCE {idx}]\n"
            f"Title: {chunk.title}\n"
            f"Source: {chunk.source}\n"
            f"Metadata: {chunk.metadata}\n"
            f"Content:\n{chunk.text}\n"
        )

    context = "\n\n".join(context_parts)

    return f"""
You are a technical validation assistant for Enterprise-Grade Data Intelligence.

You must:
1. Answer only based on the provided context.
2. Clearly separate factual support from inference.
3. Explicitly say when the context is insufficient.
4. Never invent references or concepts not grounded in the sources.
5. End with a confidence level: High, Medium, or Low.

User question:
{user_question}

Retrieved context:
{context}

Output format:
- Technical summary
- Supported points
- Gaps or uncertainties
- Confidence level
- Sources used
""".strip()