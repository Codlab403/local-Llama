from backend.src.chat import reranker
from backend.src.embeddings import adapter as embed_adapter


def test_reranker_orders_by_embedding_dot():
    query = "find alpha"
    q_emb = embed_adapter.embed_text(query)

    # Create two candidates: one aligned with query, one not
    # We'll manufacture embeddings so dot-product ranks node-a higher
    cand_a = {"node_id": "a", "metadata": {"embedding": q_emb}, "score": 0.1}
    # Reverse the embedding to get a lower dot
    cand_b = {"node_id": "b", "metadata": {"embedding": [-x for x in q_emb]}, "score": 0.2}

    reranked = reranker.rerank(query, [cand_b, cand_a], query_embedding=q_emb)
    assert reranked[0]["node_id"] == "a"
    assert reranked[1]["node_id"] == "b"
