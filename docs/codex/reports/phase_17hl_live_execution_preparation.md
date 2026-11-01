# Phase 17H-L live execution preparation — 2026-10-15

> Publication note — 1 November 2026: this document preserves a historical checkpoint. Private locations and environment identifiers are symbolic where shown; original dates, decisions and outcomes are retained. Historical handoffs are inactive and must not be run. See [Attempt 6 closure](phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md) for the later accepted single-call result and remaining Phase 17H gates.

**NO-GO for live execution.** The private execution packet and audit directory are
prepared. Six external-evidence/timing values, four verification flags, financial
contract approval, fresh operator authentication and an independent signature
remain outstanding. No live invocation, provider request or approval generation
or consumption occurred. The completed readiness assessment was retained rather
than repeated.

## Configuration and private packet

Inspected the actual private draft, latest preflight handoff, approval procedure,
launcher, financial contract, approval verification, document workflow, retrieval
boundary and existing tests. The original seven null fields were
`credential_valid_until`, `approval_expires`, `audit_directory`,
`actual_azure_rpm`, `contract.price_source`, `contract.fixed_cost` and
`contract.extra_cost`. The flags `credential_audience_verified`, `quota_verified`,
`shared_consumers_verified`, `charges_verified` and `contract.approved` were false.

Prepared a separate configuration under the operator's existing private directory
`<PRIVATE_OPERATOR_DIRECTORY>/`, leaving the original draft
unchanged. Only `audit_directory` differs from that draft: it selects the new,
empty `audit/` subdirectory. Both directories are 0700, packet files 0600. The
execution sandbox approved this scoped private creation. The packet includes
`OPERATOR_PACKET.md`, `l1-configuration.json`, `verification.json`, and an
operator-only `prepare_unsigned_review.py`. No final digest, signed approval,
run ledger or live-started marker was created.

Verified .env endpoint/model map and API-key presence without exposing values.
The selected resource is epolymind-foundry-dev-susanta; endpoint is
https://epolymind-foundry-dev-susanta.openai.azure.com/openai/v1; authentication
selects api-key. General and summarization roles both select
 epolymind-gpt-54-mini, configured underlying model gpt-5.4-mini version
2026-03-17, GlobalStandard in spaincentral. This confirms configuration, not
current Azure deployment availability or credential access.

The exact workflow uses the existing four-page generated PDF, one chunk analysis,
one structural synthesis, one root synthesis, then one grounded page-one question.
It is not an arbitrary external PDF. Reservations remain 25,000 input/3,000 output
per call and 100,000/12,000 aggregate. EUR 5 excludes existing AKS/Redis baseline;
fixed/additional incremental costs still need upper bounds. Existing catalog token
arithmetic is EUR 0.11351636747626, not a fresh commercial quote. One outstanding
run call, 61-second spacing, no retry, no fallback and no L2 remain unchanged.

Existing Entra configuration, catalog, authority paths, trust and replay location
are reused. Hashes confirm .env, three authorities, trust and empty replay contents
still match the retained final-handoff evidence; before/after checks also cover
the original draft and present authority sidecars. The embedding tree hash matches
the configured pinned artifact. Prior actual CPU encoding/local Chroma validation
is retained; this preparation did not repeat model runtime readiness testing.

## Narrow retrieval correction

The targeted offline workflow initially stopped at the post-publication retrieval
check under the real .env's OIDC mode. `publish()` created an unauthenticated pin;
`PublicationReplica.validate_pin()` correctly rejected it. The same check exists
in the live composition and could stop after three billable digestion calls,
before the fourth Q&A call. Prior tests without .env did not expose this condition.

Changed only the performance workflow: pass the already verified document
principal into `publish()`, obtain the existing authority's document authorization
snapshot and attach it to the retrieval pin. No authentication bypass, production
API change, provider-specific domain logic, authority reset or new abstraction
was introduced. A regression test explicitly enables OIDC and requires every
validated pin to carry authorization while the full four-call L1 workflow
completes. This necessary preparation fix does not repeat the readiness assessment.

## Validation and reviews

The corrected targeted script ran under a Python network-denying audit hook.
It verified private artifact reuse, embedding hash, incomplete configuration
rejection, missing-approval rejection and the real extraction/planning/publication
workflow using synthetic HTTP/embeddings in isolated temporary rehearsal storage.
Three digestion calls plus one Q&A completed; no external request occurred.
Temporary synthetic authorities are distinct from the retained real authorities;
no approval fixtures, signing keys or approval consumption were used.

`python -m pytest -q tests/integration/test_foundry_offline_workflow.py -k 'not L2'`:
**4 passed, 1 deselected in 3.01 s**. This covers OIDC publication, the four-call
pipeline, unknown usage stopping and financial denial. L2 was not executed.
No full regression or Docker rebuild was needed for this localized preparation.

Self-review checked all consumers of the changed helper, principal ownership,
authorization revalidation, unchanged request count, failure behavior and private
packet content. Separate pre-commit review checked the added prompt/report and
changed workflow/test for secrets, signing operations, dependencies, temporary
artifacts, production API changes and unrelated modifications. The private
signing key was never opened. Existing unrelated working-tree edits are preserved.
Final compilation, whitespace and private-permission results are recorded below.

## Operator handoff and approval readiness

Only the following operator work remains:

1. Attest existing API-key authority/access and a conservative use deadline; supply
   actual Azure RPM (existing policy requires at least 2), attest 30,000 TPM and all
   shared consumers, then set the corresponding three verification flags.
2. Supply the source supporting the existing EUR catalog and defensible aggregate
   fixed/additional charge bounds. Approve the EUR 5 contract and charge flag;
   select retention period, cleanup owner and independent reviewer for the already
   prepared audit directory. Unknown charges cannot be assumed zero.
3. Confirm existing public-key fingerprint/provenance independently, obtain a fresh
   verified Entra access token, and choose approval expiry covering the run. Complete
   validation and review the exact configuration-bound unsigned material before an
   independent operator signs. Retain existing trust, replay and financial state.

The packet contains exact unsigned-review and RS256 signing instructions. The
helper calls `load_configuration` and `foundry_approval.bindings` after verified
identity and existing authority authorization; it does not sign or consume. It
has not been executed. When the operator executes it, OIDC may fetch public keys
and authorization may append an audit record. No final configuration digest can
truthfully be supplied until the unresolved fields are complete. Signing must
bind that validated serialization digest, exact identity/target/budget/limits and
expiry. Any later configuration change invalidates approval.

The packet explains how to map the existing .env key privately to
POLYMIND_L1_AZURE_CREDENTIAL and supply POLYMIND_L1_OPERATOR_TOKEN; neither runtime
variable is currently populated. The final command below is concrete but
intentionally unexecutable until its reviewed digest and signed artifact exist.
Run from the repository root with the existing project interpreter **only after
separate live authorization**:

```text
python -m tests.performance.foundry_l1 --live \
  --configuration <PRIVATE_OPERATOR_DIRECTORY>/l1-configuration.json \
  --approve-sha256 "$(cat <PRIVATE_OPERATOR_DIRECTORY>/configuration.sha256)" \
  --approval <PRIVATE_OPERATOR_DIRECTORY>/operator-approval.jwt \
  --approval-trust <PRIVATE_TRUST_DIRECTORY>/approval-trust.json
```

This command was not executed. No Azure resource action, AKS restart, billable
smoke test, ledger reset, commit or push occurred. Preserve replay/run markers
and obligations even if an independently authorized future attempt fails.

Final validation: repository `compileall` with an external bytecode cache and
`git diff --check` both exited 0. Private packet permissions, empty audit directory,
helper syntax and exactly one changed configuration field passed. Final protected
file hashes, modes and modification times match prior evidence; replay remains
unchanged. No final digest or approval file exists.

Final `git status --short`: 10 modified tracked files and 28 untracked files,
including preserved earlier work; none staged. `git diff --stat`: 10 tracked
files, 138 insertions and 8 deletions, unchanged from the initial tracked diff.
This command excludes untracked files: this task changed two existing untracked
workflow/test files and added its prompt/report. No commit or push occurred.
