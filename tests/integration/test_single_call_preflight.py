"""Preflight failures use only synthetic identities and isolated authorities."""
import json
import sys
import time

import httpx
import pytest

from tests.integration.test_single_call_harness import rig, offline, entra, identity, approval_signer
from tests.performance import foundry_single_call as h
from security.identity import OIDCVerifier
from security.models import SecurityError


@pytest.mark.parametrize('missing', ['configuration', 'approve-sha256', 'approval', 'approval-trust'])
def test_required_live_arguments(monkeypatch, capsys, missing):
    args = ['single', '--live']
    for name in ('configuration', 'approve-sha256', 'approval', 'approval-trust'):
        if name != missing:
            args.extend(['--'+name, 'synthetic'])
    monkeypatch.setattr(sys, 'argv', args)
    with pytest.raises(SystemExit) as exc:
        h.main()
    assert exc.value.code == 2
    assert '--'+missing in capsys.readouterr().err


@pytest.mark.parametrize('offset,eligible,category', [
    (-1, False, 'window_not_started'), (0, True, None),
    (1199.999, True, None), (1200, False, 'window_insufficient_remaining_time'),
    (1800, False, 'window_insufficient_remaining_time'),
])
def test_window_boundaries(rig, monkeypatch, offset, eligible, category):
    cfg = rig[0].model_copy(update={'execution_not_before': 2000000000,
        'approval_expires': 2000001800, 'credential_valid_until': 2000001900})
    monkeypatch.setattr(h.time, 'time', lambda: 2000000000+offset)
    info = h.window_information(cfg)
    assert info['window_eligible'] is eligible
    assert info['launch_before_utc'] == '2033-05-18T03:53:20+00:00'
    assert info['remaining_launch_seconds'] == pytest.approx(1200-offset, abs=1e-6)
    d = h.PreflightDiagnostic()
    if eligible:
        h.check_window(cfg, d)
    else:
        with pytest.raises(SecurityError): h.check_window(cfg, d)
        assert d.category == category
    earlier = cfg.model_copy(update={'credential_valid_until':2000001500})
    assert h.window_information(earlier)['remaining_launch_seconds'] == pytest.approx(900-offset, abs=1e-6)


@pytest.mark.parametrize('case,stage,category', [
    ('invalid', 'configuration_validation', 'invalid_configuration'),
    ('window', 'execution_window', 'window_insufficient_remaining_time'),
    ('credential', 'credential_presence', 'credential_missing'),
    ('digest', 'configuration_acknowledgement', 'approval_digest_mismatch'),
    ('oidc_timeout', 'operator_identity_verification', 'operator_authentication_failed'),
    ('oidc_transport', 'operator_identity_verification', 'operator_authentication_failed'),
    ('authorization', 'security_authorization', 'operator_authorization_failed'),
    ('fixture', 'fixture_preparation', 'fixture_validation_failed'),
    ('fixture_digest', 'fixture_digest_verification', 'fixture_mismatch'),
    ('unexpected', 'fixture_preparation', 'unexpected_internal_error'),
    ('unsafe', 'private_path_validation', 'private_path_invalid'),
    ('unavailable', 'private_path_validation', 'private_path_invalid'),
])
def test_preflight_failure(rig, monkeypatch, case, stage, category):
    cfg, _, http, ledger, authority, principal, approve, artifact, trust, prepared = rig
    d = h.PreflightDiagnostic()
    credential, acknowledgement = 'SYNTHETIC', h.configuration_digest(cfg)
    def fail(exc):
        def invoke(*a, **kw): raise exc
        return invoke
    if case == 'invalid': cfg = cfg.model_copy(update={'executor_sha256':'0'*64})
    if case == 'window': cfg = cfg.model_copy(update={'approval_expires':int(time.time())})
    if case == 'credential': credential = ''
    if case == 'digest': acknowledgement = 'PRIVATE_SENTINEL'
    if case.startswith('oidc_'):
        verifier = OIDCVerifier(cfg.oidc, fetch=fail(
            httpx.ReadTimeout('PRIVATE_SENTINEL') if case == 'oidc_timeout' else httpx.ConnectError('PRIVATE_SENTINEL')))
        monkeypatch.setattr(h, 'OIDCVerifier', lambda c: verifier)
    if case == 'authorization': monkeypatch.setattr(h.SecurityAuthority, 'authorize', fail(SecurityError()))
    if case in ('fixture', 'unexpected'):
        monkeypatch.setattr(h, 'prepare_analysis', fail(
            ValueError('PRIVATE_SENTINEL') if case == 'fixture' else RuntimeError('PRIVATE_SENTINEL')))
    if case == 'fixture_digest':
        monkeypatch.setattr(h, 'prepare_analysis', lambda *a: (*prepared[:-1], '0'*64))
    if case == 'unsafe': cfg.audit_directory.chmod(0o755)
    if case == 'unavailable': cfg.audit_directory.rmdir()
    # Synthetic fresh token matches fixture verifier; it never leaves this process.
    token = rig[1].__defaults__[-1]
    with pytest.raises(Exception):
        h.launch(cfg, acknowledgement, token, credential, artifact, trust, diagnostic=d)
    assert (d.stage, d.category) == (stage, category)
    assert d.provider_attempted is False and not d.approval_consumption_entered
    assert not http.sent and not list(trust.replay_directory.iterdir())
    assert not (cfg.audit_directory/'live-started.json').exists()
    if case != 'authorization': assert not ledger.usage(principal, authority)
    records = list(cfg.audit_directory.glob('preflight-diagnostic-*.json'))
    if case in ('invalid', 'unsafe', 'unavailable'):
        assert not records
    else:
        assert len(records) == 1
        assert records[0].stat().st_mode & 0o777 == 0o600
        value = records[0].read_text()
        assert 'PRIVATE_SENTINEL' not in value
        assert json.loads(value) == d.evidence()
        d.persist()
        assert len(list(cfg.audit_directory.glob('preflight-diagnostic-*.json'))) == 1


def test_cli_invalid_and_unexpected_sanitized(rig, monkeypatch, capsys):
    cfg = rig[0]
    path = cfg.audit_directory/'config.json'
    h.durable_json(path, {'private':'PRIVATE_SENTINEL'})
    monkeypatch.setattr(sys, 'argv', ['single', '--configuration', str(path)])
    assert h.main() == 1
    out = capsys.readouterr().out
    assert 'invalid_configuration' in out and 'Provider request attempted: NO' in out
    assert 'PRIVATE_SENTINEL' not in out and 'inspect private audit' not in out
    def fail(*args): raise RuntimeError('PRIVATE_SENTINEL')
    monkeypatch.setattr(h, 'read_private', fail)
    assert h.main() == 1
    out = capsys.readouterr().out
    assert 'unexpected_internal_error' in out and 'PRIVATE_SENTINEL' not in out


def test_diagnostic_write_failure_preserves_original(rig, monkeypatch):
    cfg = rig[0]
    def fail(*args): raise OSError('PRIVATE_SENTINEL')
    monkeypatch.setattr(h, 'durable_json', fail)
    d = h.PreflightDiagnostic()
    with pytest.raises(SecurityError):
        h.launch(cfg, '', '', '', None, None, diagnostic=d)
    assert d.category == 'credential_missing' and not rig[2].sent


def test_offline_review_prints_timing(rig, monkeypatch, capsys):
    cfg = rig[0]
    path = cfg.audit_directory/'config.json'
    h.durable_json(path, cfg.model_dump(mode='json'))
    monkeypatch.setattr(sys, 'argv', ['single', '--configuration', str(path)])
    assert h.main() == 0
    info = json.loads(capsys.readouterr().out)['execution_window']
    assert info['safety_margin_seconds'] == 600 and info['window_eligible']
    assert not info['cutoff_inclusive'] and info['launch_before_utc'].endswith('+00:00')
    assert not rig[2].sent and not list(rig[8].replay_directory.iterdir())


@pytest.mark.parametrize('error', [httpx.ReadTimeout, httpx.ConnectError])
def test_real_oidc_fetch_transport_failure(entra, monkeypatch, error):
    verifier, token, _, _ = entra
    observed = []
    class Client:
        def __init__(self, **kwargs): observed.append(kwargs)
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def stream(self, *args): raise error('PRIVATE_SENTINEL')
    monkeypatch.setattr('security.identity.httpx.Client', Client)
    fresh = OIDCVerifier(verifier.config)
    with pytest.raises(SecurityError) as exc:
        fresh.verify(token())
    assert str(exc.value) == 'authentication_required'
    assert exc.value.__suppress_context__
    assert observed == [dict(timeout=3.0, follow_redirects=False, trust_env=False)]
    assert not fresh._keys


def test_post_execution_uncertainty_and_unique_evidence(rig, monkeypatch):
    cfg, _, http, _, _, _, _, artifact, trust, _ = rig
    def fail(*a): raise RuntimeError('PRIVATE_SENTINEL')
    monkeypatch.setattr(h, 'execute_stage', fail)
    d = h.PreflightDiagnostic()
    with pytest.raises(RuntimeError):
        h.launch(cfg, h.configuration_digest(cfg), rig[1].__defaults__[-1], 'SYNTHETIC', artifact, trust, diagnostic=d)
    assert d.provider_attempted is None and d.evidence()['state'] == 'FAILED'
    assert d.approval_consumption_entered and not http.sent
    first = next(cfg.audit_directory.glob('preflight-diagnostic-*.json'))
    original = first.read_bytes()
    second = h.PreflightDiagnostic()
    second.root = cfg.audit_directory
    second.persist()
    assert first.read_bytes() == original
    assert len(list(cfg.audit_directory.glob('preflight-diagnostic-*.json'))) == 2


def test_symlink_audit_never_receives_diagnostics(rig, tmp_path):
    target = tmp_path/'target'
    target.mkdir(mode=0o700)
    link = tmp_path/'link'
    link.symlink_to(target, target_is_directory=True)
    cfg = rig[0].model_copy(update={'audit_directory':link})
    d = h.PreflightDiagnostic()
    with pytest.raises(ValueError): h.launch(cfg, '', '', '', None, None, diagnostic=d)
    assert d.category == 'private_path_invalid' and not list(target.iterdir())
