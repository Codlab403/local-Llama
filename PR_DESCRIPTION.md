# PR: Implement local-first RAG backend skeleton (001-title-local-first)

Summary
-------

This PR introduces the initial local-first RAG backend prototype and implements the tasks described in `specs/001-title-local-first`. Key additions:

- FastAPI backend with endpoints for upload, ingest status, and chat orchestration
- SQLite metadata DB and migration runner; added `last_error`+`last_error_at` columns
- Filesystem upload store and ingestion worker with retry/backoff
- Deterministic LLM/embedding adapters for testing + vector store skeleton
- Observability wrapper with env toggles for OTLP and LangSmith and a safe fallback
- Unit and integration tests (all passing locally)
- Development tooling: pyproject.toml, ruff, black, pre-commit, and Docker Compose for OTLP collector

Testing
-------

Run tests locally:

```pwsh
cd backend
uv run pytest -q
```

Notes for reviewers
-------------------

- The migration runner (`backend/migrations/apply_migrations.py`) is intentionally minimal for local dev.
- Observability exporters are opt-in via env vars (`ENABLE_OTLP`, `OTLP_ENDPOINT`, `ENABLE_LANGSMITH`). The app will run with a fallback tracer even without those packages installed.
- The embedding/LLM adapters are stubs; integrating production adapters (Ollama / HF) is a next step and isolated behind adapter modules.
