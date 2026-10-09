"""Compose owner/tenant reservation with the existing provider admission port."""
from uuid import uuid4

from documents.jobs.models import canonical
from llm.admission import CallIdentity
from llm.inference import InferenceConfigurationError, InferenceError
from security.models import SecurityError


class GovernedExecution:
    def __init__(self, provider, admission, ledger, authority, snapshot):
        self.provider, self.admission, self.ledger = provider, admission, ledger
        self.authority, self.snapshot = authority, snapshot

    def execute(self, request, *, identity=None, check_active=lambda: None, workload='INTERACTIVE'):
        self.authority.revalidate(self.snapshot)
        check_active()
        model = self.provider.model_id(request.role)
        if identity is None:
            identity = CallIdentity(self.snapshot.principal.scope.identity(),uuid4(),uuid4(),1,
                                    'interactive/1',self.provider.name,request.role.value,model,request.capability.version)
        if (identity.provider != self.provider.name or identity.model != model or identity.role != request.role.value
                or identity.capability != request.capability.version):
            raise InferenceConfigurationError('Governance model identity mismatch.')
        cap = request.capability
        estimate = len(canonical({'system':request.system,'data':request.data,'schema':request.schema}).encode()) + cap.overhead_tokens + cap.safety_tokens
        if (request.output_tokens <= 0 or request.output_tokens > cap.max_output_tokens
                or estimate+request.output_tokens > cap.context_tokens):
            raise InferenceConfigurationError('Governed request exceeds capability.')
        ticket = self.ledger.reserve(self.snapshot.principal,identity,estimate,request.output_tokens,workload)
        self.ledger.transition(ticket,'RESERVED','ADMITTING')  # Duplicate attempts never execute twice.
        try:
            provider_ticket = self.admission.acquire(identity,estimate,request.output_tokens,workload)
        except BaseException:
            # Provider admission cannot execute inference; no upstream work began.
            self.ledger.transition(ticket,'ADMITTING','RELEASED')
            raise
        usage, outcome, started = None, 'unknown', False
        try:
            self.authority.revalidate(self.snapshot)
            check_active()
            self.ledger.transition(ticket,'ADMITTING','STARTED')
            started = True
            result = self.provider.execute(request)
            usage, outcome = result.usage, 'success'
            return result
        except InferenceError as exc:
            usage, outcome = getattr(exc,'usage',None), exc.category
            raise
        finally:
            if started:
                self.ledger.settle(ticket,usage)
            else:
                self.ledger.transition(ticket,'ADMITTING','RELEASED')
            self.admission.finish(provider_ticket,usage=usage,outcome=outcome)


class RestrictedProvider:
    """Factory guard: unbound paid execution is unavailable in governed mode."""
    def __init__(self, provider):
        self._provider = provider
        self.name = provider.name

    def model_id(self, role):
        return self._provider.model_id(role)

    def check_readiness(self):
        return self._provider.check_readiness()

    def close(self):
        self._provider.close()

    def generate(self, *args, **kwargs):
        raise SecurityError('unsupported_execution')

    generate_stream = generate
    execute = generate

    def bind(self, admission, ledger, authority, snapshot):
        return GovernedExecution(self._provider,admission,ledger,authority,snapshot)
