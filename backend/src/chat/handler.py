"""LangChain orchestration skeleton for Local-first RAG (T014a).

This file provides a minimal, testable orchestration entrypoint. It is
implementation-light and intended to be expanded with real LangChain chains
and components during T014/T018/T019 implementation.
"""
from typing import List, Dict, Any

from . import retriever, reranker
from ..llm import adapter as llm_adapter
from ..embeddings import adapter as embed_adapter


def _simple_rerank(candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Backwards-compatible simple sorter used as fallback
    return sorted(candidates, key=lambda x: x.get("score", 0.0), reverse=True)


def _synthesize_answer(query: str, citations: List[Dict[str, Any]]) -> str:
    # Build a simple prompt from citations and delegate to LLM adapter
    if not citations:
        return "I couldn't find anything relevant."
    prompt_parts = [c.get("snippet", "") for c in citations]
    prompt = f"User query: {query}\nCitations:\n" + "\n".join(prompt_parts)
    resp = llm_adapter.synthesize(prompt)
    return resp.get("text", "")


def stream_answer(query: str, citations: List[Dict[str, Any]]):
    prompt_parts = [c.get("snippet", "") for c in citations]
    prompt = f"User query: {query}\nCitations:\n" + "\n".join(prompt_parts)
    for tok in llm_adapter.stream_synthesize(prompt):
        yield tok


def orchestrate_query(session_id: str, query: str, top_k: int = 5, filters: Dict[str, Any] | None = None) -> Dict[str, Any]:
    # 1) Retrieve
    candidates = retriever.retrieve(query, top_k=top_k, filters=filters)

    # 2) Rerank using the cross-encoder-like reranker if available
    try:
        q_emb = embed_adapter.embed_text(query)
        reranked = reranker.rerank(query, candidates, query_embedding=q_emb)[:top_k]
    except Exception:
        # If anything goes wrong, fall back to a simple sort
        reranked = _simple_rerank(candidates)[:top_k]

    # 3) Synthesize answer
    answer = _synthesize_answer(query, reranked)

    # 4) Confidence heuristic
    confidence = float(sum(c.get("score", 0.0) for c in reranked) / (len(reranked) or 1))

    return {"answer": answer, "citations": reranked, "confidence": confidence}
