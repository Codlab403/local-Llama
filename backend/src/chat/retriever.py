from typing import List, Dict, Any

from ..vectorstore import get_default_store
from ..embeddings import adapter


def _deterministic_embedding(text: str) -> List[float]:
    # Use the same embedding function as the ingestion pipeline so queries and
    # documents are embedded consistently during tests.
    return adapter.embed_text(text)


def retrieve(query: str, top_k: int = 5, filters: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
    """Retrieve top-k candidate nodes from the in-memory vector store.

    Each result has node_id, doc_id, page, snippet, and score.
    """
    store = get_default_store()
    emb = _deterministic_embedding(query)
    hits = store.query(emb, top_k=top_k)
    return [
        {
            "node_id": h["id"],
            "doc_id": h["metadata"].get("doc_id"),
            "page": h["metadata"].get("page"),
            "snippet": h["metadata"].get("snippet"),
            "score": h["score"],
            "metadata": {**h.get("metadata", {}), "embedding": h.get("embedding")},
        }
        for h in hits
    ]

