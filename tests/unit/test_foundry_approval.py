"""Approval signatures and durable replay denial, without network or live keys."""
from concurrent.futures import ThreadPoolExecutor
import json

from cryptography.hazmat.primitives.asymmetric import rsa
import jwt
import pytest

from security.models import SecurityError
from tests.approval_helpers import approval_signer
from tests.integration.test_foundry_l1_launcher import composition, deny_network
from tests.unit.test_security_identity import identity
from tests.performance import foundry_l1 as launch
from tests.performance import foundry_approval as approval


@pytest.fixture
def approved(composition, approval_signer):
    cfg, _, http, token, verifier = composition
    access = token({'roles':['operator']})
    principal = verifier.verify(access)
    artifact, trust = approval_signer(cfg, principal)
    return cfg, principal, artifact, trust, access, verifier, http


def verify(values, **kwargs):
    cfg, principal, artifact, trust, *_ = values
    return approval.verify_artifact(kwargs.get('artifact', artifact), kwargs.get('trust', trust),
        cfg, principal, launch.configuration_digest(cfg))


def test_valid_artifact_without_custom_jwt_claim(approved):
    cfg, principal, artifact, trust, access, verifier, _ = approved
    digest = launch.configuration_digest(cfg)
    assert 'polymind_l1_approval' not in jwt.decode(access, options={'verify_signature':False})
    assert launch.verify_approval(cfg, digest, digest, access, verifier,
        approval=artifact, approval_trust=trust) == principal
    assert verify(approved)['binding']['limits']['attempts'] == 4


@pytest.mark.parametrize('changes', [
    {'purpose':'test'}, {'purpose':None}, {'exp':1}, {'exp':None}, {'exp':True},
    {'iat':4102444800}, {'iat':None}, {'iat':'1'}, {'iat':False}, {'iat':1},
    {'nbf':4102444800}, {'nbf':None}, {'nbf':True},
    {'jti':None}, {'jti':'../escape'}, {'jti':'not-a-uuid'},
    {'aud':'different'}, {'aud':['polymind-l1-live']}, {'iss':'untrusted'},
    {'binding':None}, {'binding':{}}, {'extra':'unknown'},
])
def test_signed_invalid_claims_rejected(approved, approval_signer, changes):
    cfg, principal, *_ = approved
    artifact, trust = approval_signer(cfg, principal, changes=changes)
    with pytest.raises(SecurityError, match='^access_denied$'):
        verify(approved, artifact=artifact, trust=trust)


@pytest.mark.parametrize('section,field,value', [
    ('operator','issuer','https://foreign.invalid'), ('operator','subject','bob'),
    ('operator','tenant','foreign'), ('operator','owner_scope','foreign'),
    ('foundry','resource','eci-foundry-dev-susanta'), ('foundry','deployment','eci-gpt-54-mini'),
    ('foundry','endpoint','https://attacker.invalid'), ('foundry','model_version','different'),
    ('foundry','sku','different'), ('foundry','region','different'),
    ('budget','maximum','5.01'), ('budget','currency','USD'), ('budget','extra_cost','0.01'),
    ('limits','attempts',5), ('limits','input_tokens',25001), ('limits','output_tokens',3001),
    ('limits','total_input',100001), ('limits','total_output',12001), ('limits','rpm',True),
])
def test_every_signed_binding_is_exact(approved, approval_signer, section, field, value):
    cfg, principal, *_ = approved
    bound = approval.bindings(cfg, principal, launch.configuration_digest(cfg))
    bound[section][field] = value
    artifact, trust = approval_signer(cfg, principal, changes={'binding':bound})
    with pytest.raises(SecurityError):
        verify(approved, artifact=artifact, trust=trust)


@pytest.mark.parametrize('field,value', [('configuration_sha256','0'*64), ('expires',1)])
def test_digest_and_expiration_bindings(approved, approval_signer, field, value):
    cfg, principal, *_ = approved
    bound = approval.bindings(cfg, principal, launch.configuration_digest(cfg))
    bound[field] = value
    artifact, trust = approval_signer(cfg, principal, changes={'binding':bound})
    with pytest.raises(SecurityError):
        verify(approved, artifact=artifact, trust=trust)


@pytest.mark.parametrize('change', [
    {'purpose':'test'}, {'operator_subject':'bob'}, {'operator_issuer':'other'}, {'operator_tenant':'other'},
])
def test_independent_trust_authorizes_signer_and_identity(approved, approval_signer, change):
    cfg, principal, *_ = approved
    artifact, trust = approval_signer(cfg, principal, trust_changes=change)
    with pytest.raises(SecurityError):
        verify(approved, artifact=artifact, trust=trust)


@pytest.mark.parametrize('header', [
    {'kid':'foreign', 'typ':'polymind-approval+jwt'}, {'kid':'ephemeral-offline-key', 'typ':'JWT'},
    {'kid':'ephemeral-offline-key', 'typ':'polymind-approval+jwt', 'jku':'https://attacker.invalid'},
    {'kid':'ephemeral-offline-key', 'typ':'polymind-approval+jwt', 'jwk':{}},
    {'kid':'ephemeral-offline-key', 'typ':'polymind-approval+jwt', 'crit':['x']},
])
def test_no_artifact_controlled_trust(approved, approval_signer, header):
    artifact, trust = approval_signer(approved[0], approved[1], headers=header)
    with pytest.raises(SecurityError):
        verify(approved, artifact=artifact, trust=trust)


def test_forgery_unsigned_and_algorithm_confusion(approved, approval_signer):
    foreign = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    artifact, _ = approval_signer(approved[0], approved[1], signing_key=foreign)
    claims = jwt.decode(approved[2], options={'verify_signature':False})
    for encoded in (artifact, '', 'x'*16385, json.dumps(claims),
                    jwt.encode(claims, None, algorithm='none'),
                    jwt.encode(claims, 'synthetic-test-secret-of-at-least-32-bytes', algorithm='HS256')):
        with pytest.raises(SecurityError):
            verify(approved, artifact=encoded)


def test_replay_rejected_after_restart_and_concurrently(approved):
    _, _, artifact, trust, *_ = approved
    verified = verify(approved)
    def attempt():
        try:
            approval.consume(verified, trust, artifact)
            return True
        except SecurityError:
            return False
    with ThreadPoolExecutor(max_workers=4) as pool:
        assert sum(pool.map(lambda _: attempt(), range(4))) == 1
    reopened = approval.ApprovalTrust.model_validate_json(trust.model_dump_json())
    with pytest.raises(SecurityError):
        approval.consume(verified, reopened, artifact)
    rows = list(trust.replay_directory.glob('*.consumed.json'))
    assert len(rows) == 1
    assert artifact not in rows[0].read_text()


def test_resigning_same_id_does_not_allow_replay(approved, approval_signer):
    cfg, principal, artifact, trust, *_ = approved
    verified = verify(approved)
    approval.consume(verified, trust, artifact)
    resigned, _ = approval_signer(cfg, principal, changes={'jti':verified['jti']})
    with pytest.raises(SecurityError):
        approval.consume(verify(approved, artifact=resigned), trust, resigned)


def test_fsync_failure_consumes_approval_and_refuses_retry(approved, monkeypatch):
    artifact, trust = approved[2:4]
    verified = verify(approved)
    def fail(*args):
        raise OSError('private disk failure')
    monkeypatch.setattr(approval, 'fsync_directory', fail)
    with pytest.raises(SecurityError, match='^access_denied$'):
        approval.consume(verified, trust, artifact)
    assert list(trust.replay_directory.glob('*.consumed.json'))
    with pytest.raises(SecurityError):
        approval.consume(verified, trust, artifact)


def test_legacy_claim_cannot_replace_artifact(approved, composition):
    cfg, _, _, trust, _, verifier, http = approved
    # An authentic custom issuer claim no longer substitutes for operator approval.
    digest = launch.configuration_digest(cfg)
    with pytest.raises(SecurityError):
        launch.launch(cfg, digest, digest, composition[3]({'roles':['operator'],
            'polymind_l1_approval':digest}), 'TEST-CREDENTIAL', approval_trust=trust)
    assert not http.sent


def test_private_trust_and_approval_loading(approved, tmp_path):
    _, _, artifact, trust, *_ = approved
    path = tmp_path / 'trust.json'
    path.write_text(trust.model_dump_json()); path.chmod(0o600)
    assert approval.load_trust(path) == trust
    assert approval.read_private(path, 16384)
    with pytest.raises(SecurityError):
        approval.read_private(path, 1)
    path.chmod(0o644)
    with pytest.raises(ValueError):
        approval.load_trust(path)
    path.chmod(0o600)
    link = tmp_path / 'symlink.json'; link.symlink_to(path)
    with pytest.raises(ValueError):
        approval.load_trust(link)
    test_trust = approval.ApprovalTrust.model_validate({**trust.model_dump(), 'purpose':'test'})
    path.write_text(test_trust.model_dump_json())
    with pytest.raises(SecurityError):
        approval.load_trust(path)


def test_setup_failure_consumes_approval_before_provider(approved, monkeypatch):
    cfg, _, artifact, trust, access, _, http = approved
    digest = launch.configuration_digest(cfg)
    def fail(*args):
        raise RuntimeError('local retrieval unavailable')
    monkeypatch.setattr(launch, 'local_retrieval', fail)
    with pytest.raises(RuntimeError):
        launch.launch(cfg, digest, digest, access, 'TEST-CREDENTIAL', approval=artifact, approval_trust=trust)
    with pytest.raises(SecurityError):
        launch.launch(cfg, digest, digest, access, 'TEST-CREDENTIAL', approval=artifact, approval_trust=trust)
    assert not http.sent
    assert list(trust.replay_directory.glob('*.consumed.json'))


def test_approval_cannot_be_reused_for_a_new_audit_directory(approved, approval_signer, tmp_path):
    cfg, principal, artifact, trust, access, _, http = approved
    verified = verify(approved)
    approval.consume(verified, trust, artifact)
    other = tmp_path / 'another-run'; other.mkdir(mode=0o700)
    changed = launch.LaunchConfiguration.model_validate({**cfg.model_dump(), 'audit_directory':other})
    digest = launch.configuration_digest(changed)
    # The old artifact fails its config binding, even with a fresh run directory.
    with pytest.raises(SecurityError):
        launch.launch(changed, digest, digest, access, 'TEST-CREDENTIAL', approval=artifact, approval_trust=trust)
    # Even a freshly signed changed plan cannot reuse a consumed approval ID.
    resigned, _ = approval_signer(changed, principal, changes={'jti':verified['jti']})
    with pytest.raises(SecurityError):
        launch.launch(changed, digest, digest, access, 'TEST-CREDENTIAL', approval=resigned, approval_trust=trust)
    assert not http.sent


def test_replay_state_must_be_independent_of_run_directory(approved, approval_signer):
    artifact, trust = approval_signer(approved[0], approved[1],
        trust_changes={'replay_directory':approved[0].audit_directory})
    with pytest.raises(SecurityError):
        verify(approved, artifact=artifact, trust=trust)


def test_existing_legacy_run_marker_still_blocks(approved):
    cfg, _, artifact, trust, access, _, http = approved
    marker = cfg.audit_directory / 'live-started.json'
    marker.write_text('{"stage":"L1"}'); marker.chmod(0o600)
    digest = launch.configuration_digest(cfg)
    with pytest.raises(FileExistsError):
        launch.launch(cfg, digest, digest, access, 'TEST-CREDENTIAL', approval=artifact, approval_trust=trust)
    assert not http.sent


def test_live_cli_loads_independent_trust_and_artifact(approved, tmp_path, monkeypatch, capsys):
    import sys
    cfg, _, artifact, trust, access, _, http = approved
    files = []
    for name, text in (('config.json',cfg.model_dump_json()), ('trust.json',trust.model_dump_json()),
                       ('approval.jwt',artifact)):
        path = tmp_path / name; path.write_text(text); path.chmod(0o600); files.append(str(path))
    monkeypatch.setenv('POLYMIND_L1_OPERATOR_TOKEN', access)
    monkeypatch.setenv('POLYMIND_L1_AZURE_CREDENTIAL', 'TEST-CREDENTIAL')
    monkeypatch.setattr(sys, 'argv', ['foundry_l1', '--live', '--configuration', files[0],
        '--approval-trust', files[1], '--approval', files[2], '--approve-sha256', launch.configuration_digest(cfg)])
    launch.main()
    assert json.loads(capsys.readouterr().out)['calls'] == 4
    assert len(http.sent) == 4


@pytest.mark.parametrize('omitted', ['--approval', '--approval-trust'])
def test_live_cli_requires_new_inputs(monkeypatch, omitted):
    import sys
    args = ['foundry_l1', '--live', '--configuration', '/private/config.json', '--approve-sha256', '0'*64]
    args += [('--approval-trust' if omitted == '--approval' else '--approval'), '/private/input']
    monkeypatch.setattr(sys, 'argv', args)
    monkeypatch.setattr(launch, 'launch', lambda *a, **k: pytest.fail('Live path reached'))
    with pytest.raises(SystemExit) as error:
        launch.main()
    assert error.value.code == 2


def test_invalid_approval_never_mutates_existing_governance(approved, approval_signer):
    cfg, principal, _, trust, access, _, http = approved
    before = {path:path.read_bytes() for path in (cfg.security_path, cfg.governance_path, cfg.admission_path)}
    artifact, _ = approval_signer(cfg, principal, changes={'purpose':'test'})
    digest = launch.configuration_digest(cfg)
    with pytest.raises(SecurityError):
        launch.launch(cfg, digest, digest, access, 'TEST-CREDENTIAL', approval=artifact, approval_trust=trust)
    assert all(path.read_bytes() == data for path, data in before.items())
    assert not http.sent and not list(trust.replay_directory.iterdir())


@pytest.mark.parametrize('change', ['policy', 'execution_window'])
def test_policy_migration_and_window_require_fresh_signature(approved, change):
    cfg, principal, artifact, trust, *_ = approved
    data = cfg.model_dump()
    if change == 'policy':
        data['governance_policy']['version'] = 'phase17hl-l1/2'
        for scope in ('owner', 'tenant'):
            data['governance_policy'][scope].update(requests_per_window=5,
                daily_tokens=115305, monthly_tokens=115305)
    else:
        data['execution_not_before'] = int(__import__('time').time())
    updated = launch.LaunchConfiguration.model_validate(data)
    assert launch.configuration_digest(updated) != launch.configuration_digest(cfg)
    with pytest.raises(SecurityError):
        approval.verify_artifact(artifact, trust, updated, principal, launch.configuration_digest(updated))
    assert not list(trust.replay_directory.iterdir())
