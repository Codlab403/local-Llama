from backend.src.chat import handler
from backend.src.vectorstore import get_default_store


def setup_store_with_docs():
    store = get_default_store()
    # Clear any existing store (re-create)
    store._store.clear()
    # Add a few deterministic docs
    store.add("node-1", [10.0, 0.1], {"doc_id": "doc-1", "page": 1, "snippet": "Alpha content"})
    store.add("node-2", [20.0, 0.2], {"doc_id": "doc-2", "page": 2, "snippet": "Beta content"})
    store.add("node-3", [30.0, 0.3], {"doc_id": "doc-3", "page": 3, "snippet": "Gamma content"})


def test_orchestrate_query_returns_citations_and_confidence():
    setup_store_with_docs()
    res = handler.orchestrate_query("s1", "sample query", top_k=2)
    assert "answer" in res
    assert "citations" in res
    assert isinstance(res["citations"], list)
    assert len(res["citations"]) <= 2
    assert "confidence" in res
    assert isinstance(res["confidence"], float)
