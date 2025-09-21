from typing import List, Dict, Any, Optional

from ..embeddings import adapter as embed_adapter

_cross_encoder = None

try:
    # Optional dependency; if available, we'll use it for higher-quality reranking
    from sentence_transformers import CrossEncoder

    _cross_encoder = CrossEncoder
except Exception:
    _cross_encoder = None


def _dot(a: List[float], b: List[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def _cross_encoder_score(model, query: str, texts: List[str]) -> List[float]:
    # CrossEncoder returns a list of scores for each (query, doc) pair
    inputs = [[query, t] for t in texts]
    scores = model.predict(inputs)
    return [float(s) for s in scores]


def rerank(query: str, candidates: List[Dict[str, Any]], query_embedding: Optional[List[float]] = None) -> List[Dict[str, Any]]:
    """Rerank candidates. Prefer a CrossEncoder (if installed). Fall back to dot-product.

    Candidates are expected to have a `snippet` field and optional
    `metadata.embedding` if dot-product fallback is used.
    """
    # Try cross-encoder first
    if _cross_encoder is not None and candidates:
        try:
            # Lazy model load to avoid heavy startup cost during tests
            snippets = [c.get("snippet", "") for c in candidates]
            # Only use the cross-encoder when there is actual snippet text to score.
            if not any(s for s in snippets if s and s.strip()):
                raise RuntimeError("no snippets to score; skip cross-encoder")

            model = _cross_encoder("cross-encoder/stsb-roberta-large")
            scores = _cross_encoder_score(model, query, snippets)
            scored = []
            for c, s in zip(candidates, scores):
                nc = dict(c)
                nc["rerank_score"] = float(s)
                scored.append(nc)
            return sorted(scored, key=lambda x: x.get("rerank_score", 0.0), reverse=True)
        except Exception:
            # If the model cannot be loaded (no internet / missing weights), fall back
            pass

    # Fallback deterministic dot-product reranker
    if query_embedding is None:
        query_embedding = embed_adapter.embed_text(query)

    scored: List[Dict[str, Any]] = []
    for c in candidates:
        meta = c.get("metadata") or {}
        cand_emb = meta.get("embedding") if isinstance(meta.get("embedding"), list) else None
        if cand_emb:
            score = float(_dot(query_embedding, cand_emb))
        else:
            score = float(c.get("score", 0.0))
        newc = dict(c)
        newc["rerank_score"] = score
        scored.append(newc)

    return sorted(scored, key=lambda x: x.get("rerank_score", 0.0), reverse=True)
