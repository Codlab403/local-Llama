import backend.src.chat.cross_encoder_adapter as cea


def test_cross_encoder_cache(monkeypatch):
    # Simulate presence of a CrossEncoder class by monkeypatching the module-level ref
    class Dummy:
        def __init__(self, name):
            self.name = name

    monkeypatch.setattr(cea, "_CrossEncoder", Dummy)

    # Clear any pre-existing cache
    cea.clear_cache()

    m1 = cea.get_model("model-a")
    m2 = cea.get_model("model-a")
    assert m1 is m2

    m3 = cea.get_model("model-b")
    assert m3 is not m1

    cea.clear_cache()
    m4 = cea.get_model("model-a")
    assert m4 is not m1
