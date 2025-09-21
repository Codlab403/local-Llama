from backend.src.chat import reranker


class FakeModel:
    def __init__(self, scores):
        self._scores = scores

    def predict(self, inputs):
        # ignore inputs structure; just return configured scores
        return self._scores


def test_reranker_uses_cross_encoder(monkeypatch, tmp_path, monkeypatching=None):
    # Enable the env toggle
    monkeypatch.setenv("USE_CROSS_ENCODER", "1")

    # Create two candidates with snippets; cross-encoder will score b higher
    cand_a = {"node_id": "a", "snippet": "apple pie"}
    cand_b = {"node_id": "b", "snippet": "banana split"}

    # Fake scores: [0.1, 0.9] -> b should be first
    fake = FakeModel([0.1, 0.9])

    # Monkeypatch adapter to return FakeModel class
    def fake_get_model(name=None):
        return fake

    # Patch the cross_encoder_adapter.get_model to return our fake model
    import backend.src.chat.cross_encoder_adapter as cea

    monkeypatch.setattr(cea, "get_model", fake_get_model)

    reranked = reranker.rerank("query", [cand_a, cand_b])
    assert reranked[0]["node_id"] == "b"
