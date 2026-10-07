"""Digestion adapter for the unchanged Phase 17C fixed-plan durable worker.

NORMALIZING is the existing computational stage; units/schemas identify analysis
and reduction. VALIDATING is the coverage/finalization stage. Workflow COMPLETED
means every step committed; digest COMPLETE/PARTIAL is a separate quality contract.
"""

from uuid import UUID

from documents.errors import DocumentError
from documents.jobs.errors import classify
from documents.jobs.models import Admission, ProcessingProfile, StepSpec, fingerprint
from documents.jobs.service import DocumentJobs
from documents.serialization import deserialize
from documents.digestion.codec import encode, put, read
from documents.digestion.models import (
    AnalysisChunk, Checkpoint, ChildInput, DigestArtifact, DigestionError, Plan, StageRequest,
)
from documents.digestion.planning import build_plan
from documents.digestion.validation import EvidenceIndex, inherited_summary, make_digest, validate_result


def classify_digestion(error):
    # Reuse the existing sanitized taxonomy and retry engine without altering 17C.
    mapping = {'evidence_validation_failed': 'invalid_reference',
               'synthesis_limit_exceeded': 'extraction_limit_exceeded',
               'incompatible_checkpoint': 'profile_mismatch',
               'inference_contract_error': 'serialization_error',
               'structural_planning_failed': 'invalid_document'}
    if isinstance(error, DigestionError):
        return classify(DocumentError(mapping.get(error.category, 'extraction_failed')))
    return classify(error)


def specs(plan, plan_ref):
    digest = fingerprint(plan.model_dump(mode='json'))
    anchor = f'plan/{plan_ref.object_id}'
    steps = [StepSpec(unit_id=anchor, stage='NORMALIZING', schema_version=plan.schema_version,
                      config_fingerprint=digest)]
    steps.extend(StepSpec(unit_id=str(chunk.chunk_id), stage='NORMALIZING',
                          schema_version='stage-result/1', config_fingerprint=digest, depends_on=(anchor,))
                 for chunk in plan.chunks)
    steps.extend(StepSpec(unit_id=str(node.stage_id), stage='NORMALIZING', schema_version='stage-result/1',
                          config_fingerprint=digest, depends_on=tuple(str(key) for key in node.children))
                 for node in plan.reducers)
    steps.append(StepSpec(unit_id='digest', stage='VALIDATING', schema_version='document-digest/1',
                          config_fingerprint=digest, depends_on=(str(plan.root_id),)))
    return tuple(steps)


def prepare(artifact, extraction_ref, profile, store):
    plan = build_plan(artifact, extraction_ref, profile)
    ref = put(store, artifact.document.scope, plan, profile.max_artifact_bytes)
    return plan, ref


def admit(ledger, store, plan, plan_ref, *, request_key, resume_from=None, retry=None):
    scope = plan.structure.extraction.scope
    restored = read(store, scope, plan_ref, Plan, plan.profile.max_artifact_bytes)
    if restored != plan:
        raise DigestionError('incompatible_checkpoint')
    artifact = deserialize(store.read(scope, plan.structure.extraction, max_bytes=plan.profile.max_artifact_bytes),
                           max_bytes=plan.profile.max_artifact_bytes)
    # Plan/model_copy tampering cannot bypass deterministic complete-DAG construction.
    if build_plan(artifact, plan.structure.extraction, plan.profile) != plan:
        raise DigestionError('incompatible_checkpoint')
    doc = artifact.document
    values = dict(version=plan.profile.version, parser_version=artifact.parser_version,
                  max_source_bytes=artifact.max_source_bytes, max_pages=artifact.max_pages,
                  max_characters=artifact.max_characters, max_blocks=artifact.max_blocks,
                  max_artifact_bytes=plan.profile.max_artifact_bytes, structure_required=artifact.structure_required)
    if retry is not None:
        values['retry'] = retry
    request = Admission(scope=doc.scope, document_id=doc.document_id,
                        document_version_id=doc.document_version_id, source=doc.source,
                        display_filename=doc.display_filename, mime=doc.detected_mime,
                        request_idempotency_key=request_key, resume_from=resume_from,
                        profile=ProcessingProfile(**values), steps=specs(plan, plan_ref))
    return DocumentJobs(ledger, store).admit(request)


class DigestionHandler:
    def __init__(self, ledger, plan_ref, inference):
        self.ledger, self.plan_ref, self.inference = ledger, plan_ref, inference
        self._loaded = None  # Immutable verified planning cache, never execution authority.

    def analyze(self, request, job, step, store, plan):
        """Execution-context hook; evidence validation remains below this boundary."""
        return self.inference.analyze(request)

    def _load(self, store, scope, limit):
        if self._loaded is None:
            plan = read(store, scope, self.plan_ref, Plan, limit)
            artifact = deserialize(store.read(scope, plan.structure.extraction, max_bytes=limit), max_bytes=limit)
            if build_plan(artifact, plan.structure.extraction, plan.profile) != plan:
                raise DigestionError('incompatible_checkpoint')
            self._loaded = (plan, EvidenceIndex(artifact))
            self._nodes = {c.chunk_id: c for c in plan.chunks}
            self._nodes.update({n.stage_id: n for n in plan.reducers})
            self._specs = specs(plan, self.plan_ref)
            self._plan_hash = fingerprint(plan.model_dump(mode='json'))
        plan, index = self._loaded
        if scope != self.plan_ref.scope or limit != plan.profile.max_artifact_bytes:
            raise DigestionError('incompatible_checkpoint')
        return plan, index

    @staticmethod
    def request(plan, stage_id, checkpoints, refs, nodes=None):
        if nodes is None:
            nodes = {c.chunk_id: c for c in plan.chunks}
            nodes.update({n.stage_id: n for n in plan.reducers})
        node = nodes.get(stage_id)
        if isinstance(node, AnalysisChunk):
            chunk = node
            return StageRequest(stage_id=stage_id, stage='analysis', profile=plan.profile,
                                structural_path=chunk.path, source_data=chunk.pieces)
        if node is None:
            raise DigestionError('incompatible_checkpoint')
        return StageRequest(stage_id=stage_id, stage='reduction', profile=plan.profile,
                            structural_path=node.path, children=tuple(
                                ChildInput(artifact=refs[k], result=checkpoints[k].result, inherited=checkpoints[k].inherited) for k in node.children))

    def __call__(self, job, step, store):
        scope = job.admission.scope
        limit = job.admission.profile.max_artifact_bytes
        plan, index = self._load(store, scope, limit)
        expected = self._specs
        if (job.admission.steps != expected or step.spec not in expected
                or job.admission.source != index.artifact.document.source
                or job.admission.document_version_id != plan.structure.document_version_id):
            raise DigestionError('incompatible_checkpoint')
        if step.spec.unit_id == expected[0].unit_id:
            return (put(store, scope, plan, limit), put(store, scope, plan.structure, limit))
        steps = {s.spec.unit_id: s for s in self.ledger.steps(scope, job.job_id)}
        plan_hash = self._plan_hash
        checkpoints, refs = {}, {}
        wanted = ({str(c.chunk_id) for c in plan.chunks} | {str(n.stage_id) for n in plan.reducers}
                  if step.spec.unit_id == 'digest' else set(step.spec.depends_on))
        for key in wanted:
            if key == expected[0].unit_id:
                continue
            child = steps[key]
            if child.state != 'SUCCEEDED' or len(child.manifest) != 1:
                raise DigestionError('incompatible_checkpoint')
            ref = child.manifest[0]
            cp = read(store, scope, ref, Checkpoint, limit)
            if cp.plan_hash != plan_hash or str(cp.result.stage_id) != key:
                raise DigestionError('incompatible_checkpoint')
            checkpoints[cp.result.stage_id], refs[cp.result.stage_id] = cp, ref
        if step.spec.unit_id == 'digest':
            store.inspect(scope, plan.structure.extraction, max_bytes=limit)
            store.inspect(scope, self.plan_ref, max_bytes=limit)
            # Validate accepted graph in deterministic topological order after reopening.
            ordered = {}
            for key in [c.chunk_id for c in plan.chunks] + [n.stage_id for n in plan.reducers]:
                cp = checkpoints[key]
                request = self.request(plan, key, ordered, refs, self._nodes)
                parents = ((self.plan_ref, plan.structure.extraction) if request.stage == 'analysis'
                           else tuple(child.artifact for child in request.children))
                if cp.parents != parents:
                    raise DigestionError('incompatible_checkpoint')
                validate_result(encode(cp.result), request, index)
                inherited, propositions = inherited_summary(cp.result, request,
                    tuple(ordered[c.result.stage_id] for c in request.children))
                if cp.inherited != inherited or cp.propositions != propositions:
                    raise DigestionError('incompatible_checkpoint')
                ordered[key] = cp
            digest = make_digest(plan, self.plan_ref, ordered, refs, index)
            if digest.status == 'FAILED':
                raise DigestionError('coverage_failed')
            return (put(store, scope, digest, limit), put(store, scope, digest.coverage, limit))
        stage_id = UUID(step.spec.unit_id)
        request = self.request(plan, stage_id, checkpoints, refs, self._nodes)
        result = validate_result(self.analyze(request, job, step, store, plan), request, index)
        parents = ((self.plan_ref, plan.structure.extraction) if request.stage == 'analysis'
                   else tuple(child.artifact for child in request.children))
        inherited, propositions = inherited_summary(result, request,
            tuple(checkpoints[c.result.stage_id] for c in request.children))
        cp = Checkpoint(plan_hash=plan_hash, parents=parents, result=result,
                        inherited=inherited, propositions=propositions)
        return (put(store, scope, cp, limit),)


def load_digest(ledger, store, scope, job_id):
    """Read only accepted final output. Never expose orphan/uncommitted digest bytes."""
    job = ledger.get_job(scope, job_id)
    step = next((s for s in ledger.steps(scope, job_id) if s.spec.unit_id == 'digest'), None)
    if step is None or step.state != 'SUCCEEDED' or len(step.manifest) != 2:
        raise DigestionError('coverage_failed')
    digest = read(store, scope, step.manifest[0], DigestArtifact, job.admission.profile.max_artifact_bytes)
    if digest.status == 'FAILED' or digest.document_version_id != job.admission.document_version_id:
        raise DigestionError('incompatible_checkpoint')
    return digest
