from typing import List, Dict, Any, Optional

from ..embeddings import adapter as embed_adapter


def _dot(a: List[float], b: List[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def rerank(query: str, candidates: List[Dict[str, Any]], query_embedding: Optional[List[float]] = None) -> List[Dict[str, Any]]:
    """Deterministic reranker for tests.

    Computes a simple cross-encoder-like score by taking the dot-product
    between the query embedding and each candidate's embedding found in
    candidate["metadata"]["embedding"]. If candidate embeddings are not
    present, falls back to scoring by the retriever-provided `score`.

    This keeps the implementation hermetic and deterministic for unit
    tests while mimicking a re-ranking step.
    """
    if query_embedding is None:
        query_embedding = embed_adapter.embed_text(query)

    scored: List[Dict[str, Any]] = []
    for c in candidates:
        # candidate may include an embedding in metadata or not
        cand_emb = None
        meta = c.get("metadata") or {}
        if isinstance(meta.get("embedding"), list):
            cand_emb = meta.get("embedding")

        if cand_emb:
            score = float(_dot(query_embedding, cand_emb))
        else:
            # Fallback: use retriever score (already in candidate)
            score = float(c.get("score", 0.0))

        newc = dict(c)
        newc["rerank_score"] = score
        scored.append(newc)

    return sorted(scored, key=lambda x: x.get("rerank_score", 0.0), reverse=True)
