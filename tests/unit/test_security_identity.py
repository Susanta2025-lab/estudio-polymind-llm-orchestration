"""Synthetic keys generated in memory; no deployed identity/credential material."""
import json
import time

from cryptography.hazmat.primitives.asymmetric import rsa, ec
import jwt
import pytest

from security.identity import OIDCSettings, OIDCVerifier
from security.models import Principal, SecurityError, Action, _verified_principal, session_key


@pytest.fixture
def identity():
    key = rsa.generate_private_key(public_exponent=65537,key_size=2048)
    jwk = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(key.public_key()))
    jwk.update(kid='test-key',alg='RS256',use='sig')
    config = OIDCSettings(issuer='https://identity.invalid',audience='polymind',jwks_url='https://identity.invalid/keys',
                          role_mapping={'operator':(Action.PUBLICATION_MANAGE,)})
    fetched=[]
    def fetch():
        fetched.append(True)
        return {'keys':[jwk]}
    verifier=OIDCVerifier(config,fetch=fetch)
    claims={'iss':config.issuer,'aud':config.audience,'sub':'alice','tid':'tenant-a',
            'exp':int(time.time())+3600,'nbf':int(time.time())-1,'token_use':'access'}
    def token(changes=None,headers=None,signing_key=None,algorithm='RS256'):
        payload={**claims,**(changes or {})}
        payload={k:v for k,v in payload.items() if v is not None}
        return jwt.encode(payload,signing_key or key,algorithm=algorithm,headers=headers or {'kid':'test-key'})
    return verifier,token,jwk,fetched


def test_valid_immutable_server_scope_and_cache(identity):
    verifier,token,_,fetched=identity
    p=verifier.verify(token({'roles':['operator','self-declared-admin']}))
    assert p.permissions == frozenset({Action.PUBLICATION_MANAGE})
    assert verifier.verify(token()).scope == p.scope
    assert len(fetched)==1
    with pytest.raises(Exception): p.subject='bob'
    with pytest.raises(SecurityError): Principal('issuer','sub','tenant',frozenset(),'user',int(time.time())+99)
    assert verifier.verify(token({'owner':'forged','tenant':'forged'})).scope == p.scope


@pytest.mark.parametrize('changes',[
    {'exp':1},{'nbf':4102444800},{'iss':'https://foreign.invalid'},{'aud':'foreign'},
    {'sub':None},{'sub':''},{'sub':42},{'tid':None},{'tid':[]},
    {'token_use':'id'},{'token_use':None},{'exp':'4102444800'}, {'nbf':False},
    {'roles':'operator'},{'roles':[{}]}, {'roles':['x']*33},
])
def test_invalid_claims(identity,changes):
    verifier,token,_,_=identity
    with pytest.raises(SecurityError): verifier.verify(token(changes))


@pytest.mark.parametrize('header',[
    {'kid':'unknown'},{'kid':[]},{'kid':'test-key','jku':'https://attacker.invalid/keys'},
    {'kid':'test-key','x5u':'https://attacker.invalid/cert'}, {'kid':'test-key','jwk':{}},
    {'kid':'test-key','crit':['unknown']},{'kid':'test-key','typ':'id+jwt'},
])
def test_untrusted_headers(identity,header):
    verifier,token,_,_=identity
    encoded=token()
    parts=encoded.split('.')
    parts[0]=jwt.utils.base64url_encode(json.dumps({'alg':'RS256','typ':'JWT',**header}).encode()).decode()
    with pytest.raises(SecurityError): verifier.verify('.'.join(parts))


def test_signature_algorithm_and_key_confusion(identity):
    verifier,token,jwk,_=identity
    foreign=rsa.generate_private_key(public_exponent=65537,key_size=2048)
    for encoded in (token(signing_key=foreign), token(algorithm='HS256',signing_key='test-only-secret-32-characters-long'),
                    jwt.encode({'sub':'alice'},None,algorithm='none',headers={'kid':'test-key'}),
                    token(algorithm='ES256',signing_key=ec.generate_private_key(ec.SECP256R1()))):
        with pytest.raises(SecurityError): verifier.verify(encoded)
    verifier._keys={};verifier._loaded=None;verifier._attempted=None
    jwk['kty']='EC'
    with pytest.raises(SecurityError): verifier.verify(token())


@pytest.mark.parametrize('value',['','static-shared-bearer','a.b.c','x'*16385])
def test_malformed_oversized_and_static_tokens(identity,value):
    with pytest.raises(SecurityError): identity[0].verify(value)


def test_unavailability_rotation_and_expired_cache(identity):
    verifier,token,jwk,fetched=identity
    now=[0.]
    verifier.clock=lambda:now[0]
    verifier.verify(token())
    replacement=rsa.generate_private_key(public_exponent=65537,key_size=2048)
    new=json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(replacement.public_key()))
    new.update(kid='new',alg='RS256')
    verifier.fetch=lambda:{'keys':[new]}
    now[0]=31
    verifier.verify(token(headers={'kid':'new'},signing_key=replacement))
    with pytest.raises(SecurityError): verifier.verify(token())
    verifier.fetch=lambda:(_ for _ in ()).throw(OSError('private-url'))
    now[0]=400
    with pytest.raises(SecurityError,match='authentication_required'):
        verifier.verify(token(headers={'kid':'new'},signing_key=replacement))


def test_scope_domain_separation_and_session_identity():
    make=lambda issuer,tenant,subject:_verified_principal(issuer,subject,tenant,expires=int(time.time())+3600)
    people=[make('issuer','a','alice'),make('issuer','a','bob'),make('issuer','b','carol'),make('other','a','alice')]
    assert len({p.scope.owner for p in people})==4
    assert len({session_key(p,'session-123') for p in people})==4
    assert people[0].scope.tenant==people[1].scope.tenant
    assert people[0].scope.tenant!=people[3].scope.tenant
