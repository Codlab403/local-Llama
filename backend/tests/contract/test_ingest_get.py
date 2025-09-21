from fastapi.testclient import TestClient

from backend.src.api.main import app


def test_ingest_get_status_values():
    client = TestClient(app)
    # Placeholder task id; local test should replace with a real id from upload
    task_id = "00000000-0000-0000-0000-000000000000"
    r = client.get(f"/ingest/{task_id}")
    # API should return a status field even if task not found
    assert r.status_code in (200, 404)
    if r.status_code == 200:
        j = r.json()
        assert j.get("status") in ("queued", "indexing", "ready", "error")


def test_ingest_status_not_found():
    client = TestClient(app)
    r = client.get("/ingest/does-not-exist")
    assert r.status_code == 404
