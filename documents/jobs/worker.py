"""Injected execution and local dispatch. Neither memory nor messages own state.

StepHandler is the future subprocess/sandbox boundary. The in-process reference
runner cannot preempt arbitrary parser code or impose hard CPU/RSS/time limits.
"""

from collections import deque
from io import BytesIO
import hashlib
from typing import Callable, Protocol

from documents.errors import DocumentError
from documents.extraction import extract
from documents.models import ObjectRef, stable_id
from documents.parser import NativePdfRunner, ParserRunner
from documents.storage import ObjectStore
from documents.jobs.errors import Failure, JobError, classify
from documents.jobs.ledger import JobLedger
from documents.jobs.models import Dispatch, Job, Lease, Step, fingerprint


class WorkDispatcher(Protocol):
    def send(self, message: Dispatch) -> None: ...
    def receive(self) -> Dispatch | None: ...
    def acknowledge(self, message: Dispatch) -> None: ...


class LocalDispatcher:
    """Deterministic at-least-once fixture; restart recovery comes from the ledger."""
    def __init__(self):
        self.messages = deque()

    def send(self, message):
        self.messages.append(message)

    def receive(self):
        return self.messages[0] if self.messages else None

    def acknowledge(self, message):
        if self.messages and self.messages[0] == message:
            self.messages.popleft()


def relay(ledger: JobLedger, dispatcher: WorkDispatcher, limit: int = 100) -> int:
    count = 0
    for message in ledger.pending_dispatch(limit):
        try:
            dispatcher.send(message)
        except Exception:
            raise JobError('dispatch_error') from None
        # If this fails after send, the next relay repeats the message safely.
        ledger.mark_delivered(message)
        count += 1
    return count


class IntentStore:
    """Register the expected immutable reference BEFORE invoking the object write.

    An interrupted write may never exist physically. Intents are conservative
    retention candidates, not assertions that bytes exist. No delete/list port.
    """
    def __init__(self, store: ObjectStore, ledger: JobLedger, lease: Lease):
        self.store, self.ledger, self.lease = store, ledger, lease

    def put(self, scope, kind, object_id, stream, *, max_bytes, expected_sha256=None):
        if scope != self.lease.scope:
            raise JobError('scope_mismatch')
        chunks, count = [], 0
        while chunk := stream.read(min(65536, max_bytes - count + 1)):
            count += len(chunk)
            if count > max_bytes:
                raise DocumentError('source_too_large')
            chunks.append(chunk)
        data = b''.join(chunks)
        digest = hashlib.sha256(data).hexdigest()
        if expected_sha256 is not None and expected_sha256 != digest:
            raise DocumentError('integrity_error')
        ref = ObjectRef(scope=scope, kind=kind, object_id=object_id,
                        key=stable_id(scope.identity(), kind, str(object_id)),
                        sha256=digest, byte_size=len(data))
        self.ledger.register_object(self.lease, ref)
        written = self.store.put(scope, kind, object_id, BytesIO(data), max_bytes=max_bytes,
                                 expected_sha256=digest)
        if written != ref:
            raise DocumentError('integrity_error')
        return written

    def read(self, scope, ref, *, max_bytes):
        if scope != self.lease.scope:
            raise JobError('scope_mismatch')
        return self.store.read(scope, ref, max_bytes=max_bytes)

    def inspect(self, scope, ref, *, max_bytes):
        if scope != self.lease.scope:
            raise JobError('scope_mismatch')
        return self.store.inspect(scope, ref, max_bytes=max_bytes)


class StepHandler(Protocol):
    def __call__(self, job: Job, step: Step, store: ObjectStore) -> tuple[ObjectRef, ...]: ...


class ExtractionHandler:
    def __init__(self, runner: ParserRunner | None = None):
        self.runner = runner or NativePdfRunner()

    def __call__(self, job, step, store):
        request = job.admission
        profile = request.profile
        actual = 'utf8-strict/1' if request.mime == 'text/plain' else self.runner.version
        if (step.spec.stage != 'EXTRACTING' or profile.parser_version != actual
                or step.spec.schema_version != profile.artifact_schema
                or step.spec.config_fingerprint != fingerprint({})):
            raise JobError('profile_mismatch')
        data = store.read(request.scope, request.source, max_bytes=profile.max_source_bytes)
        artifact, ref = extract(
            BytesIO(data), scope=request.scope, document_id=request.document_id,
            display_filename=request.display_filename, declared_mime=request.mime,
            store=store, limits=profile.limits(), created_at=job.document_created_at,
            extracted_at=step.execution_at, expected_sha256=request.source.sha256,
            structure_required=profile.structure_required, runner=self.runner,
        )
        if artifact.document.source != request.source:
            raise DocumentError('integrity_error')
        return (ref,)


class Worker:
    def __init__(self, ledger: JobLedger, dispatcher: WorkDispatcher, store: ObjectStore,
                 handler: StepHandler, *, owner: str,
                 classifier: Callable[[Exception], Failure] = classify):
        self.ledger, self.dispatcher, self.store = ledger, dispatcher, store
        self.handler, self.owner, self.classifier = handler, owner, classifier

    def once(self) -> bool:
        try:
            message = self.dispatcher.receive()
        except Exception:
            raise JobError('dispatch_error') from None
        if message is None:
            return False
        lease = self.ledger.claim(message.scope, message.job_id, message.step_id, self.owner)
        if lease is not None:
            job = self.ledger.get_job(message.scope, message.job_id)
            step = next(s for s in self.ledger.steps(message.scope, message.job_id) if s.step_id == message.step_id)
            tracked = IntentStore(self.store, self.ledger, lease)
            try:
                manifest = self.handler(job, step, tracked)
                for ref in manifest:
                    tracked.inspect(message.scope, ref, max_bytes=job.admission.profile.max_artifact_bytes)
            except Exception as exc:
                try:
                    self.ledger.fail(lease, self.classifier(exc))
                except JobError as error:
                    self._settle_or_raise(lease, error)
            else:
                try:
                    self.ledger.commit(lease, manifest)
                except JobError as error:
                    self._settle_or_raise(lease, error)
        try:
            self.dispatcher.acknowledge(message)
        except Exception:
            raise JobError('dispatch_error') from None
        return True

    def _settle_or_raise(self, lease, error):
        if error.category == 'cancelled':
            try:
                self.ledger.settle_cancel(lease)
            except JobError as settling:
                if settling.category not in ('stale_fence', 'invalid_transition'):
                    raise
        elif error.category not in ('stale_fence', 'lease_expired', 'invalid_transition'):
            # Ledger outage/manifest conflict is not a handler retry classification.
            # Leave delivery unacknowledged; durable expiry/reconciliation recovers.
            raise error
