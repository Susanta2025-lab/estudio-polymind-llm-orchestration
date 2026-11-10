"""Offline F1 through real responses, adapter, RunGuard and temporary ledgers.

No launcher, approval creation/signing/consumption or live authority is used.
"""

import json
import time
from decimal import Decimal
from hashlib import sha256
from uuid import uuid4

import pytest

# Permanent historical canonical-output characterization.
pytestmark = pytest.mark.usefixtures("managed_v9")


from governance.ledger import (
    EvaluationBinding,
    GovernanceError,
    GovernanceLedger,
    Limits,
    QuotaPolicy,
)
from llm.admission import CallIdentity, SQLiteInferenceAdmission
from llm.inference import InferenceConnectionError
from llm.openai_compatible import OpenAICompatibleProvider
from security.authority import SecurityAuthority
from security.identity import OIDCSettings
from security.models import Action, _verified_principal
from tests.performance import foundry_single_call as harness
from tests.performance.foundry_preflight import OfflineHTTP
from tests.performance.foundry_recalibration import (
    DEPLOYMENT,
    RESOURCE,
    candidate_policy,
)
from tests.unit.test_foundry_schema_probe import catalog, previous
from tests.unit.test_http_cleanup import SECRET, Session, real_response, scenario


@pytest.fixture
def stage(tmp_path):
    principal = _verified_principal(
        "offline",
        "f1",
        "synthetic",
        frozenset({Action.PUBLICATION_MANAGE}),
        expires=int(time.time()) + 3600,
    )
    root = tmp_path / "audit"
    root.mkdir(mode=0o700)
    policy = candidate_policy()
    binding = EvaluationBinding(
        version="polymind-evaluation/1",
        scopes=(principal.scope,),
        governance_path=str(tmp_path / "governance.sqlite"),
        provider_path=str(tmp_path / "admission.sqlite"),
        provider_key=DEPLOYMENT,
        provider_policy_sha256=sha256(policy.model_dump_json().encode()).hexdigest(),
    )
    limits = Limits(
        requests_per_window=16,
        window_seconds=86400,
        interactive_concurrent=1,
        background_concurrent=1,
        reserved_tokens=112000,
        daily_tokens=500000,
        monthly_tokens=1500000,
        monthly_cost="5",
    )
    quota = QuotaPolicy(
        version="synthetic/1", owner=limits, tenant=limits, evaluation=binding
    )
    prepared = harness.prepare_analysis(tmp_path / "preparation", principal.scope)
    tenant = "11111111-1111-4111-8111-111111111111"
    config = harness.SingleCallConfiguration(
        executor_sha256=harness.executor_digest(),
        generation_contract_sha256=harness.generation_contract_digest(),
        resource=RESOURCE,
        deployment=DEPLOYMENT,
        model="gpt-5.4-mini",
        model_version="2026-03-17",
        sku="GlobalStandard",
        endpoint=f"https://{RESOURCE}.openai.azure.com/openai/v1",
        authentication="api_key",
        owner_scope=principal.scope.identity(),
        oidc=OIDCSettings(
            token_profile="entra_v2",
            tenant_id=tenant,
            audience="22222222-2222-4222-8222-222222222222",
            issuer=f"https://login.microsoftonline.com/{tenant}/v2.0",
            jwks_url=f"https://login.microsoftonline.com/{tenant}/discovery/v2.0/keys",
        ),
        security_path=tmp_path / "security.sqlite",
        governance_path=binding.governance_path,
        admission_path=binding.provider_path,
        quota_key=DEPLOYMENT,
        policy=policy,
        governance_policy=quota,
        contract=harness.one_call_contract(previous(), catalog()),
        audit_directory=root,
        job_id=uuid4(),
        request_id=uuid4(),
        rendered_request_sha256=prepared[-1],
        fixture_sha256=prepared[-2],
        credential_valid_until=int(time.time()) + 3600,
        approval_expires=int(time.time()) + 3600,
    )
    authority = SecurityAuthority(config.security_path)
    authority.register(principal)
    authority.register_document(principal, prepared[0].document)
    ledger = GovernanceLedger(
        config.governance_path,
        quota,
        config.contract.catalog,
        provider_path=config.admission_path,
        provider_key=DEPLOYMENT,
        provider_policy=policy,
    )
    admission = SQLiteInferenceAdmission(config.admission_path, DEPLOYMENT, policy)
    guard = harness.RunGuard(root / "run.sqlite", config.contract, admission)
    return config, principal, authority, ledger, guard, prepared


class HTTP(OfflineHTTP):
    def __init__(self, case, cleanup_failure):
        super().__init__()
        self.case, self.cleanup_failure = case, cleanup_failure
        self.posts = 0
        self.response_object = None

    def post(self, url, **kwargs):
        self.posts += 1
        error = OSError(SECRET) if self.cleanup_failure else None
        if self.case in ("redirect", "oversize", "timeout", "malformed"):
            self.response_object = scenario(self.case, error)
        else:
            original = super().post(url, **kwargs)
            value = json.loads(b"".join(original.iter_content(1)))
            value["model"] = "gpt-5.4-mini-2026-03-17"
            if self.case == "truncated":
                value["choices"][0].update(
                    finish_reason="length", message={"content": None}
                )
            elif self.case == "invalid_usage":
                value["usage"]["total_tokens"] = 0
            elif self.case == "unknown_usage":
                value.pop("usage")
            elif self.case == "application_rejected":
                content = json.loads(value["choices"][0]["message"]["content"])
                content["claims"][0]["claim_id"] = SECRET
                value["choices"][0]["message"]["content"] = json.dumps(content)
            self.response_object = real_response(
                json.dumps(value).encode(), cleanup_error=error
            )
        return self.response_object


@pytest.mark.parametrize("cleanup_failure", [False, True])
@pytest.mark.parametrize(
    "case,public,known",
    [
        ("redirect", "inference_configuration", False),
        ("oversize", "inference_output_limit", False),
        ("timeout", "inference_timeout", False),
        ("malformed", "inference_invalid_response", False),
        ("valid", None, True),
        ("truncated", "inference_output_limit", True),
        ("invalid_usage", "inference_invalid_response", False),
        ("unknown_usage", "governance_denied", False),
        ("application_rejected", "serialization_error", True),
    ],
)
def test_single_call_cleanup_accounting_and_containment(
    stage, monkeypatch, case, public, known, cleanup_failure
):
    config, principal, authority, ledger, guard, prepared = stage
    http = HTTP(case, cleanup_failure)
    provider = OpenAICompatibleProvider(
        base_url=config.endpoint,
        model_map={"general": DEPLOYMENT, "summarization": DEPLOYMENT},
        http_client=http,
    )
    # All workflow entrypoints outside the single analysis are forbidden.
    from tests.performance import foundry_l1, foundry_preflight

    def forbidden(*args, **kwargs):
        raise AssertionError("Unexpected downstream workflow")

    for module, names in (
        (foundry_l1, ("launch", "local_retrieval")),
        (foundry_preflight, ("execute", "publish", "questions")),
    ):
        for name in names:
            monkeypatch.setattr(module, name, forbidden)
    result = harness.execute_stage(
        config, principal, authority, ledger, guard, provider, prepared
    )
    if cleanup_failure and case not in ("redirect", "oversize", "timeout", "malformed"):
        # Cleanup precedes adapter usage validation: no usage has been established.
        public, known = "inference_unavailable", False
    assert result["state"] == ("SUCCEEDED" if public is None else "FAILED")
    assert result.get("failure") == public
    assert result["calls"] == http.posts == len(guard.records()) == 1
    # With missing usage after provider success, accounting is the primary
    # governance failure. The marker flags cleanup failures on an existing error.
    assert result["accounting_failed"] is (not known and public != "governance_denied")
    row = ledger.usage(principal, authority)[0]
    assert row["state"] == ("SETTLED" if known else "UNKNOWN")
    if known:
        assert row["actual_input"] == 30 and row["actual_output"] == 40
        assert Decimal(row["actual_cost"]) == config.contract.catalog.price(
            "openai_compatible", DEPLOYMENT
        ).cost(30, 40)
        assert result["provider_metadata"]["completion_tokens"] == 40
    else:
        assert (
            row["actual_input"] is None
            and row["actual_output"] is None
            and row["actual_cost"] is None
        )
        assert result["provider_metadata"]["prompt_tokens"] is None
    if case == "oversize":
        assert result["output_limit"]["failure_cause"] == "unknown"
        assert result["output_limit"]["response_byte_limit"] == 10000
        assert result["output_limit"]["completion_token_limit"] == 3000
    serialized = (config.audit_directory / "outcome.json").read_text()
    assert json.loads(serialized) == result
    assert SECRET not in serialized
    assert '"content"' not in serialized and '"text"' not in serialized
    assert "UNTRUSTED_DOCUMENT_DATA" not in serialized
    identity = CallIdentity(
        principal.scope.identity(),
        uuid4(),
        uuid4(),
        1,
        config.executor,
        provider.name,
        "summarization",
        DEPLOYMENT,
        prepared[3].capability.version,
    )
    with pytest.raises(GovernanceError):
        guard.acquire(identity, 100, 3000)
    assert http.posts == 1 and len(guard.records()) == 1


@pytest.mark.parametrize(
    "case,public",
    [
        ("valid", None),
        ("truncated", "inference_output_limit"),
        ("application_rejected", "serialization_error"),
    ],
)
def test_owned_session_close_cannot_erase_settled_usage(
    stage, monkeypatch, case, public
):
    config, principal, authority, ledger, guard, prepared = stage
    http = HTTP(case, False)
    session = Session(None, cleanup_error=OSError(SECRET))
    session.post.side_effect = http.post
    monkeypatch.setattr("requests.Session", lambda: session)
    provider = OpenAICompatibleProvider(
        base_url=config.endpoint,
        model_map={"general": DEPLOYMENT, "summarization": DEPLOYMENT},
    )
    audit = None
    # Session lifetime spans execution and settlement; do not add per-call close.
    with pytest.raises(InferenceConnectionError) as caught:
        try:
            audit = harness.execute_stage(
                config, principal, authority, ledger, guard, provider, prepared
            )
        finally:
            provider.close()
    assert str(caught.value) == "Inference provider cleanup failed."
    assert caught.value.__suppress_context__ and caught.value.__cause__ is None
    assert audit.get("failure") == public and not audit["accounting_failed"]
    assert audit["provider_metadata"]["completion_tokens"] == 40
    assert ledger.usage(principal, authority)[0]["state"] == "SETTLED"
    assert (
        http.posts == session.post.call_count == audit["calls"] == session.closes == 1
    )
    assert json.loads((config.audit_directory / "outcome.json").read_text()) == audit
