# quickstart.md

Minimal local quickstart for the feature (developer preview):

Prerequisites
- Ollama installed and models available locally (or set REMOTE_LLM to true to use hosted endpoints)
- Python 3.11, pip, virtualenv

Steps (developer laptop)
1. Clone repo and checkout branch `001-title-local-first`.
2. Create and activate virtualenv: `python -m venv .venv && .venv\Scripts\Activate.ps1` (Windows PowerShell)
3. Install dependencies: `pip install -r requirements.txt` (file may be updated in main repo)
4. Start local API (PowerShell):

```pwsh
# from repo root
cd .\backend
# run inside project venv or use uv run if you use uv tooling
python -m uvicorn backend.src.api.main:app --host 127.0.0.1 --port 8000
```
5. (Optional but recommended) Apply DB migrations before running the server so the metadata DB has the latest columns:

```pwsh
# from repo root
python .\backend\migrations\apply_migrations.py
```
5. Open the frontend (if present) or use curl/postman to call APIs:
   - `POST /upload` to upload a PDF
   - Poll `GET /ingest/{task_id}` for indexing status
   - `POST /chat` to query and receive streamed tokens and final citations

Notes
- Default is local-only; enabling remote LLMs or telemetry requires updating configuration.
- No auth for MVP: run on a single-user machine or inside a secure network.
 - Observability: a simple tracer is wired into the API middleware and logs spans to the app logger. Replace `backend/src/observability.py` with LangSmith/OpenTelemetry for production.
 - Cross-encoder: to enable the cross-encoder reranker set `USE_CROSS_ENCODER=1` and install `sentence-transformers` and model weights. The service will fall back to deterministic embeddings if not enabled.
 - Cross-encoder: to enable the cross-encoder reranker set `USE_CROSS_ENCODER=1` and install `sentence-transformers` and model weights. The service will fall back to deterministic embeddings if not enabled.
    - Model name: set `CROSS_ENCODER_MODEL` to choose a different CrossEncoder; defaults to `cross-encoder/stsb-roberta-large`.
    - Caching: models are cached in-process by the adapter to avoid repeated downloads/instantiation. Use `backend/src/chat/cross_encoder_adapter.clear_cache()` in tests or scripts to reset the cache.
   - Programmatic access: the model name is also available via `backend.src.config.get_cross_encoder_model()` if you need to read it from Python code.

   Database notes
   - The ingestion task metadata table (`ingest_tasks`) now includes `last_error` and `last_error_at` columns. When a task fails after retries these fields will contain the failure message and the UTC timestamp (ISO) when the error was recorded.

Example API calls (PowerShell):

```pwsh
# upload a small text file
$resp = Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/v1/upload -Form @{ file = Get-Item './tests/fixtures/sample.txt' }
$resp | Format-List

# poll status
# replace $resp.task_id with the returned task id
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/api/v1/ingest/$($resp.task_id)"

# chat (simple example)
$body = @{ session_id = 'default'; query = 'Summarize the document' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/v1/chat -Body $body -ContentType 'application/json'
```

Example API calls (curl):

```bash
# upload
curl -F "file=@tests/fixtures/sample.txt" http://127.0.0.1:8000/api/v1/upload

# poll
curl http://127.0.0.1:8000/api/v1/ingest/<task_id>

# chat
curl -X POST -H "Content-Type: application/json" -d '{"session_id":"default","query":"Summarize the document"}' http://127.0.0.1:8000/api/v1/chat
```
