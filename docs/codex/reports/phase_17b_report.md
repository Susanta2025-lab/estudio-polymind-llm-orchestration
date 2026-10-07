# Phase 17B — Canonical Document Model, Object Storage & Extraction Plane

Date: 2026-10-07. Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`.
Branch: `master`. Architectural authority: [Phase 17A](phase_17a_report.md).

## 1. Executive summary

Implemented a local document extraction plane in `documents/`, independent of
application serving, conversation memory, inference and retrieval publication.
It produces immutable scoped document/extraction models, stores verified source
and canonical JSON objects, accounts for every PDF page, and resolves evidence to
preserved page text or UTF-8 line/character spans. Quality observations and a
conservative native/layout/OCR policy are separate modules. No new dependency,
cloud adapter, worker, public API or infrastructure was introduced.

## 2. Phase result

**Phase 17B — PASS.** The local foundational contracts and deterministic extraction
acceptance boundary are implemented and tested. This permits beginning **Phase
17C — Durable Job Orchestration, Idempotency & Recovery**, which has not started.
PASS does not establish hostile-input process isolation, production storage
recovery, calibrated OCR selection, durable jobs, synthesis, RAG publication,
tenant authentication or full Phase 17 completion.

## 3. Starting repository/worktree state

HEAD was and remains `f9b47fda4658935b64826f1d4abe0488c64f21ae`, on `master`.
Before editing, status was:

```text
## master...origin/master
 M README.md
 M docs/codex/reports/phase_16_report.md
?? docs/codex/prompts/phase_17a.md
?? docs/codex/reports/phase_17a_report.md
```

Snapshots of all four files, SHA-256 inventory, starting status and tracked diff
were saved outside the repository at `/tmp/polymind-phase17b-baseline`.
The starting tracked diff was **1,665 insertions / 1 deletion**: README 35 added
lines, Phase 16 report 1,630 added / 1 removed. None of those lines is attributed
to Phase 17B. Both Phase 17A files and the complete starting Phase 16 report were
verified byte-identical after implementation. README was edited incrementally.

## 4. Scope and exclusions

Included canonical models, scoped deterministic identity, immutable local objects,
bounded admission, PDF/text extraction, provenance, observations/policy, a future
OCR/layout protocol, deterministic JSON, fixtures, security/regression checks and
documentation. Excluded queues, leases, outbox, retry scheduling, workers, LLM
synthesis, managed inference, publication, authentication, quotas and provisioning.
No existing API request limit, runtime setting, dependency or deployment changed.

## 5. Canonical document architecture

Frozen Pydantic models with tuple collections define `Scope`, `ObjectRef`,
`Document`, `TextUnit`, `Block`, `Span`, `Geometry`, `Visual`, `Observations`,
`Decision`, `EvidenceRef` and `ExtractionArtifact`. Unknown fields are rejected;
non-finite numeric values are rejected. Ownership is explicit and immutable.

Document metadata includes opaque document/version IDs, source reference with
SHA-256/algorithm/bytes, declared/detected MIME, display filename, page count,
optional language/confidence and aware creation timestamp. The extraction envelope
adds execution timestamp, schema/profile/parser versions, effective limits and
units. A PDF unit has a 1-based physical ordinal and optional printed label,
dimensions/rotation; a text unit has no page metadata. Missing OCR/language/
geometry information remains null. Native blocks are deliberately generic text.

The block vocabulary also represents paragraph, heading, table, figure, caption
and unknown units, optional hierarchy and geometry. Visual metadata supports actual
cell rows, captions, image references and unparsed/unsupported/parsed states.
These are schema capabilities, not native semantic extraction claims.

## 6. Identifier/versioning strategy

The caller provides a UUID document identity and trusted tenant/owner UUID scope.
Version ID is UUIDv5 over an unambiguous JSON tuple of scope, document ID and
server-computed source SHA-256. Page/text source IDs derive from version and
physical ordinal/text identity. Extraction ID incorporates source version, scope,
artifact/native/normalization/policy profiles, actual parser version, UTC extraction
time and effective byte/page/character/block limits plus structural request.
Block IDs incorporate extraction, source and reading-order index. Object keys
incorporate scope, object kind and object ID. Names never participate in keys.

Versions are `document/1`, `extraction/1`, `native/1`, `identity/1`,
`native-policy/1`, `utf8-strict/1`, and installed `pypdf/6.12.2`.
Exact replay requires the same document ID, timestamps, metadata, bytes and
profiles. Default timestamps intentionally create a new extraction execution.
Changed parser/config/time yields a new extraction ID; changed bytes produce a
new document version. Same logical identity with conflicting serialized bytes
fails immutable storage creation rather than replacing earlier evidence.
UUIDv5 is an opaque representation, not an unguessability/authentication claim.
SHA-256 protects bytes; content equality never grants cross-owner access.

## 7. Source object contract

`ObjectRef(kind="source")` records immutable scope, version identity, generated
key, computed hash and actual byte count. Accepted source bytes are stored exactly,
including UTF-8 BOM and CR/LF conventions. The service verifies an optional declared
checksum against actual input before writing. Unsupported/empty/malformed/
encrypted/oversized input is rejected before source publication in normal admission.
Sources contain no execution state and are never rewritten by extraction.

## 8. Processing artifact contract

`extract()` returns `(ExtractionArtifact, ObjectRef(kind="artifact"))`. Canonical
JSON is a separate immutable object; its metadata includes its own computed hash
and byte size. The artifact embeds the parent source reference/document version.
The artifact reference is external to its own bytes, avoiding a self-hash cycle.
Objects are not a transaction with a future ledger: a failure after source creation
can leave an orphan. A byte-budget test demonstrates that boundary explicitly.

## 9. Storage abstraction

`ObjectStore` exposes `put`, `read`, and `inspect`. Writes/read operations are
bounded; inspect streams through bytes to verify size/hash without collecting the
payload. Missing objects, conflicts, corruption, scope mismatch and operational
failure have distinct sanitized categories. There is no list/delete capability.
A future Azure Blob adapter should implement conditional create-if-absent, verify
stored bytes/metadata on idempotent collisions, stream bounded reads, and return
the same scope/key/hash reference. Blob ETags would support concurrency but would
not replace the SHA-256 integrity contract. No Azure SDK/account/container was
accessed, added or selected.

## 10. Local object store

`LocalObjectStore(root)` uses an explicitly supplied operator-controlled root,
UUID filenames, 64 KiB read/write pieces, server hashing, private pending files,
fsync and hard-link create-if-absent publication followed by directory fsync.
Existing identical bytes return the same reference; conflicting bytes fail.
Root/ancestor traversal uses directory descriptors and `O_NOFOLLOW`; object reads
also reject symlinks, nonregular files and multiply linked files. Filename traversal
and absolute filenames remain harmless display metadata. Failed ordinary writes
remove only their own pending file. Temporary-directory owners handle cleanup.

This is a POSIX development adapter, not a portable Windows backend or protection
from a malicious account with write access to the root. Files can be tampered with
by that account; reads detect checksum changes. Abrupt process death can leave
pending files/hard links, and simultaneous identical writes may transiently report
storage_error while the first writer finishes publication. Crash recovery and
orphan retention are not claimed; Phase 17C must define them before durable use.

## 11. PDF extraction architecture

`NativePdfRunner` uses the existing pypdf dependency, strict parsing, no passwords,
and no image decoding/OCR invocation. It checks page count and extracts each page
separately. It records dimensions/rotation and only explicit PDF page labels.
Resources/content operators provide bounded application observations for image and
graphics presence, without pretending to understand their meaning.

Empty pages without drawing/image signals are blank; image resources/inline images
without text recommend OCR. Unresolved graphics recommend manual review. Text-bearing
pages retain native text. Page exceptions produce an explicit failed unit in place;
malformed document structure produces a sanitized document error. Budget breaches
reject the document rather than returning a truncated artifact. The pinned pypdf
module loggers suppress diagnostics only in this runner's context; legacy loader
logging remains enabled. Tests cover both behaviors.

## 12. Plain-text extraction

Plain text uses strict UTF-8 without fallback or replacement decoding. Empty/
whitespace-only input, invalid UTF-8 and disallowed C0 control characters fail.
Unicode and BOM are preserved. LF is the line delimiter; CRLF keeps its CR, and
standalone CR remains a character rather than a separate line. Each nonempty
LF-delimited segment, including its terminating newline, becomes one text block.
There is one source unit, no physical page, and no PDF dimensions/labels.

## 13. Page/block/span provenance

Spans are half-open Unicode code-point offsets, not UTF-8 byte offsets. PDF spans
address the preserved native parser output for that physical page, not offsets
inside compressed PDF bytes. Text spans address the strictly decoded source, with
1-based inclusive line coordinates. Identity normalization means these are also
normalized-text coordinates. Original bytes remain resolvable through the parent
source object.

`resolve(artifact, scope, evidence)` checks owner scope, version, extraction,
source, block, span bounds and line coordinates before returning exact text.
Serialization validates complete ordered physical-page inventory, source/block/
extraction identities, complete contiguous text coverage, block/source alignment,
line coordinates and observations. Filename plus chunk number is never used as
canonical provenance. No evidence is published to retrieval.

## 14. Normalization rules

`identity/1` performs no normalization, whitespace collapse, header/footer removal,
Unicode folding or translation. `normalized_text` is null unless identical to
source text. A nonidentity transformation requires a new profile and explicit
mapping schema before acceptance; v1 rejects differing normalized text. This
avoids pretending a lossy transformation has resolvable source offsets.

## 15. Extraction quality observations

Per-unit observations record character count, printable ratio (CR/LF/tab allowed),
replacement-character ratio, native text presence, image/graphics presence when
known, block count, parser failure and requested structural fidelity. Text quality
counts and block counts are validated against artifact contents. Structural
requirements are caller intent, not an inferred fact about the document.

## 16. Native/layout/OCR decision model

The separate policy module records source ID, unchanged observations, version,
outcome, reason and next tier. Native text is accepted without a minimum length;
requested structural fidelity with text recommends layout. Images without text
recommend OCR. Replacement/nonprintable text and unresolved graphics recommend
manual review. Blank pages are accepted as blank; parser failures remain failed.
The outcome vocabulary also supports unsupported, while unsupported admission
currently raises an error instead of manufacturing an artifact. These decisions
are conservative routing hints, not calibrated quality scores or promises that
OCR will recover text.

## 17. OCR/layout future adapter boundary

`EnhancementAdapter` accepts a validated scoped source reference, document version,
parent extraction ID, ordered physical-page selection and layout/OCR tier. Its
result contains engine/version, optional model version and mapped text units, with
optional blocks/visuals/geometry/confidence. Tests construct a deterministic fake
result and reject missing/invalid physical mapping. No implementation calls an
external service. Merging enhancement results, selecting between alternatives and
storing an enhanced canonical profile remain future work; `native/1` is the only
implemented canonical extraction profile.

## 18. Parser/resource safety

`ExtractionSettings` uses environment prefix `DOCUMENT_`, with defaults:

| Setting | Default |
| --- | ---: |
| MAX_SOURCE_BYTES | 16,000,000 |
| MAX_PAGES | 1,000 |
| MAX_CHARACTERS | 4,000,000 |
| MAX_BLOCKS | 100,000 |
| MAX_ARTIFACT_BYTES | 32,000,000 |
| STORAGE_ROOT | None; caller must choose a root |

These settings are separate from `config.settings.Settings` and the API request
limit. A caller can pass a settings instance explicitly. Storage root is available
as configuration; create `LocalObjectStore(settings.storage_root)` only after
requiring a non-null operator choice. There is no implicit store/global client.

Source reads, decoded characters, output blocks/pages and stored JSON bytes are
limited. Parser exceptions are isolated at document/page boundaries. The injectable
`ParserRunner` allows later process isolation. **No hard timeout, CPU, RSS, expanded
content-stream/pixel or decompression cap is implemented.** pypdf can allocate or
spend time before it returns a page/count, and serialized JSON size is checked
after materialization. Input and canonical artifacts are bounded in-memory, not
streamed whole-document processing. Do not expose this runner to untrusted public
uploads until a separately constrained process and stronger admission are added.
No production-sandbox claim is made.

## 19. Integrity/checksum behavior

All object hashes are computed by the server over actual bytes. Declared mismatch,
changed data at an existing key and read-time corruption fail. Same data has the
same checksum, including across scopes, but scope-specific keys differ. Tests
verify source bytes read back unchanged, artifact bytes verified before deserialization,
changed-source identities, replay equality and immutable conflicting writes.
Checksums and keys are neither credentials nor authorization decisions.

## 20. Serialization and migration

UTF-8 JSON has sorted keys, compact separators, explicit nulls, finite numbers,
stable field names and no pickle/base64 binaries. Duplicate JSON keys, unknown
fields, unknown schema versions and invalid lineage fail with serialization_error.
The serializer validates models again to catch bypasses such as unchecked copies.
The reader has a byte bound; it is not a JSON parser process sandbox.

Future schema/profile changes must retain a v1 reader or an explicit audited
conversion reader. Conversion must create a new artifact/object and preserve the
old one. Current code intentionally rejects unknown versions rather than silently
migrating them. No migration framework was added.

## 21. Existing RAG compatibility

Selected the explicitly permitted **strategy A**: legacy PDF/text loaders,
chunking and ingestion remain byte-for-byte unchanged. Their concatenation and
publication behavior is preserved by regression tests, including exact legacy PDF
text output. This introduces a separate canonical entry point using the same
pypdf dependency, not a replacement production RAG pipeline.

Phase 17F must migrate deliberately: derive encoder-budgeted retrieval spans and
scoped IDs from evidence, retain canonical references in Chroma/BM25/citations,
and implement controlled publication. It must verify actual encoder limits then;
this phase creates no retrieval chunks and performs no embeddings or publication.
No Redis document/job use, provider-specific inference logic or API/UI coupling
was introduced.

## 22. Tenant/owner scope

Scope contains both tenant and owner UUIDs; all document versions, objects and
evidence carry it. Store/read/resolution paths reject mismatched scope and tests
show identical bytes under another tenant use different keys. Scope is supplied
by a trusted caller. There is no authentication, identity provider, authorization
lookup, sharing policy or multi-user guarantee. Phase 17G must derive scope from
real identity and authorize every operation; supplying a UUID is not proof of access.

## 23. Error model

`DocumentError` exposes only a category: unsupported_format, invalid_document,
encrypted_document, source_too_large, page_limit_exceeded,
extraction_limit_exceeded, extraction_failed, integrity_error, storage_error,
object_conflict, object_not_found, scope_mismatch, serialization_error or
invalid_reference. Operational boundaries suppress upstream exception messages.
Models remain internal typed contracts; callers must not expose raw Pydantic
validation errors containing their input. No endpoint exposing these models was added.

## 24. Security findings/tests

Tests cover path/absolute/Windows-style traversal filenames, invalid object keys,
root and ancestor/object symlinks, scope mismatch, same-byte cross-scope keys,
conflicting and concurrent writes, corrupted objects, declared checksum mismatch,
byte/read/block/character/artifact limits, MIME/extension disagreement, malformed/
truncated/encrypted PDFs, invalid encodings and provenance tampering. Native parser
messages are suppressed within canonical extraction and remain available outside it.
No document content, filenames, paths, keys or owner identifiers are logged by the
new service. No metrics or high-cardinality labels were added. Aggregate worker
outcome/format/tier metrics remain a 17C/17H requirement.

## 25. Fixture matrix

All fixtures are synthetic, generated using installed pypdf and the standard
library in temporary directories. No binary documents were committed.

| Fixture | Exact expectation |
| --- | --- |
| Text/blank/text PDF | 3 pages, text on 1 and 3; blank 2 retained |
| Text/blank/image/columns/graphics PDF | 5 pages accounted, native text on 1/4, blank 2, OCR 3, manual review 5 |
| Columns with structure requested | Native text preserved, layout recommended; no fabricated cells |
| Explicit printed labels | Labels “Appendix”; physical ordinals remain 1/2/3 |
| Missing resource dictionary | Blank page remains blank, not failed |
| Forced native page exception | 3 pages retained; page 2 failed; 1/3 preserved |
| Truncated/malformed PDF | invalid_document; no partial source publication |
| Encrypted PDF | encrypted_document; no password handling |
| UTF-8/Unicode/BOM/CRLF text | Exact text and line/character resolution; no pages |
| Empty/invalid/control text | Predictable invalid_document |
| Large text and small configured limits | Exact boundary acceptance or bounded rejection |
| Fake OCR result | Selected physical mapping preserved; bad mapping rejected |

## 26. Fidelity benchmark/results

The deterministic five-page matrix accounts for **5/5 physical pages**, extracts
both expected text-bearing pages (**2/2**), classifies the one known blank
correctly (**1/1**), recommends OCR for the one synthetic image-only page (**1/1**),
and preserves physical numbering/spans. Layout escalation is verified separately
by explicit structural request. Failure and label fixtures preserve physical page
identity. The legacy three-page loader still returns exactly
`Page 1 alpha\nPage 3 alpha\n`.

The synthetic image is a tiny colored raster, not a representative scanned text
corpus. Selection is a recommendation, not a measured OCR recovery result. There
is insufficient material to calibrate numeric OCR recall, reading order, tables,
legal/technical document fidelity or Phase 17H candidate quality thresholds.

## 27. Performance observations

A local one-shot benchmark used temporary stores, fixed timestamps and tracemalloc
around extraction/storage/serialization (fixture generation excluded):

| Fixture | Source bytes | Artifact bytes | Units / blocks | Time | Peak Python-traced bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| 10,000 Unicode text lines | 190,000 | 3,495,507 | 1 / 10,000 | 2.493 s | 57,194,252 |
| 100 born-digital PDF pages | 37,507 | 107,433 | 100 / 100 | 0.192 s | 2,329,831 |

These are measurements on this environment, not SLOs, RSS limits or production
extrapolations. Line-block metadata and validation/JSON copies dominate text
memory. Large file-backed/partitioned artifacts and process memory controls need
later work. The current maximum block count must not be interpreted as a proven
safe production concurrency budget. Local benchmark script/results remain outside
the repository; deterministic acceptance assertions live in tests.

## 28. Exact Phase 17B files

Created:

```text
documents/__init__.py
documents/adapters.py
documents/config.py
documents/errors.py
documents/extraction.py
documents/models.py
documents/parser.py
documents/policy.py
documents/provenance.py
documents/serialization.py
documents/storage.py
tests/unit/documents/conftest.py
tests/unit/documents/test_contracts.py
tests/unit/documents/test_extraction.py
tests/unit/documents/test_storage.py
tests/integration/test_document_plane.py
docs/codex/prompts/phase_17b.md
docs/codex/reports/phase_17b_report.md
```

Modified incrementally: `README.md` only. No existing implementation or test file
was modified. Phase 16/17A paths shown in Git status are prior changes, not 17B edits.

## 29. Tests and validation

- New focused suite: **54 passed** (`tests/unit/documents` and
  `tests/integration/test_document_plane.py`).
- Selected existing regressions: **68 passed in 11.60 s** (deployment topology,
  retrieval, vector storage, model/config routing and API reliability).
- Final complete project suite: **285 passed**, no skips/failures.
- `PYTHONPYCACHEPREFIX=/tmp/polymind-phase17b-pycache python -m compileall -q .`:
  exit 0; external bytecode cache avoids unrelated ownership changes.
- `docker compose config --quiet`: exit 0; configuration inspection only.
- `git diff --check`: exit 0; new files also checked separately for whitespace.
- Repository CI/Makefile configure no Ruff, Black, Flake8 or type-checking gate;
  none was invented or installed.

No Docker build was needed: dependencies, Dockerfile and deployment configuration
were unchanged; no container integration behavior was modified. No Helm/cluster
validation was needed for this local domain-only change. Tests use no live external
services, credentials, cloud OCR or model downloads. Validation logs remain in
`/tmp/polymind-phase17b-*`, outside the repository.

## 30. Implementation self-review and separate pre-commit review

Reviewed complete new modules/tests and the README incremental diff. Fixed findings
included missing stored identity/line/coverage validation, quadratic per-line
provenance validation, unsafe propagation of cleanup errors, avoidable pre-limit
line splitting, blank PDFs without resource dictionaries, and unsanitized invalid page-metadata
validation errors. Added regressions
for those contract failures and context-limited parser diagnostic suppression.
Reviewed immutable writes, scope/key derivation, full page coverage, native-only
semantics, byte/character limits, no RAG publication, no job code and no cloud/
inference coupling. Policy stays separate from observations/domain data.

The separate pre-commit review inspected the exact added-file list and incremental
README edit, checked new source/test compilation, whitespace, documentation links,
secret/private-key/credential-URL/debug/TODO patterns, and verified baseline file
hashes. No credentials, private documents, environment files, generated PDFs,
dependency files, temporary benchmark logs or unrelated files were introduced.
Only synthetic fixture text and scope IDs occur in tests. No staging or commit
occurred. The remaining safety limits below are explicit, not hidden behind PASS.

## 31. Remaining risks and deferred decisions

Hard process isolation, CPU/decompression/pixel budgets and large partitioned
artifacts are deferred. Native extraction cannot guarantee reading order, detect
all images in nested forms, infer tables/headings or prove blank visual content.
Unknown drawings remain manual review. OCR/layout output integration and quality
calibration are deferred. JSON is deterministic but can be metadata-heavy.

Local filesystem durability/reconciliation and cross-process idempotent retries
need the next phase's lifecycle design. No remote production adapter or database
has been selected/provisioned. Trusted scope is not authentication. No retention,
revocation, public upload or cost/quotas implementation exists. Chroma and Redis
remain unchanged. Production security and capacity limitations from Phase 16 and
Phase 17A still apply. Metrics and full quality/recovery benchmarks remain future.

## 32. Exact Phase 17C prerequisites

Phase 17C can depend on immutable source/artifact references, verified checksums,
versioned scoped canonical bytes, source/page/evidence identity, configurable local
limits, sanitized errors and deterministic fixtures. It must supply persistent
registration metadata and stable timestamps for replay rather than treating a new
wall-clock extraction as an idempotent retry.

Before claiming durable jobs, select and validate the transactional state/dispatch
boundary, idempotency fingerprint and step keys, lease/fence/cancellation semantics,
conditional artifact-manifest commit, outbox/reconciliation and failure recovery.
Resolve orphan/pending-object retention and local-versus-production object adapter
expectations. Place parser work behind process/resource isolation before admitting
untrusted uploads. Keep scope trusted until 17G; keep Redis out of job state and
Chroma out of source authority. Do not infer permission to provision services from
this report. **Phase 17C — Durable Job Orchestration, Idempotency & Recovery**
has not been started.

## 33. Git state and no-commit confirmation

Final status is the original four dirty paths plus the 18 created Phase 17B files;
README contains both its prior 17A additions and the 17B status/report update.
Git's normal diff stat excludes untracked files; the incremental inventory above
is therefore required to understand the Phase 17B change. The final raw status
and tracked/incremental counts are recorded below after final verification.

Commit created: **NO**. Push performed: **NO**. Branch created: **NO**.
Files staged: **NO**. Prior Phase 17 work preserved: **YES**.
No Azure mutation, Kubernetes mutation, external OCR call, Foundry call, new paid
infrastructure or secret exposure occurred. Phase 16 closure modifications and
Phase 17A artifacts remain present for the deliberate no-commit Phase 17 workflow.

Final `git status --short --branch`:

```text
## master...origin/master
 M README.md
 M docs/codex/reports/phase_16_report.md
?? docs/codex/prompts/phase_17a.md
?? docs/codex/prompts/phase_17b.md
?? docs/codex/reports/phase_17a_report.md
?? docs/codex/reports/phase_17b_report.md
?? documents/
?? tests/integration/
?? tests/unit/documents/
```

Final tracked `git diff --stat`:

```text
 README.md                          |   37 +
 docs/codex/reports/phase_16_report.md | 1631 ++++++++++++++++++++++++++++++++-
 2 files changed, 1667 insertions(+), 1 deletion(-)
```

Incremental 17B accounting: **18 new untracked files**, listed in section 28,
and **README 7 added / 5 removed lines** relative to its pre-17B snapshot. The
Phase 16 report and both Phase 17A files have unchanged baseline hashes; README
retains the Phase 17A section with its current status advanced. Git's tracked
stat includes earlier work and omits all new untracked files. The final focused
run was 54 passed in 1.01 s; the final full run was 285 passed in 13.44 s.
