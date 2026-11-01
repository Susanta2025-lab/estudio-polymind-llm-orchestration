# Phase 17H-L — final operator authorization

> Publication note — 1 November 2026: this document preserves a historical checkpoint. Private locations and environment identifiers are symbolic where shown; original dates, decisions and outcomes are retained. Historical handoffs are inactive and must not be run. See [Attempt 6 closure](phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md) for the later accepted single-call result and remaining Phase 17H gates.

2026-10-15 — **NO-GO — OPERATOR ACTION REQUIRED.** Technical readiness is retained.
The user has requested the real L1 experiment under an incremental EUR 5 ceiling;
that authorization does not substitute for the separately reviewed RS256 approval.
No inference, signing, token acquisition or cloud operations occurred in this task.

## A. Completed requirements

| Requirement | Evidence and result |
| --- | --- |
| Deployment and allocation | Existing private `azure-quota-evidence.json`: target deployment/model/version, GlobalStandard, succeeded; 30 RPM / 30,000 TPM. `quota_verified=true` preserved. No quota rediscovery. |
| Credential handling and target | Presence-only check: existing API key present in mode-0600 `.env`; endpoint matches configured resource. Launcher retains `api_key` / `api-key` and both logical roles use the same deployment. Authority/acceptance are distinct unresolved questions. |
| Four-call scope | Existing launcher/workflow inspected: three digestion requests and one grounded Q&A on generated four-page PDF; four maximum, one outstanding, at least 61-second spacing, no retries/fallback/L2. |
| Local execution | Pinned MiniLM tree hash verified unchanged; local-only CPU embeddings and isolated Chroma retained. OIDC-authorized retrieval pin correction remains present. No new paid cloud resources required by this composition. |
| Known consumers | Operator-established facts reused: dedicated PolyMind deployment; ECI separate; AKS scaled two to zero. No restart or cloud mutation. These facts do not enumerate all external consumers. |
| Financial authorization/source | EUR 5 incremental ceiling and existing calculation catalog approved by operator. `contract.price_source` now identifies catalog `phase17hl-pricing-eur-202610/1`, effective 2026-10-01, and this operator approval. Catalog/rates unchanged. |
| RSA consistency | Operator manually derived matching public fingerprints from both keys: `35785596dd2f38a3ae5fc8eeb93015a1ba3c8b4f16f06a1d73fbe521f9657816`. PASS for consistency only; private key never opened by Codex. |
| Retention/review | Approved 90 days after execution, existing private audit directory, operator cleanup owner and human output reviewer. Review is independent of generation, not third-party review. Preserve legal evidence, replay records and unresolved obligations. |
| Authority preservation | Before/after hashes, modes and modification times match for three authorities, trust, public key and `.env`. Replay directory remains empty/unchanged; audit remains empty. |

The private packet and attestations now preserve these decisions and supersede
stale instructions asking to reapprove quota or retention. The previous ambiguous
“provenance and execution signature: separately verified/approved” statement is
explicitly clarified as an outstanding requirement, not completed evidence.

October 2026 Azure billing is reused only as operator-reported historical baseline
context. No invoice/export was identified in the inspected packet and reports;
no historical amount or tariff is invented. The calculation source is the existing
operator-approved EUR catalog, not a newly verified Azure quote. Historical
AKS/Redis baseline costs are excluded; this exclusion cannot establish that new
network, storage, local compute, service or logging charges are zero.

## B. Unresolved operator actions

| Field or requirement | Existing evidence / why unresolved | Minimum operator action |
| --- | --- | --- |
| `credential_audience_verified` | Key presence and exact resource configuration are verified; neither proves the key's resource authority. No live acceptance test performed. | Record non-secret provenance confirming this existing key came from this resource and is authorized for this deployment; then set true. Attest resource authority, not live-verified acceptance. No inference probe needed. |
| `shared_consumers_verified` | Dedicated deployment, separate ECI deployment and AKS zero are established. Local ledger cannot control scripts, playgrounds or other processes; owner/tenant four-request budget is fully reserved by L1. | Review remaining consumers and attest none will use the deployment or L1 owner/tenant budget during this run; then set true. Exact statement is in the private packet. |
| `contract.fixed_cost`, `contract.extra_cost`, `charges_verified`, `contract.approved` | Ceiling/catalog authorized, but aggregate L1-only non-token bounds and their bases are absent. | Record defensible aggregate EUR bounds covering attributable local CPU/storage, networking and services, excluding existing AKS/Redis baseline. Review complete contract; only then set the two approval flags. Zero requires a supported absence of attributable charges. |
| `credential_valid_until`, `approval_expires` | No launch/signing time fixed. API keys have no JWT expiration claim. | Immediately before review/signing, explicitly adopt an operator-defined credential-use deadline and approval expiry, e.g. integer UTC `int(time.time()) + 1800` for each, with prompt launch as described below. |
| Fresh `POLYMIND_L1_OPERATOR_TOKEN` | Existing Entra identity/authority retained; current token not acquired or verified. | Operator uses existing approved interactive delegated flow and secure environment procedure; request `api://<ENTRA_API_CLIENT_ID>/access_as_user`. No new client/consent or manufactured token. |
| Signing-key provenance / independent review | Matching fingerprints establish pair consistency, not association with the trusted operator. | Confirm association through the existing independent provenance procedure; independently review complete configuration and generated bindings, then unlock/sign locally with the existing key. |

Catalog arithmetic: `0.11351636747626 + fixed_cost + extra_cost <= 5` EUR.
Thus fixed plus additional upper bounds must be at most **EUR 4.88648363252374**.
The total cannot yet be certified. The remainder is an allowance, not an estimate
or justification for inserting that amount as a cost bound.

## C. Final approval readiness

- **Configuration validation: FAIL, expected.** Actual `load_configuration` rejected
  seven field locations: `credential_valid_until`, `credential_audience_verified`,
  `shared_consumers_verified`, `charges_verified`, `approval_expires`,
  `contract.fixed_cost`, `contract.extra_cost`. `contract.approved=false` also
  remains a gate; nested field failures prevent its model validator being reached.
- **Unsigned review: blocked.** Existing helper preserved; no unsigned review or
  digest generated. There is no final validated configuration digest or binding
  to present honestly while these values and the verified fresh identity are absent.
- **Independent signing: not ready.** Complete the above evidence, time window and
  provenance review first. No signed approval issued or consumed.
- **Launcher acceptance: currently blocked.** A future matching, unexpired RS256
  approval plus fresh verified operator token and complete configuration can be
  evaluated by the existing launcher; service acceptance is not certified offline.

Choose deadlines only when ready to sign. With both set to finalization time plus
1800 seconds, sign promptly and launch within ten minutes of finalization. Ensure
more than ten minutes remain at launch and enough time for local preparation and
the whole four-call window. Identity token must also cover the run. Approval `exp`
must equal the reviewed configuration expiry and be within 86400 seconds of `iat`.
If delayed, revise deadlines and repeat review; any post-signing configuration
change invalidates approval and requires fresh independent review/signing.

## D. Execution handoff — operator only

Use the existing private packet:
`<PRIVATE_OPERATOR_DIRECTORY>/OPERATOR_PACKET.md`.
It contains exact pending attestation statements, credential environment handling,
unsigned binding review and the existing RS256 payload/signing procedure. The
repository documents the approved Entra scope/flow, but no established acquisition
command was found to repeat; do not substitute an ARM token or invent a login client.
Never put tokens, passphrases or key contents in commands, logs, chat or Git.

After completing the fields and obtaining the fresh operator token, run from the
repository root with the existing project interpreter:

```text
PYTHONPATH=. python "<PRIVATE_OPERATOR_DIRECTORY>/prepare_unsigned_review.py"
```

The helper validates configuration, verifies identity/trust and existing authority,
then exclusively writes `unsigned-review.json` and `configuration.sha256`. It may
fetch Entra public keys and append an authorization audit entry when the operator
runs it. It does not sign or consume. Review the whole configuration and exact
binding: digest, operator identity/owner, target/model, EUR budget, token/call/rate
limits and expiry. Do not replace the digest with a raw-file hash.

Confirm signing-key provenance, unlock the existing passphrase-protected key
locally, and independently use the existing PyJWT RS256 procedure in the packet
and [approval runbook](../../evaluation/phase_17hl_operator_approval.md). Preserve
the exact reviewed header/binding, fresh UUID, integer `iat`/`nbf`/`exp`, live purpose
and prescribed issuer/audience. Securely save only the compact JWS in
`operator-approval.jwt`, mode 0600 with restrictive umask and exclusive creation.
Preserve trust and replay records. Do not overwrite an earlier review blindly.

After those gates pass, with both runtime secrets securely in the environment,
the exact existing four-call launch command is:

```text
python -m tests.performance.foundry_l1 --live \
  --configuration "<PRIVATE_OPERATOR_DIRECTORY>/l1-configuration.json" \
  --approve-sha256 "$(cat "<PRIVATE_OPERATOR_DIRECTORY>/configuration.sha256")" \
  --approval "<PRIVATE_OPERATOR_DIRECTORY>/operator-approval.jwt" \
  --approval-trust "<PRIVATE_TRUST_DIRECTORY>/approval-trust.json"
```

Not executed. Failed starts can consume approval; retain all replay/run markers
and financial obligations. Review actual outputs and citations after execution.
No automatic retries or L2 progression.

## E. Safety accounting and verification

| Item | This task |
| --- | --- |
| Live model requests / incremental inference spend | 0 / EUR 0 |
| Azure resource changes / AKS restarts | 0 / 0 |
| Authority, ledger, trust or replay mutations | 0; six protected files and empty replay verified unchanged |
| Signed approvals issued / consumed | 0 / 0 |
| Signing-key access / token acquisition | 0 / 0 |
| Private changes | Existing packet and attestation document updated; only configuration `contract.price_source` populated. All three files remain 0600. Unsupported flags remain false. |
| Git changes from this task | This report only; previous working-tree changes preserved. No commit, push, staging or remote mutation. |

Focused read-only checks confirmed expected validation rejection, exact Decimal
cost arithmetic, protected-file preservation, empty audit/replay, absent approval
artifacts, unchanged embedding hash and private modes. No implementation changed;
no regression suite, inference rehearsal, Docker build or broad cost investigation
was rerun. Self-review checked field evidence, signing/identity separation, expiry
rules, consumer scope and cost exclusions. Separate pre-commit review found no
secrets, replacement authorities, implementation/API changes or new dependencies
introduced by this task. Temporary snapshot/update tooling remains outside Git.

Final `git diff --check`: passed. `git diff --stat`: existing 10 tracked files,
138 insertions and 8 deletions, unchanged from task start; the new report is
untracked and therefore absent from that statistic. `git status --short`: existing
10 modified tracked files and 28 prior untracked files, plus this report (29
untracked). No commit or push occurred.
