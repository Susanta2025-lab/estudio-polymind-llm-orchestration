"""Trusted-scope service entry point. Scope is not authentication."""

from uuid import UUID

from documents.errors import DocumentError
from documents.jobs.errors import JobError
from documents.jobs.ledger import JobLedger
from documents.jobs.models import Admission
from documents.models import Scope
from documents.storage import ObjectStore


class DocumentJobs:
    def __init__(self, ledger: JobLedger, store: ObjectStore):
        self.ledger, self.store = ledger, store

    def admit(self, request: Admission):
        try:
            request = Admission.model_validate(request.model_dump(mode='json'))
        except Exception:
            raise JobError('invalid_configuration') from None
        # Object verification is outside the database transaction; bytes are
        # immutable. The ledger adapter accepts verified references from services.
        verified = self.store.inspect(request.scope, request.source,
                                      max_bytes=request.profile.max_source_bytes)
        if verified != request.source:
            raise DocumentError('integrity_error')
        if request.resume_from:
            prior = self.ledger.get_job(request.scope, request.resume_from)
            if prior.admission.compatibility() == request.compatibility():
                old_steps = {step.spec.unit_id: step for step in self.ledger.steps(request.scope, prior.job_id)}
                reusable = set()
                for spec in request.steps:
                    old = old_steps.get(spec.unit_id)
                    if (old and old.state == 'SUCCEEDED' and old.spec == spec
                            and set(spec.depends_on).issubset(reusable)):
                        for ref in old.manifest:
                            if self.store.inspect(request.scope, ref, max_bytes=request.profile.max_artifact_bytes) != ref:
                                raise DocumentError('integrity_error')
                        reusable.add(spec.unit_id)
        return self.ledger.admit(request)

    def get(self, scope: Scope, job_id: UUID):
        return self.ledger.get_job(scope, job_id)

    def cancel(self, scope: Scope, job_id: UUID):
        return self.ledger.cancel(scope, job_id)
