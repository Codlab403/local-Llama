````markdown
# Tasks: Local-first RAG chatbot core (001-title-local-first)

**Input**: `plan.md`, `spec.md`, `data-model.md`, `contracts/openapi.yaml`, `research.md`
**Prerequisites**: Phase 0 & Phase 1 artifacts exist (done)

## Execution Flow (derived)
1. Generate failing contract tests for each contract in `specs/001-title-local-first/contracts/` (must fail).
2. Generate model schemas for entities in `data-model.md` under `src/models/`.
3. Create persistence layer and adapters: SQLite metadata, local FS raw storage, vector-store adapter.
4. Implement ingestion pipeline and background task runner with task ids.
5. Implement chat endpoint that streams tokens and assembles final response with citations.
6. Add nightly evaluation job (skeleton) and admin metrics endpoint wiring.

## Format: `[ID] [P?] Description` (see template rules)

## Phase 3.1: Setup
- [ ] T001 Initialize Python project and virtualenv in `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\` (use venv/Poetry)
- [ ] T002 [P] Create `backend/` with `backend/src/`, `backend/tests/`, `backend/pyproject.toml`
- [ ] T003 [P] Configure linting and formatting (ruff/black/isort) in repo root

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE IMPLEMENTATION
These tests must be written and fail before implementation code is added.
- [ ] T004 [P] Contract test for POST `/upload` in `backend/tests/contract/test_upload_post.py` — assert 200 and task id format
- [ ] T005 [P] Contract test for GET `/ingest/{task_id}` in `backend/tests/contract/test_ingest_get.py` — assert status states (queued|indexing|ready|error)
- [ ] T006 [P] Contract test for POST `/chat` in `backend/tests/contract/test_chat_post.py` — assert streaming tokens and final JSON includes `citations` array and `confidence` float
 - [x] T004 [P] Contract test for POST `/upload` in `backend/tests/contract/test_upload_post.py` — assert 200 and task id format (created)
 - [x] T005 [P] Contract test for GET `/ingest/{task_id}` in `backend/tests/contract/test_ingest_get.py` — assert status states (queued|indexing|ready|error) (created)
 - [x] T006 [P] Contract test for POST `/chat` in `backend/tests/contract/test_chat_post.py` — assert streaming tokens and final JSON includes `citations` array and `confidence` float (created)
- [ ] T007 [P] Integration test: upload small PDF and verify ingestion task completes to `ready` in `backend/tests/integration/test_ingest_pipeline.py`

## Phase 3.3: Core Implementation (ONLY after tests fail)
- [ ] T008 [P] Implement `src/models/document.py` (Document JSON schema) at `backend/src/models/document.py` from `data-model.md`
- [ ] T009 [P] Implement `backend/src/models/node.py` (Node/Chunk schema)
 - [x] T010 [P] Implement `backend/src/db/meta.py` — SQLite wrapper to persist metadata and task state (created)
 - [x] T011 [P] Implement `backend/src/storage/fs_store.py` — save raw uploads to `data/uploads/` and return file path (created)
 - [x] T012 Implement ingestion background worker `backend/src/ingest/worker.py` and task API wiring (created)
 - [x] T013 Implement `backend/src/embeddings/adapter.py` — wrapper for LlamaIndex embeddings to local vector store (Chroma fallback) (created)
 - [x] T014 Implement `backend/src/chat/handler.py` — chat orchestration: retrieve, rerank, synthesize (uses Ollama by default) (skeleton created)
 - [x] T015 Implement `backend/src/api/upload.py` — POST /upload endpoint wiring to queue ingest task (implemented in `backend/src/api/main.py`)
 - [x] T016 Implement `backend/src/api/ingest.py` — GET /ingest/{task_id} status endpoint (implemented in `backend/src/api/main.py`)
 - [x] T017 Implement `backend/src/api/chat.py` — POST /chat endpoint streaming tokens and final response assembly (implemented in `backend/src/api/main.py`)

## Phase 3.4: Integration
 - [x] T018 Connect retriever to vector DB adapter in `backend/src/chat/retriever.py` (skeleton created)
 - [x] T019 Add cross-encoder reranker in `backend/src/chat/reranker.py` (skeleton created)
 - [x] T020 Add request/response logging and traces via LangSmith hooks in `backend/src/observability.py` (implemented; env toggles for OTLP/LangSmith; fallback tracer)

## Phase 3.5: Polish
- [ ] T021 [P] Unit tests for models in `backend/tests/unit/test_models.py`
- [ ] T022 Nightly evaluation skeleton: `backend/src/eval/nightly.py` and job registration
- [ ] T023 [P] Docs: update `specs/001-title-local-first/quickstart.md` with exact run commands and env vars

## Dependencies & Ordering
- Tests (T004-T007) must be created and failing before T008-T017 are implemented.
- T008-T011 should be parallel where possible (different files).
- T012 (worker) depends on T011 and T013.

````markdown
# Tasks: Local-first RAG chatbot core (001-title-local-first)

**Feature dir**: C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\specs\001-title-local-first
**Repo root**: C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot
**Input**: `plan.md`, `spec.md`, `data-model.md`, `contracts/openapi.yaml`, `research.md`, `quickstart.md`
**Prerequisites**: Phase 0 & Phase 1 artifacts exist (done)

## Execution Flow (derived)
1. Create failing contract tests (one per endpoint in `contracts/openapi.yaml`) at `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\tests\contract\`.
2. Create integration test scenario(s) from `quickstart.md` at `backend/tests/integration/`.
3. Create model files from `data-model.md` under `backend/src/models/`.
4. Implement persistence (SQLite) + raw FS storage + vector-store adapter under `backend/src/`.
5. Implement ingestion worker and API wiring (endpoints in `contracts/openapi.yaml`).
6. Implement chat orchestration and streaming endpoint; add nightly eval skeleton.

## Format: `[ID] [P?] Description` (explicit absolute paths and sample commands)

## Phase 3.1: Setup
- [ ] T001 Initialize Python project and virtualenv in repo root
	- Files/paths created: `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\.venv` (managed by `uv`), `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\uv.lock`
	- Use Astral `uv` for project, venv, and dependency management. Example PowerShell flow:
		```pwsh
		# Install uv (one-time - choose installer or pipx)
		# Option A: installer (recommended):
		iwr https://astral.sh/uv/install.ps1 -useb | iex
		# Option B: pipx (if you prefer pipx-managed):
		pipx install uv

		# Initialize a uv project in backend/ (creates project metadata)
		cd C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend
		uv init local-rag

		# Add runtime and tooling dependencies (FastAPI + Uvicorn + extras)
		uv add fastapi "uvicorn[standard]" python-multipart requests

		# Create a .venv for the project (uv will create .venv automatically)
		uv venv --python 3.11

		# Lock and sync dependencies (reproducible lockfile)
		uv lock
		uv sync

		# Run dev server via uv (runs inside the project environment)
		uv run uvicorn backend.src.api.main:app --reload --host 0.0.0.0 --port 8000
		```

	- Notes: `uv` provides a pip-compatible interface (`uv pip`) and workspace features; use `uv lock`/`uv sync` to maintain reproducible installs.

- [ ] T002 [P] Create `backend/` structure
	- Create directories:
		- `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\src\models\`
		- `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\src\api\`
		- `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\tests\contract\`
		- `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\tests\integration\`

- [ ] T003 [P] Add linting/format configs in repo root
	- Add `pyproject.toml` or `.flake8`, `pyproject.toml` entries, `.pre-commit-config.yaml`

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE IMPLEMENTATION
These tests must be created and intentionally failing.

- [ ] T004 [P] Contract test for POST `/upload`
	- Path: `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\tests\contract\test_upload_post.py`
	- Purpose: assert API returns 200 and JSON {"task_id": "<uuid>"}
	- Test skeleton (agent command creates this file with content):
		```pwsh
		@'
		import re
		import requests

		def test_upload_returns_task_id():
				url = "http://localhost:8000/upload"
				files = {"file": ("sample.txt", "hello world")}
				r = requests.post(url, files=files)
				assert r.status_code == 200
				assert "task_id" in r.json()
		'@ | Out-File -FilePath 'C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\tests\contract\test_upload_post.py' -Encoding utf8
		```

- [ ] T005 [P] Contract test for GET `/ingest/{task_id}`
	- Path: `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\tests\contract\test_ingest_get.py`
	- Purpose: assert status is one of queued|indexing|ready|error
	- Test skeleton: creates file with a placeholder task id and asserts allowed states

- [ ] T006 [P] Contract test for POST `/chat`
	- Path: `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\tests\contract\test_chat_post.py`
	- Purpose: assert streaming behavior (can be approximated) and final JSON contains `citations` and `confidence`
	- Test skeleton: POST to `/chat` and assert keys in final JSON

- [ ] T007 [P] Integration test: ingest pipeline
	- Path: `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\tests\integration\test_ingest_pipeline.py`
	- Purpose: upload a small PDF/text, poll `/ingest/{task_id}` until status `ready` or `error` (timeout 30s)
	- Test skeleton creates a `tests/fixtures/sample.txt` and runs the flow

## Phase 3.3: Core Implementation (ONLY after tests fail)
- [ ] T008 [P] Implement model `Document` at `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\src\models\document.py`
	- Use fields from `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\specs\001-title-local-first\data-model.md`

- [ ] T009 [P] Implement model `Node` at `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\src\models\node.py`

- [ ] T010 [P] Implement SQLite metadata wrapper at `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\src\db\meta.py`
	- Must support: create tables, insert/update document/task state, query by id

- [ ] T011 [P] Implement FS storage at `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\src\storage\fs_store.py`
	- Store uploads under `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\data\uploads\` and return absolute file path

- [ ] T012 Implement ingestion worker at `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\src\ingest\worker.py`
	- Worker reads queued tasks from SQLite and updates task status; on processing it writes nodes and calls embedding adapter

- [ ] T013 Implement embedding adapter at `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\src\embeddings\adapter.py`
	- Provide `embed_text(text: str) -> List[float]` and a `persist(embedding, node_id)` primitive (Chroma fallback)

- [ ] T014 Implement chat handler at `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\src\chat\handler.py`
 - [ ] T014 Implement chat handler at `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\src\chat\handler.py`
 - [x] T014a [P] LangChain orchestration skeleton at `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\src\chat\handler.py` (created)
	- Orchestrates retrieval, reranking, synthesis (Ollama by default), and returns streaming tokens and final JSON with `citations` and `confidence`

- [ ] T015 Implement API endpoint `POST /upload` at `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\src\api\upload.py`
- [ ] T016 Implement API endpoint `GET /ingest/{task_id}` at `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\src\api\ingest.py`
- [ ] T017 Implement API endpoint `POST /chat` at `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\src\api\chat.py`

## Phase 3.4: Integration
- [ ] T018 Connect retriever to vector DB adapter at `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\src\chat\retriever.py`
- [ ] T019 Add cross-encoder reranker at `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\src\chat\reranker.py`
- [ ] T020 Observability hooks at `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\src\observability.py` (LangSmith traces)

## Phase 3.5: Polish
- [ ] T021 [P] Unit tests for models: `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\tests\unit\test_models.py`
- [ ] T022 Nightly evaluation skeleton: `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\backend\src\eval\nightly.py`
 - [x] T023 [P] Update `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\specs\001-title-local-first\quickstart.md` with exact run commands and env vars (updated migration step & DB note)

## Migration & Docs updates (recent)

- [x] Added DB columns `last_error` and `last_error_at` to `ingest_tasks` (migration SQL + runner added)
- [x] Added `backend/migrations/apply_migrations.py` (migration runner)
- [x] Added `backend/README.md` describing the DB schema & migration runner

## Dependencies & Ordering
- Setup tasks (T001-T003) before any test/implementation tasks
- Tests (T004-T007) MUST be added and failing before T008-T017 start (TDD)
- Models (T008-T009) before services and DB adapters (T010-T013)
- Worker (T012) depends on FS storage (T011) and embedding adapter (T013)

## Parallel Execution Examples
- Group A (safe to run in parallel): T004, T005, T006 (contract tests — different files)
	- Example agent commands (create files):
		```pwsh
		# create test_upload_post.py
		@'<test file content>'@ | Out-File -FilePath 'C:\...\test_upload_post.py' -Encoding utf8
		# create test_ingest_get.py
		@'<test file content>'@ | Out-File -FilePath 'C:\...\test_ingest_get.py' -Encoding utf8
		# create test_chat_post.py
		@'<test file content>'@ | Out-File -FilePath 'C:\...\test_chat_post.py' -Encoding utf8
		```

- Group B (models & storage can run in parallel): T008, T009, T011

## Validation Checklist (Before moving to implementation)
- [ ] All endpoints in `C:\Users\Tcyber\Documents\PROJECTS\LlamaInde-Chatbot\specs\001-title-local-first\contracts\openapi.yaml` have corresponding contract tests in `backend/tests/contract/`
- [ ] All entities in `data-model.md` have model files under `backend/src/models/`
- [ ] Tests fail (run `pytest`) before implementation begins
- [ ] Each task specifies exact file paths and owner (owner TBD)

## How an LLM agent should execute a single task (example: T004)
1. Create the test file at the absolute path using the provided skeleton.
2. Run `pytest backend/tests/contract/test_upload_post.py` locally (expects failure).
3. Report failure output and the test file path.

````
