"""Explicit RS256 access-token contract; no discovery or token-controlled URLs."""
import json
import threading
import time
from typing import Protocol
from urllib.parse import urlsplit

import httpx
import jwt
from pydantic import Field, model_validator

from documents.models import FrozenModel
from security.models import Action, Principal, SecurityError, _verified_principal


class IdentityVerifier(Protocol):
    def verify(self, access_token: str) -> Principal: ...


class OIDCSettings(FrozenModel):
    issuer: str = Field(min_length=1, max_length=2048)
    audience: str = Field(min_length=1, max_length=512)
    jwks_url: str = Field(min_length=1, max_length=2048)
    tenant_claim: str = Field(default='tid', pattern=r'^[A-Za-z][A-Za-z0-9_]{0,63}$')
    roles_claim: str = Field(default='roles', pattern=r'^[A-Za-z][A-Za-z0-9_]{0,63}$')
    # Explicit access-token discriminator prevents ID-token substitution.
    purpose_claim: str = Field(default='token_use', pattern=r'^[A-Za-z][A-Za-z0-9_]{0,63}$')
    purpose_value: str = Field(default='access', min_length=1, max_length=64)
    role_mapping: dict[str, tuple[Action, ...]] = Field(default_factory=dict)
    service_roles: tuple[str, ...] = ()
    cache_seconds: int = Field(default=300, ge=1, le=3600)
    refresh_seconds: int = Field(default=30, ge=1, le=300)
    timeout_seconds: float = Field(default=3, gt=0, le=10)

    @model_validator(mode='after')
    def trusted_urls(self):
        for url in (self.issuer, self.jwks_url):
            p = urlsplit(url)
            if p.scheme != 'https' or not p.hostname or p.username or p.password or p.fragment:
                raise ValueError('OIDC anchors require explicit HTTPS URLs')
        if len({self.tenant_claim, self.roles_claim, self.purpose_claim, 'sub', 'iss', 'aud', 'exp', 'nbf'}) != 8:
            raise ValueError('OIDC claim mappings must be distinct')
        if len(self.role_mapping) > 32 or len(self.service_roles) > 32:
            raise ValueError('OIDC role mapping too large')
        return self


class OIDCVerifier:
    def __init__(self, configuration, *, fetch=None, clock=time.monotonic):
        self.config = OIDCSettings.model_validate(configuration.model_dump())
        self.fetch = fetch or self._fetch
        self.clock = clock
        self._lock = threading.Lock()
        self._keys, self._loaded, self._attempted = {}, None, None

    def _fetch(self):
        # No redirects, environment proxies or arbitrary URLs. Bound bytes and total time.
        started = time.monotonic()
        with httpx.Client(timeout=self.config.timeout_seconds, follow_redirects=False, trust_env=False) as client:
            with client.stream('GET', self.config.jwks_url) as response:
                response.raise_for_status()
                data = bytearray()
                for chunk in response.iter_bytes(chunk_size=1024):
                    data.extend(chunk)
                    if len(data) > 65536 or time.monotonic() - started > self.config.timeout_seconds:
                        raise SecurityError('security_unavailable')
        return json.loads(data)

    def _key(self, kid):
        with self._lock:
            now = self.clock()
            expired = self._loaded is None or now - self._loaded >= self.config.cache_seconds
            if expired or kid not in self._keys:
                if self._attempted is None or now - self._attempted >= self.config.refresh_seconds:
                    self._attempted = now
                    raw = self.fetch()
                    if not isinstance(raw, dict) or not isinstance(raw.get('keys'), list) or not 1 <= len(raw['keys']) <= 32:
                        raise SecurityError('security_unavailable')
                    keys = {}
                    for item in raw['keys']:
                        if not isinstance(item, dict):
                            raise SecurityError('security_unavailable')
                        key_id = item.get('kid')
                        if type(key_id) is not str or not 1 <= len(key_id) <= 128 or key_id in keys:
                            raise SecurityError('security_unavailable')
                        if (item.get('kty') != 'RSA' or item.get('alg', 'RS256') != 'RS256'
                                or item.get('use', 'sig') != 'sig' or item.get('key_ops', ['verify']) != ['verify']
                                or any(k in item for k in ('d', 'p', 'q', 'jku', 'x5u', 'k'))):
                            raise SecurityError('security_unavailable')
                        if (type(item.get('n')) is not str or not 256 <= len(item['n']) <= 1400
                                or type(item.get('e')) is not str or not 1 <= len(item['e']) <= 16):
                            raise SecurityError('security_unavailable')
                        key = jwt.PyJWK.from_dict(item, algorithm='RS256').key
                        if key.key_size < 2048 or key.key_size > 8192:
                            raise SecurityError('security_unavailable')
                        keys[key_id] = key
                    self._keys, self._loaded = keys, now
                if self._loaded is None or now - self._loaded >= self.config.cache_seconds:
                    raise SecurityError('security_unavailable')
            if kid not in self._keys:
                raise SecurityError('authentication_required')
            return self._keys[kid]

    def verify(self, access_token):
        try:
            if type(access_token) is not str or not 1 <= len(access_token) <= 16384:
                raise ValueError()
            header = jwt.get_unverified_header(access_token)
            if (header.get('alg') != 'RS256' or header.get('typ') not in {'JWT', 'at+jwt'}
                    or set(header) - {'alg', 'kid', 'typ'}
                    or type(header.get('kid')) is not str or not 1 <= len(header['kid']) <= 128):
                raise ValueError()
            c = self.config
            claims = jwt.decode(access_token, self._key(header['kid']), algorithms=['RS256'],
                                issuer=c.issuer, audience=c.audience,
                                options={'require': ['iss', 'aud', 'sub', 'exp', 'nbf', c.tenant_claim, c.purpose_claim]})
            if (type(claims['exp']) is not int or type(claims['nbf']) is not int
                    or claims['nbf'] >= claims['exp'] or claims[c.purpose_claim] != c.purpose_value):
                raise ValueError()
            roles = claims.get(c.roles_claim, [])
            if not isinstance(roles, list) or len(roles) > 32 or any(type(r) is not str or len(r) > 128 for r in roles):
                raise ValueError()
            permissions = frozenset(a for r in roles for a in c.role_mapping.get(r, ()))
            return _verified_principal(c.issuer, claims['sub'], claims[c.tenant_claim], permissions,
                'service' if set(roles).intersection(c.service_roles) else 'user', claims['exp'])
        except Exception:
            # No raw claims/token/JWKS/transport exception may escape.
            raise SecurityError('authentication_required') from None

    def ready(self):
        try:
            self._key(next(iter(self._keys),'__readiness__'))
        except Exception:
            pass
        return bool(self._keys) and self._loaded is not None and self.clock()-self._loaded < self.config.cache_seconds
