"""Controlled concurrent access/revocation against one shared local authority."""
from concurrent.futures import ThreadPoolExecutor
import threading
from uuid import UUID

import pytest

from documents.publication.analysis import AnalysisRequest
from security.authority import SecurityAuthority
from security.models import SecurityError
from test_security import secure_publication


@pytest.mark.parametrize('mutation',['revoke','tombstone'])
def test_concurrent_owner_shared_and_cross_tenant_with_fresh_revoker(secure_publication,mutation):
    secured,auth,(a,b,c,op),service,analysis,provider=secure_publication
    auth.share(a,UUID(int=3),b.scope.owner)
    entered=threading.Barrier(3,timeout=10);finish=threading.Event()
    def pause():
        entered.wait();assert finish.wait(10)
    provider.pause=pause
    request=AnalysisRequest(query='alpha',document_ids=(UUID(int=3),))
    def foreign():
        with pytest.raises(SecurityError):secured.analyze(c,request)
    with ThreadPoolExecutor(3) as pool:
        owned=pool.submit(secured.analyze,a,request)
        shared=pool.submit(secured.analyze,b,request)
        denied=pool.submit(foreign)
        try:
            entered.wait();denied.result(10)
            revoker=SecurityAuthority(auth.path)
            if mutation=='revoke':revoker.share(a,UUID(int=3),b.scope.owner,revoke=True)
            else:revoker.tombstone(a,UUID(int=3))
        finally:finish.set()
        # Epoch changes conservatively invalidate even an owner's old snapshot.
        with pytest.raises(SecurityError):owned.result(10)
        with pytest.raises(SecurityError):shared.result(10)
    assert len(provider.calls)==2
    assert len(secured.ledger.usage(a,auth))==len(secured.ledger.usage(b,auth))==1
    assert secured.ledger.usage(c,auth)==[]
    assert all(secured.ledger.usage(p,auth)[0]['actual_input']==100 for p in (a,b))
    provider.pause=None
    result,_=secured.analyze(a,AnalysisRequest(query='private',document_ids=(UUID(int=4),)))
    assert result['citations']
