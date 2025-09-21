import importlib
import os
import sys
import types


def reload_observability():
    # Ensure fresh import
    if "backend.src.observability" in sys.modules:
        del sys.modules["backend.src.observability"]
    return importlib.import_module("backend.src.observability")


def test_fallback_tracer_no_otel(monkeypatch):
    # Ensure opentelemetry not present
    monkeypatch.delenv("ENABLE_OTLP", raising=False)
    monkeypatch.delenv("ENABLE_LANGSMITH", raising=False)
    for key in list(sys.modules):
        if key.startswith("opentelemetry") or key.startswith("langsmith"):
            sys.modules.pop(key, None)

    obs = reload_observability()

    # Basic API should be present and usable as context manager
    with obs.default_tracer.start_span("test-span"):
        obs.record_request("r1", {"k": "v"})
        obs.record_response("r1", {"ok": True})


def make_fake_opentelemetry():
    # Build minimal fake opentelemetry package structure required by observability.py
    pkg = types.ModuleType("opentelemetry")
    trace = types.SimpleNamespace()

    class FakeTracer:
        def start_as_current_span(self, name):
            class Ctx:
                def __enter__(self):
                    return None

                def __exit__(self, exc_type, exc, tb):
                    return False

            return Ctx()

        def get_tracer(self, _name):
            return FakeTracer()

    trace.get_tracer = lambda name: FakeTracer()
    trace.set_tracer_provider = lambda _p: None

    sdk = types.ModuleType("opentelemetry.sdk")
    sdk.trace = types.SimpleNamespace()

    class TracerProvider:
        def add_span_processor(self, _p):
            return None

    sdk.trace.TracerProvider = TracerProvider

    sdk_trace_export = types.ModuleType("opentelemetry.sdk.trace.export")

    class ConsoleSpanExporter:
        pass

    class SimpleSpanProcessor:
        def __init__(self, _e):
            pass

    sdk_trace_export.ConsoleSpanExporter = ConsoleSpanExporter
    sdk_trace_export.SimpleSpanProcessor = SimpleSpanProcessor

    # OTLP exporter
    otlp = types.ModuleType(
        "opentelemetry.exporter.otlp.proto.grpc.trace_exporter"
    )

    class OTLPSpanExporter:
        def __init__(self, endpoint=None):
            self.endpoint = endpoint

    otlp.OTLPSpanExporter = OTLPSpanExporter

    # Attach into modules
    pkg.trace = trace
    sys.modules["opentelemetry"] = pkg
    sys.modules["opentelemetry.trace"] = pkg.trace
    sys.modules["opentelemetry.sdk"] = sdk
    sys.modules["opentelemetry.sdk.trace"] = sdk.trace
    sys.modules["opentelemetry.sdk.trace.export"] = sdk_trace_export
    sys.modules[
        "opentelemetry.exporter.otlp.proto.grpc.trace_exporter"
    ] = otlp


def make_fake_langsmith():
    exporter_mod = types.ModuleType("langsmith.exporter")

    class LangSmithSpanExporter:
        def __init__(self, *a, **k):
            pass

    exporter_mod.LangSmithSpanExporter = LangSmithSpanExporter
    sys.modules["langsmith"] = types.ModuleType("langsmith")
    sys.modules["langsmith.exporter"] = exporter_mod


def test_enable_otlp_and_langsmith_env(monkeypatch):
    # Inject fake opentelemetry and langsmith
    make_fake_opentelemetry()
    make_fake_langsmith()

    monkeypatch.setenv("ENABLE_OTLP", "1")
    monkeypatch.setenv("OTLP_ENDPOINT", "http://localhost:4317")
    monkeypatch.setenv("ENABLE_LANGSMITH", "1")

    obs = reload_observability()

    # Should configure without raising and provide tracer
    with obs.default_tracer.start_span("span-otlp"):
        obs.record_request("r2", {"x": 1})
        obs.record_response("r2", {"ok": True})
from backend.src import observability


def test_observability_api_surface():
    # record_request/record_response should be callable
    observability.record_request("r1", {"foo": "bar"})
    observability.record_response("r1", {"ok": True})

    # default_tracer should provide start_span context manager
    with observability.default_tracer.start_span("test-span"):
        pass
