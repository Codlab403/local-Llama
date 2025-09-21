# quickstart.md

Minimal local quickstart for the feature (developer preview):

Prerequisites
- Ollama installed and models available locally (or set REMOTE_LLM to true to use hosted endpoints)
- Python 3.11, pip, virtualenv

Steps (developer laptop)
1. Clone repo and checkout branch `001-title-local-first`.
2. Create and activate virtualenv: `python -m venv .venv && .venv\Scripts\Activate.ps1` (Windows PowerShell)
3. Install dependencies: `pip install -r requirements.txt` (file may be updated in main repo)
4. Start local API: `uvicorn src.main:app --reload --host 127.0.0.1 --port 8000`
5. Open the frontend (if present) or use curl/postman to call APIs:
   - `POST /upload` to upload a PDF
   - Poll `GET /ingest/{task_id}` for indexing status
   - `POST /chat` to query and receive streamed tokens and final citations

Notes
- Default is local-only; enabling remote LLMs or telemetry requires updating configuration.
- No auth for MVP: run on a single-user machine or inside a secure network.
 - Observability: a simple tracer is wired into the API middleware and logs spans to the app logger. Replace `backend/src/observability.py` with LangSmith/OpenTelemetry for production.
 - Cross-encoder: to enable the cross-encoder reranker set `USE_CROSS_ENCODER=1` and install `sentence-transformers` and model weights. The service will fall back to deterministic embeddings if not enabled.
