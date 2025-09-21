from backend.src.chat import handler


def test_stream_answer_yields_tokens():
    citations = [{"doc_id": "d1", "page": 1, "snippet": "alpha snippet"}]
    toks = list(handler.stream_answer("what is alpha", citations))
    assert len(toks) > 0
    joined = " ".join(toks)
    assert "Answer (test):" in joined or "alpha" in joined
