"""Optional preparation adapter for the existing Phase 17C Worker, not a scheduler.

Activation remains an explicit administrative service decision after preparation.
The worker's accepted object manifest is still governed by its lease/cancel fence.
"""
from io import BytesIO

from documents.digestion.codec import encode
from documents.jobs.models import StepSpec, fingerprint
from documents.models import stable_id
from documents.publication.models import PublicationError


def publication_step(manifest):
    return StepSpec(unit_id=f'publication/{manifest.generation}', stage='NORMALIZING',
                    schema_version='publication/1', config_fingerprint=fingerprint(manifest.model_dump(mode='json')))


class PublicationHandler:
    def __init__(self, service, generation):
        self.service, self.generation = service, generation

    def __call__(self, job, step, store):
        manifest = self.service.manifest(self.generation)
        if job.admission.scope != manifest.scope or step.spec != publication_step(manifest):
            raise PublicationError('publication_invalid_input')
        self.service.prepare(self.generation)
        data = encode(manifest)
        return (store.put(manifest.scope, 'artifact', stable_id('publication-manifest/1', str(manifest.generation)),
                          BytesIO(data), max_bytes=job.admission.profile.max_artifact_bytes),)
