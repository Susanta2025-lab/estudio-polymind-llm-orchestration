from documents.jobs.service import DocumentJobs
from documents.jobs.worker import Worker, LocalDispatcher, relay
from documents.publication.workflow import PublicationHandler, publication_step


def test_preparation_runs_in_existing_durable_worker(env):
    service, document = env
    source_job = document()
    m = service.plan([source_job])
    source = service.jobs.get_job(service.scope, source_job)
    request = source.admission.model_copy(update={'request_idempotency_key':'publication-preparation',
                                                  'steps':(publication_step(m),)})
    job = DocumentJobs(service.jobs, service.objects).admit(request)
    queue = LocalDispatcher(); relay(service.jobs,queue)
    worker = Worker(service.jobs,queue,service.objects,PublicationHandler(service,m.generation),owner='publisher')
    assert worker.once()
    assert service.jobs.get_job(service.scope,job.job_id).state == 'COMPLETED'
    assert service.authority.active().generation is None
    assert service.authority.candidate(m.generation)[1] == 'READY'
    service.activate(m.generation)
