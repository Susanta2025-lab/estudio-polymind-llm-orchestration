"""Private governed Chat/Documents assembly with explicit execution authority.

Historical SessionApproval records guarantee zero_paid_execution=True. Only a
distinct execution approval plus independent permission can authorize execution.
"""
import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, model_validator

from config.settings import Settings
from documents.digestion.managed import ManagedSettings
from documents.digestion.models import DigestionProfile
from documents.jobs.models import JobSettings
from documents.jobs.sqlite import SQLiteJobLedger
from documents.models import Scope, stable_id
from documents.operator.actions import Actions
from documents.operator.service import LocalRunner, OperatorWorkflow
from documents.pilot import SessionApproval, SourceApproval, SupervisedPilot
from documents.pilot.models import PilotError, ExecutionSessionApproval
from documents.publication.authority import SQLitePublicationAuthority
from documents.publication.encoding import RetrievalEncoder
from documents.publication.models import RetrievalProfile
from documents.publication.service import PublicationService
from documents.storage import LocalObjectStore
from llm.provider_factory import _create_inference_provider
from llm.inference import ModelRole
from llm.structured import CapabilityProfile
from security.identity import OIDCSettings
from security.runtime import SecurityRuntime
from deployment.phase19.storage import DATABASES, private_path, local_filesystem


from security.chat import ChatPolicy


class RuntimeManifest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    version: str = 'phase19-runtime/1'
    enrollment: tuple[str, str, str]
    sources: tuple[SourceApproval, ...] = Field(min_length=1)
    approvals: tuple[SessionApproval | ExecutionSessionApproval, ...] = ()
    execution_permissions: bool = False
    execution_authority_root: str = '/run/secrets/execution-authority'
    chat: ChatPolicy | None = None
    managed: ManagedSettings
    analysis: CapabilityProfile
    planning: DigestionProfile

    @model_validator(mode='after')
    def valid(self):
        if self.version != 'phase19-runtime/1' or not all(self.enrollment):
            raise ValueError('Runtime manifest unavailable')
        if len({s.approval_id for s in self.sources}) != len(self.sources):
            raise ValueError('Duplicate source approval')
        return self


def configuration(root):
    local_filesystem(root, durable=True)
    path = private_path(root / 'configuration.json', directory=False)
    values = json.loads(path.read_text())
    required = {'DEPLOYMENT_ENV', 'API_AUTH_MODE', 'OIDC_CONFIGURATION',
        'GOVERNANCE_ENABLED', 'GOVERNANCE_POLICY', 'GOVERNANCE_PRICING', 'GOVERNANCE_PROVIDER_POLICY',
        'GOVERNANCE_PROVIDER_KEY', 'INFERENCE_PROVIDER', 'OPENAI_COMPATIBLE_BASE_URL',
        'OPENAI_COMPATIBLE_MODEL_MAP', 'OPENAI_COMPATIBLE_API_KEY_FILE'}
    if not required <= values.keys():
        raise ValueError('Explicit production configuration required')
    # Ignore inherited environment/dotenv. All settings for this process are
    # explicit in the private reviewed configuration, including defaults.
    values = {**Settings.model_construct().model_dump(), **values}
    cfg = Settings(_env_file=None, **values)
    oidc = OIDCSettings.model_validate(cfg.OIDC_CONFIGURATION)
    if (cfg.DEPLOYMENT_ENV != 'production' or cfg.authentication_mode != 'oidc_jwt'
            or oidc.token_profile != 'entra_v2' or not cfg.GOVERNANCE_ENABLED
            or cfg.OPENAI_COMPATIBLE_API_KEY is not None
            or not cfg.OPENAI_COMPATIBLE_API_KEY_FILE):
        raise ValueError('Production identity, authority and mounted provider credential required')
    from urllib.parse import urlsplit
    endpoint = urlsplit(cfg.OPENAI_COMPATIBLE_BASE_URL)
    if (endpoint.scheme != 'https' or endpoint.username or endpoint.password or endpoint.query
            or endpoint.fragment or not endpoint.path.rstrip('/').endswith('/v1')):
        raise ValueError('HTTPS v1 inference endpoint required')
    expected = [str(root / 'private' / n) for n in DATABASES[:3]]
    if [cfg.SECURITY_AUTHORITY_PATH, cfg.GOVERNANCE_AUTHORITY_PATH, cfg.GOVERNANCE_PROVIDER_PATH] != expected:
        raise ValueError('Stable authority paths required')
    return cfg


def deny_external_execution(*args, **kwargs):
    raise PilotError('pilot_not_ready')


def build(root, *, initialize=False):
    root = Path(root)
    cfg = configuration(root)
    manifest = RuntimeManifest.model_validate_json(private_path(root / 'manifest.json', directory=False).read_text())
    issuer, tenant, subject = manifest.enrollment
    oidc = OIDCSettings.model_validate(cfg.OIDC_CONFIGURATION)
    scope = Scope(tenant=stable_id('polymind-identity/1/tenant', issuer, tenant),
                  owner=stable_id('polymind-identity/1/owner', issuer, tenant, subject))
    if issuer != oidc.issuer or tenant != oidc.tenant_id or any(s.owner != scope for s in manifest.sources):
        raise ValueError('Enrollment/source binding unavailable')
    catalog = {}
    for source in manifest.sources:
        data = private_path(root / 'sources' / source.sha256, directory=False).read_bytes()
        from hashlib import sha256
        if len(data) > 1_000_000 or sha256(data).hexdigest() != source.sha256:
            raise ValueError('Source integrity unavailable')
        catalog[source.approval_id] = data
    if (not manifest.managed.capability.usage_reporting or not manifest.analysis.usage_reporting
            or manifest.managed.capability.schema_profile != 'azure-strict/1'):
        raise ValueError('Explicit usage and strict schema capabilities required')
    from governance.ledger import PricingCatalog
    catalog_prices = PricingCatalog.model_validate(cfg.GOVERNANCE_PRICING)
    for role in ('general', 'summarization'):
        catalog_prices.price('openai_compatible', cfg.OPENAI_COMPATIBLE_MODEL_MAP[role])
    runtime = SecurityRuntime(cfg)
    provider = _create_inference_provider(cfg)
    vectors = None
    try:
        from rag.vector_store_factory import create_publication_vector_store
        from config.model_artifacts import validate_model_artifacts
        validate_model_artifacts(cfg.MODEL_ARTIFACT_DIR)
        from sentence_transformers import SentenceTransformer, CrossEncoder
        from config.model_artifacts import EMBEDDING_MODEL, RERANKER_MODEL, model_source
        model = SentenceTransformer(model_source(EMBEDDING_MODEL, cfg.MODEL_ARTIFACT_DIR),
                                    local_files_only=True, device='cpu')
        ranking = CrossEncoder(model_source(RERANKER_MODEL, cfg.MODEL_ARTIFACT_DIR),
                               local_files_only=True, device='cpu')

        def rerank(query, docs, top_k):
            if not docs:
                return []
            scores = ranking.predict([(query, d['text']) for d in docs])
            return [dict(d, rerank_score=float(score)) for d, score in
                    sorted(zip(docs, scores), key=lambda item: float(item[1]), reverse=True)][:top_k]
        vectors = create_publication_vector_store(cfg, administrative=True)
        private = root / 'private'
        objects = LocalObjectStore(private / 'objects')
        jobs = SQLiteJobLedger(JobSettings(database_path=private / 'jobs.sqlite', lease_seconds=120))
        publication = PublicationService(SQLitePublicationAuthority(private / 'publication.sqlite'), objects,
                                         jobs, vectors, RetrievalEncoder(RetrievalProfile(), model), scope)
        pilot = SupervisedPilot(control_path=private / 'pilot.sqlite', authority=runtime.authority,
            objects=objects, jobs=jobs, governance=runtime.governance, admission=runtime.admission,
            provider=provider, managed_settings=manifest.managed, analysis_capability=manifest.analysis,
            planning_profile=manifest.planning, publication=publication, sources=manifest.sources,
            reranker=rerank, execution_permission=deny_external_execution, initialize=initialize)
        actions = Actions(private / 'actions.sqlite', initialize=initialize)
        permissions = None
        if manifest.execution_permissions:
            from security.execution import ExecutionPermissions, DocumentsExecutionPermission
            def binding():
                # Includes sources, session IDs, caps, endpoint/alias/header and exact
                # authority paths/policies/catalog. Never contains secret bytes.
                return {'configuration': cfg.model_dump(mode='json'), 'manifest':manifest.model_dump(mode='json'),
                        'models':{r:provider.model_id(ModelRole(r))
                                  for r in cfg.OPENAI_COMPATIBLE_MODEL_MAP},
                        'financial':runtime.governance.policy.model_dump(mode='json'),
                        'catalog':runtime.governance.catalog.model_dump(mode='json'),
                        'admission':runtime.admission.policy.model_dump(mode='json'),
                        'profiles': {'managed':pilot.managed_settings.model_dump(mode='json'),
                                     'analysis':pilot.analysis_capability.model_dump(mode='json'),
                                     'planning':pilot.planning_profile.model_dump(mode='json')},
                        'dispatch_url':provider.url,
                        'chat_policy':runner.chat.policy.model_dump(mode='json') if runner.chat is not None else None}
            authority_root = Path(manifest.execution_authority_root)
            permissions = ExecutionPermissions(authority_root, authority_root / 'trust.json', actions,
                                               runtime.authority, binding, ledger=runtime.governance)
            pilot.execution_permission = DocumentsExecutionPermission(permissions)
        workflow = OperatorWorkflow(pilot, actions, manifest.enrollment, catalog, manifest.approvals,
                                    synthetic=False, execution_enabled=permissions is not None)
        def admission_ready():
            # The pilot forecasts serial worst-case calls at 61-second spacing.
            # Wait without claiming a step/permission or reserving finances.
            # Actual shared admission still performs the authoritative check.
            with runtime.admission._transaction() as db:
                rows = list(db.execute('SELECT started,active FROM inference_calls WHERE quota=?',
                                       (runtime.admission.quota_key,)))
            return not any(r['active'] for r in rows) and (
                not rows or runtime.admission.clock() >= max(r['started'] for r in rows) + 61)
        runner = LocalRunner(workflow, admission_ready=admission_ready)
        chat = None
        if manifest.chat is not None:
            if permissions is None:
                raise ValueError('Chat requires independent execution permissions')
            from memory.provider_factory import create_memory_store
            from security.chat import AuthorizedChat
            memory = create_memory_store(cfg)
            chat = AuthorizedChat(runtime, provider, memory, publication, rerank, permissions,
                                  manifest.chat, manifest.enrollment, sources=manifest.sources)
        runner.chat = chat
    except BaseException:
        provider.close()
        if vectors is not None:
            vectors.close()
        raise

    def cleanup():
        try:
            provider.close()
        finally:
            vectors.close()
            if runner.chat is not None:
                runner.chat.memory.close()
    return runtime, workflow, runner, cleanup
