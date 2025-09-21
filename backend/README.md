Backend quick reference
======================

This backend is a minimal local-first RAG prototype used for development and testing.

Database (metadata)
- SQLite DB file: data/metadata.db
- Table: ingest_tasks
  - task_id TEXT PRIMARY KEY
  - filename TEXT
  - upload_path TEXT
  - status TEXT
  - created_at TEXT (UTC ISO)
  - attempts INTEGER
  - next_retry_at TEXT (UTC ISO)
  - last_error TEXT (error message, truncated)
  - last_error_at TEXT (UTC ISO)

Migrations (local dev)
- Simple migration runner is provided at `backend/migrations/apply_migrations.py`.
- Migrations are stored as SQL files in `backend/migrations/` and applied in lexical order.

Run migrations locally (PowerShell):
```pwsh
cd C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot
python .\backend\migrations\apply_migrations.py
```

Notes
- The migration runner is intentionally minimal and safe for local dev. For production use a full migration tool like Alembic.
- The runner attempts to re-use the application's DB path (via `backend.src.db.meta.DB_PATH`) so it migrates the same DB the app uses.

Observability
-------------

The backend includes a small observability wrapper at `backend/src/observability.py` that:

- Always provides a lightweight in-process tracer (logs span start/end) so traces are available even without extra deps.
- Optionally configures OpenTelemetry OTLP exporter and a LangSmith exporter when requested via environment variables.

Environment variables
- `ENABLE_OTLP=1` — try to configure an OTLP exporter (requires `opentelemetry` packages to be installed).
- `OTLP_ENDPOINT` — optional endpoint for the OTLP exporter (e.g. `http://localhost:4317`).
- `ENABLE_LANGSMITH=1` — try to configure a LangSmith exporter (requires LangSmith exporter to be available).

Example (PowerShell) to enable OTLP to a local collector:

```pwsh
# Set env and run the server in the current shell session
$env:ENABLE_OTLP = '1'
$env:OTLP_ENDPOINT = 'http://localhost:4317'
uv run uvicorn backend.src.api.main:app --reload --host 127.0.0.1 --port 8000
```

If the optional packages are not installed the application will continue to run with the fallback tracer; enabling the env vars is a safe no-op in that case.

Running a local OTLP collector (optional)
----------------------------------------

You can run a local OpenTelemetry Collector that will accept OTLP traces and print them to stdout (useful for local testing):

```pwsh
# From repo root
docker compose up otel-collector
# or on older Docker Compose
docker-compose up
```

Collector config is `backend/otel-collector-config.yaml` and docker-compose entrypoint `docker-compose.yml` maps OTLP ports 4317 (gRPC) and 4318 (HTTP).
