"""Preparation only for the separately approved, single-analysis Azure probe.

There is deliberately no live entry point. Review material is not an approval;
fresh verified identity, an execution implementation bound into configuration,
and the existing operator-controlled RSA workflow are still required.
"""
from hashlib import sha256
from io import BytesIO
import json
from uuid import UUID, uuid4

from documents.config import ExtractionSettings
from documents.digestion.managed import (
    ManagedSettings, ManagedSynthesisInference, StageProfile, generation_schema,
)
from documents.digestion.validation import EvidenceIndex
from documents.digestion.workflow import DigestionHandler, prepare
from documents.extraction import extract
from documents.storage import LocalObjectStore
from llm.azure_schema import provider_schema
from tests.performance.fixtures import NOW, pdf, profile
from tests.performance.foundry_budget import Contract
from tests.performance.foundry_l1 import generation_contract_digest
from tests.performance.foundry_recalibration import DEPLOYMENT, candidate_capability

GENERATION = '6f936342efb8e22faf23d59ebf71f7846d3255692d398c27d1e6a449ef41e247'
SCHEMA = '4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2'
CATALOG = 'dad37bc0f349cdfbea16e25cae028a0b5042e4e3e3daac4f141f9b566c5bc65e'


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def verified_schema():
    schema = provider_schema(generation_schema())
    if generation_contract_digest() != GENERATION or digest(schema) != SCHEMA:
        raise ValueError('Authorized generation contract changed; operator review required')
    return schema


def one_call_contract(previous, catalog):
    """Narrow the reviewed financial contract; never expand an old authorization."""
    if (catalog.version != 'phase17hl-pricing-eur-202610/1'
            or sha256(catalog.model_dump_json().encode()).hexdigest() != CATALOG):
        raise ValueError('Reviewed pricing catalog changed')
    values = dict(previous, catalog=catalog.model_dump(mode='json'), attempts=1,
                  input_tokens=25000, output_tokens=3000, total_input=25000,
                  total_output=3000, context=28000, rpm=1)
    contract = Contract.model_validate(values)
    if (contract.provider != 'openai_compatible' or contract.model != DEPLOYMENT
            or contract.tier != 'GlobalStandard' or contract.fixed_cost != 0
            or contract.extra_cost != 0 or not contract.fits(1) or contract.fits(2)):
        raise ValueError('Incompatible one-call financial contract')
    return contract


class PreparationProvider:
    """Model identity for rendering only; cannot send a request."""
    name = 'openai_compatible'

    def model_id(self, role):
        return DEPLOYMENT

    def execute(self, request):
        raise RuntimeError('Preparation cannot perform inference')


def prepare_stage(root, scope):
    """Use the same extraction, planning, evidence IDs and managed prompt as L1."""
    schema = verified_schema()
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
    plan, plan_ref = prepare(artifact, ref, chosen, store)
    if len(plan.chunks) != 1 or len(artifact.units) != 4:
        raise ValueError('Unexpected fixture composition')
    request = DigestionHandler.request(plan, plan.chunks[0].chunk_id, {}, {})
    index = EvidenceIndex(artifact)
    if any(index.resolve(p.evidence) != p.text for p in request.source_data):
        raise ValueError('Source evidence mismatch')
    generation, estimate = adapter.render(request)
    if estimate > 25000:
        raise ValueError('Input reservation exceeded')
    return dict(version='polymind-schema-probe-preparation/1',
        status='BLOCKED_OPERATOR_AUTHENTICATION_AND_SIGNING', executable=False,
        experiment_id=str(uuid4()), job_id=str(uuid4()), request_id=str(uuid4()),
        generation_contract_sha256=GENERATION, provider_schema_sha256=SCHEMA,
        response_format=dict(type='json_schema', json_schema=dict(
            name='polymind_stage_result', strict=True, schema=schema)),
        fixture=manifest, source_artifact_sha256=ref.sha256, plan_sha256=plan_ref.sha256,
        first_stage=request.model_dump(mode='json'),
        managed_settings=settings.model_dump(mode='json'), managed_fingerprint=adapter.config,
        rendered_request_sha256=digest(dict(system=generation.system, data=generation.data,
                                           schema=generation.schema)),
        estimated_input_tokens=estimate,
        limits=dict(calls=1, input_tokens=25000, output_tokens=3000, context_tokens=28000,
                    response_utf8_bytes=10000, canonical_ascii_bytes=10000,
                    http_envelope_bytes=26192, retries=0, fallback=None),
        execution_scope='first_managed_analysis_only',
        fresh_identity_verified=False, approval_created=False, provider_calls=0)
