# Phase 17H–L — C1 final isolated offline regression

Date: 1 November 2026. Branch: master. [Normalized task](../prompts/phase_17hl_c1_final_isolated_offline_regression.md).
Only this report and the normalized task are repository changes made by this audit.

## 1. Executive verdict

**REGRESSION EXECUTION: COMPLETE. Full eligible offline suite: PASS. Isolation: PASS.
C1 COMMIT READINESS: CONDITIONALLY READY.** The final complete default suite collected
and passed **1,810 tests** in **141.92 seconds**, with **0 failures, 0 skips,
0 collection/setup errors, 0 xfails and 0 xpasses**. There was one third-party
deprecation warning. All 77 collected modules were under unit/integration; no
default-suite test was deselected. Of these cases, 1,185 reside in C1 test modules.

The condition is engineering review of **324 existing pending-file Ruff findings**
and an environment qualification: the available installed PyTorch is **2.12.0**,
whereas `requirements-ml-cpu.txt` specifies **2.12.0+cpu**. All selected tests ran,
including real local Chroma and static Helm rendering checks; this is nevertheless
not certification of the exact CPU-pinned dependency build. There is no demonstrated
high-severity C1 defect or failed final assertion. Lint is **REVIEW REQUIRED**, not
PASS, and this audit does not grant an operator waiver.

An initial collection-only invocation encountered one isolated-environment username
lookup error; its cause, correction and original evidence are retained in section 8.
The successful repeat and full execution do not erase that event. No test/source
was changed to obtain the result. Historical paid Attempt 6 is not rerun or counted
as this regression evidence. Full Phase 17H remains PARTIAL.

## 2. Repository and C1 baseline

The independently measured initial state exactly matches the supplied baseline:
`master`, HEAD `af4a7a076c918ef13aea05d74bf239c0af909133`, **25 modified tracked
files + 131 untracked files = 156 pending files; 0 staged files**. Tracked diff:
**25 files, 1,001 insertions, 99 deletions**. There were 414 existing Git-visible
public files, all captured before either new Markdown artifact was written.
Directory-collapsed Git status is not used to count files.

Initial index-entry SHA-256 was
`a8227a1b0119fd5d7ab5db8de1c9e4aa905170a352e9172d781a08d62e53cffc`;
the raw index-file SHA-256 was
`b01e1ef4216af5dc05ae6d2c74f212f27f3e5655328504fc2983a800faafbb8b`.
Both remain unchanged. Per-file initial SHA-256 values, full status and commands
are retained in the external baseline. The C1 hashes below provide permanent
reviewable source inventory evidence.

The exact membership was parsed from section 15 of the
[documentation remediation report](phase_17hl_documentation_remediation_and_readme_sync.md),
not reconstructed from status or extensions. **69 unique C1 members exist**:
18 application/provider/security/governance modules, four test infrastructure
helpers, five contract fixtures, 13 integration modules, nine performance/support
modules and 20 unit modules. All 87 C2 members also exist; the initial pending
set equals exactly the disjoint union of these two sets. There is no missing or
silently reassigned engineering file.

Static AST inspection found **449 distinct per-file absolute local import edges**
in C1, with **zero unresolved local module/package targets** in the public snapshot.
The newly required `diagnostics`, `azure_schema`, `evaluation`, `migration`, test
helpers and all five frozen fixtures are in C1. Existing dependency modules remain
tracked at HEAD. Runtime imports and test references resolve during the full
77-module collection/execution. Static AST analysis alone does not certify every
possible dynamic import; the three explicit dynamic execution/import sites were
reviewed: hash-pinned historical fixture execution, fixed synthetic source mutation
tests and a standard-library time import. None loads operator material.

All **15 engineering file hashes** individually published in Attempt 6 readiness
match current bytes, including renderer, codec, validator, planning/workflow,
schema/provider, executor, generation composition and accounting. Its two published
document hashes also match. The aggregate executor/generation bindings match.
No source change invalidating Attempt 6 implementation evidence was found.

| C1 member, unchanged before/after | Initial and final SHA-256 |
|---|---|
| `documents/digestion/codec.py` | `9e5c7afbb0ac2574a909fda4da7eaacc9376e61b7e10960daa8c4e327953b768` |
| `documents/digestion/diagnostics.py` | `10f1143deb706e56dc6b9554fd768aa452425fcba75b93b8a1eb633a92931ebf` |
| `documents/digestion/managed.py` | `fa6cd701b73c0cdd486b645a64748f3bb70509b17d310b40c9455c619dbc91a9` |
| `documents/digestion/models.py` | `f767ee7e6cfced13b321028999aee042146ef4265755d7dfd054ae1d5cb96e67` |
| `documents/digestion/validation.py` | `5b6c4efa905758d11b179495f49c88f56e0cfbdcc079274b9d03044ee110a8b4` |
| `documents/publication/analysis.py` | `635cc5c03b66cb16d367c44db4fba71b426e77a4eedb7a68015c2af86f8b4fde` |
| `governance/evaluation.py` | `f15316c842eb68ba3a80d4477f8d638ba282388c24f336b6c480144fdfecf4f3` |
| `governance/execution.py` | `979abd479f0b8cdddc79193b5dc76fe1f2a7e07269e9c5eb6264c84f1b2fd134` |
| `governance/ledger.py` | `de6f45b910b2ecadab466cd26119ebda0b4facac5d35037f0c9df6c19c4f28d6` |
| `governance/migration.py` | `6b2f1fee3262a9c15acd789e764e361949b2c9e58b43122d1ec53f73054f2959` |
| `llm/azure_schema.py` | `36cab2377fb6cbf850c1e58e83f03e8861c056ee4d44bba8cc6e0749cc7abf25` |
| `llm/bounded_http.py` | `8aff0e76883576f8f0130bb79920840112981028c4ceb9d6c4179593860eba01` |
| `llm/inference.py` | `281abcf3210fe823f29e9574a8d61f66f1bd3d602f03cdf4f89c309eaf892131` |
| `llm/ollama_client.py` | `7c0519f116aa6a8a0c6df03227fca41316180c04ae7739d21b8eb58ec02e461f` |
| `llm/openai_compatible.py` | `d0505c5297e8259f6737324cfe5a65867d7551c0f2b98949c103f2a14df752db` |
| `llm/structured.py` | `ce24763d62ce3ded77c41630fcdd9aa2766212183d89baac5bc24777d13c9334` |
| `security/identity.py` | `6b498a56c9f4501d68abc6ea3223d99ae4687978399d9378f546a41d6a0a260b` |
| `security/runtime.py` | `82918957d10593f87ac0f856969811c3300f07d816d450d50cc3e72b97277e11` |
| `tests/approval_helpers.py` | `e8c1235dab844e78925f6081d621f3eab03764e9286a4e49e183d24c6cbe9aa4` |
| `tests/conftest.py` | `c9066aa852326fecb3a97ff01fc351db8d3d7cce87f2976f2380d2050468e459` |
| `tests/fixtures/digestion_contracts/managed_prompt3.py.txt` | `5b272d4a7591692eeeb328da09bc39b35d402bebd1d8ada3b891f6b1d6e8928c` |
| `tests/fixtures/digestion_contracts/managed_prompt4.json` | `b0caa2e2a701b7e43ab54b1df19d73bf0a3d57f0b6419f10bfb403afa659ea94` |
| `tests/fixtures/digestion_contracts/managed_prompt4_subject.txt` | `3583382755184d562e4cc6c2c42b1df9c1fd8d10c117891be68fab6d858641bb` |
| `tests/fixtures/digestion_contracts/models.py.txt` | `83783aadde2ecae7616fa6ffd934da3eb396a76c17e0d5f05b573510f690be08` |
| `tests/fixtures/digestion_contracts/validation.py.txt` | `da9cef97360d51a512dcff0d6e09405faf349db427daae141e3460aa2562f031` |
| `tests/integration/test_attempt3_serialization.py` | `0f578b769f5fce759d9af6974bf3b27d86bb6c974bee7075cadfdfd491546079` |
| `tests/integration/test_final_offline_azure_compatibility.py` | `e64a3f72093075859596953b34aaa793fb5411272b79b507d06619faa609db22` |
| `tests/integration/test_foundry_l1_entra.py` | `746eddaa5a5d4edc90d5b98fb05b438b6f58204dc9c744e8735b3b845349e933` |
| `tests/integration/test_foundry_l1_launcher.py` | `8fb69f5f003916673cc68539f097d5ff0e83ce2ceaec9c5139525b5cbfc00569` |
| `tests/integration/test_foundry_offline_workflow.py` | `9e0d79f6f46084e06ef71c40679af96e874083cac4de13da442b1650f6c3fe33` |
| `tests/integration/test_http_cleanup_governance.py` | `6d2936552f33d19427e1b93621e096f01b713fab4e74052646036705bda22339` |
| `tests/integration/test_live_failure_observability.py` | `364acb53b029679b9dbf10aa2511cc4b921882bfbf25893c64b21ac0e51bb972` |
| `tests/integration/test_managed_digestion.py` | `b3ee1cd91bc0dcc2d591bd1e8af5fd3dc7e92155cb09006b29c6c111cdbfd12e` |
| `tests/integration/test_output_limit_hardening.py` | `8cfffca5ff4b3801f2757397657ade65aa6fdbfc888b26cbc5d8edd930f91226` |
| `tests/integration/test_phase17hl_offline_e2e.py` | `b2e8fe85fb3d7d8d576a2f515847ad1a2c2016848cf9795ece7472994f5daace` |
| `tests/integration/test_single_call_harness.py` | `7fc15f117993280ed2b401574e2fe709ed00c65a90b5e30b8e2482d4a67e313b` |
| `tests/integration/test_single_call_preflight.py` | `3858bc5401cb507f1d89622aa9235d3160e9fe4f70712b50675187e054905280` |
| `tests/integration/test_validation_diagnostics.py` | `4995abfd2aff75d17f1f6c203c83b6d0e60e220b39adae6aaabefcec56c5c30b` |
| `tests/performance/foundry_approval.py` | `3fa458e0f46d782e6102bd574881d23489824ca1fe7dde35f99fa0f8cd393f3f` |
| `tests/performance/foundry_budget.py` | `07305ea077f9003192e72120c5d4c61443f9254fc4dfcee4f305c967d8dd81da` |
| `tests/performance/foundry_envelopes.py` | `38eadaf1530ff7da139424b47c0f7b114ce5ffdbb3fe9c3bf288df4edda6f08f` |
| `tests/performance/foundry_l1.py` | `7f90695897cb4056b290f3ff79d414aa274469824b5e7f2155f10cd82679fc3c` |
| `tests/performance/foundry_preflight.py` | `dd594c9bb97ed36858ee067508499015cba4db42a5a6abe1477f495e31e4d7a8` |
| `tests/performance/foundry_recalibration.py` | `96b4b5670482f66875823916cee8daeb935dc51c8e7df9ac8ef4c90c75f60fd7` |
| `tests/performance/foundry_schema_diagnostics.py` | `676da2ac3ea91dcf571ef4c3469e2d826e9402e06b4606b107f17e3116dd2ebb` |
| `tests/performance/foundry_schema_probe.py` | `ef3fea7bfe7637ef2395dd495210b8d9d6fdae7b599761d7720eea263ab3092b` |
| `tests/performance/foundry_single_call.py` | `c016a3c90bd5fef7a3a35ccfaa5efe26e21019ced02c9db1782629e37275e761` |
| `tests/settings_isolation.py` | `00d3e567600d592a6e14d8f8d1b5f6bbb38170e9a2e6394e0b29817efde56698` |
| `tests/source_contracts.py` | `375e7c8de34ce2390b985e1b568101f5b79c6744d72954ba3e265b3f3e8d9baf` |
| `tests/unit/documents/test_independent_json_limits.py` | `3ed9e45dcfe9a4719f27312d297046a964e4892996c1f0a754a576c6d455fdc8` |
| `tests/unit/documents/test_managed_inference.py` | `5a754ad92327f600685c2abe7d577f3cd1dbf58737990910e1d4f17e2d082416` |
| `tests/unit/documents/test_output_limit_sizes.py` | `3b781e755174a329ea480b1dc75defc5e4fa66f2148d2384794b7ad7b1d61980` |
| `tests/unit/documents/test_strict_schema_compatibility.py` | `8520bd66c1a824115906193fb7750e3eb9446af174c0c3f928c3fdcbe74670fa` |
| `tests/unit/documents/test_two_layer_output.py` | `523dde5fd18c007951683021209cdda52582a9799d0a668ad8f02ebdaa5a7326` |
| `tests/unit/publication/test_analysis.py` | `2c56f56558c8d198ab74ad35c7e25a7c272966e373512a6471e6e244ab7eaf57` |
| `tests/unit/test_evaluation_activation.py` | `3fbaaa8fab08555bcac927dbcd45b1fa66340e102f8854ece6097eac888df805` |
| `tests/unit/test_evaluation_governance.py` | `fda9414c5d9209aeeb7f56876e278d2c361b140246a0a6defa887b3efe073993` |
| `tests/unit/test_foundry_30k.py` | `d3f6926496fc007acb149d71314fc75e778829449fac9358f5b8ff239093d8f6` |
| `tests/unit/test_foundry_approval.py` | `64eea6864e58e3e994bcceaa3a6fc112d87511d39c99a2c433af8a121c58e127` |
| `tests/unit/test_foundry_preflight.py` | `24ecffcf05f095acd2fc4d3e05397d24616ecb4e40d504a59289596758159e16` |
| `tests/unit/test_foundry_schema_probe.py` | `5b6b8cb0f01fb3bb331ec3cc9667fc2d603ffe6d5ac29194b2f91cee7ab83a3b` |
| `tests/unit/test_governance_migration.py` | `bf57b575f4787d946c082d24061e0eb7fee5863da8abe1c395e5144235e1afda` |
| `tests/unit/test_http_cleanup.py` | `20eb1dde61f036708e230137afc2d1dd82b2ef25154882c679e2882547346f0a` |
| `tests/unit/test_output_limit_diagnostics.py` | `14268b265efaf4034e14229874eb18c8c973624d98abad29f793db765b465e4e` |
| `tests/unit/test_security_entra.py` | `68ec1f2ace00aaa7a3d250ed502e670522fce938cf0d7b993b4fb8af355cb27b` |
| `tests/unit/test_settings_isolation.py` | `5fe8671135e01c19963b459b78a09bd664adf23243a4dc7b03f4590acc92e98f` |
| `tests/unit/test_single_call_diagnostics.py` | `6042eead59c04309aacb44e8774525a64672334ec13b910a2bd940a41b23fb3e` |
| `tests/unit/test_source_contracts.py` | `e081f9689b888f7f0c744acb8586b86385912ac0865134753160ac4aa559ab38` |
| `tests/unit/test_structured_provider.py` | `0886c3b6d3fe75d5b8ee1a8114ea28d1dec0fd4e5ab8765224f609f0af07345e` |

## 3. Isolation architecture and enforcement

Ordinary host pytest was never used. A public snapshot was constructed at
`/tmp/polymind-c1-final-20261101-dwon8fer/snapshot`, exclusively from
`git ls-files --cached --others --exclude-standard -z`, using current working-tree
bytes. All 414 allowed files copied; all 69 C1 members included. Each path was
checked for absolute/traversal components, symlink ancestors and nonregular type.
No symlinks or prohibited paths were encountered. No ignored/private directory
walk supplied snapshot content.

Copy exclusions cover `.git`, operator/cloud/SSH directories, real dotenv files,
private keys/certificates, signed JWT material, protected database extensions,
virtual environments and runtime caches. `.env.example` is public sample text.
No such excluded candidate appeared in the Git-visible input list. Content checks
also rejected private-key PEM markers or credential-shaped signed JWT material;
there was no rejection. Credentials and raw private inference responses were never
copied. The historical v3 text fixture is explicitly public synthetic source.

The preferred Docker image was inspected without pulling/building: the available
local PolyMind image ID is
`sha256:f81886ebfec049bab446be0513d2ee0c987561272f605bdf4c0506de3e29746c`.
It has no configured entrypoint and a default uvicorn API command; the dependency
probe explicitly replaced startup with Python, used `--pull=never --network=none
--read-only --cap-drop=ALL --security-opt=no-new-privileges`, nonroot UID 10001,
temporary `/tmp` and **no host mounts**. Python 3.10.22 and pytest 8.4.2 were present,
but PyJWT and cryptography were absent. Its image ID is the recorded local immutable
identity; no registry manifest verification is claimed. The probe's stopped
container is left untouched; no image/container pruning was performed.

The permitted equivalent fallback is **Bubblewrap with operating-system namespaces**,
using existing installed dependencies. Core flags are `--unshare-all`,
`--die-with-parent`, `--new-session`, `--cap-drop ALL`, `--clearenv`, a final
`--remount-ro /`, read-only snapshot/runtime/tool mounts, isolated `/proc`, minimal
`/dev`, and tmpfs `/tmp`. A bind under `/tmp/out` exposes only this task's disposable
external evidence directory. No original checkout, host home directory, Docker
socket, SSH agent, cloud config, approval directory or authority database is mounted.
Only the exact public Python installation prefixes are read-only runtime mounts;
they are separate from the source snapshot and expose no operator home/configuration.
`/usr`, `/lib`, `/lib64` and individual local Helm/Ruff binaries are read-only.

The probe observed a network namespace different from the host:
host `net:[4026531833]`, probe `net:[4026532416]`; the full session independently
reported `net:[4026532417]`. The namespace has **only loopback and no routes**.
All capability sets are zero; `NoNewPrivs: 1`; UID is nonroot 1000. Writes to both
snapshot and root were rejected with EROFS. Host repository and private home paths
were absent. Mountinfo, namespace IDs and `/proc` network evidence are retained
in `evidence/probe.json`; full session namespace is in `full-audit.json`.
Subprocesses inherit this isolation and cannot obtain external connectivity.

An explicitly loaded precollection pytest audit plugin additionally denies socket
connect/connect_ex/sendto and DNS APIs, uses CPython socket audit events, records
attempts even if swallowed, and fails the session if any are seen. **Observed main
pytest process network attempts: 0**, in both collection runs and the full run.
Fingerprint sessions also observed zero. A comprehensive native/subprocess syscall
attempt counter was not available: **external network attempts, across all processes:
NOT MEASURED**. This does not weaken namespace-level external network denial;
it limits the scope of the numeric observation. No successful cloud call occurred.

## 4. Offline test environment

No dependency was installed, upgraded or downloaded. Fallback Python is **3.10.13**,
pytest **8.4.2**. Key installed versions are Pydantic 2.13.4, pydantic-settings
2.14.1, requests 2.34.2, jsonschema 4.26.0, PyJWT 2.15.0, cryptography 50.0.2,
cffi 2.1.1, pycparser 3.0, pypdf 6.12.2, Redis client 6.4.0, httpx 0.28.1 and
FastAPI 0.136.3. Metadata checks covered **142 dependency names** from both public
requirements files; **141 satisfy their pins**, with the sole PyTorch build-suffix
difference described above. No GPU device or model cache is mounted; no model is
downloaded or instantiated for external inference.

`pyproject.toml`, repository Ruff configuration and pre-commit configuration are
absent. `pytest.ini` selects `tests`, with `-ra`. The existing CI workflow uses
Python 3.10, requirements, pytest and compileall; its network installation/build/
deployment-adjacent steps were not executed. The root README and both test/fixture
READMEs were reviewed alongside the four mandatory reports. Their defaults and
live/performance boundaries agree with observed collection.

The environment is constructed from an explicit allowlist, rather than inherited
host values. Protections include `PYTHONDONTWRITEBYTECODE=1`, `PYTHONNOUSERSITE=1`,
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`,
`PIP_NO_INDEX=1`, temporary HOME/XDG/HF/Torch/Helm paths and a public-snapshot
PYTHONPATH. Only the reviewed audit plugin is explicitly loaded; no async or other
third-party pytest plugin is required. The two installed Python `.pth` startup
hooks were reviewed: conditional coloredlogs installation and the setuptools
distutils shim; neither imports application settings or credentials here.

Application dotenv isolation remains the repository's root conftest adapter.
It supplies `_env_file=None` only when omitted for application Settings, retains
explicit synthetic dotenv tests and restores the public constructor on shutdown.
It neither supplies credentials nor bypasses security/governance validation.
The restricted root contains no real `.env`; the snapshot includes public
`pytest.ini` and all default fixtures.

## 5. Test safety classification

Classification was based on imports, fixture construction, transport substitutions,
subprocess bodies and main guards, not filenames alone.

| Group | Disposition and source-backed safety |
|---|---|
| A — safe offline units | All 1,286 unit cases executed. Contracts, fake providers, temporary stores/SQLite authorities, in-process ASGI clients and pure configuration checks. No live provider factory is activated. |
| B — safe offline integrations | All 524 integration cases executed, including local disposable Chroma and job/reliability subprocesses. Runtime authorities use tmp_path; subprocesses remain inside the same namespaces. |
| C — synthetic Foundry workflows | Included within A/B. `rig` replaces no-retry HTTP construction with OfflineHTTP; `composition` replaces requests.Session and local retrieval; OIDC fetch uses generated JWKs. `approval_signer` generates in-memory RSA keys and a new replay directory. Financial scopes, approvals and accounting are synthetic. |
| D — conditional dependencies | jsonschema and Redis-client importorskip branches were reviewed; both dependencies are present and execute. Helm-conditional tests have the preinstalled Helm binary mounted and execute local lint/template only. No dependency skip occurs. |
| E — unsafe live/operator-bound execution | Excluded from direct execution: Foundry L1/single-call live CLI entry points, actual trust/approval files, credentials, authorities and cloud authentication. No performance CLI was launched by the operator/audit. Modules are imported by tests only where reviewed fixtures contain their effects. |

Reviewed especially: `tests/conftest.py`, `settings_isolation.py`, `approval_helpers.py`,
the six named Foundry/single-call integration modules and `test_phase17hl_offline_e2e.py`,
plus `foundry_l1`, `foundry_single_call`, `foundry_approval` and `foundry_preflight`.
Harness imports define configuration/functions; they do not execute main guards.
Approval, identity and authority access happens inside invoked paths. Live-capable
function coverage is safe only through synthetic `rig`/`composition` fixtures.
CLI argument/exit tests set synthetic argv and intercept real transport/identity;
they do not submit an actual paid CLI request.

The reviewed real child-process test calls L1 **default offline mode**, without
`--live`, configuration or approval input; its script installs a pre-import socket
guard and uses synthetic HTTP. Other child scripts handle temporary job ledgers,
crash/restart tests, import-only checks or temporary settings projects. Helm
subprocesses only lint/render public chart files. No Kubernetes deployment is run.
Default collection contains **77 test modules, all under unit or integration**;
no additional offline default path is left unexecuted. Performance support imports
are not performance CLI execution.

## 6. Test execution matrix

Counts below are observed in retained logs, JUnit and the audit node/outcome lists.
The unit/integration breakdown is a partition of the single full run, not extra runs.

| Suite | Selected tests | Passed | Failed | Skipped | Errors | Exit status | Notes |
|---|---:|---:|---:|---:|---:|---|---|
| Initial default collection only | 1,787 collected before interruption | 0 | 0 | 0 | 1 | 2 | 14.69 s; username lookup environment error; no test body executed |
| Corrected default collection only | 1,810 | 0 | 0 | 0 | 0 | 0 | 9.55 s; identical source/selectors; no deselection |
| Full configured default offline suite | 1,810 | 1,810 | 0 | 0 | 0 | 0 | 141.92 s; one deprecation warning; xfail/xpass 0/0 |
| Unit partition of full run | 1,286 | 1,286 | 0 | 0 | 0 | parent 0 | Not an additional run |
| Integration partition of full run | 524 | 524 | 0 | 0 | 0 | parent 0 | Not an additional run |

Exact outer regression commands executed:

```sh
python /tmp/polymind-c1-final-20261101-dwon8fer/driver.py collect
python /tmp/polymind-c1-final-20261101-dwon8fer/driver.py collect2
python /tmp/polymind-c1-final-20261101-dwon8fer/driver.py full
```

The driver invokes Bubblewrap and the following exact pytest arguments. `PYTHON`
denotes the preinstalled Python 3.10.13 executable bound read-only at its installed
prefix; its resolved absolute path and every Bubblewrap/environment argument are
retained in `evidence/command-collect.json`, `command-collect2.json` and
`command-full.json`. No shell glob expands the selection.

```sh
"$PYTHON" -B -s -m pytest -q -c /workspace/pytest.ini \
  --basetemp=/tmp/pytest-collect -o cache_dir=/tmp/pytest-cache \
  -o junit_family=legacy --junitxml=/tmp/out/collect.xml \
  /workspace/tests --collect-only

"$PYTHON" -B -s -m pytest -q -c /workspace/pytest.ini \
  --basetemp=/tmp/pytest-collect2 -o cache_dir=/tmp/pytest-cache \
  -o junit_family=legacy --junitxml=/tmp/out/collect2.xml \
  /workspace/tests --collect-only

"$PYTHON" -B -s -m pytest -q -c /workspace/pytest.ini \
  --basetemp=/tmp/pytest-full -o cache_dir=/tmp/pytest-cache \
  -o junit_family=legacy --junitxml=/tmp/out/full.xml /workspace/tests
```

The correction only adds synthetic USER/LOGNAME and temporary Torch cache values
to the harness environment. The source snapshot, pytest options and assertions
remain unchanged. No failing test was retried or excluded: there were no failed
executed tests; only the explicitly documented collection rerun occurred.

All C1 test modules' coverage in that full run follows. Every listed case passed;
the remaining 625 cases cover pre-existing repository contracts outside C1 modules.

| C1 test module | Collected | Passed | Failed/skipped/errors |
|---|---:|---:|---:|
| `tests/integration/test_attempt3_serialization.py` | 7 | 7 | 0 |
| `tests/integration/test_final_offline_azure_compatibility.py` | 116 | 116 | 0 |
| `tests/integration/test_foundry_l1_entra.py` | 10 | 10 | 0 |
| `tests/integration/test_foundry_l1_launcher.py` | 26 | 26 | 0 |
| `tests/integration/test_foundry_offline_workflow.py` | 5 | 5 | 0 |
| `tests/integration/test_http_cleanup_governance.py` | 21 | 21 | 0 |
| `tests/integration/test_live_failure_observability.py` | 119 | 119 | 0 |
| `tests/integration/test_managed_digestion.py` | 11 | 11 | 0 |
| `tests/integration/test_output_limit_hardening.py` | 6 | 6 | 0 |
| `tests/integration/test_phase17hl_offline_e2e.py` | 31 | 31 | 0 |
| `tests/integration/test_single_call_harness.py` | 46 | 46 | 0 |
| `tests/integration/test_single_call_preflight.py` | 28 | 28 | 0 |
| `tests/integration/test_validation_diagnostics.py` | 25 | 25 | 0 |
| `tests/unit/documents/test_independent_json_limits.py` | 26 | 26 | 0 |
| `tests/unit/documents/test_managed_inference.py` | 49 | 49 | 0 |
| `tests/unit/documents/test_output_limit_sizes.py` | 8 | 8 | 0 |
| `tests/unit/documents/test_strict_schema_compatibility.py` | 13 | 13 | 0 |
| `tests/unit/documents/test_two_layer_output.py` | 81 | 81 | 0 |
| `tests/unit/publication/test_analysis.py` | 10 | 10 | 0 |
| `tests/unit/test_evaluation_activation.py` | 5 | 5 | 0 |
| `tests/unit/test_evaluation_governance.py` | 23 | 23 | 0 |
| `tests/unit/test_foundry_30k.py` | 26 | 26 | 0 |
| `tests/unit/test_foundry_approval.py` | 69 | 69 | 0 |
| `tests/unit/test_foundry_preflight.py` | 68 | 68 | 0 |
| `tests/unit/test_foundry_schema_probe.py` | 8 | 8 | 0 |
| `tests/unit/test_governance_migration.py` | 9 | 9 | 0 |
| `tests/unit/test_http_cleanup.py` | 56 | 56 | 0 |
| `tests/unit/test_output_limit_diagnostics.py` | 41 | 41 | 0 |
| `tests/unit/test_security_entra.py` | 96 | 96 | 0 |
| `tests/unit/test_settings_isolation.py` | 23 | 23 | 0 |
| `tests/unit/test_single_call_diagnostics.py` | 21 | 21 | 0 |
| `tests/unit/test_source_contracts.py` | 47 | 47 | 0 |
| `tests/unit/test_structured_provider.py` | 55 | 55 | 0 |

## 7. Targeted contract coverage

The groups overlap and must not be added. Counts represent complete selected
modules within the full run; test function examples identify inspected assertions,
not a claim of formal branch coverage. All parameterized instances execute.

| Component | Executed module-group cases | Meaningful assertion coverage |
|---|---:|---|
| A. JSON and serialization | 89 passed | `test_provider_boundary_and_unchanged_completion_request`, `test_canonical_boundary`, `test_raw_and_canonical_are_independent`, `test_utf8_and_envelope_bounds`; transport duplicate-key rejection in `test_invalid_transport_json`. Assertions distinguish raw UTF-8, canonical ASCII expansion, envelope and completion limits. |
| B. Strict structured output | 210 passed | `test_conversion_preserves_structure_and_does_not_mutate`, `test_unknown_constructs_fail_before_transport`, `test_complexity_and_references_fail_closed`, `test_subject_contract_matrix`, `test_exact_rendered_contract_and_unmodified_witness`. Closed objects, all required fields, unsupported constructs and structurally valid/domain-invalid output remain separate gates. |
| C. Managed digestion | 226 passed | `test_determinism_untrusted_boundary_and_usage`, `test_stale_execution_binding_fails_before_admission`, `test_explicit_v3_stage_configuration_rejected`, `test_active_v4_generation_contract`, `test_complete_pre_edit_generation_contract`, `test_historical_results_readable_but_requests_cannot_resume`. Checks cover claim IDs, evidence membership, source/child coverage, lineage, historical checkpoints and v4 binding. |
| D. HTTP errors and cleanup | 77 passed | `test_response_primary_precedence`, `test_active_error_identity_preserved`, `test_owned_session_precedence`, `test_adapter_retains_transport_error`, `test_single_call_cleanup_accounting_and_containment`, `test_owned_session_close_cannot_erase_settled_usage`. Original failures, output-limit priority, normalized transport and durable known/UNKNOWN usage are asserted. |
| E. Governance | 50 passed | `test_four_experiments_rolling_window_no_reset`, `test_unresolved_carries_across_months`, `test_substitution_denied`, `test_shared_provider_admission_cannot_be_replenished`, `test_activation_atomicity_and_history`, `test_history_backup_idempotency_and_four_call_admission`; harness settlement-failure tests add terminal containment. All authorities and migration backups are synthetic temporary state. |
| F. Entra and security | 177 passed | `test_rejected_claims_are_sanitized`, `test_delegated_identity_has_only_l1_permission`, `test_signed_untrusted_headers_rejected`, `test_signature_algorithm_and_key_confusion`, `test_jwks_readiness`, authority/API permission and revocation cases. Tenant issuer/audience, fixed scope/role, trusted JWKS, generic OIDC compatibility and fail-closed token behavior are exercised. |
| G. Foundry harness | 338 passed | `test_exact_one_call_and_accounting`, `test_http_session_no_retries`, `test_security_fails_before_reservation`, `test_replay_rejected_after_restart_and_concurrently`, `test_consumed_approval_cannot_authorize_another_directory`, `test_preflight_failure`, `test_real_offline_process_exit_status`. Explicit authorization, source/configuration/window bindings, replay, durable settlement, failure exits and complete synthetic pipeline behavior are covered. |
| H. Test infrastructure | 70 passed | `test_collection_isolation_and_shutdown_restoration`, `test_application_subclasses_inherit_isolation`, `test_unrelated_settings_models_keep_their_dotenv`, source-contract mutation/acceptance checks. Explicit synthetic dotenv inputs remain functional; implicit application dotenv is disabled before collection. `identity`, `entra` and `approval_signer` generate fresh in-memory test keys; no deployed key is read. |

Additional cross-boundary assertions in the 31-case offline E2E module validate
complete extraction/DAG/schema/digest/citation/accounting/reopen behavior, failed
digestion/Q&A exits, authorization/revocation and durable unknown/settled state.
The 26 signed-launcher and 10 Entra-launcher cases cover real composition through
intercepted transports. The 46 single-call harness and 28 preflight cases exercise
explicit source/approval/window gates, no implicit retries, durable failure and
terminal exit classification. These are included in the 1,810, not extra checks.

## 8. Regression failures and skip assessment

**Executed regression failures: 0. Final collection/setup errors: 0. Expected
skips: 0. Unexpected skips: 0. Unexecuted eligible default tests: 0.** All dependency-
conditional cases ran. No assertion was suppressed, weakened, xfailed or removed.

Initial collection error: `tests/unit/test_deployment_topology.py`, importing
`rag.ingest` → text splitters → sentence-transformers → transformers →
`torch._dynamo` → cache initialization → `getpass.getuser()`, raised
`KeyError: getpwuid(): uid not found: 1000`. This is a restricted-filesystem fixture
setup issue: host passwd/user records were deliberately not mounted. It is neither
a C1 assertion failure nor missing application dependency. The original invocation
returned 2 with 1,787 collected and one error before any test execution.

After source/trace inspection, the external harness set `USER=offline`,
`LOGNAME=offline`, `TORCHINDUCTOR_CACHE_DIR=/tmp/torchinductor` and
`TORCH_HOME=/tmp/torch`. No host account file or private path was exposed. Repeated
collection then found all 1,810 cases; the full unchanged suite passed. This cause
is resolved and does not block the commit gate. Original `collect.log/xml` and
`collect-audit.json` remain alongside the later results.

The full run's sole warning is OpenTelemetry's `SelectableGroups dict interface is
deprecated. Use select.` in
`tests/integration/test_publication_chroma.py::test_real_chroma_generation_and_selection_are_prefiltered`.
It is third-party deprecation debt, with no suppressed failure or missing test.
No pytest plugin rewrite warning, runtime authority failure or provider error
escaped the expected negative-test assertions.

## 9. Historical evidence reconciliation

| Historical evidence, not newly executed as its original session | Comparison with this audit |
|---|---|
| F1 HTTP cleanup: 1,755 passed | Current full suite has 1,810 passes, a net increase of 55. Both F1 modules execute: 56 unit and 21 integration cases; provider/usage/cleanup containment remains green. |
| managed-prompt/4: 447 distinct selected checks | All underlying permanent modules and current instances execute, including previously excluded synthetic signed-approval fixtures. The report documents 55 added cases, consistent with the 1,810 minus 1,755 collection difference. |
| Attempt 6 readiness: 108 distinct checks | Permanent source/subject/schema/history tests remain covered; the eight disposable historical readiness cases were not recreated or claimed rerun. Current permanent workflow/harness cases provide broader integration coverage. |
| Attempt 6 accepted paid analysis | Historical evidence only; no request, approval, real financial operation or acceptance simulation against an actual provider occurred. |

These counts are **not added together**. Original historical JUnit files at the
three explicitly named historical temporary locations are unavailable in this
environment. Therefore exact historical node-by-node additions/removals cannot
be independently proved from those unavailable logs. The +55 agrees with the
v4 report's explicit additions, and no required permanent test was found removed,
but that agreement is source/report reconciliation, not recovered historical
execution evidence. The current 77-module collection and all passing node IDs are
directly observed. It supplies stronger current-tree, signed-synthetic and
OS-isolated evidence than those selected runs, while not certifying live model
behavior or any unavailable one-off synthetic assertion.

## 10. Managed-prompt/4 and frozen-contract integrity

**PASS.** All four active StageProfiles use managed-prompt/4. Actual adapter
configuration and provider schema recompute to the historical v4 values.
The v4 fixture pins current `managed.py` bytes to
`fa6cd701b73c0cdd486b645a64748f3bb70509b17d310b40c9455c619dbc91a9`.
Chunk/structural/root request-generation-payload witnesses match; intermediate
has behavioral rendering/acceptance coverage rather than an invented golden.

Historical managed-prompt/3 source remains
`5b272d4a7591692eeeb328da09bc39b35d402bebd1d8ada3b891f6b1d6e8928c`.
Its nine frozen complete request/generation/payload checks pass through the
checksum-gated test-only historical module. Domain model declarations and
validation predicates/order pass fixed-source token comparisons and mutation
tests; diagnostic metadata does not erase new executable predicates. Structurally
valid nonfact subjects still fail domain validation, and null factual subjects
remain allowed. Active stale labels/settings/executor bindings are rejected;
historical synthetic results/checkpoints remain readable under original evidence.

| Frozen C1 fixture | Unchanged SHA-256 |
|---|---|
| `tests/fixtures/digestion_contracts/managed_prompt3.py.txt` | `5b272d4a7591692eeeb328da09bc39b35d402bebd1d8ada3b891f6b1d6e8928c` |
| `tests/fixtures/digestion_contracts/managed_prompt4.json` | `b0caa2e2a701b7e43ab54b1df19d73bf0a3d57f0b6419f10bfb403afa659ea94` |
| `tests/fixtures/digestion_contracts/managed_prompt4_subject.txt` | `3583382755184d562e4cc6c2c42b1df9c1fd8d10c117891be68fab6d858641bb` |
| `tests/fixtures/digestion_contracts/models.py.txt` | `83783aadde2ecae7616fa6ffd934da3eb396a76c17e0d5f05b573510f690be08` |
| `tests/fixtures/digestion_contracts/validation.py.txt` | `da9cef97360d51a512dcff0d6e09405faf349db427daae141e3460aa2562f031` |

The inactive proposal patch remains byte-identical, SHA-256
`e96c2e784ea587f12f49ef4f64ce82229e296a821107bab8f84b7db165900201`,
matching the documentation-remediation preservation value. It was not applied.
No fixture or checksum was regenerated. Original runtime, tests and fixtures
retain their pre-task hashes.

## 11. Source fingerprint verification

| Binding | Before, isolated runtime recomputation, and after | Verdict |
|---|---|---|
| Executor source | `d9af24e556305246ec145d15b3511e3e65fcf4e955e5b5f0dc550b4119b58a75` | MATCH |
| Generation contract source | `74cf9320b0ebf6d45df531e81827c5a8710b5b4d58fa75aad05dfa5039552290` | MATCH |
| Strict provider schema | `4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2` | MATCH |
| Managed strict inference configuration | `71adc072da8e99d47b81afa859e78bde4866e633ae0e841e0b17f48d6450b831` | MATCH |

Initial original/snapshot source hashes used the repository's **actual digest
function bodies**, AST-extracted without application imports: `executor_digest`,
`generation_contract_digest` and their existing canonical JSON `digest` helper.
The algorithm/path membership was not substituted. Isolated before/after runtime
calculations then invoked the actual imported repository functions, the actual
strict schema converter and `ManagedSynthesisInference.config`, with settings
isolation and render-only PreparationProvider identity. No transport/authority
constructor or private configuration was needed. All three calculations agree.

Executor coverage is all Python under documents, governance, security, llm and
tests/performance; generation coverage is its explicit twelve-file inventory.
Provider schema and settings source preservation are therefore backed by both
matching source inputs and actual safe runtime calculations. The private complete
launch-configuration digest was not read/recomputed; it is different from the
public inference-configuration fingerprint and cannot be inferred from it.

## 12. Ruff and formatting assessment

**Ruff: REVIEW REQUIRED; not PASS.** Ruff **0.16.1**, no cache, fixes or formatting
writes. The exact manifest supplies 64 pending Python files: 18 modified tracked
and 46 new. Read-only command families executed inside the isolated namespace:

```sh
/tools/ruff check --no-cache --output-format=json <exact pending Python manifest>
/tools/ruff check --no-cache --output-format=json <18 modified tracked paths>
/tools/ruff check --no-cache --output-format=json <46 new Python paths>
/tools/ruff format --check --no-cache <exact pending Python manifest>
```

HEAD checks run the 18 tracked paths against public HEAD object bytes in a separate
read-only `/head` tree. Exact expanded argument arrays are in `lint-commands.json`
and `head-lint.log`; `--show-settings --no-cache` also records resolved settings.
`ruff format --check` is a read-only diagnostic; no unqualified formatter/write
mode, automatic fix, black or isort write was used.

| Read-only diagnostic | Observed | Exit | Historical reconciliation |
|---|---:|---:|---|
| Pending 64 Python files | 324 findings | 1 | Matches 324 |
| Modified tracked 18 Python files | 93 findings | 1 | Matches 93 |
| Same tracked paths at HEAD, complete package context | 82 findings | 1 | Matches 82 |
| New 46 Python files | 231 findings | 1 | Matches 231 |
| Formatting check | 52 would reformat, 12 already formatted | 1 | Matches historical 52 |

An initial HEAD-only extraction containing just the 18 files reported 90 findings.
Investigation found incomplete first-party package context affecting eight I001
classifications. Completing `/head` with all 283 public tracked HEAD files produced
82, without changing any bytes or Ruff options. Both diagnostics are retained;
82 is the valid like-for-like baseline, not a concealed source fix.

Ignoring line shifts, a multiset comparison by file/rule/message identifies
**14 added and three removed findings in tracked files, net +11**. The additions
are two BLE001 cleanup catches, six UP045 annotations, two C408 test literals,
one C408 provider test literal, one RUF059 unused test unpack, one SIM114 branch
and one SIM102 nested condition. All 231 new-file findings are current pending
debt; they cannot be attributed to HEAD. Total pending rules:
BLE001 18, I001 51, C408 75, TRY004 1, FURB157 3, DTZ007 1, B023 3,
SIM102 2, SIM114 1, UP035 4, UP045 22, UP006 2, F401 31, SIM117 1,
S110 2, F811 37, B017 14, RUF012 2, RUF059 48, F841 1, DTZ011 1,
B008 1, PLR0402 1 and PLR0133 2.

Correctness/security/test-reliability review found no demonstrated commit-blocking
defect among these findings:

| Finding family | Review and disposition |
|---|---|
| BLE001/S110 | Provider/governance cleanup preserves original errors and records accounting failure; security normalization fails closed; preflight diagnostics cannot override original failures. Negative/cleanup/settlement tests pass. Existing silent readiness/diagnostic catches remain operational diagnosability debt. |
| B023, three closures | Governance `unsettled` is consumed synchronously inside the current loop iteration and is itself invariant; Foundry-envelope capture/data callbacks are invoked under each current synchronous patch before the next iteration. No escaping deferred callback found. The governance finding is already present at HEAD. |
| F401/F811, 68 | Mainly pytest fixture imports reused through test arguments; retaining those imports is necessary for fixture discovery. Other unused imports are cleanup debt. No undefined-name finding appears. |
| B017, 14 | Broad exception expectations in negative tests reduce precision; surrounding no-provider/no-marker/state assertions and dedicated precise-category tests provide independent controls. Test reliability review debt remains. |
| RUF012/B008/F841 | Synthetic response headers/class defaults and a frozen InferenceUsage default, plus an unused local whose constructor initializes a temporary admission DB. Reviewed within isolated fixture lifetime; no production shared-secret state found. |
| I/UP/C408/SIM/FURB/date/constants/unused variables | Import ordering, modern annotations, literals, simplification and test cleanup; the naive date is a date-only validation step. No security boundary or financial arithmetic change is required to address these styles. |

No automatic mass formatting is recommended as part of this fingerprint-preserving
gate. Operator review/acceptance or a separately scoped correction task is the
remaining lint condition. Any later source change requires a fresh fingerprint and
appropriate regression/approval review.

Isolated `compileall.compile_dir('/workspace', quiet=1)` passed with
`sys.pycache_prefix=/tmp/compile-cache`; no checkout bytecode was written.
`git diff --check` passed. No Docker build, Compose runtime, Helm deployment or
Kubernetes operation was needed or performed; only local Helm test rendering ran.

## 13. Security and governance invariants

The application/provider-neutral boundary is preserved: application/RAG/orchestration
uses inference contracts; Azure schema and transport behavior stay in llm/provider
infrastructure. External vLLM remains external. Existing provider/API/streaming
tests pass; upstream SSE is not exposed as a new application contract. This audit
changes no endpoint, routing, memory or configuration behavior.

No Azure CLI, login, token exchange, API-key validation, HTTP provider request,
production deployment or paid inference was performed. Real operator keys,
signed JWT payloads, approval files, credential directories and protected financial
databases were never opened. No actual authority reservation, settlement, migration
or replay state was read or mutated. Synthetic RSA and approval consumption occur
only in the isolated temporary fixtures explicitly allowed by this task.

Fresh test authorities and disposable SQLite ledgers exercise actual admission,
reservation, known settlement, UNKNOWN obligations, failed settlement containment,
explicit evaluation policy binding and migration rollback. Source/configuration
hash gates run before real authority/approval boundaries; stale generation/executor
substitution tests pass. Entra tenant-specific issuer/audience, delegated scope and
role, fixed JWKS anchors, algorithm/signature rejection and SecurityAuthority
authorization remain enforced. Generic OIDC serialization compatibility also passes.

Separate pre-commit review checked the manifest/public snapshot for sensitive path
types, private PEM/JWT markers, accidental credentials, debug/temp artifacts,
dependency changes, stale task additions and API changes. Sensitive-looking literals
reviewed in tests are explicitly synthetic sentinels, fake bearer material, generated
keys or public deployment allowlists. The two new artifacts contain no raw response,
credential, private payload, actual approval identity or executable staging command.
Existing implementation changes remain the operator's C1 review scope; no new
engineering code, dependency or runtime configuration was introduced by this audit.

## 14. Original repository preservation

**PASS.** All **414 pre-existing Git-visible files** and the 414 snapshot files
match their captured hashes; all **69 C1 members**, all five contract fixtures and
the historical proposal patch are byte-identical. Both source digests match after
all test/lint/runtime fingerprint activity. Source modifications: **0**.
Test/fixture modifications: **0**. Existing documentation modifications by this
task: **0**. Only the required report and normalized prompt are added.

The original repository was not mounted into the test environment. Test caches,
SQLite state, signing material, subprocess projects and output are confined to
disposable `/tmp`; no test-created artifact was added to the checkout. Final
Git-visible inventory differs from the initial one only by those two Markdown
paths. Branch/HEAD, index entries and raw index bytes match the baseline; staged
paths remain empty. No restore/reset/clean was needed or used.

This preservation statement covers the original public Git-visible content and
index directly. Private ignored contents were deliberately not read or hashed;
their protection follows the absence of any original/private mounts and the lack
of any host-side private-state operation, not a fabricated private database hash.
No commit or push occurred.

## 15. C1 commit-readiness gate

| Criterion | Decision |
|---|---|
| Required isolation | PASS: namespace/filesystem/credential enforcement verified |
| Full eligible offline test coverage | PASS: 1,810/1,810, zero final failures/errors/skips |
| C1 membership and dependencies | PASS: exact 69 members; no engineering dependency assigned only to C2 |
| Active/frozen contracts and source bindings | PASS: runtime/schema/settings/source calculations and frozen assertions match |
| Original repository/index preservation | PASS: hashes and exact inventory delta verified |
| Security/governance containment | PASS within offline synthetic scope; no real authority accessible |
| Lint/format | REVIEW REQUIRED: 324 findings; no demonstrated severe defect; explicit operator disposition needed |
| Exact pinned runtime build | LIMITATION: installed torch 2.12.0 differs from CPU pin 2.12.0+cpu |
| Paid/live/full Phase 17H validation | OUTSIDE THIS GATE; remains unvalidated beyond historical one-call evidence |

**CONDITIONALLY READY for manual local engineering commit review.** There is no
current regression failure requiring C1 rejection and no isolation/dependency blocker
that prevented the eligible suite from executing. The operator can assess the full
passing evidence while explicitly accepting the bounded dependency-build evidence
and remaining lint debt. This is not an assertion that Ruff is clean or the exact
CPU-pinned environment was verified. No staging or commit is performed or authorized
automatically. Recommended action: review the exact C1 inventory and lint disposition,
decide whether these two limitations are acceptable for a local engineering commit,
then stage/commit manually only after that decision. If exact CPU-build certification
is mandatory, retain the gate pending a separately provided offline pinned runtime.

## 16. Remaining engineering risks

The PyTorch build mismatch prevents an exact CPU-runtime qualification; these
tests use synthetic model behavior rather than real model execution. Passing
inference-boundary tests do not prove ML binary equivalence, future model output
compliance, Azure billing, semantic quality or representative workload reliability.

Ruff debt includes negative-test precision and diagnostic catch concerns as well
as style; it is preserved for review. No broad exception is declared universally
safe solely because a test passed. No branch/coverage instrumentation was added,
and the module mapping is assertion-based scope evidence rather than a numeric
line-coverage claim. Native/child network attempts are not comprehensively counted,
although OS-level external isolation applies to all processes.

Historical one-off readiness tests and original historical JUnit node inventories
are unavailable and not rerun. Frozen historical source is executed only by its
existing checksum-protected synthetic fixture. Source/profile changes made after
this report invalidate the exact fingerprint/byte-preservation conclusion and
require renewed verification. The `/tmp` evidence is disposable; this permanent
report preserves results/inventory, not an assurance of indefinite log retention.

Full live L1 reductions, complete live digestion/publication/retrieval/Q&A,
independent semantic review and production/distributed readiness remain outside
this engineering commit gate. No next major phase was started.

## 17. Updated Git inventory and C1/C2 classification

Final pending files: **158 = 25 modified tracked + 133 untracked**. **C1 stays 69**,
with exact membership and hashes in section 2. **C2 becomes 89**: the prior exact
87-member documentation/configuration-example inventory plus:

| New artifact | Classification |
|---|---|
| `docs/codex/reports/phase_17hl_c1_final_isolated_offline_regression.md` | C2 |
| `docs/codex/prompts/phase_17hl_c1_final_isolated_offline_regression.md` | C2 |

No implementation file is reassigned. Staged files: **0**. Branch and HEAD remain
the baseline. The final file-level status and tracked diff statistics follow;
untracked Markdown additions are counted in inventory but do not appear in
ordinary tracked `git diff --stat`.

```text
 M .env.example
 M README.md
 M deployment/helm/polymind/README.md
 M docs/evaluation/phase_17h.md
 M docs/security/phase_17g.md
 M docs/security/production-security.md
 M docs/security/threat-model.md
 M documents/digestion/codec.py
 M documents/digestion/managed.py
 M documents/digestion/models.py
 M documents/digestion/validation.py
 M documents/publication/analysis.py
 M governance/execution.py
 M governance/ledger.py
 M llm/bounded_http.py
 M llm/inference.py
 M llm/ollama_client.py
 M llm/openai_compatible.py
 M llm/structured.py
 M security/identity.py
 M security/runtime.py
 M tests/integration/test_managed_digestion.py
 M tests/unit/documents/test_managed_inference.py
 M tests/unit/publication/test_analysis.py
 M tests/unit/test_structured_provider.py
?? docs/adr/phase_17hl_application_owned_identifiers_assessment.md
?? docs/codex/prompts/phase_17h_live_preflight.md
?? docs/codex/prompts/phase_17hl_ast_test_portability_fix.md
?? docs/codex/prompts/phase_17hl_attempt5_final_readiness_and_operator_preparation.md
?? docs/codex/prompts/phase_17hl_attempt5_operator_authorization_and_single_call_execution.md
?? docs/codex/prompts/phase_17hl_attempt5_readiness_authorization_assessment.md
?? docs/codex/prompts/phase_17hl_c1_final_isolated_offline_regression.md
?? docs/codex/prompts/phase_17hl_diagnostic_hardening.md
?? docs/codex/prompts/phase_17hl_documentation_remediation_and_readme_sync.md
?? docs/codex/prompts/phase_17hl_entra_v2.md
?? docs/codex/prompts/phase_17hl_f1_http_cleanup_failure_preservation.md
?? docs/codex/prompts/phase_17hl_final_handoff.md
?? docs/codex/prompts/phase_17hl_final_offline_azure_compatibility_audit.md
?? docs/codex/prompts/phase_17hl_first_failure_diagnosis.md
?? docs/codex/prompts/phase_17hl_full_suite_configuration_isolation.md
?? docs/codex/prompts/phase_17hl_l1_attempt3_serialization.md
?? docs/codex/prompts/phase_17hl_live_execution_preparation.md
?? docs/codex/prompts/phase_17hl_live_failure_observability_and_contract_options.md
?? docs/codex/prompts/phase_17hl_managed_prompt4_subject_contract_implementation.md
?? docs/codex/prompts/phase_17hl_offline_e2e_contract_verification.md
?? docs/codex/prompts/phase_17hl_offline_readiness.md
?? docs/codex/prompts/phase_17hl_operator_approval.md
?? docs/codex/prompts/phase_17hl_preflight_observability_timing_hardening.md
?? docs/codex/prompts/phase_17hl_regression_reconciliation.md
?? docs/codex/prompts/phase_17hl_reusable_evaluation_governance.md
?? docs/codex/prompts/phase_17hl_same_day_attempt2.md
?? docs/codex/prompts/phase_17hl_second_attempt_preparation.md
?? docs/codex/prompts/phase_17hl_structured_output_compatibility.md
?? docs/codex/prompts/phase_17hl_two_layer_structured_output.md
?? docs/codex/proposals/managed_prompt_4.patch
?? docs/codex/proposals/phase_17hl_generation_instruction_clarifications.md
?? docs/codex/reports/phase_17h_live_preflight.md
?? docs/codex/reports/phase_17hl_ast_test_portability_fix.md
?? docs/codex/reports/phase_17hl_attempt5_final_readiness_and_operator_preparation.md
?? docs/codex/reports/phase_17hl_attempt5_live_execution_report.md
?? docs/codex/reports/phase_17hl_attempt5_operator_authorization_and_single_call_execution.md
?? docs/codex/reports/phase_17hl_attempt5_operator_checklist_verification.md
?? docs/codex/reports/phase_17hl_attempt5_post_execution_diagnostics.md
?? docs/codex/reports/phase_17hl_attempt5_readiness_authorization_assessment.md
?? docs/codex/reports/phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md
?? docs/codex/reports/phase_17hl_attempt6_offline_integration_readiness.md
?? docs/codex/reports/phase_17hl_azure_strict_schema_live_compatibility.md
?? docs/codex/reports/phase_17hl_c1_final_isolated_offline_regression.md
?? docs/codex/reports/phase_17hl_diagnostic_hardening.md
?? docs/codex/reports/phase_17hl_documentation_remediation_and_readme_sync.md
?? docs/codex/reports/phase_17hl_entra_v2_report.md
?? docs/codex/reports/phase_17hl_evaluation_activation_readiness.md
?? docs/codex/reports/phase_17hl_evaluation_policy_activation.md
?? docs/codex/reports/phase_17hl_f1_http_cleanup_failure_preservation.md
?? docs/codex/reports/phase_17hl_final_offline_azure_compatibility_audit.md
?? docs/codex/reports/phase_17hl_final_operator_authorization.md
?? docs/codex/reports/phase_17hl_first_failure_diagnosis.md
?? docs/codex/reports/phase_17hl_full_suite_configuration_isolation.md
?? docs/codex/reports/phase_17hl_independent_json_byte_limits.md
?? docs/codex/reports/phase_17hl_l1_attempt3_preparation.md
?? docs/codex/reports/phase_17hl_l1_attempt3_serialization_root_cause.md
?? docs/codex/reports/phase_17hl_launch_authorization_final.md
?? docs/codex/reports/phase_17hl_live_execution_preparation.md
?? docs/codex/reports/phase_17hl_live_failure_observability_and_contract_options.md
?? docs/codex/reports/phase_17hl_managed_prompt4_subject_contract_implementation.md
?? docs/codex/reports/phase_17hl_offline_e2e_contract_verification.md
?? docs/codex/reports/phase_17hl_operator_approval_report.md
?? docs/codex/reports/phase_17hl_output_limit_hardening.md
?? docs/codex/reports/phase_17hl_preflight_observability_timing_hardening.md
?? docs/codex/reports/phase_17hl_regression_reconciliation.md
?? docs/codex/reports/phase_17hl_reusable_evaluation_governance.md
?? docs/codex/reports/phase_17hl_same_day_attempt2_handoff.md
?? docs/codex/reports/phase_17hl_second_attempt_preparation.md
?? docs/codex/reports/phase_17hl_single_call_execution_failure_diagnosis.md
?? docs/codex/reports/phase_17hl_single_call_harness_offline.md
?? docs/codex/reports/phase_17hl_structured_output_compatibility.md
?? docs/codex/reports/phase_17hl_two_layer_structured_output.md
?? docs/engineering/llm_structured_output_validation.md
?? docs/engineering/postmortems/Estudio_PolyMind_Phase17HL_L1_Three_Attempts_Postmortem_2026-10-16.md
?? docs/evaluation/phase_17h_foundry_approval.template.json
?? docs/evaluation/phase_17h_foundry_validation.md
?? docs/evaluation/phase_17hl_operator_approval.md
?? docs/governance/evaluation-binding.template.json
?? docs/governance/evaluation-policy.md
?? docs/security/entra_v2.md
?? documents/digestion/diagnostics.py
?? governance/evaluation.py
?? governance/migration.py
?? llm/azure_schema.py
?? tests/README.md
?? tests/approval_helpers.py
?? tests/conftest.py
?? tests/fixtures/digestion_contracts/README.md
?? tests/fixtures/digestion_contracts/managed_prompt3.py.txt
?? tests/fixtures/digestion_contracts/managed_prompt4.json
?? tests/fixtures/digestion_contracts/managed_prompt4_subject.txt
?? tests/fixtures/digestion_contracts/models.py.txt
?? tests/fixtures/digestion_contracts/validation.py.txt
?? tests/integration/test_attempt3_serialization.py
?? tests/integration/test_final_offline_azure_compatibility.py
?? tests/integration/test_foundry_l1_entra.py
?? tests/integration/test_foundry_l1_launcher.py
?? tests/integration/test_foundry_offline_workflow.py
?? tests/integration/test_http_cleanup_governance.py
?? tests/integration/test_live_failure_observability.py
?? tests/integration/test_output_limit_hardening.py
?? tests/integration/test_phase17hl_offline_e2e.py
?? tests/integration/test_single_call_harness.py
?? tests/integration/test_single_call_preflight.py
?? tests/integration/test_validation_diagnostics.py
?? tests/performance/foundry_approval.py
?? tests/performance/foundry_budget.py
?? tests/performance/foundry_envelopes.py
?? tests/performance/foundry_l1.py
?? tests/performance/foundry_preflight.py
?? tests/performance/foundry_recalibration.py
?? tests/performance/foundry_schema_diagnostics.py
?? tests/performance/foundry_schema_probe.py
?? tests/performance/foundry_single_call.py
?? tests/settings_isolation.py
?? tests/source_contracts.py
?? tests/unit/documents/test_independent_json_limits.py
?? tests/unit/documents/test_output_limit_sizes.py
?? tests/unit/documents/test_strict_schema_compatibility.py
?? tests/unit/documents/test_two_layer_output.py
?? tests/unit/test_evaluation_activation.py
?? tests/unit/test_evaluation_governance.py
?? tests/unit/test_foundry_30k.py
?? tests/unit/test_foundry_approval.py
?? tests/unit/test_foundry_preflight.py
?? tests/unit/test_foundry_schema_probe.py
?? tests/unit/test_governance_migration.py
?? tests/unit/test_http_cleanup.py
?? tests/unit/test_output_limit_diagnostics.py
?? tests/unit/test_security_entra.py
?? tests/unit/test_settings_isolation.py
?? tests/unit/test_single_call_diagnostics.py
?? tests/unit/test_source_contracts.py
```

```text
 .env.example                                   |   5 +
 README.md                                      |  66 ++++++++--
 deployment/helm/polymind/README.md             |  12 +-
 docs/evaluation/phase_17h.md                   |   7 ++
 docs/security/phase_17g.md                     |  15 ++-
 docs/security/production-security.md           |  16 ++-
 docs/security/threat-model.md                  |  11 ++
 documents/digestion/codec.py                   |  52 +++++++-
 documents/digestion/managed.py                 |  76 ++++++++++--
 documents/digestion/models.py                  |  41 +++++-
 documents/digestion/validation.py              | 165 +++++++++++++++++++++----
 documents/publication/analysis.py              |   7 +-
 governance/execution.py                        |  28 ++++-
 governance/ledger.py                           |  74 ++++++++++-
 llm/bounded_http.py                            |  75 +++++++++--
 llm/inference.py                               |  18 +++
 llm/ollama_client.py                           |  16 ++-
 llm/openai_compatible.py                       |  95 ++++++++++++--
 llm/structured.py                              |  82 +++++++++++-
 security/identity.py                           |  61 ++++++++-
 security/runtime.py                            |   5 +-
 tests/integration/test_managed_digestion.py    |  10 ++
 tests/unit/documents/test_managed_inference.py | 117 ++++++++++++++++++
 tests/unit/publication/test_analysis.py        |   3 +
 tests/unit/test_structured_provider.py         |  43 +++++++
 25 files changed, 1001 insertions(+), 99 deletions(-)
```

## 18. Final safety attestation

Isolation PASS; full eligible suite PASS; managed-prompt/4 and frozen contracts
PASS; source/index/public repository preservation PASS. Comprehensive external
network-attempt count NOT MEASURED; main pytest audited attempts **0**. Actual
cloud inference calls **0**; paid requests **0**; cloud authentication **0**;
real signing/approval operations **0**; protected financial mutations **0**.
Only disposable synthetic signing and accounting occurred inside isolation.

No source/test/fixture edit, active configuration change, patch application,
dependency installation, Docker pull/build, deployment, Git staging/history/ref
mutation, commit or push occurred. **Commits: 0. Pushes: 0.** The only repository
additions are this C2 report and its C2 normalized prompt. C1 remains uncommitted
for independent operator review. Execution COMPLETE and commit CONDITIONALLY
READY are distinct conclusions.
