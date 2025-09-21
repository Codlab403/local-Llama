# AGENTS.md

A specification file to guide coding agents (or AI assistants) working on the Local RAG Chatbot project.

---

## Project Overview

- **Name**: Local Document / Knowledge‑Base Chatbot  
- **Purpose**: Users upload documents, ask questions via conversational AI, get answers with citations; manage sessions & documents via sidebar UI.  
- **Stack**:
  - Frontend: Next.js + Tailwind CSS + shadcn/ui  
  - Backend: Python + FastAPI  
  - Ingestion / Retrieval: LlamaIndex  
  - Tool orchestration: LangChain (+ LangSmith observability)  
  - Vector Store: Chroma (for local dev) / Milvus or Weaviate (for scale)  
  - LLM: Ollama (local) by default; optional hosted LLMs as needed

---

## Setup Commands (using uv)

`uv` is used for creating and managing Python virtual environments, dependency installation, version locking, and running Python commands.

### Install `uv`

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Alternatively via pipx or pip
pip install uv
```

### Initialize project environment (backend)

```bash
cd backend

# Initialize uv project (creates pyproject.toml and .venv)
uv init

# Or if migrating from an existing requirements.txt
uv init
uv pip sync requirements.txt
```

### Create / activate virtual environment

```bash
# To explicitly create a venv (if needed)
uv venv --python 3.11

# Activate it (classic way)
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate         # Windows

# Alternatively, use uv run for commands without manual activation
uv run python -m app.main
```

### Install dependencies

```bash
# Add production dependencies (updates project metadata)
uv add fastapi llama-index uv-tooling <other-deps>

# Add dev dependencies
uv add --dev pytest black ruff

# Or install from lock / requirements
uv pip sync requirements.txt
```

### Locking dependencies

```bash
# Generate lock file
uv lock

# Or ensure dependencies are locked when using `uv add`
```

### Running the backend

```bash
cd backend

# Use uv run to ensure .venv is used
uv run uv pip install -r requirements.txt
uv run uv run python -m app.main:app --reload # or appropriate uv run command
```

### Running tests

```bash
cd backend
uv run pytest
```

---

## API & Data Contracts

(As before; interfaces and endpoints remain same; agents should follow contract specs in the PRD.)

### Endpoints

| Method | Path                         | Description                                  |
|--------|-----------------------------|----------------------------------------------|
| GET    | `/api/v1/sessions`          | List all sessions                            |
| POST   | `/api/v1/sessions`          | Create a new session                         |
| GET    | `/api/v1/history/:sessionId`| Get messages in that session                 |
| DELETE | `/api/v1/sessions/:id`      | Delete a session                             |
| PATCH  | `/api/v1/sessions/:id`      | Rename or update session metadata            |
| POST   | `/api/v1/upload`            | Upload document                              |
| GET    | `/api/v1/documents`         | List documents                               |
| DELETE | `/api/v1/documents/:id`     | Delete document                              |
| POST   | `/api/v1/chat`              | Send user query → streaming assistant answer + citations |
| POST   | `/api/v1/regenerate`        | Retry/refine assistant response              |

### Data Models

```ts
interface Session {
  id: string;
  title: string;
  createdAt: string;
  lastUpdated: string;
  userId: string;
  ephemeral: boolean;
}

interface Document {
  id: string;
  filename: string;
  status: 'queued' | 'uploading' | 'parsing' | 'indexing' | 'ready' | 'error';
  uploadedAt: string;
  pages?: number;
  sizeKB?: number;
  version: number;
  tags?: string[];
  acl?: string[];
}

interface Message {
  id: string;
  sessionId: string;
  role: 'user' | 'assistant';
  content: string;
  createdAt: string;
  citations?: Array<{
    docId: string;
    page: number;
    snippet: string;
    nodeId: string;
    status: 'available' | 'removed';
  }>;
  cachedSnippets?: {
    [docId: string]: string;
  };
}
```

---

## Code Style & Conventions

- **Backend** (Python):
  - Use uv for all dependency management; `uv add` / `uv sync` etc.
  - Utilize Pydantic models for request/response schemas.
  - Organize code modularly: ingestion, retrieval, API, orchestration (LangChain).
  - Type hints everywhere; linting with `ruff`, formatting with `black`.
- **Frontend**:
  - TypeScript strict mode.
  - React functional components & hooks.
  - Tailwind CSS with utility classes, consistent spacing & theming.
  - Use shadcn/ui component primitives for Buttons, Dialogs, Tabs, etc.
  - Avoid large bundle dependencies; lazy‑load DocumentViewer / PDF rendering.

- **General**:
  - Use consistent naming (snake_case on backend, camelCase in frontend).
  - Commit messages prefixed with subsystem e.g. `[frontend]`, `[backend]`, `[ingest]`, `[UI]`.

---

## UI Layout & Behavior (Sidebar Version)

Agents should know how the UI is structured so changes align.

- Left Sidebar: contains a list of sessions (chat history) and documents. Sessions at top; documents below. Sidebar visible on desktop, collapsible / slide‑over on mobile.
- Center area: main chat interface: message list + input bar fixed bottom.
- Right Drawer: DocumentViewer opens upon clicking a citation or sidebar document.
- UI supports upload, streaming, delete with undo, snippet caching, citation chips.

---

## Testing & QA

- Unit tests for core components & backend routines.
- Integration tests for flows: upload → index → chat → citation → viewer.
- E2E tests using Playwright/Cypress for full UX (mobile & desktop).
- Tests for offline mode and sync behavior.
- Nightly evaluative tests: Recall@k, citation accuracy, hallucination flags using gold Q/A set.

---

## Observability & Telemetry

- Use LangChain + LangSmith to trace:
  - retrieval candidates, reranker scores
  - prompt used
  - LLM latency and token counts
  - errors & fallback paths

- Backend logging:
  - ingestion pipeline status
  - API call timings, failures
  - usage of special tools (DuckDB, KG)

- Frontend metrics:
  - latency from user “send” to first token
  - time to index docs
  - error rates in upload/document viewing

---

## Agents Task Guidance

When asked to build/modify features, follow these guidelines:

- **Feature requests** should be implemented end‑to‑end: UI + API + backend + indexing logic + tests.
- For UI behavior, mirror the design in the layout spec: sidebar sessions & documents, DocumentViewer, streaming responses.
- When adding new endpoints or data models, update frontend and backend contracts, and include Pydantic/Typescript types.
- Always include citations support: snippet + page + docId + status (removed or available).
- For components affected by deletions (docs or sessions), include undo logic and UI feedback.

---

## Build & Deployment

- Dev: run frontend and backend locally; vector store local or hosted dev instance.
- For production or hosted LLMs: configure environment variables for LLM endpoint, API keys.
- If using Milvus or Weaviate, include start‑up scripts or Docker Compose definitions.
- Persist storage directories, vector DB data, metadata DB; version control frontend; backup raw documents.

---

## Security & Privacy Notes

- Docs and user data are sensitive: operations must default local; no external data leaks.
- If hosted LLMs are enabled, ensure data policies are clear, optional.
- ACL metadata must be enforced in retrieval (backend).
- Document deletion must not expose removed content; cached snippet only visible in historical context with “removed” status.

---

## Contribution & PR Guidelines

- Branch naming: `feature/<short‑desc>` or `fix/<short‑desc>`
- Before merging:
  1. Run lint / formatting checks (prettier / eslint / black / flake8)
  2. Run tests (unit & integration)
  3. Verify UI behavior matches design spec (screenshots or storybook if available)
  4. If new API changes: update API docs (OpenAPI / Swagger) + update frontend types
  5. Ensure commit history is clean

---

## Where to Find More Context

- README.md for high-level usage and setup  
- UI design tokens and Figma file for look & feel  
- Backend architecture docs for ingestion / indexing / query pipelines  
- Evaluation plan & gold Q/A set in `qa/` folder  

---

## Why AGENTS.md Exists

This file is the single source of truth for coding agents (AI or human) to understand the project’s architecture, coding conventions, UI layout, and integration points. It complements README and detailed design docs by gathering instructions in one structured place.

---
