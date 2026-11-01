# Phase 17H-L — final launch authorization

> Publication note — 1 November 2026: this document preserves a historical checkpoint. Private locations and environment identifiers are symbolic where shown; original dates, decisions and outcomes are retained. Historical handoffs are inactive and must not be run. See [Attempt 6 closure](phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md) for the later accepted single-call result and remaining Phase 17H gates.

2026-10-15 — **NO-GO — EXACT REMAINING BLOCKER:** a fresh delegated operator
access token is absent from this process. Obtain it through the existing approved
interactive authentication procedure, then execute the prepared local handoff.
No further credential-authority, consumer, budget or retention decision is needed.

## A. Authorization summary

The latest explicit operator confirmations are recorded in the existing private
`operator-attestations.md`. All verification flags are now true, including retained
`quota_verified=true`; `contract.approved=true`. Credential verification means
operator-attested resource authority, not tested live provider acceptance.
Shared-consumer verification records operator exclusivity, not local-ledger control
of external processes. AKS stays paused; ECI uses its separate deployment.

The approved scope remains GPT-5.4 mini, deployment `epolymind-gpt-54-mini`, three
PDF digestion calls and one grounded Q&A, maximum four, one outstanding request,
61-second minimum spacing, no retries/fallback/L2. Existing local WSL MiniLM/Chroma,
OIDC retrieval authorization, authorities, API-key configuration, 30 RPM / 30,000
TPM allocation and approved EUR catalog/source remain unchanged.

`fixed_cost=0` reflects no new provisioning, rental or fixed service charge.
`extra_cost=0` reflects the operator-confirmed absence of separately billed cloud
networking, storage, embedding or other services in this local execution design.
Existing local hardware/storage and AKS/Redis baseline are not incremental service
purchases. This does not claim electricity or hardware wear has zero economic value.
Total reserved billed cost: **EUR 0.11351636747626 <= EUR 5**. No invented allowance,
new tariff, ledger policy change or broad cost investigation was introduced.

Retention is 90 days after execution; operator owns cleanup and human output review
in the existing private audit directory. Preserve legal evidence, replay records
and unresolved obligations. Review is independent of generation, not third-party.
RSA fingerprint consistency and operator-reported control are recorded; historical
provenance is not independently established. The existing signing procedure still
requires the operator to confirm the pinned key association during personal review.

## B. Final configuration

Actual `load_configuration` on the saved configuration: **FAIL only for the two
intentionally deferred timestamps**, `credential_valid_until` and `approval_expires`.
Actual `load_configuration` on an isolated temporary copy with both set to integer
UTC now+1800: **PASS**, including the exact four-call financial contract. That
projection is not the final reviewed configuration and its digest was not issued.

The private `operator_handoff.py prepare` authenticates the operator with more than
30 minutes of token lifetime, sets both deadlines to now+1800, then invokes the
unchanged `prepare_unsigned_review.py`. The API-key deadline is explicitly an
operator-defined use deadline, not an Azure expiry. Launch within ten minutes of
preparation, with more than ten minutes remaining. Approval expires within 24 hours
of signing. Delay or any configuration change requires fresh review/signature;
existing artifacts are never automatically overwritten or reset.

No unsigned-review/digest/approval artifact exists yet. Its exact binding must be
produced from the validated configuration and fresh verified identity, not copied
from trust metadata. It will cover the operator/owner scope, configured resource
v1 endpoint, deployment/model/version, GlobalStandard/spaincentral, EUR 5 ceiling
and zero fixed/extras, four attempts, 25K/3K per-call and 100K/12K aggregate token
bounds, one RPM, 30K TPM, 28K context and final expiry. The digest binds all remaining
configuration fields, catalog, policies, paths and pinned embedding hash.

## C. Operator signing — one local procedure

Use the existing approved delegated interactive authentication mechanism to obtain
an access token for `api://<ENTRA_API_CLIENT_ID>/access_as_user`, using
the existing client/consent. No established acquisition CLI command was present in
the inspected procedure; do not invent a client or substitute an ARM/Graph/ID token.
Keep the token out of chat, logs and literal shell commands. In the existing zsh
terminal, hidden input can securely populate its runtime environment:

```zsh
read -rs 'POLYMIND_L1_OPERATOR_TOKEN?Fresh delegated access token (hidden): '
export POLYMIND_L1_OPERATOR_TOKEN
```

From repository root with the project interpreter, execute personally:

```text
PYTHONPATH=. python "<PRIVATE_OPERATOR_DIRECTORY>/operator_handoff.py" prepare
# Independently review l1-configuration.json, unsigned-review.json and configuration.sha256.
PYTHONPATH=. python "<PRIVATE_OPERATOR_DIRECTORY>/operator_handoff.py" sign
PYTHONPATH=. python "<PRIVATE_OPERATOR_DIRECTORY>/operator_handoff.py" verify
```

The helper implements the existing [RS256 procedure](../../evaluation/phase_17hl_operator_approval.md):
explicit personal SIGN confirmation, hidden passphrase input, existing private key,
pinned-key comparison, exact reviewed header/bindings, fresh UUID and integer times.
It verifies with the existing `verify_approval` before exclusively saving the compact
JWS as mode-0600 `operator-approval.jwt`. `verify` checks it again without consumption.
Only the operator executes these actions; Codex did not open/unlock/sign with the key.
The prepare action can append the existing authority's normal authorization audit
entry. No helper action launches inference or calls approval consumption.
Actual signed-approval verification remains pending because no signature exists.

## D. L1 execution — only after successful independent signing/verification

Keep shell tracing disabled. Load the existing Azure key into the runtime environment
without printing it to the terminal or passing its value in command arguments:

```text
export POLYMIND_L1_AZURE_CREDENTIAL="$(python -c 'from dotenv import dotenv_values; print(dotenv_values(".env")["OPENAI_COMPATIBLE_API_KEY"], end="")')"
python -m tests.performance.foundry_l1 --live \
  --configuration "<PRIVATE_OPERATOR_DIRECTORY>/l1-configuration.json" \
  --approve-sha256 "$(cat "<PRIVATE_OPERATOR_DIRECTORY>/configuration.sha256")" \
  --approval "<PRIVATE_OPERATOR_DIRECTORY>/operator-approval.jwt" \
  --approval-trust "<PRIVATE_TRUST_DIRECTORY>/approval-trust.json"
```

Not executed. Four requests maximum; no extra smoke requests. Failed starts may
consume approval: retain replay markers and obligations, with no automatic retry.

## E. Safety accounting

Inference requests **0**; incremental inference spend **EUR 0**; cloud mutations,
AKS restarts, signing-key reads, approvals issued/consumed and authority/ledger/replay
mutations **0**. Six protected files (three authorities, trust, public key, `.env`)
retain hashes/modes/mtimes; replay and audit remain empty. Existing artifacts reused.

Private changes: three attestation flags, contract approval and two zero cost fields;
attestations/packet updated; operator-only helper added with mode 0600. Deadlines
remain unset pending authentication. Syntax parsing, actual configuration-loader
checks and protected-state comparisons passed as described above. Helper signing
was not executed or integration-tested with a key; no full regression was rerun.
Self-review checked secret handling, exclusive writes, expiry/binding checks and
absence of launch/consume calls. No production implementation or dependencies changed.

`git diff --check`: PASS. `git diff --stat`: prior 10 tracked files, 138 insertions,
8 deletions, unchanged. `git status --short`: 10 prior modified tracked files and
30 untracked files including this new report; previous work preserved. This task's
only repository addition is this report. **No commit or push.**
