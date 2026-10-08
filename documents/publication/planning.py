"""Consume accepted final manifests and independently validate their source graph."""
from bisect import bisect_left

from documents.digestion.codec import read
from documents.digestion.models import DigestArtifact, Plan
from documents.digestion.validation import EvidenceIndex
from documents.digestion.workflow import DigestionHandler, load_digest
from documents.models import EvidenceRef, Span
from documents.serialization import deserialize
from documents.publication.models import AcceptedDocument, PublicationError, record_values, manifest_values

LIMIT = 32_000_000


class VerifyOnlyStore:
    """Recompute final 17D output without writing objects during verification."""
    def __init__(self, store):
        self.store = store
        self.produced = []
    def read(self, *args, **kwargs):
        return self.store.read(*args, **kwargs)
    def inspect(self, *args, **kwargs):
        return self.store.inspect(*args, **kwargs)
    def put(self, scope, kind, object_id, stream, *, max_bytes, **kwargs):
        from hashlib import sha256
        from documents.models import ObjectRef, stable_id
        data = stream.read(max_bytes + 1)
        if len(data) > max_bytes:
            raise PublicationError('publication_invalid_input')
        ref = ObjectRef(scope=scope, kind=kind, object_id=object_id,
                        key=stable_id(scope.identity(), kind, str(object_id)),
                        sha256=sha256(data).hexdigest(), byte_size=len(data))
        self.produced.append(data)
        return ref


def accepted(ledger, store, scope, job_id):
    try:
        job = ledger.get_job(scope, job_id)
        if job.state != 'COMPLETED' or job.cancel_requested:
            raise PublicationError('publication_invalid_input')
        digest = load_digest(ledger, store, scope, job_id)
        if digest.status != 'COMPLETE':
            raise PublicationError('publication_invalid_input')
        limit = job.admission.profile.max_artifact_bytes
        if limit > LIMIT:
            raise PublicationError('publication_invalid_input')
        plan = read(store, scope, digest.plan, Plan, limit)
        final = next(s for s in ledger.steps(scope, job_id) if s.spec.unit_id == 'digest')
        # Reuses the actual 17D DAG/evidence/coverage validator, without inference or writes.
        handler = DigestionHandler(ledger, digest.plan, None)
        verification = VerifyOnlyStore(store)
        handler(job, final, verification)
        # 17D retains checkpoint/qualification sets in execution iteration order.
        # Revalidation must tolerate that order across interpreter hash seeds.
        from documents.digestion.codec import decode
        from documents.digestion.models import Coverage
        rebuilt = decode(verification.produced[0], DigestArtifact, limit)
        def normalized(value):
            payload = value.model_dump(mode='json')
            from documents.jobs.models import canonical
            for name in ('checkpoints', 'qualifications'):
                payload[name] = sorted(payload[name], key=canonical)
            return payload
        if normalized(rebuilt) != normalized(digest) or read(
                store, scope, final.manifest[1], Coverage, limit) != digest.coverage:
            raise PublicationError('publication_invalid_input')
        artifact = deserialize(store.read(scope, digest.extraction, max_bytes=limit), max_bytes=limit)
        store.inspect(scope, artifact.document.source, max_bytes=artifact.max_source_bytes)
        d = AcceptedDocument(scope=scope, job_id=job_id, document_id=artifact.document.document_id,
            document_version_id=artifact.document.document_version_id, extraction_id=artifact.extraction_id,
            extraction=digest.extraction, digest=final.manifest[0])
        return d, artifact, digest, plan
    except PublicationError:
        raise
    except Exception:
        raise PublicationError('publication_invalid_input') from None


def records(document, artifact, digest, plan, encoder):
    index = EvidenceIndex(artifact)
    included = set(digest.coverage.included)
    owners = {bid: u.path for u in plan.structure.units for bid in u.block_ids}
    result = []
    for unit in artifact.units:
        lines = index.lines.get(unit.source_id)
        for block in unit.blocks:
            if block.block_id not in included:
                continue
            for start, end, text in encoder.split(block.source_text):
                start, end = start + block.span.start, end + block.span.start
                line = None if lines is None else 1 + bisect_left(lines, start)
                span = Span(start=start, end=end, line_start=line,
                            line_end=None if line is None else line + text.rstrip('\n').count('\n'))
                evidence = EvidenceRef(scope=document.scope, document_version_id=document.document_version_id,
                    extraction_id=document.extraction_id, source_id=unit.source_id, block_id=block.block_id, span=span)
                if index.resolve(evidence) != text:
                    raise PublicationError('provenance_invalid')
                result.append(record_values(document_id=document.document_id,
                    document_version_id=document.document_version_id, extraction_id=document.extraction_id,
                    text=text, evidence=evidence, structural_path=owners.get(block.block_id, ()),
                    source_kind=block.kind, profile=encoder.profile.digest(),
                    limitation='uninterpreted_visual' if block.kind in ('table', 'figure') else 'none'))
    return tuple(result)


def plan_publication(ledger, store, scope, job_ids, base, encoder, previous=None):
    docs, rows = [], []
    for key in sorted(set(job_ids), key=str):
        doc, artifact, digest, plan = accepted(ledger, store, scope, key)
        docs.append(doc)
        rows.extend(records(doc, artifact, digest, plan, encoder))
    docs.sort(key=lambda d: str(d.document_id))
    rows.sort(key=lambda r: str(r.document_id))  # Stable sort retains canonical reading order.
    removed = () if previous is None else tuple(sorted(
        {d.document_version_id for d in previous.documents} - {d.document_version_id for d in docs}, key=str))
    return manifest_values(scope=scope, base=base, profile=encoder.profile, documents=tuple(docs),
                           records=tuple(rows), removed_versions=removed)
