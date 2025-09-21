# Changelog

## 0.1.0 - 2025-09-21

- Initial local-first RAG backend prototype.
- Implemented upload → ingest → index → retrieve skeleton with tests.
- Features:
  - FastAPI endpoints: `/upload`, `/ingest/{task_id}`, `/chat` (streaming skeleton)
  - SQLite metadata DB with `ingest_tasks` (attempts, next_retry_at, last_error)
  - Filesystem upload store under `data/uploads/`
  - Ingestion worker with retry/backoff and failure recording
  - Deterministic embedding/LLM adapters (stubs for tests)
  - RetrievER, reranker skeletons and LangChain orchestration stub
  - Observability: fallback tracer, optional OTLP & LangSmith exporters
  - Migration runner and SQL migration for schema changes
  - Tests: unit + integration (full suite passing locally)
