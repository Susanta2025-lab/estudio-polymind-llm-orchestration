from uuid import UUID
import pytest
from pydantic import ValidationError
from documents.publication.models import PublicationManifest, PublicationError, RetrievalProfile
from documents.publication.planning import accepted
from documents.digestion.validation import EvidenceIndex


def test_deterministic_complete_immutable_manifest_and_records(env):
    service, document = env
    job = document()
    first = service.plan([job])
    assert service.plan([job]) == first
    assert len(first.records) == 3
    assert all(r.classification == 'ORIGINAL' for r in first.records)
    with pytest.raises(ValidationError):
        first.policy = 'PARTIAL'
    with pytest.raises(ValidationError):
        PublicationManifest.model_validate({**first.model_dump(), 'schema_version': 'publication/2'})


def test_span_splitting_no_loss_or_truncation(env):
    service, document = env
    text = 'alpha ' * 100 + '\n'
    job = document(text)
    manifest = service.plan([job])
    assert ''.join(r.text for r in manifest.records) == text
    assert len(manifest.records) > 1
    _, artifact, _, _ = accepted(service.jobs, service.objects, service.scope, job)
    for record in manifest.records:
        assert EvidenceIndex(artifact).resolve(record.evidence) == record.text
        assert service.encoder.count(record.text) <= 240
    with pytest.raises(PublicationError, match='embedding_limit'):
        service.encoder.embed(text)


def test_profile_change_invalidates_identity(env):
    service, document = env
    job = document()
    first = service.plan([job])
    from documents.publication.encoding import RetrievalEncoder
    service.encoder = RetrievalEncoder(RetrievalProfile(version='source-retrieval/2'), service.encoder.model)
    second = service.plan([job])
    assert first.generation != second.generation
    assert first.records[0].record_id != second.records[0].record_id


def test_corrupt_digest_and_missing_manifest_rejected(env):
    service, document = env
    with pytest.raises(PublicationError, match='publication_invalid_input'):
        service.plan([UUID(int=999)])
    job = document()
    manifest = service.plan([job])
    (service.objects.root/str(manifest.documents[0].digest.key)).write_bytes(b'corrupt')
    with pytest.raises(PublicationError, match='publication_invalid_input'):
        service.plan([job])


def test_complete_only_policy_and_cancelled_inputs(env):
    service, document = env
    job = document()
    # Persisted quality status cannot be overridden by COMPLETED workflow state.
    manifest = service.plan([job])
    assert manifest.policy == 'COMPLETE_ONLY'
    with pytest.raises(ValidationError):
        PublicationManifest.model_validate({**manifest.model_dump(), 'policy':'ALLOW_PARTIAL'})
    # Input admission with no accepted final manifest is rejected independently of state.
    old = service.jobs.get_job(service.scope,job)
    from documents.jobs.models import Admission
    from documents.jobs.service import DocumentJobs
    pending = DocumentJobs(service.jobs, service.objects).admit(old.admission.model_copy(update={
        'request_idempotency_key':'cancelled-publication-input'}))
    service.jobs.cancel(service.scope,pending.job_id)
    with pytest.raises(PublicationError,match='publication_invalid_input'):
        service.plan([pending.job_id])


def test_wrong_version_extraction_and_derived_forgery_rejected(env):
    service, document = env
    m = service.plan([document()])
    r = m.records[0]
    for changes in [{'extraction_id':UUID(int=99)}, {'document_version_id':UUID(int=99)},
                    {'classification':'DERIVED'}, {'material':'DERIVED_DOCUMENT_SUMMARY'}]:
        with pytest.raises(ValidationError):
            type(r).model_validate({**r.model_dump(), **changes})


def test_reprofile_active_corpus_creates_new_generation(env):
    from documents.publication.encoding import RetrievalEncoder
    service, document = env
    job = document(); first = service.plan([job])
    service.prepare(first.generation); service.activate(first.generation)
    service.encoder = RetrievalEncoder(RetrievalProfile(version='source-retrieval/2'),service.encoder.model)
    second = service.plan([job]); service.prepare(second.generation); service.activate(second.generation)
    assert second.generation != first.generation
    with pytest.raises(PublicationError,match='publication_incompatible'):
        service.rollback(first.generation, service.authority.active())


@pytest.mark.parametrize('quality',['PARTIAL','FAILED'])
def test_partial_failed_digest_never_published(env,quality):
    from documents.digestion.inference import FakeInference
    from documents.digestion.codec import encode
    from documents.digestion.models import StageResult, DigestionError
    class Unavailable(FakeInference):
        def analyze(self,request):
            if request.stage == 'analysis' and request.source_data[0].text.startswith('unavailable'):
                if quality == 'FAILED':
                    raise DigestionError('analysis_failed')
                return encode(StageResult(stage_id=request.stage_id,kind='analysis',outcome='unavailable',
                                          claims=(),limitations=('Synthetic unavailable source.',)))
            return super().analyze(request)
    service, document = env
    job = document('unavailable portion\n' + 'alpha evidence\n'*10, inference=Unavailable(),
                   profile_changes={'allow_partial':True,'minimum_coverage':.1,'max_failed_units':5,'chunk_characters':20})
    if quality == 'PARTIAL':
        from documents.digestion.workflow import load_digest
        assert load_digest(service.jobs,service.objects,service.scope,job).status == 'PARTIAL'
    else:
        assert service.jobs.get_job(service.scope,job).state == 'FAILED'
    with pytest.raises(PublicationError,match='publication_invalid_input'):
        service.plan([job])
