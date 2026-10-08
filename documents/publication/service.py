"""Administrative preparation/reconciliation and fenced logical activation."""
from io import BytesIO

from rank_bm25 import BM25Okapi

from documents.digestion.codec import decode, encode
from documents.models import stable_id
from documents.publication.models import (
    PublicationError, PublicationManifest, physical_id, vector_metadata,
)
from documents.publication.planning import LIMIT, accepted, plan_publication, records
from rag.bm25 import tokenize
from rag.vector_store import VectorFilter


class PublicationReader:
    """Read-only composition used by serving; no admin vector capability required."""
    def __init__(self, authority, objects, jobs, vectors, encoder, scope):
        self.authority, self.objects, self.jobs = authority, objects, jobs
        self.vectors, self.encoder, self.scope = vectors, encoder, scope

    def manifest(self, generation, *, compatible=True):
        try:
            ref, _, base = self.authority.candidate(generation)
            m = decode(self.objects.read(self.scope, ref, max_bytes=LIMIT), PublicationManifest, LIMIT)
            if m.base != base or m.generation != generation or m.scope != self.scope or (compatible and m.profile != self.encoder.profile):
                raise PublicationError('publication_incompatible')
            return m
        except PublicationError:
            raise
        except Exception:
            raise PublicationError('publication_validation_failed') from None

    def validate(self, generation, *, sparse=False):
        try:
            manifest = self.manifest(generation)
            expected = []
            for d in manifest.documents:
                verified, artifact, digest, plan = accepted(self.jobs, self.objects, self.scope, d.job_id)
                if verified != d:
                    raise PublicationError('provenance_invalid')
                expected.extend(records(d, artifact, digest, plan, self.encoder))
            if {r.record_id: r for r in expected} != {r.record_id: r for r in manifest.records}:
                raise PublicationError('provenance_invalid')
            inventory = self.vectors.list_documents(scope=VectorFilter(str(generation)))
            wanted = {str(r.record_id): (r.text, vector_metadata(manifest, r)) for r in manifest.records}
            actual = {r.metadata.get('record_id'): (r.document, r.metadata) for r in inventory}
            if len(inventory) != len(wanted) or actual != wanted:
                raise PublicationError('publication_validation_failed')
            # Empty generation is valid for revoking the last document.
            corpus = [tokenize(r.text) for r in manifest.records]
            if sparse and corpus and any(corpus):
                BM25Okapi(corpus)
            return manifest
        except PublicationError:
            raise
        except Exception:
            raise PublicationError('publication_validation_failed') from None


class PublicationService(PublicationReader):
    def plan(self, job_ids):
        base = self.authority.active()
        previous = self.manifest(base.generation, compatible=False) if base.generation else None
        candidate = plan_publication(self.jobs, self.objects, self.scope, job_ids, base, self.encoder, previous)
        if previous and candidate.records == previous.records and candidate.profile == previous.profile and (
                tuple(d.digest for d in candidate.documents) == tuple(d.digest for d in previous.documents)):
            self.validate(previous.generation)
            return previous  # Repeated compatible full-corpus publication is a no-op.
        if candidate.generation in self.authority.inventory():
            # Equivalent accepted inputs may have a different resumed job audit ID.
            return self.manifest(candidate.generation)
        data = encode(candidate)
        ref = self.objects.put(self.scope, 'artifact', stable_id('publication-manifest/1', str(candidate.generation)),
                               BytesIO(data), max_bytes=LIMIT)
        self.authority.register(candidate, ref)
        return candidate

    def prepare(self, generation, *, checkpoint=lambda _point: None):
        """Resume by deterministic upsert; no physical exactly-once claim."""
        manifest = self.manifest(generation)
        _, state, base = self.authority.candidate(generation)
        if state == 'ACCEPTED':
            return self.validate(generation)
        if self.authority.active() != base:
            self.authority.mark(generation, 'STALE')
            raise PublicationError('publication_stale_candidate')
        try:
            checkpoint('before_writes')
            for record in manifest.records:
                self.vectors.upsert([physical_id(generation, record.record_id)], [record.text],
                    [self.encoder.embed(record.text)], [vector_metadata(manifest, record)])
                checkpoint('after_write')
            checkpoint('after_writes')
            self.validate(generation, sparse=True)
            checkpoint('after_validation')
            self.authority.mark(generation, 'READY')
            return manifest
        except Exception:
            self.authority.mark(generation, 'FAILED', 'publication_write_failure')
            raise PublicationError('publication_write_failure') from None

    def activate(self, generation, *, checkpoint=lambda _point: None):
        self.validate(generation, sparse=True)
        _, _, base = self.authority.candidate(generation)
        checkpoint('before_activation')
        result = self.authority.activate(generation, base)
        checkpoint('after_activation')
        return result

    def revoke(self, document_ids, *, checkpoint=lambda _point: None):
        active = self.authority.active()
        if active.generation is None:
            raise PublicationError('retrieval_scope_invalid')
        current = self.manifest(active.generation)
        selected = set(document_ids)
        if not selected or not selected <= {d.document_id for d in current.documents}:
            raise PublicationError('retrieval_scope_invalid')
        candidate = self.plan([d.job_id for d in current.documents if d.document_id not in selected])
        self.prepare(candidate.generation, checkpoint=checkpoint)
        return self.activate(candidate.generation, checkpoint=checkpoint)

    def rollback(self, generation, expected, *, checkpoint=lambda _point: None):
        self.validate(generation, sparse=True)
        checkpoint('before_activation')
        result = self.authority.activate(generation, expected, rollback=True)
        checkpoint('after_activation')
        return result

    def reconcile(self):
        """Diagnostic only. Inactive physical rows need no deletion for correctness."""
        known = self.authority.inventory()
        physical = {r.metadata.get('generation') for r in self.vectors.list_documents()}
        active = self.authority.active()
        if active.generation:
            self.validate(active.generation)
        return {'orphan_generations': tuple(sorted(g for g in physical if g not in {str(k) for k in known})),
                'inactive_generations': tuple(str(k) for k in known if k != active.generation)}
