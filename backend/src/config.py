import os


def use_cross_encoder() -> bool:
    v = os.getenv("USE_CROSS_ENCODER", "0")
    return v.lower() in ("1", "true", "yes")
