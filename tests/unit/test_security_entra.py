"""Offline Entra contract tests: ephemeral RSA keys, no deployed credentials."""
import json
import socket
import time

from cryptography.hazmat.primitives.asymmetric import rsa
import jwt
import pytest
from pydantic import ValidationError

from config.settings import Settings
from security.authority import SecurityAuthority
from security.identity import OIDCSettings, OIDCVerifier
from security.models import Action, SecurityError
from tests.unit.test_security_configuration import configured
from tests.unit.test_security_identity import identity


TENANT = '11111111-1111-4111-8111-111111111111'
AUDIENCE = '22222222-2222-4222-8222-222222222222'
ROLE = 'PolyMind.L1Operator'


@pytest.fixture(autouse=True)
def offline(monkeypatch):
    def deny(*args, **kwargs):
        raise AssertionError('Network forbidden in identity tests')
    monkeypatch.setattr(socket.socket, 'connect', deny)
    monkeypatch.setattr(socket, 'create_connection', deny)


@pytest.fixture
def entra(identity):
    legacy, sign, jwk, fetched = identity
    config = OIDCSettings(token_profile='entra_v2', tenant_id=TENANT, audience=AUDIENCE,
        issuer=f'https://login.microsoftonline.com/{TENANT}/v2.0',
        jwks_url=f'https://login.microsoftonline.com/{TENANT}/discovery/v2.0/keys')
    verifier = OIDCVerifier(config, fetch=legacy.fetch)

    def token(changes=None, **kwargs):
        return sign({'iss':config.issuer, 'aud':AUDIENCE, 'tid':TENANT,
                     'ver':'2.0', 'iat':int(time.time()) - 1, 'scp':'access_as_user',
                     'roles':[ROLE], 'token_use':None, **(changes or {})}, **kwargs)
    return verifier, token, jwk, fetched


def test_delegated_identity_has_only_l1_permission(entra):
    verifier, token, _, fetched = entra
    principal = verifier.verify(token())
    assert principal.permissions == frozenset({Action.PUBLICATION_MANAGE})
    assert principal.kind == 'user'
    assert principal.tenant_identity == TENANT
    assert principal.subject == 'alice'
    assert verifier.verify(token({'scp':'other access_as_user extra'})) == principal
    assert len(fetched) == 1
    assert verifier.verify(token({'owner':'forged', 'tenant':'forged', 'groups':['admin'],
                                  'wids':['admin'], 'oid':'different'})).scope == principal.scope


@pytest.mark.parametrize('changes', [
    {'iss':'https://sts.windows.net/' + TENANT + '/'},
    {'iss':'https://login.microsoftonline.com/common/v2.0'},
    {'iss':'https://attacker.invalid/v2.0'}, {'iss':None},
    {'aud':'00000003-0000-0000-c000-000000000000'},  # Microsoft Graph
    {'aud':'https://cognitiveservices.azure.com/'}, {'aud':'api://' + AUDIENCE},
    {'aud':TENANT}, {'aud':[AUDIENCE]}, {'aud':[AUDIENCE, 'other']}, {'aud':None},
    {'tid':AUDIENCE}, {'tid':None}, {'tid':[]},
    {'ver':'1.0'}, {'ver':2}, {'ver':None},
    {'exp':1}, {'exp':None}, {'exp':'4102444800'}, {'exp':True},
    {'nbf':4102444800}, {'nbf':None}, {'nbf':False},
    {'iat':4102444800}, {'iat':None}, {'iat':'1'}, {'iat':True},
    {'nbf':1, 'exp':1}, {'sub':None}, {'sub':''}, {'sub':42},
    {'scp':None}, {'scp':''}, {'scp':['access_as_user']}, {'scp':True},
    {'scp':'access_as_user.extra'}, {'scp':'prefix_access_as_user'},
    {'scp':'ACCESS_AS_USER'}, {'scp':'openid profile email'},
    {'scp':'other\taccess_as_user'},
    {'roles':None}, {'roles':[]}, {'roles':ROLE}, {'roles':[{}]},
    {'roles':['PolyMind.Admin']}, {'roles':['polymind.l1operator']},
    {'roles':[ROLE, 'PolyMind.Admin']}, {'roles':[ROLE] * 33},
    {'scp':None, 'idtyp':'app'}, {'idtyp':'app'},
    {'token_use':'id'}, {'scp':None, 'nonce':'id-token-nonce', 'roles':[ROLE]},
])
def test_rejected_claims_are_sanitized(entra, changes):
    verifier, token, _, _ = entra
    with pytest.raises(SecurityError, match='^authentication_required$') as error:
        verifier.verify(token(changes))
    assert error.value.__cause__ is None


@pytest.mark.parametrize('headers', [
    {'kid':'untrusted'}, {'kid':'test-key', 'typ':'id+jwt'},
    {'kid':'test-key', 'jku':'https://attacker.invalid/keys'},
    {'kid':'test-key', 'x5u':'https://attacker.invalid/cert'},
    {'kid':'test-key', 'jwk':{}}, {'kid':'test-key', 'crit':['scp']},
])
def test_signed_untrusted_headers_rejected(entra, headers):
    with pytest.raises(SecurityError):
        entra[0].verify(entra[1](headers=headers))


def test_wrong_key_and_algorithms_rejected(entra):
    verifier, token, _, _ = entra
    foreign = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    for encoded in (token(signing_key=foreign),
                    token(algorithm='HS256', signing_key='synthetic-secret-at-least-32-characters'),
                    jwt.encode({'sub':'alice'}, None, algorithm='none', headers={'kid':'test-key'})):
        with pytest.raises(SecurityError):
            verifier.verify(encoded)


@pytest.mark.parametrize('issuer', [
    None, f'https://login.microsoftonline.com/{TENANT}/v2.0',
    'https://login.microsoftonline.com/{tenantid}/v2.0',
])
def test_trusted_jwks_issuer_and_entra_metadata(entra, issuer):
    verifier, token, jwk, _ = entra
    jwk.update(x5t='public-thumbprint', x5c=['unused-public-certificate-metadata'])
    if issuer is not None:
        jwk['issuer'] = issuer
    assert verifier.verify(token()).kind == 'user'


@pytest.mark.parametrize('change', [
    {'issuer':'https://attacker.invalid'},
    {'issuer':f'https://login.microsoftonline.com/{AUDIENCE}/v2.0'},
    {'issuer':None}, {'issuer':{}}, {'kty':'oct'}, {'use':'enc'},
    {'alg':'HS256'}, {'key_ops':['sign']}, {'jku':'https://attacker.invalid'},
])
def test_untrusted_jwks_rejected(entra, change):
    verifier, token, jwk, _ = entra
    jwk.update(change)
    with pytest.raises(SecurityError):
        verifier.verify(token())


def test_rotation_and_expired_cache_fail_closed(entra):
    verifier, token, _, fetched = entra
    now = [0.0]
    verifier.clock = lambda: now[0]
    verifier.verify(token())
    with pytest.raises(SecurityError):
        verifier.verify(token(headers={'kid':'unknown'}))
    assert len(fetched) == 1  # Unknown kid cannot force an unbounded refresh.
    replacement = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    jwk = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(replacement.public_key()))
    jwk.update(kid='replacement', alg='RS256')
    verifier.fetch = lambda: {'keys':[jwk]}
    now[0] = 31
    encoded = token(headers={'kid':'replacement'}, signing_key=replacement)
    verifier.verify(encoded)
    with pytest.raises(SecurityError):
        verifier.verify(token())
    def unavailable():
        raise OSError('private transport detail')
    verifier.fetch = unavailable
    now[0] = 400
    with pytest.raises(SecurityError, match='^authentication_required$'):
        verifier.verify(encoded)
    assert not verifier.ready()


@pytest.mark.parametrize('change', [
    {'tenant_id':None}, {'tenant_id':'common'}, {'tenant_id':AUDIENCE},
    {'audience':'api://' + AUDIENCE}, {'audience':'polymind'},
    {'issuer':f'https://login.microsoftonline.com/{TENANT}/v2.0/'},
    {'issuer':'https://login.microsoftonline.com/common/v2.0'},
    {'jwks_url':'https://login.microsoftonline.com/common/discovery/v2.0/keys'},
    {'jwks_url':'https://attacker.invalid/keys'},
    {'jwks_url':f'https://login.microsoftonline.com/{TENANT}/discovery/v2.0/keys?app=other'},
    {'tenant_claim':'tenant'}, {'roles_claim':'groups'}, {'purpose_claim':'scp'},
    {'purpose_value':'id'}, {'service_roles':[ROLE]},
    {'role_mapping':{ROLE:['TENANT_ADMIN']}}, {'token_profile':'unknown'},
])
def test_invalid_configuration_fails_at_startup(entra, tmp_path, change):
    raw = {**entra[0].config.model_dump(mode='json'), **change}
    with pytest.raises(ValidationError):
        Settings(**{**configured(tmp_path), 'OIDC_CONFIGURATION':raw})


def test_settings_accept_profile_without_changing_governance(entra, tmp_path):
    values = {**configured(tmp_path), 'OIDC_CONFIGURATION':entra[0].config.model_dump(mode='json')}
    assert Settings(**values).authentication_mode == 'oidc_jwt'
    with pytest.raises(ValidationError):
        Settings(**{**values, 'GOVERNANCE_ENABLED':False})
    with pytest.raises(ValidationError):
        Settings(**{**values, 'API_AUTH_TOKEN':'synthetic-static-token'})


def test_profiles_cannot_be_selected_by_token(entra, identity):
    with pytest.raises(SecurityError):
        identity[0].verify(entra[1]())
    with pytest.raises(SecurityError):
        entra[0].verify(identity[1]({'roles':['operator']}))
    # Even at identical anchors, generic OIDC still requires its purpose claim.
    generic = OIDCVerifier(OIDCSettings(**{
        **entra[0].config.model_dump(), 'token_profile':'oidc', 'tenant_id':None,
    }), fetch=entra[0].fetch)
    with pytest.raises(SecurityError):
        generic.verify(entra[1]())


def test_generic_oidc_serialization_preserves_existing_approval_hashes(identity, entra):
    config = identity[0].config
    original = dict(issuer='https://identity.invalid', audience='polymind',
        jwks_url='https://identity.invalid/keys', tenant_claim='tid', roles_claim='roles',
        purpose_claim='token_use', purpose_value='access',
        role_mapping={'operator':['PUBLICATION_MANAGE']}, service_roles=[],
        cache_seconds=300, refresh_seconds=30, timeout_seconds=3.0)
    assert config.model_dump(mode='json') == original
    assert config.model_dump_json() == json.dumps(original, separators=(',', ':'))
    assert entra[0].config.model_dump()['token_profile'] == 'entra_v2'
    assert OIDCSettings.model_validate_json(config.model_dump_json()) == config


def test_l1_authority_remains_registered_and_scoped(entra, tmp_path):
    verifier, token, _, _ = entra
    principal = verifier.verify(token())
    authority = SecurityAuthority(tmp_path / 'security.sqlite')
    with pytest.raises(SecurityError):
        authority.authorize(principal, Action.PUBLICATION_MANAGE)
    authority.register(principal)
    authority.authorize(principal, Action.PUBLICATION_MANAGE)
    authority.authorize(principal, Action.SESSION_READ, principal.scope)
    with pytest.raises(SecurityError):
        authority.authorize(principal, Action.TENANT_ADMIN)
    other = verifier.verify(token({'sub':'bob'}))
    assert other.scope.owner != principal.scope.owner
    with pytest.raises(SecurityError):
        authority.authorize(principal, Action.SESSION_READ, other.scope)


def test_dotenv_json_profile_loads(entra, tmp_path):
    # Only synthetic public identifiers enter this temporary .env fixture.
    env = tmp_path / '.env'
    env.write_text("OIDC_CONFIGURATION='" + entra[0].config.model_dump_json() + "'\n")
    values = configured(tmp_path)
    values.pop('OIDC_CONFIGURATION')
    values['_env_file'] = env
    assert OIDCSettings.model_validate(Settings(**values).OIDC_CONFIGURATION) == entra[0].config
