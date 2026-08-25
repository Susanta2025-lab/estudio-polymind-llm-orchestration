from pathlib import Path
import shutil
import subprocess

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[2]
CHART = ROOT / "deployment" / "helm" / "polymind"
PHASE10 = ROOT / "deployment" / "kind" / "phase10"


def test_chart_contains_required_artifacts_and_safe_defaults():
    expected = {
        "Chart.yaml",
        "values.yaml",
        "README.md",
        "templates/_helpers.tpl",
        "templates/configmap.yaml",
        "templates/deployment.yaml",
        "templates/ingress.yaml",
        "templates/networkpolicy.yaml",
        "templates/secret.yaml",
        "templates/service.yaml",
        "templates/serviceaccount.yaml",
        "templates/servicemonitor.yaml",
        "templates/hpa.yaml",
    }
    assert expected <= {
        str(path.relative_to(CHART)) for path in CHART.rglob("*") if path.is_file()
    }

    values = yaml.safe_load((CHART / "values.yaml").read_text())
    assert values["replicaCount"] >= 2
    assert values["ingress"]["enabled"] is False
    assert values["secrets"]["create"] is False
    assert values["secrets"]["values"] == {
        "apiAuthToken": "",
        "openaiCompatibleApiKey": "",
        "redisUrl": "",
    }
    assert values["application"]["deploymentEnv"] == "production"
    assert values["application"]["memoryProvider"] == "redis"
    assert values["application"]["vectorStoreProvider"] == "chroma_http"
    assert values["application"]["authEnabled"] is True
    assert values["application"]["docsEnabled"] is False
    assert values["networkPolicy"]["enabled"] is True
    assert values["securityContext"]["readOnlyRootFilesystem"] is True
    assert values["temporaryStorage"] == {"sizeLimit": "256Mi"}
    assert values["deployment"]["terminationGracePeriodSeconds"] == 135
    assert values["monitoring"]["scrapeAnnotations"]["enabled"] is False
    assert values["monitoring"]["serviceMonitor"]["enabled"] is False
    assert values["autoscaling"]["enabled"] is False
    assert values["autoscaling"]["maxReplicas"] is None
    assert values["autoscaling"]["targetAverageActiveQueries"] is None


def test_templates_wire_probes_configuration_secrets_and_security():
    deployment = (CHART / "templates" / "deployment.yaml").read_text()
    configmap = (CHART / "templates" / "configmap.yaml").read_text()
    assert "path: /health" in deployment
    assert "path: /ready" in deployment
    assert "configMapRef:" in deployment
    assert "secretKeyRef:" in deployment
    assert "allowPrivilegeEscalation: false" in (CHART / "values.yaml").read_text()
    for name in (
        "DEPLOYMENT_ENV",
        "INFERENCE_PROVIDER",
        "OPENAI_COMPATIBLE_BASE_URL",
        "MEMORY_PROVIDER",
        "VECTOR_STORE_PROVIDER",
        "VECTOR_STORE_HOST",
        "VECTOR_STORE_PORT",
        "VECTOR_STORE_COLLECTION",
        "BM25_CORPUS_VERSION",
        "API_PORT",
        "API_AUTH_ENABLED",
        "API_DOCS_ENABLED",
        "MAX_REQUEST_BYTES",
        "MODEL_ARTIFACT_DIR",
        "MODEL_OFFLINE_MODE",
        "HF_HOME",
        "SENTENCE_TRANSFORMERS_HOME",
    ):
        assert f"{name}:" in configmap
    assert "REDIS_URL" not in configmap
    assert "OPENAI_COMPATIBLE_API_KEY" not in configmap
    assert "API_AUTH_TOKEN" not in configmap
    assert "API_AUTH_TOKEN" in deployment
    assert "mountPath: /tmp" in deployment
    assert "sizeLimit:" in deployment
    assert "terminationGracePeriodSeconds:" in deployment


def test_phase10_values_are_local_non_sensitive_overrides():
    values = yaml.safe_load((PHASE10 / "values.yaml").read_text())
    assert values["image"] == {"repository": "polymind", "tag": "phase10", "pullPolicy": "Never"}
    assert values["application"]["deploymentEnv"] == "production"
    assert values["application"]["vectorStoreHost"] == "phase10-chroma"
    assert values["secrets"] == {"create": False, "existingSecret": "polymind-phase10-secrets"}
    assert values["networkPolicy"]["enabled"] is False
    serialized = (PHASE10 / "values.yaml").read_text().lower()
    assert "api_key" not in serialized
    assert "password" not in serialized


def test_phase10_fixtures_remain_outside_production_chart():
    fixtures = list(yaml.safe_load_all((PHASE10 / "fixtures.yaml").read_text()))
    names = {item["metadata"]["name"] for item in fixtures}
    assert names == {"phase10-inference", "phase10-redis", "phase10-chroma"}
    chart_text = "\n".join(path.read_text() for path in (CHART / "templates").glob("*.yaml")).lower()
    for dependency in ("kind: statefulset", "phase10-redis", "phase10-chroma", "phase10-inference"):
        assert dependency not in chart_text


def test_phase10_script_has_fixed_cluster_context_and_scoped_deletes():
    script = (PHASE10 / "phase10.sh").read_text()
    assert 'CLUSTER="polymind-phase10"' in script
    assert 'CONTEXT="kind-polymind-phase10"' in script
    assert 'NAMESPACE="polymind-phase10"' in script
    assert "require_context" in script
    assert "kubectl delete namespace" not in script
    assert "kubectl delete --all" not in script
    assert "helm uninstall" not in script
    assert 'delete cluster --name "$CLUSTER"' in script
    assert "docker system prune" not in script
    assert "curl -fsS http://127.0.0.1:18001/metrics" in script
    fixtures = (PHASE10 / "fixtures.yaml").read_text()
    assert "hostPath:" not in fixtures
    assert "docker.sock" not in fixtures
    assert "runAsUser: 999" in fixtures


def test_container_defines_the_helm_non_root_identity():
    dockerfile = (ROOT / "Dockerfile").read_text()
    assert "groupadd --gid 10001 polymind" in dockerfile
    assert "useradd --uid 10001 --gid 10001 --no-create-home" in dockerfile
    assert "USER 10001:10001" in dockerfile


def test_network_policy_and_public_ingress_are_secure_by_default():
    policy = (CHART / "templates" / "networkpolicy.yaml").read_text()
    values = yaml.safe_load((CHART / "values.yaml").read_text())
    assert "policyTypes:" in policy
    assert "- Ingress" in policy and "- Egress" in policy
    assert "port: 53" in policy
    assert "namespaceSelector:" in policy and "podSelector:" in policy
    assert "0.0.0.0/0" not in policy
    assert values["ingress"]["hosts"][0]["paths"] == [
        {"path": "/query", "pathType": "Prefix"}
    ]
    assert values["ingress"]["tls"] == []


def test_ingress_template_supports_tls_without_public_metrics_or_probes():
    ingress = (CHART / "templates" / "ingress.yaml").read_text()
    values = yaml.safe_load((CHART / "values.yaml").read_text())
    assert ".Values.ingress.tls" in ingress
    for private_path in ("/metrics", "/health", "/ready", "/docs", "/openapi.json"):
        assert private_path not in ingress
        assert all(path["path"] != private_path for host in values["ingress"]["hosts"] for path in host["paths"])


def test_monitoring_contract_is_opt_in_bounded_and_network_restricted():
    values = yaml.safe_load((CHART / "values.yaml").read_text())
    deployment = (CHART / "templates" / "deployment.yaml").read_text()
    monitor = (CHART / "templates" / "servicemonitor.yaml").read_text()
    policy = (CHART / "templates" / "networkpolicy.yaml").read_text()

    assert values["monitoring"]["scrapeAnnotations"] == {
        "enabled": False,
        "path": "/metrics",
        "port": "",
        "scheme": "http",
    }
    assert ".Values.monitoring.scrapeAnnotations.enabled" in deployment
    assert "prometheus.io/scrape" in deployment
    assert ".Values.podAnnotations" in deployment
    assert "monitoring.coreos.com/v1" in monitor
    assert ".Values.monitoring.serviceMonitor.enabled" in monitor
    assert "namespaceSelector:" in policy and "podSelector:" in policy
    assert values["networkPolicy"]["ingress"]["monitoring"]["enabled"] is False


@pytest.mark.skipif(shutil.which("helm") is None, reason="Helm is not installed")
def test_helm_lint_and_default_render():
    subprocess.run(["helm", "lint", str(CHART)], check=True, capture_output=True, text=True)
    rendered = subprocess.run(
        ["helm", "template", "polymind", str(CHART)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert "kind: Deployment" in rendered
    assert "kind: Service" in rendered
    assert "kind: ConfigMap" in rendered
    assert "kind: NetworkPolicy" in rendered
    assert 'MAX_REQUEST_BYTES: "1048576"' in rendered
    assert "kind: Ingress" not in rendered
    assert "kind: ServiceMonitor" not in rendered
    assert "kind: HorizontalPodAutoscaler" not in rendered
    assert "replicas: 2" in rendered

    enabled = subprocess.run(
        [
            "helm", "template", "polymind", str(CHART),
            "--set", "monitoring.scrapeAnnotations.enabled=true",
            "--set", "monitoring.serviceMonitor.enabled=true",
            "--set", "networkPolicy.ingress.monitoring.enabled=true",
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert 'prometheus.io/scrape: "true"' in enabled
    assert 'prometheus.io/path: "/metrics"' in enabled
    assert 'prometheus.io/port: "8001"' in enabled
    assert "kind: ServiceMonitor" in enabled
    assert "app.kubernetes.io/name: prometheus" in enabled

    autoscaled = subprocess.run(
        [
            "helm", "template", "polymind", str(CHART),
            "--set", "autoscaling.enabled=true",
            "--set", "autoscaling.maxReplicas=4",
            "--set", "autoscaling.targetAverageActiveQueries=1",
        ],
        check=True, capture_output=True, text=True,
    ).stdout
    documents = [item for item in yaml.safe_load_all(autoscaled) if item]
    hpa = next(item for item in documents if item["kind"] == "HorizontalPodAutoscaler")
    deployment = next(item for item in documents if item["kind"] == "Deployment")
    assert hpa["apiVersion"] == "autoscaling/v2"
    assert hpa["spec"]["scaleTargetRef"] == {
        "apiVersion": "apps/v1", "kind": "Deployment", "name": "polymind-polymind",
    }
    assert hpa["spec"]["minReplicas"] == 2
    assert hpa["spec"]["maxReplicas"] == 4
    assert hpa["spec"]["metrics"][0] == {
        "type": "Pods",
        "pods": {
            "metric": {"name": "polymind_active_query_requests"},
            "target": {"type": "AverageValue", "averageValue": "1"},
        },
    }
    assert set(hpa["spec"]["behavior"]) == {"scaleUp", "scaleDown"}
    assert "replicas" not in deployment["spec"]


@pytest.mark.skipif(shutil.which("helm") is None, reason="Helm is not installed")
def test_hpa_requires_explicit_target_and_maximum():
    result = subprocess.run(
        ["helm", "template", "polymind", str(CHART), "--set", "autoscaling.enabled=true"],
        capture_output=True, text=True,
    )
    assert result.returncode != 0
    assert "autoscaling.maxReplicas is required" in result.stderr
