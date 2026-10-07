"""Neutral structured interface and deterministic, nonsemantic local fake."""

from collections import Counter
from typing import Protocol
from uuid import UUID

from documents.jobs.errors import JobError
from documents.jobs.models import fingerprint
from documents.models import FrozenModel, stable_id
from documents.digestion.codec import encode
from documents.digestion.models import (
    Claim, ClaimLink, DigestionError, Qualification, StageRequest, StageResult, Text,
)
from documents.digestion.planning import check_request


class SynthesisInference(Protocol):
    def analyze(self, request: StageRequest) -> bytes: ...


class Fixture(FrozenModel):
    block_id: UUID
    text: Text
    qualification: Text | None = None
    subject: str | None = None
    stance: str = 'unknown'


class FakeInference:
    """Fixtures are operator inputs, never commands parsed from source text.

    Failure counters simulate calls only; Phase 17C owns all actual retry decisions.
    Recreating this object with no faults produces identical successful bytes.
    """
    def __init__(self, fixtures=(), *, fail_first=(), fail_always=(), unavailable=()):
        self.fixtures = tuple(fixtures)
        self.config = fingerprint([f.model_dump(mode='json') for f in self.fixtures])
        self.by_block = {f.block_id: f for f in self.fixtures}
        if len(self.by_block) != len(self.fixtures):
            raise DigestionError('inference_contract_error')
        self.fail_first, self.fail_always = set(fail_first), set(fail_always)
        self.unavailable = set(unavailable)
        self.calls = Counter()

    def analyze(self, request):
        check_request(request)
        if request.profile.inference_config != self.config:
            raise DigestionError('incompatible_checkpoint')
        key = request.stage_id
        self.calls[key] += 1
        if key in self.fail_first and self.calls[key] == 1:
            raise JobError('worker_interrupted')
        if key in self.fail_always:
            raise DigestionError('analysis_failed' if request.stage == 'analysis' else 'reducer_failed')
        if key in self.unavailable and request.stage == 'analysis':
            return encode(StageResult(stage_id=key, kind=request.stage, outcome='unavailable', claims=(),
                                      limitations=('Synthetic analysis unavailable.',)))
        claims = []
        if request.stage == 'analysis':
            fixtures = [p for p in request.source_data if p.evidence.block_id in self.by_block]
            ordinary = [p for p in request.source_data if p.evidence.block_id not in self.by_block]
            for piece in fixtures:
                fixture = self.by_block[piece.evidence.block_id]
                evidence = (piece.evidence_id(),)
                claims.append(Claim(claim_id=stable_id(str(key), str(len(claims))), originating_stage=key, text=fixture.text,
                                    kind='fact', evidence_ids=evidence, subject=fixture.subject,
                                    stance=fixture.stance, qualifications=(Qualification(
                                        text=fixture.qualification, evidence_ids=evidence),) if fixture.qualification else ()))
            if ordinary:
                claims.append(Claim(claim_id=stable_id(str(key), str(len(claims))), originating_stage=key,
                                    text='Synthetic source observation; no semantic quality asserted.',
                                    kind='fact', evidence_ids=tuple(p.evidence_id() for p in ordinary)))
        else:
            links = tuple(ClaimLink(stage_id=child.result.stage_id, claim_id=c.claim_id)
                          for child in request.children for c in child.result.claims)
            if links:
                claims.append(Claim(claim_id=stable_id(str(key), '0'), originating_stage=key, kind='commentary',
                                    text='Inherited findings; all linked qualifications and unresolved conflicts apply.',
                                    lineage=links))
        limitations = tuple(sorted({p.limitation for p in request.source_data if p.limitation != 'none'}))
        return encode(StageResult(stage_id=key, kind=request.stage, claims=tuple(claims), limitations=limitations))
