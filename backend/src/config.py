import os


def use_cross_encoder() -> bool:
    v = os.getenv("USE_CROSS_ENCODER", "0")
    return v.lower() in ("1", "true", "yes")


def get_cross_encoder_model() -> str:
    """Return the CrossEncoder model name to use (from env).

    Default: cross-encoder/stsb-roberta-large
    """
    return os.getenv("CROSS_ENCODER_MODEL", "cross-encoder/stsb-roberta-large")
