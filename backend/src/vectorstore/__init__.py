"""In-memory vector store used for tests and local dev.

This is a tiny, deterministic store that keeps embeddings in memory and
supports a nearest-neighbors search using cosine similarity.
"""
from __future__ import annotations

from typing import List, Dict, Any, Tuple
import math
import json
from pathlib import Path
from threading import RLock



def _serialize_store(store: Dict[str, Tuple[List[float], Dict[str, Any]]]) -> Dict[str, Any]:
    return {k: {"embedding": v[0], "metadata": v[1]} for k, v in store.items()}


def _deserialize_store(data: Dict[str, Any]) -> Dict[str, Tuple[List[float], Dict[str, Any]]]:
    out: Dict[str, Tuple[List[float], Dict[str, Any]]] = {}
    for k, v in data.items():
        out[k] = (v.get("embedding", []), v.get("metadata", {}))
    return out


class InMemoryVectorStore:
    def __init__(self):
        # id -> (embedding, metadata)
        self._store: Dict[str, Tuple[List[float], Dict[str, Any]]] = {}
        self._persist_path = Path("data/vectorstore.json")
        self._lock = RLock()
        self._load()

    def _save(self) -> None:
        try:
            self._persist_path.parent.mkdir(parents=True, exist_ok=True)
            with self._persist_path.open("w", encoding="utf-8") as f:
                json.dump(_serialize_store(self._store), f, ensure_ascii=False, indent=2)
        except Exception:
            # best effort for tests/dev; don't crash the app on save errors
            pass

    def _load(self) -> None:
        try:
            if not self._persist_path.exists():
                return
            with self._persist_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            self._store = _deserialize_store(data)
        except Exception:
            # best effort; ignore malformed file
            self._store = {}

    def add(self, id: str, embedding: List[float], metadata: Dict[str, Any]) -> None:
        with self._lock:
            self._store[id] = (embedding, metadata)
            self._save()

    def _cosine(self, a: List[float], b: List[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(y * y for y in b))
        if na == 0 or nb == 0:
            return 0.0
        return dot / (na * nb)

    def query(self, embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        scored = []
        for id, (emb, meta) in self._store.items():
            score = self._cosine(embedding, emb)
            scored.append((score, id, meta))
        scored.sort(key=lambda x: x[0], reverse=True)
        results = []
        for score, id, meta in scored[:top_k]:
            # Include the stored embedding in the returned hit so callers
            # can use it for reranking without another round-trip to the store.
            emb = self._store.get(id, ([], {}))[0]
            item = {"id": id, "score": score, "metadata": meta, "embedding": emb}
            results.append(item)
        return results


_default_store: InMemoryVectorStore | None = None


def get_default_store() -> InMemoryVectorStore:
    global _default_store
    if _default_store is None:
        _default_store = InMemoryVectorStore()
    return _default_store

    
    def _serialize_store(store: Dict[str, Tuple[List[float], Dict[str, Any]]]) -> Dict[str, Any]:
        return {k: {"embedding": v[0], "metadata": v[1]} for k, v in store.items()}


    def _deserialize_store(data: Dict[str, Any]) -> Dict[str, Tuple[List[float], Dict[str, Any]]]:
        out: Dict[str, Tuple[List[float], Dict[str, Any]]] = {}
        for k, v in data.items():
            out[k] = (v.get("embedding", []), v.get("metadata", {}))
        return out

