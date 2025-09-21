# Start the backend dev server (no reload by default to avoid child-process lifecycle issues)
# Usage: .\dev.ps1

cd .\backend
# Activate venv if you use one; otherwise runs with current python
# Start uvicorn (no reload). Press Ctrl+C to stop.
python -m uvicorn backend.src.api.main:app --host 127.0.0.1 --port 8000
