from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "deployment" / "monitoring" / "prometheus-rules.yaml"
RULE_TESTS = ROOT / "deployment" / "monitoring" / "prometheus-rules.test.yaml"


def _rules():
    document = yaml.safe_load(RULES.read_text())
    return [rule for group in document["groups"] for rule in group["rules"]]


def test_recording_rules_use_restart_safe_and_histogram_correct_promql():
    rules = _rules()
    records = {rule["record"]: rule["expr"] for rule in rules if "record" in rule}

    assert "rate(application_requests_total[5m])" in records[
        "polymind:application_requests:rate5m"
    ]
    assert "histogram_quantile(0.95" in records[
        "polymind:application_request_duration_seconds:p95_rate5m"
    ]
    assert "sum by (namespace, operation, le)" in records[
        "polymind:application_request_duration_seconds:p95_rate5m"
    ]
    assert "sum by (namespace, provider, logical_role, le)" in records[
        "polymind:inference_ttft_seconds:p95_rate5m"
    ]
    assert "sum by (namespace, pod)" in records[
        "polymind:active_query_requests:sum_by_pod"
    ]


def test_recording_and_alert_rules_keep_dimensions_bounded():
    serialized = RULES.read_text().lower()
    forbidden = (
        "request_id", "session_id", "prompt", "document_id", "redis_key",
        "exception_message", "bearer", "authorization",
    )
    assert not any(label in serialized for label in forbidden)
    assert "custom.metrics.k8s.io" not in serialized
    assert "kind: horizontalpodautoscaler" not in serialized
    assert all("for" in rule for rule in _rules() if "alert" in rule)


def test_prometheus_fixture_covers_rate_histogram_and_active_query_contract():
    fixture = yaml.safe_load(RULE_TESTS.read_text())
    expressions = {
        case["expr"] for test in fixture["tests"] for case in test["promql_expr_test"]
    }
    assert expressions == {
        "polymind:application_requests:rate5m",
        "polymind:application_request_duration_seconds:p95_rate5m",
        "polymind:active_query_requests:sum_by_pod",
    }
