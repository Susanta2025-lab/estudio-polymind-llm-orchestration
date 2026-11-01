"""Entra identity through L1 approval/governance, with all transport intercepted."""
import pytest

from security.authority import SecurityAuthority
from security.models import SecurityError
from tests.integration.test_foundry_l1_launcher import composition, deny_network
from tests.performance import foundry_l1 as launch
from tests.unit.test_security_identity import identity
from tests.unit.test_security_entra import entra
from tests.approval_helpers import approval_signer


@pytest.mark.parametrize('approval', ['valid', 'missing', 'wrong'])
def test_entra_l1_preserves_signed_approval_and_governance(composition, entra, monkeypatch, approval, approval_signer):
    cfg, _, http, _, _ = composition
    verifier, token, _, _ = entra
    principal = verifier.verify(token())
    cfg = launch.LaunchConfiguration.model_validate({
        **cfg.model_dump(), 'oidc':verifier.config, 'owner_scope':principal.scope.identity(),
    })
    SecurityAuthority(cfg.security_path).register(principal)
    monkeypatch.setattr(launch, 'OIDCVerifier', lambda _: verifier)
    digest = launch.configuration_digest(cfg)
    access = token()  # No custom issuer claim is needed.
    artifact,trust = approval_signer(cfg, principal,
        changes={'purpose':'test'} if approval == 'wrong' else None)
    if approval == 'missing':
        artifact = None
    if approval != 'valid':
        with pytest.raises(SecurityError):
            launch.launch(cfg, digest, digest, access, 'TEST-CREDENTIAL',
                          approval=artifact, approval_trust=trust)
        assert not http.sent
        assert not (cfg.audit_directory / 'live-started.json').exists()
    else:
        result = launch.launch(cfg, digest, digest, access, 'TEST-CREDENTIAL',
                          approval=artifact, approval_trust=trust)
        assert result['calls'] == 4
        assert result['job_state'] == 'COMPLETED'
        assert result['questions']['status'] == 'COMPLETE'
        assert result['publication']['citations'] == 8
        assert all(row['state'] == 'SETTLED' for row in result['governance_records'])


@pytest.mark.parametrize('changes', [
    {'scp':None}, {'roles':[]}, {'roles':['PolyMind.Admin']}, {'aud':'foreign'},
    {'tid':'foreign'}, {'exp':1}, {'token_use':'id'},
])
def test_operator_artifact_never_bypasses_entra_authentication(composition, entra, monkeypatch, approval_signer, changes):
    cfg, _, http, _, _ = composition
    verifier, token, _, _ = entra
    principal = verifier.verify(token())
    cfg = launch.LaunchConfiguration.model_validate({
        **cfg.model_dump(), 'oidc':verifier.config, 'owner_scope':principal.scope.identity(),
    })
    SecurityAuthority(cfg.security_path).register(principal)
    monkeypatch.setattr(launch, 'OIDCVerifier', lambda _:verifier)
    artifact, trust = approval_signer(cfg, principal)
    digest = launch.configuration_digest(cfg)
    with pytest.raises(SecurityError):
        launch.launch(cfg, digest, digest, token(changes), 'TEST-CREDENTIAL',
                      approval=artifact, approval_trust=trust)
    assert not http.sent and not list(trust.replay_directory.iterdir())
