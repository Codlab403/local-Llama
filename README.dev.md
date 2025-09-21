# Developer quickstart (local)

This tiny guide shows how to run the backend locally and run tests.

Prerequisites
- Python 3.11+ (recommended)
- Optional: `uv` (astral) or a virtualenv

Start backend (PowerShell):

```powershell
# From repo root
.\dev.ps1
```

Run tests:

```powershell
.\run_tests.ps1
```

Notes
- The dev server script starts Uvicorn without the auto-reloader because the reloader can spawn child processes and cause immediate shutdowns in some environments. Use the `--reload` flag manually if you need it.
- For TDD, the repository tests use FastAPI TestClient and run fast without a running server.
 - Observability: a lightweight observability stub is wired into the API middleware. Replace `backend/src/observability.py` with your LangSmith/OpenTelemetry adapter as needed.
 - Cross-encoder reranker: set the `USE_CROSS_ENCODER=1` environment variable to enable the cross-encoder reranker (requires `sentence-transformers` and model weights). By default the reranker falls back to deterministic embeddings for hermetic tests.
