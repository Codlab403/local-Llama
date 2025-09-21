import logging
import time
from typing import Any, Dict


logger = logging.getLogger("llamainde")


def record_request(req_id: str, payload: Dict[str, Any]):
    logger.info("request %s %s", req_id, payload)


def record_response(req_id: str, resp: Dict[str, Any]):
    logger.info("response %s %s", req_id, resp)


class Tracer:
    """Minimal tracer stub — replace with LangSmith or another tracer.

    Use as:
        with default_tracer.start_span("ingest"):
            ...
    """

    class _Span:
        def __init__(self, name: str):
            self.name = name
            self.start = time.time()
            logger.debug("span start %s", name)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            duration = time.time() - self.start
            logger.debug("span end %s duration=%s", self.name, duration)

    def start_span(self, name: str):
        return Tracer._Span(name)


default_tracer = Tracer()
