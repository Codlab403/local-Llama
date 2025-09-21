import time
from fastapi.testclient import TestClient


def test_ingest_pipeline():
    from backend.src.api import main as api_main

    client = TestClient(api_main.app)

    files = {"file": ("sample.txt", b"hello from integration test")}
    r = client.post("/upload", files=files)
    assert r.status_code == 200
    data = r.json()
    assert "task_id" in data
    task_id = data["task_id"]

    # poll until ready or error
    timeout = 10
    start = time.time()
    status = None
    while time.time() - start < timeout:
        r2 = client.get(f"/ingest/{task_id}")
        assert r2.status_code == 200
        payload = r2.json()
        status = payload.get("status")
        if status in ("ready", "error"):
            break
        time.sleep(0.2)

    assert status == "ready", f"ingest did not reach ready (final={status})"
import time
from fastapi.testclient import TestClient
from backend.src.api.main import app


def test_ingest_pipeline_completed():
    client = TestClient(app)
    files = {"file": ("sample_pipeline.txt", b"one\ntwo\nthree")}
    r = client.post("/upload", files=files)
    assert r.status_code == 200
    task_id = r.json().get("task_id")
    assert task_id

    # poll until ready or timeout (5s for tests)
    end = time.time() + 5
    status = None
    while time.time() < end:
        r2 = client.get(f"/ingest/{task_id}")
        assert r2.status_code in (200, 404)
        if r2.status_code == 200:
            status = r2.json().get("status")
            if status in ("ready", "error"):
                break
        time.sleep(0.2)

    assert status == "ready"
