"""Fixed Phase 19B browser/API trust, independent verification and minimal evidence."""

from datetime import datetime, timezone

import jwt

from security.identity import OIDCSettings, OIDCVerifier
from security.models import SecurityError

ORIGIN = "https://polymind.test:9443"
TENANT = "afabeaf8-0fea-42c9-afb4-7e5c07eff3f3"
API_CLIENT = "5aa70f9d-9f9e-4b5b-972b-698d4d68105e"
BROWSER_CLIENT = "a43f5479-4cbd-45a0-86e0-9c658e77d133"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT}"


def settings():
    return OIDCSettings(
        token_profile="entra_v2",
        tenant_id=TENANT,
        audience=API_CLIENT,
        issuer=AUTHORITY + "/v2.0",
        jwks_url=AUTHORITY + "/discovery/v2.0/keys",
    )


def validate_auth(values):
    """No discovery; reject extra providers, overrides, token exposure or placeholders."""
    try:
        auth = values["auth"]
        if (
            set(values) != {"auth"}
            or set(auth)
            != {
                "redirect_uri",
                "server_metadata_url",
                "client_id",
                "client_secret",
                "cookie_secret",
                "expose_tokens",
                "client_kwargs",
            }
            or auth["redirect_uri"] != ORIGIN + "/oauth2callback"
            or auth["server_metadata_url"]
            != AUTHORITY + "/v2.0/.well-known/openid-configuration"
            or auth["client_id"] != BROWSER_CLIENT
            or auth["expose_tokens"] != ["access"]
            or auth["client_kwargs"]
            != {"scope": f"openid api://{API_CLIENT}/access_as_user"}
        ):
            raise ValueError()
        for name, minimum in (("client_secret", 16), ("cookie_secret", 64)):
            value = auth[name]
            if (
                type(value) is not str
                or not minimum <= len(value) <= 4096
                or any(ord(c) < 33 or ord(c) > 126 for c in value)
                or any(
                    s in value.lower()
                    for s in ("<", ">", "placeholder", "supplied", "changeme")
                )
            ):
                raise ValueError()
        if auth["client_secret"] == auth["cookie_secret"]:
            raise ValueError()
    except Exception:
        raise SecurityError("security_configuration") from None


class BootstrapVerifier:
    def __init__(self, *, fetch=None):
        self.verifier = OIDCVerifier(settings(), fetch=fetch)

    def verify(self, token):
        principal = self.verifier.verify(token)
        try:
            # This exact immutable string has ALREADY passed cryptographic verification
            # and all production claim checks above. No unverified-token path reaches here.
            claims = jwt.decode(token, options={"verify_signature": False})
            if claims.get("azp") != BROWSER_CLIENT:
                raise ValueError()
            return principal
        except Exception:
            raise SecurityError("authentication_required") from None


def candidate(principal):
    def utc(seconds):
        return (
            datetime.fromtimestamp(seconds, timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        )

    return dict(
        schema_version="phase19b-enrollment-candidate/1",
        purpose="phase19b_identity_bootstrap",
        issuer=principal.issuer,
        tenant_id=principal.tenant_identity,
        subject=principal.subject,
        canonical_tenant_id=str(principal.scope.tenant),
        canonical_owner_id=str(principal.scope.owner),
        api_audience=API_CLIENT,
        verified_at_utc=utc(datetime.now(timezone.utc).timestamp()),
        token_expires_at_utc=utc(principal.expires),
        execution_authorized=False,
    )
