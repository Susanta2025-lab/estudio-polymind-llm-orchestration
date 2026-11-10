"""Additive v10 proposal evidence in the existing fenced step manifest.

Commit order: settled provider call -> immutable raw record -> decode/G2/G1 ->
checkpoint -> receipt -> atomic ledger manifest. Uncommitted objects are orphans,
never resumable inference authority. Recovery verifies, never calls a provider.
"""

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Literal
from uuid import UUID

from pydantic import Field, StrictInt

from documents.digestion.codec import read
from documents.digestion.models import DigestionError
from documents.digestion.wire import DECODER, VERSION, construct, references
from documents.jobs.models import fingerprint
from documents.models import Digest, FrozenModel, ObjectRef


def generation_hash(generation):
    value = asdict(generation)
    value["capability"] = generation.capability.model_dump(mode="json")
    value["role"] = generation.role.value
    return fingerprint(value)


def audit_hash(generation):
    """Same request digest as the existing Foundry raw provider recorder."""
    return sha256(
        json.dumps(
            {
                "system": generation.system,
                "data": generation.data,
                "schema": generation.schema,
                "output": generation.output_tokens,
            },
            sort_keys=True,
        ).encode()
    ).hexdigest()


@dataclass(frozen=True)
class ProposedResult:
    canonical: bytes
    proposal: ObjectRef


class ProposalRecord(FrozenModel):
    schema_version: Literal["stage-provider-record/1"] = "stage-provider-record/1"
    wire_version: Literal["stage-proposal/1"] = VERSION
    decoder_version: Literal["stage-decoder/1"] = DECODER
    plan: ObjectRef
    job_id: UUID
    step_id: UUID
    attempt: StrictInt = Field(gt=0)
    fence: StrictInt = Field(gt=0)
    request_sha256: Digest
    table_sha256: Digest
    generation_sha256: Digest
    audit_request_sha256: Digest
    config_sha256: Digest
    raw_sha256: Digest
    # Exact generated content, including whitespace; upstream HTTP bodies remain
    # in the existing transport/audit boundary. No credentials or headers here.
    raw: str


class DecodingReceipt(FrozenModel):
    schema_version: Literal["stage-decoding-receipt/1"] = "stage-decoding-receipt/1"
    wire_version: Literal["stage-proposal/1"] = VERSION
    decoder_version: Literal["stage-decoder/1"] = DECODER
    proposal: ObjectRef
    checkpoint: ObjectRef
    request_sha256: Digest
    table_sha256: Digest
    canonical_sha256: Digest
    generation_sha256: Digest
    audit_request_sha256: Digest


def verify(
    ledger,
    store,
    job,
    step,
    plan_ref,
    request,
    checkpoint_ref,
    checkpoint,
    *,
    committed=True,
):
    """Reopen a committed association; authoritative scope comes from the job."""
    if len(step.manifest) != 3 or step.manifest[0] != checkpoint_ref:
        raise DigestionError("incompatible_checkpoint")
    scope = job.admission.scope
    limit = job.admission.profile.max_artifact_bytes
    receipt = read(store, scope, step.manifest[1], DecodingReceipt, limit)
    record = read(store, scope, step.manifest[2], ProposalRecord, limit)
    table = references(request)
    raw = record.raw.encode("utf-8")
    # Follow ledger-owned reuse edges, including repeated resumes. Every hop
    # must retain the identical committed association and authenticated scope.
    source, source_job = step, job
    seen = set()
    from documents.jobs.errors import JobError

    try:
        while source.reused_from is not None:
            prior = source_job.admission.resume_from
            if prior is None or prior in seen:
                raise DigestionError("incompatible_checkpoint")
            seen.add(prior)
            source_job = ledger.get_job(scope, prior)
            source = next(
                (
                    s
                    for s in ledger.steps(scope, prior)
                    if s.step_id == source.reused_from
                ),
                None,
            )
            if (
                source is None
                or source.state != "SUCCEEDED"
                or source.manifest != step.manifest
            ):
                raise DigestionError("incompatible_checkpoint")
    except JobError:
        raise DigestionError("incompatible_checkpoint") from None
    if (
        receipt.proposal != step.manifest[2]
        or receipt.checkpoint != checkpoint_ref
        or record.plan != plan_ref
        or record.step_id != source.step_id
        or record.job_id != source_job.job_id
        or record.attempt != source.attempt_count
        or record.fence != source.fence
        or record.config_sha256 != request.profile.inference_config
        or record.request_sha256 != table.request_sha256
        or receipt.request_sha256 != table.request_sha256
        or record.table_sha256 != table.digest
        or receipt.table_sha256 != table.digest
        or receipt.generation_sha256 != record.generation_sha256
        or receipt.audit_request_sha256 != record.audit_request_sha256
        or record.raw_sha256 != sha256(raw).hexdigest()
    ):
        raise DigestionError("incompatible_checkpoint")
    try:
        attempts = ledger.attempts(scope, record.job_id, record.step_id)
    except JobError:
        raise DigestionError("incompatible_checkpoint") from None
    if not any(
        a.number == record.attempt
        and a.fence == record.fence
        and a.outcome == ("SUCCEEDED" if committed else "RUNNING")
        for a in attempts
    ):
        raise DigestionError("incompatible_checkpoint")
    if not committed and (
        record.fence != step.fence or record.attempt != step.attempt_count
    ):
        raise DigestionError("incompatible_checkpoint")
    canonical = construct(raw, request, table)
    from documents.digestion.codec import encode

    if sha256(canonical).hexdigest() != receipt.canonical_sha256 or canonical != encode(
        checkpoint.result
    ):
        raise DigestionError("incompatible_checkpoint")
