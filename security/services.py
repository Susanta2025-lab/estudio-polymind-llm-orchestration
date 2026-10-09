"""Explicit authorized composition over existing application ports."""
from security.models import Action, SecurityError


class AuthorizedAnalysis:
    def __init__(self, authority, ledger, admission, publications):
        # Keys are canonical owning Scope identities supplied by the operator.
        self.authority, self.ledger, self.admission = authority, ledger, admission
        self.publications = dict(publications)

    def analyze(self, principal, request):
        snapshot = self.authority.snapshot(principal,request.document_ids)
        scopes = {s.identity() for d,s,e in snapshot.documents}
        if len(scopes) != 1:
            raise SecurityError('mixed_owners')
        service = self.publications.get(next(iter(scopes)))
        if service is None or service.replica.reader.scope.identity() not in scopes:
            raise SecurityError('security_unavailable')
        from governance.execution import GovernedExecution, RestrictedProvider
        provider = service.provider
        executor = (provider.bind(self.admission,self.ledger,self.authority,snapshot)
                    if isinstance(provider,RestrictedProvider)
                    else GovernedExecution(provider,self.admission,self.ledger,self.authority,snapshot))
        result = service.analyze(request,authorization=(self.authority,snapshot),executor=executor)
        self.authority.revalidate(snapshot)
        return result,snapshot

    def ready(self):
        return (self.authority.ready() and self.ledger.ready() and bool(self.publications)
                and all(s.replica.ready() for s in self.publications.values()))


class AuthorizedJobs:
    def __init__(self, authority, jobs):
        self.authority,self.jobs=authority,jobs

    def get(self, principal, job_id):
        self.authority.snapshot(principal)
        # The existing ledger enforces scope in SQL; callers cannot override it.
        from documents.jobs.errors import JobError
        try:
            job=self.jobs.get(principal.scope,job_id)
        except JobError:
            raise SecurityError() from None
        self.authority.authorize(principal,Action.DOCUMENT_READ,job.admission.document_id)
        return job

    def cancel(self, principal, job_id):
        job=self.get(principal,job_id)
        snapshot=self.authority.snapshot(principal,(job.admission.document_id,),Action.DOCUMENT_DELETE)
        with self.authority.release(snapshot):
            return self.jobs.cancel(principal.scope,job_id)


class AuthorizedPublication:
    def __init__(self, authority, service):
        self.authority,self.service=authority,service

    def run(self, principal, operation, *args, **kwargs):
        if operation not in {'plan','prepare','activate','rollback','revoke','reconcile'}:
            raise SecurityError()
        self.authority.authorize(principal,Action.PUBLICATION_MANAGE)
        if principal.scope.tenant != self.service.scope.tenant:
            raise SecurityError()
        return getattr(self.service,operation)(*args,authorization=(self.authority,principal),**kwargs)
