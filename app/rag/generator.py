from __future__ import annotations

import ollama

from app.common.config import settings


class LocalGenerator:
    def __init__(self) -> None:
        self.model_name = settings.ollama_model

    def generate(self, prompt: str) -> str:
        response = ollama.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise technical assistant. "
                        "Do not fabricate facts. Use only the supplied context."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        return response["message"]["content"]