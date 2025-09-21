from typing import Optional, Dict
from .. import config


# Optional class reference
_CrossEncoder = None

try:
    # optional dependency
    from sentence_transformers import CrossEncoder as _CE

    _CrossEncoder = _CE
except Exception:
    _CrossEncoder = None


# Simple cache for loaded models to avoid re-downloading / re-instantiation
_MODEL_CACHE: Dict[str, object] = {}


def get_cross_encoder_class():
    """Return the CrossEncoder class if available, otherwise None.

    Keep this in a tiny adapter so unit tests can monkeypatch it easily.
    """
    return _CrossEncoder


def get_model(model_name: Optional[str] = None):
    """Return a cached model instance for `model_name` (or default).

    If sentence-transformers is not installed, returns None.
    """
    if _CrossEncoder is None:
        return None

    model_name = model_name or config.get_cross_encoder_model()
    if model_name in _MODEL_CACHE:
        return _MODEL_CACHE[model_name]

    model = _CrossEncoder(model_name)
    _MODEL_CACHE[model_name] = model
    return model


def clear_cache():
    """Clear the model cache (useful for tests)."""
    _MODEL_CACHE.clear()
