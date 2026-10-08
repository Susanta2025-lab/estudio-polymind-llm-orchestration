from datetime import datetime, timezone
from io import BytesIO
from uuid import UUID

import numpy as np
import pytest

from documents.extraction import extract
from documents.storage import LocalObjectStore
from documents.models import Scope
from documents.jobs.models import JobSettings
from documents.jobs.sqlite import SQLiteJobLedger
from documents.jobs.worker import LocalDispatcher, Worker, relay
from documents.digestion.inference import FakeInference
from documents.digestion.models import DigestionProfile
from documents.digestion.workflow import prepare, admit, DigestionHandler, classify_digestion
from documents.publication.authority import SQLitePublicationAuthority
from documents.publication.encoding import RetrievalEncoder
from documents.publication.models import RetrievalProfile
from documents.publication.service import PublicationService
from rag.vector_store import VectorDocument, VectorMatch

SCOPE = Scope(tenant=UUID(int=1), owner=UUID(int=2))


class Model:
    max_seq_length = 256
    class Tokenizer:
        model_max_length = 512
        def __call__(self, text, **kwargs):
            assert kwargs['truncation'] is False
            return {'input_ids': [0] * (len(text) + 2)}
    tokenizer = Tokenizer()
    def get_sentence_embedding_dimension(self):
        return 384
    def encode(self, text, **kwargs):
        return np.array([1.] + [0.] * 383)


class Vectors:
    def __init__(self):
        self.rows = {}
    def upsert(self, ids, documents, embeddings, metadatas):
        for key, text, meta in zip(ids, documents, metadatas):
            self.rows[key] = VectorDocument(text, meta)
    def list_documents(self, *, scope=None):
        return [r for r in self.rows.values() if scope is None or (
            r.metadata['generation'] == scope.generation and
            (not scope.document_ids or r.metadata['document_id'] in scope.document_ids))]
    def similarity_search(self, embedding, limit, *, scope=None):
        return [VectorMatch(r.document, r.metadata, .1) for r in self.list_documents(scope=scope)[:limit]]


@pytest.fixture
def env(tmp_path):
    objects = LocalObjectStore(tmp_path/'objects')
    jobs = SQLiteJobLedger(JobSettings(database_path=tmp_path/'jobs.sqlite'))
    authority = SQLitePublicationAuthority(tmp_path/'publication.sqlite')
    vectors = Vectors()
    encoder = RetrievalEncoder(RetrievalProfile(), Model())
    service = PublicationService(authority, objects, jobs, vectors, encoder, SCOPE)
    def document(text='alpha evidence\nbeta qualification\ngamma opposition\n', identity=3, inference=None, pdf=None, profile_changes=None):
        now = datetime(2026,10,8,tzinfo=timezone.utc)
        artifact, ref = extract(BytesIO(pdf if pdf is not None else text.encode()), scope=SCOPE, document_id=UUID(int=identity),
            display_filename='synthetic.pdf' if pdf else 'synthetic.txt', declared_mime='application/pdf' if pdf else 'text/plain', store=objects,
            created_at=now, extracted_at=now)
        profile = DigestionProfile(context_tokens=30000, reserved_output_tokens=3000, template_tokens=64,
            chunk_characters=100, max_fan_in=4, max_result_characters=3000, max_claims=4,
            max_claim_characters=256, max_annotations=8, max_source_units=5000, max_chunks=800,
            max_steps=1000, max_artifact_bytes=16000000, max_depth=32, minimum_coverage=1, max_failed_units=0)
        if callable(inference):
            inference = inference(artifact)
        if inference is not None:
            profile = profile.model_copy(update={'inference_config': inference.config})
        if profile_changes:
            profile = profile.model_copy(update=profile_changes)
        plan, plan_ref = prepare(artifact, ref, profile, objects)
        job = admit(jobs, objects, plan, plan_ref, request_key=str(plan_ref.object_id))
        queue = LocalDispatcher()
        worker = Worker(jobs, queue, objects, DigestionHandler(jobs, plan_ref, inference or FakeInference()),
                        owner='synthetic', classifier=classify_digestion)
        for _ in range(1000):
            relay(jobs, queue)
            if not worker.once():
                break
        return job.job_id
    return service, document
