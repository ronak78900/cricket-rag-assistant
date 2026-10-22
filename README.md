# cricket-rag-assistant

Corrective RAG assistant for cricket. It answers rules questions from the Laws and playing conditions with citations, answers stats questions through read-only SQL over ball-by-ball data, and flags when a newer rule supersedes an older one.

Status: Day 1 (model router set up).

## Day 1 setup

1. Install Python 3.11 or 3.12.
2. Create the environment and install:
   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -e .
   ```
3. Copy `.env.example` to `.env` and add your free keys from console.groq.com and aistudio.google.com.
4. Install Ollama, then run `ollama pull llama3.2:3b`.
5. Run the smoke test:
   ```bash
   python scripts/smoke_test.py
   ```

You should see `[ ok ]` for each provider you configured and for the structured-output check. A `[skip]` for a provider with no key is fine. Model names and free-tier limits change, so edit them in `.env` rather than in code.

## Git

```bash
git init
git add .
git commit -m "Day 1: project skeleton and model router"
git branch -M main
git remote add origin https://github.com/<your-username>/cricket-rag-assistant.git
git push -u origin main
```

Never commit `.env`. The included `.gitignore` already excludes it.

## Layout

```
src/llm/        model router (Ollama, Groq, Gemini with fallback)
src/ingestion/  PDF parsing and chunking (Week 1)
src/retrieval/  Qdrant, hybrid search, reranker (Week 2)
src/graph/      LangGraph corrective RAG (Week 3)
src/eval/       Ragas evaluation (Week 4)
src/api/        FastAPI streaming service (Week 4)
```
