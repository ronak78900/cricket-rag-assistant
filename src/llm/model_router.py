"""Hybrid model router: local Ollama + free cloud APIs (Groq, Gemini).

Each pipeline job (a "role") has a preferred provider order. If a provider is not
configured or fails at call time, the next one is tried automatically.
"""
from __future__ import annotations

import os
from enum import Enum
from typing import Callable

from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import Runnable
from pydantic import BaseModel

load_dotenv()


class Role(str, Enum):
    GRADER = "grader"            # cheap yes/no relevance checks -> local first
    REWRITER = "rewriter"        # query rewriting and routing -> fast cloud first
    SYNTHESIZER = "synthesizer"  # final cited answer -> long-context cloud first
    JUDGE = "judge"              # Ragas judge -> strong cloud model


# ---- provider factories (imports inside so a missing package only fails when used) ----

def _ollama() -> BaseChatModel:
    from langchain_ollama import ChatOllama

    return ChatOllama(
        model=os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        temperature=0,
    )


def _groq() -> BaseChatModel:
    from langchain_groq import ChatGroq

    return ChatGroq(model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"), temperature=0)


def _gemini() -> BaseChatModel:
    from langchain_google_genai import ChatGoogleGenerativeAI

    return ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"), temperature=0)


_FACTORIES: dict[str, Callable[[], BaseChatModel]] = {
    "ollama": _ollama,
    "groq": _groq,
    "gemini": _gemini,
}

_REQUIRED_KEY = {"ollama": None, "groq": "GROQ_API_KEY", "gemini": "GOOGLE_API_KEY"}

_PREFERENCE: dict[Role, list[str]] = {
    Role.GRADER: ["ollama", "groq", "gemini"],
    Role.REWRITER: ["groq", "gemini", "ollama"],
    Role.SYNTHESIZER: ["gemini", "groq", "ollama"],
    Role.JUDGE: ["gemini", "groq"],
}


def _available(role: Role) -> list[str]:
    names = []
    for name in _PREFERENCE[role]:
        key = _REQUIRED_KEY[name]
        if key is None or os.getenv(key):
            names.append(name)
    if not names:
        raise RuntimeError(f"No provider configured for role {role.value}. Check your .env file.")
    return names


def get_llm(role: Role) -> Runnable:
    """Return a chat model for this role, with automatic fallback to the next provider."""
    names = _available(role)
    models = [_FACTORIES[n]() for n in names]
    return models[0].with_fallbacks(models[1:]) if len(models) > 1 else models[0]


def get_structured_llm(role: Role, schema: type[BaseModel]) -> Runnable:
    """Return a model that outputs a validated Pydantic object, with provider fallback.

    Structured output is applied to each provider first, then the fallbacks are chained,
    because the fallback wrapper itself does not expose with_structured_output().
    """
    names = _available(role)
    chains = [_FACTORIES[n]().with_structured_output(schema) for n in names]
    return chains[0].with_fallbacks(chains[1:]) if len(chains) > 1 else chains[0]


def provider_for(name: str) -> BaseChatModel:
    """Get one specific provider (used by the smoke test)."""
    return _FACTORIES[name]()
