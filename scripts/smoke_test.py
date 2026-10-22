"""Day 1 smoke test: call every configured provider and a structured-output chain.

Run from the project root:
    python scripts/smoke_test.py
"""
from __future__ import annotations

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydantic import BaseModel, Field

from src.llm.model_router import Role, get_structured_llm, provider_for

PROMPT = "In one sentence, why do annual reports break naive text chunking?"


class Verdict(BaseModel):
    relevant: bool = Field(description="True if the passage helps answer the question")
    reason: str = Field(description="One short reason")


def test_provider(name: str, needs_key: str | None) -> None:
    if needs_key and not os.getenv(needs_key):
        print(f"[skip] {name}: {needs_key} not set")
        return
    start = time.time()
    try:
        reply = provider_for(name).invoke(PROMPT)
        print(f"[ ok ] {name} ({time.time() - start:.1f}s): {reply.content[:120]!r}")
    except Exception as exc:  # noqa: BLE001 - show any provider failure plainly
        print(f"[FAIL] {name}: {type(exc).__name__}: {str(exc)[:150]}")


def test_structured() -> None:
    try:
        llm = get_structured_llm(Role.GRADER, Verdict)
        result = llm.invoke(
            "Question: What was the 2026 timeout limit?\n"
            "Passage: The 2026 SLA lowers the payment timeout limit to 3 seconds.\n"
            "Is the passage relevant?"
        )
        print(f"[ ok ] structured output: {result}")
    except Exception as exc:  # noqa: BLE001
        print(f"[FAIL] structured output: {type(exc).__name__}: {str(exc)[:150]}")


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    test_provider("ollama", None)
    test_provider("groq", "GROQ_API_KEY")
    test_provider("gemini", "GOOGLE_API_KEY")
    test_structured()
