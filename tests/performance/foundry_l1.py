"""Operator-bound L1 composition. Default command is a network-forbidden dry run.

Live execution requires a separately signed operator approval bound to the private
configuration hash, explicit CLI opt-in and existing security/quota authorities.
Never import synthetic identities or prices into the live construction path.
"""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import time
from typing import Literal

from pydantic import Field, model_serializer, model_validator

from documents.models import FrozenModel
from governance.ledger import GovernanceLedger, QuotaPolicy
from llm.admission import AdmissionPolicy, SQLiteInferenceAdmission
from llm.openai_compatible import OpenAICompatibleProvider
from security.authority import SecurityAuthority
from security.identity import OIDCSettings, OIDCVerifier
from security.models import Action, SecurityError
from tests.performance.foundry_approval import (
    consume, fsync_directory, load_trust, private_path, read_private, verify_artifact,
)
from tests.performance.foundry_budget import Contract, RunGuard
from tests.performance.foundry_recalibration import DEPLOYMENT, RESOURCE, deployment_configuration


def generation_contract_digest():
    """generation-inventory/2: additive wire, identity and durable-association sources."""
    root = Path(__file__).resolve().parents[2]
    paths = ('documents/digestion/managed.py', 'documents/digestion/models.py',
             'documents/digestion/validation.py', 'documents/digestion/planning.py',
             'documents/digestion/sizing.py', 'documents/digestion/workflow.py',
             'documents/digestion/diagnostics.py',
             'documents/digestion/wire.py', 'documents/digestion/receipts.py',
             'documents/digestion/codec.py',
             'documents/models.py', 'documents/jobs/models.py',
             'documents/jobs/worker.py', 'documents/jobs/sqlite.py',
             'documents/storage.py', 'tests/performance/foundry_l1.py',
             'tests/performance/foundry_single_call.py',
             'documents/publication/analysis.py', 'llm/structured.py',
             'llm/bounded_http.py', 'llm/openai_compatible.py', 'llm/azure_schema.py',
             'tests/performance/fixtures.py', 'tests/performance/foundry_preflight.py',
             'tests/performance/foundry_recalibration.py')
    hashes = {path: sha256((root/path).read_bytes()).hexdigest() for path in paths}
    return sha256(json.dumps(hashes, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


class LaunchConfiguration(FrozenModel):
    managed_prompt_version: Literal['managed-prompt/10', 'managed-prompt/11'] = 'managed-prompt/10'
    resource: Literal['epolymind-foundry-dev-susanta']
    deployment: Literal['epolymind-gpt-54-mini']
    model: Literal['gpt-5.4-mini']
    model_version: Literal['2026-03-17']
    sku: Literal['GlobalStandard']
    endpoint: str
    authentication: Literal['entra_bearer', 'api_key']
    credential_valid_until: int
    credential_audience_verified: Literal[True]
    quota_verified: Literal[True]
    shared_consumers_verified: Literal[True]
    charges_verified: Literal[True]
    approval_expires: int
    generation_contract_sha256: str = Field(default_factory=generation_contract_digest,
                                             pattern=r'^[0-9a-f]{64}$')
    execution_not_before: int = Field(default=0, ge=0)
    owner_scope: str
    oidc: OIDCSettings
    security_path: Path
    governance_path: Path
    admission_path: Path
    quota_key: str = Field(min_length=1)
    audit_directory: Path
    embedding_directory: Path
    embedding_tree_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')
    actual_azure_rpm: int = Field(ge=1)
    actual_azure_tpm: int = Field(ge=1, le=30000)
    policy: AdmissionPolicy
    governance_policy: QuotaPolicy
    contract: Contract

    @model_serializer(mode='wrap')
    def serialize(self, handler):
        value = handler(self)
        # Preserve the established default-v10 canonical configuration shape.
        # Explicit v11 selection is included in the configuration/signature binding.
        if self.managed_prompt_version == 'managed-prompt/10':
            value.pop('managed_prompt_version', None)
        return value

    @model_validator(mode='after')
    def bounded(self):
        c, p = self.contract, self.policy
        if self.governance_policy.evaluation is not None:
            binding = self.governance_policy.evaluation
            binding.validate_authorities(self.governance_path, self.admission_path, self.quota_key, p)
            if self.owner_scope not in {scope.identity() for scope in binding.scopes}:
                raise ValueError('L1 evaluation scope is not authorized')
        if (self.generation_contract_sha256 != generation_contract_digest()
                or self.execution_not_before + 600 >= min(self.approval_expires, self.credential_valid_until)):
            raise ValueError('Reviewed generation contract or execution window is incompatible')
        deployment_configuration(self.endpoint, {'general':self.deployment,'summarization':self.deployment},
                                 self.resource, self.deployment)
        if (c.provider != 'openai_compatible' or c.model != DEPLOYMENT or c.tier != 'GlobalStandard'
                or c.attempts != 4 or c.total_input > 100000 or c.total_output > 12000
                or c.context > 28000 or c.rpm != 1 or not c.fits(4)
                or p.interactive_tpm < 2000 or p.per_job_rpm != 1
                or p.tpm > self.actual_azure_tpm or p.rpm > self.actual_azure_rpm
                or c.tpm > p.tpm or c.input_tokens+c.output_tokens > p.tpm-p.interactive_tpm
                or c.output_tokens != 3000
                or any(x <= 0 for x in (c.catalog.price(c.provider,c.model).input_price,
                                        c.catalog.price(c.provider,c.model).output_price))):
            raise ValueError('L1 financial or quota contract is incompatible')
        if min(self.approval_expires,self.credential_valid_until) <= time.time()+600:
            raise ValueError('Approval and credential lifetime must cover L1')
        return self


def load_configuration(path):
    raw = read_private(path, 262144)
    config = LaunchConfiguration.model_validate_json(raw)
    return config, configuration_digest(config)


def configuration_digest(config):
    return sha256(config.model_dump_json().encode()).hexdigest()


def verify_approval(config, digest, acknowledgement, access_token, verifier, *, approval=None, approval_trust=None):
    if acknowledgement != digest or digest != configuration_digest(config):
        raise SecurityError()
    principal = verifier.verify(access_token)
    if (principal.scope.identity() != config.owner_scope
            or Action.PUBLICATION_MANAGE not in principal.permissions):
        raise SecurityError()
    verify_artifact(approval, approval_trust, config, principal, digest)
    return principal


class Runtime:
    def __init__(self, config, principal, authority, ledger, guard, provider, vectors, encoder):
        self.config, self.principal, self.authority = config, principal, authority
        self.contract, self.ledger, self.guard = config.contract, ledger, guard
        self.provider, self.vectors, self.encoder = provider, vectors, encoder

    def wait(self):
        while True:
            if min(self.config.approval_expires,self.config.credential_valid_until,self.principal.expires) <= time.time()+60:
                self.guard.stop('identity')
                raise SecurityError()
            if (self.config.audit_directory/'CANCEL').exists():
                self.guard.stop('cancelled')
                raise SecurityError()
            rows = self.guard.records()
            delay = max(0, max((r['started'] for r in rows), default=0)+61-time.time())
            if not delay:
                return
            time.sleep(min(delay, 1))


def local_retrieval(config):
    # Explicit local-only pinned model directory; never download or use cloud embeddings.
    from config.model_artifacts import EMBEDDING_MODEL
    from sentence_transformers import SentenceTransformer
    from documents.publication.encoding import RetrievalEncoder
    from documents.publication.models import RetrievalProfile
    from rag.chroma_store import ChromaVectorStore
    import chromadb
    from chromadb.config import Settings
    directory = config.embedding_directory
    if not directory.is_absolute() or not directory.is_dir():
        raise ValueError('Approved local embedding artifacts required')
    digest = sha256()
    for path in sorted(directory.rglob('*')):
        if path.is_symlink():
            raise ValueError('Embedding symlinks are not allowed')
        if path.is_file():
            digest.update(str(path.relative_to(directory)).encode()+b'\0')
            digest.update(sha256(path.read_bytes()).digest())
    if digest.hexdigest() != config.embedding_tree_sha256:
        raise ValueError('Approved embedding artifact hash mismatch')
    model = SentenceTransformer(str(directory), local_files_only=True, device='cpu')
    profile = RetrievalProfile()
    if profile.embedding_revision != EMBEDDING_MODEL.revision:
        raise ValueError('Pinned embedding revision mismatch')
    encoder = RetrievalEncoder(profile, model)
    client = chromadb.PersistentClient(path=str(config.audit_directory/'vectors'),
                                       settings=Settings(anonymized_telemetry=False))
    return ChromaVectorStore(client, 'phase17hl_documents', 'chroma_local', administrative=True), encoder


def launch(config, digest, acknowledgement, access_token, credential, *, approval=None, approval_trust=None):
    """Live entry point. Tests intercept dependencies; command never calls this by default."""
    config = LaunchConfiguration.model_validate(config.model_dump())
    if time.time() < config.execution_not_before:
        raise SecurityError('unsupported_execution')
    root = private_path(config.audit_directory, directory=True)
    for path in (config.security_path,config.governance_path,config.admission_path):
        private_path(path)  # Must already exist; never replace shared authorities.
    if not credential or not credential.strip():
        raise SecurityError('authentication_required')
    principal = verify_approval(config, digest, acknowledgement, access_token, OIDCVerifier(config.oidc),
        approval=approval, approval_trust=approval_trust)
    authority = SecurityAuthority(config.security_path)
    authority.authorize(principal, Action.PUBLICATION_MANAGE)  # Existing registered principal only.
    ledger = GovernanceLedger(config.governance_path, config.governance_policy, config.contract.catalog,
                              provider_path=config.admission_path, provider_key=config.quota_key,
                              provider_policy=config.policy)
    admission = SQLiteInferenceAdmission(config.admission_path, config.quota_key, config.policy)
    guard = RunGuard(root/'run.sqlite', config.contract, admission)
    if guard.records():
        raise SecurityError('unsupported_execution')  # Reconciliation, never automatic replay.
    # Verify again at consumption after authority setup; no stale authentication/approval.
    verified = verify_artifact(approval, approval_trust, config, principal, digest)
    consume(verified, approval_trust, approval)
    # Keep the existing run marker as an independent guard, including legacy runs.
    fd = os.open(root/'live-started.json', os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd,'w') as stream:
        json.dump({'configuration_sha256':digest,'stage':'L1','approval_id':verified['jti'],
                   'approval_sha256':sha256(approval.encode()).hexdigest()},stream)
        stream.flush()
        os.fsync(stream.fileno())
    fsync_directory(root)
    provider = vectors = session = None
    try:
        vectors, encoder = local_retrieval(config)
        import requests
        session = requests.Session()
        session.trust_env = False
        provider = OpenAICompatibleProvider(base_url=config.endpoint,
            model_map={'summarization':DEPLOYMENT,'general':DEPLOYMENT}, api_key=credential,
            authentication_header='api-key' if config.authentication == 'api_key' else 'Authorization',
            connect_timeout=5, read_timeout=60, readiness_retries=0, http_client=session)
        runtime = Runtime(config,principal,authority,ledger,guard,provider,vectors,encoder)
        from tests.performance.foundry_preflight import execute
        result = execute(root,'L1',runtime=runtime)
        if result['job_state'] != 'COMPLETED' or result.get('questions',{}).get('status') != 'COMPLETE':
            guard.stop('evidence')
        return result
    except BaseException:
        guard.stop('provider')
        raise
    finally:
        from tests.performance.phase17h import write
        try:
            write(root/'financial-audit.json', {'run':guard.records(),'governance':ledger.usage(principal,authority)})
        finally:
            try:
                if session is not None:
                    session.close()
            finally:
                if vectors is not None:
                    vectors.close()


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--configuration', type=Path)
    parser.add_argument('--approve-sha256')
    parser.add_argument('--approval', type=Path)
    parser.add_argument('--approval-trust', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    os.umask(0o077)
    try:
        if not args.live:
            if args.output is None:
                parser.error('--output required for offline rehearsal')
            root = private_path(args.output, exists=False)
            root.mkdir(mode=0o700,parents=True,exist_ok=False)
            from unittest.mock import patch
            from tests.performance.foundry_preflight import execute
            def deny(*a,**k):
                raise RuntimeError('Network forbidden in dry run')
            with patch('socket.socket.connect',deny), patch('socket.create_connection',deny):
                result = execute(root,'L1')
        else:
            if (args.configuration is None or not args.approve_sha256
                    or args.approval is None or args.approval_trust is None):
                parser.error('Private configuration, approval, independent trust and acknowledgement required')
            config,digest = load_configuration(args.configuration)
            result = launch(config,digest,args.approve_sha256,
                os.environ.get('POLYMIND_L1_OPERATOR_TOKEN',''),os.environ.get('POLYMIND_L1_AZURE_CREDENTIAL',''),
                approval=read_private(args.approval, 16384).decode('ascii').strip(),
                approval_trust=load_trust(args.approval_trust))
        print(json.dumps({'stage':'L1','state':result['job_state'],'calls':result['calls'],
                          'questions_status':result.get('questions', {}).get('status')}))
        if (result['job_state'] != 'COMPLETED'
                or result.get('questions', {}).get('status') != 'COMPLETE'):
            parser.exit(1)
    except Exception:
        # Never render configuration, token validation data, URLs or upstream bodies.
        parser.exit(1,'L1 blocked; inspect private audit artifacts and configuration.\n')


if __name__ == '__main__':
    main()
