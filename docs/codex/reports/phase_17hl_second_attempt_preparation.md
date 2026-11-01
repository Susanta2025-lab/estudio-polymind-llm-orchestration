# Phase 17H-L — second attempt preparation

> Publication note — 1 November 2026: this document preserves a historical checkpoint. Private locations and environment identifiers are symbolic where shown; original dates, decisions and outcomes are retained. Historical handoffs are inactive and must not be run. See [Attempt 6 closure](phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md) for the later accepted single-call result and remaining Phase 17H gates.

**NO-GO now.** Corrected generation is technically ready for another evaluation,
but a full new four-call maximum is not covered by the remaining October allowance.
A separate unsigned packet targets **1 November 2026, 00:00–01:00 UTC**, with
unchanged policies and authorities. This is a conservative full-envelope choice,
not a claim that every earlier per-call admission would be denied. An optional
window-preference question received no answer before preparation; the full-envelope
window was selected explicitly. No live execution was performed.

## Technical contract and narrowly scoped launcher changes

Verified `managed-prompt/2` in `ManagedSynthesisInference.profile`, every managed
stage profile, and the actual offline chunk, structural and root HTTP requests.
All generated schemas explicitly require default fields; the unchanged validator
still rejects canonical results above 3,000 bytes. The fourth call remains the
existing grounded Q&A contract, not a digestion prompt.

Added `generation_contract_sha256` to `LaunchConfiguration` and checked it during
validation/launch, before authority construction and approval consumption. The hash
covers the managed prompt, digestion models, Q&A prompt, structured capability
model, fixture profile, L1 composition and capability settings source files. Thus
configuration/signature binding now explicitly covers the current generation code;
it is not merely a deployment/budget digest. Any covered source change requires a
new review. This is source binding, not a hostile-host integrity mechanism.

Added `execution_not_before` to bind the selected window and reject premature launch
before any ledger or approval access. Defaults preserve configuration construction
for existing test callers; serialized digests change, so old signatures cannot
silently authorize the new contract. Historical artifacts were not rewritten.
No provider behavior, canonical limit, financial policy, retry or infrastructure
change was introduced. New job identities and the changed planning fingerprint
prevent reuse of the failed analysis; the existing run and consumed approval remain
untouched.

Private verification records exact fingerprints:

- Generation contract: `3da39a6b00a75a7f689a49e56a4dc3255576e0d16265a2d509f259f2d533e16f`
- Managed inference: `8e00a72d46bf6a633b3fed08bb1bb12bbd20860eef6eb6cd62d32c04edb26a5e`
- Digestion profile: `cd40340473e39f1eb9f4875cc25a53ef924e94b6cb19fd366d9ff75ac6afd358`
- New configuration: `28f4698cb9c050bf55ed93ddc36040d9d2febcd2cff08bd9db432e75b1163306`

## Authoritative accounting and eligibility

Read the original private audit and both shared SQLite authorities using read-only
connections; no ledger constructors or admission/reservation operations were used.
Authoritative policy/catalog serializations match the retained configuration.

There is exactly one governance reservation, **SETTLED**, with actual input 1,845,
output 1,460, total **3,305 tokens**, and **EUR 0.00699907602956752** actual cost.
Its original governance estimate was 10,052 input plus 3,000 output. The shared
provider row is inactive with outcome success. The original run guard retained
its historical 25,000/3,000 reservation row, but it is finished and belongs to the
old run only. There are no outstanding obligations requiring reconciliation.

Both owner and tenant policies permit four requests per rolling 86,400 seconds,
112,000 daily tokens, 112,000 monthly tokens and EUR 5 monthly cost. Settled usage
still counts toward these limits. The old request was created at
**2026-10-15 11:01:42.868029 UTC** and stops counting in the rolling window at
**2026-10-16 11:01:42.868029 UTC**. The old provider-minute reservation has already
expired. The new runtime continues to space calls by 61 seconds.

Today there are only three rolling request slots and 108,695 daily/monthly tokens
left. On 16 October the daily token counter no longer includes the old usage, but
October still has **108,695 monthly tokens remaining**. The new contract permits
100,000 input plus 12,000 output: **112,000 maximum**, exceeding remaining monthly
capacity by **3,305**. Actual governance reserves each rendered call and replaces
settled estimates with actual usage; it does NOT atomically reserve the whole run
ceiling. Consequently an October run after the rolling window clears could finish
if its actual/reserved per-call totals fit, or could stop at a later admission.
This packet deliberately does not depend on that outcome. Even a run begun slightly
before rolling expiry could place its fourth request after expiry; we do not use
that timing strategy.

Without changing policies, **1 November 00:00 UTC** is the first monthly boundary
that covers the complete new maximum from the observed state. This is a projection,
conditional on no intervening usage or unresolved reservations. The installed
read-only eligibility helper checks the full envelope against both scopes and
requires a clear provider window before signing/verification. It is a conservative
packet check, not a new authoritative ledger policy or reservation. The actual
launcher still enforces its original per-call admission and replay protections.

The operator may instead request a separately reviewed October packet accepting
possible per-call denial, or explicitly authorize a supported policy migration.
Simply editing policy JSON will not work: stored-policy equality is enforced.
Neither option was carried out; no token/ledger limit was raised or reset.

Cost arithmetic reuses the approved EUR catalog (no new pricing investigation):

| Measure | EUR |
|---|---:|
| New four-call maximum incremental reservation | 0.11351636747626 |
| Previous measured usage | 0.00699907602956752 |
| Combined previous actual + new maximum | 0.12051544350582752 |

The cost limit is not the blocker. Fixed/additional incremental charges remain the
previously attested zero. Historical cost is preserved even though its October
monthly accounting bucket expires in November.

## Private packet and independent operator work

Installed at:
`<PRIVATE_OPERATOR_DIRECTORY>/`

Contains a separate `l1-configuration.json`, empty `audit/`, exactly one
`unsigned-review.json`, `configuration.sha256`, `verification.json`,
`operator_handoff.py`, read-only `eligibility.py`, inherited-attestation note,
`OPERATOR_PACKET.md` and evidence hashes. Directories are 0700; files 0600.
No new run database, live marker, signed approval or replay marker exists.

Reused existing verified quota evidence, approved catalog, credential/resource
attestations, public RSA trust, replay directory and pinned local embeddings.
The old approval signature was verified historically using the public key with
expiration deliberately excluded solely for evidence inspection; its binding
matches the old unsigned review and its replay marker exists. It cannot authorize
another execution. The new unsigned review uses that historically verified identity
and pinned trust metadata; it makes no claim of fresh authentication. The signing
helper requires a fresh matching delegated identity before opening the private key.

New proposed approval/API-key use deadlines are **1 November 01:00 UTC**. The latter
is an operator-approved use window, not an Azure key expiration. Existing operational
attestations must still be true then. No new OAuth setup or broad readiness review
is necessary. The token needs over 30 minutes remaining for signing. Sign near the
selected start; launch before 00:50 UTC. Any expired window, covered source change,
configuration change or intervening blocking usage requires stopping and preparing
new reviewed material, not overwriting signed evidence.

From the repository root with the existing project interpreter, after obtaining the
fresh token using the established delegated authentication procedure (keep tracing
disabled):

```zsh
read -rs 'POLYMIND_L1_OPERATOR_TOKEN?Fresh delegated access token (hidden): '
export POLYMIND_L1_OPERATOR_TOKEN
```

At/after the selected window start, personally run:

```text
PYTHONPATH=. python "<PRIVATE_OPERATOR_DIRECTORY>/eligibility.py"
PYTHONPATH=. python "<PRIVATE_OPERATOR_DIRECTORY>/operator_handoff.py" sign
PYTHONPATH=. python "<PRIVATE_OPERATOR_DIRECTORY>/operator_handoff.py" verify
```

Review the full configuration and unsigned bindings independently before typing
SIGN. Existing RS256 trust and hidden passphrase input are reused; a fresh UUID is
created only during personal signing. Verification does not consume approval.

Exact eventual launch, **not executed**:

```text
export POLYMIND_L1_AZURE_CREDENTIAL="$(python -c 'from dotenv import dotenv_values; print(dotenv_values(".env")["OPENAI_COMPATIBLE_API_KEY"], end="")')"
python -m tests.performance.foundry_l1 --live \
  --configuration "<PRIVATE_OPERATOR_DIRECTORY>/l1-configuration.json" \
  --approve-sha256 "$(cat "<PRIVATE_OPERATOR_DIRECTORY>/configuration.sha256")" \
  --approval "<PRIVATE_OPERATOR_DIRECTORY>/operator-approval.jwt" \
  --approval-trust "<PRIVATE_TRUST_DIRECTORY>/approval-trust.json"
```

## Validation, review and repository state

Network-blocked focused run: **67 passed, one L2 case deselected** (managed inference,
launcher and offline L1 workflow). After adding assertions for every actual digestion
stage, launcher plus approval checks: **93 passed**. These counts overlap; they are
two test runs, not 160 distinct tests. RSA activity in these automated tests uses
isolated test keys/artifacts only, never the real operator key or replay directory.

Installed configuration load/digest, unsigned bindings, file modes, helper syntax,
empty audit directory and absent signature checks passed. Read-only eligibility is
false now and true at the selected future boundary against the same observed state.
All **29 protected files** covering the old packet/audit, authoritative databases,
trust and replay evidence retained their SHA-256 hashes. No original artifacts or
financial records were changed. The private installer required filesystem sandbox
approval. Its first login-shell invocation stalled and was cancelled; the same
exclusive installer completed without login-shell initialization.

`git diff --check` and focused `compileall` passed with external bytecode cache.
Self-review checked binding order, pre-consumption rejection, full-envelope versus
actual admission semantics, read-only connections and exclusive packet writes.
Separate pre-commit review found no private tokens, signing keys, raw model content,
new dependencies, generated repository artifacts or unrelated edits introduced.
No full-suite, Azure, Docker, infrastructure, model-runtime or L2 assessment was run.

This task edits the already-untracked `tests/performance/foundry_l1.py` and
`tests/integration/test_foundry_l1_launcher.py`, adds this prompt/report, and creates
the new private packet. Existing uncommitted work is preserved. `git diff --stat`
for tracked work remains 12 files, 211 insertions and 12 deletions; it excludes these
untracked files. `git status --short` records the existing dirty worktree plus the
new prompt/report. **No commit or push occurred.**

## Resumed-session completion record — 2026-10-15

**SECOND L1 ATTEMPT PREPARATION COMPLETE — AWAITING ELIGIBILITY**

**A. Recovery status.** The previous final file-writing operation completed
successfully. The task prompt, this report (including exact signing/verification
and launch commands), and installed private packet are complete. No partial file
or unfinished implementation was found. This resumed session inspected Git state,
confirmed packet presence and added only this completion record. The outstanding
work was the final operator handoff, not another preparation or test run.

**B. Retained evidence.** Accept the completed **67 passed** and **93 passed** runs;
no tests or rehearsals were rerun. The prior before/after evidence establishes
**29 protected files unchanged**, including original audit, governance, trust and
replay records. This session did not reopen those ledgers or repeat that investigation;
it read the existing evidence manifest and left all protected records untouched.

**C. Readiness.** The verified `managed-prompt/2` correction remains the prepared
contract. The separate `run-20261101-attempt2` packet and unsigned review exist;
its audit directory is still empty and its signed approval is absent. Loading the
saved configuration and recomputing its validated digest confirmed it still equals
`28f4698cb9c050bf55ed93ddc36040d9d2febcd2cff08bd9db432e75b1163306`, matching the saved
digest and unsigned binding. No configuration or approval material was regenerated.

Execution remains **NO-GO now**. From the retained ledger evidence, one settled
request counts toward the four-request rolling window, and 3,305 consumed October
tokens leave 108,695 of the owner/tenant monthly allowance versus the new 112,000
maximum. No active/unsettled reservation requires clearing. The selected conservative
window remains **1 November 2026, 00:00–01:00 UTC**; projected eligibility is neither
a reservation nor permission to execute.

**D. Future operator handoff.** At the selected time, use the existing packet's
read-only eligibility command to check current authoritative usage, rolling windows,
outstanding reservations and remaining allowance. Confirm inherited attestations
remain true; review the configuration and digest separately, obtain a fresh delegated
operator token, personally sign with the existing RSA key and verify the signature.
Use the exact launch command already recorded above and in the private
`OPERATOR_PACKET.md` only after separate live authorization. If the selected window,
configuration or covered code changes, prepare freshly reviewed timestamps/digest
and a corresponding signature then; do not overwrite signed evidence. Nothing was
refreshed or signed during this recovery.

**E. Resumed-session safety accounting.** New inference requests: **0**. Azure
operations/modifications: **0**. Approval signatures/consumption: **0**. Ledger or
replay mutations: **0**. Tests/rehearsals: **0**. New repository changes: **this report
append only**; no implementation or private-packet edits. No staging, commit or push.
The existing tracked diff remains 12 files, 211 insertions and 12 deletions; this
already-untracked report is excluded from that aggregate.
