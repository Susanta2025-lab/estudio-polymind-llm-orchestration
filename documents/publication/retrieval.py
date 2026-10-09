"""Read-only replica snapshots, pinned hybrid retrieval and canonical citations."""
from dataclasses import dataclass
from types import MappingProxyType
from typing import Literal
from uuid import UUID

from pydantic import Field
from rank_bm25 import BM25Okapi

from documents.digestion.codec import read
from documents.digestion.models import DigestArtifact
from documents.digestion.validation import EvidenceIndex
from documents.models import FrozenModel, Span
from documents.publication.models import PublicationError, vector_metadata
from documents.publication.planning import LIMIT
from documents.serialization import deserialize
from rag.bm25 import tokenize
from rag.hybrid_retriever import fuse_rankings
from rag.vector_store import VectorFilter


class Citation(FrozenModel):
    citation_id: str
    generation: UUID
    record_id: UUID
    document_id: UUID
    document_version_id: UUID
    extraction_id: UUID
    display_source: str = Field(max_length=512)
    physical_page: int | None = None
    span: Span
    structural_path: tuple[str, ...]
    excerpt: str = Field(max_length=4096)
    provenance: Literal['validated'] = 'validated'
    semantic_support: Literal['not_evaluated'] = 'not_evaluated'


@dataclass(frozen=True)
class PinnedRequest:
    snapshot: object
    document_ids: tuple[UUID, ...]
    authorization: object = None
    sparse_indexes: object = None


class PublicationReplica:
    def __init__(self, reader, expected_version):
        self.reader, self.expected_version = reader, str(expected_version)
        self.snapshot = None
        self.sparse_indexes = None

    def load(self):
        """Controlled startup operation only; requests/readiness never call this."""
        active = self.reader.authority.active()
        if str(active.generation) != self.expected_version:
            raise PublicationError('publication_generation_mismatch')
        manifest = self.reader.validate(active.generation)
        corpus = [tokenize(r.text) for r in manifest.records]
        index = BM25Okapi(corpus) if corpus and any(corpus) else None
        isolated = {}
        for doc in manifest.documents:
            positions = tuple(i for i,r in enumerate(manifest.records) if r.document_id == doc.document_id)
            tokens = [corpus[i] for i in positions]
            isolated[doc.document_id] = (positions, BM25Okapi(tokens) if any(tokens) else None)
        if self.reader.authority.active() != active:
            raise PublicationError('publication_generation_mismatch')
        self.snapshot = (manifest, index)
        self.sparse_indexes = MappingProxyType(isolated)

    def ready(self):
        try:
            self.pin()
            return True
        except Exception:
            return False

    def pin(self, document_ids=None, *, authorization=None):
        snapshot = self.snapshot
        active = self.reader.authority.active()
        if (snapshot is None or str(active.generation) != self.expected_version
                or snapshot[0].generation != active.generation):
            raise PublicationError('publication_generation_mismatch')
        # Detect active inventory/artifact loss. Validation never repairs or builds snapshots.
        if authorization is None:
            self.reader.validate(active.generation)
        else:
            authority, auth = authorization
            authority.revalidate(auth)
            if (not document_ids or set(document_ids) != {d for d,s,e in auth.documents}
                    or any(s != snapshot[0].scope for d,s,e in auth.documents)):
                from security.models import SecurityError
                raise SecurityError()
        available = {d.document_id for d in snapshot[0].documents}
        selected = available if document_ids is None else set(document_ids)
        if document_ids is not None and (not selected or not selected <= available):
            raise PublicationError('retrieval_scope_invalid')
        return PinnedRequest(snapshot, tuple(sorted(selected, key=str)), authorization, self.sparse_indexes)

    def validate_pin(self, pin):
        from config.settings import settings
        if pin.authorization is None:
            if settings.authentication_mode == 'oidc_jwt':
                from security.models import SecurityError
                raise SecurityError()
            return self.reader.validate(pin.snapshot[0].generation)
        authority, auth = pin.authorization
        authority.revalidate(auth)
        if (set(pin.document_ids) != {d for d,s,e in auth.documents}
                or any(s != pin.snapshot[0].scope for d,s,e in auth.documents)):
            from security.models import SecurityError
            raise SecurityError()
        return self.reader.validate(pin.snapshot[0].generation, document_ids=pin.document_ids,
                                    pinned_manifest=pin.snapshot[0])

    def retrieve(self, query, pin, *, top_k=8, reranker=None):
        manifest, index = pin.snapshot
        selected = set(pin.document_ids)
        if not selected:
            return []
        if not 1 <= top_k <= 32:
            raise PublicationError('retrieval_scope_invalid')
        # A pinned old generation may finish, but only while it remains intact.
        self.validate_pin(pin)
        scope = VectorFilter(str(manifest.generation), tuple(str(d) for d in pin.document_ids))
        by_id = {str(r.record_id): r for r in manifest.records}
        dense = []
        for match in self.reader.vectors.similarity_search(self.reader.encoder.embed(query), top_k, scope=scope):
            record = by_id.get(match.metadata.get('record_id'))
            if (record is None or record.document_id not in selected or match.document != record.text
                    or match.metadata != vector_metadata(manifest, record)):
                raise PublicationError('provenance_invalid')
            if match.distance < 1:
                dense.append({**match.metadata, 'text': match.document, 'score': max(0., 1-match.distance)})
        sparse = []
        if pin.authorization is not None:
            ranked = []
            for doc in pin.document_ids:
                positions, isolated = pin.sparse_indexes[doc]
                if isolated:
                    scores = isolated.get_scores(tokenize(query))
                    ranked.extend((positions[i], float(score)) for i,score in enumerate(scores) if score > 0)
            for i,score in sorted(ranked, key=lambda item:(-item[1],str(manifest.records[item[0]].record_id)))[:top_k]:
                record = manifest.records[i]
                sparse.append({**vector_metadata(manifest, record), 'text':record.text, 'score':score})
        elif index:
            scores = index.get_scores(tokenize(query))
            ranking = sorted((i for i,r in enumerate(manifest.records) if r.document_id in selected),
                             key=lambda i: (-scores[i], str(manifest.records[i].record_id)))
            for i in ranking[:top_k]:
                if scores[i] > 0:
                    record = manifest.records[i]
                    sparse.append({**vector_metadata(manifest, record), 'text': record.text, 'score': float(scores[i])})
        fused = fuse_rankings(dense, sparse)
        if not fused:
            return []
        if reranker is None:
            from rag.reranker import rerank
            reranker = rerank
        permitted_hits = {h['record_id'] for h in fused}
        result = reranker(query, fused, top_k=top_k)
        if (len(result) > top_k or len({h.get('record_id') for h in result}) != len(result)
                or any(h.get('record_id') not in permitted_hits for h in result)):
            raise PublicationError('provenance_invalid')
        # Reranking may change score/order only, never authority.
        for item in result:
            record = by_id.get(item.get('record_id'))
            if record is None or record.document_id not in selected or item.get('text') != record.text or any(
                    item.get(k) != v for k,v in vector_metadata(manifest, record).items()):
                raise PublicationError('provenance_invalid')
        return result

    def citations(self, pin, results):
        self.validate_pin(pin)
        manifest, _ = pin.snapshot
        by_id = {str(r.record_id): r for r in manifest.records}
        docs = {d.document_id: d for d in manifest.documents}
        indexes, citations = {}, []
        try:
            for item in results:
                r = by_id.get(item.get('record_id'))
                if (r is None or r.document_id not in pin.document_ids
                        or item.get('generation') != str(manifest.generation)
                        or item.get('text') != r.text):
                    raise PublicationError('provenance_invalid')
                d = docs[r.document_id]
                if d.document_id not in indexes:
                    artifact = deserialize(self.reader.objects.read(d.scope, d.extraction, max_bytes=LIMIT))
                    if artifact.extraction_id != d.extraction_id or artifact.document.document_id != d.document_id:
                        raise PublicationError('provenance_invalid')
                    self.reader.objects.inspect(d.scope, artifact.document.source, max_bytes=artifact.max_source_bytes)
                    indexes[d.document_id] = EvidenceIndex(artifact)
                index = indexes[d.document_id]
                excerpt = index.resolve(r.evidence)
                if excerpt != r.text:
                    raise PublicationError('provenance_invalid')
                unit, _ = index.blocks[r.evidence.block_id]
                citations.append(Citation(citation_id=f'C{len(citations)+1}', generation=manifest.generation,
                    record_id=r.record_id, document_id=d.document_id, document_version_id=d.document_version_id,
                    extraction_id=d.extraction_id, display_source=index.artifact.document.display_filename,
                    physical_page=unit.physical_page, span=r.evidence.span, structural_path=r.structural_path,
                    excerpt=excerpt))
            return tuple(citations)
        except PublicationError:
            raise
        except Exception:
            raise PublicationError('provenance_invalid') from None

    def annotations(self, pin):
        """Generated annotations remain derived; preserve both sides and qualifications."""
        self.validate_pin(pin)
        manifest, _ = pin.snapshot
        result = []
        for d in manifest.documents:
            if d.document_id in pin.document_ids:
                digest = read(self.reader.objects, d.scope, d.digest, DigestArtifact, LIMIT)
                conflicting_ids = {key for c in digest.contradictions for key in (*c.affirmed, *c.denied)}
                result.append({'document_id': str(d.document_id), 'status': digest.status,
                    'qualifications': [q.model_dump(mode='json') for q in digest.qualifications],
                    'contradictions': [c.model_dump(mode='json') for c in digest.contradictions],
                    'conflicting_findings': [f.model_dump(mode='json') for f in digest.findings
                        if f.claim_id in conflicting_ids],
                    'limitations': digest.limitations, 'open_questions': digest.open_questions})
        return result
