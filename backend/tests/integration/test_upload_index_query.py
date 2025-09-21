from fastapi.testclient import TestClient
from backend.src.api.main import app
from backend.src.vectorstore import get_default_store
import os


def test_upload_indexes_and_query():
    client = TestClient(app)
    sample_text = "Line one\nLine two\nLine three with unique-token-abc123"
    files = {"file": ("sample_upload.txt", sample_text.encode("utf-8"))}
    r = client.post("/upload", files=files)
    assert r.status_code == 200
    j = r.json()
    assert "task_id" in j
    task_id = j["task_id"]

    # After upload, worker runs synchronously and should have indexed nodes into vectorstore
    store = get_default_store()
    # Ensure at least one node exists whose metadata.doc_id == task_id
    hits = [m for _, (emb, m) in store._store.items() if m.get("doc_id") == task_id]
    assert len(hits) > 0

    # Query via chat and expect citations that reference doc_id
    payload = {"session_id": "s1", "query": "unique-token-abc123", "top_k": 3}
    r2 = client.post("/chat", json=payload)
    assert r2.status_code == 200
    res = r2.json()
    assert "citations" in res
    assert any(c.get("doc_id") == task_id for c in res["citations"]) 
