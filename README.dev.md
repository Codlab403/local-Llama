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
