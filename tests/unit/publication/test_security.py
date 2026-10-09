from concurrent.futures import ThreadPoolExecutor
import json
import threading
import time
from uuid import UUID

import pytest

from documents.publication.analysis import AnalysisRequest, DocumentAnalysis
from documents.publication.retrieval import PublicationReplica
from documents.serialization import deserialize
from governance.ledger import GovernanceLedger
from llm.admission import AdmissionPolicy, SQLiteInferenceAdmission
from llm.inference import InferenceUsage
from llm.structured import CapabilityProfile, GenerationResult
from security.authority import SecurityAuthority
from security.models import Action, SecurityError, _verified_principal
from security.services import AuthorizedAnalysis
from tests.unit.test_governance import configuration


@pytest.fixture
def secure_publication(env,tmp_path,monkeypatch):
    service,document=env
    auth=SecurityAuthority(tmp_path/'security.sqlite')
    def person(subject,tenant='a',permissions=frozenset()):
        p=_verified_principal('issuer',subject,tenant,permissions,expires=int(time.time())+3600)
        auth.register(p);return p
    a,b,c=person('alice'),person('bob'),person('carol','b')
    op=person('operator',permissions=frozenset({Action.PUBLICATION_MANAGE}))
    monkeypatch.setitem(document.__globals__,'SCOPE',a.scope)
    service.scope=a.scope
    jobs=[document('alpha protected evidence\nbeta condition\ngamma explanation\n',identity=3),
          document('private unrelated evidence\n',identity=4)]
    m=service.plan(jobs);service.prepare(m.generation);service.activate(m.generation)
    for d in m.documents:
        artifact=deserialize(service.objects.read(d.scope,d.extraction,max_bytes=16000000))
        auth.register_document(op,artifact.document)
    replica=PublicationReplica(service,m.generation);replica.load()
    class Provider:
        name='fake'
        def __init__(self):self.calls=[];self.pause=None
        def model_id(self,role):return 'model'
        def execute(self,request):
            self.calls.append(request)
            if self.pause:self.pause()
            return GenerationResult(json.dumps({'answer':'protected answer','evidence_status':'available','citation_ids':['C1']}),
                                    InferenceUsage(100,10,110),'model')
    provider=Provider()
    cap=CapabilityProfile(version='test/1',context_tokens=100000,max_output_tokens=2048,overhead_tokens=0,safety_tokens=0)
    analysis=DocumentAnalysis(replica,provider,cap,reranker=lambda q,docs,top_k:docs[:top_k])
    gov=GovernanceLedger(tmp_path/'governance.sqlite',*configuration('1000000'))
    admission=SQLiteInferenceAdmission(tmp_path/'provider.sqlite','test',AdmissionPolicy(rpm=100,tpm=1000000,concurrent=10,
        interactive_rpm=50,interactive_tpm=500000,interactive_slots=5,per_job_rpm=10))
    secured=AuthorizedAnalysis(auth,gov,admission,{a.scope.identity():analysis})
    return secured,auth,(a,b,c,op),service,analysis,provider


def test_real_analysis_denies_before_search_or_provider_and_shared_owner_resolution(secure_publication,monkeypatch):
    secured,auth,(a,b,c,op),service,analysis,provider=secure_publication
    original=service.vectors.similarity_search
    searched=[]
    def search(embedding,limit,*,scope):
        searched.append(scope)
        return original(embedding,limit,scope=scope)
    monkeypatch.setattr(service.vectors,'similarity_search',search)
    request=AnalysisRequest(query='alpha',document_ids=(UUID(int=3),))
    for p in (b,c):
        with pytest.raises(SecurityError):secured.analyze(p,request)
    assert not searched and not provider.calls
    auth.share(a,UUID(int=3),b.scope.owner)
    result,snapshot=secured.analyze(b,request)
    assert snapshot.documents[0][1]==a.scope
    assert result['citations'][0]['document_id']==str(UUID(int=3))
    assert all(s.document_ids==(str(UUID(int=3)),) for s in searched)
    assert 'private unrelated' not in provider.calls[0].data
    # The legacy whole-corpus BM25 cannot be used by authorized requests.
    analysis.replica.snapshot[1].get_scores=lambda q:(_ for _ in ()).throw(AssertionError('unscoped BM25'))
    secured.analyze(b,request)
    auth.share(a,UUID(int=3),b.scope.owner,revoke=True)
    calls=len(provider.calls);searches=len(searched)
    with pytest.raises(SecurityError):secured.analyze(b,request)
    assert (len(provider.calls),len(searched))==(calls,searches)


@pytest.mark.parametrize('mutation',['revoke','tombstone'])
def test_provider_paused_then_revocation_blocks_answer_and_keeps_usage(secure_publication,mutation):
    secured,auth,(a,b,c,op),service,analysis,provider=secure_publication
    auth.share(a,UUID(int=3),b.scope.owner)
    entered,finish=threading.Event(),threading.Event()
    def pause():
        entered.set();assert finish.wait(10)
    provider.pause=pause
    with ThreadPoolExecutor(1) as pool:
        future=pool.submit(secured.analyze,b,AnalysisRequest(query='alpha',document_ids=(UUID(int=3),)))
        assert entered.wait(10)
        if mutation=='revoke':auth.share(a,UUID(int=3),b.scope.owner,revoke=True)
        else:auth.tombstone(a,UUID(int=3))
        finish.set()
        with pytest.raises(SecurityError):future.result(10)
    rows=secured.ledger.usage(b,auth)
    assert len(rows)==1 and rows[0]['state']=='SETTLED' and rows[0]['actual_input']==100


def test_rollback_never_restores_revoked_or_tombstoned_access(secure_publication):
    secured,auth,(a,b,c,op),service,analysis,provider=secure_publication
    g1=service.authority.active()
    auth.share(a,UUID(int=3),b.scope.owner)
    g2=service.revoke([UUID(int=3)])
    auth.share(a,UUID(int=3),b.scope.owner,revoke=True)
    auth.tombstone(a,UUID(int=3))
    service.rollback(g1.generation,g2)
    analysis.replica=PublicationReplica(service,g1.generation);analysis.replica.load()
    for p in (a,b,c):
        with pytest.raises(SecurityError):secured.analyze(p,AnalysisRequest(query='alpha',document_ids=(UUID(int=3),)))
    assert not provider.calls
    assert auth.track_purge(op,UUID(int=3))['state']=='PURGE_PENDING'
    # Untombstoned document remains readable and physical inventory is preserved.
    result,_=secured.analyze(a,AnalysisRequest(query='private',document_ids=(UUID(int=4),)))
    assert result['citations']


def test_job_ownership_and_publication_administration(secure_publication,monkeypatch):
    from documents.jobs.service import DocumentJobs
    from security.services import AuthorizedJobs,AuthorizedPublication
    from config.settings import settings
    secured,auth,(a,b,c,op),service,analysis,provider=secure_publication
    jobs=AuthorizedJobs(auth,DocumentJobs(service.jobs,service.objects))
    manifest=analysis.replica.snapshot[0]
    job_id=manifest.documents[0].job_id
    assert jobs.get(a,job_id).admission.scope==a.scope
    for person in (b,c):
        with pytest.raises(SecurityError):jobs.get(person,job_id)
        with pytest.raises(SecurityError):jobs.cancel(person,job_id)
    monkeypatch.setattr(settings,'API_AUTH_MODE','oidc_jwt')
    with pytest.raises(SecurityError):service.rollback(manifest.generation,service.authority.active())
    admin=AuthorizedPublication(auth,service)
    with pytest.raises(SecurityError):admin.run(a,'reconcile')
    assert 'inactive_generations' in admin.run(op,'reconcile')


def test_authorized_reranker_cannot_insert_unselected_record(secure_publication):
    from documents.publication.models import PublicationError
    from documents.publication.retrieval import vector_metadata
    secured, auth, (alice, bob, carol, operator), service, analysis, provider = secure_publication
    auth.share(alice, UUID(int=3), bob.scope.owner)
    manifest = analysis.replica.snapshot[0]
    foreign = next(record for record in manifest.records if record.document_id == UUID(int=4))
    analysis.reranker = lambda query, docs, top_k: [
        {**vector_metadata(manifest, foreign), 'text': foreign.text}]
    with pytest.raises(PublicationError, match='provenance_invalid'):
        secured.analyze(bob, AnalysisRequest(query='alpha', document_ids=(UUID(int=3),)))
    assert not provider.calls
