import logging
import os
import time
from typing import Any, Dict

logger = logging.getLogger("llamainde")


def record_request(req_id: str, payload: Dict[str, Any]):
    logger.info("request %s %s", req_id, payload)


def record_response(req_id: str, resp: Dict[str, Any]):
    logger.info("response %s %s", req_id, resp)


# Observability config via env vars
# - ENABLE_OTLP: if set to '1', attempt to configure OTLP exporter
# - OTLP_ENDPOINT: endpoint for OTLP exporter (default: none)
# - ENABLE_LANGSMITH: if set to '1', attempt to configure LangSmith exporter
_ENABLE_OTLP = os.getenv("ENABLE_OTLP", "0") == "1"
_OTLP_ENDPOINT = os.getenv("OTLP_ENDPOINT")
_ENABLE_LANGSMITH = os.getenv("ENABLE_LANGSMITH", "0") == "1"


# Try to wire OpenTelemetry exporters if available; otherwise fallback tracer
_otel_available = False
try:
    from opentelemetry import trace as _trace
    from opentelemetry.sdk.trace import TracerProvider as _TracerProvider
    from opentelemetry.sdk.trace.export import (
        ConsoleSpanExporter as _ConsoleSpanExporter,
        SimpleSpanProcessor as _SimpleSpanProcessor,
    )

    # Optional OTLP exporter if requested
    try:
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
            OTLPSpanExporter as _OTLPSpanExporter,
        )
    except Exception:
        _OTLPSpanExporter = None

    _otel_available = True
except Exception:
    _otel_available = False


class Tracer:
    """Minimal tracer wrapper that uses OpenTelemetry when available.

    Usage:
        with default_tracer.start_span("ingest"):
            ...
    """

    if _otel_available:
        # Configure provider and processors
        _provider = _TracerProvider()

        # Console exporter for development / fallback
        _provider.add_span_processor(_SimpleSpanProcessor(_ConsoleSpanExporter()))

        # OTLP exporter when enabled and available
        if _ENABLE_OTLP and _OTLPSpanExporter is not None:
            try:
                if _OTLP_ENDPOINT:
                    otlp_exp = _OTLPSpanExporter(endpoint=_OTLP_ENDPOINT)
                else:
                    otlp_exp = _OTLPSpanExporter()
                _provider.add_span_processor(_SimpleSpanProcessor(otlp_exp))
                logger.info("OTLP exporter configured")
            except Exception as e:
                logger.warning("failed to configure OTLP exporter: %s", e)

        # LangSmith exporter stub: if requested, try to wire the LangSmith exporter
        if _ENABLE_LANGSMITH:
            try:
                # LangSmith exporter exists in opentelemetry-collector or via langsmith lib; attempt to import
                from langsmith.exporter import LangSmithSpanExporter as _LangSmithSpanExporter

                _provider.add_span_processor(_SimpleSpanProcessor(_LangSmithSpanExporter()))
                logger.info("LangSmith exporter configured")
            except Exception:
                logger.warning("LangSmith exporter requested but not available")

        _trace.set_tracer_provider(_provider)
        _impl = _trace.get_tracer(__name__)

        class _OtelSpan:
            def __init__(self, name: str):
                self._name = name
                self._span = Tracer._impl.start_as_current_span(name)

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                # OpenTelemetry context manager handles end
                return False

        def start_span(self, name: str):
            return Tracer._OtelSpan(name)

    else:
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
