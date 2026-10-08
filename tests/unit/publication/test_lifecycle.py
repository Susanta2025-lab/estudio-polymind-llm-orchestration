from concurrent.futures import ThreadPoolExecutor

import pytest
from documents.publication.authority import SQLitePublicationAuthority
from documents.publication.models import PublicationError


def publish(service, jobs):
    m = service.plan(jobs)
    service.prepare(m.generation)
    service.activate(m.generation)
    return m


def test_concurrent_candidates_fencing_retry_and_aba(env):
    service, document = env
    one, two, three = document(), document('delta replacement\n'), document('third replacement\n')
    g1 = publish(service, [one])
    g2, g3 = service.plan([two]), service.plan([three])
    service.prepare(g2.generation); service.prepare(g3.generation)
    def activate(g):
        try:
            return service.activate(g.generation)
        except PublicationError as e:
            return e.category
    with ThreadPoolExecutor(2) as pool:
        results = list(pool.map(activate, [g2, g3]))
    assert sum(r == 'publication_stale_candidate' for r in results) == 1
    winner = service.authority.active()
    loser = g3 if winner.generation == g2.generation else g2
    with pytest.raises(PublicationError, match='publication_stale_candidate'):
        service.activate(loser.generation)
    service.rollback(g1.generation, winner)
    with pytest.raises(PublicationError, match='publication_stale_candidate'):
        service.activate(loser.generation)
    # An old successful publisher cannot reactivate after a later activation.
    with pytest.raises(PublicationError, match='publication_stale_candidate'):
        service.activate(winner.generation)


class Crash(BaseException):
    pass


@pytest.mark.parametrize('point', ['before_writes','after_write','after_writes','after_validation','before_activation','after_activation'])
def test_durable_crash_resume(env, point):
    service, document = env
    first = publish(service, [document()])
    second = service.plan([document('replacement one\nreplacement two\n')])
    def crash(at):
        if at == point:
            raise Crash()
    with pytest.raises(Crash):
        service.prepare(second.generation, checkpoint=crash)
        service.activate(second.generation, checkpoint=crash)
    assert service.authority.active().generation == (second.generation if point == 'after_activation' else first.generation)
    service.authority = SQLitePublicationAuthority(service.authority.path)
    service.prepare(second.generation)
    service.activate(second.generation)
    assert service.authority.active().generation == second.generation
    count = len(service.vectors.rows)
    assert service.plan([second.documents[0].job_id]).generation == second.generation
    service.prepare(second.generation)
    assert len(service.vectors.rows) == count


def test_failed_supersession_and_orphan_detection(env):
    service, document = env
    first = publish(service, [document()])
    second = service.plan([document('changed\n')])
    def failure(at):
        if at == 'after_write':
            raise RuntimeError('secret raw provider error')
    with pytest.raises(PublicationError, match='^publication_write_failure$'):
        service.prepare(second.generation, checkpoint=failure)
    assert service.authority.active().generation == first.generation
    assert service.authority.candidate(second.generation)[1] == 'FAILED'
    assert str(second.generation) in service.reconcile()['inactive_generations']
    service.prepare(second.generation)
    service.activate(second.generation)


@pytest.mark.parametrize('operation', ['revocation', 'rollback'])
@pytest.mark.parametrize('point', ['before_activation','after_activation'])
def test_revocation_rollback_interruption(env, operation, point):
    service, document = env
    first = publish(service, [document()])
    second = publish(service, [document('new version\n')])
    expected = service.authority.active()
    def crash(at):
        if at == point:
            raise Crash()
    with pytest.raises(Crash):
        if operation == 'revocation':
            service.revoke([second.documents[0].document_id], checkpoint=crash)
        else:
            service.rollback(first.generation, expected, checkpoint=crash)
    if point == 'before_activation':
        assert service.authority.active() == expected
    elif operation == 'revocation':
        assert service.manifest(service.authority.active().generation).records == ()
    else:
        assert service.authority.active().generation == first.generation
        assert service.rollback(first.generation, expected) == service.authority.active()


@pytest.mark.parametrize('corruption', ['dense','source','manifest','digest'])
def test_rollback_revalidates_inventory_and_provenance(env, corruption):
    service, document = env
    first = publish(service, [document()])
    publish(service, [document('new version\n')])
    before = service.authority.active()
    if corruption == 'dense':
        key = next(k for k,v in service.vectors.rows.items() if v.metadata['generation'] == str(first.generation))
        del service.vectors.rows[key]
    else:
        if corruption == 'manifest':
            ref = service.authority.candidate(first.generation)[0]
        elif corruption == 'digest':
            ref = first.documents[0].digest
        else:
            from documents.serialization import deserialize
            ref = deserialize(service.objects.read(service.scope, first.documents[0].extraction, max_bytes=32000000)).document.source
        (service.objects.root/str(ref.key)).write_bytes(b'corrupt')
    with pytest.raises(PublicationError):
        service.rollback(first.generation, before)
    assert service.authority.active() == before
