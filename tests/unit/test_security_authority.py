import time
from io import BytesIO
from uuid import uuid4
from concurrent.futures import ThreadPoolExecutor
import threading

import pytest

from documents.extraction import extract
from documents.storage import LocalObjectStore
from security.authority import SecurityAuthority
from security.models import Action, SecurityError, _verified_principal


@pytest.fixture
def secured(tmp_path):
    authority=SecurityAuthority(tmp_path/'security.sqlite')
    def person(subject,tenant='a',permissions=frozenset()):
        p=_verified_principal('https://issuer.invalid',subject,tenant,permissions,expires=int(time.time())+3600)
        authority.register(p)
        return p
    a,b,c=person('alice'),person('bob'),person('carol','b')
    op=person('operator',permissions=frozenset({Action.PUBLICATION_MANAGE,Action.TENANT_ADMIN}))
    op_b=person('operator','b',frozenset({Action.PUBLICATION_MANAGE}))
    docs=[]
    for p,operator in ((a,op),(b,op),(c,op_b)):
        artifact,_=extract(BytesIO(b'Synthetic evidence\n'),scope=p.scope,document_id=uuid4(),
            display_filename='synthetic.txt',declared_mime='text/plain',store=LocalObjectStore(tmp_path/'objects'))
        authority.register_document(operator,artifact.document)
        docs.append(artifact.document)
    return authority,(a,b,c,op),docs


def test_isolation_sharing_and_tombstone_matrix(secured):
    authority,(a,b,c,op),(x,y,z)=secured
    authority.authorize(a,Action.DOCUMENT_READ,x.document_id)
    for person,doc in ((a,y),(a,z),(b,x),(c,x)):
        with pytest.raises(SecurityError): authority.snapshot(person,(doc.document_id,))
    gid=authority.share(a,x.document_id,b.scope.owner)
    assert authority.share(a,x.document_id,b.scope.owner)==gid
    snapshot=authority.snapshot(b,(x.document_id,))
    for action in (Action.DOCUMENT_DELETE,Action.DOCUMENT_SHARE):
        with pytest.raises(SecurityError): authority.authorize(b,action,x.document_id)
    with pytest.raises(SecurityError): authority.share(b,x.document_id,c.scope.owner)
    with pytest.raises(SecurityError): authority.share(a,x.document_id,c.scope.owner)
    with pytest.raises(SecurityError): authority.share(a,x.document_id,uuid4())
    authority.share(a,x.document_id,b.scope.owner,revoke=True)
    with pytest.raises(SecurityError): authority.revalidate(snapshot)
    with pytest.raises(SecurityError): authority.snapshot(b,(x.document_id,))
    assert authority.tombstone(a,x.document_id)=='TOMBSTONED'
    assert authority.tombstone(a,x.document_id)=='TOMBSTONED'
    with pytest.raises(SecurityError): authority.snapshot(a,(x.document_id,))
    with pytest.raises(SecurityError): authority.register_document(op,x)
    assert authority.track_purge(op,x.document_id)['state']=='PURGE_PENDING'
    reopened=SecurityAuthority(authority.path)
    assert reopened.track_purge(op,x.document_id)['state']=='PURGE_PENDING'
    with pytest.raises(SecurityError): reopened.snapshot(a,(x.document_id,))
    reopened.snapshot(b,(y.document_id,))
    with reopened.transaction() as db:
        assert db.execute("SELECT COUNT(*) FROM audit WHERE action='TOMBSTONED'").fetchone()[0]==1


def test_denial_unknown_action_missing_owner_and_admin(secured):
    auth,(a,b,c,op),docs=secured
    for action in ('DOCUMENT_READ','UNKNOWN',Action.PUBLICATION_MANAGE,Action.TENANT_ADMIN):
        with pytest.raises(SecurityError): auth.authorize(a,action,docs[0].document_id)
    auth.authorize(op,Action.PUBLICATION_MANAGE)
    with pytest.raises(SecurityError): auth.authorize(a,Action.DOCUMENT_READ,uuid4())
    with pytest.raises(SecurityError): auth.authorize(a,Action.USAGE_READ,b.scope)
    with pytest.raises(SecurityError): auth.track_purge(c,docs[0].document_id)


def test_epoch_revalidation_after_controlled_inflight_revoke(secured):
    authority,(a,b,c,op),(x,y,z)=secured
    authority.share(a,x.document_id,b.scope.owner)
    retrieved,finish=threading.Event(),threading.Event()
    released=[]
    def request():
        snap=authority.snapshot(b,(x.document_id,))
        retrieved.set()
        assert finish.wait(5)
        with authority.release(snap): released.append('protected output')
    with ThreadPoolExecutor(1) as pool:
        future=pool.submit(request)
        assert retrieved.wait(5)
        authority.share(a,x.document_id,b.scope.owner,revoke=True)
        finish.set()
        with pytest.raises(SecurityError): future.result(5)
    assert released==[]


def test_audit_capacity_failure_rolls_back_mutation(secured):
    authority,(a,b,c,op),(x,y,z)=secured
    authority.audit_limit=1
    with pytest.raises(SecurityError): authority.share(a,x.document_id,b.scope.owner)
    with authority.transaction() as db:
        assert db.execute('SELECT COUNT(*) FROM grants').fetchone()[0]==0


def test_database_paths_symlinks_and_permissions(tmp_path):
    target=tmp_path/'db'
    SecurityAuthority(target)
    assert target.stat().st_mode & 0o777 == 0o600
    link=tmp_path/'link';link.symlink_to(target)
    with pytest.raises(SecurityError): SecurityAuthority(link)
    target.chmod(0o644)
    with pytest.raises(SecurityError): SecurityAuthority(target)


def test_scoped_file_and_redis_memory(secured,tmp_path):
    from security.memory import ScopedMemory
    from memory.memory_store import FileMemoryStore,RedisMemoryStore
    from tests.unit.test_memory_store import FakeRedis
    authority,people,docs=secured
    for store in (FileMemoryStore(str(tmp_path/'memory.json'),10),RedisMemoryStore(FakeRedis(),10)):
        store.append_exchange('session-123','legacy','private legacy answer')
        facades=[ScopedMemory(store,authority,p) for p in people[:3]]
        for i,f in enumerate(facades):
            assert f.get_history('session-123')==[]
            f.append_exchange('session-123',str(i),f'answer {i}')
        for i,f in enumerate(facades):
            history=f.get_history('session-123')
            assert history[0]['content']==str(i)
            assert all('session_id' not in m for m in history)
        facades[0].clear_session('session-123')
        assert facades[0].get_history('session-123')==[]
        assert len(facades[1].get_history('session-123'))==2
        assert store.get_history('session-123')[0]['content']=='legacy'


def test_disabled_principal_blocks_reads_writes_and_token_reregistration(secured,tmp_path):
    from security.memory import ScopedMemory
    from memory.memory_store import FileMemoryStore
    authority,(a,b,c,op),docs=secured
    memory=ScopedMemory(FileMemoryStore(str(tmp_path/'history.json'),6),authority,a)
    memory.append_exchange('session','question','answer')
    authority.disable_principal(op,a.scope.owner)
    for fn in (lambda:memory.get_history('session'),lambda:memory.append_exchange('session','q','a'),
               lambda:memory.clear_session('session'),lambda:authority.register(a)):
        with pytest.raises(SecurityError):fn()


def test_mixed_owner_selections_rejected_before_publication_lookup(secured):
    from security.services import AuthorizedAnalysis
    from documents.publication.analysis import AnalysisRequest
    authority,(a,b,c,op),(x,y,z)=secured
    authority.share(a,x.document_id,b.scope.owner)
    service=AuthorizedAnalysis(authority,None,None,{})
    with pytest.raises(SecurityError,match='mixed_owners'):
        service.analyze(b,AnalysisRequest(query='q',document_ids=(x.document_id,y.document_id)))


def test_missing_and_foreign_documents_have_identical_denials(secured):
    authority, (alice, bob, carol, operator), (own, foreign, cross_tenant) = secured
    errors = []
    for document_id in (uuid4(), foreign.document_id, cross_tenant.document_id):
        with pytest.raises(SecurityError) as error:
            authority.snapshot(alice, (document_id,))
        errors.append((error.value.category, str(error.value)))
    assert errors == [('access_denied', 'access_denied')] * 3
