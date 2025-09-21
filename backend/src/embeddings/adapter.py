from typing import List, Optional
import os
import hashlib
import logging

logger = logging.getLogger(__name__)


def _deterministic_embed(text: str, dim: int = 8) -> List[float]:
    # simple deterministic embedding: use SHA256 and split into floats
    h = hashlib.sha256(text.encode("utf-8")).digest()
    vals = []
    for i in range(dim):
        vals.append(float(h[i] % 100) / 100.0)
    return vals


def embed_text(text: str, backend: Optional[str] = None) -> List[float]:
    """Return an embedding vector for `text`.

    backend: 'test' (default) or 'ollama' (stub). If 'ollama' is requested but
    not configured, falls back to deterministic test embeddings.
    """
    if backend is None:
        backend = os.environ.get("EMBEDDING_BACKEND", "test")

    if backend == "ollama":
        # Stubbed: if OLLAMA_URL is configured we would call it. For now, log
        # and fall back to deterministic embeddings to keep tests hermetic.
        url = os.environ.get("OLLAMA_URL")
        if not url:
            logger.debug("OLLAMA_URL not set; falling back to test embeddings")
            return _deterministic_embed(text)
        # Network calls are intentionally omitted in tests; fallback instead.
        logger.debug("OLLAMA backend requested but network calls disabled in tests")
        return _deterministic_embed(text)

    # default
    return _deterministic_embed(text)


def persist(embedding: List[float], node_id: str) -> None:
    """Placeholder persist hook. Kept for API compatibility.

    In the future this can write to a dedicated vector DB directly.
    """
    return None
