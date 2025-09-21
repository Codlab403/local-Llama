from fastapi.testclient import TestClient

from backend.src.api.main import app


def test_upload_returns_task_id():
    client = TestClient(app)
    files = {"file": ("sample.txt", b"hello world")}
    r = client.post("/upload", files=files)
    assert r.status_code == 200
    j = r.json()
    assert "task_id" in j
