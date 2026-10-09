"""Explicit reference authority construction; no cloud discovery/provisioning."""
from pathlib import Path

from governance.ledger import GovernanceLedger, PricingCatalog, QuotaPolicy
from llm.admission import AdmissionPolicy, SQLiteInferenceAdmission
from security.authority import SecurityAuthority
from security.identity import OIDCSettings, OIDCVerifier


class SecurityRuntime:
    def __init__(self, configuration):
        self.authority=SecurityAuthority(configuration.SECURITY_AUTHORITY_PATH)
        self.verifier=OIDCVerifier(OIDCSettings.model_validate(configuration.OIDC_CONFIGURATION))
        self.governance=GovernanceLedger(configuration.GOVERNANCE_AUTHORITY_PATH,
            QuotaPolicy.model_validate(configuration.GOVERNANCE_POLICY),
            PricingCatalog.model_validate(configuration.GOVERNANCE_PRICING))
        self.admission=SQLiteInferenceAdmission(Path(configuration.GOVERNANCE_PROVIDER_PATH),
            configuration.GOVERNANCE_PROVIDER_KEY,AdmissionPolicy.model_validate(configuration.GOVERNANCE_PROVIDER_POLICY))

    def ready(self):
        return (self.authority.ready() and self.governance.ready()
                and self.admission.ready() and self.verifier.ready())
