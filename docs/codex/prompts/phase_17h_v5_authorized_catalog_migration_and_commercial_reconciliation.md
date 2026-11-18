# Phase 17H v5 authorized catalog migration and commercial reconciliation

Clean record of the operator instruction, 7 November 2026. The operator explicitly
authorized the existing private `catalog-migration.proposed.json` with expected
canonical SHA-256:

```text
53939016e34ae7b6db8fc93d8929abd0a38e53182e982ce7e02d051dc35e1677
```

Before applying, verify the exact proposal, affected authorities, migration
safety and preservation of historical settlements. Retain the EUR 5 ceiling;
do not modify historical billing records or pricing versions. Use the exact
reviewed prospective versioned catalog migration rather than an unreviewed
replacement or exception.

For commercial reconciliation, use 23% VAT as a conservative mainland Portugal
budgeting assumption until actual Azure profile/invoice treatment is verified.
Exclude existing unrelated infrastructure from incremental evaluation cost only
where current billing evidence supports the exclusion. Do not assume zero fixed,
network, storage or monitoring charges without evidence. Inspect available billing
and configuration information for defensible bounds and report uncertainty
requiring operator confirmation.

Keep `charges_verified=false` until complete commercial reconciliation is
supported and independently reviewed. Authorization covers only the specified
catalog migration. It does not authorize RSA signing, approval consumption or
paid Azure inference. After migration and verification, report the remaining
blockers before proceeding. Repository instructions continue to prohibit staging,
commits and pushes.
