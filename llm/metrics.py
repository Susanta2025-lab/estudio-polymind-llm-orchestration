import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Optional

from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram, generate_latest
from prometheus_client.exposition import CONTENT_TYPE_LATEST

from llm.inference import InferenceError, InferenceUsage, ModelRole, ReadinessResult


_LATENCY_BUCKETS = (0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10, 30, 60, 120)


class Metrics:
    """Bounded, process-local Prometheus instrumentation."""

    def __init__(self, registry: Optional[CollectorRegistry] = None):
        self.registry = registry or CollectorRegistry()
        inference_labels = ("provider", "logical_role", "served_model", "operation", "outcome")
        self.inference_requests = Counter(
            "inference_requests_total", "Completed inference operations.", inference_labels,
            registry=self.registry,
        )
        self.inference_duration = Histogram(
            "inference_request_duration_seconds", "End-to-end provider operation duration.",
            inference_labels, buckets=_LATENCY_BUCKETS, registry=self.registry,
        )
        stream_labels = ("provider", "logical_role", "served_model")
        self.inference_ttft = Histogram(
            "inference_time_to_first_token_seconds",
            "Time until the first non-empty generated streaming chunk.", stream_labels,
            buckets=_LATENCY_BUCKETS, registry=self.registry,
        )
        self.inference_stream_duration = Histogram(
            "inference_stream_duration_seconds", "Total provider stream lifetime.",
            (*stream_labels, "outcome"), buckets=_LATENCY_BUCKETS, registry=self.registry,
        )
        self.inference_errors = Counter(
            "inference_errors_total", "Normalized inference failures.",
            ("provider", "operation", "error_category"), registry=self.registry,
        )
        self.inference_tokens = Counter(
            "inference_tokens_total", "Provider-reported token usage.",
            ("provider", "logical_role", "served_model", "token_type"), registry=self.registry,
        )
        self.application_requests = Counter(
            "application_requests_total", "Completed semantic-route requests.",
            ("route", "operation", "outcome"), registry=self.registry,
        )
        self.application_duration = Histogram(
            "application_request_duration_seconds", "Semantic-route request duration.",
            ("route", "operation", "outcome"), buckets=_LATENCY_BUCKETS,
            registry=self.registry,
        )
        self.active_application_requests = Gauge(
            "active_application_requests",
            "Application requests whose orchestration or stream iterator is active.",
            ("operation",), registry=self.registry,
        )
        self.active_ndjson_streams = Gauge(
            "active_ndjson_streams",
            "NDJSON response iterators that are currently active.",
            registry=self.registry,
        )
        self.ndjson_stream_outcomes = Counter(
            "ndjson_stream_outcomes_total",
            "Completed, failed, or cancelled NDJSON response iterators.",
            ("outcome",), registry=self.registry,
        )
        self.readiness_checks = Counter(
            "readiness_checks_total", "Provider readiness outcomes.",
            ("provider", "outcome"), registry=self.registry,
        )
        self.readiness_duration = Histogram(
            "readiness_check_duration_seconds", "Provider readiness check duration.",
            ("provider", "outcome"), buckets=_LATENCY_BUCKETS, registry=self.registry,
        )
        self.memory_operations = Counter(
            "memory_operations_total", "Completed conversation-memory operations.",
            ("provider", "operation", "outcome"), registry=self.registry,
        )
        self.memory_duration = Histogram(
            "memory_operation_duration_seconds", "Conversation-memory operation duration.",
            ("provider", "operation", "outcome"), buckets=_LATENCY_BUCKETS, registry=self.registry,
        )
        self.memory_errors = Counter(
            "memory_errors_total", "Normalized conversation-memory failures.",
            ("provider", "operation", "error_category"), registry=self.registry,
        )
        self.memory_readiness = Counter(
            "memory_readiness_checks_total", "Conversation-memory readiness outcomes.",
            ("provider", "outcome"), registry=self.registry,
        )
        self.memory_readiness_duration = Histogram(
            "memory_readiness_check_duration_seconds", "Conversation-memory readiness duration.",
            ("provider", "outcome"), buckets=_LATENCY_BUCKETS, registry=self.registry,
        )
        self.vector_operations = Counter(
            "vector_operations_total", "Completed vector-store operations.",
            ("provider", "operation", "outcome"), registry=self.registry,
        )
        self.vector_duration = Histogram(
            "vector_operation_duration_seconds", "Vector-store operation duration.",
            ("provider", "operation", "outcome"), buckets=_LATENCY_BUCKETS, registry=self.registry,
        )
        self.vector_errors = Counter(
            "vector_errors_total", "Normalized vector-store failures.",
            ("provider", "operation", "error_category"), registry=self.registry,
        )
        self.vector_readiness = Counter(
            "vector_readiness_checks_total", "Vector-store readiness outcomes.",
            ("provider", "outcome"), registry=self.registry,
        )
        self.vector_readiness_duration = Histogram(
            "vector_readiness_duration_seconds", "Vector-store readiness duration.",
            ("provider", "outcome"), buckets=_LATENCY_BUCKETS, registry=self.registry,
        )
        self.component_readiness = Gauge(
            "component_readiness", "Current readiness of each required component.",
            ("component",), registry=self.registry,
        )
        self.bm25_build_duration = Histogram(
            "bm25_snapshot_build_duration_seconds", "BM25 startup snapshot build duration.",
            buckets=_LATENCY_BUCKETS, registry=self.registry,
        )
        self.bm25_refreshes = Counter(
            "bm25_snapshot_refresh_total", "Completed BM25 snapshot builds.",
            ("outcome",), registry=self.registry,
        )
        self.authentication_requests = Counter(
            "authentication_requests_total", "Authentication decisions for protected API endpoints.",
            ("endpoint_class", "outcome"), registry=self.registry,
        )
        self.request_rejections = Counter(
            "request_rejections_total", "Requests rejected at the application security boundary.",
            ("endpoint_class", "reason"), registry=self.registry,
        )

    def inference(self, provider: str, role: ModelRole, model: str, operation: str):
        return InferenceObservation(self, provider, role.value, model, operation)

    def observe_readiness(self, result: ReadinessResult, duration: float) -> None:
        labels = (result.provider, result.status.value)
        self.readiness_checks.labels(*labels).inc()
        self.readiness_duration.labels(*labels).observe(duration)

    def observe_application(self, route: str, operation: str, outcome: str, duration: float) -> None:
        safe_route = route if route in {"rag", "direct", "tool"} else "unknown"
        labels = (safe_route, operation, outcome)
        self.application_requests.labels(*labels).inc()
        self.application_duration.labels(*labels).observe(duration)

    @contextmanager
    def active_request(self, operation: str):
        safe_operation = operation if operation in {"query", "stream"} else "unknown"
        gauge = self.active_application_requests.labels(safe_operation)
        gauge.inc()
        try:
            yield
        finally:
            gauge.dec()

    @contextmanager
    def active_stream(self):
        self.active_ndjson_streams.inc()
        try:
            yield
        except GeneratorExit:
            self.ndjson_stream_outcomes.labels("cancelled").inc()
            raise
        except BaseException:
            self.ndjson_stream_outcomes.labels("error").inc()
            raise
        else:
            self.ndjson_stream_outcomes.labels("success").inc()
        finally:
            self.active_ndjson_streams.dec()

    def memory(self, provider: str, operation: str):
        return MemoryObservation(self, provider, operation)

    def observe_memory_readiness(self, result, duration: float) -> None:
        labels = (result.provider, result.status)
        self.memory_readiness.labels(*labels).inc()
        self.memory_readiness_duration.labels(*labels).observe(duration)

    def observe_vector(self, provider: str, operation: str, error, duration: float) -> None:
        outcome = "error" if error is not None else "success"
        self.vector_operations.labels(provider, operation, outcome).inc()
        self.vector_duration.labels(provider, operation, outcome).observe(duration)
        if error is not None:
            self.vector_errors.labels(provider, operation, error.category).inc()

    def observe_vector_readiness(self, provider: str, outcome: str, duration: float) -> None:
        self.vector_readiness.labels(provider, outcome).inc()
        self.vector_readiness_duration.labels(provider, outcome).observe(duration)

    def set_component_readiness(self, component: str, ready: bool) -> None:
        self.component_readiness.labels(component).set(1 if ready else 0)

    def observe_bm25_build(self, duration: float, successful: bool) -> None:
        self.bm25_build_duration.observe(duration)
        self.bm25_refreshes.labels("success" if successful else "error").inc()

    def observe_authentication(self, endpoint_class: str, outcome: str) -> None:
        self.authentication_requests.labels(endpoint_class, outcome).inc()

    def observe_request_rejection(self, endpoint_class: str, reason: str) -> None:
        self.request_rejections.labels(endpoint_class, reason).inc()

    def render(self) -> bytes:
        return generate_latest(self.registry)


@dataclass
class InferenceObservation:
    metrics: Metrics
    provider: str
    role: str
    model: str
    operation: str

    def __post_init__(self):
        self.started = time.perf_counter()
        self.ttft_recorded = False
        self.usage_recorded = False
        self.finished = False

    def observe_content(self, content: str) -> None:
        if self.operation == "stream" and content and not self.ttft_recorded:
            self.metrics.inference_ttft.labels(self.provider, self.role, self.model).observe(
                time.perf_counter() - self.started
            )
            self.ttft_recorded = True

    def observe_usage(self, usage: Optional[InferenceUsage]) -> None:
        if usage is None or self.usage_recorded:
            return
        self.usage_recorded = True
        for token_type, value in usage.values():
            if value is not None:
                self.metrics.inference_tokens.labels(
                    self.provider, self.role, self.model, token_type
                ).inc(value)

    def finish(self, error: Optional[BaseException] = None) -> float:
        if self.finished:
            return time.perf_counter() - self.started
        self.finished = True
        duration = time.perf_counter() - self.started
        outcome = "error" if error is not None else "success"
        labels = (self.provider, self.role, self.model, self.operation, outcome)
        self.metrics.inference_requests.labels(*labels).inc()
        self.metrics.inference_duration.labels(*labels).observe(duration)
        if self.operation == "stream":
            self.metrics.inference_stream_duration.labels(
                self.provider, self.role, self.model, outcome
            ).observe(duration)
        if isinstance(error, InferenceError):
            self.metrics.inference_errors.labels(
                self.provider, self.operation, error.category
            ).inc()
        return duration


@dataclass
class MemoryObservation:
    metrics: Metrics
    provider: str
    operation: str

    def __enter__(self):
        self.started = time.perf_counter()
        return self

    def __exit__(self, error_type, error, traceback):
        duration = time.perf_counter() - self.started
        outcome = "error" if error is not None else "success"
        labels = (self.provider, self.operation, outcome)
        self.metrics.memory_operations.labels(*labels).inc()
        self.metrics.memory_duration.labels(*labels).observe(duration)
        if error is not None:
            category = getattr(error, "category", "memory_failure")
            self.metrics.memory_errors.labels(self.provider, self.operation, category).inc()
        return False


metrics = Metrics()

__all__ = ["CONTENT_TYPE_LATEST", "Metrics", "metrics"]
