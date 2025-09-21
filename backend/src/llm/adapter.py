from typing import Iterable, Dict, Any, List, Generator, Optional
import os
import logging

logger = logging.getLogger(__name__)


def synthesize(prompt: str, backend: Optional[str] = None) -> Dict[str, Any]:
    """Synthesize a final answer for the given prompt. Returns dict with 'text'.

    Default backend is 'test' which returns a deterministic string. An
    'ollama' backend can be added later; it should stream tokens instead.
    """
    if backend is None:
        backend = os.environ.get("LLM_BACKEND", "test")

    if backend == "ollama":
        # Stub: Ollama network calls omitted in tests
        logger.debug("Ollama requested but not available in test environment")
        backend = "test"

    # test backend: echo the prompt summary
    return {"text": f"Answer (test): summary of '{prompt[:80]}'"}


def stream_synthesize(prompt: str, backend: Optional[str] = None) -> Generator[str, None, None]:
    """Yield tokens deterministically for test backend."""
    final = synthesize(prompt, backend=backend)["text"]
    # naive tokenization by spaces
    for tok in final.split():
        yield tok
