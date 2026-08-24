from pathlib import Path
import shutil
import subprocess

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[2]
CHART = ROOT / "deployment" / "helm" / "polymind"


def test_chart_contains_required_artifacts_and_safe_defaults():
    expected = {
        "Chart.yaml",
        "values.yaml",
        "README.md",
        "templates/_helpers.tpl",
        "templates/configmap.yaml",
        "templates/deployment.yaml",
        "templates/ingress.yaml",
        "templates/secret.yaml",
        "templates/service.yaml",
        "templates/serviceaccount.yaml",
    }
    assert expected <= {
        str(path.relative_to(CHART)) for path in CHART.rglob("*") if path.is_file()
    }

    values = yaml.safe_load((CHART / "values.yaml").read_text())
    assert values["replicaCount"] >= 2
    assert values["ingress"]["enabled"] is False
    assert values["secrets"]["create"] is False
    assert values["secrets"]["values"] == {
        "openaiCompatibleApiKey": "",
        "redisUrl": "",
    }
    assert values["application"]["deploymentEnv"] == "production"
    assert values["application"]["memoryProvider"] == "redis"
    assert values["application"]["vectorStoreProvider"] == "chroma_http"


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
    ):
        assert f"{name}:" in configmap
    assert "REDIS_URL" not in configmap
    assert "OPENAI_COMPATIBLE_API_KEY" not in configmap


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
    assert "kind: Ingress" not in rendered

