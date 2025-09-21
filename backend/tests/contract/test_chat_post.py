from fastapi.testclient import TestClient

from backend.src.api.main import app


def test_chat_post_returns_citations_and_confidence():
    client = TestClient(app)
    payload = {"session_id": "test-session", "query": "What is in sample?", "top_k": 3}
    r = client.post("/chat", json=payload)
    assert r.status_code == 200
    j = r.json()
    assert "citations" in j
    assert "confidence" in j
