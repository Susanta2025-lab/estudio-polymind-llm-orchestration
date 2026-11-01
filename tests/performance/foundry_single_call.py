"""One managed analysis, independently bound and governed. No default live action."""
import argparse
from dataclasses import asdict
from contextlib import contextmanager
from datetime import datetime, timezone
from hashlib import sha256
from io import BytesIO
import json
import os
from pathlib import Path
import time
from typing import Literal
from uuid import UUID, uuid4

from pydantic import Field, model_validator
from documents.models import FrozenModel
from documents.config import ExtractionSettings
from documents.extraction import extract
from documents.storage import LocalObjectStore
from documents.digestion.managed import ManagedSettings, ManagedSynthesisInference, StageProfile, generation_schema
from documents.digestion.models import DigestionError, ValidationDiagnostic
from documents.digestion.diagnostics import PydanticDiagnostic, ValidationReason
from llm.structured import ProviderResultMetadata
from documents.digestion.validation import EvidenceIndex, validate_result
from documents.digestion.workflow import DigestionHandler, prepare
from governance.execution import GovernedExecution
from governance.ledger import GovernanceLedger, QuotaPolicy
from llm.admission import AdmissionPolicy, CallIdentity, SQLiteInferenceAdmission
from llm.azure_schema import provider_schema
from llm.openai_compatible import OpenAICompatibleProvider
from security.authority import SecurityAuthority
from security.identity import OIDCSettings, OIDCVerifier
from security.models import Action, SecurityError
from tests.performance.fixtures import NOW, pdf, profile
from tests.performance.foundry_approval import consume, fsync_directory, load_trust, private_path, read_private, verify_artifact
from tests.performance.foundry_budget import Contract, RunGuard
from tests.performance.foundry_l1 import configuration_digest, generation_contract_digest
from tests.performance.foundry_recalibration import DEPLOYMENT, deployment_configuration, candidate_capability
from tests.performance.foundry_schema_probe import SCHEMA, one_call_contract, digest, PreparationProvider


def executor_digest():
    """Bind transitive local implementation, including security and accounting."""
    root = Path(__file__).resolve().parents[2]
    paths = set()
    for directory in ('documents', 'governance', 'security', 'llm', 'tests/performance'):
        paths.update((root / directory).rglob('*.py'))
    hashes = {str(p.relative_to(root)): sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
    return digest(hashes)


SAFETY_MARGIN_SECONDS = 600


class PreflightDiagnostic:
    """Invocation-local observation only; never an authorization authority."""
    def __init__(self):
        self.stage = 'configuration_loading'
        self.category = 'unexpected_internal_error'
        self.provider_attempted = False
        self.approval_consumption_entered = False
        self.root = None
        self.recorded = False

    @contextmanager
    def step(self, stage, category, expected=(SecurityError,)):
        self.stage = stage
        self.category = 'unexpected_internal_error'
        try:
            yield
        except expected:
            if self.category == 'unexpected_internal_error':
                self.category = category
            raise

    def evidence(self):
        return dict(schema_version='single-call-preflight-diagnostic/1',
                    state='BLOCKED' if self.provider_attempted is False else 'FAILED',
                    stage=self.stage, category=self.category,
                    provider_attempted=self.provider_attempted,
                    approval_consumption_entered=self.approval_consumption_entered)

    def persist(self):
        if self.recorded or self.root is None:
            return
        self.recorded = True
        try:
            root = private_path(self.root, directory=True)
            durable_json(root / f'preflight-diagnostic-{uuid4()}.json', self.evidence())
        except Exception:
            # Diagnostic availability never changes the original failure or permits execution.
            pass


def window_information(config, *, now=None):
    """Offline timing observation, not approval or proof of credential validity."""
    now = time.time() if now is None else now
    start, expires, credential = (config.execution_not_before, config.approval_expires,
                                  config.credential_valid_until)
    cutoff = None if expires is None or credential is None else min(expires, credential) - SAFETY_MARGIN_SECONDS
    def utc(value):
        return None if value is None else datetime.fromtimestamp(value, timezone.utc).isoformat()
    return dict(reviewed_at_utc=utc(now), execution_not_before_utc=utc(start),
                approval_expires_utc=utc(expires), credential_valid_until_utc=utc(credential),
                launch_before_utc=utc(cutoff), safety_margin_seconds=SAFETY_MARGIN_SECONDS,
                remaining_launch_seconds=None if cutoff is None else cutoff-now,
                window_eligible=start is not None and cutoff is not None and start <= now < cutoff,
                cutoff_inclusive=False)


class SingleCallConfiguration(FrozenModel):
    executor: Literal['polymind-single-analysis/1'] = 'polymind-single-analysis/1'
    executor_sha256: str
    generation_contract_sha256: str
    provider_schema_sha256: Literal[SCHEMA] = SCHEMA
    maximum_calls: Literal[1] = 1
    resource: Literal['epolymind-foundry-dev-susanta']
    deployment: Literal['epolymind-gpt-54-mini']
    model: Literal['gpt-5.4-mini']
    model_version: Literal['2026-03-17']
    sku: Literal['GlobalStandard']
    endpoint: str
    authentication: Literal['entra_bearer', 'api_key']
    owner_scope: str
    oidc: OIDCSettings
    security_path: Path
    governance_path: Path
    admission_path: Path
    quota_key: str
    policy: AdmissionPolicy
    governance_policy: QuotaPolicy
    contract: Contract
    audit_directory: Path
    job_id: UUID
    request_id: UUID
    rendered_request_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')
    fixture_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')
    # Preparation deliberately cannot invent these fresh operator attestations.
    credential_valid_until: int | None = None
    approval_expires: int | None = None
    execution_not_before: int | None = None
    credential_audience_verified: Literal[True] | None = None
    quota_verified: Literal[True] | None = None
    shared_consumers_verified: Literal[True] | None = None
    charges_verified: Literal[True] | None = None
    actual_azure_rpm: int | None = Field(default=None, ge=1)
    actual_azure_tpm: int | None = Field(default=None, ge=28000, le=30000)

    @model_validator(mode='after')
    def bounded(self):
        if (self.executor_sha256 != executor_digest()
                or self.generation_contract_sha256 != generation_contract_digest()
                or digest(provider_schema(generation_schema())) != self.provider_schema_sha256):
            raise ValueError('Execution contract changed')
        c = self.contract
        if c != one_call_contract(c.model_dump(mode='json'), c.catalog):
            raise ValueError('Exactly one bounded attempt required')
        binding = self.governance_policy.evaluation
        if (binding is None or binding.version != 'polymind-evaluation/1'
                or self.owner_scope not in {s.identity() for s in binding.scopes}
                or self.oidc.token_profile != 'entra_v2'):
            raise ValueError('Existing evaluation scope and Entra identity required')
        binding.validate_authorities(self.governance_path, self.admission_path, self.quota_key, self.policy)
        p = self.policy
        if (p.interactive_tpm < 2000 or p.per_job_rpm != 1 or c.tpm > p.tpm
                or c.input_tokens + c.output_tokens > p.tpm - p.interactive_tpm):
            raise ValueError('Shared provider capacity incompatible')
        deployment_configuration(self.endpoint, {'general': self.deployment, 'summarization': self.deployment},
                                 self.resource, self.deployment)
        return self

    def require_live_window(self, *, now=None):
        names = ('credential_valid_until', 'approval_expires', 'execution_not_before',
                 'credential_audience_verified', 'quota_verified', 'shared_consumers_verified',
                 'charges_verified', 'actual_azure_rpm', 'actual_azure_tpm')
        if any(getattr(self, name) is None for name in names):
            raise SecurityError('authentication_required')
        now = time.time() if now is None else now
        if (not self.execution_not_before <= now
                or min(self.approval_expires, self.credential_valid_until) <= now + SAFETY_MARGIN_SECONDS
                or self.policy.rpm > self.actual_azure_rpm or self.policy.tpm > self.actual_azure_tpm):
            raise SecurityError('unsupported_execution')



def prepare_analysis(root, scope):
    """Same four-page extraction, plan and first managed request; no execution."""
    settings = ManagedSettings(capability=candidate_capability(strict_digestion=True),
        generation_profile='managed-generation/2', max_response_envelope_bytes=26192,
        profiles=tuple(StageProfile(stage=s, input_tokens=24800, output_tokens=3000)
                       for s in ('chunk', 'intermediate', 'structural', 'root')))
    adapter = ManagedSynthesisInference(PreparationProvider(), settings, None)
    chosen = adapter.profile(profile(context_tokens=28000, reserved_output_tokens=3000,
                                    max_result_characters=10000, max_response_bytes=10000))
    source, manifest = pdf(4, seed=1708)
    store = LocalObjectStore(root / 'objects')
    artifact, ref = extract(BytesIO(source), scope=scope, document_id=UUID(int=4),
        display_filename='manual.pdf', declared_mime='application/pdf', store=store,
        limits=ExtractionSettings(), created_at=NOW, extracted_at=NOW)
    plan, _ = prepare(artifact, ref, chosen, store)
    if len(plan.chunks) != 1 or len(artifact.units) != 4:
        raise ValueError('Fixture composition changed')
    request = DigestionHandler.request(plan, plan.chunks[0].chunk_id, {}, {})
    index = EvidenceIndex(artifact)
    if any(index.resolve(p.evidence) != p.text for p in request.source_data):
        raise ValueError('Evidence mismatch')
    generation, estimate = adapter.render(request)
    if estimate > 25000:
        raise ValueError('Input reservation exceeded')
    request_hash = digest(dict(system=generation.system, data=generation.data, schema=generation.schema))
    return artifact, request, index, generation, manifest['sha256'], request_hash


def durable_json(path, value):
    """New immutable evidence only, private and fsynced; never rewrite history."""
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'w') as stream:
        json.dump(value, stream, sort_keys=True, separators=(',', ':'))
        stream.flush()
        os.fsync(stream.fileno())
    fsync_directory(path.parent)


def no_retry_session():
    import requests
    from requests.adapters import HTTPAdapter
    session = requests.Session()
    session.trust_env = False
    session.mount('https://', HTTPAdapter(max_retries=0))
    if session.get_adapter('https://').max_retries.total != 0:
        session.close()
        raise SecurityError('unsupported_execution')
    return session


def execute_stage(config, principal, authority, ledger, guard, provider, prepared):
    """Only first analysis. RunGuard plus durable ledger transitions forbid replay."""
    config = SingleCallConfiguration.model_validate(config.model_dump())
    artifact, request, index, generation, fixture_hash, request_hash = prepared
    if (fixture_hash != config.fixture_sha256 or request_hash != config.rendered_request_sha256
            or request.stage != 'analysis' or request.children
            or artifact.document.scope != principal.scope or config.contract.attempts != 1
            or guard.contract != config.contract):
        raise SecurityError('unsupported_execution')
    snapshot = authority.snapshot(principal, (artifact.document.document_id,), Action.DOCUMENT_DELETE)
    identity = CallIdentity(principal.scope.identity(), config.job_id, config.request_id, 1,
        config.executor, provider.name, generation.role.value, config.deployment, generation.capability.version)
    audit = dict(state='FAILED', provider_acceptance='not_observed', application_validation='not_reached',
                 configuration_sha256=configuration_digest(config), accounting_failed=False)
    class ObservedProvider:
        name = provider.name

        def model_id(self, role):
            return provider.model_id(role)

        def execute(self, generation):
            try:
                result = provider.execute(generation)
            except BaseException as exc:
                metadata = getattr(exc, 'provider_metadata', None)
                if type(metadata) is ProviderResultMetadata:
                    audit['provider_metadata'] = metadata.evidence()
                raise
            if type(result.metadata) is ProviderResultMetadata:
                audit['provider_metadata'] = result.metadata.evidence()
            audit['provider_acceptance'] = 'completed_strict_response'
            return result

    governed = GovernedExecution(ObservedProvider(), guard, ledger, authority, snapshot)
    def active():
        if (min(config.approval_expires or 0, config.credential_valid_until or 0, principal.expires)
                <= time.time() + 60 or (config.audit_directory / 'CANCEL').exists()):
            raise SecurityError()
    try:
        response = governed.execute(generation, identity=identity, check_active=active,
                                    workload='DOCUMENT_BACKGROUND')
        audit['provider_acceptance'] = 'completed_strict_response'
        authority.revalidate(snapshot)
        audit['application_validation'] = 'failed'
        result = validate_result(response.text.encode('utf-8'), request, index)
        audit['application_validation'] = 'accepted'
        from documents.digestion.codec import encode
        audit['canonical_bytes'] = len(encode(result))
        audit['result_sha256'] = sha256(encode(result)).hexdigest()
        audit['state'] = 'SUCCEEDED'
    except BaseException as exc:
        # Closed categories only. Never serialize exceptions, prompts or response bodies.
        from documents.digestion.managed import classify_managed
        audit['failure'] = classify_managed(exc).category
        if (audit['application_validation'] == 'failed' and isinstance(exc, DigestionError)
                and type(exc.validation_diagnostic) is ValidationDiagnostic):
            audit['validation_diagnostic'] = exc.validation_diagnostic.value
            if type(exc.validation_reason) is ValidationReason:
                audit['validation_reason'] = exc.validation_reason.value
            if type(exc.pydantic_diagnostic) is PydanticDiagnostic:
                audit['pydantic_diagnostic'] = exc.pydantic_diagnostic.evidence()
        audit['accounting_failed'] = bool(getattr(exc, 'accounting_failed', False))
        if hasattr(exc, 'rejection_diagnostics'):
            audit['rejection'] = exc.rejection_diagnostics
            if audit['rejection']['reason'] == 'strict_schema_rejected':
                audit['provider_acceptance'] = 'schema_rejected'
        from llm.inference import InferenceOutputLimitError
        if isinstance(exc, InferenceOutputLimitError):
            audit['output_limit'] = asdict(exc.diagnostics)
        try:
            guard.stop('provider')
        except BaseException:
            audit['accounting_failed'] = True
    # Always finalize before returning a status. Audit failure itself fails the CLI.
    try:
        audit['run'] = guard.records()
        audit['calls'] = len(audit['run'])
        audit['governance'] = [r for r in ledger.usage(principal, authority)
                               if json.loads(r['identity'])['job'] == str(config.job_id)]
    except BaseException:
        audit['state'] = 'FAILED'
        audit['accounting_failed'] = True
        audit.setdefault('failure', 'governance_denied')
        audit.setdefault('calls', None)
    durable_json(config.audit_directory / 'outcome.json', audit)
    return audit


def check_window(config, diagnostic):
    with diagnostic.step('execution_window', 'window_requirements_not_met'):
        now = time.time()
        try:
            config.require_live_window(now=now)
        except SecurityError:
            if config.execution_not_before is not None and now < config.execution_not_before:
                diagnostic.category = 'window_not_started'
            elif (config.approval_expires is not None and config.credential_valid_until is not None
                  and min(config.approval_expires, config.credential_valid_until) <= now + SAFETY_MARGIN_SECONDS):
                diagnostic.category = 'window_insufficient_remaining_time'
            raise


def launch(config, acknowledgement, access_token, credential, approval, trust, *, diagnostic=None):
    diagnostic = diagnostic or PreflightDiagnostic()
    try:
        return _launch(config, acknowledgement, access_token, credential, approval, trust, diagnostic)
    except Exception:
        diagnostic.persist()
        raise


def _launch(config, acknowledgement, access_token, credential, approval, trust, diagnostic):
    with diagnostic.step('configuration_validation', 'invalid_configuration', (ValueError,)):
        config = SingleCallConfiguration.model_validate(config.model_dump())
    # A validated directory can receive early-window diagnostics without creating it.
    diagnostic.root = config.audit_directory
    check_window(config, diagnostic)
    with diagnostic.step('private_path_validation', 'private_path_invalid', (ValueError, OSError)):
        root = private_path(config.audit_directory, directory=True)
        for path in (config.security_path, config.governance_path, config.admission_path):
            private_path(path)
    with diagnostic.step('credential_presence', 'credential_missing'):
        if not credential or not credential.strip():
            raise SecurityError('authentication_required')
    with diagnostic.step('configuration_acknowledgement', 'approval_digest_mismatch'):
        fingerprint = configuration_digest(config)
        if acknowledgement != fingerprint:
            raise SecurityError()
    with diagnostic.step('operator_identity_verification', 'operator_authentication_failed'):
        principal = OIDCVerifier(config.oidc).verify(access_token)
    with diagnostic.step('operator_scope_verification', 'operator_authorization_failed'):
        if (principal.scope.identity() != config.owner_scope
                or Action.PUBLICATION_MANAGE not in principal.permissions):
            raise SecurityError()
    with diagnostic.step('signed_approval_verification', 'approval_verification_failed'):
        verify_artifact(approval, trust, config, principal, fingerprint)
    with diagnostic.step('security_authorization', 'operator_authorization_failed'):
        authority = SecurityAuthority(config.security_path)
        authority.authorize(principal, Action.PUBLICATION_MANAGE)
    with diagnostic.step('fixture_preparation', 'fixture_validation_failed', (ValueError, SecurityError)):
        prepared = prepare_analysis(root, principal.scope)
    with diagnostic.step('fixture_digest_verification', 'fixture_mismatch'):
        if prepared[-2:] != (config.fixture_sha256, config.rendered_request_sha256):
            raise SecurityError('unsupported_execution')
    with diagnostic.step('governance_initialization', 'governance_unavailable', (OSError,)):
        ledger = GovernanceLedger(config.governance_path, config.governance_policy, config.contract.catalog,
            provider_path=config.admission_path, provider_key=config.quota_key, provider_policy=config.policy)
        admission = SQLiteInferenceAdmission(config.admission_path, config.quota_key, config.policy)
    with diagnostic.step('replay_protection', 'replay_rejected'):
        guard = RunGuard(root / 'run.sqlite', config.contract, admission)
        if guard.records() or (root / 'live-started.json').exists():
            raise SecurityError('unsupported_execution')
    with diagnostic.step('signed_approval_verification', 'approval_verification_failed'):
        verified = verify_artifact(approval, trust, config, principal, fingerprint)
    with diagnostic.step('approval_consumption', 'approval_consumption_failed', (SecurityError, OSError)):
        diagnostic.approval_consumption_entered = True
        consume(verified, trust, approval)
    with diagnostic.step('live_marker_creation', 'live_marker_failed', (OSError,)):
        durable_json(root / 'live-started.json', dict(configuration_sha256=fingerprint,
                                                    approval_id=verified['jti'], executor=config.executor))
    diagnostic.stage = 'provider_initialization'
    diagnostic.category = 'unexpected_internal_error'
    authority.register_document(principal, prepared[0].document)
    session = no_retry_session()
    try:
        provider = OpenAICompatibleProvider(base_url=config.endpoint,
            model_map={'summarization': config.deployment, 'general': config.deployment}, api_key=credential,
            authentication_header='api-key' if config.authentication == 'api_key' else 'Authorization',
            connect_timeout=5, read_timeout=60, readiness_retries=0, http_client=session)
        diagnostic.stage = 'provider_execution'
        # Entering execution is not proof that the HTTP transport was reached.
        diagnostic.provider_attempted = None
        return execute_stage(config, principal, authority, ledger, guard, provider, prepared)
    finally:
        session.close()


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--configuration', type=Path, required=True)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--approve-sha256')
    parser.add_argument('--approval', type=Path)
    parser.add_argument('--approval-trust', type=Path)
    parser.add_argument('--attestations', type=Path,
                        help='Offline: bind fresh operator window/capacity attestations')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.live:
        for name in ('approve_sha256', 'approval', 'approval_trust'):
            if not getattr(args, name):
                parser.error('--live requires --' + name.replace('_', '-'))
    os.umask(0o077)
    diagnostic = PreflightDiagnostic()
    try:
        with diagnostic.step('configuration_loading', 'configuration_unavailable', (ValueError, OSError)):
            raw = read_private(args.configuration, 262144)
        with diagnostic.step('configuration_validation', 'invalid_configuration', (ValueError,)):
            config = SingleCallConfiguration.model_validate_json(raw)
        diagnostic.root = config.audit_directory
        if args.attestations:
            with diagnostic.step('configuration_finalization', 'invalid_configuration', (ValueError,)):
                if args.live or args.output is None:
                    raise ValueError('Finalization is offline only and requires a new output path')
                values = json.loads(read_private(args.attestations, 16384))
                allowed = {'credential_valid_until', 'approval_expires', 'execution_not_before',
                           'credential_audience_verified', 'quota_verified', 'shared_consumers_verified',
                           'charges_verified', 'actual_azure_rpm', 'actual_azure_tpm'}
                if set(values) != allowed:
                    raise ValueError('Exact fresh attestations required')
                config = SingleCallConfiguration.model_validate({**config.model_dump(), **values})
            check_window(config, diagnostic)
            with diagnostic.step('private_path_validation', 'private_path_invalid', (ValueError, OSError)):
                output = private_path(args.output, exists=False)
                private_path(output.parent, directory=True)
                durable_json(output, config.model_dump(mode='json'))
        if not args.live:
            print(json.dumps({'state': 'PREPARED', 'configuration_sha256': configuration_digest(config),
                              'executor_sha256': config.executor_sha256,
                              'execution_window': window_information(config)}))
            return 0
        with diagnostic.step('approval_loading', 'approval_unavailable', (ValueError, OSError)):
            approval = read_private(args.approval, 16384).decode('ascii').strip()
            trust = load_trust(args.approval_trust)
        outcome = launch(config, args.approve_sha256, os.environ.get('POLYMIND_L1_OPERATOR_TOKEN', ''),
            os.environ.get('POLYMIND_L1_AZURE_CREDENTIAL', ''),
            approval, trust, diagnostic=diagnostic)
        print(json.dumps({k: outcome[k] for k in ('state', 'calls')}))
        return 0 if outcome['state'] == 'SUCCEEDED' else 1
    except Exception:
        diagnostic.persist()
        evidence = diagnostic.evidence()
        print('Single-call execution: ' + evidence['state'])
        print('Stage: ' + evidence['stage'])
        print('Category: ' + evidence['category'])
        print('Provider request attempted: ' + ('NO' if diagnostic.provider_attempted is False else 'UNKNOWN'))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
