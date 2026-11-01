# Phase 17H-L — same-day attempt 2 handoff

> Publication note — 1 November 2026: this document preserves a historical checkpoint. Private locations and environment identifiers are symbolic where shown; original dates, decisions and outcomes are retained. Historical handoffs are inactive and must not be run. See [Attempt 6 closure](phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md) for the later accepted single-call result and remaining Phase 17H gates.

**GO — SAME-DAY L1 READY FOR OPERATOR SIGNATURE**

## A. Policy migration — PASS

Both owner and tenant migrated from `phase17hl-l1/1` to `phase17hl-l1/2`:

| Field | Before | After |
|---|---:|---:|
| Requests per rolling 86,400 seconds | 4 | 5 |
| Daily tokens | 112,000 | 115,305 |
| Monthly tokens | 112,000 | 115,305 |
| Monthly financial ceiling | EUR 5 | EUR 5 |

No supported migration existed. `governance/migration.py` now provides the narrow
explicit migration, using the existing schema and event model. It validates the
exact old policy, catalog and schema, rejects unresolved obligations, obtains a
SQLite writer lock, makes an exclusive durable SQLite backup, and atomically
updates the policy plus a migration event. That event records full old/new policies,
exact field changes, catalog hash, prior history hash and backup hash/path.
Repeated application returns the existing evidence without another mutation.
Unexpected policy/schema/state fails closed; a failed transaction rolls back.
`GovernanceLedger.reserve` and readiness now reject stale in-memory policies.
Settlement remains available for historical obligations.

The private `.env` policy and new launch configuration match the stored policy.
Its nonsecret policy value alone was replaced after an exclusive private backup.
Database/configuration files are not one filesystem transaction: interruption
between them fails closed through policy equality, rather than admitting stale
configuration. No authority database was reconstructed or replaced. Existing
processes retaining policy /1 must reload before new admissions; no service was
restarted. Historical packets remain immutable and cannot open authority under /1.

Backups and `policy-migration.json` are under:
`<PRIVATE_OPERATOR_DIRECTORY>/`.
All historical reservation/event rows match the backup, excluding the single added
migration event. **37 protected files** match pre-migration hashes, including both
prior packets, original audit, security/provider authorities, trust and replay.
Pricing, identities, paths, concurrency and reserved-token caps are unchanged.

## B. Admission eligibility — GO

Authoritative read-only verification after migration finds exactly one SETTLED
request: 1,845 input + 1,460 output = 3,305 tokens, EUR 0.00699907602956752.
There are no unresolved obligations. Both scopes have **four rolling request slots**
and **112,000 daily/monthly tokens available**, sufficient for the full new maximum.
The existing 112,000 simultaneous reserved-token cap is unchanged; calls are sequential.

Provider ledger is clear. Reused Azure attestation is 30 RPM / 30,000 TPM; local
admission remains 2 RPM / 30,000 TPM / two slots, protecting one interactive RPM,
2,000 TPM and one slot. Run limits remain one call at a time, 61-second spacing,
four calls, 100,000 input and 12,000 output tokens, without retries or fallback.
New maximum cost is EUR 0.11351636747626; combined historical actual/new maximum
is **EUR 0.12051544350582752**, within EUR 5. No budget increase was made.
Eligibility is a current snapshot, not an atomic reservation of the entire run;
the operator helper rechecks it and runtime retains per-call enforcement.

## C. Technical readiness

New packet: `<PRIVATE_OPERATOR_DIRECTORY>/`.
All directories are 0700, files 0600; audit is empty and no signature exists.

- Configuration digest: `cdb67dd63b6438b24cc9623c5de16c41feaed67466d5cfcb8838a29146b4c13b`.
- Unchanged generation digest: `3da39a6b00a75a7f689a49e56a4dc3255576e0d16265a2d509f259f2d533e16f`.
- Window: **15 October 2026, 14:44:35–15:44:35 UTC**, or
  **15:44:35–16:44:35 Lisbon**. Start was actual installation time, not backdated.
  Launch strictly before **15:34:35 UTC / 16:34:35 Lisbon**.

`managed-prompt/2`, canonical 3,000-byte validation, 3,000 output-token reservation,
evidence/lineage checks, OIDC retrieval pin, local MiniLM and isolated Chroma are
unchanged. Configuration retains the existing owner/tenant, Entra identity settings,
authority and embedding paths, endpoint, `epolymind-gpt-54-mini`, model
`gpt-5.4-mini` version `2026-03-17`, GlobalStandard/spaincentral, pricing and EUR 5
incremental ceiling. Full exact bindings are in configuration and unsigned review.
The November digest is not reused. Existing attestations and RSA trust are reused;
fresh identity and signature remain operator work.

Focused validation: **19 passed** (new migration and affected governance tests),
then **9 passed, 86 deselected** (new policy/window signature rejection, digest,
generation/window guards, intercepted four-call execution and no-retry timeout).
Two initial launcher runs using conflicting test-only environment overrides each
had 6 passes/3 failures; a one-case diagnostic reproduced settings rejection before
provider calls. Removing those overrides produced the final nine passes without
implementation changes. Prior 67/93/195-test evidence was reused; no full suite.

`git diff --check`, relevant compilation, installed helper compilation and independent
read-only checks of policy consistency, digest/bindings, backup/history, permissions,
empty audit and current admission passed. Scoped self-review and separate pre-commit
review found no generation/provider changes, new dependencies, secret material in
repository artifacts, retry changes or unintended API changes.

## D. Exact operator handoff

From the repository root with the existing project interpreter:

**A — Fresh Entra authentication.** Use the existing approved delegated process for
this API's `access_as_user` scope and assigned operator role; token must have more
than 30 minutes remaining when signing. Keep shell tracing disabled.

```zsh
set +x
read -rs 'POLYMIND_L1_OPERATOR_TOKEN?Fresh delegated access token (hidden): '
export POLYMIND_L1_OPERATOR_TOKEN
export PYTHONDONTWRITEBYTECODE=1
L1_PACKET="<PRIVATE_OPERATOR_DIRECTORY>"
```

**B — Review.** Check the exact bindings and digest above against these materials:

```zsh
cat "$L1_PACKET/l1-configuration.json" "$L1_PACKET/configuration.sha256" "$L1_PACKET/unsigned-review.json" "$L1_PACKET/verification.json"
PYTHONPATH=. python "$L1_PACKET/eligibility.py"
```

**C — Personally sign.** The existing helper verifies fresh identity, displays
bindings, requires `SIGN`, and privately prompts for the existing RSA passphrase.

```text
PYTHONPATH=. python "$L1_PACKET/operator_handoff.py" sign
```

**D — Independently verify**, without consuming approval:

```text
PYTHONPATH=. python "$L1_PACKET/operator_handoff.py" verify
```

**E — Execute once**, only after review, signing and verification succeed:

```text
export POLYMIND_L1_AZURE_CREDENTIAL="$(python -c 'from dotenv import dotenv_values; print(dotenv_values(".env")["OPENAI_COMPATIBLE_API_KEY"], end="")')"
python -m tests.performance.foundry_l1 --live \
  --configuration "$L1_PACKET/l1-configuration.json" \
  --approve-sha256 "$(cat "$L1_PACKET/configuration.sha256")" \
  --approval "$L1_PACKET/operator-approval.jwt" \
  --approval-trust "<PRIVATE_TRUST_DIRECTORY>/approval-trust.json"
unset POLYMIND_L1_OPERATOR_TOKEN POLYMIND_L1_AZURE_CREDENTIAL
```

A failed start may consume approval. Preserve all records and never retry
automatically. If the window expires, stop for newly reviewed material; do not
rewrite signed evidence. The private `OPERATOR_PACKET.md` contains this procedure.

## E. Safety accounting and Git

Azure inference calls **0**; Azure resource modifications **0**; AKS operations **0**;
real approval signing/consumption **0**. Authority changes: one configuration policy
update and one migration event, in one transaction; no historical row changes.
Private `.env` policy synchronized; secure backups retained. No new run database,
model execution, token acquisition, private-key access or L2 execution occurred.

`git status --short` retains pre-existing uncommitted work plus this task's
`governance/ledger.py`, new `governance/migration.py`, new migration tests, additions
to the already-untracked approval test file, and task prompt/report. `.env` remains
ignored. Aggregate tracked `git diff --stat`: **13 files, 218 insertions, 12 deletions**;
this includes prior work and excludes untracked files. This task's tracked delta
is seven lines in `governance/ledger.py`. **No staging, commit or push occurred.**
